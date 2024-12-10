# tasks/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..models import Task
from ..serializers import TaskSerializer
from users.permissions import IsAdmin
from django.utils.timezone import now


@api_view(['POST'])
@permission_classes([IsAdmin])
def task_create(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdmin])
def task_list(request):
    if request.method == 'GET':
        
        Task.objects.filter(
            user=request.user,
            status='pending',
            due_date__lt=now(),
            deleted_at__isnull=True
        ).update(status='overdue')

        tasks = Task.objects.filter(user=request.user, deleted_at__isnull=True)

        # Apply status filter
        status_filter = request.GET.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)

        # Apply date range filter
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            tasks = tasks.filter(due_date__range=[start_date, end_date])

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdmin])
def task_update(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
def task_delete(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        task.deleted_at = timezone.now()
        task.save()
        return Response({'detail': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
def task_batch_delete(request):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    if not start_date or not end_date:
        return Response({'detail': 'Start date and end date are required.'}, status=status.HTTP_400_BAD_REQUEST)

    tasks = Task.objects.filter(user=request.user, start_date__range=[start_date, end_date], deleted_at__isnull=True)

    # Mark tasks as deleted
    tasks.update(deleted_at=timezone.now())

    return Response({'detail': f'{tasks.count()} tasks deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAdmin])
def restore_last_deleted_task(request):
    try:
        task = Task.objects.filter(user=request.user, deleted_at__isnull=False).latest('deleted_at')
    except Task.DoesNotExist:
        return Response({'detail': 'No deleted tasks found.'}, status=status.HTTP_404_NOT_FOUND)

    task.deleted_at = None
    task.save()

    return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
