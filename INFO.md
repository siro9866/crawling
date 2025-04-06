```commandline
PIP INSTALL
pip install selenium
pip install webdriver-manager
pip install selenium-wire
pip install blinker==1.4
pip install setuptools

-- playwright
pip install playwright
pip install playwright pillow
playwright install

pip install beautifulsoup4
```
```
이슈
Iframe 의 경우 XPATH 대로 해도 못 찾는 이슈 있음 지피티에 물어바

```
🔥 Playwright vs Selenium 비교
항목	Playwright	Selenium
1. 개발 난이도	✅ 간결하고 직관적
비동기 지원 (async/await)이지만 문법은 명확하고 현대적인 API 제공	⚠️ 조금 더 복잡
클래식한 방식이고 일부 동작은 복잡한 코드 요구
2. 변경 대응력	✅ 유연하고 안정적
자동 대기(auto wait), 프레임 전환, 팝업 처리 등에 강함	⚠️ 수동 대기가 많음
sleep 또는 WebDriverWait을 자주 사용해야 안정성 확보
3. 대규모 크롤링	✅ 병렬 처리 쉬움
브라우저 컨텍스트 분리로 리소스 적게 사용	⚠️ 리소스 소모 큼
브라우저 여러 개 띄우면 무거워짐
4. 안정성	✅ 높음
JS 처리나 DOM 렌더링 타이밍 문제에 강함	⚠️ JS 렌더링 대기 문제 많음
사이트 로딩 중 예외 발생 빈도 높음
5. 속도	✅ 더 빠름
설계 자체가 빠르고 효율적	⚠️ 느린 편
오래된 구조와 무거운 드라이버
6. 기타 추천 포인트	- 모바일 에뮬레이션, 다중 브라우저 (WebKit까지 지원)
- Chromium, Firefox, WebKit 지원
- 스크린샷, PDF 저장, 영상 녹화 등 기본 포함	- 브라우저 자동화 툴로 가장 오래됨
- Java, C#, Python 등 언어 호환성 넓음
- 많은 예제가 존재