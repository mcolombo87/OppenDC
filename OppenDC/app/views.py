from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, 'app/index.html')

def login(request):
    return render(request, 'app/login.html')