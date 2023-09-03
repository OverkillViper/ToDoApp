from rest_framework import serializers
from .models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'user', 'name', 'color')
        
class TaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateField(format='%Y-%m-%d')
    group = GroupSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'status', 'created_at', 'deadline', 'user', 'group')