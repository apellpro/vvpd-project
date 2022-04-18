from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .github import *
from .models import Project, Student

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('projects')
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password']
                            )
        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            return render(request, 'main_page', context={
                'error': 'Неверный логин и/или пароль'
            })
    return render(request, 'main_page.html')


def auth_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home')
def projects_list(request):
    # @TODO
    return render(request, 'projects.html')


def project_review(request, git_user, git_repo):
    colors = ['red', 'blue', 'green', 'orange']
    project = Project.objects.filter(github_slug=f'{git_user}/{git_repo}')
    if not request.user.is_authenticated or not project:
        # guest mode
        pass
    else:
        project = project[0]
        project_name = project.name
        return render(request, 'review.html', context={
            'main_tile': {
                'project_name': project_name,
                'students': zip(count(), colors, project.student_set.all())
            },
            'impact_tile': '',
            'tasks_tile': get_issues_num(git_user, git_repo)
        })
