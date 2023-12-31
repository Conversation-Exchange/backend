"""Маршруты приложения users."""

from django.urls import include, path

from rest_framework import routers

from users.routers import CustomRouter
from users.views import (CountryViewSet, GoalViewSet, InterestViewSet,
                         LanguageViewSet, UserViewSet)

router_user = CustomRouter()
router = routers.DefaultRouter()

router_user.register('users', UserViewSet, basename='users')

router.register('languages', LanguageViewSet, basename='languages')
router.register('countries', CountryViewSet, basename='countries')
router.register('interests', InterestViewSet, basename='interests')
router.register('goals', GoalViewSet, basename='goals')

router_user._urls = [
    url for url in router_user.urls
    if not any(
        url.name.endswith(bad) for bad in [
            'set-username', 'reset-username', 'reset-username-confirm',
            'users-activation', 'users-resend-activation',
            'users-reset-password', 'users-reset-password-confirm',
        ]
    )
]

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('accounts/', include('allauth.urls')),
    path('', include(router_user.urls)),
    path('', include(router.urls)),
]
