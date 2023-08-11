# from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.filters import IngredientFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeMinSerializer,
                             RecipeReadSerializer, RecipeWriteSerializer,
                             TagSerializer, UserFollowSerializer)
from api.utils import handle_action
from recipes.models import Ingredient, Recipe, Tag
from users.models import Follow

User = get_user_model()


class TagViewSet(RetrieveModelMixin,
                 ListModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(RetrieveModelMixin,
                        ListModelMixin,
                        GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class CustomUserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']

    @action(detail=False, serializer_class=UserFollowSerializer)
    def subscriptions(self, request):
        followed_user = User.objects.filter(
            following__user=request.user
        )

        page = self.paginate_queryset(followed_user)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(followed_user, many=True)
        return Response(serializer.data)

    @action(methods=['post'],
            detail=True,
            serializer_class=UserFollowSerializer)
    def subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, pk=id)
        if Follow.objects.filter(author=following, user=user).exists():
            raise ValidationError('Подписка уже сушествует')
        if user == following:
            raise ValidationError('Вы не можете подписаться на самого себя')
        Follow.objects.create(author=following, user=request.user)
        serializer = self.get_serializer(following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        follow = Follow.objects.filter(author=author, user=user)
        if not follow.exists():
            raise ValidationError('Подписка не существует')
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params

        is_favorited = query_params.get('is_favorited')
        if is_favorited == '1':
            queryset = queryset.filter(favorite=self.request.user)

        is_in_shopping_cart = query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(shoppingcart=self.request.user)

        author = query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author=author)

        tags = query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        return queryset

    @action(methods=['post', 'delete'],
            detail=True,
            serializer_class=RecipeMinSerializer)
    def shopping_cart(self, request, pk):
        return handle_action(
            request=request,
            pk=pk,
            relation='shoppingcart',
            error_message='Рецепт отсутствует в списке покупок',
            serializer=self.serializer_class
        )

    @action(methods=['post', 'delete'],
            detail=True,
            serializer_class=RecipeMinSerializer)
    def favorite(self, request, pk):
        return handle_action(
            request=request,
            pk=pk,
            relation='favorite',
            error_message='Рецепт отсутствует в списке избранных',
            serializer=self.serializer_class
        )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        recipes_in_shopping_cart = Recipe.objects.filter(
            shoppingcart=request.user).values('id')
        recipe_ingredients = Ingredient.objects.filter(
            recipe__id__in=recipes_in_shopping_cart
        ).annotate(total_count=Sum('ingredientinrecipe__amount'))

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=shopping_cart'
        response.writelines('Игредиенты для покупок by FoodGram:\n\n')
        response.writelines(f'{i.name}: {i.total_count}'
                            f'{i.measurement_unit}\n'
                            for i in recipe_ingredients)
        return response
