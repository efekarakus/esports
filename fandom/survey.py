"""
Find out how the fans changed between the two seasons of League of Legends.
@author Efe Karakus
"""

import collections
import csv
import pprint
import json
import operator

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
    na_empty = 0
    eu_empty = 0
    for entry in data:
        na_s4 = entry[0] if entry[0] != "" else "empty"
        na_s5 = entry[1] if entry[1] != "" else "empty"
        eu_s4 = entry[2] if entry[2] != "" else "empty"
        eu_s5 = entry[3] if entry[3] != "" else "empty"

        # get the directions between na teams
        if na_s4 != "empty" or na_s5 != "empty":
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
        else:
            na_empty += 1

        if eu_s4 != "empty" or eu_s5 != "empty":
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
        else:
            eu_empty += 1


    print "na_empty: ", na_empty
    print "eu_empty: ", eu_empty
    return (na, eu)

def get_overall_stats(region):
    counts = collections.defaultdict(int)
    for season in region:
        for team in region[season]:
            counts[season] += region[season][team]['count']
        counts[season] -= region[season]['empty']['count']
    return dict(counts)

def tojson(region, data):
    with open(region + '.json', 'w') as fp:
        json.dump(data, fp)

def print_retention(region, title):
    counts = collections.defaultdict(int)

    maps = {
        'na': {
            "LMQ": "Team Impulse",
            "Curse": "Team Liquid",
            "Evil Geniuses": "Winterfox"
        },
        "eu": {
            "Alliance": "Elements",
            "Supa Hot Crew": "Meet Your Makers"
        }
    }

    s4 = 0
    s5 = 0
    team_count = 0
    for team in region["s4"]:
        if team == "empty": continue

        t = team
        t2 = team

        if t in maps[title]:
            t2 = maps[title][t]

        if not t2 in region["s4"][t]: continue

        s4 += region["s4"][t]["count"]
        s5 += region["s4"][t][t2]
        team_count += 1

    print title, team_count, "s4: %d" % s4, "s5: %d" % s5, (float(s5)/s4)*100

def print_top_counts(region, title):
    print title, "S4"
    teams = {}
    for team in region["s4"]:
        teams[team] = region["s4"][team]["count"]
    for (team,count) in reversed(sorted(teams.items(), key = operator.itemgetter(1))):
        print team, count
    print ""
    print title, "S5"
    teams = {}
    for team in region["s5"]:
        teams[team] = region["s5"][team]["count"]
    for (team,count) in reversed(sorted(teams.items(), key = operator.itemgetter(1))):
        print team, count
    print ""


data = get_data()
(na, eu) = get_flows(data)
#na_overall = get_overall_stats(na)
#eu_overall = get_overall_stats(eu)

#print_retention(na, 'na')
#print_retention(eu, 'eu')

#print_top_counts(na, "NA")
#print_top_counts(eu, "EU")

#tojson('na', na)
#tojson('eu', eu)
#print 'na', na_overall
#print 'eu', eu_overall
