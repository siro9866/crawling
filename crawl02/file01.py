import os
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse

id= "아이디"
pw= "패스"

# 전체 화면 html
async def get_html(base_url):
    parsed = urlparse(base_url)
    folder_name = parsed.hostname
    os.makedirs(folder_name, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(base_url)
        await page.wait_for_load_state("load")  # 페이지 로딩 완료까지 대기

        html = await page.content()
        # print(html)  # 전체 HTML 출력

        # ✅ HTML 저장
        file_path = os.path.join(folder_name, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        await browser.close()

# 전체 화면 스크린샷
async def get_screenshot(base_url):
    parsed = urlparse(base_url)
    os.makedirs(parsed.hostname, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 1080})
        await page.goto(base_url, wait_until="networkidle")

        # 스크롤 끝까지 내려서 Lazy Load 유도
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)  # 3초 대기 (이미지 로딩 시간)

        # 전체 페이지 스크린샷 저장
        await page.screenshot(path=f"{parsed.hostname}/index.png", full_page=True)
        await browser.close()
        print("스크린샷 저장완료")

# 로그인
async def login(base_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # True면 브라우저 안 보임
        page = await browser.new_page()

        # 1. 네이버 로그인 페이지 접속
        await page.goto("https://nid.naver.com/nidlogin.login")

        # 2. 아이디/비밀번호 입력
        await page.fill("input#id", id)
        await page.fill("input#pw", pw)

        # 3. 로그인 버튼 클릭
        await page.click("button[type=submit]")

        # 4. 로그인 처리 대기 (몇 초 필요할 수 있음)
        await page.wait_for_timeout(5000)

        # 5. 메일 읽기 페이지 이동
        mail_url = "https://mail.naver.com/v2/folders/0"
        await page.goto(mail_url)

        # 6. 페이지 로딩 대기
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)  # 여유를 줘야 메일 본문까지 로딩됨

        # 7. 전체 HTML 출력 or 스크린샷
        html = await page.content()
        print("메일 페이지 HTML:", html[:500])  # 너무 길면 일부만 출력

        await page.screenshot(path="mail_read.png", full_page=True)
        print("메일 스크린샷 저장 완료!")

        await browser.close()


#base_url = "https://news.naver.com"
# base_url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
# base_url = "https://nid.naver.com/nidlogin.login"

# asyncio.run(get_html(base_url))
#asyncio.run(get_screenshot(base_url))
# asyncio.run(login(base_url))