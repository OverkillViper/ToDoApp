from django.forms import ModelForm

from .models import *

class TaskForm(ModelForm):
    
    class Meta:
        model = Task
        fields = ('title', 'deadline',)
        
class GroupForm(ModelForm):
    
    class Meta:
        model = Group
        fields = ('name', 'color',)

