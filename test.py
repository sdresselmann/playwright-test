from ast import dump
import asyncio
import json
import html_to_json
from bs4 import BeautifulSoup

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
    locator = page.locator('.vignette')
    count = await locator.count()
    array = ""
    for i in range(count):
        # i+1 because locator starts at 1
        locator = page.locator(':nth-match(.vignette, {0})'.format(i+1))
        array = await locator.inner_html()
    return array


def convertHtmlToJSON(input_html):
    output_json = html_to_json.convert(input_html)
    return output_json


def dumpIntoJSON(data):
    with open('searchResults.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


async def visitPage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await browser.new_page()
        await page.goto(URL)

        await acceptCookies(page)
        await searchForWord(WORD, page)

        searchResultsAsHTML = await findMainElement(page)

        soup = BeautifulSoup(searchResultsAsHTML, "html.parser")

        vignette_title = soup.find('strong').text
        vignette_title = vignette_title.replace("\xad", "")

        vignette_snippet = soup.find('p').text

        vignette_link = URL + soup.find('a')['href']

        json_object = {"searchResults": [{
            '1': {
                'vignette_title': vignette_title,
                'vignette_snippet': vignette_snippet,
                'vignette_link': vignette_link
            }
        }]}

        dumpIntoJSON(json_object)

        await browser.close()


asyncio.run(visitPage())
