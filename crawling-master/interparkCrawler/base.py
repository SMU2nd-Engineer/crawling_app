from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
  option = Options()
  option.add_argument("window-size=1000,2500")
  option.add_argument('--disable-gpu')
  option.add_argument('--enable-unsafe-swiftshader')
  option.add_argument('--disable-dev-shm-usage')  # 메모리 공유 이슈 완화
  option.add_argument('--no-sandbox')
  option.page_load_strategy = 'eager'
  return webdriver.Chrome(options=option)
