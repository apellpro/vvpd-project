from requests import request

def getUsersCommits(repo: str):
    payload={}
    headers = {}
    return len(request("GET", "https://api.github.com/repos/" + repo + "commits", headers=headers, data=payload).json())

def getCommitBySHA(repo, sha: str):
    payload={}
    headers = {}
    return request("GET", "https://api.github.com/repos/" + repo + "commits/" + sha, headers=headers, data=payload).json()

def getCommitActivity(repo: str):
    payload={}
    headers = {}
    return request("GET", "https://api.github.com/repos/" + repo + "stats/commit_activity" , headers=headers, data=payload).json()

def getMetrics(repo: str):
    payload={}
    headers = {}
    return request("GET", "https://api.github.com/repos/" + repo + "community/profile", headers=headers, data=payload).json()

def getIssuesNum(repo: str):
    payload={}
    headers = {}
    issues_num = (request("GET", "https://api.github.com/" + "search/issues?q=repo:" + repo, headers=headers, data=payload).json())["total_count"]
    open_issues_num = (request("GET", "https://api.github.com/" + "search/issues?q=repo:" + repo + "+state:open", headers=headers, data=payload).json())["total_count"]
    return issues_num, open_issues_num

def getOpenedIssues(repo: str):
    payload={}
    headers = {}
    issues = request("GET", "https://api.github.com/" + "search/issues?q=repo:" + repo + "+state:open", headers=headers, data=payload).json()
    return issues

def getReleases(repo: str):
    payload={}
    headers = {}
    return request("GET", "https://api.github.com/repos/" + repo + "releases", headers=headers, data=payload).json()
