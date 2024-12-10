from django.db import models
from users.models import CustomUser

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    completion_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )

    user = models.OneToOneField(CustomUser, related_name='subscription', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    report_time = models.IntegerField()

    def __str__(self):
        return f"{self.user.email} - {self.frequency} subscription"