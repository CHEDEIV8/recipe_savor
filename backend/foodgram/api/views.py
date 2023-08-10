# from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status

from api.serializers import (IngredientSerializer,
                             TagSerializer,
                             UserFollowSerializer)
from recipes.models import Ingredient, Tag
from users.models import Follow
from .filters import IngredientFilter

User = get_user_model()


class TagViewSet(RetrieveModelMixin,
                 ListModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(RetrieveModelMixin,
                        ListModelMixin,
                        GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
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
