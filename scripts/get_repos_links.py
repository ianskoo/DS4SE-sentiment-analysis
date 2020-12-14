import requests

# Define number of projects (1 * 100 projects)
nr_proj = 10

# Define and modify call to GitHub API
link = "\
    q=stars:>=1000\
    &updated:<2020-01-01\
    &per_page=100\
    &sort=stars\
    &order=asc\
    &page=" # Needed at the end for page number

with open("./data/links_medium.txt", 'w+') as f:

    # Request 100 projects per page ("nr_proj" nr of pages)
    for p in range(nr_proj):
        try:
            r = requests.get(
                f"https://api.github.com/search/repositories?{link}{p}",
                headers={'Accept': 'application/json', 'Authorization': 'token 5a26950162202d524bcd2e14307f9ab0505f7387'}
                )

            if isinstance(r, list):
                data = r.json()

                # Write links to file
                for i in range(len(data['items'])):
                    f.write(data['items'][i]['html_url'] + '\n')

            else:
                print(r)
                break

        except Exception as e:
            print("Error: ", e)
            break
