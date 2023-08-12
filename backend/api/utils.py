from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.serializers import RecipeMinSerializer
from recipes.models import Recipe


def handle_action(request, pk, relation, error_message, serializer):
    """
    Создает обработчик для пары действий POST и DELETE
    на основе переданных параметров.
    """

    user = request.user
    recipe = get_object_or_404(Recipe, pk=pk)
    relation_set = getattr(recipe, relation)

    if request.method == 'POST':
        if relation_set.contains(user):
            raise ValidationError(error_message)
        relation_set.add(user)
    elif request.method == 'DELETE':
        if not relation_set.contains(user):
            raise ValidationError(error_message)
        relation_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = RecipeMinSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
