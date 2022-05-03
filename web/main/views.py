from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .github import *
from .models import Project, Student, YearGroup, Tag


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('projects')
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
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


def year_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        studying_year = request.POST.get('enter-year')
        is_main = request.POST.get('do-main-year-group')

        if name and name.isalpha() and studying_year and is_main:
            new_group = YearGroup.objects.create(
                name=name,
                studying_year=studying_year,
                is_main=is_main)
        new_group.save()

        return redirect('projects')

    else:
        return redirect('projects')


def project(request):
    if request.method == 'POST':
        if 'name' in request.POST and 'github_slug' in request.POST:
            name = request.POST.get('project-name')
            github_slug = request.POST.get('git-link')

            new_project = Project.objects.create(
                name=name,
                github_slug='github_slug',
            )
            new_project.save()

            for i in range(1, 5):
                if f'stud-name-{i}' not in request.POST:
                    continue
                new_student = Student.objects.create(
                    firstname=request.POST.get('stud-name'),
                    surname=request.get('stud-surname'),
                    patronymic=request.get('stud-patronymic'),
                    education_group=request.get('stud-group'),
                    education_type=request.get('stud-edu'),
                    github_username=request.get('stud-git'),
                    vk_uid=request.get('stud-vk'),
                    is_leader=request.get('is_leader'),
                )
                new_student.save()
            return redirect(request, 'projects')
        else:
            return redirect(request, 'project')


def tag(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        background_color = request.POST.get('background_color')
        text_color = request.POST.get('text_color')
        new_tag = Tag.objects.create(
            text=text,
            background_color=background_color,
            text_color=text_color,
            user=request.user
        )
        new_tag.save()
        return redirect('projects')
    else:
        return redirect('home')
