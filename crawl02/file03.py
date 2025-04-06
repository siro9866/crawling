# 경로에 포함된 모든 resource 파일 다운로드
import asyncio
import os
import requests
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# 확장자 기반 폴더 매핑
EXTENSION_DIR_MAP = {
    ".jpg": "img", ".jpeg": "img", ".png": "img", ".gif": "img", ".webp": "img", ".svg": "img", ".ico": "img",
    ".css": "css",
    ".js": "js",
    ".woff": "font", ".woff2": "font", ".ttf": "font", ".otf": "font",
}

# 저장 경로 설정
def get_save_path(base_url, url):
    baseParsed = urlparse(base_url)
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[-1].lower()
    subdir = EXTENSION_DIR_MAP.get(ext, "other")
    os.makedirs(os.path.join(baseParsed.hostname, subdir), exist_ok=True)
    filename = unquote(os.path.basename(parsed.path)) or "index.html"
    return os.path.join(baseParsed.hostname, subdir, filename)

# 다운로드 함수
def download_file(base_url, url):
    try:
        path = get_save_path(base_url, url)
        if not os.path.exists(path):
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"✅ 저장 완료: {path}")
    except Exception as e:
        print(f"❌ 실패: {url} ({e})")

# 메인 실행
async def get_resources(base_url):
    parsed = urlparse(base_url)
    os.makedirs(parsed.hostname, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("🔗 페이지 접속 중...")
        await page.goto(base_url, wait_until="networkidle")

        # 스크롤로 lazy-load 유도
        for _ in range(10):
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(1)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        resource_urls = set()

        # 이미지
        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                resource_urls.add(urljoin(base_url, src))

        # CSS, favicon, preload 등
        for link in soup.find_all("link", href=True):
            rel = link.get("rel", [])
            if any(r in rel for r in ["stylesheet", "icon", "preload", "apple-touch-icon"]):
                resource_urls.add(urljoin(base_url, link["href"]))

        # JS
        for script in soup.find_all("script", src=True):
            resource_urls.add(urljoin(base_url, script["src"]))

        print(f"📦 총 리소스 수: {len(resource_urls)}개")

        # 다운로드 실행
        for url in resource_urls:
            download_file(base_url, url)

        await browser.close()
        print("🎉 모든 리소스 다운로드 완료.")

# 실행
BASE_URL = "https://news.naver.com"
asyncio.run(get_resources(BASE_URL))