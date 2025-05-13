# melon_crawler/base.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 페이지 끝까지 스크롤하는 함수
def scrollToEnd(driver):
    """페이지 끝까지 스크롤합니다."""
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

# create_driver 함수 (get_driver와 동일)
def createDriver():
    """웹 드라이버를 설정하고 반환합니다."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 크롬 드라이버 경로 설정 (os.path.join으로 현재 경로 + chromedriver)
    # service = webdriver 
    driver = webdriver.Chrome(options=chrome_options)

    # 드라이버 초기 설정
    driver.implicitly_wait(2)  # 기본 대기 시간 설정 (선택 사항)

    return driver
