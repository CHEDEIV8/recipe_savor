# Generated by Django 4.2.4 on 2023-08-08 15:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(db_table='recipe_favorite', related_name='favorited', to=settings.AUTH_USER_MODEL, verbose_name='Избранное пользователя'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='shoppingcart',
            field=models.ManyToManyField(db_table='recipe_shoppingcart', related_name='shoppingcart', to=settings.AUTH_USER_MODEL, verbose_name='Покупки пользователя'),
        ),
    ]
