from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
  option = Options()
  option.add_argument("window-size=1000,2500")
  option.add_argument("--no-sandbox")
  option.add_argument("--disable-dev-shm-usage")
  return webdriver.Chrome(options=option)
