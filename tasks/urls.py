from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name="tasks"),
    path('lists', views.TaskListView.as_view(), name="lists"),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name="task"),
    path('my-tasks', views.TaskDetailView.as_view(), name="my-tasks"),
    path('task-create', views.TaskDetailView.as_view(), name="task-create"),
    path('task-update/<int:pk>', views.TaskDetailView.as_view(), name="task-update"),
    path('task-delete/<int:pk>', views.TaskDetailView.as_view(), name="task-delete"),
    path('task-comment-create/<int:pk>', views.TaskDetailView.as_view(), name="task-comment-create"),
]

