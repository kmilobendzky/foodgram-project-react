from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow_user',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow_following',
        verbose_name='Подписан на'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following',],
                name='Подписчик и объект подписки должны быть уникальными',
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.following}'   