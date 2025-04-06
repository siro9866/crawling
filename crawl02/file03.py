# 경로에 포함된 모든 resource 파일 다운로드
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urljoin, urlparse, unquote

SAVE_DIR = "naver_news_img"

# 디렉토리 생성
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(url):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    return unquote(filename) if filename else "default.jpg"

def download_image(url):
    try:
        filename = sanitize_filename(url)
        path = os.path.join(SAVE_DIR, filename)

        if not os.path.exists(path):
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"✅ 저장 완료: {filename}")
    except Exception as e:
        print(f"❌ 실패: {url} ({e})")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("🧭 페이지 로딩 중...")
        await page.goto("https://news.naver.com", wait_until="networkidle")

        # 스크롤 다운하여 lazy load 유도
        for _ in range(10):
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(1)

        # HTML 가져오기
        content = await page.content()

        # BeautifulSoup 으로 이미지 파싱
        soup = BeautifulSoup(content, "html.parser")
        img_tags = soup.find_all("img")

        print(f"📸 이미지 태그 수: {len(img_tags)}")

        img_urls = set()
        for img in img_tags:
            src = img.get("src")
            if src:
                full_url = urljoin("https://news.naver.com", src)
                img_urls.add(full_url)

        print(f"🖼️ 유효 이미지 URL 수: {len(img_urls)}")

        # 이미지 다운로드
        for url in img_urls:
            download_image(url)

        await browser.close()
        print("✅ 모든 이미지 다운로드 완료.")

asyncio.run(main())