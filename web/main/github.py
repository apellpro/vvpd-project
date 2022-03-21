from requests import request

def getUsersCommits(URL: str):
    payload={}
    headers = {}
    return request("GET", URL + "commits", headers=headers, data=payload).json()

def getCommitBySHA(URL, sha: str):
    payload={}
    headers = {}
    return request("GET", URL + "commits/" + sha, headers=headers, data=payload).json()

def getCommitActivity(URL):
    payload={}
    headers = {}
    return request("GET", URL + "stats/commit_activity" , headers=headers, data=payload).json()

def getMetrics(URL: str):
    payload={}
    headers = {}
    return request("GET", URL + "community/profile", headers=headers, data=payload).json()

def getIssues(URL: str):
    payload={}
    headers = {}
    return request("GET", URL + "issues", headers=headers, data=payload).json()

def getReleases(URL: str):
    payload={}
    headers = {}
    return request("GET", URL + "releases", headers=headers, data=payload).json()
