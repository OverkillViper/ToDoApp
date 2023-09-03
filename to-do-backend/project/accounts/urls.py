from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

urlpatterns = [
    path('signup/', api.signup, name='signup'),
    path('me/', api.me, name='me'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('password-recover/', api.password_recover, name='password-recover'),
    path('password-reset/', api.reset_password, name='password-reset'),
    path('check-password/', api.check_user_password, name='password-check'),
    path('change-password/', api.change_password, name='password-change'),
    path('delete-user/', api.delete_user, name='user-delete'),
    path('upload-avatar/', api.upload_avatar, name='avatar-upload'),
    path('change-username/', api.change_username, name='username-change'),
]