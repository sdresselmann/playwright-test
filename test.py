import asyncio
from playwright.async_api import async_playwright


async def visitPage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto("https://www.duden.de/")
        await browser.close()

asyncio.run(visitPage())
