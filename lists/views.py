from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from lists.models import Task, TaskComment, TaskList


def set_message(request, message):
    """ Set a message in the session """
    request.session["message"] = message


def get_message(request):
    """ Get a message from the session """
    message = None
    if "message" in request.session:
        message = request.session["message"]
        del request.session["message"]
    return message if message else None


#####################
####### LISTS #######
#####################
class TaskListsView(LoginRequiredMixin, ListView):
    model = TaskList
    template_name = "lists/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lists"] = TaskList.objects.filter(participants=self.request.user.id)
        context["message"] = get_message(self.request)
        return context


class TaskListView(LoginRequiredMixin, ListView):
    template_name = "lists/task_list.html"

    def get(self, request, *args, **kwargs):
        task_list = TaskList.objects.get(id=self.kwargs["id"])
        if request.user not in task_list.participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = get_message(self.request)
        context['task_list'] = TaskList.objects.get(id=self.kwargs["id"])
        return context

    def get_queryset(self):
        return Task.objects.filter(task_list=self.kwargs["id"])


class CreateListView(LoginRequiredMixin, CreateView):
    model = TaskList
    fields = ["title", "description", "participants"]
    template_name = "lists/create_list.html"
    success_url = reverse_lazy("lists")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.owner = self.request.user
            task_list = form.save()

            # Add the user as owner and participant
            task_list.participants.add(self.request.user)
            task_list.save()
            return redirect("lists")
        else:
            return self.form_invalid(form)


class EditListView(LoginRequiredMixin, UpdateView):
    model = TaskList
    fields = ["title", "description", "participants"]
    template_name = "lists/edit_list.html"
    success_url = reverse_lazy("lists")

    def get(self, request, *args, **kwargs):
        task_list = TaskList.objects.get(id=kwargs["pk"])
        if request.user != task_list.owner:
            set_message(request, "You are not the owner of this list.")
            return redirect("lists")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task_list = TaskList.objects.get(id=kwargs["pk"])
        if request.user != task_list.owner:
            set_message(request, "You are not the owner of this list.")
            return redirect("lists")

        return super().post(request, *args, **kwargs)


class DeleteListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_list = TaskList.objects.get(id=kwargs["id"])
        if request.user != task_list.owner:
            set_message(request, "You are not the owner of this list.")
            return redirect("lists")

        task_list.delete()
        return redirect("lists")


#####################
####### TASKS #######
#####################

def redirect_to_previous_or_list(request, list_id):
    """ Redirect to the previous page, or to the list page if there is no previous page """

    # Get the referer URL from the request headers
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect("list", id=list_id)


class MyTasksView(LoginRequiredMixin, View):
    template = "tasks/my_tasks.html"

    def get(self, request):
        task_lists = TaskList.objects.filter(participants=request.user)
        tasks = Task.objects.filter(task_list__in=task_lists).filter(assigned_to=request.user)

        # Create a dictionary of user tasks, where the key is the task list id
        task_dict = {}
        for task_list in task_lists:
            if tasks.filter(task_list=task_list).exists():
                task_dict[task_list.id] = tasks.filter(task_list=task_list)

        # Remove task lists without user tasks
        task_lists = task_lists.filter(id__in=task_dict.keys())
        return render(request, self.template, {"lists": task_lists, "task_dict": task_dict, "message": get_message(request)})


class TaskDetailView(LoginRequiredMixin, View):
    template = "tasks/task_detail.html"

    def get(self, request, list_id, task_id):
        if request.user not in TaskList.objects.get(id=list_id).participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")

        task = Task.objects.get(id=task_id)
        comments = TaskComment.objects.filter(task=task)
        return render(request, self.template, {"task": task, 'comments': comments, 'message': get_message(request)})


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "assigned_to", "due_datetime", "attachment", "priority"]
    template_name = "tasks/create_task.html"

    def get(self, request, *args, **kwargs):
        task_list = TaskList.objects.get(id=kwargs["list_id"])
        if request.user not in task_list.participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")
        return super().get(request, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        if request.user not in TaskList.objects.get(id=kwargs["list_id"]).participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")

        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            # Add the task to the task_list, after it is created
            task_list = TaskList.objects.get(id=self.kwargs["list_id"])
            task_list.tasks.add(self.object)
            task_list.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "assigned_to", "due_datetime", "attachment", "priority"]
    template_name = "tasks/edit_task.html"
    success_url = reverse_lazy("my-tasks")

    def get(self, request, *args, **kwargs):
        if request.user not in TaskList.objects.get(id=kwargs["list_id"]).participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user not in TaskList.objects.get(id=kwargs["list_id"]).participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect_to_previous_or_list(request, kwargs["list_id"])

        task = Task.objects.get(id=kwargs["pk"])
        self.success_url = reverse_lazy("task", kwargs={"list_id": task.task_list.id, "task_id": task.id})
        return super().post(request, *args, **kwargs)


class DeleteTaskView(LoginRequiredMixin, View):
    def get(self, request, list_id, task_id):
        if request.user not in TaskList.objects.get(id=list_id).participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")

        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect_to_previous_or_list(request, list_id)


class CompleteTaskView(LoginRequiredMixin, View):
    def get(self, request, list_id, task_id):
        # Only the user assignee can complete the task
        if request.user != Task.objects.get(id=task_id).assigned_to:
            set_message(request, "You are not the assignee of this task.")
            return redirect_to_previous_or_list(request, list_id)

        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        return redirect_to_previous_or_list(request, list_id)


#####################
##### COMMENTS ######
#####################

class AddCommentView(LoginRequiredMixin, View):
    model = TaskComment

    def post(self, request, list_id, task_id):

        # Only the task list participants can comment
        if request.user not in TaskList.objects.get(id=list_id).participants.all():
            set_message(request, "You are not a participant of this list.")
            return redirect("lists")

        if not request.POST.get("comment") or not request.POST.get("comment").strip():
            set_message(request, "Comment cannot be empty.")
            return redirect("task", list_id=list_id, task_id=task_id)

        task = Task.objects.get(id=task_id)
        comment = TaskComment.objects.create(comment=request.POST.get("comment"), task=task, user=request.user)
        comment.save()
        return redirect("task", list_id=list_id, task_id=task_id)


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, list_id, task_id, comment_id):
        # Only the comment owner can delete the comment
        comment = TaskComment.objects.get(id=comment_id)
        if request.user != comment.user:
            set_message(request, "You are not the creator of this comment.")
            return redirect("task", list_id=list_id, task_id=task_id)
        comment.delete()
        return redirect("task", list_id=list_id, task_id=task_id)
