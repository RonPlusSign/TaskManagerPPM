from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from lists.models import Task, TaskList


class TaskListsView(ListView):
    model = TaskList
    template_name = "tasks/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lists"] = TaskList.objects.all()
        return context


class TaskListView(ListView):
    template_name = "tasks/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = TaskList.objects.get(id=self.kwargs["pk"])
        return context

    def get_queryset(self):
        return Task.objects.filter(task_list=self.kwargs["pk"])


class TaskDetailView(View):
    template = "task_detail.html"

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        return render(request, self.template, {"task": task})

    def post(self, request):
        pass

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        task.delete()
        return redirect("lists")

    def put(self, request):
        """ Update the task """
        pass


class MyTasksView(View):
    template = "tasks/my_tasks.html"

    def get(self, request):
        task_lists = TaskList.objects.filter(participants=request.user)
        tasks = Task.objects.filter(task_list__in=task_lists).filter(assigned_to=request.user)
        for task_list in task_lists:
            task_list.tasks = tasks.filter(task_list=task_list)

        return render(request, self.template, {"task_lists": task_lists})


class CreateListView(CreateView):
    model = TaskList
    fields = ["title", "description", "participants"]
    template_name = "tasks/create_list.html"
    success_url = reverse_lazy("lists")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
