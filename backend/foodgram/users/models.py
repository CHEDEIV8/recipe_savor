from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


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
                name='uniqe_follow'
                )
            ]

    def __str__(self):
        return f'Подписчик: {self.user.username} - автор {self.author.username}'

    def clean(self):
        if self.user == self.author:
            raise ValidationError("Вы не можете подписаться на самого себя")
