from sentistrength import PySentiStr

# Initialize SentiStrength
senti = PySentiStr()
senti.setSentiStrengthPath('./scripts/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('./SentStrength_Data_Sept2011/')

# Open dataset to evaluate
with open('./data/repos_commits2.csv', 'w+') as f:
    for el in f.readlines():
        sentiment = senti.getSentiment(el[2])
        el[4] = sentiment[0]
        # el[5] = sentiment[1]
        # el[6] = sentiment[2]
        