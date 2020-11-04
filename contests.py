import csv
with open('input/states_august_weighted.csv', mode='r') as infile:
    reader = csv.reader(infile)
    contests = {rows[0]:rows[1:11] for rows in reader}
    del contests['State']