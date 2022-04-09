from requests import request


def get_users_commits(owner, repo: str):
    payload = {}
    headers = {}
    commits = len(request("GET", f"https://api.github.com/repos/{owner}/{repo}/commits", headers=headers, data=payload).json())


def get_commit_by_sha(owner, repo, sha: str):
    payload = {}
    headers = {}
    return request("GET", f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}", headers=headers, data=payload).json()


def get_commit_activity(owner, repo: str):
    payload = {}
    headers = {}
    return request("GET", f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity", headers=headers, data=payload).json()


def get_metrics(owner, repo: str):
    payload = {}
    headers = {}
    return request("GET", f"https://api.github.com/repos/{owner}/{repo}/community/profile", headers=headers, data=payload).json()


def get_issues_num(owner, repo: str):
    payload = {}
    headers = {}
    issues = request("GET", f"https://api.github.com/search/issues?q=repo:{owner}/{repo}", headers=headers, data=payload).json()
    issues_num = issues["total_count"]
    open_issues_num = 0
    for i in issues:
        if i["state"] == "open":
            open_issues_num += 1
    return issues_num, open_issues_num


def get_opened_issues(owner, repo: str):
    payload = {}
    headers = {}
    issues = request("GET", f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+state:open", headers=headers, data=payload).json()
    return issues


def get_releases(owner, repo: str):
    payload = {}
    headers = {}
    imported_releases = request("GET", f"https://api.github.com/repos/{owner}/{repo}/releases", headers=headers, data=payload).json()
    releases = dict()
    for i in imported_releases:
        releases[i["name"]] = i["created_at"]
    return releases
