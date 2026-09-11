import requests
from bs4 import BeautifulSoup
from .base import BaseParse

class AsuraParse(BaseParse):
    def can_handle(self, url):
        return "asurascans.com" in url

    def get_latest_chapter(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.get_text(strip=True)
        title = title.split("|")[0].strip()

        chapters = []

        for link in soup.find_all("a"):
            href = link.get("href")

            if href and "/chapter/" in href:
                chapter_number = int(href.split("/chapter/")[-1])

                chapter = {
                    "chapter": chapter_number,
                    "url": href
                }

                if chapter not in chapters:
                    chapters.append(chapter)

        latest = max(chapters, key=lambda x: x["chapter"])

        return {
            "title": title,
            "chapter": latest["chapter"],
            "url": "https://asurascans.com" + latest["url"]
        }