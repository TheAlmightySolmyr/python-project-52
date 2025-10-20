from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from .forms import UserRegistrationForm, UserUpdateForm


class UserView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_message = 'Пользователь успешно зарегистрирован'

    def get_success_url(self):
        return '/login/'


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_message = 'Пользователь успешно обновлен'

    def get_success_url(self):
        return '/users/'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        return redirect('/users/')


class UserDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_message = 'Пользователь успешно удален'

    def get_success_url(self):
        return '/users/'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        return redirect('/users/')