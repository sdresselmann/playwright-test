import asyncio
from playwright.async_api import async_playwright

url = 'https://www.duden.de/'
searchword = "Präliminarien"


async def visitPage():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto(url)
        await page.fill('#edit-search-api-fulltext--2', searchword)
        await page.click('button:has-text("Nachschlagen")')
        await browser.close()

asyncio.run(visitPage())
