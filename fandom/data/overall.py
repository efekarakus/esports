import json
import sys

def swapNS(t):
    ns_i = 0
    index = 0
    for team in t:
        if team["name"] == "NS":
            ns_i = index
            break
        index += 1
    if ns_i == len(t) - 1:
        return

    temp = t[-1]
    t[-1] = t[ns_i]
    t[ns_i] = temp

def get_teams(teams, season):
    t = []
    for team in teams:
        if not teams[team][season] == {}:
            details = teams[team][season]["details"]
            t.append({
                "name": team,
                "count": details["count"],
                "percentage": details["percentage"]
            })
    # endfor

    t = sorted(t, key=lambda team: team["percentage"])
    t.reverse()

    swapNS(t)

    return t

if __name__=="__main__":
    with open("na-flow.json", "r") as f:
        na = json.load(f)
    with open("eu-flow.json", "r") as f:
        eu = json.load(f)

    s4_na = get_teams(na["teams"], "4")
    s5_na = get_teams(na["teams"], "5")

    s4_eu = get_teams(eu["teams"], "4")
    s5_eu = get_teams(eu["teams"], "5")

    data = {
        "na": {
            "4": s4_na,
            "5": s5_na
        },
        "eu": {
            "4": s4_eu,
            "5": s5_eu
        }
    }

    with open("overall.json", "w") as f:
        json.dump(data, f, indent=4)
