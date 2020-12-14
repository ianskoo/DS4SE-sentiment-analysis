import requests
import time
import json
import csv
import numpy as np
from sentistrength import PySentiStr

# ---------------------------------------
# Parameters for the API request:
per_page = 100
params = f"?since:2020-01-01T00:00:00Z\
    &per_page={per_page}\
    &page="
# ---------------------------------------


# Initialize SentiStrength
senti = PySentiStr()
senti.setSentiStrengthPath('./scripts/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('./SentStrength_Data_Sept2011/')


# Open file with links to repositories
repos = []
with open('./data/links.txt') as links:
    for link in links.readlines():
        repos.append(link[19:-1])


# Insert token in 'Authorization'
# Returns an API response for a repository at index repo_index
def make_request(repo_index, per_page, params):
    commmits_info = requests.get(f"https://api.github.com/repos/{repos[repo_index]}/commits{params}",
                                 headers={'Accept': 'application/json', 'Authorization': 'token 5a26950162202d524bcd2e14307f9ab0505f7387'})

    return json.loads(commmits_info.text)


# Function to save the downloaded data
def save_data(array):
    print("Saving data, this could take a moment...")

    np.save('./data/magic_array', array)
    with open('./data/repos_commits2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for x in array:
            writer.writerow([x[0],x[1],x[2],x[3],x[4]])


# Iterate over all projects
arr = np.array
np.append(arr, ["i", "Date", "Commit Message", "Author","Senti Strength"])
req_cnt = 0
comm_cnt = 0
stop = 0

for i in range(len(repos[0:1000])):
    while True:
        # Pause every 60 repos to avoid reaching the rate limit
        print(f"{i}/1000 repos done -- {comm_cnt} messages retrieved", end="\r")

        if req_cnt != 0 and req_cnt % 60 == 0:
            time.sleep(60)
            print("Waiting 60s to avoid API rate limit...")


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

                        # Sentiment evaluation (could be moved to separate script)
                        sentiment = senti.getSentiment(message)[0]

                        np.append(arr, [i, date, message, person, sentiment])

            # Condition to break out of the while loop (finish curr repo)
            if len(commits) < per_page:
                break
                        
        # Save data if download is interrupted
        except Exception as e:
            save_data(arr)
            print(f"Error: {e} \nAPI rate limit reached! Downloaded repositories: %d" %req_cnt)

save_data(arr)
print("Operation completed. Downloaded repositories: %d" %req_cnt)

