# pip install unidecode
import pandas as pd
import os
import csv
import json

output_folder = "new_dataset"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# matches.csv 불러와서 list로 불러오기 (02/03 ~ 21/22)
csv_matches = pd.read_csv("matches.csv", encoding="cp949")
f = open("matches.csv", "r")
reader = csv.reader(f)
data = list(reader)


# team index 찾기
def find_team_index(list, team):
    for index in range(len(list)):
        if list[index][0] == team:
            return index


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
    ["17_18", 5703, 6083],
    ["18_19", 6083, 6463],
    ["19_20", 6463, 6843],
    ["20_21", 6843, 7223],
    ["21_22", 7223, 7600],
]

# 시즌 별로 json 파일 list로 불러오기
for season in seasons:
    with open("output/{0}_team_stat.json".format(season[0]), "r") as f:
        team_stat_list = json.load(f)
    with open("output/{0}_GK.json".format(season[0]), "r") as f:
        gks = json.load(f)
    with open("output/{0}_standard_stat.json".format(season[0]), "r") as f:
        standard_stat = json.load(f)
    with open("output/{0}_shooting_stat.json".format(season[0]), "r") as f:
        shooting_stat = json.load(f)
    with open("output/{0}_defensive_stat.json".format(season[0]), "r") as f:
        defensive_stat = json.load(f)
    with open("output/{0}_gca_stat.json".format(season[0]), "r") as f:
        gca_stat = json.load(f)

    data_of_a_season = []
    score_of_a_season = []
    home_team_stats = []
    away_team_stats = []

    # 시즌 별 팀, 선수 스텟 가져와 저장
    start = season[1]
    end = season[2]
    for match in range(start, end):
        if len(home_team_stats) == 12 and len(away_team_stats) == 12:
            home_team_stats = sum(home_team_stats, [])
            away_team_stats = sum(away_team_stats, [])
            data_of_a_season.append(home_team_stats + away_team_stats)
            home_score = float(data[match - 1][3])
            away_score = float(data[match - 1][4])
            score_of_a_season.append([home_score, away_score])
        away_team_stats = []
        home_team_stats = []
        # 팀 스텟 가져오기
        for i in range(2):
            team = data[match][i]
            index = find_team_index(team_stat_list, team)
            if index == None:
                break
            team_gls = team_stat_list[index][1]
            team_ast = team_stat_list[index][2]
            team_xgls = team_stat_list[index][3]
            team_xast = team_stat_list[index][4]
            team_ga = team_stat_list[index][5]
            team_wr = team_stat_list[index][6]
            team_dr = team_stat_list[index][7]
            team_lr = team_stat_list[index][8]
            team_csr = team_stat_list[index][9]
            team_sr = team_stat_list[index][10]

            team_stats = [
                team_gls,  # 팀 골
                team_xgls,  # 팀 기대 골 (provided by Opta)
                team_ast,  # 팀 어시스트
                team_xast,  # 팀 기대 어시스트 (provided by Opta)
                team_ga,  # 팀 실점률
                team_wr,  # 팀 승률
                team_dr,  # 팀 비길 확률
                team_lr,  # 팀 질 확률
            ]
            if i == 0:
                home_team_stats.append(team_stats)
            elif i == 1:
                away_team_stats.append(team_stats)

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
            # defensive stat 가져오기
            index = find_index(defensive_stat, team, name)
            tkl = defensive_stat[index][2]
            shot_block = defensive_stat[index][3]
            pass_block = defensive_stat[index][4]
            intercept = defensive_stat[index][5]
            clearance = defensive_stat[index][6]
            # gca stat 가져오기
            index = find_index(gca_stat, team, name)
            sca = gca_stat[index][2]
            gca = gca_stat[index][3]
            stats = [
                age,
                appearance,
                gls,
                ast,
                pk_made,
                sot,  # 유효 슈팅
                goal_per_sot,  # 골/유효슈팅
                tkl,  # 태클 수
                shot_block,
                pass_block,
                intercept,
                clearance,
                sca,  # shoot create action
                gca,  # goal create action
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
