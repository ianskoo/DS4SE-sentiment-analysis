import requests
import time
import csv
import numpy as np

# ---------------------------------------
# Parameters for the API request:
per_page = 100
params = f"?since:2020-01-01T00:00:00Z&per_page={per_page}&page="
# ---------------------------------------

# Open file with links to repositories
repos = []
with open('./data/links_small.txt') as links:
    for link in links.readlines():
        repos.append(link[19:-1])


# Insert token in 'Authorization'
# Returns an API response for a repository at index repo_index
def make_request(repo_index, per_page, params):
    
    commits_info = requests.get(f"https://api.github.com/repos/{repos[repo_index]}/commits{params}",
                                headers={'Accept': 'application/json', 'Authorization': 'token 5a26950162202d524bcd2e14307f9ab0505f7387'})

    if commits_info.headers['X-RateLimit-Remaining'] == '1':
        print("Waiting 60s to avoid API rate limit...")
        time.sleep(60)

    return commits_info.json()


# Function to save the downloaded data
def save_data(array):
    print("Saving data, this could take a moment...", end="\r")
    # np.save('./data/magic_array', array)

    with open('./data/repos_commits2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for x in array:
            writer.writerow([x[0],x[1],x[2],x[3]])


# Iterate over all projects
arr = [["i", "Date", "Commit Message", "Author"]]
req_cnt = 0
comm_cnt = 0
stop = 0

for i in range(len(repos)):
    while True:
        print(f"{i}/1000 repos done -- {comm_cnt} messages retrieved", end="\r")

        # Try requesting messages for given repo, if an error occurs save everything.
        try:
            commits = make_request(i, per_page, params)
            if isinstance(commits, list):
                req_cnt += 1
                # Iterate over all commits of a single project
                for commit in commits:
                    if commit['commit']['message'] != "":
                        comm_cnt += 1

                        date = commit['commit']['committer']['date']
                        message = commit['commit']['message']
                        person = commit['commit']['author']['name']

                        arr.append([i, date, message, person])

            # Condition to break out of the while loop (finish curr repo)
            if len(commits) < per_page:
                break
                        
        # Save data if download is interrupted
        except Exception as e:
            # save_data(arr)
            print(f"Error: {e} \nAPI rate limit reached! Downloaded repositories: %d" %req_cnt)
    
    # Save to csv after each repo
    save_data(arr)

print("Operation completed. Downloaded repositories: %d" %(i+1))

