from django.urls import path

from . import views

urlpatterns = [
    # Lists
    path('', views.TaskListsView.as_view(), name="lists"),
    path('<int:id>', views.TaskListView.as_view(), name="list"),
    path('new', views.CreateListView.as_view(), name="list_new"),
    path('<int:id>/edit', views.EditListView.as_view(), name="list_edit"),
    path('<int:id>/delete', views.DeleteListView.as_view(), name="list_delete"),

    # Tasks
    path('my-lists', views.MyTasksView.as_view(), name="my-tasks"),
    path('<int:list_id>/<int:task_id>', views.TaskDetailView.as_view(), name="task"),
    path('<int:list_id>/new', views.CreateTaskView.as_view(), name="task_new"),
    path('<int:list_id>/<int:task_id>/edit', views.EditTaskView.as_view(), name="task_edit"),
    path('<int:list_id>/<int:task_id>/delete', views.DeleteTaskView.as_view(), name="task_delete"),
]
