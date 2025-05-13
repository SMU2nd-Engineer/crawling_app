from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

# 크롬드라이버 설정(공통)
def create_driver(headless: bool = False) -> webdriver.Chrome:
    chromeOptions = Options()
    if headless:
        chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(options=chromeOptions)
    return driver

# 파일저장 날짜 포맷 설정(공통)
# def get_date_string() -> str:
#     today = datetime.datetime.now()
#     return today.strftime('%Y%m%d_%H%M%S')

# 경기날짜 연도 포맷 설정(스포츠)
def get_current_year_month() -> tuple:
    today = datetime.datetime.now()
    return today.year, today.month