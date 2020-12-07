from sentistrength import PySentiStr
import time
senti = PySentiStr()
senti.setSentiStrengthPath('./SentiStrength.jar') # Note: Provide absolute path instead of relative path
senti.setSentiStrengthLanguageFolderPath('../SentStrength_Data_Sept2011/') # Note: Provide absolute path instead of relative path
result = senti.getSentiment("I love you but hate the current political climate.",score='dual')
print(result)


import requests
import json
import csv
import numpy as np

repos = []
with open('links.txt') as links:
    for link in links.readlines():
        repos.append(link[19:-1])


# Inserire token generato da github in Authorization
# Ritorna riposta api per una repository all'indice repo_index
def make_request(repo_index):
    commmits_info = requests.get(f"https://api.github.com/repos/{repos[repo_index]}/commits",
                                 headers={'Accept': 'application/json', 'Authorization': 'token 5a26950162202d524bcd2e14307f9ab0505f7387'})

    return json.loads(commmits_info.text)

# Funzione per salvare i dati
def save_data(array):
    np.save('magic_array', np.array(arr))
    with open('repos_commits.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for x in arr:
            writer.writerow([x[0],x[1],x[2],x[3],x[4]])

# Provare richiesta per la prima repository per vedere se il rate limit non è stato superato
commmits = make_request(0)
arr = []
arr.append(["i", "Date", "Commit Message", "Author","Senti Strength"])
count = 0
stop = 0
for i in range(len(repos[0:1000])):
    if stop == 60:
        time.sleep(60)
        stop = 0
    count+=1
    commmits = make_request(i)
    stop += 1
    print(count)

    # Testare per ogni iterazione se il rate limit non è stato superato
    try:
        if isinstance(commmits, list):
            # Iterare tutti i commits di un singolo progetto
            for commit in commmits:
                if commit['commit']['message'] != "":
                    date = commit['commit']['committer']['date']
                    message = commit['commit']['message']
                    person = commit['commit']['author']['name']
                    arr.append([i, date, message, person, senti.getSentiment(message)[0]])

    except:
        save_data(arr)
        print("API rate limit superato! Repo salvate: %d" %count)

save_data(arr)
print("Operazione completata! Repo salvate: %d" %count)

