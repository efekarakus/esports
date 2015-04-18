import sys, os, getopt
import csv
from dateutil.parser import parse
from datetime import datetime, timedelta
import json

types = ["break", "analysis", "game"]
tournament_dates = {
    "csgo": {
        1: "March 12th",
        2: "March 13th",
        3: "March 14th",
        4: "March 15th"
    }    
}


timeline = {
    "csgo": {
        1: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (0, 26, 0)
            },
            {
                "type": 1,
                "start": (0, 26, 0),
                "end": (0, 45, 1)
            },
            {
                "type": 0,
                "start": (0, 45, 1),
                "end": (0, 54, 26)
            },
            {
                "type": 1,
                "start": (0, 54, 26),
                "end": (1, 11, 50)
            },
            {
                "type": 0,
                "start": (1, 11, 50),
                "end": (1, 15, 0)
            },
            {
                "type": 1,
                "start": (1, 15, 0),
                "end": (1, 23, 39)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "Titan",
                "scoreA": 16,
                "scoreB": 14,
                "start": (1, 23, 39),
                "end": (2, 12, 33)
            },
            {
                "type": 1,
                "start": (2, 12, 33),
                "end": (2, 25, 24)
            },
            {
                "type": 0,
                "start": (2, 25, 24),
                "end": (2, 43, 37)
            },
            {
                "type": 1,
                "start": (2, 43, 37),
                "end": (2, 56, 56)
            },
            {
                "type": 0,
                "start": (2, 56, 56),
                "end": (2, 59, 45)
            },
            {
                "type": 1,
                "start": (2, 59, 45),
                "end": (3, 3, 34)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "LGB eSports",
                "scoreA": 16,
                "scoreB": 8,
                "start": (3, 3, 34),
                "end": (3, 39, 52)
            },
            {
                "type": 1,
                "start": (3, 39, 52),
                "end": (3, 50, 36)
            },
            {
                "type": 0,
                "start": (3, 50, 36),
                "end": (4, 4, 24)
            },
            {
                "type": 1,
                "start": (4, 4, 24),
                "end": (4, 20, 19)
            },
            {
                "type": 0,
                "start": (4, 20, 19),
                "end": (4, 22, 35)
            },
            {
                "type": 1,
                "start": (4, 22, 35),
                "end": (4, 23, 20)
            },
            {
                "type": 2,
                "teamA": "Natus Vincere",
                "teamB": "fnatic",
                "scoreA": 7,
                "scoreB": 16,
                "start": (4, 23, 20),
                "end": (5, 2, 32)
            },
            {
                "type": 1,
                "start": (5, 2, 32),
                "end": (5, 14, 1)
            },
            {
                "type": 0,
                "start": (5, 14, 1),
                "end": (5, 37, 57)
            },
            {
                "type": 1,
                "start": (5, 37, 57),
                "end": (6, 1, 37)
            },
            {
                "type": 2,
                "teamA": "Natus Vincere",
                "teamB": "Vox Eminor",
                "scoreA": 16,
                "scoreB": 3,
                "start": (6, 1, 37),
                "end": (6, 29, 7)
            },
            {
                "type": 1,
                "start": (6, 29, 7),
                "end": (6, 37, 57)
            },
            {
                "type": 0,
                "start": (6, 37, 57),
                "end": (6, 55, 46)
            },
            {
                "type": 1,
                "start": (6, 55, 46),
                "end": (7, 11, 25)
            }, 
            {
                "type": 0,
                "start": (7, 11, 25),
                "end": (7, 22, 6)
            },
            {
                "type": 1,
                "start": (7, 22, 6),
                "end": (7, 37, 30)
            },
            {
                "type": 0,
                "start": (7, 37, 30),
                "end": (7, 53, 12)
            },
            {
                "type": 1,
                "start": (7, 53, 12),
                "end": (7, 57, 41)
            },
            {
                "type": 2,
                "teamA": "Ninjas in Pyjamas",
                "teamB": "Counter Logic Gaming",
                "scoreA": 16,
                "scoreB": 7,
                "start": (7, 57, 41),
                "end": (8, 35, 53)
            },
            {
                "type": 1,
                "start": (8, 35, 53),
                "end": (8, 42, 48)
            },
            {
                "type": 0,
                "start": (8, 42, 48),
                "end": (8, 57, 1)
            },
            {
                "type": 1,
                "start": (8, 57, 1),
                "end": (9, 14, 1)
            },
            {
                "type": 0,
                "start": (9, 14, 1),
                "end": (9, 19, 21)
            },
            {
                "type": 1,
                "start": (9, 19, 21),
                "end": (9, 27, 1)
            },
            {
                "type": 2,
                "teamA": "Virtus.Pro",
                "teamB": "Cloud9 G2A",
                "scoreA": 16,
                "scoreB": 11,
                "start": (9, 27, 1),
                "end": (10, 17, 18)
            },
            {
                "type": 1,
                "start": (10, 17, 18),
                "end": (10, 27, 7)
            },
            {
                "type": 0,
                "start": (10, 27, 7),
                "end": (10, 41, 18)
            },
            {
                "type": 1,
                "start": (10, 41, 18),
                "end": (10, 56, 50)
            },
            {
                "type": 2,
                "teamA": "Cloud9 G2A",
                "teamB": "TSM Kinguin",
                "scoreA": 8,
                "scoreB": 16,
                "start": (10, 56, 50),
                "end": (11, 50, 52)
            },
            {
                "type": 1,
                "start": (11, 50, 52),
                "end": (11, 59, 6)
            },
            {
                "type": 0,
                "start": (11, 59, 6),
                "end": (12, 9, 26)
            }
        ],
        2: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (0, 22, 8)
            },
            {
                "type": 1,
                "start": (0, 22, 8),
                "end": (0, 36, 54)
            },
            {
                "type": 0,
                "start": (0, 36, 54),
                "end": (0, 42, 26)
            },
            {
                "type": 1,
                "start": (0, 42, 26),
                "end": (0, 58, 17)
            },
            {
                "type": 0,
                "start": (0, 58, 17),
                "end": (1, 1, 31)
            },
            {
                "type": 1,
                "start": (1, 1, 31),
                "end": (1, 2, 34)
            },
            {
                "type": 2,
                "teamA": "Natus Vincere",
                "teamB": "TEAM ENVYUS",
                "scoreA": 12,
                "scoreB": 16,
                "start": (1, 2, 34),
                "end": (1, 48, 5)
            },
            {
                "type": 1,
                "start": (1, 48, 5),
                "end": (1, 50, 47)
            },
            {
                "type": 0,
                "start": (1, 50, 47),
                "end": (1, 59, 38)
            },
            {
                "type": 1,
                "start": (1, 59, 38),
                "end": (2, 8, 50)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "Natus Vincere",
                "scoreA": 1,
                "scoreB": 0,
                "start": (2, 8, 50),
                "end": (2, 10, 25),
            },
            {
                "type": 1,
                "start": (2, 10, 25),
                "end": (2, 12, 0)
            },
            {
                "type": 0,
                "start": (2, 12, 0),
                "end": (2, 29, 19)
            },
            {
                "type": 1,
                "start": (2, 29, 19),
                "end": (2, 30, 53)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "Natus Vincere",
                "scoreA": 14,
                "scoreB": 16,
                "start": (2, 30, 53),
                "end": (3, 22, 45)
            },
            {
                "type": 1,
                "start": (3, 22, 45),
                "end": (3, 24, 25)
            },
            {
                "type": 0,
                "start": (3, 24, 25),
                "end": (3, 34, 18)
            },
            {
                "type": 1,
                "start": (3, 34, 18),
                "end": (3, 43, 35)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "Natus Vincere",
                "scoreA": 16,
                "scoreB": 3,
                "start": (3, 43, 35),
                "end": (4, 12, 42)
            },
            {
                "type": 1,
                "start": (4, 12, 42),
                "end": (4, 21, 20)
            },
            {
                "type": 0,
                "start": (4, 21, 20),
                "end": (4, 37, 45)
            },
            {
                "type": 1,
                "start": (4, 37, 45),
                "end": (5, 4, 22)
            },
            {
                "type": 0,
                "start": (5, 4, 22),
                "end": (5, 7, 42)
            },
            {
                "type": 1,
                "start": (5, 7, 42),
                "end": (5, 12, 12)
            },
            {
                "type": 2,
                "teamA": "PENTA Sports",
                "teamB": "fnatic",
                "scoreA": 8,
                "scoreB": 16,
                "start": (5, 12, 12),
                "end": (5, 59, 25)
            },
            {
                "type": 1,
                "start": (5, 59, 25),
                "end": (6, 1, 21)
            },
            {
                "type": 0,
                "start": (6, 1, 21),
                "end": (6, 10, 57)
            },
            {
                "type": 1,
                "start": (6, 10, 57),
                "end": (6, 12, 34)
            },
            {
                "type": 2,
                "teamA": "fnatic",
                "teamB": "PENTA Sports",
                "scoreA": 16,
                "scoreB": 7,
                "start": (6, 12, 34),
                "end": (6, 47, 45)
            },
            {
                "type": 1,
                "start": (6, 47, 45),
                "end": (6, 53, 30)
            },
            {
                "type": 0,
                "start": (6, 53, 30),
                "end": (7, 12, 48)
            },
            {
                "type": 1,
                "start": (7, 12, 48),
                "end": (7, 36, 38)
            },
            {
                "type": 2,
                "teamA": "Virtus.Pro",
                "teamB": "Keyd Stars",
                "scoreA": 16,
                "scoreB": 4,
                "start": (7, 36, 38),
                "end": (8, 9, 2)
            },
            {
                "type": 1,
                "start": (8, 9, 2),
                "end": (8, 10, 4)
            },
            {
                "type": 0,
                "start": (8, 10, 4),
                "end": (8, 19, 42)
            },
            {
                "type": 1,
                "start": (8, 19, 42),
                "end": (8, 27, 8)
            },
            {
                "type": 2,
                "teamA": "Virtus.Pro",
                "teamB": "Keyd Stars",
                "scoreA": 17,
                "scoreB": 19,
                "start": (8, 27, 8),
                "end": (9, 33, 23)
            },
            {
                "type": 1,
                "start": (9, 33, 23),
                "end": (9, 35, 26)
            },
            {
                "type": 0,
                "start": (9, 35, 26),
                "end": (9, 46, 50)
            },
            {
                "type": 1,
                "start": (9, 46, 50),
                "end": (10, 0, 50)
            },
            {
                "type": 2,
                "teamA": "Virtus.Pro",
                "teamB": "Keyd Stars",
                "scoreA": 16,
                "scoreB": 1,
                "start": (10, 0, 50),
                "end": (10, 30, 28)
            },
            {
                "type": 1,
                "start": (10, 30, 28),
                "end": (10, 39, 28)
            },
            {
                "type": 0,
                "start": (10, 39, 28),
                "end": (10, 44, 38)
            }
        ],
        3: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (0, 24, 48)
            },
            {
                "type": 1,
                "start": (0, 24, 48),
                "end": (0, 40, 28)
            },
            {
                "type": 0,
                "start": (0, 40, 28),
                "end": (0, 44, 5)
            },
            {
                "type": 1,
                "start": (0, 44, 5),
                "end": (0, 59, 39)
            },
            {
                "type": 0,
                "start": (0, 59, 39),
                "end": (1, 2, 59)
            },
            {
                "type": 1,
                "start": (1, 2, 59),
                "end": (1, 5, 52)
            },
            {
                "type": 2,
                "teamA": "TSM Kinguin",
                "teamB": "Ninjas in Pyjamas",
                "scoreA": 8,
                "scoreB": 16,
                "start": (1, 5, 52),
                "end": (1, 51, 48)
            },
            {
                "type": 1,
                "start": (1, 51, 48),
                "end": (1, 53, 19)
            },
            {
                "type": 0,
                "start": (1, 53, 19),
                "end": (2, 3, 55)
            },
            {
                "type": 1,
                "start": (2, 3, 55),
                "end": (2, 10, 46)
            },
            {
                "type": 2,
                "teamA": "Ninjas in Pyjamas",
                "teamB": "TSM Kinguin",
                "scoreA": 4,
                "scoreB": 16,
                "start": (2,10,46),
                "end": (2, 49, 52)
            },
            {
                "type": 1,
                "start": (2, 49, 52),
                "end": (2, 51, 10)
            },
            {
                "type": 0,
                "start": (2, 51, 10),
                "end": (3, 1, 57)
            },
            {
                "type": 1,
                "start": (3, 1, 57),
                "end": (3, 12, 46)
            },
            {
                "type": 2,
                "teamA": "Ninjas in Pyjamas",
                "teamB": "TSM Kinguin",
                "scoreA": 16,
                "scoreB": 12,
                "start": (3, 12, 46),
                "end": (4, 3, 9)
            },
            {
                "type": 1,
                "start": (4, 3, 9),
                "end": (4, 13, 21)
            },
            {
                "type": 0,
                "start": (4, 13, 21),
                "end": (4, 29, 41)
            },
            {
                "type": 1,
                "start": (4, 29, 41),
                "end": (4, 50, 1)
            },
            {
                "type": 2,
                "teamA": "fnatic",
                "teamB": "Virtus.Pro",
                "scoreA": 19,
                "scoreB": 17,
                "start": (4, 50, 1),
                "end": (6, 2, 34)
            },
            {
                "type": 1,
                "start": (6, 2, 34),
                "end": (6, 3, 56)
            },
            {
                "type": 0,
                "start": (6, 3, 56),
                "end": (6, 19, 13)
            },
            {
                "type": 1,
                "start": (6, 19, 13),
                "end": (6, 27, 26)
            },
            {
                "type": 2,
                "teamA": "fnatic",
                "teamB": "Virtus.Pro",
                "scoreA": 16,
                "scoreB": 8,
                "start": (6,27, 26),
                "end": (7, 10, 41)
            },
            {
                "type": 1,
                "start": (7, 10, 41),
                "end": (7, 18, 24)
            },
            {
                "type": 0,
                "start": (7, 18, 24),
                "end": (7, 42, 45)
            },
            {
                "type": 1,
                "start": (7, 42, 45),
                "end": (8, 4, 46)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "Ninjas in Pyjamas",
                "scoreA": 9,
                "scoreB": 16,
                "start": (8, 4, 46),
                "end": (8, 48, 55)
            },
            {
                "type": 1,
                "start": (8, 48, 55),
                "end": (8, 51, 11)
            },
            {
                "type": 0,
                "start": (8, 51, 11),
                "end": (9, 3, 24)
            },
            {
                "type": 1,
                "start": (9, 3, 24),
                "end": (9, 11, 50)
            },
            {
                "type": 2,
                "teamA": "TEAM ENVYUS",
                "teamB": "Ninjas in Pyjamas",
                "scoreA": 10,
                "scoreB": 16,
                "start": (9, 11, 50),
                "end": (9, 51, 21)
            },
            {
                "type": 1,
                "start": (9, 51, 21),
                "end": (10, 1, 44)
            },
            {
                "type": 0,
                "start": (10, 1, 44),
                "end": (10, 8, 4)
            }
        ],
        4: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (0, 18, 29)
            },
            {
                "type": 1,
                "start": (0, 18, 29),
                "end": (0, 32, 15)
            },
            {
                "type": 0,
                "start": (0, 32, 15),
                "end": (0, 36, 28)
            },
            {
                "type": 1,
                "start": (0, 36, 28),
                "end": (0, 40, 9)
            },
            {
                "type": 2,
                "teamA": "fnatic",
                "teamB": "Ninjas in Pyjamas",
                "scoreA": 16,
                "scoreB": 14,
                "start": (0, 40, 9),
                "end": (1, 38, 41)
            },
            {
                "type": 1,
                "start": (1, 38, 41),
                "end": (1, 41, 16)
            },
            {
                "type": 0,
                "start": (1, 41, 16),
                "end": (1, 49, 46)
            },
            {
                "type": 1,
                "start": (1, 49, 46),
                "end": (1, 54, 4)
            },
            {
                "type": 2,
                "teamA": "fnatic",
                "teamB": "Ninjas in Pyjamas",
                "scoreA": 10,
                "scoreB": 16,
                "start": (1, 54, 4),
                "end": (2, 38, 24)
            },
            {
                "type": 1,
                "start": (2, 38, 24),
                "end": (2, 41, 0)
            },
            {
                "type": 0,
                "start": (2, 41, 0),
                "end": (2, 49, 10)
            },
            {
                "type": 1,
                "start": (2, 49, 10),
                "end": (2, 51, 52)
            },
            {
                "type": 2,
                "teamA": "fnatic",
                "teamB": "Ninjas in Pyjamas",
                "scoreA": 16,
                "scoreB": 13,
                "start": (2, 51, 52),
                "end": (3, 48, 31)
            },
            {
                "type": 1,
                "start": (3, 48, 31),
                "end": (3, 56, 35)
            },
            {
                "type": 0,
                "start": (3, 56, 35),
                "end": (4, 0, 50)
            }
        ]
    },
    "lol": {}
}

