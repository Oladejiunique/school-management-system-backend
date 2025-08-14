from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, StudentViewSet,
    RequestPasswordResetView, ValidateResetTokenView, ResetPasswordConfirmView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/password-reset-request/', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('auth/password-reset-validate/', ValidateResetTokenView.as_view(), name='password-reset-validate'),
    path('auth/password-reset-confirm/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),
]
