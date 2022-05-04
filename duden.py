import asyncio
import json
import sys
import argparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


URL = 'https://www.duden.de/'
SEARCHWORD = "Präliminarien"
result_data = {"searchResults": []}


async def acceptCookies(page):
    cookie_iframe = page.frame_locator('#sp_message_iframe_622759')
    await cookie_iframe.locator("button[title='AKZEPTIEREN']").click()


async def searchForWord(searchword, page):
    await page.fill('#edit-search-api-fulltext--2', searchword)
    await page.click('button:has-text("Nachschlagen")')


async def getSearchResults(page):
    locator = page.locator('.vignette')
    count = await locator.count()
    array = ""
    for i in range(count):
        # i+1 because locator starts at 1
        position = i+1
        locator = page.locator(':nth-match(.vignette, {0})'.format(position))
        array = await locator.inner_html()
        parseResults(position, array)


def parseResults(key, data):
    global result_data
    soup = BeautifulSoup(data, "html.parser")

    vignette_title = soup.find('strong').text
    # replacing empty spaces in strong text for better readability in json
    vignette_title = vignette_title.replace("\xad", "")
    vignette_snippet = soup.find('p').text
    vignette_link = URL + soup.find('a')['href']

    json_object = {
        'vignette_title': vignette_title,
        'vignette_snippet': vignette_snippet,
        'vignette_link': vignette_link
    }

    result_data[key] = json_object


def writeDataToJSON(data):
    with open('searchResults.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


async def visitPage():
    print(sys.argv)
    global result_data
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await browser.new_page()
        await page.goto(URL)

        await acceptCookies(page)
        await searchForWord(SEARCHWORD, page)

        await getSearchResults(page)

        writeDataToJSON(result_data)

        await browser.close()


def main():
    asyncio.run(visitPage())


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("\nFehler: Es wurde kein Suchwort als Parameter übergeben! \n" +
              "Aufruf von Playwright-Bot Beispiel:" +
              "\"python duden Präliminarien\" \n ")
        sys.exit(1)
    print(sys.argv[1])
    main()
