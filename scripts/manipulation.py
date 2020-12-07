import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar

lol = np.load('magic_array.npy')

dataset = pd.read_csv('repos_commits.csv')

dataset['Month'] = pd.DatetimeIndex(dataset['Date']).month
dataset['Week_Day'] = pd.DatetimeIndex(dataset['Date']).weekday
b = dataset.groupby('Author',sort=False).size().reset_index(name='file_changed')
dataset = pd.merge(dataset, b, on='Author')
dataset = dataset[['i', 'Author', 'file_changed','Date', 'Month','Week_Day','Commit Message','Senti Strength']]
dataset['Month'] = dataset['Month'].apply(lambda x: calendar.month_abbr[x])
dataset.to_csv('final_file.csv')

sal = dataset['Senti Strength'].value_counts().plot(kind="bar",figsize=(6,6))
sal.set_ylabel('Number of authors')
plt.savefig('authors_sentistrenght_count.png')
plt.show()

sel = dataset.groupby(['Month','Senti Strength']).size().unstack().plot(kind="bar",stacked=False,figsize=(14,6))
sel.set_ylabel('Number of authors')
sel.set_xlabel('Months')
plt.savefig('sentistrenght_month_authors')
plt.show()