from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = Task.objects.all().order_by('-created_at')
        self.filter = TaskFilter(self.request.GET, queryset=queryset, request=self.request)
        return self.filter.qs
    
    def get_context_data(self, **kwargs):
        context = {}
        if hasattr(self, 'filter'):
            context['filter'] = self.filter
        else:
            queryset = Task.objects.all().order_by('-created_at')
            context['filter'] = TaskFilter(self.request.GET, queryset=queryset, request=self.request)
        context['tasks'] = context['filter'].qs
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_object(self, queryset=None):
        task_id = self.kwargs.get('pk')
        return Task.objects.get(id=task_id)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/tasks/'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_message = 'Задача успешно изменена'

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/tasks/'
    
    def get_object(self, queryset=None):
        task_id = self.kwargs.get('pk')
        return Task.objects.get(id=task_id)
    
    def get(self, request, *args, **kwargs):
        task = self.get_object()
        form = self.form_class(instance=task)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_message = 'Задача успешно удалена'

    def get_success_url(self):
        return '/tasks/'

    def delete_task(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        messages.success(request, self.success_message)
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.delete_task(request, *args, **kwargs)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author
    
    def get_object(self, queryset=None):
        task_id = self.kwargs.get('pk')
        return Task.objects.get(id=task_id)

    def handle_no_permission(self):
        messages.error(request, 'Задачу может удалить только её автор')
        return redirect('/tasks/')
    
    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return render(request, self.template_name, {'object': task})