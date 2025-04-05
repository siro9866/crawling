import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 웹드라이버 객체 생성시 수반될 서비스나 옵션
from selenium.webdriver.chrome.service import Service
# 선택자 및 키보드 입력
from selenium.webdriver.common.by import By

customService = Service()
# 크롬 옵션 설정
customOption = Options()
customOption.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
customOption.add_experimental_option("excludeSwitches", ["enable-automation"])
customOption.add_experimental_option("useAutomationExtension", False)
customOption.add_argument("--start-maximized")

browser = webdriver.Chrome(service=customService, options=customOption)

URL = "https://www.naver.com/"
browser.get(URL)
# 브라우저가 로딩 될때까지 기다릴 최대시간
browser.implicitly_wait(10)

# 요소 찾기
try:
    elem = browser.find_element(By.XPATH, '//*[@id="account"]/div/a')
    elem.click()
except Exception as e:
    print("요소 못 찾음:", e)


time.sleep(3)
