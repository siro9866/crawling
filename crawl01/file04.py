## 로그인

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 웹드라이버 객체 생성시 수반될 서비스나 옵션
from selenium.webdriver.chrome.service import Service
# 선택자 및 키보드 입력
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

customService = Service()
# 크롬 옵션 설정
customOption = Options()
customOption.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
customOption.add_experimental_option("excludeSwitches", ["enable-automation"])
customOption.add_experimental_option("useAutomationExtension", False)
customOption.add_argument("--start-maximized")

browser = webdriver.Chrome(service=customService, options=customOption)

URL = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"
browser.get(URL)
# 브라우저가 로딩 될때까지 기다릴 최대시간
browser.implicitly_wait(10)

# 요소 찾기
browser.execute_script('document.getElementsByName("id")[0].value="아이디"')
time.sleep(1)
browser.execute_script('document.getElementsByName("pw")[0].value="비번"')
time.sleep(1)

browser.find_element(By.XPATH, '//*[@id="log.login"]').click()

time.sleep(3)