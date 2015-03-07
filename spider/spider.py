"""
Crawl match histories and timelines for 
professional League of Legends matches.

@author Efe Karakus
"""
import sys, os
import argparse, csv
import time
import urllib, json

GAMES_PATH = "./games.csv"
SLEEP_DELAY = 1.5 # sleep for 1.5 seconds between requests

class URL:
    PLATFORMS = {
        "NA": "TRLH1",
        "EU": "TRLH3",
        "LCK": "TRKR1"
    }
    OVERVIEW = "https://acs.leagueoflegends.com/v1/stats/game/%s/%s?gameHash=%s"
    TIMELINE = "https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s"

    def __init__(self, region, game_id, game_hash):
        self.region = region
        self.game_id = game_id
        self.game_hash = game_hash

    def get_overview_url(self):
        return URL.OVERVIEW % (URL.PLATFORMS[self.region], self.game_id, self.game_hash)

    def get_timeline_url(self):
        return URL.TIMELINE % (URL.PLATFORMS[self.region], self.game_id, self.game_hash)

class Team:
    @staticmethod
    def crawl(region, week, date, teamA, teamB, game_number, game_id, game_hash):
        path = "%s/%d/%s/" % (region, week, date)
        if not os.path.exists(path):
            os.makedirs(path)

        print path, teamA, teamB

        url = URL(region, game_id, game_hash)
        overview = json.loads( urllib.urlopen(url.get_overview_url()).read() )
        time.sleep(SLEEP_DELAY)
        timeline = json.loads( urllib.urlopen(url.get_timeline_url()).read() )

        details = ""
        if game_number != '':
            details = "-game%s" % (game_number)

        with open(path + ("%s-%s%s.json" % (teamA, teamB, details)), "w") as f:
            json.dump(overview, f, indent=4)

        with open(path + ("%s-%s%s-timeline.json" % (teamA, teamB, details)), "w") as f:
            json.dump(timeline, f, indent=4)

class Date:
    @staticmethod
    def crawl(region, week, date, games):
        games = [game for game in games if game["region"] == region and game["week"] == week and game["date"] == date]
        Games.crawl(games)

class Week:
    @staticmethod
    def crawl(region, week, games):
        games = [game for game in games if game["region"] == region and game["week"] == week]
        Games.crawl(games)

class Region:
    @staticmethod
    def crawl(region, games):
        games = [game for game in games if game["region"] == region]
        Games.crawl(games)

class Games:
    @staticmethod
    def crawl(games):
        for game in games:
            region = game["region"]
            week = game["week"]
            date = game["date"]
            teamA = game["teamA"]
            teamB = game["teamB"]
            gnumber = game["gamenumber"]
            gid = game["id"]
            ghash = game["hash"]

            Team.crawl(region, week, date, teamA, teamB, gnumber, gid, ghash)
            time.sleep(SLEEP_DELAY)

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
                "gamenumber": row[5],
                "id": row[6],
                "hash": row[7],
            })
    return games

if __name__=="__main__":
    games = games(GAMES_PATH)

    # Crawl all the dataset
    #Games.crawl(games)

    # Crawl only a week
    Week.crawl("EU", 7, games)
