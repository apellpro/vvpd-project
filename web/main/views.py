from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from json import dumps
from .github import *
from .models import Project, Student, YearGroup, Tag

# Create your views here.


def format_name(tpl):
    return tpl[0][0].upper() + tpl[0][1:].replace('_', ' '), tpl[1]


def get_context(git_owner, git_repo):
    commits = get_commits(git_owner, git_repo)
    stats = get_metrics(git_owner, git_repo)
    # releases = get_releases(git_owner, git_repo)
    for commit in commits:
        commit['commit']['committer']['date'] = datetime.fromisoformat(
            commit['commit']['committer']['date'][:-1]
        ).strftime("%d.%m.%y %H:%M")
    # for key, date in releases.items():
    #     releases[key] = datetime.fromisoformat(date).strftime("%d.%m.%y")
    return commits, stats, []


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
    ex = {
        "projectName": "ПО для мониторинга проектов",
        "students": [
            "Присяжнюк Даниил",
            "Надобных Дмитрий"
        ],
        "repo": "apellnoob/vvpd-project",
        "tags": {
            "Tag2": {
                "bgColor": "#FCA3A3",
                "txtColor": "#000000"
            },
            "Tag5": {
                "bgColor": "#FCA303",
                "txtColor": "#000000"
            }
        },
        "year": "2020/2021"
    }
    projects_json = [
        {
            "projectName": project.name,
            "students": list(map(
                lambda x: f'{x.firstname} {x.surname}',
                list(project.student_set.all())
            )),
            "repo": project.github_slug,
            "tags": dict(
                [(tag.text,
                  {
                      "bgColor": tag.background_color,
                      "txtColor": tag.text_color
                  }
                  )for tag in project.tag_set.all()]
            ),
            "year": str(project.year_group.name)
        } for project in Project.objects.all()
    ]
    return render(request, 'projects_list.html', context={
        'projects': dumps(projects_json),
        'tags': Tag.objects.all(),
        'year_groups': YearGroup.objects.all(),
    })


def project_review(request, git_user, git_repo):
    colors = ['red', 'blue', 'green', 'orange']
    project = None
    error = False
    commits, releases = [], []
    stats = None
    if request.user.is_authenticated:
        if project := Project.objects.filter(github_slug=f'{git_user}/{git_repo}'):
            project = project[0]
    commits, stats, releases = get_context(git_user, git_repo)
    try:
        commits, stats, releases = get_context(git_user, git_repo)
    except BaseException:
        error = True

    context = {
        'guest': not bool(project),
        'error': error
    }
    if project:
        context |= {
            'students': zip(count(), colors, project.student_set.all()),
            'main_tile': {
                'project_name': project.name,
                'students': zip(count(), colors, project.student_set.all())
            },
            'ajax': {
                'owner': git_user,
                'repo': git_repo
            }
        }
    if not error:
        context |= {
            'tasks_tile': get_issues_stats(git_user, git_repo),
            'commits_tile': {
                'commits': commits[:5],
                'show_info': len(commits) > 5,
                'count': len(commits) - 5
            },
            'graphic_tile': get_commits_per_weeks(git_user, git_repo),
            'release_tile': releases[:4],
            'delta_tile': get_project_delta(git_user, git_repo),
            'rating_tile': {
                'percentage': stats['health_percentage'],
                'advanced': map(format_name, list([
                  ('description', stats['description']),
                ] + [
                  i for i in stats['files'].items() if i[0] != 'code_of_conduct_file'
                ]))
            },
        }

    if not error and project:
        context |= {
            'impact_tile': [
                len(get_commits(git_user, git_repo, i.github_username))
                for i in project.student_set.all()
            ],
        }

    return render(request, 'review.html', context=context)



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


def ajax_commits(request):
    if request.method != 'POST':
        return redirect(request, 'projects')
    if all(i in request.POST for i in ['git_owner', 'git_repo', 'git_user']):
        answer = get_commits(
            request.POST['git_owner'], request.POST['git_repo'], request.POST['git_user']
        )
        for i in range(min(5, len(answer))):
            answer[i]['commit']['committer']['date'] = datetime.fromisoformat(answer[i]['commit']['committer']['date'][:-1]).strftime("%d.%m.%y %H:%M")
        return JsonResponse(answer, safe=False)
    return JsonResponse({'error': 0})


def ajax_delta(request):
    if request.method != 'POST':
        return redirect(request, 'projects')
    if all(i in request.POST for i in ['git_owner', 'git_repo', 'git_user']):
        answer = get_contributor_delta(
            request.POST['git_owner'], request.POST['git_repo'], request.POST['git_user']
        )
        return JsonResponse(answer, safe=False)
    return JsonResponse({'error': 0})