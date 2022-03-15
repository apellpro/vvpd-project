from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def homepage(request):
    return render(request, 'homepage.html')


def projects(request):
    return render(request, 'projects.html')


def get_some_information(request):
    info = {
        'one': 1,
        'two': 'четыре',
        'field': ['aaa', 'aaaaa']
    }
    return JsonResponse(info)
