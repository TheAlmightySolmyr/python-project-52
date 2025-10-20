from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')