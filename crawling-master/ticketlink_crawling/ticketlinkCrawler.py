from perfomance_crawler import crawlPerformance
from sports_crawler import crawlSports
from config import BASEBALL_TEAMS, ESPORTS_TEAMS, SOCCER_TEAMS, ICEHOCKEY_TEAMS, HANDBALL_TEAMS
from utils import get_date_string
import pandas as pd

def ticketlinkCrawler():
    savePathPerformance = f'data/ticketlink/ticketPerformance.xlsx'
    savePathSports = f'data/ticketlink/ticketSports.xlsx'

    # 공연 데이터 엑셀저장
    df_performance = crawlPerformance()
    df_performance.to_excel(savePathPerformance, index=False)
    print(f"공연 엑셀 저장 완료: {savePathPerformance}")

    # 스포츠 데이터 엑셀저장
    df_baseball = crawlSports(BASEBALL_TEAMS, "야구")
    df_esports = crawlSports(ESPORTS_TEAMS, "이스포츠")
    df_soccer = crawlSports(SOCCER_TEAMS, "축구")
    df_icehockey = crawlSports(ICEHOCKEY_TEAMS, "아이스하키")
    df_handball = crawlSports(HANDBALL_TEAMS, "배구")

    with pd.ExcelWriter(savePathSports) as writer:
        df_baseball.to_excel(writer, sheet_name="야구", index=False)
        df_esports.to_excel(writer, sheet_name="이스포츠", index=False)
        df_soccer.to_excel(writer, sheet_name="축구", index=False)
        df_icehockey.to_excel(writer, sheet_name="아이스하키", index=False)
        df_handball.to_excel(writer, sheet_name="배구", index=False)

    print(f"스포츠 엑셀 저장 완료: {savePathSports}")

if __name__ == "__main__":
    ticketlinkCrawler()