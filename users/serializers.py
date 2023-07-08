import datetime as dt

from djoser.serializers import UserSerializer as DjoserSerializer
from rest_framework import serializers

from users.models import City, User, UserLanguage


class CityNameField(serializers.RelatedField):
    """Кастомное поле, позволяющее делать update
    города по id и получать его строковое
    название при GET-запросе."""
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return City.objects.get(id=data)


class UserLanguageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='language.id')
    language = serializers.ReadOnlyField(source='language.name')

    class Meta:
        model = UserLanguage
        fields = (
            'id',
            'language',
            'skill_level'
        )

class UserSerializer(DjoserSerializer):
    """Сериализатор для модели пользователя."""
    age = serializers.SerializerMethodField()
    native_language = serializers.StringRelatedField()
    city = CityNameField(queryset=City.objects.all())
    foreign_languages = UserLanguageSerializer(
        source='user',
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'age',
            'country',
            'city',
            'birthdate',
            'native_language',
            'foreign_languages',
            'gender',
            'phone_number',
            )

    def get_age(self, obj):
        """Вычисляем возраст пользователя."""
        if obj.birthdate:
            age_days = (dt.datetime.now().date() - obj.birthdate).days
            return int(age_days / 365)
        return

    def create_foreign_languages(self, user, foreign_languages):
        """Создание объектов в промежуточной таблице."""
        for language in foreign_languages:
            UserLanguage.objects.create(
                user=user,
                language_id=language.get('id'),
                skill_level=language.get('skill_level')
            )

    def to_internal_value(self, data):
        request = self.context.get('request', None)
        if request.method == 'POST':
            return super().to_internal_value(data)
        elif request.method == 'PATCH':
            # другая логика работы метода, т.к. при update появляются M2M-связи
            if 'foreign_languages' in data:
                foreign_languages = data.pop('foreign_languages')
                result = super().to_internal_value(data)
                result['foreign_languages'] = foreign_languages
                return result
            else:
                return super().to_internal_value(data)

    def update(self, instance, validated_data):
        """Кастомные метод update, учитывающий through-таблицу"""
        if 'foreign_languages' in validated_data:
            UserLanguage.objects.filter(user=instance).delete()
            self.create_foreign_languages(
                user=instance,
                foreign_languages=validated_data.pop('foreign_languages')
            )
            super().update(instance, validated_data)
            return instance
        else:
            return super().update(instance, validated_data)



