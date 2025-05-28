from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from .utils import create_driver, get_current_year_month

def crawlSports(teams: dict, genre: int) -> pd.DataFrame:
    driver = create_driver()
    currentYear, currentMonth = get_current_year_month()

    detailDataList = []
    maxTry = 3

    for team_url, team_name in teams.items():
        url = "https://www.ticketlink.co.kr" + team_url
        driver.get(url)
        time.sleep(2)

        for _ in range(maxTry):
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        try:
            matches = driver.find_elements(By.CSS_SELECTOR, "div.reserve_lst_bx > ul > li")

            for match in range(1, len(matches) + 1):
                try:
                    time.sleep(2)
                    importedDate = driver.find_element(By.CSS_SELECTOR, f"div.reserve_lst_bx > ul > li:nth-child({match}) > div.match_day > div.date > span").text
                    eventMonth = int(importedDate.split('.')[0])
                    adjustedYear = currentYear
                    if currentMonth == 12 and eventMonth == 1:
                        adjustedYear += 1
                    date = f"{adjustedYear}.{importedDate}"

                    gameTime = driver.find_element(By.CSS_SELECTOR, f"div.reserve_lst_bx > ul > li:nth-child({match}) > div.match_day > div.day_time > div.time > span").text
                    mainTeamLogoImage = driver.find_element(By.CSS_SELECTOR, "div.team_logo > img").get_attribute("src")
                    place = driver.find_element(By.CSS_SELECTOR, f"#reservation > div.reserve_lst_bx > ul > li:nth-child({match}) > div.match_team_info > div:nth-child(3) > div").text   
                    link = url

                    matchTourName = ""
                    matchName = ""
                    matchTotal = ""

                    try:
                        matchInfoFound = driver.find_element(By.CSS_SELECTOR, f"#reservation > div.reserve_lst_bx > ul > li:nth-child({match}) > div.match_team_info > div:nth-child(2)")
                        childDivs = matchInfoFound.find_elements(By.TAG_NAME, "div")

                        if len(childDivs) >= 2:
                            matchTourName = childDivs[1].text
                            if len(childDivs) >= 3:
                                matchName = childDivs[2].text

                        if matchTourName and matchName:
                            matchTotal = matchTourName + " " + matchName
                        elif matchTourName:
                            matchTotal = matchTourName
                        elif matchName:
                            matchTotal = matchName

                    except Exception as e:
                        print(f"투어명/경기명 가져오기 실패: {e}")

                    time.sleep(2)
                    detailData = {
                        'sub_idx': genre,
                        'title': matchTotal,
                        'company': "티켓링크",
                        'link': link,
                        'sdate': date,
                        'edate': date,
                        'place': place,
                        'price': "",
                        'grade': "전연령",
                        'cast': "",
                        'runningtime': gameTime,
                        'img': mainTeamLogoImage,
                        'etc': ""
                    }
                    time.sleep(2)
                    print(detailData)
                    detailDataList.append(detailData)

                except Exception as e:
                    print(f"{team_name} 경기정보 하나 가져오기 실패: {e}")

        except Exception as e:
            print(f"{team_name} 페이지 접속 또는 경기 리스트 가져오기 실패: {e}")

    driver.quit()
    return pd.DataFrame(detailDataList)