"""
Crawl match histories and timelines for 
professional League of Legends matches.

@author Efe Karakus
"""
import sys
import csv
import argparse

GAMES_PATH = "./games.csv"

class Team:
    @staticmethod
    def crawl(region, week, date, teamA, teamB, game_id, game_hash):
        return

class Date:
    @staticmethod
    def crawl(region, week, date, data):
        return

class Week:
    @staticmethod
    def crawl(region, week, data):
        return

class Region:
    @staticmethod
    def crawl(region, data):
        return

class All:
    @staticmethod
    def crawl(data):
        return

def games(path):
    games = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            games.append({
                "region": row[0],
                "week": int(row[1]),
                "date": row[2],
                "teamA": row[3],
                "teamB": row[4],
                "id": row[5],
                "hash": row[6],
            })
    return games

if __name__=="__main__":
    games = games(GAMES_PATH)
    print games
