from django.core.validators import RegexValidator
from django.db import models

MAX_LENGTH_TAG_NAME = 200
MAX_LENGTH_TAG_SLUG = 200
MAX_LENGTH_TAG_HEX_COLOR = 7

MAX_LENGTH_INGREDIENT_NAME = 200
MAX_LENGTH_INGREDIENT_MU = 200


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_INGREDIENT_NAME,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_INGREDIENT_MU,
        verbose_name='Еденица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_TAG_NAME,
                            verbose_name='Название',
                            unique=True)
    color = models.CharField(max_length=MAX_LENGTH_TAG_HEX_COLOR,
                             verbose_name='Цвет',
                             unique=True,
                             validators=[
                                 RegexValidator(
                                     regex=r'#[0-9a-fA-F]{6}\Z',
                                     message='Введите верное HEX значение'
                                 )
                             ])
    slug = models.SlugField(max_length=MAX_LENGTH_TAG_SLUG,
                            verbose_name='Слаг',
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    pass
