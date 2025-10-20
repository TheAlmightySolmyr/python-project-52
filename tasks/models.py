from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        verbose_name='Исполнитель'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'