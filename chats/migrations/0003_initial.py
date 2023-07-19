# Generated by Django 4.2.2 on 2023-07-19 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chats", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="messagereaders",
            name="user",
            field=models.ForeignKey(
                help_text="Пользователь, который прочитал сообщение",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="chat",
            field=models.ForeignKey(
                help_text="Чат, к которому относится сообщение",
                on_delete=django.db.models.deletion.CASCADE,
                to="chats.chat",
                verbose_name="Чат",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="responding_to",
            field=models.ForeignKey(
                blank=True,
                help_text="Ответ на другое сообщение",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="chats.message",
                verbose_name="Ответ на другое сообщение",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                help_text="Отправитель сообщения",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Отправитель сообщения",
            ),
        ),
        migrations.AddField(
            model_name="chatmembers",
            name="chat",
            field=models.ForeignKey(
                help_text="Чат, в котором участвует пользователь",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members_info",
                to="chats.chat",
                verbose_name="Чат",
            ),
        ),
        migrations.AddField(
            model_name="chatmembers",
            name="member",
            field=models.ForeignKey(
                help_text="Может просматривать и отправлять сообщения в чате",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chats_info",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Участник чата",
            ),
        ),
        migrations.AddField(
            model_name="chat",
            name="members",
            field=models.ManyToManyField(
                help_text="Кто может просматривать и отправлять сообщения в чате",
                related_name="chats",
                through="chats.ChatMembers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Участники",
            ),
        ),
        migrations.AddField(
            model_name="attachment",
            name="message",
            field=models.ForeignKey(
                help_text="Сообщение, к которому относится вложение",
                on_delete=django.db.models.deletion.CASCADE,
                to="chats.message",
                verbose_name="Сообщение",
            ),
        ),
        migrations.AddConstraint(
            model_name="message",
            constraint=models.UniqueConstraint(
                fields=("text", "sender", "chat"), name="уникальное сообщение"
            ),
        ),
        migrations.AddConstraint(
            model_name="chatmembers",
            constraint=models.UniqueConstraint(
                fields=("chat", "member"), name="уникальные участники"
            ),
        ),
    ]
