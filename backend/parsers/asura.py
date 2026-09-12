import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .base import BaseParse


class AsuraParse(BaseParse):
    def can_handle(self, url):
        return "asurascans.com" in url

    def get_chapters(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        chapters = []

        for link in soup.find_all("a"):
            href = link.get("href")

            if href and "/chapter/" in href:
                href = urljoin(url, href)

                chapter_number = int(href.split("/chapter/")[-1])

                chapter = {
                    "chapter": chapter_number,
                    "url": href
                }

                if chapter not in chapters:
                    chapters.append(chapter)

        return chapters

    def get_latest_chapter(self, url):
        chapters = self.get_chapters(url)

        latest = max(chapters, key=lambda x: x["chapter"])

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.get_text(strip=True)
        title = title.split("|")[0].strip()

        return {
            "title": title,
            "chapter": latest["chapter"],
            "url": latest["url"]
        }

parser = AsuraParse()

chapters = parser.get_latest_chapter(
    "https://asurascans.com/comics/magic-academys-genius-blinker-53fc8424"
)

print(chapters)