import pandas as pd
import datetime
from prettytable import PrettyTable


# count of total mondays etc..
mondays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}
tuesdays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}
wednesdays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}
thursdays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}
fridays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}
saturdays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}
sundays = {'tot': 0, 'pos': 0, 'neg': 0, 'neutr': 0}


def check_score(score, dic):
    if score == 0:
        dic['neutr'] += 1

    elif score > 0:
        dic['pos'] += 1

    elif score < 0:
        dic['neg'] += 1


weekday_table = PrettyTable()
dataset = pd.read_csv('../data/final_file.csv', lineterminator='\n')
dataset = pd.DataFrame(dataset)
for el in dataset.iterrows():
    day = datetime.datetime.strptime(el[1][2], "%Y-%m-%dT%H:%M:%SZ").weekday()
    if day == 0:
        mondays['tot'] += 1
        check_score(el[1][6], mondays)

    elif day == 1:
        tuesdays['tot'] += 1
        check_score(el[1][6], tuesdays)

    elif day == 2:
        wednesdays['tot'] += 1
        check_score(el[1][6], wednesdays)

    elif day == 3:
        thursdays['tot'] += 1
        check_score(el[1][6], thursdays)

    elif day == 4:
        fridays['tot'] += 1
        check_score(el[1][6], fridays)

    elif day == 5:
        saturdays['tot'] += 1
        check_score(el[1][6], saturdays)

    elif day == 6:
        sundays['tot'] += 1
        check_score(el[1][6], sundays)


weekday_table.field_names = ["Day", "#Commits", "#Pos. Commits", "#Neutral Commits", "#Neg. commits"]
weekday_table.add_row(["Monday", mondays['tot'], mondays['pos'], mondays['neutr'], mondays['neg']])
weekday_table.add_row(["Tuesday", tuesdays['tot'], tuesdays['pos'], tuesdays['neutr'], tuesdays['neg']])
weekday_table.add_row(["Wednesday", wednesdays['tot'], wednesdays['pos'], wednesdays['neutr'], wednesdays['neg']])
weekday_table.add_row(["Thursday", thursdays['tot'], thursdays['pos'], thursdays['neutr'], thursdays['neg']])
weekday_table.add_row(["Friday", fridays['tot'], fridays['pos'], fridays['neutr'], fridays['neg']])
weekday_table.add_row(["Saturday", saturdays['tot'], saturdays['pos'], saturdays['neutr'], saturdays['neg']])
weekday_table.add_row(["Sunday", sundays['tot'], sundays['pos'], sundays['neutr'], sundays['neg']])

print("Number of commits per weekday")
print(weekday_table)


scores = {'tot': 0, '0': 0, '1': 0, '-1': 0, '2': 0, '-2': 0, '3': 0, '-3': 0}

for el in dataset['SentiStrength\r']:
    scores['tot'] += 1

    if el == 0:
        scores['0'] += 1
    elif el == 1:
        scores['1'] += 1
    elif el == -1:
        scores['-1'] += 1
    elif el == 2:
        scores['2'] += 1
    elif el == -2:
        scores['-2'] += 1
    elif el == 3:
        scores['3'] += 1
    elif el == -3:
        scores['-3'] += 1

percentages = {'per_0': round(scores['0'] / scores['tot'] * 100, 3),
               'per_1': round(scores['1'] / scores['tot'] * 100, 3),
               'per_minus1': round(scores['-1'] / scores['tot'] * 100, 3),
               'per_2': round(scores['2'] / scores['tot'] * 100, 3),
               'per_minus2': round(scores['-2'] / scores['tot'] * 100, 3),
               'per_3': round(scores['3'] / scores['tot'] * 100, 3),
               'per_minus3': round(scores['-3'] / scores['tot'] * 100, 3)
               }
print("\n\n")
print("Number of commits per Sentistrength value")
count_table = PrettyTable()
count_table.field_names = ["Score", "#Commits", "Percentage"]
count_table.add_row(["-3", scores['-3'], "{}%".format(percentages['per_minus3'])])
count_table.add_row(["-2", scores['-2'], "{}%".format(percentages['per_minus2'])])
count_table.add_row(["-1", scores['-1'], "{}%".format(percentages['per_minus1'])])
count_table.add_row(["0", scores['0'], "{}%".format(percentages['per_0'])])
count_table.add_row(["1", scores['1'], "{}%".format(percentages['per_1'])])
count_table.add_row(["2", scores['2'], "{}%".format(percentages['per_2'])])
count_table.add_row(["3", scores['3'], "{}%".format(percentages['per_3'])])

print(count_table)
print("\n\n")

negative_comments = round((scores['-1']+scores['-2']+scores['-3'])/scores['tot'] * 100, 3)
print("#negative comments: {}%".format(negative_comments))

neutral_comments = round(scores['0']/scores['tot'] * 100, 3)
print("#neutral comments: {}%".format(neutral_comments))

positive_comments = round((scores['1']+scores['2']+scores['3'])/scores['tot'] * 100, 3)
print("#positive comments: {}%".format(positive_comments))
