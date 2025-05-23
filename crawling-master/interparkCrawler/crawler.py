from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def ticket_info(driver, concert_ticket, visited_titles, start_idx, end_idx, current_scroll, genre):
  for i in range(start_idx, end_idx + 1):
    if genre == 3006:
      xpath = f'//*[@id="contents"]/article[5]/section/div[2]/div[2]/a[{i}]'
    else:
      xpath = f'//*[@id="contents"]/article[4]/section/div[2]/div[2]/a[{i}]'
    concert = driver.find_elements(By.XPATH, xpath)
    if not concert:
        print(f'공연 요소가 없음: {xpath}')
        continue

    try:
      title_xpath = f'{xpath}/ul/li[1]'
      title = driver.find_element(By.XPATH, title_xpath).text

      if title in visited_titles:
        continue

      # 공연 내용 로딩될때까지 기다리기
      try:
        concert[0].click()
        time.sleep(2.5)
      except (TimeoutException, TimeoutError):
        print("공연 내용이 다시 로딩되지 않았습니다.")
        concert[0].click()
        print(f'{title} 클릭 재시도')
        time.sleep(2.5)
      except Exception as e:
        print(f'공연 클릭 실패: {e}')
      print(f'{title} 공연클릭 완료')

      current_url = driver.current_url
      if current_url == "data:,":
        driver.back()
        time.sleep(1)
        continue
      
      # 팝업 제거
      try:
        popup = driver.find_element(By.XPATH, '//*[@id="popup-prdGuide"]/div/div[3]/button/span')
        popup.click() 
        print('팝업을 제거했습니다')
      except:
        popup = None

      print(f'{title} 공연정보 추출 시작')
      period = driver.find_element(By.CSS_SELECTOR, ".infoText").text
      sdate, edate = (period.split(" ~") if " ~" in period else (period, period))
      # edate가 '오픈런' 일때 값 변경하기
      if edate.strip() == '오픈런':
        sdate = edate
        
      place = driver.find_element(By.CSS_SELECTOR, ".infoBtn").text.replace("(자세히)", "")
      img = driver.find_element(By.CSS_SELECTOR, ".posterBoxImage").get_attribute("src")

      try:
        text = driver.find_element(By.CSS_SELECTOR, "div.summaryBody > ul > li:nth-child(3) > strong").text
        if text == '공연시간':
          runningtime = driver.find_element(By.CSS_SELECTOR, "div.summaryBody > ul > li:nth-child(3) > div > p").text
          grade = driver.find_element(By.CSS_SELECTOR, "div.summaryBody > ul > li:nth-child(4) > div > p").text
        elif text == '관람연령':
          runningtime = ''
          grade = driver.find_element(By.CSS_SELECTOR, "div.summaryBody > ul > li:nth-child(3) > div > p").text
        else:
          runningtime = ''
          grade = ''
      except:
        runningtime = ''
        grade = ''

      try:
        driver.find_element(By.CSS_SELECTOR, "li.infoItem.infoPrice > div > ul > li:nth-child(2)")
        price = driver.find_element(By.CSS_SELECTOR, "li.infoItem.infoPrice > div > ul").text.replace("전체가격보기 (자세히)\n", "").replace("\n", "/")
      except NoSuchElementException:
        try:
          popup = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/div/div[2]/ul/li[5]/div/ul/li/a')
          driver.execute_script("arguments[0].click();", popup)
          time.sleep(1)
          price = driver.find_element(By.CSS_SELECTOR, "#popup-info-price > div > div.popupBody > div > div > table > tbody").text.replace("\n", "/")
        except:
          price = "가격 정보 없음"

      cast_elements = driver.find_elements(By.CSS_SELECTOR, "div.castingName")
      cast = "/".join([el.text.strip() for el in cast_elements if el.text.strip()]) if cast_elements else ""

      try:
        etc = driver.find_element(By.CSS_SELECTOR, 'div.contentDetail').text
      except:
        etc = ""

      # 모든 값 저장
      concert_ticket['sub_idx'].append(genre)
      concert_ticket['title'].append(title)
      concert_ticket['company'].append("인터파크")
      concert_ticket['link'].append(current_url)
      concert_ticket['sdate'].append(sdate)
      concert_ticket['edate'].append(edate)
      concert_ticket['place'].append(place)
      concert_ticket['price'].append(price)
      concert_ticket['grade'].append(grade)
      concert_ticket['cast'].append(cast)
      concert_ticket['runningtime'].append(runningtime)
      concert_ticket['img'].append(img)
      concert_ticket['etc'].append(etc)

      visited_titles.add(title)
      print(f'{title} 공연정보 추출 완료')

      

      # 공연 목록 중 하나가 다시 로딩될 때까지 기다리기
      try:
        # 뒤로가기
        driver.back()
        time.sleep(2.5)
      except (TimeoutException, TimeoutError):
        print("뒤로가기가 정상적으로 작동하지 않았습니다.")
        try:
          driver.refresh()
          print("새로고침")
          time.sleep(2)
        except Exception as e:
          print(f"새로고침도 실패: {e}")
          continue
      except Exception as e:
        print(f'뒤로가기 실패 : {e}')
        continue

      print(f'{title} 뒤로가기 완료')

      driver.execute_script(f"window.scrollTo(0, {current_scroll});")
      time.sleep(0.5)
      print('스크롤 내리기')

    except Exception as e:
      print(f"[오류 발생] {e}")
      driver.back()
      time.sleep(1)
      continue

def crawl_genre(driver, url, genre):
  driver.get(url)
  print(f"{genre} 페이지 접속 완료")
  time.sleep(2)

  # "전체" 버튼 클릭
  if genre == 3006:
    driver.find_element(By.XPATH, '//*[@id="contents"]/article[5]/section/div[2]/div[1]/div[1]/button[1]').click()
    # print('전체 버튼 클릭')
  else: 
    driver.find_element(By.XPATH, '//*[@id="contents"]/article[4]/section/div[2]/div[1]/div[1]/button[1]/span').click()
  time.sleep(1)

  # 변수 초기화
  visited_titles = set()

  # 티켓정보 가져오기
  ticket_data = {
    'title': [], 'sub_idx': [], 'company': [], 'link': [], 'sdate': [], 'edate': [],
    'place': [], 'price': [], 'grade': [], 'cast': [], 'runningtime': [],
    'img': [], 'etc': []
  }

  scroll_count = 1
  driver.execute_script("window.scrollBy(0, 878);")
  # print('스크롤 내리기')
  time.sleep(1)

  # 정보 수집 반복문
  while True:
    # 현재 스크롤 위치 저장
    current_scroll = driver.execute_script("return window.pageYOffset;")

    if scroll_count == 1:
      # print('스크롤 카운트 1')
      ticket_info(driver, ticket_data, visited_titles, 1, 5, current_scroll, genre)
      scroll_count += 1

    elif scroll_count == 2:
      # print('스크롤 카운트 2')
      try:
        ticket_info(driver, ticket_data, visited_titles, 6, 10, current_scroll, genre)
      except (TimeoutException, TimeoutError, WebDriverException):
        print('티켓정보 가져오기 재시도')
        ticket_info(driver, ticket_data, visited_titles, 6, 10, current_scroll, genre)

    driver.execute_script("window.scrollBy(0, 750);")
    # print('스크롤 5칸 내리기')
    time.sleep(1.5)
    

    # 새 높이 가져오기
    new_scroll = driver.execute_script("return window.pageYOffset;")

    # 스크롤 내리기 이전 스크롤 높이와 이후 스크롤 높이가 같으면 break
    if new_scroll == current_scroll:
      break

  return ticket_data
    