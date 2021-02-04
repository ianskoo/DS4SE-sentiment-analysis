import pandas as pd

count = 0
count_0 = 0
count_1 = 0
count_minus1 = 0
count_2 = 0
count_minus2 = 0
count_3 = 0
count_minus3 = 0

dataset = pd.read_csv('../data/final_file.csv', lineterminator='\n')
dataset = pd.DataFrame(dataset)

for el in dataset['SentiStrength\r']:
    count += 1

    if el == 0:
        count_0 += 1
    elif el == 1:
        count_1 += 1
    elif el == -1:
        count_minus1 += 1

    elif el == 2:
        count_2 += 1
    elif el == -2:
        count_minus2 += 1
    elif el == 3:
        count_3 += 1

    elif el == -3:
        count_minus3 += 1

per_0 = count_0 / count * 100
per_1 = count_1 / count * 100
per_minus1 = count_minus1 / count * 100
per_2 = count_2 / count * 100
per_minus2 = count_minus2 / count * 100
per_3 = count_3 / count * 100
per_minus3 = count_minus3 / count * 100

print("Number of 0: {}%".format(per_0))
print("Number of 1: {}%".format(per_1))
print("Number of -1: {}%".format(per_minus1))
print("Number of 2: {}%".format(per_2))
print("Number of -2: {}%".format(per_minus2))
print("Number of 3: {}%".format(per_3))
print("Number of -3: {}%".format(per_minus3))

print("total: {}".format(per_0+per_1+per_2+per_3+per_minus1+per_minus2+per_minus3))
