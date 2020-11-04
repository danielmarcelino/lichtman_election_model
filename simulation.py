import random
from contests import contests
from terminaltables import AsciiTable, SingleTable
from model_index import scores
import sys
import csv
from termcolor import colored
from itertools import zip_longest
from progress.bar import Bar

results = {}

democrat_electors = []
republican_electors = []

democrat_states = []
republican_states = []

def state_election():
    for key, value in contests.items():

        name = key
        id = value[0]
        ec = value[1]

        democratic_average = float(value[2]) * random.uniform(1, 1.09) 
        republican_average = float(value[3]) * random.uniform(1, 1.09) 

        model_index_d = scores[key][0]
        model_index_r = scores[key][1]

        democrat_c = democratic_average * model_index_d
        republican_c = republican_average * model_index_r
        third_c = 3

        temp_results = random.choices(["D","R", "T"], [democrat_c, republican_c, third_c], k=10000)

        democrat = temp_results.count("D") / 100
        republican = temp_results.count("R") / 100
        third = temp_results.count("T") / 100
        
        if democrat > republican:
            democrat_electors.append(int(ec))
            party = 3

            democrat_t = str(round(democrat - (third / 2), 2)) + '%'
            republican_t = str(round(100 - democrat - (third / 2), 2)) + '%'
            third_t = str(third) + '%'

            margin = round((democrat - republican), 4)
            margin_t = str("Biden +" + str(margin) + "%")

            if democrat - republican > 5:
                party = 2

                if democrat - republican > 10:
                    party = 1

            democrat_states.append(name)

            results[id] = [name, ec, party, democrat_t, republican_t, third_t, margin_t, "D"]

        if democrat < republican:
            republican_electors.append(int(ec))
            party = 4

            democrat_t = str(round(100 - republican - (third / 2), 2)) + '%'
            republican_t = str(round(republican - (third / 2), 2)) + '%'
            third_t = str(third) + '%'

            margin = round((republican - democrat), 4)
            margin_t = str("Trump +" + str(margin) + "%")

            if republican - democrat > 5:
                party = 5

                if republican - democrat > 10:
                    party = 6

            republican_states.append(name)
            results[id] = [name, ec, party, democrat_t, republican_t, third_t, margin_t, "R"]


if __name__ == '__main__':
    if sys.argv[1] == 'rundown':
        temp_dump = []
        for _ in range(10):
            state_election()
            if sum(democrat_electors) > sum(republican_electors):
                temp_dump.append("D")
            
            if sum(democrat_electors) < sum(republican_electors):
                temp_dump.append("R") 

            democrat_electors = []
            republican_electors = []
        print(temp_dump.count("D"), temp_dump.count("R"))

    if sys.argv[1] == 'single':
        state_election()
        se_table_data = [
        [colored('DEMOCRAT', 'white', 'on_blue'), colored('REPUBLICAN', 'white', 'on_red'), 'TOTAL'],
        [str(sum(democrat_electors)), str(sum(republican_electors)), str(sum(democrat_electors) + sum(republican_electors))]
        ]
        se_table = SingleTable(se_table_data)
        se_table.title = 'GE Simulation'
        se_table.justify_columns[0] = 'center' 
        se_table.justify_columns[1] = 'center'
        se_table.justify_columns[2] = 'center' 
        print (se_table.table)

    if sys.argv[1] == 'states':
        out = 0
        for _ in range(100):
            state_election()
            with open(f'temp/2020_weighted/{out}_2020_weighted.csv', 'w') as csvfile:
                filewriter = csv.writer(csvfile,
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(["name", "ec", "margin", "winner"])
                
                for key, value in results.items():
                    filewriter.writerow([value[0], value[1], value[6], value[7]])
                    
                filewriter.writerow([sum(democrat_electors), sum(republican_electors)])
            print('File outputed at temp/2020/' + str(out) + '_2020.csv')
            out = out + 1
            democrat_electors = []
            republican_electors = []

    if sys.argv[1] == 'prob':
        bar = Bar('Processing', max=100)
        temp_dump = []

        dem = 0
        rep = 0

        for _ in range(100):
            state_election()
            dem = dem + sum(democrat_electors)
            rep = rep + sum(republican_electors)

            if sum(democrat_electors) > sum(republican_electors):
                temp_dump.append("D")
            
            if sum(democrat_electors) < sum(republican_electors):
                temp_dump.append("R")

            if sum(democrat_electors) == sum(republican_electors):
                temp_dump.append("T")

            democrat_electors = []
            republican_electors = []
            bar.next()

        democrat_probability = temp_dump.count('D')
        republican_probability = temp_dump.count('R')
        tie_probability = temp_dump.count('T')

        table_data = [
        [colored('DEMOCRAT', 'white', 'on_blue'), colored('REPUBLICAN', 'white', 'on_red'), 'TIE', 'TOTAL'],
        [str(democrat_probability) + '%', str(republican_probability) + '%', str(tie_probability) + '%',
            str(democrat_probability + republican_probability + tie_probability) + '%']
        ]

        table_data_ec = [
        [colored('DEMOCRAT', 'white', 'on_blue'), colored('REPUBLICAN', 'white', 'on_red')],
        [str(dem/100), str(rep/100)]
        ]

        table = SingleTable(table_data)
        table.title = 'GE Win Chances [k=100]'
        table.justify_columns[0] = 'center' 
        table.justify_columns[1] = 'center'
        table.justify_columns[2] = 'center'  

        table_ec = SingleTable(table_data_ec)
        table_ec.title = 'Average EC Votes [k=100]'
        table_ec.justify_columns[0] = 'center' 
        table_ec.justify_columns[1] = 'center'
        table_ec.justify_columns[2] = 'center'  

        bar.finish()
        print (table.table)
        print (table_ec.table)

    elif sys.argv[1] == 'results':
        state_election()
        with open('results_august.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile,
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["id", "name", "ec", "party", "democrat", "republican", "third", "margin", "winner"])
            
            for key, value in results.items():
                filewriter.writerow([key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]])
                
            filewriter.writerow([sum(democrat_electors), sum(republican_electors)])
        print('File outputed as results_august.csv')