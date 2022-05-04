import asyncio
import json
import logging
import sys
import traceback
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright import *


URL = 'https://www.duden.de/'
# example searchword for testing purposes
searchword = "Präliminarien"
result_data = {}


async def acceptCookies(page):
    '''
       Parameters: \n
       page (Page) \n
    '''
    cookie_iframe = page.frame_locator('#sp_message_iframe_622759')
    await cookie_iframe.locator("button[title='AKZEPTIEREN']").click()


async def searchForWord(word: str, page):
    '''
       Parameters: \n
       word (str) -- that is entered into the search bar \n
       page (Page) \n
    '''
    await page.fill('#edit-search-api-fulltext--2', word)
    await page.click('button:has-text("Nachschlagen")')


async def getSearchResults(page):
    '''
       Read search result data that is stored in vignette 
       class tags inside the main part  \n
       Parameters: \n
       page (Page) \n
    '''
    locator = page.locator('.vignette')
    count = await locator.count()
    html_data = ""
    for i in range(count):
        # i+1 because locator starts at 1
        position = i+1
        locator = page.locator(':nth-match(.vignette, {0})'.format(position))
        html_data = await locator.inner_html()
        parseResults(position, html_data)


def parseResults(key: int, data: str):
    '''
       Parse given data into a fixed json format \n
       Parameters: \n
       key (int) -- used as id number for object  \n
       data (str) -- html text that is parsed into json format
    '''
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

    array = [json_object]
    result_data[key] = array


def writeDataToJSON(data: json, path: str = "searchResults.json"):
    '''
       Parameters: \n
       data (json) -- that has to be written into file
       path (str)  -- path to file
    '''
    with open(path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


async def crawlPage(url: str):
    '''
       Crawling the webpage and saving search results into a json file \n
       Parameters: \n
       url (str) -- of target webpage  \n
    '''
    # seperating tasks even more would only make the code less readable
    global result_data
    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=50)
        page = await browser.new_page()
        await page.goto(url)

        await acceptCookies(page)
        await searchForWord(searchword, page)

        await getSearchResults(page)

        writeDataToJSON(result_data)
        await browser.close()


def main():
    print("Suche startet für: {0}".format(searchword))

    try:
        asyncio.run(crawlPage(URL))
    # just in case something goes terribly wrong
    except Exception as e:
        logging.error(traceback.format_exc)

    asyncio.run(crawlPage(URL))


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("\nFehler: Es wurde kein Suchwort als Parameter übergeben! \n" +
              "Aufruf von Playwright-Bot Beispiel:" +
              "\"python duden Präliminarien\" \n ")
        sys.exit(1)

    searchword = sys.argv[1]

    main()
