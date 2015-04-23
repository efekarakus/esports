import sys, os, getopt
import csv
from dateutil.parser import parse
from datetime import datetime, timedelta
import json
import numpy

types = ["break", "analysis", "game"]
tournament_dates = {
    "csgo": {
        1: "March 12th",
        2: "March 13th",
        3: "March 14th",
        4: "March 15th"
    },
    "lol": {
        1: "March 13th (Group Stage)",
        2: "March 14th (Semi Finals)",
        3: "March 15th (Grand Finals)"
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
    "lol": {
        1: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (1, 0, 54)
            },
            {
                "type": 1,
                "start": (1, 0, 54),
                "end": (1, 7, 49)
            },
            {
                "type": 0,
                "start": (1, 7, 49),
                "end": (1, 8, 47)
            },
            {
                "type": 1,
                "start": (1, 8, 47),
                "end": (1, 24, 58)
            },
            {
                "type": 2,
                "teamA": "Cloud9",
                "teamB": "GE Tigers",
                "scoreA": 0,
                "scoreB": 1,
                "start": (1, 24, 58),
                "end": (2, 2, 7)
            },
            {
                "type": 1,
                "start": (2, 2, 7),
                "end": (2, 14, 2)
            },
            {
                "type": 0,
                "start": (2, 14, 2),
                "end": (2, 26, 34)
            },
            {
                "type": 1,
                "start": (2, 26, 34),
                "end": (2, 43, 49)
            },
            {
                "type": 2,
                "teamA": "SK Gaming",
                "teamB": "yoe Flash Wolves",
                "scoreA": 1,
                "scoreB": 0,
                "start": (2, 43, 49),
                "end": (3, 34, 31)
            },
            {
                "type": 1,
                "start": (3, 34, 31),
                "end": (3, 48, 54)
            },
            {
                "type": 0,
                "start": (3, 48, 54),
                "end": (3, 57, 46)
            },
            {
                "type": 1,
                "start": (3, 57, 46),
                "end": (4, 8, 29)
            },
            {
                "type": 2,
                "teamA": "GE Tigers",
                "teamB": "SK Gaming",
                "scoreA": 1,
                "scoreB": 0,
                "start": (4, 8, 29),
                "end": (4, 50, 25)
            },
            {
                "type": 1,
                "start": (4, 50, 25),
                "end": (5, 3, 1)
            },
            {
                "type": 0,
                "start": (5, 3, 1),
                "end": (5, 11, 28)
            },
            {
                "type": 1,
                "start": (5, 11, 28),
                "end": (5, 21, 42)
            },
            {
                "type": 2,
                "teamA": "Cloud9",
                "teamB": "yoe Flash Wolves",
                "scoreA": 0,
                "scoreB": 1,
                "start": (5, 21, 42),
                "end": (6, 16, 13)
            },
            {
                "type": 1,
                "start": (6, 16, 13),
                "end": (6, 30, 25)
            },
            {
                "type": 0,
                "start": (6, 30, 25),
                "end": (6, 38, 54)
            },
            {
                "type": 1,
                "start": (6, 38, 54),
                "end": (6, 55, 41)
            },
            {
                "type": 2,
                "teamA": "Gambit Gaming",
                "teamB": "CJ Entus",
                "scoreA": 0,
                "scoreB": 1,
                "start": (6, 55, 41),
                "end": (7, 48, 26)
            },
            {
                "type": 1,
                "start": (7, 48, 26),
                "end": (8, 1, 30)
            },
            {
                "type": 0,
                "start": (8, 1, 30),
                "end": (8, 10, 22)
            },
            {
                "type": 1,
                "start": (8, 10, 22),
                "end": (8, 25, 58)
            },
            {
                "type": 2,
                "teamA": "Team SoloMid",
                "teamB": "Team WE",
                "scoreA": 1,
                "scoreB": 0,
                "start": (8, 25, 58),
                "end": (9, 9, 18)
            },
            {
                "type": 1,
                "start": (9, 9, 18),
                "end": (9, 16, 5)
            },
            {
                "type": 0,
                "start": (9, 16, 5),
                "end": (9, 24, 34)
            },
            {
                "type": 1,
                "start": (9, 24, 34),
                "end": (9, 41, 23)
            },
            {
                "type": 2,
                "teamA": "CJ Entus",
                "teamB": "Team SoloMid",
                "scoreA": 0,
                "scoreB": 1,
                "start": (9, 41, 23),
                "end": (10, 19, 46)
            },
            {
                "type": 1,
                "start": (10, 19, 46),
                "end": (10, 29, 13)
            },
            {
                "type": 0,
                "start": (10, 29, 13),
                "end": (10, 38, 6)
            },
            {
                "type": 1,
                "start": (10, 38, 6),
                "end": (10, 50, 48)
            },
            {
                "type": 2,
                "teamA": "Team WE",
                "teamB": "Gambit Gaming",
                "scoreA": 1,
                "scoreB": 0,
                "start": (10, 50, 48),
                "end": (11, 29, 10)
            },
            {
                "type": 1,
                "start": (11, 29, 10),
                "end": (11, 39, 38)
            },
            {
                "type": 0,
                "start": (11, 39, 38),
                "end": (11, 44, 16)
            }
        ],
        2: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (0, 29, 46)
            },
            {
                "type": 1,
                "start": (0, 29, 46),
                "end": (0, 47, 30)
            },
            {
                "type": 2,
                "teamA": "SK Gaming",
                "teamB": "yoe Flash Wolves",
                "scoreA": 0,
                "scoreB": 1,
                "start": (0, 47, 30),
                "end": (1, 30, 14)
            },
            {
                "type": 1,
                "start": (1, 30, 14),
                "end": (1, 43, 57)
            },
            {
                "type": 0,
                "start": (1, 43, 57),
                "end": (1, 52, 26)
            },
            {
                "type": 1,
                "start": (1, 52, 26),
                "end": (2, 3, 20)
            },
            {
                "type": 2,
                "teamA": "Team WE",
                "teamB": "CJ Entus",
                "scoreA": 1,
                "scoreB": 0,
                "start": (2, 3, 20),
                "end": (2, 53, 27)
            },
            {
                "type": 1,
                "start": (2, 53, 27),
                "end": (3, 4, 57)
            },
            {
                "type": 0,
                "start": (3, 4, 57),
                "end": (3, 16, 44)
            },
            {
                "type": 1,
                "start": (3, 16, 44),
                "end": (3, 26, 43)
            },
            {
                "type": 2,
                "teamA": "Team SoloMid",
                "teamB": "yoe Flash Wolves",
                "scoreA": 0,
                "scoreB": 1,
                "start": (3, 26, 43),
                "end": (4, 13, 35)
            },
            {
                "type": 1,
                "start": (4, 13, 35),
                "end": (4, 21, 59)
            },
            {
                "type": 0,
                "start": (4, 21, 59),
                "end": (4, 29, 46)
            },
            {
                "type": 2,
                "teamA": "yoe Flash Wolves",
                "teamB": "Team SoloMid",
                "scoreA": 0,
                "scoreB": 1,
                "start": (4, 29, 46),
                "end": (5, 25, 48)
            },
            {
                "type": 1,
                "start": (5, 25, 48),
                "end": (5, 30, 29)
            },
            {
                "type": 0,
                "start": (5, 30, 29),
                "end": (5, 38, 59)
            },
            {
                "type": 1,
                "start": (5, 38, 59),
                "end": (5, 42, 55)
            },
            {
                "type": 2,
                "teamA": "yoe Flash Wolves",
                "teamB": "Team SoloMid",
                "scoreA": 0,
                "scoreB": 1,
                "start": (5, 42, 55),
                "end": (6, 23, 3)
            },
            {
                "type": 1,
                "start": (6, 23, 3),
                "end": (6, 32, 9)
            },
            {
                "type": 0,
                "start": (6, 32, 9),
                "end": (6, 41, 1)
            },
            {
                "type": 1,
                "start": (6, 41, 1),
                "end": (6, 50, 37)
            },
            {
                "type": 2,
                "teamA": "GE Tigers",
                "teamB": "Team WE",
                "scoreA": 1,
                "scoreB": 0,
                "start": (6, 50, 37),
                "end": (7, 33, 31)
            },
            {
                "type": 1,
                "start": (7, 33, 31),
                "end": (7, 39, 8)
            },
            {
                "type": 0,
                "start": (7, 39, 8),
                "end": (7, 47, 36)
            },
            {
                "type": 1,
                "start": (7, 47, 36),
                "end": (7, 49, 41)
            },
            {
                "type": 2,
                "teamA": "Team WE",
                "teamB": "GE Tigers",
                "scoreA": 1,
                "scoreB": 0,
                "start": (7, 49, 41),
                "end": (8, 26, 58)
            },
            {
                "type": 1,
                "start": (8, 26, 58),
                "end": (8, 32, 14)
            },
            {
                "type": 0,
                "start": (8, 32, 14),
                "end": (8, 41, 5)
            },
            {
                "type": 1,
                "start": (8, 41, 5),
                "end": (8, 41, 50)
            },
            {
                "type": 2,
                "teamA": "Team WE",
                "teamB": "GE Tigers",
                "scoreA": 1,
                "scoreB": 0,
                "start": (8, 41, 50),
                "end": (9, 16, 52)
            },
            {
                "type": 1,
                "start": (9, 16, 52),
                "end": (9, 30, 9)
            },
            {
                "type": 0,
                "start": (9, 30, 9),
                "end": (9, 33, 43)
            }
        ],
        3: [
            {
                "type": 0,
                "start": (0, 0, 0),
                "end": (0, 23, 30)
            },
            {
                "type": 1,
                "start": (0, 23, 30),
                "end": (0, 34, 59)
            },
            {
                "type": 2,
                "teamA": "Team WE",
                "teamB": "Team SoloMid",
                "scoreA": 0,
                "scoreB": 1,
                "start": (0, 34, 59),
                "end": (1, 23, 51)
            },
            {
                "type": 1,
                "start": (1, 23, 51),
                "end": (1, 27, 49)
            },
            {
                "type": 0,
                "start": (1, 27, 49),
                "end": (1, 35, 48)
            },
            {
                "type": 1,
                "start": (1, 35, 48),
                "end": (1, 38, 33)
            },
            {
                "type": 2,
                "teamA": "Team SoloMid",
                "teamB": "Team WE",
                "scoreA": 1,
                "scoreB": 0,
                "start": (1, 38, 33),
                "end": (2, 16, 20)
            },
            {
                "type": 1,
                "start": (2, 16, 20),
                "end": (2, 21, 3)
            },
            {
                "type": 0,
                "start": (2, 21, 3),
                "end": (2, 29, 24)
            },
            {
                "type": 1,
                "start": (2, 29, 24),
                "end": (2, 31, 22)
            },
            {
                "type": 2,
                "teamA": "Team WE",
                "teamB": "Team SoloMid",
                "scoreA": 0,
                "scoreB": 1,
                "start": (2, 31, 22),
                "end": (3, 3, 42)
            },
            {
                "type": 1,
                "start": (3, 3, 42),
                "end": (3, 11, 7)
            },
            {
                "type": 0,
                "start": (3, 11, 7),
                "end": (3, 22, 21)
            }
        ]
    }
}

def breaks(js):
    streams = js["streams"]
    number_breaks = 0
    breaks = []

    for stream in streams:
        areas = stream["areas"][1:len(stream["areas"])-2]
        for i in range(len(areas)):
            chunk = areas[i]
            if chunk["type"] == "break" and (areas[i-1]["type"] == "game" or areas[i-2]["type"] == "game"):
                number_breaks += 1
                start = chunk["points"][0]["count"]
                end = chunk["points"][-1]["count"]

                breaks.append(start - end)


    print number_breaks, numpy.mean(breaks), numpy.std(breaks)

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
    stats("lol")
    #js = structurize(get_streams("esl_csgo-pruned.csv"), "csgo")
    #breaks(js)

    js = structurize(get_streams("esl_lol-pruned.csv"), "lol")
    with open("esl_lol.json", "w") as f:
        json.dump(js, f)

    """
    js = structurize(get_streams("esl_csgo-pruned.csv"), "csgo")
    with open("esl_csgo.json", "w") as f:
        json.dump(js, f, indent=4)
    """