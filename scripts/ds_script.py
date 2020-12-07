import requests, json


repos = []
with open('links.txt') as links:
    for link in links.readlines():
        repos.append(link[19:])


print(len(repos[0:10]))

repositories_info = []

for repo in repos[0:1]:
    commmits = requests.get(f"https://api.github.com/repos/{repo}/commits")
    commits = json.loads(commmits.text)

    repo_info = {"owner": repo, "commits": []}

    print(commits)

    for commit in commits:
        repo_info['commits'].append(commit)

    repositories_info.append(repo_info)

print(repo_info)

