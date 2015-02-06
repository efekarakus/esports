"""
Find out how the fans changed between the two seasons of League of Legends.
@author Efe Karakus
"""

import csv

PATH = 'data/reddit-survey.csv'

NA_S4_TEAMS = set(["Cloud9", "LMQ", "Team SoloMid", "Curse", 
"Counter Logic Gaming", "Team Dignitas", "Evil Geniuses", "compLexity Black", "empty"])

NA_S5_TEAMS = set(["Counter Logic Gaming", "Gravity", "Team SoloMid",
"Team 8", "Team Impulse", "Team Liquid", "Winterfox", "Cloud9", "Team Coast", "Team Dignitas", "empty"])

EU_S4_TEAMS = set(["Alliance", "Fnatic", "Supa Hot Crew", "SK Gaming",
"Millenium", "ROCCAT", "Copenhagen Wolves", "Gambit Gaming", "empty"])

EU_S5_TEAMS = set(["Fnatic", "SK Gaming", "Elements", "GIANTS GAMING",
"H2k", "Unicorns of Love", "Copenhagen Wolves", "Meet Your Makers", "ROCCAT", "Gambit Gaming", "empty"])

def is_valid(na_s4, na_s5, eu_s4, eu_s5):
    if na_s4 == "" and na_s5 == "" and eu_s4 == "" and eu_s5 == "":
        return False
    return True

def get_data():
    data = []
    with open(PATH, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            na_s4 = row[1]
            na_s5 = row[2]
            eu_s4 = row[3]
            eu_s5 = row[4]

            # skip empty entries
            if not is_valid(na_s4, na_s5, eu_s4, eu_s5):
                continue

            data.append([na_s4, na_s5, eu_s4, eu_s5])
    return data

def get_flows(data):
    na = {
        's4': {},
        's5': {}
    }

    eu = {
        's4': {},
        's5': {}
    }
    for entry in data:
        na_s4 = entry[0] if entry[0] != "" else "empty"
        na_s5 = entry[1] if entry[1] != "" else "empty"
        eu_s4 = entry[2] if entry[2] != "" else "empty"
        eu_s5 = entry[3] if entry[3] != "" else "empty"

        # get the directions between na teams
        if na_s4 != "" or na_s5 != "":
            if not na_s4 in na['s4']:
                na['s4'][na_s4] = {'count': 1}
                for team in NA_S5_TEAMS:
                    na['s4'][na_s4][team] = 0
                na['s4'][na_s4][na_s5] += 1
            else:
                na['s4'][na_s4]['count'] += 1
                na['s4'][na_s4][na_s5] += 1

            if not na_s5 in na['s5']:
                na['s5'][na_s5] = {'count': 1}
                for team in NA_S4_TEAMS:
                    na['s5'][na_s5][team] = 0
                na['s5'][na_s5][na_s4] += 1
            else:
                na['s5'][na_s5]['count'] += 1
                na['s5'][na_s5][na_s4] += 1

        if eu_s4 != "" or eu_s5 != "":
            if not eu_s4 in eu['s4']:
                eu['s4'][eu_s4] = {'count': 1}
                for team in EU_S5_TEAMS:
                    eu['s4'][eu_s4][team] = 0
                eu['s4'][eu_s4][eu_s5] += 1
            else:
                eu['s4'][eu_s4]['count'] += 1
                eu['s4'][eu_s4][eu_s5] += 1

            if not eu_s5 in eu['s5']:
                eu['s5'][eu_s5] = {'count': 1}
                for team in EU_S4_TEAMS:
                    eu['s5'][eu_s5][team] = 0
                eu['s5'][eu_s5][eu_s4] += 1
            else:
                eu['s5'][eu_s5]['count'] += 1
                eu['s5'][eu_s5][eu_s4] += 1


    return (na, eu)


data = get_data()
(na, eu) = get_flows(data)
print eu['s5']['SK Gaming']
print eu['s4']['Alliance']
