"""View-функции приложения users."""

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User


@extend_schema(tags=['Users'])
class UserViewSet(DjoserViewSet):
    """Вьюсет модели пользователя."""

    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country', 'gender')

    @action(
        methods=('PATCH',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=None
    )
    def hide_show_age(self, request):
        """Метод для отображения/скрытия возраста."""
        user = request.user
        user.age_is_hidden = 1 if not user.age_is_hidden else 0
        request.user.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=('PATCH',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=None
    )
    def hide_show_gender(self, request):
        """Метод для отображения/скрытия пола."""
        user = request.user
        user.gender_is_hidden = 1 if not user.gender_is_hidden else 0
        request.user.save()
        return Response(status=status.HTTP_200_OK)
