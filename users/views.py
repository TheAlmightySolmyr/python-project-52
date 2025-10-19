from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
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
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован!'

class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Пользователь успешно обновлен'
    
    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return User.objects.get(id=user_id)
    
    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        return redirect('user_list')

class UserDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Пользователь успешно удален'
    
    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return User.objects.get(id=user_id)
    
    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        return redirect('user_list')