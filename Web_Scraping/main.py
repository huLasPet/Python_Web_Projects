import requests
import asyncio
from bs4 import BeautifulSoup

URLS = {"Gamepod": "https://gamepod.hu/index.html", "Prohardver": "https://prohardver.hu/index.html"}
SELECTORS = {"Gamepod": "html body.gp main#page-index div#middle div.container div.row div#center "
                        "div.content-list.content-list-detailed ul.list-unstyled li.media div.media-body "
                        "h4.media-heading a",
             "Prohardver": "html body.ph main#page-index-2 div#middle div.container div.row div#center "
                           "div.content-list.content-list-compact.content-image-medium.content-image-right "
                           "ul.list-unstyled li.media div.media-body h4.media-heading a"}


async def get_news():
    pass


for url in URLS:
    print(f"\nLatest news from {url} - {URLS[url]}:")
    response = requests.get(URLS[url])
    soup = BeautifulSoup(response.text, "html.parser")
    site_data = soup.select(selector=SELECTORS[url])
    for article in site_data:
        print(f"{article.text} - https://gamepod.hu{article.get('href')}")
