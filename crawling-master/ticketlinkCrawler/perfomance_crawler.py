from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from .utils import create_driver
from .config import CATEGORY_DICT, GENRE_NUM_LIST

def crawlPerformance():
    driver = create_driver(headless=False)
    driver.maximize_window()
    url = "https://www.ticketlink.co.kr/local"
    driver.get(url)    
    time.sleep(2)

    detailDataList = []
    maxTry = 50

    listLength = {}

    countryLength = driver.find_elements(By.XPATH, '//*[@id="content"]/section[1]/div/div/div/ul/li/button')

    for countryNum in range(1, len(countryLength) + 1):
        countryButton = driver.find_element(By.XPATH, f'//*[@id="content"]/section[1]/div/div/div/ul/li[{countryNum}]/button')
        countryButton.click()
        time.sleep(1)

        for _ in range(maxTry):
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        for genreNum in GENRE_NUM_LIST:
            listLength[genreNum] = len(driver.find_elements(By.XPATH, f'//*[@id="genre_{genreNum}"]/div/div/ul/li'))
            time.sleep(1)

        # 카테고리 버튼 한 번씩 클릭
        for locationNum in range(1, len(GENRE_NUM_LIST) + 1):
          for liNum in range(1, listLength[GENRE_NUM_LIST[locationNum - 1]] + 1):
            tabButton = driver.find_element(By.XPATH, f'//*[@id="content"]/section[2]/div[1]/div/ul/li[{locationNum}]/button')
            tabButton.click() 
            time.sleep(1)

            # //*[@id="content"]/section[2]/div[1]/div/ul/li[1]
            # //*[@id="content"]/section[2]/div[1]/div/ul/li[2]
            # //*[@id="content"]/section[2]/div[1]/div/ul/li[7]

            # 스크롤 위치 저장
            scrollHeight = driver.execute_script("return window.pageYOffset;")
            time.sleep(1)

            for _ in range(0, int(((liNum - 1)/4))):
              scrollHeight += 546
              driver.execute_script(f"window.scrollTo(0, {scrollHeight})")
              time.sleep(1)

            # 저장된 스크롤 위치로 이동
            driver.execute_script(f"window.scrollTo(0, {scrollHeight})")
            time.sleep(2)

            try:
              if GENRE_NUM_LIST[locationNum-1] == 16:
                selectedElement = driver.find_element(By.XPATH, f'//*[@id="genre_{GENRE_NUM_LIST[locationNum-1]}"]/div/div/ul/li[{liNum}]')
              else :
                 selectedElement = driver.find_element(By.XPATH, f'//*[@id="genre_{GENRE_NUM_LIST[locationNum-1]}"]/div[2]/div/ul/li[{liNum}]')
              time.sleep(2)

              # 상세정보 클릭
              selectedElement.click()
              time.sleep(2)

              # 팝업 창 지우기
              try:
                popup = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[3]/button')
                popup.click()
              except:
                popup = None

              link = driver.current_url

              #필요한 정보 가져오기
              driver.implicitly_wait(2)
              title = driver.find_element(By.CSS_SELECTOR, ".product_title").text
              image = driver.find_element(By.CSS_SELECTOR, ".product_detail_img").get_attribute("src")
              artistList =  driver.find_elements(By.CSS_SELECTOR, "div.product_casting > div > ul > li > a > span.product_casting_name")
              priceList = driver.find_elements(By.CSS_SELECTOR, "div.product_info > ul:nth-child(3) > li:nth-child(1) > div > ul > li")
              category = CATEGORY_DICT.get(GENRE_NUM_LIST[locationNum - 1], "기타")
              etcList = driver.find_elements(By.CSS_SELECTOR, "#content > section.common_section.section_product_content > div > section > div:nth-child(3)")

              info = driver.find_elements(By.CSS_SELECTOR, "div.product_info > ul > li > span")
              for idx, i in enumerate(info, start=1):  # idx는 1부터 시작
                label = i.text.strip()  # span 안에 들어있는 텍스트 가져오기

                if label == "장소":
                    place = driver.find_element(By.CSS_SELECTOR, f"div.product_info > ul > li:nth-child({idx}) button").text

                elif label == "관람시간":
                    runningTime = driver.find_element(By.CSS_SELECTOR, f"div.product_info > ul > li:nth-child({idx}) div").text

                elif label == "기간":
                    date = driver.find_element(By.CSS_SELECTOR, f"div.product_info > ul > li:nth-child({idx}) div").text
                    sdate = date.split('-')[0].strip()
                    edate = date.split()[-1].strip()

                elif label == "관람등급":
                    age = driver.find_element(By.CSS_SELECTOR, f"div.product_info > ul > li:nth-child({idx}) div").text

              prices = [priceText.text for priceText in priceList]
              price = '/'.join(prices)

              artistNames = [artistText.text for artistText in artistList]
              artist = '/'.join(artistNames)

              etcs = [etcText.text for etcText in etcList]
              etc = '/'.join(etcs)


              detailData = {
                  'sub_idx': category,
                  'title': title,
                  'company': "티켓링크",
                  'link': link,
                  'sdate': sdate,
                  'edate': edate,
                  'place': place,
                  'price': price,
                  'grade': age,
                  'cast': artist,
                  'runningtime': runningTime,
                  'img': image,
                  'etc': etc
              }

              print(detailData)

              detailDataList.append(detailData)
              driver.back()
              time.sleep(1)

            except Exception as e:
              print(f"에러 발생: {e}")
              driver.get(url)
              time.sleep(2)

    driver.quit()
    return pd.DataFrame(detailDataList)