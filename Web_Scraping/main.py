import requests
from bs4 import BeautifulSoup

response = requests.get('https://gamepod.hu/index.html')
soup = BeautifulSoup(response.text, "html.parser")
site_data = soup.select(
    selector="html body.gp main#page-index div#middle div.container div.row div#center "
             "div.content-list.content-list-detailed ul.list-unstyled li.media div.media-body h4.media-heading a")

print("Latest news from Gamepod:")
for article in site_data:
    print(f"{article.text} - https://gamepod.hu{article.get('href')}")
