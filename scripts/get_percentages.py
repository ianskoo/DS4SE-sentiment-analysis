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
        #print(el[1][5])
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
weekday_table.add_row(["Monday", mondays['tot'], "{} ({})".format(mondays['pos'], round(mondays['pos']/mondays['tot']* 100, 2)), "{} ({})".format(mondays['neutr'], round(mondays['neutr']/mondays['tot']* 100, 2)), "{} ({})".format(mondays['neg'], round(mondays['neg']/mondays['tot']* 100, 2))])
weekday_table.add_row(["Tuesday", tuesdays['tot'], "{} ({})".format(tuesdays['pos'], round(tuesdays['pos']/tuesdays['tot']* 100, 2)), "{} ({})".format(tuesdays['neutr'], round(tuesdays['neutr']/tuesdays['tot']* 100, 2)), "{} ({})".format(tuesdays['neg'], round(tuesdays['neg']/tuesdays['tot']* 100, 2))])
weekday_table.add_row(["Wednesday", wednesdays['tot'], "{} ({})".format(wednesdays['pos'], round(wednesdays['pos']/wednesdays['tot']* 100, 2)), "{} ({})".format(wednesdays['neutr'], round(wednesdays['neutr']/wednesdays['tot']* 100, 2)), "{} ({})".format(wednesdays['neg'], round(wednesdays['neg']/wednesdays['tot']* 100, 2))])
weekday_table.add_row(["Thursday", thursdays['tot'], "{} ({})".format(thursdays['pos'], round(thursdays['pos']/thursdays['tot']* 100, 2)), "{} ({})".format(thursdays['neutr'], round(thursdays['neutr']/thursdays['tot']* 100, 2)), "{} ({})".format(thursdays['neg'], round(thursdays['neg']/thursdays['tot']* 100, 2))])
weekday_table.add_row(["Friday", fridays['tot'], "{} ({})".format(fridays['pos'], round(fridays['pos']/fridays['tot']* 100, 2)), "{} ({})".format(fridays['neutr'], round(fridays['neutr']/fridays['tot']* 100, 2)), "{} ({})".format(fridays['neg'], round(fridays['neg']/fridays['tot']* 100, 2))])
weekday_table.add_row(["Saturday", saturdays['tot'], "{} ({})".format(saturdays['pos'], round(saturdays['pos']/saturdays['tot']* 100, 2)), "{} ({})".format(saturdays['neutr'], round(saturdays['neutr']/saturdays['tot']* 100, 2)), "{} ({})".format(saturdays['neg'], round(saturdays['neg']/saturdays['tot']* 100, 2))])
weekday_table.add_row(["Sunday", sundays['tot'],"{} ({})".format(sundays['pos'], round(sundays['pos']/sundays['tot']* 100, 2)), "{} ({})".format(sundays['neutr'], round(sundays['neutr']/sundays['tot']* 100, 2)), "{} ({})".format(sundays['neg'], round(sundays['neg']/sundays['tot']* 100, 2))])

print("Number of commits per weekday")
print(weekday_table)


scores = {'tot': 0, '0': 0, '1': 0, '-1': 0, '2': 0, '-2': 0, '3': 0, '-3': 0}

for el in dataset['SentiStrength']:
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
