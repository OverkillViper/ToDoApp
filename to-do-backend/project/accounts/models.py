from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import AccountManager
from django.utils import timezone
import uuid

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email           = models.EmailField(unique=True, blank=True, default='')
    name            = models.CharField(default="", max_length=255, blank=True)
    avatar          = models.ImageField(upload_to='avatars', blank=True, null=True)

    is_active       = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)

    date_joined     = models.DateTimeField(default=timezone.now)
    last_login      = models.DateTimeField(blank=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_avatar(self):
        if self.avatar:
            return 'https://todoapp-infx.onrender.com' + self.avatar.url
        else:
            return 'https://picsum.photos/200/200'
        
    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email