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
with open("output/03_04_GK.json", "r") as f:
    gks = json.load(f)
with open("output/03_04_standard_stat.json", "r") as f:
    standard_stat = json.load(f)
with open("output/03_04_shooting_stat.json", "r") as f:
    shooting_stat = json.load(f)

data_of_a_season = {"home team": [], "away team": []}
home_team_stats = []
away_team_stats = []


# 선수 index 찾기
def find_index(list, team, name):
    can_index = []
    for index in range(len(list)):
        if list[index][1].lower().replace(" ", "").replace(
            "-", ""
        ) == name.lower().replace(" ", "").replace("-", ""):
            can_index.append(index)
    if len(can_index) == 1:
        return can_index[0]
    else:
        for index in can_index:
            if list[index][0] == team:
                return index

    # 일치하는 이름 없는 경우 andrew, matthew 검사
    for index in range(len(list)):
        if list[index][1].lower().replace(" ", "").replace(
            "-", ""
        ) == name.lower().replace(" ", "").replace("-", "").replace(
            "andrew", "andy"
        ).replace(
            "matthew", "matt"
        ):
            can_index.append(index)
    if len(can_index) == 1:
        return can_index[0]
    else:
        for index in can_index:
            if list[index][0] == team:
                return index


# csv 파일에서 match data 읽어오기
# 02-03 : 1,381
# 03-04 : 381, 744
for match in range(381, 744):
    if len(home_team_stats) == 11 and len(away_team_stats) == 11:
        globals()[f"home_team_stats_{match}"] = home_team_stats
        globals()[f"away_team_stats_{match}"] = away_team_stats
        data_of_a_season["home team"].append(globals()[f"home_team_stats_{match}"])
        data_of_a_season["away team"].append(globals()[f"away_team_stats_{match}"])
    away_team_stats = []
    home_team_stats = []
    for gk in range(5, 7):
        name = data[match][gk]
        if gk == 5:
            team = data[match][0]
        else:
            team = data[match][1]
        index = find_index(gks, team, name)
        if index == None:
            print(name)
            break
        age = gks[index][2]
        appearance = gks[index][3]
        save = gks[index][4]
        ga = gks[index][5]
        wins = gks[index][6]
        draws = gks[index][7]
        loses = gks[index][8]
        cs = gks[index][9]
        gk_stats = [
            age,
            appearance,
            save,  # 선방률
            ga,  # 실점률
            wins,
            draws,
            loses,
            cs,  # clean sheet 비율
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
            print(name)
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
            sot,  # 유효 슈팅
            goal_per_sot,  # 골/유효슈팅
        ]
        if player < 17:
            home_team_stats.append(stats)
        else:
            away_team_stats.append(stats)

with open(
    os.path.join(output_folder, "08_09.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(data_of_a_season, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")
print(len(data_of_a_season["home team"]))
print(len(data_of_a_season["away team"]))
