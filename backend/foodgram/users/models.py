from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_me

MAX_EMAIL_LENGTH = 254
MAX_FIELDS_LENGTH = 150


class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(unique=True,
                              max_length=MAX_EMAIL_LENGTH,
                              verbose_name='Электронная почта')
    username = models.CharField(unique=True,
                                max_length=MAX_FIELDS_LENGTH,
                                verbose_name='Имя пользователя',
                                validators=[
                                    UnicodeUsernameValidator(),
                                    validate_me
                                ])
    first_name = models.CharField(max_length=MAX_FIELDS_LENGTH,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=MAX_FIELDS_LENGTH,
                                 verbose_name='Фамилия')
    password = models.CharField(max_length=MAX_FIELDS_LENGTH,
                                verbose_name='Пароль')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(User,
                             related_name='follower',
                             verbose_name='Подписчик',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               related_name='following',
                               verbose_name='Автор',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'Подписчик: {self.user} - автор {self.author}'

    def clean(self):
        if self.user == self.author:
            raise ValidationError("Вы не можете подписаться на самого себя")
