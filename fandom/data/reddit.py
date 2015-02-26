import praw
r = praw.Reddit("League of Legends flair bot")

r.login()

r.get_flair("leagueoflegends", "malahay")