def stats(game):
    print "Game: ", game
    print ""

    break_total = 0
    analysis_total = 0
    game_total = 0
    for sid in timeline[game]:
        
        break_time = 0
        analysis_time = 0
        game_time = 0

        print "Stream %d" % sid
        print "--------"
        for chunk in timeline[game][sid]:
            t = chunk["type"]
            start = timedelta(hours=chunk["start"][0], minutes=chunk["start"][1], seconds=chunk["start"][2])
            end = timedelta(hours=chunk["end"][0], minutes=chunk["end"][1], seconds=chunk["end"][2])

            delta = (end - start).total_seconds()
            if t == 0:
                break_time += delta
            elif t == 1:
                analysis_time += delta
            else:
                game_time += delta
        # endfor
        print "Break: %d hours, %d minutes, %d seconds" % (break_time / 3600, (break_time - (int(break_time/3600) * 3600)) / 60, break_time % 60)
        print "Analysis: %d hours, %d minutes, %d seconds" % (analysis_time / 3600, (analysis_time - (int(analysis_time/3600) * 3600)) / 60, analysis_time % 60)
        print "Game: %d hours, %d minutes, %d seconds" % (game_time / 3600, (game_time - (int(game_time/3600) * 3600)) / 60, game_time % 60)
        print ""

        break_total += break_time
        analysis_total += analysis_time
        game_total += game_time

    print "Total Break: %d hours, %d minutes, %d seconds" % (break_total / 3600, (break_total - (int(break_total/ 3600) * 3600)) / 60, break_total % 60)
    print "Total Analysis: %d hours, %d minutes, %d seconds" % (analysis_total / 3600, (analysis_total - (int(analysis_total/3600) * 3600))/ 60, analysis_total % 60)
    print "Total Game: %d hours, %d minutes, %d seconds" % (game_total / 3600, (game_total - (int(game_total/3600) * 3600))/ 60, game_total % 60)

