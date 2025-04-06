# html, schreenshot, resource 수집
import asyncio
from crawl02 import file01, file03


async def main(base_url):
    await file01.get_html(base_url)
    await file01.get_screenshot(base_url)
    await file03.get_resources(base_url)

if __name__ == "__main__":
    BASE_URL = "https://news.naver.com"
    asyncio.run(main(BASE_URL))
