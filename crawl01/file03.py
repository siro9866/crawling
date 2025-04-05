## 네이버쇼핑

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

URL = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
browser.get(URL)
# 브라우저가 로딩 될때까지 기다릴 최대시간
browser.implicitly_wait(10)

## 분류
class1 = "식품"
class2 = "축산물"
class3 = "돼지고기"
class4 = ""

# class1
browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click()
browser.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li/a[contains(text(), "{class1}")]').click()

# class2
if class2 != '' :
    browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click()
    browser.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li/a[contains(text(), "{class2}")]').click()

# class3
if class3 != '' :
    browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span').click()
    browser.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li/a[contains(text(), "{class3}")]').click()

# class4
if class4 != '' :
    browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[4]/span').click()
    browser.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[4]/ul/li/a[contains(text(), "{class4}")]').click()


## 조회
browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a/span').click()
time.sleep(3)

# TOP 500 긁기
result = []
for i in range(25):
    print(f'{i+1} 페이지')
    for j in range(1, 21, 1):
        #rank = browser.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{j}]/a/span').text
        names = browser.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[{j}]/a').text.split("\n")
        rank = names[0]
        name = names[1]

        result.append((rank, name))
        print(rank, name)
    browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
    time.sleep(2)

print(len(result))

