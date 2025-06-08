from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from ticketlinkCrawler.config import SPORTS_NUM

import time
import re
from datetime import datetime

# 경기 날짜 추출 함수
def parse_num_display(elements):
  result = ''
  for el in elements:
    class_name = el.get_attribute('class')
    if 'num' in class_name:
      if 'dot' in class_name:
        result += '.'
      elif 'colon' in class_name:
        result += ':'
      else:
        parts = class_name.split()
        for part in parts:
          if part.startswith('num') and part != 'num':
            result += part.replace('num', '')
    elif 'date' in class_name:
      result += el.text.strip()
  return result

# 스포츠 정보 가져오는 함수
def sports_ticket_info(driver, count_ticket, img, current_url):

  # 티켓정보 가져오기
  sports_ticket = {
    'title': [],
    'company': [],
    'link': [],
    'sdate': [],
    'edate': [],
    'pdate': [],
    'place': [],
    'price': [],
    'grade': [],
    'cast': [],
    'runningtime': [],
    'img': [],
    'sub_idx': [],
    'etc': []
  }
  
  i = 1
  while i <= count_ticket:
    try:
      try:
        # 제목  
        team1 = driver.find_element(By.CSS_SELECTOR, f'div.timeScheduleList > div:nth-child({i}) > div.teamMatch > div.team1 > a:nth-child(2)').text
        team2 = driver.find_element(By.CSS_SELECTOR, f'div.timeScheduleList > div:nth-child({i}) > div.teamMatch > div.team2 > a:nth-child(2)').text
        title = team1 + ' VS ' + team2
      except NoSuchElementException:
        try: 
          title = driver.find_element(By.CSS_SELECTOR, f'div.timeScheduleList > div:nth-child({i}) > div.textInfoBox > p').text
        except NoSuchElementException:
          print(f'{i}번째 경기: 요소없음, 다음으로 건너뜀')
      # 경기 날짜
      date_elements = driver.find_elements(By.CSS_SELECTOR, f"div.timeScheduleList > div:nth-child({i}) > div.scheduleDate > div")
      time_elements = driver.find_elements(By.CSS_SELECTOR, f"div.timeScheduleList > div:nth-child({i}) > div.scheduleTime > div")
      
      date_str = parse_num_display(date_elements)
      time_str = parse_num_display(time_elements)

      current_year = datetime.now().year
      sdate = f'{current_year}.' + re.sub(r'\(.*?\)', '', date_str)
      edate = sdate

      # 수집 시각 (등록일)
      pdate = time.strftime("%Y-%m-%d")

      # 장소
      place = driver.find_element(By.CSS_SELECTOR, f'div.timeScheduleList > div:nth-child({i}) > div.ground > div > span').text

      # etc
      etc = time_str

      # sports_ticket에 직접 저장
      sports_ticket['sub_idx'].append(SPORTS_NUM)
      sports_ticket['title'].append(title)
      sports_ticket['company'].append("인터파크")  # 고정값
      sports_ticket['link'].append(current_url)
      sports_ticket['sdate'].append(sdate)
      sports_ticket['edate'].append(edate)
      sports_ticket['pdate'].append(pdate)
      sports_ticket['place'].append(place)
      sports_ticket['price'].append('')
      sports_ticket['grade'].append('전연령')
      sports_ticket['cast'].append('')
      sports_ticket['runningtime'].append(etc)
      sports_ticket['img'].append(img)
      sports_ticket['etc'].append('')

      print({k: sports_ticket[k][-1] for k in sports_ticket})

    except NoSuchElementException:
      print(f'{i}번째 경기: 요소없음, 다음으로 건너뜀')
      count_ticket += 1

    except Exception as e:
      print(f'{i}번째 경기 오류 발생: {e}')
      
    i += 1
  return sports_ticket


def crawl_sports(driver, sport_url):
  driver.get(sport_url)
  time.sleep(1)

  # 티켓정보 가져오기
  all_tickets = {
    'sub_idx': [], 'title': [], 'company': [], 'link': [], 'sdate': [], 'edate': [], 'pdate': [],
    'place': [], 'price': [], 'grade': [], 'cast': [], 'runningtime': [],
    'img': [], 'etc': []
  }

  # 예매카드 있는지 확인
  count_card = driver.find_elements(By.CLASS_NAME, 'listWrap')
  k = 1
  if count_card == []:
    k = 0
    img = ''

  current_url = driver.current_url
  
  while k <= len(count_card):
    if k > 1:
      driver.back()
      time.sleep(1)
    if count_card:
      # 이미지 저장
      img_selector = f'div.bridgeListWrapper > ul > li:nth-child({k}) > div > div.imgWrap > img'
      img = driver.find_element(By.CSS_SELECTOR, img_selector).get_attribute('src')
      # 예매하기 클릭
      xpath_booking = f'//*[@id="container"]/div/div[2]/ul/li[{k}]/div/button'
      driver.find_element(By.XPATH, xpath_booking).click()
      time.sleep(2)

    # 최근 링크
    current_url = driver.current_url
    k += 1
    # 더보기 버튼
    while True:
      try:
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        # 더보기 버튼 찾기
        more_button = driver.find_element(By.CSS_SELECTOR, 'a.moreBtn')
        
        more_button.click()
        time.sleep(2)

      except (ElementNotInteractableException, NoSuchElementException) as errorCode:
        print(f'더보기 버튼 못찾음:{errorCode.msg}')
        driver.execute_script("window.scrollTo(0, 500)")
        break
      except Exception as e:
        print(f'예외 발생:{e}')
        break

    # 티켓 개수      
    count_ticket = driver.find_elements(By.CLASS_NAME, 'timeSchedule')
    ticket_data = sports_ticket_info(driver, len(count_ticket), img, current_url)

    # 키(sport_url)별로 데이터 누적 저장하기
    for key in all_tickets:
      all_tickets[key].extend(ticket_data[key])

  return all_tickets
