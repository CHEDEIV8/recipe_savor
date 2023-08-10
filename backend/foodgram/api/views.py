# from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.serializers import (IngredientSerializer,
                             TagSerializer,
                             UserFollowSerializer,
                             RecipeReadSerializer,
                             RecipeWriteSerializer,
                             RecipeMinSerializer)
from recipes.models import Ingredient, Tag, Recipe
from users.models import Follow
from api.permissions import IsAuthorOrReadOnly
from .filters import IngredientFilter

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
            queryset = queryset.filter(tags__slug__in=tags)

        return queryset

    @action(methods=['post'],
            detail=True,
            serializer_class=RecipeMinSerializer)
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.shoppingcart.contains(user):
            raise ValidationError('Рецепт уже есть в списке покупок')
        recipe.shoppingcart.add(user)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def shoping_cart_delete(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not recipe.shoppingcart.contains(user):
            raise ValidationError('Рецепт отсутствует в списке покупок')
        recipe.shoppingcart.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'],
            detail=True,
            serializer_class=RecipeMinSerializer)
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.favorite.contains(user):
            raise ValidationError('Рецепт уже есть в списке избранных')
        recipe.favorite.add(user)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not recipe.favorite.contains(user):
            raise ValidationError('Рецепт отсутствует в списке избранных')
        recipe.favorite.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
