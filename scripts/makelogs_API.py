import requests
import time
import json
import csv
import numpy as np
from sentistrength import PySentiStr

# Initialize SentiStrength
senti = PySentiStr()
senti.setSentiStrengthPath('./SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('../SentStrength_Data_Sept2011/')

# Open file with links to repositories
repos = []
with open('links.txt') as links:
    for link in links.readlines():
        repos.append(link[19:-1])


# Insert token in 'Authorization'
# Returns an API response for a repository at index repo_index
def make_request(repo_index):
    commmits_info = requests.get(f"https://api.github.com/repos/{repos[repo_index]}/commits",
                                 headers={'Accept': 'application/json', 'Authorization': 'token 5a26950162202d524bcd2e14307f9ab0505f7387'})

    return json.loads(commmits_info.text)

# Function to save the downloaded data
def save_data(array):
    np.save('magic_array', np.array(arr))
    with open('repos_commits.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for x in arr:
            writer.writerow([x[0],x[1],x[2],x[3],x[4]])

# Try a request on the first repo to see if the limit hasn't been reached
commmits = make_request(0)
arr = []
arr.append(["i", "Date", "Commit Message", "Author","Senti Strength"])
count = 0
stop = 0

# Iterate over all projects
for i in range(len(repos[0:1000])):
    # Pause every 60 projects to avoid reaching the rate limit
    if stop == 60:
        time.sleep(60)
        stop = 0
    count+=1
    commmits = make_request(i)
    stop += 1
    print(count)

    try:
        if isinstance(commmits, list):
            # Iterate over all commits of a single project
            for commit in commmits:
                if commit['commit']['message'] != "":
                    date = commit['commit']['committer']['date']
                    message = commit['commit']['message']
                    person = commit['commit']['author']['name']

                    # Sentiment evaluation (could be moved to separate script)
                    arr.append([i, date, message, person, senti.getSentiment(message)[0]])

    # Save data if download is interrupted
    except:
        save_data(arr)
        print("API rate limit reached! Downloaded repositories: %d" %count)

save_data(arr)
print("Operation completed. Downloaded repositories: %d" %count)

