from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from lists.models import Task, TaskComment, TaskList


#####################
####### LISTS #######
#####################
class TaskListsView(ListView):
    model = TaskList
    template_name = "lists/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lists"] = TaskList.objects.all()
        return context


class TaskListView(ListView):
    template_name = "lists/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = TaskList.objects.get(id=self.kwargs["id"])
        return context

    def get_queryset(self):
        return Task.objects.filter(task_list=self.kwargs["id"])


class CreateListView(CreateView):
    model = TaskList
    fields = ["title", "description", "participants"]
    template_name = "lists/create_list.html"
    success_url = reverse_lazy("lists")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.participants.add(self.request.user)
        return super().form_valid(form)


class EditListView(View):
    template = "lists/edit_list.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login")

        task_list = TaskList.objects.get(id=pk)
        if request.user != task_list.owner:
            return redirect("lists")

        return render(request, self.template, {"task_list": task_list})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login")

        task_list = TaskList.objects.get(id=pk)
        if request.user != task_list.owner:
            return redirect("lists")

        task_list.title = request.POST.get("title")
        task_list.description = request.POST.get("description")
        task_list.participants.set(request.POST.getlist("participants"))
        task_list.save()
        return redirect("lists")


class DeleteListView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login")

        task_list = TaskList.objects.get(id=pk)
        if request.user != task_list.owner:
            return redirect("lists")

        task_list.delete()
        return redirect("lists")


#####################
####### TASKS #######
#####################


class MyTasksView(View):
    template = "tasks/my_tasks.html"  # TODO

    def get(self, request):
        task_lists = TaskList.objects.filter(participants=request.user)
        tasks = Task.objects.filter(task_list__in=task_lists).filter(assigned_to=request.user)
        for task_list in task_lists:
            task_list.tasks = tasks.filter(task_list=task_list)

        return render(request, self.template, {"task_lists": task_lists})


class TaskDetailView(View):
    template = "tasks/task_detail.html"

    def get(self, request, list_id, task_id):
        task = Task.objects.get(id=task_id)
        comments = TaskComment.objects.filter(task=task)
        return render(request, self.template, {"task": task, 'comments': comments})

    def post(self, request):
        # TODO
        pass

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        task.delete()
        return redirect("lists")

    def put(self, request):
        """ Update the task """
        # TODO
        pass


class CreateTaskView(CreateView):
    model = Task
    fields = ["title", "description", "assigned_to", "due_datetime", "attachment", "priority"]
    template_name = "tasks/create_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = TaskList.objects.get(id=self.kwargs["list_id"])
        return context

    def form_valid(self, form):
        form.instance.task_list = TaskList.objects.get(id=self.kwargs["list_id"])
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list", kwargs={"id": self.kwargs["list_id"]})

    # Also add the task to the task_list, after it is created
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            task_list = TaskList.objects.get(id=self.kwargs["list_id"])
            task_list.tasks.add(self.object)
            task_list.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class EditTaskView(View):
    template = "tasks/edit_task.html"  # TODO

    def get(self, request, list_id, task_id):
        task = Task.objects.get(id=task_id)
        return render(request, self.template, {"task": task})

    def post(self, request, list_id, task_id):
        task = Task.objects.get(id=task_id)
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.assigned_to = request.POST.get("assigned_to")
        task.due_datetime = request.POST.get("due_datetime")
        task.save()
        return redirect("list", id=list_id)


class DeleteTaskView(View):
    def get(self, request, list_id, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect("list", id=list_id)


class CompleteTaskView(View):
    def get(self, request, list_id, task_id):
        if not request.user.is_authenticated:
            return redirect("login")

        # Only the user assignee can complete the task
        if request.user != Task.objects.get(id=task_id).assigned_to:
            return redirect("list", id=list_id)

        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return redirect("list", id=list_id)


#####################
##### COMMENTS ######
#####################

class AddCommentView(View):
    model = TaskComment

    def post(self, request, list_id, task_id):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.POST.get("comment") or not request.POST.get("comment").strip():
            return redirect("task", list_id=list_id, task_id=task_id)

        task = Task.objects.get(id=task_id)
        comment = TaskComment.objects.create(
            comment=request.POST.get("comment"),
            task=task,
            user=request.user,
        )
        comment.save()
        return redirect("task", list_id=list_id, task_id=task_id)
