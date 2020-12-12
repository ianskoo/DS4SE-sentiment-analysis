import requests

# Define number of projects (1 * 100 projects)
nr_proj = 10

# Define and modify call to GitHub API
link = "\
    q=stars:>=10000\
    &updated:<2020-01-01\
    &per_page=100\
    &sort=stars\
    &order=desc\
    &page=" # Needed at the end for page number

with open("links.txt", 'w+') as f:

    # Request 100 projects per page ("nr_proj" nr of pages)
    for p in range(nr_proj):
        r = requests.get(f"https://api.github.com/search/repositories?{link}{p}")
        # headers = r.headers
        data = r.json()

        # Write links to file
        for i in range(len(data['items'])):
            f.write(data['items'][i]['html_url'] + '\n')
