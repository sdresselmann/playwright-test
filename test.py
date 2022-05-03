import asyncio
from playwright.async_api import async_playwright

url = "https://www.duden.de/"


async def visitPage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto(url)
        await browser.close()

asyncio.run(visitPage())
