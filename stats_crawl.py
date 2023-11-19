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


for season in range(21, 22):
    standard_stats_url = "https://fbref.com/en/comps/9/20{0}-20{1}/stats/20{0}-20{1}-Premier-League-Stats".format(
        season, season + 1
    )
    shooting_stats_url = "https://fbref.com/en/comps/9/20{0}-20{1}/shooting/20{0}-20{1}-Premier-League-Stats".format(
        season, season + 1
    )
    goalkeeping_stats_url = "https://fbref.com/en/comps/9/20{0}-20{1}/keepers/20{0}-20{1}-Premier-League-Stats".format(
        season, season + 1
    )
    defensive_stats_url = "https://fbref.com/en/comps/9/20{0}-20{1}/defense/20{0}-20{1}-Premier-League-Stats#all_stats_defense".format(
        season, season + 1
    )
    Goal_Shot_Creation_url = "https://fbref.com/en/comps/9/20{0}-20{1}/gca/20{0}-20{1}-Premier-League-Stats#all_stats_gca".format(
        season, season + 1
    )
    driver = webdriver.Chrome()
    """
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
            if save == "":
                save = 0
            ga = driver.find_element(
                By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[12]'.format(num)
            ).text
            if ga == "":
                ga = 0
            wins = driver.find_element(
                By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[16]'.format(num)
            ).text
            if wins == "":
                wins = 0
            draws = driver.find_element(
                By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[17]'.format(num)
            ).text
            if draws == "":
                draws = 0
            loses = driver.find_element(
                By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[18]'.format(num)
            ).text
            if loses == "":
                loses = 0
            cs = driver.find_element(
                By.XPATH, '//*[@id="stats_keeper"]/tbody/tr[{0}]/td[20]'.format(num)
            ).text
            if cs == "":
                cs = 0
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
        os.path.join(output_folder, f"0{season}_0{season+1}_GK.json"),
        "w",
        encoding="utf-8",
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
            if gls == "":
                gls = 0
            ast = driver.find_element(
                By.XPATH, '//*[@id="stats_standard"]/tbody/tr[{0}]/td[20]'.format(num)
            ).text
            if ast == "":
                ast = 0
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
        os.path.join(output_folder, f"0{season}_0{season+1}_standard_stat.json"),
        "w",
        encoding="utf-8",
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
            if sot == "":
                sot = 0
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
        os.path.join(output_folder, f"{season}_{season+1}_shooting_stat.json"),
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(shooting_stat, output_file, ensure_ascii=False)
        print(f"데이터가 파일에 저장되었습니다.")
    """
    # 수비 스텟 가져오기
    driver.implicitly_wait(10)
    driver.get(defensive_stats_url)
    defensive_stat = []
    num = 1
    while True:
        if (num % 26) == 0:
            num += 1
        try:
            name = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[1]'.format(num)
            ).text
            team = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[4]'.format(num)
            ).text
            tkl = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[15]'.format(num)
            ).text
            if tkl == "":
                tkl = 0
            shot_block = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[18]'.format(num)
            ).text
            if shot_block == "":
                shot_block = 0
            pass_block = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[19]'.format(num)
            ).text
            if pass_block == "":
                pass_block = 0
            intercept = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[20]'.format(num)
            ).text
            if intercept == "":
                intercept = 0
            clearance = driver.find_element(
                By.XPATH, '//*[@id="stats_defense"]/tbody/tr[{0}]/td[22]'.format(num)
            ).text
            if clearance == "":
                clearance = 0
        except NoSuchElementException:
            break
        defensive_stat.append(
            (
                team,
                unidecode(name),
                float(tkl),
                float(shot_block),
                float(pass_block),
                float(intercept),
                float(clearance),
            )
        )
        num += 1

    with open(
        os.path.join(output_folder, f"{season}_{season+1}_defensive_stat.json"),
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(defensive_stat, output_file, ensure_ascii=False)
        print(f"데이터가 파일에 저장되었습니다.")

    # gca 스텟 가져오기
    driver.implicitly_wait(10)
    driver.get(Goal_Shot_Creation_url)
    gca_stat = []
    num = 1
    while True:
        if (num % 26) == 0:
            num += 1
        try:
            name = driver.find_element(
                By.XPATH, '//*[@id="stats_gca"]/tbody/tr[{0}]/td[1]'.format(num)
            ).text
            team = driver.find_element(
                By.XPATH, '//*[@id="stats_gca"]/tbody/tr[{0}]/td[4]'.format(num)
            ).text
            sca = driver.find_element(
                By.XPATH, '//*[@id="stats_gca"]/tbody/tr[{0}]/td[9]'.format(num)
            ).text
            if sca == "":
                sca = 0
            gca = driver.find_element(
                By.XPATH, '//*[@id="stats_gca"]/tbody/tr[{0}]/td[17]'.format(num)
            ).text
            if gca == "":
                gca = 0
        except NoSuchElementException:
            break
        gca_stat.append((team, unidecode(name), float(sca), float(gca)))
        num += 1

    with open(
        os.path.join(output_folder, f"{season}_{season+1}_gca_stat.json"),
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(gca_stat, output_file, ensure_ascii=False)
        print(f"데이터가 파일에 저장되었습니다.")
