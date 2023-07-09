from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.text import slugify

from core.models import DateCreatedModel, DateEditedModel

User = get_user_model()


class Chat(DateCreatedModel, DateEditedModel):
    '''Модель чата'''
    title = models.CharField(
        max_length=255,
        verbose_name='Название чата',
        help_text='Придумайте название чату',
        blank=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        max_length=100,
        blank=False
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='own_chats',
        verbose_name='Создатель',
        null=True
    )
    is_private = models.BooleanField(
        default=True
    )
    password = models.CharField(
        max_length=128,
        verbose_name='Пароль чата',
        help_text='Добавьте к чату пароль',
        blank=True
    )
    allow_anonymous_access = models.BooleanField(
        default=False
    )
    members = models.ManyToManyField(
        User,
        through='Members',
        verbose_name='Участники',
        help_text='Добавьте в чат участников',
        related_name='chats',
    )

    def __str__(self) -> str:
        if self.private:
            return f'Приватный чат `{self.title}`'
        return f'Открытый чат `{self.title}`'

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        if self.password:
            self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Members(DateCreatedModel):
    '''Модель участников чата'''
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='members_info',
        verbose_name='Чат'
    )
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats_info',
        verbose_name='Участник чата'
    )
    chat_is_pinned = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        constraints = [
            models.UniqueConstraint(
                fields=['chat', 'member'],
                name='уникальные участники'
            )
        ]
