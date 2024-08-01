from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to home page </h1>')
    return render(request, 'home.html', {'name':'Sara Zuluaga'})

def about(request):
    return render(request,'about.html')
