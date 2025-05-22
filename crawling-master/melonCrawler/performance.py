# melon_crawler/performance.py

import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from melonCrawler.utils import greneToCode

def getPerformanceDetails(driver, liList):
    # WebDriverWait을 사용하는 예시
    wait = WebDriverWait(driver, 10)  # 10초 대기
    # 페이지 로딩될 때까지 대기
    wait.until(EC.presence_of_element_located((By.ID, "perf_poster")))
    time.sleep(2)  # 로딩 후 2초 대기
  
    detailDataList = []

    for i in range(len(liList)):
        try:
            listItem = liList[i]
            linkElement = listItem.find_element(By.TAG_NAME, 'a')
            hrefValue = linkElement.get_attribute('href')
            print(f"[{i+1}] 접근 URL: {hrefValue}")

            # 새로운 탭으로 페이지 열기
            driver.execute_script("window.open(arguments[0]);", hrefValue)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)

            # 필요한 정보 가져오기
            driver.implicitly_wait(2)

            # 상세페이지의 텍스트
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 현재 URL 확인
            current_url = driver.current_url
            print(f"[{i+1}] 현재 페이지 URL: {current_url}")

            try:
                popup = driver.find_element(By.XPATH, '//*[@id="noticeAlert_layerpopup_close"]')
                popup.click()
                time.sleep(2)
            except NoSuchElementException:
                pass

            try:
              titleElement = soup.select_one('.box_consert_txt .tit')
              title = titleElement.get_text(strip=True) if titleElement else "제목 정보 없음"
            except Exception as e:
              titleElement = ""
              print(f"[{i+1}] 제목 추출 오류: {e}")

            print(f"[{i+1}] 제목: {title}")

            # 티켓구매링크 link 정보 추출
            try:
                link = driver.current_url
            except Exception as e:
                link = "티켓구매링크 정보 없음"
                print(f"[{i+1}] 티켓구매링크 오류: {e}")

            print(f"[{i+1}] 티켓구매링크: {link}")

            """ 시작일자 sdate / 종료일자 edate 정보 추출
                  edate가 text인 경우 sdate yyyy.mm.dd 형식으로 출력 """
            try:
                dateElement = soup.select_one('.box_consert_txt .box_consert_info .info_left #periodInfo')
                date = dateElement.get_text(strip=True) if dateElement else "시작종료일자 정보 없음"
                sdate = date.split('-')[0].strip()
                edateCandidate = date.split()[-1].strip()
                # edate가 날짜 형식이면 그대로, 아니면 sdate로 통일
                edate = edateCandidate if re.match(r'\d{4}\.\d{2}\.\d{2}', edateCandidate) else sdate
            except Exception as e:
                sdate = edate = ""
                print(f"[{i+1}] 공연기간 추출 오류: {e}")

            # 장소 place 정보 추출
            try:            
              placeElement = soup.select_one('.box_consert_txt .box_consert_info .info_right .place')
              place = placeElement.get_text(strip=True) if placeElement else "장소 정보 없음"            
            except Exception as e:
                 placeElement = "" 
                 print(f"[{i+1}] 장소 추출 오류: {e}")  

              # 가격 price 정보 추출
            try:
                priceElement = soup.select('.box_bace_price ul li')
                if priceElement:
                    priceList = [priceInformation.get_text(strip=True) for priceInformation in priceElement if priceInformation.get_text(strip=True)]
                    price = '/'.join(priceList)
                else:
                    price = " "
            except Exception as e:
                price = " " 
                print(f"[{i+1}] 가격 추출 오류: {e}") 

            # 관람연령 grade 정보 추출
            try:           
                gradeElement = soup.select_one('.box_consert_txt .box_consert_info .info_right dd:nth-child(4)')
                grade = gradeElement.get_text(strip=True) if gradeElement else "관람연령 정보 없음"            
            except Exception as e:
                gradeElement = ""
                print(f"[{i+1}] 관람연령 추출 오류: {e}")   

            # 출연진 cast 정보 추출
            cast = ''
            try:
                castElements = soup.select('div.box_artist_checking ul li a strong')
                castList = [el.get_text(strip=True) for el in castElements if el.get_text(strip=True)]
                cast = '/'.join(castList)
                if not cast:
                    cast = ""
            except Exception as e:
                cast = ""
                print(f"[{i+1}] 출연진 추출 오류: {e}")

            # 공연기간(러닝타임) runningtime 정보 추출
            try:
                runningtimeElement = soup.select_one('.box_consert_txt .box_consert_info .info_left dd:nth-child(4)')
                runningtime = runningtimeElement.get_text(strip=True) if runningtimeElement else "공연기간 정보 없음"
            except Exception as e:
                runningtimeElement = ""
                print(f"[{i+1}] 공연기간 추출 오류: {e}") 

            # 이미지 img 정보 추출
            try:
                imgElement = soup.select_one('.box_consert_thumb.thumb_180x254 img')
                img = imgElement['src'] if imgElement and imgElement.has_attr('src') else "이미지 정보 없음"
            except Exception as e:
                imgElement = ""
                print(f"[{i+1}] 이미지 추출 오류: {e}")     

            # genre(장르) 정보 추출
            try:
              categoryElement = soup.select_one('.box_consert_txt .box_consert_info .info_left dd:nth-child(6)')
              category = greneToCode( categoryElement.get_text(strip=True))
              

            except Exception as e:
              categoryElement = ""
              print(f"[{i+1}] 장르 추출 오류: {e}")
      

            # 공연시간 정보 etc 정보 추출
            try:
                # '공연시간' 텍스트 제외
                etcElement = soup.select('.box_concert_time > p, .box_concert_time > span, .box_concert_time > div')[1:]                  
                # 텍스트 정리: 공백 통일, 슬래시 앞뒤 공백 제거
                etcList = [
                    re.sub(r'\s*/\s*', '/', re.sub(r'\s+', ' ', el.get_text()))
                    for el in etcElement if el.get_text(strip=True)
                ]

                # 슬래시 포함 항목은 그대로, 그 외는 공백으로 구분
                etc = ' '.join(etcList).replace('\t', '')
                etc = re.sub(r'\s+', ' ', etc).strip()

            except Exception as e:
                etc = ""
                print(f"[{i+1}] 공연시간 정보 추출 오류: {e}")

            # 필수 정보 체크 후 저장
            try:
                defualtD = [title, sdate, edate]
                if all("정보 없음" not in val for val in defualtD):
                    detailDataList.append({
                        'title': title,
                        'sub_idx': category,
                        'company': '멜론티켓',
                        'link': link,
                        'sdate': sdate,
                        'edate': edate,
                        'place': place,
                        'price': price,
                        'grade': grade,
                        'cast': cast,
                        'runningtime': runningtime,
                        'img': img,
                        'etc': etc
                    })
                else:
                    print(f"[{i+1}] 필수 정보 누락으로 저장하지 않음.")
            except Exception as filterE:
                print(f"[{i+1}] 필터링 중 오류 발생: {filterE}")

        except Exception as detailE:
            print(f"[{i+1}] 상세 페이지 파싱 오류: {detailE}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    return detailDataList
