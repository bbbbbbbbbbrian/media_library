import requests
from bs4 import BeautifulSoup

def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title_chapter = soup.title.text
    title, chapter = title_chapter.split("· ", 1)

    return {
        "title": title, 
        "chapter": chapter,
        "url": url
    }

