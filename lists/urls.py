from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListsView.as_view(), name="lists"),
    path('new', views.CreateListView.as_view(), name="new_list"),
    path('<int:pk>', views.TaskListView.as_view(), name="list"),
    path('<int:list_pk>/<int:task_pk>', views.TaskDetailView.as_view(), name="task"),
    path('my-tasks', views.MyTasksView.as_view(), name="my-tasks"),
]
