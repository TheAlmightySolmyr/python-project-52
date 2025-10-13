from django.shortcuts import render, get_object_or_404
from django.views import View

def index(request):
    return render(request, 'index.html')