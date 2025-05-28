from ticketlinkCrawler.perfomance_crawler import crawlPerformance
from .sports_crawler import crawlSports
from .config import BASEBALL_TEAMS, ESPORTS_TEAMS, SOCCER_TEAMS, ICEHOCKEY_TEAMS, HANDBALL_TEAMS, SPORTS_NUM
import pandas as pd
import os
from datetime import datetime

def ticketlinkCrawler():
    # 디렉토리 존재 여부 확인 후 없으면 생성
    saveDir = 'data/ticketlink'
    os.makedirs(saveDir, exist_ok=True)

    # 현재 날짜 및 시간 가져오기
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')

    # 데이터 통합(공연+스포츠) 엑셀저장
    saveFilename = f'ticketlinkTicket_{timestamp}.xlsx'
    savePath = os.path.join(saveDir, saveFilename)

    # 공연 데이터 
    df_performance = crawlPerformance()

    # 스포츠 데이터
    df_baseball = crawlSports(BASEBALL_TEAMS, SPORTS_NUM)
    df_esports = crawlSports(ESPORTS_TEAMS, SPORTS_NUM)
    df_soccer = crawlSports(SOCCER_TEAMS, SPORTS_NUM)
    df_icehockey = crawlSports(ICEHOCKEY_TEAMS, SPORTS_NUM)
    df_handball = crawlSports(HANDBALL_TEAMS, SPORTS_NUM)

    with pd.ExcelWriter(savePath, engine='xlsxwriter') as writer:
        df_performance.to_excel(writer, sheet_name="공연", index=False)
        df_baseball.to_excel(writer, sheet_name="야구", index=False)
        df_esports.to_excel(writer, sheet_name="이스포츠", index=False)
        df_soccer.to_excel(writer, sheet_name="축구", index=False)
        df_icehockey.to_excel(writer, sheet_name="아이스하키", index=False)
        df_handball.to_excel(writer, sheet_name="배구", index=False)

    df_all = pd.concat([df_performance, df_baseball, df_esports, df_soccer, df_icehockey, df_handball], ignore_index=True)

    return df_all
