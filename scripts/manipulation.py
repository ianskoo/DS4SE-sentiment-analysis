import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar
import re
import math
import itertools
from pandas.api.types import is_string_dtype
from sentistrength import PySentiStr

# Initialize SentiStrength
senti = PySentiStr()

senti.setSentiStrengthPath('./scripts/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('./SentStrength_Data_Sept2011')

#Lasciate qua se no a me non runna il senti
# senti.setSentiStrengthPath('/Users/giomonopoli/Downloads/SentiStrength.jar')
# senti.setSentiStrengthLanguageFolderPath('/Users/giomonopoli/Downloads/SentStrength_Data_Sept2011')

##Function for creating sentistrength table
def createSenti(message):
    value = senti.getSentiment(message)[0]
    print('%d: %s' %(value, message))
    return value

##Function for checking chinese messages
def checkChinese(message):
    return re.findall(r'[\u4e00-\u9fff]+', str(message))

## Function for cleaning the dataset if a cleaned version is not available
def cleanDataset(dataset):
    ###Clean initial dataset by removing multilines commit messages and putting them in single lines.
    print("Cleaning initial dataset...")
    for col in dataset.columns:
        if is_string_dtype(dataset[col]):
            dataset[col] = dataset[col].str.replace('\n', '')

    ###Apply senti strength on each row
    #dataset['SentiStrength'] = senti.getSentiment(dataset['Commit Message'])[0]

    ###Take out rows with empty commit message
    dataset = dataset[dataset['Commit Message'] != None]

    ###Take out rows with commit messages (and authors) which includes "bot" or "#NAME?"
    dataset.drop(dataset.loc[dataset['Commit Message'].str.contains(
        'bot', na=False)].index, inplace=True)
    dataset.drop(dataset.loc[dataset['Commit Message'].str.contains(
        '#NAME?', na=False)].index, inplace=True)
    dataset.drop(dataset.loc[dataset['Commit Message'].str.contains(
        'Merge', na=False)].index, inplace=True)
    dataset.drop(dataset.loc[dataset['Author'].str.contains(
        'bot', na=False)].index, inplace=True)

    ###Just some cleaning
    dataset['i'] = dataset['i'].astype(str).replace('\.0', '', regex=True)

    ### Drop all rows which contain NA values, i.e some values are missing so its not a clean data.
    dataset = dataset.dropna()

    ###Remove commit messages in chinese since sentistrength is done on English words
    dataset['Chinese'] = dataset['Commit Message'].apply(checkChinese)
    dataset = dataset[~dataset.Chinese.str.len().gt(0)]
    dataset['Chinese'] = dataset['Author'].apply(checkChinese)
    dataset = dataset[~dataset.Chinese.str.len().gt(0)]
    del dataset['Chinese']

    ###Remove commit messages with more numbers than letter (versioning messages etc..)
    dataset['Bal_char'] = 0
    for i, row in dataset.iterrows():
        numbers = sum(c.isdigit() for c in row['Commit Message'])
        letters = sum(c.isalpha() for c in row['Commit Message'])
        ifor_val = letters - numbers
        dataset.at[i, 'Bal_char'] = ifor_val

    dataset = dataset[~dataset.Bal_char.lt(0)]
    del dataset['Bal_char']

    dataset.to_csv('./data/cleaned_10k_dataset.csv')

#--------------------------------------------------------------

###Read csv file (get cleaned dataset if available)
print("Reading CSV into Pandas dataframe...")
try:
    dataset = pd.read_csv('./data/cleaned_10k_dataset.csv')
except FileNotFoundError:
    cleanDataset(pd.read_csv('./data/repos_commits_10k_stars_2020.csv'))
    print("Reading cleaned CSV into Pandas dataframe...")
    dataset = pd.read_csv('./data/cleaned_10k_dataset.csv')

### Output dataset
b = dataset['i'].unique()
dfObj = pd.DataFrame(columns=['i', 'Date', 'Commit Message','Author'])

### Sampling
print("Sampling dataset...")
quanto_prendi = 40
for i in b:
    dfObj = dfObj.append(dataset.loc[dataset['i'] == i].sample(n=math.ceil(dataset.loc[dataset['i'] == i].shape[0]/quanto_prendi)),ignore_index=True)

### SentiStrength evaluation
print("Evalutating SentiStrenght score of dataset...")
dfObj['SentiStrength'] = dfObj['Commit Message'].apply(createSenti)

### Saving results
dfObj.to_csv('./data/final_file.csv')

### Plotting
dataset = pd.read_csv('./data/final_file.csv',lineterminator='\n')
dataset['Month'] = pd.DatetimeIndex(dataset['Date']).month
dataset['Week_Day'] = pd.DatetimeIndex(dataset['Date']).weekday
b = dataset.groupby('Author',sort=False).size().reset_index(name='file_changed')
dataset = pd.merge(dataset, b, on='Author')
dataset = dataset[['i', 'Author', 'file_changed','Date', 'Month','Week_Day','Commit Message','SentiStrength']]
#dataset['Month'] = dataset['Month'].apply(lambda x: calendar.month_abbr[x])
#dataset.to_csv('final_file.csv')

sal = dataset['SentiStrength'].value_counts().plot(kind="bar",figsize=(6,6))
sal.set_ylabel('Number of authors')
plt.savefig('./graphs/authors_sentistrenght_count.png')
# plt.show()

sel = dataset.groupby(['Month','SentiStrength']).size().unstack().plot(kind="bar",stacked=False,figsize=(14,6))
sel.set_ylabel('Number of authors')
sel.set_xlabel('Months')
plt.savefig('./graphs/sentistrenght_month_authors')
# plt.show()

#scatter plot displaying number file changed vs months, not working yet
boh = dataset.groupby(['Month'])
bro = dataset[~dataset.Author.duplicated()]
bro.groupby(['Month']).sum()['file_changed'].plot(kind="bar",figsize=(6,6)).set_ylabel('Number of file changed')
#plot.scatter(x='Month', y='file_changed')
#changed_months.set_xlabel('Months')
#plt.show()

sentiment_vs_weekday = dataset.groupby(['Week_Day','SentiStrength']).size().unstack().plot(kind="bar",stacked=False,figsize=(14,6))
sentiment_vs_weekday.set_ylabel('Number of Authors')
sentiment_vs_weekday.set_xlabel('Week day')
plt.savefig('./graphs/sentistrenght_weekday_authors')
#plt.show()

