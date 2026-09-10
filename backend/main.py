from parser import parse_page
from database import engine, SessionLocal
from models import Base, Comic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    data = parse_page(url)

    db = SessionLocal()

    comic = db.query(Comic).filter(Comic.title == data["title"]).first()

    if comic:
        comic.chapter = data["chapter"]
        comic.url = data["url"]
    else:
        comic = Comic(
            title = data["title"],
            chapter = data["chapter"],
            url = data["url"]
        )

    db.add(comic)
    db.commit()  

    print("AFTER COMMIT:", comic.chapter, comic.url)

    return comic

@app.get("/reading")
def get_reading():
    db = SessionLocal()
    comics = db.query(Comic).all()

    return comics

@app.delete("/reading/{comic_id}")
def delete_reading(comic_id: int):
    db = SessionLocal()

    comic = db.query(Comic).filter(Comic.id == comic_id).first()

    if not comic:
        return {"error": "Reading not found"}

    db.delete(comic)
    db.commit()

    return {"message": "Reading deleted"}