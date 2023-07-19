# Generated by Django 4.2.2 on 2023-07-19 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="city",
            field=models.ForeignKey(
                blank=True,
                help_text="Город проживания пользователя",
                max_length=255,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="users_in_this_city",
                to="users.city",
                verbose_name="Город проживания",
            ),
        ),
    ]
