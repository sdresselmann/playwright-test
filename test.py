import asyncio
import json
from playwright.async_api import async_playwright


URL = 'https://www.duden.de/'
WORD = "Präliminarien"


async def acceptCookies(page):
    cookie_iframe = page.frame_locator('#sp_message_iframe_622759')
    await cookie_iframe.locator("button[title='AKZEPTIEREN']").click()


async def searchForWord(searchword, page):
    await page.fill('#edit-search-api-fulltext--2', searchword)
    await page.click('button:has-text("Nachschlagen")')


async def findMainElement(page):
    locator = page.locator('main')
    return await locator.inner_text()


async def visitPage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await browser.new_page()
        await page.goto(URL)

        await acceptCookies(page)
        await searchForWord(WORD, page)
        searchResults = await findMainElement(page)
        with open('searchResults.json', mode='w', encoding='utf-8') as file:
            json.dump(searchResults, file, ensure_ascii=False, indent=4)

        '''
        async with page.expect_navigation():
            await page.wait_for_load_state("networkidle")
            findMainElement()
            '''
        await browser.close()


asyncio.run(visitPage())
