import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import json
import re

output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 07-08 season
standard_stats_url = "https://fbref.com/en/comps/9/2007-2008/stats/2007-2008-Premier-League-Stats#all_stats_standard"
standard_req = requests.get(standard_stats_url)
standard_stats = BeautifulSoup(standard_req.text, "html.parser")

print(standard_stats)
shooting_stats_url = (
    "https://fbref.com/en/comps/9/2007-2008/shooting/2007-2008-Premier-League-Stats"
)
shooting_req = requests.get(shooting_stats_url)
shooting_stats = BeautifulSoup(shooting_req.text, "html.parser")

goalkeeping_stats_url = (
    "https://fbref.com/en/comps/9/2007-2008/keepers/2007-2008-Premier-League-Stats"
)
goalkeeping_req = requests.get(goalkeeping_stats_url)
goalkeeping_stats = BeautifulSoup(goalkeeping_req.text, "html.parser")

# matches.csv 불러와서 list형태로 저장 (07/08 ~ 21/22)
csv_matches = pd.read_csv("matches_ENG.csv", encoding="cp949")
f = open("matches_ENG.csv", "r")
reader = csv.reader(f)
data = list(reader)

data_of_a_season = {"home team": [], "away team": []}
home_team_stats = []
away_team_stats = []

table = standard_stats.select("table#stats_standard")
players = table.find_all("tr")
