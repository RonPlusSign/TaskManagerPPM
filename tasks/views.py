from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from tasks.models import Task


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    ordering = ["-due_datetime"]
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context


class TaskDetailView(View):
    template = "task_detail.html"

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        return render(request, self.template, {"task": task})

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        task.done = not task.done
        task.save()
        return render(request, self.template, {"task": task})

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        task.delete()
        return redirect("tasks")

    def put(self, request, pk):
        """ Toggle the task status """

        task = Task.objects.get(id=pk)
        task.done = not task.done
        task.save()
        return redirect("tasks")
