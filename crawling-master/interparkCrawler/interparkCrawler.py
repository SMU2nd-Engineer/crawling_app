from interparkCrawler.base import get_driver
from interparkCrawler.crawler import crawl_genre
from interparkCrawler.crawler_sports import crawl_sports

import pandas as pd
import os

def interparkCrawler():

  # 결과 수집
  all_data = []

  driver = get_driver()

  # 공연
  # 장르 리스트: (url, 초기 스크롤 위치, 장르명)
  genres = [
      ("https://tickets.interpark.com/contents/genre/concert", 3001),
      ("https://tickets.interpark.com/contents/genre/musical", 3002),
      ("https://tickets.interpark.com/contents/genre/classic", 3005),
      ("https://tickets.interpark.com/contents/genre/exhibition", 3004)
      ("https://tickets.interpark.com/contents/genre/play", 3003),
      ("https://tickets.interpark.com/contents/genre/family", 3006),
      ("https://tickets.interpark.com/contents/genre/leisure", 3007)
  ]

  # 공연 장르 반복
  for url, genre in genres:
    ticket_data = crawl_genre(driver, url, genre)
    if ticket_data:
      df = pd.DataFrame(ticket_data)
      all_data.append(df)

  driver.quit()

  # 드라이버는 공연과 스포츠 별도로 사용
  driver = get_driver()
  sports_data = []

  # 스포츠
  # 스포츠 리스트
  sports_list = [
    'https://ticket.interpark.com/Contents/Sports/Bridge/baseball',
    'https://ticket.interpark.com/Contents/Sports/Bridge/Soccer',
    'https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE015',
    'https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE023'
  ]

  # 스포츠 반복
  for sport_url in sports_list:
    sports_ticket_data = crawl_sports(driver, sport_url)
    if sports_ticket_data:
      df = pd.DataFrame(sports_ticket_data)
      sports_data.append(df)

  driver.quit()

  all_genre_data = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
  all_sports_data = pd.concat(sports_data, ignore_index=True) if sports_data else pd.DataFrame()

  total_data = pd.concat([all_genre_data, all_sports_data], ignore_index=True)

  return total_data

def save_interpark_to_excel():
  file_path = r'data\interpark\interparkTicket.xlsx'
  total_data = interparkCrawler()

  # 파일 경로 존재 여부 확인 및 폴더 생성
  dir_name = os.path.dirname(file_path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

  # 엑셀로 저장
  with pd.ExcelWriter(file_path, engine='xlsxwriter', mode='w') as writer:  
    total_data.to_excel(writer, index=False)
  
  return total_data



