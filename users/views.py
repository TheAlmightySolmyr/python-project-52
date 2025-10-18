from django.shortcuts import render
from django.views import View

class UserView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/user_list.html')
    
class UserCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/user_form.html')
    
class UserUpdate(View):
    def get(self, request, *args, **kwawrgs):
        return render(request, 'users/user_form.html')
    
class UserDelete(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/user_confirm_delete.html')