def get_streams(path):
    streams = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        sid = None
        partials = []

        for row in reader:
            rid = int(row[0])
            rstreamer = row[1]
            rcount = int(row[2])
            rtime = parse(row[3])

            if sid != rid:
                if partials:
                    streams.append(partials)
                sid = rid
                partials = []

            partials.append({
                'id': rid,
                'streamer': rstreamer,
                'count': rcount,
                'timestamp': rtime
            })
        if partials:
            streams.append(partials)
    return streams

def get_closest_timestamp(partials, t):
    closest = datetime(year=2016, month=1, day=1)
    diff = (closest - t).total_seconds()
    for partial in partials:
        timestamp = partial["timestamp"]
        d = abs((timestamp - t).total_seconds())
        if d < diff:
            closest = timestamp
            diff = d
    return closest

def get_points(start, end, partials):
    points = []
    for partial in partials:
        timestamp = partial["timestamp"]
        cstart = get_closest_timestamp(partials, start)
        cend = get_closest_timestamp(partials, end)
        if timestamp >= cstart and timestamp <= cend:
            points.append({
                    "count": partial["count"],
                    "timestamp": str(timestamp)
                })
    return points

def structurize(streams, game):
    struc = { "streams": [] }
    for partials in streams:
        sid = partials[0]['id']
        print sid
        stream_start = partials[0]["timestamp"]
        if not sid in timeline[game]: continue

        js = {}
        js["day"] = tournament_dates[game][sid]
        js["stream_id"] = sid
        js["areas"] = []

        timesteps = timeline[game][sid]
        for timestep in timesteps:
            ttype = types[ timestep["type"] ] # break, analysis, or game
            
            start = stream_start + timedelta(hours=timestep["start"][0], minutes=timestep["start"][1], seconds=timestep["start"][2])
            end = stream_start + timedelta(hours=timestep["end"][0], minutes=timestep["end"][1], seconds=timestep["end"][2])
            
            points = get_points(start, end, partials)

            if ttype == "game":
                js["areas"].append({
                        "type": ttype,
                        "teamA": timestep["teamA"],
                        "teamB": timestep["teamB"],
                        "scoreA": timestep["scoreA"],
                        "scoreB": timestep["scoreB"],
                        "points": points
                    })
            else:
                js["areas"].append({
                        "type": ttype,
                        "points": points
                    })

        struc["streams"].append(js)
    # endfor partials
    return struc


if __name__ == '__main__':
    stats("csgo")

    """
    js = structurize(get_streams("esl_csgo-pruned.csv"), "csgo")
    with open("esl_csgo.json", "w") as f:
        json.dump(js, f, indent=4)
    """