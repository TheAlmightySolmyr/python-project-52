from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_message = 'Метка успешно создана'

    def get_success_url(self):
        return '/labels/'


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_message = 'Метка успешно изменена'

    def get_success_url(self):
        return '/labels/'


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_message = 'Метка успешно удалена'

    def get_success_url(self):
        return '/labels/'

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        
        if label.task_set.exists():
            messages.error(
                request,
                'Невозможно удалить метку, потому что она используется в задачах'
            )
        else:
            label.delete()
            messages.success(request, self.success_message)
        
        return redirect('/labels/')