from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
import csv
import json
from collections import OrderedDict

file_data = OrderedDict()

output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# matches.csv 불러와서 list형태로 저장 (07/08 ~ 21/22)
csv_matches = pd.read_csv("matches.csv", encoding="cp949")
f = open("matches.csv", "r")
reader = csv.reader(f)
data = list(reader)

# 크롤링으로 선수 stat 가져오기
driver = webdriver.Chrome()
url = f"https://www.premierleague.com/players"
driver.get(url)
time.sleep(3)
driver.maximize_window()
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

data_of_a_season = {"home team": [], "away team": []}
# 07/08 시즌 (1~380), 08/09 시즌 (381 ~ 761) ...
home_team_stats = []
away_team_stats = []

for match in range(1, 381):
    if len(home_team_stats) == 14:
        data_of_a_season["home team"].append(home_team_stats)
        home_team_stats.clear()
    if len(away_team_stats) == 14:
        data_of_a_season["away team"].append(away_team_stats)
        away_team_stats.clear()
    for player in range(5, 33):
        # 선수 이름 검색
        time.sleep(2)
        search_box = driver.find_element(By.XPATH, '//*[@id="search-input"]')
        search_box.send_keys(data[match][player])
        search_box.send_keys("\n")
        time.sleep(2)

        # 최상단 선수 click
        driver.find_element(
            By.XPATH,
            '//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody/tr[1]/td[1]/a',
        ).click()
        time.sleep(2)

        # 포지션 확인, 없으면 다음 경기로
        try:
            position = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/nav/div/section[1]/div[2]/div[2]',
            ).text
        except NoSuchElementException:
            driver.find_element(
                By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
            ).click()
            break

        # stats click
        driver.find_element(
            By.XPATH, '//*[@id="mainContent"]/div[2]/div/div/nav/ul/li[2]/a'
        ).click()
        time.sleep(2)

        # 해당 시즌으로 이동
        driver.find_element(
            By.XPATH,
            '//*[@id="mainContent"]/div[2]/div/div/div/div/section/div[2]/div[2]',
        ).click()
        time.sleep(3)
        driver.find_element(
            By.XPATH,
            '//*[@id="mainContent"]/div[2]/div/div/div/div/section/div[2]/div[3]/ul/li[18]',
        ).click()
        time.sleep(1)

        # 출전수 확인 후 0이면 다음 경기로
        appearances = driver.find_element(
            By.XPATH,
            '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[1]/span/span',
        ).text
        if appearances == "0":
            driver.find_element(
                By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
            ).click()
            break

        # poistion에 따라 정보 다르게 가져오기
        if position == "Goalkeeper":
            # 1
            Wins = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[3]/span/span',
            ).text
            # 2
            Losses = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[4]/span/span',
            ).text
            # 3
            Clean_sheets = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[2]/span',
            ).text
            # 4
            Saves = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[2]/span',
            ).text
            # 5
            Penalties_Saved = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[3]/span',
            ).text
            # 6
            Punches = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[4]/span',
            ).text
            # 7
            High_claims = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[5]/span',
            ).text
            # 8
            Catches = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[6]/span',
            ).text
            # 9
            Sweeper_clearances = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[7]/span',
            ).text
            # 10
            Throw_outs = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[8]/span',
            ).text
            # 11
            Goal_Kicks = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[9]/span',
            ).text
            # 12
            Goals_Conceded = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[3]/span',
            ).text
            # 13
            Errors_leading_to_goal = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[4]/span',
            ).text

            appearances = float(appearances)
            stats = [
                position,
                float(Wins) / appearances,
                float(Losses) / appearances,
                float(Clean_sheets) / appearances,
                float(Saves) / appearances,
                float(Penalties_Saved) / appearances,
                float(Punches) / appearances,
                float(High_claims) / appearances,
                float(Catches) / appearances,
                float(Sweeper_clearances) / appearances,
                float(Throw_outs) / appearances,
                float(Goal_Kicks) / appearances,
                float(Goals_Conceded) / appearances,
                float(Errors_leading_to_goal) / appearances,
            ]
            if player < 19:
                home_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()
            else:
                away_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()

        elif position == "Defender":
            # 1
            Wins = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[3]/span/span',
            ).text
            # 2
            Losses = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[4]/span/span',
            ).text
            # 3
            Goals = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[4]/div/div[2]/span',
            ).text
            # 4
            Assists = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[2]/span',
            ).text
            # 5
            Passes = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[4]/span',
            ).text
            # 6
            Clean_sheets = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[2]/span',
            ).text
            # 7
            Tackles = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[4]/span',
            ).text
            # 8
            Tackle_success_rate = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[5]/span',
            ).text
            Tackle_success_rate = Tackle_success_rate[:-1]
            # 9
            Interceptions = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[8]/span',
            ).text
            # 10
            Clearances = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[9]/span',
            ).text
            # 11
            Recoveries = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[12]/span',
            ).text
            # 12
            Fouls = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[3]/div/div[4]/span',
            ).text
            # 13
            Accurate_long_balls = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[9]/span',
            ).text

            appearances = float(appearances)
            stats = [
                position,
                float(Wins) / appearances,
                float(Losses) / appearances,
                float(Goals) / appearances,
                float(Assists) / appearances,
                float(Passes),
                float(Clean_sheets) / appearances,
                float(Tackles) / appearances,
                float(Tackle_success_rate) / 100.0,
                float(Interceptions) / appearances,
                float(Clearances) / appearances,
                float(Recoveries) / appearances,
                float(Fouls) / appearances,
                float(Accurate_long_balls) / appearances,
            ]
            if player < 19:
                home_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()
            else:
                away_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()

        elif position == "Midfielder":
            # 1
            Wins = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[3]/span/span',
            ).text
            # 2
            Losses = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[4]/span/span',
            ).text
            # 3
            Goals = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[3]/span',
            ).text
            # 4
            Assists = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[2]/span',
            ).text
            # 5
            Passes = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[4]/span',
            ).text
            # 6
            Shots = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[9]/span',
            ).text
            # 7
            Shooting_accuracy = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[11]/span',
            ).text
            Shooting_accuracy = Shooting_accuracy[:-1]
            # 8
            Tackles = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[4]/div/div[2]/span',
            ).text
            # 9
            Tackle_success_rate = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[4]/div/div[3]/span',
            ).text
            Tackle_success_rate = Tackle_success_rate[:-1]
            # 10
            Interceptions = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[4]/div/div[5]/span',
            ).text
            # 11
            Recoveries = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[4]/div/div[8]/span',
            ).text
            # 12
            Fouls = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[3]/div/div[4]/span',
            ).text
            # 13
            Accurate_long_balls = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[9]/span',
            ).text

            appearances = float(appearances)
            stats = [
                position,
                float(Wins) / appearances,
                float(Losses) / appearances,
                float(Goals),
                float(Assists) / appearances,
                float(Passes),
                float(Shots) / appearances,
                float(Shooting_accuracy) / 100.0,
                float(Tackles) / appearances,
                float(Tackle_success_rate) / 100.0,
                float(Interceptions) / appearances,
                float(Recoveries) / appearances,
                float(Fouls) / appearances,
                float(Accurate_long_balls) / appearances,
            ]
            if player < 19:
                home_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()
            else:
                away_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()

        elif position == "Forward":
            # 1
            Wins = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[3]/span/span',
            ).text
            # 2
            Losses = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/div/div[4]/span/span',
            ).text
            # 3
            Goals = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[3]/span',
            ).text
            # 4
            Assists = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[2]/span',
            ).text
            # 5
            Passes = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[4]/span',
            ).text
            # 6
            Shots = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[9]/span',
            ).text
            # 7
            Shooting_accuracy = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[11]/span',
            ).text
            Shooting_accuracy = Shooting_accuracy[:-1]
            # 8
            Big_chances_missed = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[13]/span',
            ).text
            # 9
            Big_Chances_Created = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[5]/span',
            ).text
            # 10
            Penalties_scored = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[7]/span',
            ).text

            # 11
            Freekicks_scored = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[1]/div/div[8]/span',
            ).text

            # 12
            Crosses = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[2]/div/div[6]/span',
            ).text

            # 13
            Fouls = driver.find_element(
                By.XPATH,
                '//*[@id="mainContent"]/div[2]/div/div/div/div/ul/li[3]/div/div[4]/span',
            ).text

            appearances = float(appearances)
            stats = [
                position,
                float(Wins) / appearances,
                float(Losses) / appearances,
                float(Goals),
                float(Assists) / appearances,
                float(Passes),
                float(Shots) / appearances,
                float(Shooting_accuracy) / 100.0,
                float(Big_chances_missed) / appearances,
                float(Big_Chances_Created) / 100.0,
                float(Penalties_scored) / appearances,
                float(Freekicks_scored) / appearances,
                float(Crosses) / appearances,
                float(Fouls) / appearances,
            ]
            if player < 19:
                home_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()
            else:
                away_team_stats.append(stats)
                driver.find_element(
                    By.XPATH, "/html/body/header/div/nav/ul/li[11]/a"
                ).click()

with open(
    os.path.join(output_folder, "07_08.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(data_of_a_season, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")
