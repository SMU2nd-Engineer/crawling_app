from interparkCrawler.interparkCrawler import save_interpark_to_excel
from melonCrawler.melonCrawler import melonCrawler
from ticketlinkCrawler.ticketlinkCrawler import ticketlinkCrawler
import traceback
import pandas as pd
from sqlalchemy import create_engine
import pymysql

# DB 접속 정보
DB_USER = 'culturemoa'
DB_PASSWORD = 'culturemoa'
DB_CONNECTION_STR = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/culturemoa'

def main():
    # 인터파크 크롤링
    interpark = pd.DataFrame()
    try:
        print("Interpark 크롤링을 진행 합니다.")
        interpark = save_interpark_to_excel()
        print("Interpark 크롤링이 완료 되었습니다.\n")
    except Exception as e:
        print("Interpark 크롤링 중 오류가 발생했습니다.")
        print(f"에러: {e}")
        traceback.print_exc()

    # 인터파크 DB 저장
    # try:
    #     interpark.to_sql(name='ticket_tbl', con=DB_CONNECTION_STR,  if_exists='append', index=False)
    #     print("Interpark 데이터 DB 저장 완료")
    # except Exception as e:
    #     print("Interpark 데이터 DB 저장 중 오류가 발생했습니다. ")
    #     print(f"에러: {e}")
    #     traceback.print_exc()

    # 멜론 크롤링
    melon = pd.DataFrame()
    try:
        print("Melon 크롤링을 진행 합니다.")
        melon = melonCrawler()
        print("Melon 크롤링이 완료 되었습니다.\n")
    except Exception as e:
        print("Melon 크롤링 중 오류가 발생했습니다.")
        print(f"에러: {e}")
        traceback.print_exc()

    # # 멜론 DB 저장
    # try:
    #     melon.to_sql(name='ticket_tbl', con=DB_CONNECTION_STR,  if_exists='append', index=False)
    #     print("Melon 데이터 DB 저장 완료")
    # except Exception as e:
    #     print("Melon 데이터 DB 저장 중 오류가 발생했습니다. ")
    #     print(f"에러: {e}")
    #     traceback.print_exc()

    # 티켓링크 크롤링
    ticketlink = pd.DataFrame()
    try:
        print("Ticketlink 크롤링을 진행 합니다.")
        ticketlink = ticketlinkCrawler()
        print("Ticketlink 크롤링이 완료 되었습니다.\n")
    except Exception as e:
        print("Ticketlink 크롤링 중 오류가 발생했습니다.")
        print(f"에러: {e}")
        traceback.print_exc()

    # # 티켓링크 DB 저장
    # try:
    #     ticketlink.to_sql(name='ticket_tbl', con=DB_CONNECTION_STR,  if_exists='append', index=False)
    #     print("Ticketlink 데이터 DB 저장 완료")
    # except Exception as e:
    #     print("Ticketlink 데이터 DB 저장 중 오류가 발생했습니다. ")
    #     print(f"에러: {e}")
    #     traceback.print_exc()

if __name__ == "__main__":
    main()