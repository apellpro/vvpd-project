from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .github import *
from .models import Project, Student

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('projects_list')
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password']
                            )
        if user is not None:
            login(request, user)
            return redirect('projects_list')
        else:
            return render(request, 'main_page', context={
                'error': 'Неверный логин и/или пароль'
            })
    return render(request, 'main_page')


def auth_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home')
def projects_list(request):
    # @TODO
    return render()


def project_review(request, repo_owner, repo_name):
    # @TODO
    return render(request, 'review')
