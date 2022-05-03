import asyncio
from playwright.async_api import async_playwright


url = 'https://www.duden.de/'
searchword = "Präliminarien"


async def findMainElement(page):
    locator = page.locator('main')
    print(await locator.inner_text())


async def visitPage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await browser.new_page()
        await page.goto(url)
        cookie_iframe = page.frame_locator('#sp_message_iframe_622759')
        await cookie_iframe.locator("button[title='AKZEPTIEREN']").click()

        '''
        await page.click("button[title='AKZEPTIEREN']")
        await page.fill('#edit-search-api-fulltext--2', searchword)
        await page.click('button:has-text("Nachschlagen")')
        async with page.expect_navigation():
            await page.wait_for_load_state("networkidle")
            findMainElement()
            '''
        await browser.close()


asyncio.run(visitPage())
