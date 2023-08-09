from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    TagViewSet,
    IngredientViewSet,
    CustomUserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet, basename='tag')
router_v1.register(r'ingrediens', IngredientViewSet, basename='ingredient')
router_v1.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]