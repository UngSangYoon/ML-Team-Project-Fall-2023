# pip install unidecode
import pandas as pd
import os
import csv
import json

output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# matches.csv 불러와서 list로 불러오기 (02/03 ~ 21/22)
csv_matches = pd.read_csv("matches.csv", encoding="cp949")
f = open("matches.csv", "r")
reader = csv.reader(f)
data = list(reader)


# json 파일 list로 불러오기
with open("output/07_08_GK.json", "r") as f:
    gks = json.load(f)
with open("output/07_08_standard_stat.json", "r") as f:
    standard_stat = json.load(f)
with open("output/07_08_shooting_stat.json", "r") as f:
    shooting_stat = json.load(f)

data_of_a_season = {"home team": [], "away team": []}
home_team_stats = []
away_team_stats = []


# 선수 index 찾기
def find_index(list, team, name):
    for index in range(len(list)):
        if list[index][0] == team and list[index][1] == name:
            return index


# csv 파일에서 match data 읽어오기
for match in range(1903, 2283):
    if len(home_team_stats) == 11:
        data_of_a_season["home team"].append(home_team_stats)
        home_team_stats.clear()
    if len(away_team_stats) == 11:
        data_of_a_season["away team"].append(away_team_stats)
        away_team_stats.clear()
    for gk in range(5, 7):
        name = data[match][gk]
        if gk == 5:
            team = data[match][0]
        else:
            team = data[match][1]
        index = find_index(gks, team, name)
        if index == None:
            break
        position = "GK"
        age = gks[index][2]
        appearance = gks[index][3]
        save = gks[index][4]
        ga = gks[index][5]
        wins = gks[index][6]
        draws = gks[index][7]
        loses = gks[index][8]
        cs = gks[index][9]
        gk_stats = [
            position,
            age,
            appearance,
            save,
            ga,
            wins,
            loses,
            cs,
        ]
        if gk == 5:
            home_team_stats.append(gk_stats)
        else:
            away_team_stats.append(gk_stats)

    for player in range(7, 27):
        name = data[match][player]
        if player < 17:
            team = data[match][0]
        else:
            team = data[match][1]
        index = find_index(standard_stat, team, name)
        if index == None:
            break
        # stadard stat 가져오기
        position = standard_stat[index][2]
        age = standard_stat[index][3]
        appearance = standard_stat[index][4]
        gls = standard_stat[index][5]
        ast = standard_stat[index][6]
        pk_made = standard_stat[index][7]
        # shooting stat 가져오기
        index = find_index(shooting_stat, team, name)
        if index == None:
            break
        sot = shooting_stat[index][2]
        goal_per_sot = shooting_stat[index][3]

        stats = [
            position,
            age,
            appearance,
            gls,
            ast,
            pk_made,
            sot,
            goal_per_sot,
        ]
        if player < 17:
            home_team_stats.append(stats)
        else:
            away_team_stats.append(stats)

with open(
    os.path.join(output_folder, "07_08.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(data_of_a_season, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")
