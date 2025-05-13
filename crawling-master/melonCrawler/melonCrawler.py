# melon_crawler/melonCrawler.py

import time
import os
import pandas as pd
from datetime import datetime
from melonCrawler.base import createDriver, scrollToEnd
from melonCrawler.performance import getPerformanceDetails
from selenium.webdriver.common.by import By

def melonCrawler():
    # 날짜 기반 엑셀파일 저장 포멧
    # dateFormat = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 엑셀파일 상대경로로 저장 
    fileName = f'data/melon/melonTicket.xlsx'

    # 상대경로 지정된 폴더 없으면 저장 폴더 자동 생성 
    os.makedirs(os.path.dirname(fileName), exist_ok=True)

    # 웹 드라이버 시작
    driver = createDriver()
    driver.get("https://ticket.melon.com/concert/index.htm?genreType=GENRE_CON")
    time.sleep(2)

    # 전체 데이터 누적 리스트
    totalDetailData = []

    for tapNumber in range(1, 6):
        # 메뉴 클릭 (콘서트, 뮤지컬/연극, 팬클럽/팬미팅, 클래식. 전시/행사)         
        driver.find_element(By.XPATH, f'//*[@id="gnb_menu"]/ul/li[{tapNumber}]/a').click()
        time.sleep(2)
        # "전체" 필터 클릭
        driver.find_element(By.XPATH, '//*[@id="conts"]/div[2]/a[1]').click()
        time.sleep(2)

        # 페이지 전체 스크롤 내리는 함수 실행
        scrollToEnd(driver)
        time.sleep(2)

        # 공연(콘서트, 뮤지컬/연극, 팬클럽/팬미팅, 클래식. 전시/행사) 리스트 가져오기
        liList = driver.find_elements(By.XPATH, '//*[@id="perf_poster"]/li')
        print(f"총 {len(liList)}개의 공연 정보를 찾았습니다.")

        # detailDataList: 각 탭의 데이터 임시 저장 리스트 
        # totalDetailData: 전체 데이터 누적 리스트
        detailDataList = getPerformanceDetails(driver, liList)
        totalDetailData.extend(detailDataList)

    # 데이터 프레임으로 변환하여 엑셀 저장
    df = pd.DataFrame(totalDetailData)
    try:
        df.to_excel(fileName, index=False)
        print(f"엑셀 저장 완료: {fileName}")
    except PermissionError:
        print("엑셀 파일이 열려 있어서 저장할 수 없습니다. 파일을 닫고 다시 시도하세요.")

    # 드라이버 종료
    # driver.quit()

    print("멜론티켓 Performance 엑셀 저장 완료.")

