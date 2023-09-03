from django.db import models
import uuid
from accounts.models import User
from datetime import date

# Create your models here.
class Group(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, related_name='group', on_delete=models.CASCADE)
    
    name        = models.CharField(max_length=255)
    color       = models.CharField(default="#9c82f7", max_length=20)
    
    def __str__(self):
        return self.name
      
class Task(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(User, related_name='task', on_delete=models.CASCADE)
    
    title       = models.CharField(max_length=255)
    status      = models.CharField(max_length=100, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)
    deadline    = models.DateField(default=date.today)
    group       = models.ForeignKey(Group, related_name='task', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created_at',)

