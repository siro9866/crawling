## 바이브뮤직 탑100

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

URL = "https://vibe.naver.com/chart/total"
browser.get(URL)
# 브라우저가 로딩 될때까지 기다릴 최대시간
browser.implicitly_wait(10)

# 요소 찾기
result = []
try:
    # 팝업창 x 클릭코드
    browser.find_element(By.XPATH, '//*[@id="__modal-container"]/div/div/div/div/a[2]').click()

    for i in range(1, 101, 1):
        rank= browser.find_element(By.XPATH, f'//*[@id="content"]/div[4]/div[2]/div/table/tbody/tr[{i}]/td[3]/span').text
        title = browser.find_element(By.XPATH, f'//*[@id="content"]/div[4]/div[2]/div/table/tbody/tr[{i}]/td[4]/div[1]/span/a').text
        artist = browser.find_element(By.XPATH, f'//*[@id="content"]/div[4]/div[2]/div/table/tbody/tr[{i}]/td[5]/span/span/span/a/span').text
        album = browser.find_element(By.XPATH, f'//*[@id="content"]/div[4]/div[2]/div/table/tbody/tr[{i}]/td[6]/a').text
        result.append((rank, title, artist, album))
        # print(f"순위:{rank}, 제목:{title}, 가수:{artist}, 앨범{album}")


except Exception as e:
    print("요소 못 찾음:", e)

for i in result:
    print(f'{i[0]}위는 {i[2]}의 {i[1]}입니다.')

time.sleep(10)
