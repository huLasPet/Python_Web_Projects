import requests
import cProfile
import pstats
from bs4 import BeautifulSoup

URLS = {"Gamepod": "https://gamepod.hu/index.html", "Prohardver": "https://prohardver.hu/index.html"}
SELECTORS = {"Gamepod": "html body.gp main#page-index div#middle div.container div.row div#center "
                        "div.content-list.content-list-detailed ul.list-unstyled li.media div.media-body "
                        "h4.media-heading a",
             "Prohardver": "html body.ph main#page-index-2 div#middle div.container div.row div#center "
                           "div.content-list.content-list-compact.content-image-medium.content-image-right "
                           "ul.list-unstyled li.media div.media-body h4.media-heading a"}


def get_news():
    """Goes through the dict of pages where i want news from and prints out the top articles and their url."""
    for url in URLS:
        print(f"\nLatest news from {url} - {URLS[url]}:")
        response = requests.get(URLS[url])
        soup = BeautifulSoup(response.text, "html.parser")
        site_data = soup.select(selector=SELECTORS[url])
        for article in site_data:
            print(f"{article.text} - https://gamepod.hu{article.get('href')}")


if __name__ == '__main__':
    """Running get news and getting performance stats for the 10 top items ordered by time."""
    with cProfile.Profile() as pr:
        get_news()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(10)
