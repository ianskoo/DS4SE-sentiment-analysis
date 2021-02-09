# DS4SE-sentiment-analysis
Seminar project: Sentiment analysis of Github comments in modern projects using SentiStrength.

The code can be found under the folder scripts, containing 4 main scripts:

* <em>get_repos_links.py</em> gets the link of the first 1000 projects with more or equal 10'000 stars in ascending order from the 01.01.2020. The result of running this script can be found under 'data\links.txt'
* <em>makelogs_API.py</em> take the csv with the links and output in a file 'repos_commits_10k_stars.csv' the commit messages for every project with the corresponding date and author. This csv file cannot be found under the folder data because it is too big.
* <em>manipulation.py</em> take the result of makelogs_API.py and does the sentiment evaluation with SentiStrength. After that the dataset is cleaned and sampled and saved in our final dataset which can be found under 'data\final_file.csv'. In order ro run this script the file 'SentiStrength.jar' is needed under the folder \scripts, which is not included for Copyright purposes. In order to obtain that file a request to the creator of SentiStrength Mike Thelwall is needed. This script produces also graphs created with Matplotlib: these can be found under the folder '\graphs'.
* <em>get_percentages.py</em> takes 'final_file.csv' and print out with prettytable some percentages useful for responding to the research questions.
