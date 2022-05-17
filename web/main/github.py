from requests import request
from datetime import *


def get_commits(owner, repo, contributer_login = ""):
    """Функция возвращает все коммиты проекта
    или коммиты конкретного пользователя
    с подробной информацией в виде словаря

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория
        contributer_login (str): "" - все коммиты
                           "{name}" - пользователь
    Returns:
        dict - если все коммиты
        list - если коммиты пользователя
    """
    payload = {}
    headers = {}
    commits = request("GET", f"https://api.github.com/repos/{owner}/{repo}/commits", headers=headers, data=payload).json()
    if not contributer_login:
        return commits
    contributer_commits = []
    for commit in commits:
        if commit["author"]["login"] == contributer_login:
            contributer_commits.append(commit)
    return contributer_commits


def get_project_delta(owner, repo):
    """Функция возвращает статистику по
    количесвту изменений в коде
    в виде словаря

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория

    Returns:
        dict
    """
    payload = {}
    headers = {}
    delta_plus = 0
    delta_minus = 0
    weeks = request("GET", f"https://api.github.com/repos/{owner}/{repo}/stats/code_frequency", headers=headers, data=payload).json()
    for week in reversed(weeks):
        if (datetime.utcnow() - datetime.utcfromtimestamp(week[0])).days < 18:
            delta_plus += week[1]
            delta_minus += week[2]

    return {
        "delta_plus": delta_plus,
        "delta_minus": delta_minus
    }


def get_contributor_delta(owner, repo, contributer_login):
    """Функция возвращает статистику по
    количесвту изменений в коде одним
    пользователем в виде словаря

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория
        contributer (str): "{name}" - пользователь
    Returns:
        dict
    """
    payload = {}
    headers = {}
    delta_plus = 0
    delta_minus = 0
    contributors = request("GET", f"https://api.github.com/repos/{owner}/{repo}/stats/contributors", headers=headers, data=payload).json()
    for contributor in contributors:
        if contributor["author"]["login"] == contributer_login:
            for week in reversed(contributor["weeks"]):
                if (datetime.utcnow() - datetime.utcfromtimestamp(week["w"])).days < 18:
                    delta_plus += week["a"]
                    delta_minus -= week["d"]
    return {
        "delta_plus": delta_plus,
        "delta_minus": delta_minus
    }


def get_metrics(owner, repo):
    """Функция возвращает статистику по
    Community Standards в виде словаря

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория

    Returns:
        dict: key (str) - один из пунктов,
                 value - состояние
    """
    payload = {}
    headers = {}
    return request("GET", f"https://api.github.com/repos/{owner}/{repo}/community/profile", headers=headers, data=payload).json()


def get_issues_stats(owner, repo):
    """Функция возвращает количество закрытых,
    открытых и общее кол-во задач в виде словаря

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория

    Returns:
        dict: key (str) - состояние задачи,
                 value (str) - количество
    """
    payload = {}
    headers = {}
    issues = request("GET", f"https://api.github.com/search/issues?q=repo:{owner}/{repo}", headers=headers, data=payload).json()
    issues_num = issues["total_count"]
    open_issues_num = 0
    open_issues_num_2w = 0
    closed_issues_num_2w = 0
    for i in issues['items']:
        if i["state"] == "open":
            open_issues_num += 1
            date = i["created_at"]
            datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            if((datetime.utcnow() - datetime_object).days < 14):
                open_issues_num_2w += 1
        else:
            date = i["closed_at"]
            datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            if((datetime.utcnow() - datetime_object).days < 14):
                closed_issues_num_2w += 1
    return {
        'total': issues_num,
        'opened': open_issues_num,
        'closed': issues_num - open_issues_num,
        'opened_2w': open_issues_num_2w,
        'closed_2w': closed_issues_num_2w
    } 


def get_contributor_issues(owner, repo, contributor_login):
    """Функция возвращает список открытых задач
    которые закреплены за пользователем

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория
        contributor_login (str): пользователь

    Returns:
        list
    """
    payload = {}
    headers = {}
    contributor_issues = []
    issues = request("GET", f'https://api.github.com/search/issues?q=repo:{owner}/{repo}+state:"open"', headers=headers, data=payload).json()
    for issue in issues["items"]:
        for contributor in issue["assignees"]:
            if contributor["login"] == contributor_login:
                contributor_issues.append(issue)
    return contributor_issues


def get_releases(owner, repo):
    """Функция возвращает релизы в виде словаря

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория

    Returns:
        dict: key (str) - название, value (str) - дата
    """
    payload = {}
    headers = {}
    imported_releases = request("GET", f"https://api.github.com/repos/{owner}/{repo}/releases", headers=headers, data=payload).json()
    releases = []
    for i in imported_releases:
        releases.append([[i["name"]], i["created_at"]])
    return releases


def get_commits_per_weeks(owner, repo):
    """Функция возвращает список из количеств
    коммитов за последние 10 недель

    Args:
        owner (str): владелец репозитория
        repo (str): название репозитория

    Returns:
        weeks (list[int]): колличество коммитов
    """
    payload = {}
    headers = {}
    imported_weeks = request("GET", f"https://api.github.com/repos/{owner}/{repo}/stats/participation", headers=headers, data=payload).json()
    weeks = imported_weeks['all'][-10::]
    return weeks
