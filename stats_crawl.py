# pip install unidecode
from unidecode import unidecode
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

standard_stats_url = (
    "https://fbref.com/en/comps/9/2007-2008/stats/2007-2008-Premier-League-Stats"
)
shooting_stats_url = (
    "https://fbref.com/en/comps/9/2007-2008/shooting/2007-2008-Premier-League-Stats"
)
goalkeeping_stats_url = (
    "https://fbref.com/en/comps/9/2007-2008/keepers/2007-2008-Premier-League-Stats"
)
driver = webdriver.Chrome()

# 골키퍼 스텟 가져오기
driver.implicitly_wait(10)
driver.get(goalkeeping_stats_url)
gks = []
num = 1
while True:
    if (num % 26) == 0:
        num += 1
    try:
        name = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[1]'.format(num)
        ).text
        team = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[4]'.format(num)
        ).text
        age = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[5]'.format(num)
        ).text
        appearance = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[10]'.format(num)
        ).text
        save = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[15]'.format(num)
        ).text
        ga = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[12]'.format(num)
        ).text
        wins = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[16]'.format(num)
        ).text
        draws = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[17]'.format(num)
        ).text
        loses = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[18]'.format(num)
        ).text
        cs = driver.find_element(
            By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[20]'.format(num)
        ).text
    except NoSuchElementException:
        break
    gks.append(
        (
            team,
            unidecode(name),
            float(age),
            float(appearance),
            float(save),
            float(ga),
            float(wins),
            float(draws),
            float(loses),
            float(cs),
        )
    )
    num += 1

with open(
    os.path.join(output_folder, "07_08_GK.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(gks, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")

# 모든 선수 stat가져오기
driver.implicitly_wait(10)
driver.get(standard_stats_url)

standard_stat = []
num = 1
while True:
    if (num % 26) == 0:
        num += 1
    try:
        name = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[1]'.format(num)
        ).text
        team = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[4]'.format(num)
        ).text
        position = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[3]'.format(num)
        ).text
        age = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[5]'.format(num)
        ).text
        appearance = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[10]'.format(num)
        ).text
        gls = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[19]'.format(num)
        ).text
        ast = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[20]'.format(num)
        ).text
        pk_made = driver.find_element(
            By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[15]'.format(num)
        ).text
        if pk_made == "":
            pk_made = 0
    except NoSuchElementException:
        break
    standard_stat.append(
        (
            team,
            unidecode(name),
            position,
            float(age),
            float(appearance),
            float(gls),
            float(ast),
            float(pk_made),
        )
    )
    num += 1

with open(
    os.path.join(output_folder, "07_08_standard_stat.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(standard_stat, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")

# shooting 스텟 가져오기
driver.implicitly_wait(10)
driver.get(shooting_stats_url)
shooting_stat = []
num = 1
while True:
    if (num % 26) == 0:
        num += 1
    try:
        name = driver.find_element(
            By.XPATH, '//*[@id="stats_shooting"]/tbody/tr[{0}]/td[1]'.format(num)
        ).text
        team = driver.find_element(
            By.XPATH, '//*[@id="stats_shooting"]/tbody/tr[{0}]/td[4]'.format(num)
        ).text
        sot = driver.find_element(
            By.XPATH, '//*[@id="stats_shooting"]/tbody/tr[{0}]/td[13]'.format(num)
        ).text
        goal_per_sot = driver.find_element(
            By.XPATH, '//*[@id="stats_shooting"]/tbody/tr[{0}]/td[15]'.format(num)
        ).text
        if goal_per_sot == "":
            goal_per_sot = 0
    except NoSuchElementException:
        break
    shooting_stat.append((team, unidecode(name), float(sot), float(goal_per_sot)))
    num += 1

with open(
    os.path.join(output_folder, "07_08_shooting_stat.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(shooting_stat, output_file, ensure_ascii=False)
    print(f"데이터가 파일에 저장되었습니다.")
