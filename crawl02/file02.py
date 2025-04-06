# 가운데 스크롤 있는경우 화면 분할 촬영후 머지
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import os

async def screenshot_and_merge():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 눈으로 확인 가능
        context = await browser.new_context()
        page = await context.new_page()

        # ▶️ 네이버 로그인
        await page.goto("https://nid.naver.com/nidlogin.login")
        await page.fill("input#id", "네이버아이디")  # 여기에 아이디 입력
        await page.fill("input#pw", "비밀번호")     # 여기에 비밀번호 입력
        await page.click("button[type=submit]")

        # ✅ 로그인 후 메인 페이지로 리디렉션됨
        await page.wait_for_url("https://www.naver.com/", timeout=20000)

        # ▶️ 메일 페이지로 직접 이동
        await page.goto("https://mail.naver.com/v2/folders/0")
        await page.wait_for_selector('div[role="main"]')

        mail_area = await page.query_selector('div[role="main"]')

        screenshots = []
        scroll_count = 6  # 원하는 만큼 조절

        for i in range(scroll_count):
            filename = f"screenshot_{i}.png"
            await mail_area.screenshot(path=filename)
            screenshots.append(filename)

            # 메일 리스트 스크롤 다운
            await page.evaluate('''
                const el = document.querySelector('div[role="main"]');
                el.scrollBy(0, 600);
            ''')
            await page.wait_for_timeout(1000)

        await browser.close()

        # 이미지 병합
        images = [Image.open(img) for img in screenshots]
        widths, heights = zip(*(img.size for img in images))

        total_height = sum(heights)
        max_width = max(widths)

        final_img = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))

        y_offset = 0
        for img in images:
            final_img.paste(img, (0, y_offset))
            y_offset += img.size[1]

        final_img.save("merged_mail_list.png")
        print("✅ 병합 완료: merged_mail_list.png")

        # 임시 이미지 삭제 (선택)
        for file in screenshots:
            os.remove(file)

asyncio.run(screenshot_and_merge())