"""Файл административных настроек для приложения users."""

import datetime as dt

from django.contrib import admin

from .models import City, Language, User


class LanguageInlineAdmin(admin.TabularInline):
    model = User.foreign_languages.through


@admin.register(User)
class AdvUserAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'email',
        '_age',
        'country',
        'city',
        'native_language',
        '_foreign_languages',
        'date_joined'
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'country',
        'native_language__name',
        'city__name'
    )
    fields = (
        ('username', 'email', 'slug'),
        ('first_name'),
        ('country', 'native_language'),
        ('birthdate', 'age_is_hidden'),
        ('gender', 'gender_is_hidden'),
        ('phone_number'),
        ('city'),
        ('is_staff', 'is_superuser'),
        ('date_joined')
    )
    inlines = (LanguageInlineAdmin,)

    def _age(self, obj):
        """Возраст пользователя."""
        if obj.birthdate:
            age_days = (dt.datetime.now().date() - obj.birthdate).days
            return int(age_days / 365)
        return None

    _age.short_description = 'Возраст'

    def _foreign_languages(self, obj):
        """Изучаемые языки пользователя."""
        return ", ".join(
            [str(language) for language in obj.foreign_languages.all()]
        )

    _foreign_languages.short_description = 'Изучаемые языки'


admin.site.register(City)
admin.site.register(Language)
