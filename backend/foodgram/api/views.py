# from django.shortcuts import render
from django.db.models import Count

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import (IngredientSerializer,
                             TagSerializer,
                             UserFollowSerializer)
from recipes.models import Ingredient, Tag

User = get_user_model()


class TagViewSet(RetrieveModelMixin,
                 ListModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(RetrieveModelMixin,
                        ListModelMixin,
                        GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CustomUserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']

    @action(detail=False, serializer_class=UserFollowSerializer)
    def subscriptions(self, request):
        followed_user = User.objects.filter(
            following__user=request.user
        ).annotate(recipes_count=Count('recipes')).order_by('-id')

        page = self.paginate_queryset(followed_user)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(followed_user, many=True)
        return Response(serializer.data)
