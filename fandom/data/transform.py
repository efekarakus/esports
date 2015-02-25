import sys
import json
import pprint

ABBRS = {
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

def usage():
    print "python transform.py <region>.json <gap> <width> <height>"
    print "\t<region>.json -- na.json or eu.json"
    print "\t <gap> -- 600px"
    print "\t<width> -- width of the rectangle"
    print "\t<height> -- height of the rectangle"

def get_overall_p(data, team):
    teams = data.keys()
    my_c = data[team]["count"]
    total = 0
    for t in teams:
        total += data[t]["count"]

    return round(float(my_c)/total * 100)


def trans_teams(data):
    trans = {}
    teams = ABBRS.keys()

    for team in teams:
        abbr = ABBRS[team]
        if not abbr in trans:
            trans[abbr] = {
                "4": {},
                "5": {}
            }

        s4 = None
        if team in data["s4"]:
            s4 = data["s4"][team]

        s5 = None
        if team in data["s5"]:
            s5 = data["s5"][team]

        if s4:
            keys = data["s4"][team].keys()
            for key in keys:
                if key == "count":
                    trans[abbr]["4"]["details"] = {
                        "count": data["s4"][team]["count"],
                        "percentage": get_overall_p(data["s4"], team)
                    }
                else:
                    abbr2 = ABBRS[key]
                    trans[abbr]["4"][abbr2] = {
                        "count": data["s4"][team][key],
                        "percentage": round(float(data["s4"][team][key])/data["s4"][team]["count"] * 100)
                    }
        if s5:
            keys = data["s5"][team].keys()
            for key in keys:
                if key == "count":
                    trans[abbr]["5"]["details"] = {
                        "count": data["s5"][team]["count"],
                        "percentage": get_overall_p(data["s5"], team)
                    }
                else:
                    abbr2 = ABBRS[key]
                    trans[abbr]["5"][abbr2] = {
                        "count": data["s5"][team][key],
                        "percentage": round(float(data["s5"][team][key])/data["s5"][team]["count"] * 100)
                    }
        if not s4 and not s5:
            del trans[abbr]

    return trans

def swap_empty_tolast(teams):
    index = 0
    for (t, data) in teams:
        if t == "empty": break
        index += 1

    if index == len(teams) - 1: 
        return

    temp = teams[index]
    teams[index] = teams[-1]
    teams[-1] = temp

def get_total_count(teams):
    total = 0
    for (t, data) in teams:
        total += data["count"]
    return total

def nodes(data, gap, width, height):
    nodes = []
    for season in data:
        teams = sorted(data[season].items(), key =lambda x: x[1]["count"])
        teams.reverse()
        swap_empty_tolast(teams)

        total = get_total_count(teams)

        index = 0
        for (t, content) in teams:
            abbr = ABBRS[t]
            s = int(season[1])

            x = 0
            if s == 5:
                x = gap - width

            h = round(float(content["count"])*height/total)
            if h == 0.0:
                h = 1.0
            y = ((index+1)*height) - h

            nodes.append({
                "team": abbr,
                "season": s,
                "x": x,
                "y": y,
                "width": width,
                "height": h
            })

            index += 1


    return nodes

def get_index(data, team):
    index = 0
    for (t, content) in data:
        if t == team:
            return index
        index += 1
    return None

def links(data, gap, width, height):
    links = []
    s4 = sorted(data["s4"].items(), key =lambda x: x[1]["count"])
    s4.reverse()
    swap_empty_tolast(s4)

    s4_total = get_total_count(s4)

    s5 = sorted(data["s5"].items(), key =lambda x: x[1]["count"])
    s5.reverse()
    swap_empty_tolast(s5)

    s5_total = get_total_count(s5)

    for (from_t, content) in s4:
        if from_t == "count": continue

        from_a = ABBRS[from_t]
        dy0 = 0
        for to_t in content:
            if to_t == "count": continue

            to_a = ABBRS[to_t]
            
            x0 = width
            h0 = round(float(content["count"])*height/s4_total)
            if h0 == 0.0:
                h0 = 1.0
            y0 = ((get_index(s4, from_t)+1)*height) - h0 + dy0

            x1 = gap - width
            h1 = round(float(s5[get_index(s5, to_t)][1]["count"])*height/s5_total)
            if h1 == 0.0:
                h1 = 1.0
            y1 = ((get_index(s5, to_t)+1)*height) - h1

            x2 = width
            h2 = round(float(content[to_t])*h0/content["count"])
            if h2 == 0.0:
                h2 = 1.0

            dy0 += h2
            y2 = y0 + h2

            x3 = gap - width
            h3 = round( float(content[to_t])*h1/s5[get_index(s5, to_t)][1]["count"] )
            if h3 == 0.0:
                h3 = 1.0
            y3 = y1 + h3

            links.append({
                "from": from_a,
                "to": to_a,
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "x3": x3,
                "y3": y3
            })


    return links

if __name__=="__main__":
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    gap = int(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])

    teams = trans_teams(data)
    nodes = nodes(data, gap, width, height)
    links = links(data, gap, width, height)

    out = {
        "teams": teams,
        "nodes": nodes,
        "links": links
    }

    with open("flow.json", "w") as f:
        json.dump(out, f, indent=4)
