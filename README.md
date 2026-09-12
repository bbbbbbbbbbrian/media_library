# Webtoon Vault

A full-stack reading management platform for organizing online series. Users can provide a chapter URL, automatically extract the series title and chapter information, and keep their reading progress synchronized through a web interface.

## How It Works

1. The user provides a chapter URL.
2. The FastAPI backend fetches and parses the webpage using BeautifulSoup.
3. The parser extracts the series title and chapter information.
4. The database is checked for an existing series.
5. If the series exists, its chapter and URL are updated; otherwise, a new entry is created.
6. Saved entries can be viewed and opened directly from the reading list.

```text
Chapter URL
     ↓
FastAPI
     ↓
BeautifulSoup
     ↓
Extract Title + Chapter
     ↓
Check PostgreSQL
     ↓
Create / Update Entry
     ↓
Reading List
```

## Tech Stack

* Python
* FastAPI — REST API and backend
* PostgreSQL — persistent reading data
* SQLAlchemy — database ORM
* BeautifulSoup — webpage parsing
* HTML / CSS / JavaScript — frontend

## Project Structure

```text
media_library/
├── backend/
│   └── ...
├── frontend/
│   └── ...
└── README.md
```

* `backend/` — FastAPI application, database models, and web scraping logic
* `frontend/` — web interface for managing the reading list

## Example

Given a chapter URL such as:

```text
https://example.com/series-name/chapter-42
```

The backend extracts the series information and stores it in PostgreSQL.

If the series is already in the library, adding a new chapter updates the existing entry rather than creating a duplicate.

```text
Before:
Series Name → Chapter 41

Add Chapter 42
      ↓

After:
Series Name → Chapter 42
```

## REST API

The backend provides endpoints for managing reading entries:

* `POST /reading` — add a chapter URL or update an existing series
* `GET /reading` — retrieve saved reading entries
* `PUT /reading/{id}` — update an entry
* `DELETE /reading/{id}` — delete an entry

## Why I Built This

I wanted to build something more useful than a basic CRUD application while getting experience working with real-world web data.

The project combines web scraping, REST APIs, relational databases, and frontend development to turn unstructured chapter URLs into structured reading data that can be automatically maintained.
