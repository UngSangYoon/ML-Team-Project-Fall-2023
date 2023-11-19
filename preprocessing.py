# pip install unidecode
import pandas as pd
import os
import csv
import json

output_folder = "dataset"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# matches.csv 불러와서 list로 불러오기 (02/03 ~ 21/22)
csv_matches = pd.read_csv("matches.csv", encoding="cp949")
f = open("matches.csv", "r")
reader = csv.reader(f)
data = list(reader)


# 선수 index 찾기
def find_index(list, team, name):
    can_index = []
    for index in range(len(list)):
        if list[index][1].lower().replace(" ", "").replace("-", "").replace(
            "'", ""
        ) == name.lower().replace(" ", "").replace("-", "").replace("'", ""):
            can_index.append(index)
    if len(can_index) == 1:
        return can_index[0]
    else:
        for index in can_index:
            if list[index][0] == team:
                return index

    # 일치하는 이름 없는 경우 검사
    for index in range(len(list)):
        if list[index][1].lower().replace(" ", "").replace(
            "-", ""
        ) == name.lower().replace(" ", "").replace("-", "").replace(
            "andrew", "andy"
        ).replace(
            "matthew", "matt"
        ).replace(
            "mathew", "mat"
        ).replace(
            "daniel", "danny"
        ).replace(
            "michael", "mike"
        ):
            can_index.append(index)
    if len(can_index) == 1:
        return can_index[0]
    else:
        for index in can_index:
            if list[index][0] == team:
                return index


seasons = [
    ["03_04", 381, 761],
    ["04_05", 761, 1141],
    ["05_06", 1141, 1522],
    ["06_07", 1522, 1903],
    ["07_08", 1903, 2283],
    ["08_09", 2283, 2663],
    ["09_10", 2663, 3043],
    ["10_11", 3043, 3423],
    ["11_12", 3423, 3803],
    ["12_13", 3803, 4183],
    ["13_14", 4183, 4563],
    ["14_15", 4563, 4943],
    ["15_16", 4943, 5323],
    ["16_17", 5323, 5703],
    ["17_18", 5703, 6083],
    ["18_19", 6083, 6463],
    ["19_20", 6463, 6843],
    ["20_21", 6843, 7223],
    ["21_22", 7223, 7600],
]

# 시즌 별로 json 파일 list로 불러오기
for season in seasons:
    with open("output/{0}_GK.json".format(season[0]), "r") as f:
        gks = json.load(f)
    with open("output/{0}_standard_stat.json".format(season[0]), "r") as f:
        standard_stat = json.load(f)
    with open("output/{0}_shooting_stat.json".format(season[0]), "r") as f:
        shooting_stat = json.load(f)

    data_of_a_season = []
    score_of_a_season = []
    home_team_stats = []
    away_team_stats = []

    # 시즌 별 선수 스텟 가져와 저장
    start = season[1]
    end = season[2]
    for match in range(start, end):
        if len(home_team_stats) == 11 and len(away_team_stats) == 11:
            home_team_stats = sum(home_team_stats, [])
            away_team_stats = sum(away_team_stats, [])
            data_of_a_season.append(home_team_stats + away_team_stats)
            home_score = float(data[match - 1][3])
            away_score = float(data[match - 1][4])
            score_of_a_season.append([home_score, away_score])
        away_team_stats = []
        home_team_stats = []
        # 키퍼 스텟 가져오기
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

    # 시즌 별 경기 결과 파일 저장
    with open(
        os.path.join(output_folder, "{0}_score.json".format(season[0])),
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(score_of_a_season, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")

    # 시즌 매치 별 선발 선수 스텟 파일 저장
    with open(
        os.path.join(output_folder, "{0}.json".format(season[0])),
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(data_of_a_season, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")
    print(len(score_of_a_season))
