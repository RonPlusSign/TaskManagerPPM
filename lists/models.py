from django.contrib.auth.models import User
from django.db import models


class TaskList(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    participants = models.ManyToManyField(User, related_name="participants")
    tasks = models.ManyToManyField("Task", related_name="tasks")

    def __str__(self):
        return self.title


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    due_datetime = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_to")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    attachment = models.FileField(upload_to="media/", null=True, blank=True)

    priority = models.CharField(choices=Priority.choices, max_length=6, null=True, blank=True, default=None)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="task_list")

    def __str__(self):
        return self.title


class TaskComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
