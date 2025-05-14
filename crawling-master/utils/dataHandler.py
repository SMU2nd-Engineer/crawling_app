import pandas as pd
import pymysql

def excel_to_mysql():
  # DB 접속 정보
  DB_USER = 'culturemoa'
  DB_PASSWORD = 'culturemoa'
  DB_CONNECTION_STR = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/culturemoa'

  interpark = pd.read_excel('/data/interpark/interparkTicket.xlsx')
  interpark.to_sql(name='ticket_tbl', con=DB_CONNECTION_STR,  if_exists='append',index=False)

  melon = pd.read_excel('/data/melon/melonTicket.xlsx')
  melon.to_sql(name='ticket_tbl', con=DB_CONNECTION_STR,  if_exists='append',index=False)

  ticketlink = pd.read_excel('/data/ticketlink/ticketlinkTicket.xlsx')
  ticketlink.to_sql(name='ticket_tbl', con=DB_CONNECTION_STR,  if_exists='append',index=False)

if __name__ == "__main__":
    excel_to_mysql()