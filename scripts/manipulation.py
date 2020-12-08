import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar

dataset = pd.read_csv('../data/repos_commits.csv')

dataset['Month'] = pd.DatetimeIndex(dataset['Date']).month
dataset['Week_Day'] = pd.DatetimeIndex(dataset['Date']).weekday
b = dataset.groupby('Author',sort=False).size().reset_index(name='file_changed')
dataset = pd.merge(dataset, b, on='Author')
dataset = dataset[['i', 'Author', 'file_changed','Date', 'Month','Week_Day','Commit Message','Senti Strength']]
#dataset['Month'] = dataset['Month'].apply(lambda x: calendar.month_abbr[x])
dataset.to_csv('final_file.csv')

sal = dataset['Senti Strength'].value_counts().plot(kind="bar",figsize=(6,6))
sal.set_ylabel('Number of authors')
plt.savefig('../graphs/authors_sentistrenght_count.png')
plt.show()

sel = dataset.groupby(['Month','Senti Strength']).size().unstack().plot(kind="bar",stacked=False,figsize=(14,6))
sel.set_ylabel('Number of authors')
sel.set_xlabel('Months')
plt.savefig('../graphs/sentistrenght_month_authors')
plt.show()

#scatter plot displaying number file changed vs months, not working yet
boh = dataset.groupby(['Month'])
bro = dataset[~dataset.Author.duplicated()]
bro.groupby(['Month']).sum()['file_changed'].plot(kind="bar",figsize=(6,6)).set_ylabel('Number of file changed')
#plot.scatter(x='Month', y='file_changed')
#changed_months.set_xlabel('Months')
plt.show()