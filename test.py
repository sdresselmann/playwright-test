import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()


async def firstScript():
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto("http://whatsmyuseragent.org/")
        await page.screenshot(path="example.png")
        await browser.close()


asyncio.run(main())
asyncio.run(firstScript())
