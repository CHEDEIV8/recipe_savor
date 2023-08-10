from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from users.models import User

MAX_LENGTH_TAG_NAME = 200
MAX_LENGTH_TAG_SLUG = 200
MAX_LENGTH_TAG_HEX_COLOR = 7

MAX_LENGTH_INGREDIENT_NAME = 200
MAX_LENGTH_INGREDIENT_MU = 200

MAX_LENGTH_RECIPE_NAME = 200


class Ingredient(models.Model):
    """Модель ингредиентов для рецептов"""

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
    """Модель тегов для рецептов"""

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
    """Модель рецептов"""

    name = models.CharField(max_length=MAX_LENGTH_RECIPE_NAME,
                            verbose_name='Название рецепта')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тэги',
                                  related_name='recipes',
                                  blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         verbose_name='Список ингредиентов')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1, 'Время должно быть не меньше 1 минуты'
            )
        ]
    )
    favorite = models.ManyToManyField(
        User,
        verbose_name='Избранное пользователя',
        related_name='favorited',
        db_table='recipe_favorite',
        blank=True)

    shoppingcart = models.ManyToManyField(
        User,
        verbose_name='Покупки пользователя',
        related_name='shoppingcart',
        db_table='recipe_shoppingcart',
        blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов не может быть меньше 1'
            )
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингрединт к рецепту'
        verbose_name_plural = 'Ингрединты к рецепту'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.recipe.name}: {self.ingredient.name} - '
            f'{self.amount} {self.ingredient.measurement_unit}'
        )
