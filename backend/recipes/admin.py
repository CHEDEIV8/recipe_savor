from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
    list_filter = ('name',)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorite')
    list_filter = ('name', 'author', 'tags')
    inlines = (IngredientInRecipeInline,)

    @admin.display(description='Добавления в избранные')
    def count_favorite(self, instance):
        return instance.favorite.count()


@admin.register(Recipe.shoppingcart.through)
class ShoppingCart(admin.ModelAdmin):
    list_display = ('recipe', 'user')
