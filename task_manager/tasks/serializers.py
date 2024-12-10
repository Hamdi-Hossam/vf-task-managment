# tasks/serializers.py
from rest_framework import serializers
from .models import Task, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'start_date', 'due_date', 'completion_date', 'status', 'user', 'created_at', 'deleted_at']

        def validate(self, data):
            if data['due_date'] <= data['start_date']:
                raise serializers.ValidationError("Due date must be after start date.")
            if data.get('completion_date') and data['completion_date'] < data['start_date']:
                raise serializers.ValidationError("Completion date cannot be before start date.")
            return data

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['start_date', 'frequency', 'report_time']

    def validate_start_date(self, value):
        if value.minute != 0 or value.second != 0:
            raise serializers.ValidationError("start_date must have valid hours (00 to 23) with no minutes or seconds.")
        return value

    def validate_report_time(self, value):
        if not (0 <= value <= 11):
            raise serializers.ValidationError("report_time must be an hour between 00 and 11.")
        return value