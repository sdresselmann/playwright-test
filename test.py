import asyncio
from playwright.async_api import async_playwright


url = 'https://www.duden.de/'
searchword = "Präliminarien"


def test(page):
    locator = page.locator('main')
    print(locator)


async def visitPage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto(url)

        # Get all popups when they open
        async def handle_popup(popup):
            await popup.wait_for_load_state()
            print(await popup.title())

            page.on("popup", handle_popup)

        await page.click("button[title='AKZEPTIEREN']")
        await page.fill('#edit-search-api-fulltext--2', searchword)
        await page.click('button:has-text("Nachschlagen")')
        async with page.expect_navigation():
            await page.wait_for_load_state("networkidle")
            locator = page.locator('main')
            print(await locator.inner_text())
            await browser.close()


asyncio.run(visitPage())
