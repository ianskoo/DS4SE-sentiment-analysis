import requests
import time
import csv
import numpy as np

# ---------------------------------------
# Parameters for the API request and I/O:
per_page = 100
params = f"?since=2020-01-01T00:00:00Z&per_page={per_page}&page="
repos_list_path = './data/links.txt'
output_csv_path = './data/repos_commits_10k_stars.csv'
# ---------------------------------------


# Open file with links to repositories
repos = []
with open(repos_list_path) as links:
    for link in links.readlines():
        repos.append(link[19:-1])


# Insert token in 'Authorization'
# Returns an API response for a repository at index repo_index
def make_request(repo_index, per_page, page_nr, params):
    
    link = f"https://api.github.com/repos/{repos[repo_index]}/commits{params}{page_nr}"
    headers = {'Accept': 'application/json', 'Authorization': 'token 5a26950162202d524bcd2e14307f9ab0505f7387'}

    commits_info = requests.get(link, headers=headers)

    # Sleep while API limit reached
    while commits_info.headers['X-RateLimit-Remaining'] == '0':
        print("Waiting 60s to avoid API rate limit...")
        time.sleep(60)
        # Try again
        commits_info = requests.get(link, headers=headers)
        
    return commits_info.json()


# Function to save the downloaded data
def save_data(array):
    # print("Saving data...", end="\r")
    # np.save('./data/magic_array', array)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for x in array:
            writer.writerow([x[0],x[1],x[2],x[3]])


# Iterate over all projects
arr = [["i", "Date", "Commit Message", "Author"]]
req_cnt = 0
comm_cnt = 0
stop = 0

for i in range(len(repos)):

    # Initialize page nr for iteration over API resulting pages
    page = 1

    while True:
        print(f"{i}/1000 repos done -- {comm_cnt} messages retrieved", end="\r")

        # Try requesting messages for given repo, if an error occurs save everything.
        try:
            commits = make_request(i, per_page, page, params)
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

                # Increase page counter to continue iteration of messages on next API page
                page += 1

            # Condition to break out of the while loop (finish curr repo)
            if len(commits) < per_page:
                break
                        
        # Save data if download is interrupted
        except Exception as e:
            save_data(arr)
            print(f"Error: {e} \n. Processed repositories: %d; retrieved commits: %d" %(req_cnt, comm_cnt))
            break

    # Save to csv after each repo 
    # TODO: free array to free memory, append data to csv instead of overwriting
    save_data(arr)

print("Operation completed. Processed repositories: %d; retrieved commits: %d" %(i+1, comm_cnt))

