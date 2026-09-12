import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .base import BaseParse


class MangaKatanaParse(BaseParse):

    def can_handle(self, url):
        return "mangakatana.com" in url

    def get_chapters(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        chapters = []

        for link in soup.find_all("a"):
            href = link.get("href")
            text = link.get_text(strip=True)

            if href and href.startswith(url + "/c") and text.startswith("Chapter "):
                href = urljoin(url, href)

                chapter_number = text.split(":")[0].replace("Chapter ", "").strip()

                chapter = {
                    "chapter": chapter_number,
                    "url": href
                }

                if chapter not in chapters:
                    chapters.append(chapter)

        return chapters

    def get_latest_chapter(self, url):
        chapters = self.get_chapters(url)

        def is_numeric(chapter):
            try:
                float(chapter)
                return True
            except ValueError:
                return False

        numeric_chapters = [
            x for x in chapters
            if is_numeric(x["chapter"])
        ]

        latest = max(
            numeric_chapters,
            key=lambda x: float(x["chapter"])
        )

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").get_text(strip=True)

        return {
            "title": title,
            "chapter": latest["chapter"],
            "url": latest["url"]
        }

