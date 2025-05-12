from interparkCrawler.base import get_driver
from interparkCrawler.crawler import crawl_genre
from interparkCrawler.crawler_sports import crawl_sports

import pandas as pd
import os

def interparkCrawler():

  # 결과 수집
  all_data = {}

  driver = get_driver()

  # 공연
  # 장르 리스트: (url, 초기 스크롤 위치, 장르명)
  genres = [
      ("https://tickets.interpark.com/contents/genre/concert", "콘서트"),
      ("https://tickets.interpark.com/contents/genre/musical", "뮤지컬"),
      ("https://tickets.interpark.com/contents/genre/classic", "클래식"),
      ("https://tickets.interpark.com/contents/genre/exhibition", "전시"),
      ("https://tickets.interpark.com/contents/genre/play", "연극"),
      ("https://tickets.interpark.com/contents/genre/family", "아동/가족"),
      ("https://tickets.interpark.com/contents/genre/leisure", "레저")
  ]

  # 공연 장르 반복
  for url, genre in genres:
    print(f"[{genre}] 크롤링 시작")
    ticket_data = crawl_genre(driver, url, genre)
    if ticket_data:
      df = pd.DataFrame(ticket_data)
      df['카테고리'] = genre
      all_data[genre] = df

  driver.quit()

  # 드라이버는 공연과 스포츠 별도로 사용
  driver = get_driver()
  sports_data = []

  # 스포츠
  # 스포츠 리스트
  sports_list = [
    ('https://ticket.interpark.com/Contents/Sports/Bridge/baseball', "야구"),
    ('https://ticket.interpark.com/Contents/Sports/Bridge/Soccer', "축구"),
    ('https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE015', "LCK"),
    ('https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE023', "VCT 퍼시픽 리그")
  ]

  # 스포츠 반복
  for sport_name, sport_url in sports_list:
    sports_ticket_data = crawl_sports(driver,sport_url, sport_name)
    if sports_ticket_data:
      df = pd.DataFrame(sports_ticket_data)
      df["카테고리"] = '스포츠'
      sports_data.append(df)

  driver.quit()

  all_genre_data = pd.concat(all_data.values(), ignore_index=True) if all_data else pd.DataFrame()
  all_sports_data = pd.concat(sports_data, ignore_index=True) if sports_data else pd.DataFrame()

  total_data = pd.concat([all_genre_data, all_sports_data], ignore_index=True)

  return total_data

def save_data_to_excel():
  file_path = r'data\interpark\interpark.xlsx'
  total_data = interparkCrawler()

  # 파일 경로 존재 여부 확인 및 폴더 생성
  dir_name = os.path.dirname(file_path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    print(f'폴더 생성완료: {dir_name}')

  # 엑셀로 저장
  with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
    # '카테고리' 기준으로 그룹핑 후 각각 시트로 저장
    for genre, df in total_data.groupby('카테고리'):
      sheet_name = genre[:31] # 엑셀 시트 최대 31자
      df.to_excel(writer, sheet_name=sheet_name, index=False)
      print(f'[{sheet_name}] 시트 저장 완료')

  print(f'엑셀에 저장 완료: {file_path}')




