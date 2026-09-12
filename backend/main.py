from database import engine, SessionLocal
from models import Base, Comic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parsers.manager import get_latest_chapter
from parsers.asura import AsuraParse
from parsers.katana import MangaKatanaParse

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/reading")
def add_reading(url: str):
    data = get_latest_chapter(url)

    db = SessionLocal()

    comic = db.query(Comic).filter(Comic.title == data["title"]).first()

    if comic:
        comic.latest_chapter = data["chapter"]
    else:
        comic = Comic(
            title=data["title"],
            series_url=url,
            latest_chapter=data["chapter"],
            current_chapter=data["chapter"],
            current_url=data["url"]
        )

    db.add(comic)
    db.commit()

    return comic


@app.get("/reading")
def get_reading():
    db = SessionLocal()
    comics = db.query(Comic).all()

    return comics


@app.put("/reading/{comic_id}")
def update_chapter(comic_id: int, current_chapter: str):
    db = SessionLocal()

    comic = db.query(Comic).filter(Comic.id == comic_id).first()

    if not comic:
        return {"error": "Reading not found"}

    parsers = [
        AsuraParse(),
        MangaKatanaParse()
    ]

    parser = next(
        (p for p in parsers if p.can_handle(comic.series_url)),
        None
    )

    if not parser:
        return {"error": "No parser available for this site"}

    chapters = parser.get_chapters(comic.series_url)

    print("SERIES URL:", comic.series_url)
    print("REQUESTED CHAPTER:", current_chapter)
    print("CHAPTERS FOUND:", chapters)

    requested_chapter = float(current_chapter)

    matching_chapter = next(
        (
            chapter for chapter in chapters
            if float(chapter["chapter"]) == requested_chapter
        ),
        None
    )

    if not matching_chapter:
        return {"error": "Chapter not found"}

    comic.current_chapter = current_chapter
    comic.current_url = matching_chapter["url"]

    db.commit()
    db.refresh(comic)

    print("UPDATED:", comic.current_chapter, comic.current_url)

    return comic


@app.delete("/reading/{comic_id}")
def delete_reading(comic_id: int):
    db = SessionLocal()

    comic = db.query(Comic).filter(Comic.id == comic_id).first()

    if not comic:
        return {"error": "Reading not found"}

    db.delete(comic)
    db.commit()

    return {"message": "Reading deleted"}