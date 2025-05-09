from crawlers.base import get_driver
from crawlers.crawler import crawl_genre
from crawlers.crawler_sports import crawl_sports

import pandas as pd

# 저장 경로
file_path = r'C:\DEV\크롤링\smu_project\ticket_info.xlsx'

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
    all_data[genre] = pd.DataFrame(ticket_data)

driver.quit()

# 드라이버는 공연과 스포츠 별도로 사용
driver = get_driver()
all_data_sports = []

# 스포츠
# 스포츠 리스트
sports_list = [
  ("야구", 'https://ticket.interpark.com/Contents/Sports/Bridge/baseball'),
  ("축구", 'https://ticket.interpark.com/Contents/Sports/Bridge/Soccer'),
  ("LCK", 'https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE015'),
  ("VCT 퍼시픽 리그", 'https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE023')
]

# 스포츠 반복
for sport_name, sport_url in sports_list:
  sports_ticket_data = crawl_sports(driver, sport_name, sport_url)
  all_data_sports.append(pd.DataFrame(sports_ticket_data))

driver.quit()

if all_data_sports:
  all_data['스포츠'] = pd.concat(all_data_sports, ignore_index=True)

with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
  for genre_name, df in all_data.items():
    if not df.empty:
      df.to_excel(writer, sheet_name=genre_name[:31], index=False)

print(f"모든 티켓 정보가 {file_path}에 저장되었습니다.")