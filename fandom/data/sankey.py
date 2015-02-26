"""
Transform na.json and eu.json into 
sankey.js readable format

@author Efe Karakus
"""

import sys
import json

NA_S4_TEAMS = set(["Cloud9", "LMQ", "Team SoloMid", "Curse", 
"Counter Logic Gaming", "Team Dignitas", "Evil Geniuses", "compLexity Black", "empty"])

NA_S5_TEAMS = set(["Counter Logic Gaming", "Gravity", "Team SoloMid",
"Team 8", "Team Impulse", "Team Liquid", "Winterfox", "Cloud9", "Team Coast", "Team Dignitas", "empty"])

EU_S4_TEAMS = set(["Alliance", "Fnatic", "Supa Hot Crew", "SK Gaming",
"Millenium", "ROCCAT", "Copenhagen Wolves", "Gambit Gaming", "empty"])

EU_S5_TEAMS = set(["Fnatic", "SK Gaming", "Elements", "GIANTS GAMING",
"H2k", "Unicorns of Love", "Copenhagen Wolves", "Meet Your Makers", "ROCCAT", "Gambit Gaming", "empty"])

class Team:
    def __init__(self, name, season):
        self.name = name
        self.season = int(season)
    
    def __hash__(self):
        return hash((self.name, self.season))

    def __eq__(self, other):
        return (self.name, self.season) == (other.name, other.season)

    def __str__(self):
        return self.name + ", " + str(self.season)

    def to_obj(self):
        return {
            "name": self.name,
            "season": self.season
        }

def abbr(team):
    abbrs = {
        "Cloud9": "C9",
        "LMQ": "LMQ",
        "Team SoloMid": "TSM",
        "Curse": "CRS",
        "Counter Logic Gaming": "CLG",
        "Team Dignitas": "DIG",
        "Evil Geniuses": "EG",
        "compLexity Black": "COL",
        "empty": "NS",
        "Gravity": "GV",
        "Team 8": "T8",
        "Team Impulse": "TIP",
        "Team Liquid": "TL",
        "Winterfox": "WFX",
        "Team Coast": "CST",
        "Alliance": "ALL",
        "Fnatic": "FNC",
        "Supa Hot Crew": "SHC",
        "SK Gaming": "SK",
        "Millenium": "MIL",
        "ROCCAT": "ROC",
        "Copenhagen Wolves": "CW",
        "Gambit Gaming": "GMB",
        "Elements": "EL",
        "GIANTS GAMING": "GIA",
        "H2k": "H2K",
        "Unicorns of Love": "UOL",
        "Meet Your Makers": "MYM"
    }
    return abbrs[team]

def nodes(region):
    nodes = []
    if region == "na":
        for name in NA_S4_TEAMS:
            name = abbr(name)
            nodes.append(Team(name, 4))

        for name in NA_S5_TEAMS:
            name = abbr(name)
            nodes.append(Team(name, 5))
    else:
        for name in EU_S4_TEAMS:
            name = abbr(name)
            nodes.append(Team(name, 4))
        
        for name in EU_S5_TEAMS:
            name = abbr(name)
            nodes.append(Team(name, 5))

    return nodes

def map_nodes(nodes):
    m = {}
    for i, node in enumerate(nodes):
        m[str(node)] = i
    return m

def links(region, m):
    def key(name, season):
        return abbr(name) + ", " + str(season)

    def data(region):
        d = None
        with open(region + ".json", "r") as f:
            d = json.load(f)
        return d

    links = []
    data = data(region)

    for fr in data["s4"]:
        source = m[ key(fr, 4) ]
        for to in data["s4"][fr]:
            if to == "count": continue
            target = m[ key(to, 5) ]
            value = data["s4"][fr][to]

            if value != 0:
                links.append({
                    "source": source,
                    "target": target,
                    "value": value
                })
    return links

if __name__=="__main__":
    region = sys.argv[1]
    nodes = nodes(region)
    m = map_nodes(nodes)
    links = links(region, m)

    out = {
        "nodes": map((lambda team: team.to_obj()), nodes),
        "links": links
    }

    with open(region + "-flow.json", "w") as f:
        json.dump(out, f, indent=4)
