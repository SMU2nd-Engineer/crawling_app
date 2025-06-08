import pandas as pd
import pymysql
from sqlalchemy import create_engine  # 이 줄 추가

def excel_to_mysql():
  # DB 접속 정보
  DB_USER = 'culturemoa'
  DB_PASSWORD = 'culturemoa'
  # DB_CONNECTION_STR = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/culturemoa'
  DB_CONNECTION_STR = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@culturemoa.cd2miikuq292.ap-northeast-2.rds.amazonaws.com:3306/culturemoa'

  column_mapping = {
    'sub_idx': 'SUB_IDX',
    'title': 'TITLE',
    'company': 'COMPANY',
    'link': 'LINK',
    'sdate': 'SDATE',
    'edate': 'EDATE',
    'place': 'PLACE',
    'price': 'PRICE',
    'grade': 'GRADE',
    'cast': 'CAST',
    'runningtime': 'RUNNINGTIME',
    'img': 'IMG',
    'etc': 'ETC'
  }

  interpark = pd.read_excel('C:/DEV/crawling/data/interparkTicket.xlsx')
  interpark.rename(columns=column_mapping)
  interpark.to_sql(name='TICKET_TBL', con=DB_CONNECTION_STR,  if_exists='append',index=False)

  melon = pd.read_excel('C:/DEV/crawling/data/melonTicket.xlsx')
  melon.rename(columns=column_mapping)
  melon.to_sql(name='TICKET_TBL', con=DB_CONNECTION_STR,  if_exists='append',index=False)

  ticketlink1 = pd.read_excel('C:/DEV/crawling/data/ticketlinkTicket.xlsx', sheet_name = '공연')
  ticketlink1.rename(columns=column_mapping)
  ticketlink1.to_sql(name='TICKET_TBL', con=DB_CONNECTION_STR,  if_exists='append', index=False)
  print("엑셀 → MySQL 저장 시도 완료")
  ticketlink2 = pd.read_excel('C:/DEV/crawling/data/ticketlinkTicket.xlsx', sheet_name = '야구')
  ticketlink2.rename(columns=column_mapping)
  ticketlink2.to_sql(name='TICKET_TBL', con=DB_CONNECTION_STR,  if_exists='append', index=False)
  print("엑셀 → MySQL 저장 시도 완료")
  ticketlink3 = pd.read_excel('C:/DEV/crawling/data/ticketlinkTicket.xlsx', sheet_name = '이스포츠')
  ticketlink3.rename(columns=column_mapping)
  ticketlink3.to_sql(name='TICKET_TBL', con=DB_CONNECTION_STR,  if_exists='append', index=False)
  print("엑셀 → MySQL 저장 시도 완료")
  ticketlink4 = pd.read_excel('C:/DEV/crawling/data/ticketlinkTicket.xlsx', sheet_name = '축구')
  ticketlink4.rename(columns=column_mapping)
  ticketlink4.to_sql(name='TICKET_TBL', con=DB_CONNECTION_STR,  if_exists='append', index=False)
  print("엑셀 → MySQL 저장 시도 완료")

if __name__ == "__main__":
    excel_to_mysql()