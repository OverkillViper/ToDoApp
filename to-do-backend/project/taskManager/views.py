from django.shortcuts import render
from django.http import JsonResponse
from .serializers import TaskSerializer, GroupSerializer
from .models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

# Create your views here.
@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({
        'data' : serializer.data
    })


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupUpdateView(APIView):
    def put(self, request, id):
        try:
            group = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupCreateView(APIView):
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDeleteView(APIView):
    def delete(self, request, id):
        try:
            group = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskGroupNameView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            group_id = task.group_id
            group = Group.objects.get(id=group_id)
            group_name = group.name
            return Response({"group_name": group_name})
        except (Task.DoesNotExist, Group.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class TaskGroupColorView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            group_id = task.group_id
            group = Group.objects.get(id=group_id)
            group_color = group.color
            return Response({"group_color": group_color})
        except (Task.DoesNotExist, Group.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class TaskGroupItemCountView(APIView):
    def get(self, request, group_id):
        try:
            tasks = Task.objects.all().filter(group_id=group_id)
            group_item_count = tasks.count()
            return Response({"group_item_count": group_item_count})
        except (Task.DoesNotExist, Group.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class TasksByGroupView(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return Task.objects.filter(group_id=group_id)

class GroupDetailView(APIView):
    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        serializer = GroupSerializer(group)
        return Response(serializer.data)


class TaskChangeStatusView(APIView):
    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskUpdateView(APIView):
    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PUT':
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteView(APIView):
    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PendingTasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(status='pending')
    serializer_class = TaskSerializer

class CompletedTasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(status='complete')
    serializer_class = TaskSerializer

class TodaysTasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deadline=timezone.now().date(), status='pending')
    serializer_class = TaskSerializer