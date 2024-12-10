# tasks/urls.py
from django.urls import path
from .views import admin, user

urlpatterns = [
    path('tasks/', admin.task_list, name='task_list'),
    path('tasks/create/', admin.task_create, name='task_create'),
    path('tasks/<int:pk>/', admin.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', admin.task_delete, name='task_delete'),
    path('tasks/batch-delete/', admin.task_batch_delete, name='task_batch_delete'),
    path('tasks/restore-last-deleted/', admin.restore_last_deleted_task, name='restore_last_deleted_task'),
    path('subscribe/', user.subscribe_to_reports, name='subscribe_to_report'),
    path('unsubscribe/', user.unsubscribe_from_reports, name='unsubscribe_from_report'),
]
