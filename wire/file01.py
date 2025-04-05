# 내트워크 패킷 캡처 selenuim-wire
# 셀레늄으로 불가능한 크롤링(ex: js로 처리되는 차트등)

import time

from dotenv.parser import decode_escapes
from selenium.webdriver.chrome.options import Options
# 웹드라이버 객체 생성시 수반될 서비스나 옵션
from selenium.webdriver.chrome.service import Service
# 선택자 및 키보드 입력
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from seleniumwire import webdriver
from seleniumwire.utils import decode

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

## 조회
browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a/span').click()
time.sleep(3)

# 네트워크 패킷관련 메서드
# 특정 버튼이나 값을 드라이버 객체 메서들ㄹ 통해 클릭한 다음 통신하는 네트워크를 획득하는 메소드
# https://datalab.naver.com/shoppingInsight/getCategoryClickTrend.naver
# 위 url 의 근거는 차트등 에 활용되는 데이타의 경우 xpath 로 잡히지 않아 네트워크에서 해당 네트워크의 url
# 요청 응답 헤더 및 바디 확인 메서드
for request in browser.requests:
    #print(request)

    if str(request) == 'https://datalab.naver.com/shoppingInsight/getCategoryClickTrend.naver':
        print(request)
        print(request.response.body)
        # 이때 응답 받은 데이터에 대해서 디코딩을 진행해야 원본 데이터 획득 가능
        decodeData = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('UTF-8')
        print(decodeData)

#
#    print(request.headers)
#    print(request.body)
#    print(request.path)
#    print(request.querystring)
#
#    print(request.response)
#    print(request.response.headers)
#    print(request.response.body)

