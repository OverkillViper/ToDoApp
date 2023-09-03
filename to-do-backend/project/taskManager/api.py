from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import TaskSerializer, GroupSerializer
from .models import *
from accounts.models import User
from .forms import TaskForm, GroupForm
from django.utils import timezone

@api_view(['GET'])
def all_task_list(request):
    tasks = Task.objects.all().filter(user=request.user)

    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def pending_task_list(request):
    tasks = Task.objects.all().filter(user=request.user, status='pending')

    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def completed_task_list(request):
    tasks = Task.objects.all().filter(user=request.user, status='complete')

    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def todays_task_list(request):
    tasks = Task.objects.all().filter(user=request.user, status='pending', deadline=timezone.now().date())

    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def create_task(request):
    data = request.data
    
    form = TaskForm(request.data)
    
    if form.is_valid():
        task = form.save(commit=False)
        group = Group.objects.get(id=request.data['groupID'])
        task.user   = request.user
        task.group  = group
        task.save()
        
        serializer = TaskSerializer(task)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'The form is not valid'})

@api_view(['POST'])
def update_task(request, id):

    task = Task.objects.get(id=id)
    group = Group.objects.get(id=request.data['groupID'])
    task.title = request.data['title']
    task.group = group
    task.deadline = request.data['deadline']
    task.save()
    
    return JsonResponse({'message':'Task updated'})
    
@api_view(['DELETE'])
def delete_task(request, id):
    task = Task.objects.filter(user=request.user).get(id=id)
    task.delete()
    
    return JsonResponse({'message':'task deleted'})

@api_view(['POST'])
def mark_task_complete(request, id):
    task        = Task.objects.get(id=id)
    task.status = 'complete'
    task.save()
    
    return JsonResponse({'message': 'Task marked as completed'})

@api_view(['POST'])
def mark_task_pending(request, id):
    task        = Task.objects.get(id=id)
    task.status = 'pending'
    task.save()
    
    return JsonResponse({'message': 'Task marked as pending'})

@api_view(['GET'])
def group_list(request):
    groups  = Group.objects.all().filter(user=request.user)

    serializer = GroupSerializer(groups, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def create_group(request):
    data = request.data
    
    form = GroupForm(request.data)
    
    if form.is_valid():
        group = form.save(commit=False)
        group.user   = request.user
        group.save()
        
        serializer = GroupSerializer(group)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'The form is not valid'})

@api_view(['POST'])
def update_group(request, id):

    group = Group.objects.get(id=id)
    group.name = request.data['name']
    group.color = request.data['color']

    group.save()
    
    return JsonResponse({'message':'Group updated'})

@api_view(['DELETE'])
def delete_group(request, id):
    group = Group.objects.filter(user=request.user).get(id=id)
    group.delete()
    
    return JsonResponse({'message':'group deleted'})
