# Personal Reading Management Platform

A full-stack web application for managing reading progress across online series. Users can save chapter URLs, automatically extract title and chapter information, and manage their reading list through a web interface.

## Features

- Add reading entries by providing a chapter URL
- Automatically extract title and chapter information with BeautifulSoup
- Update an existing series when a new chapter URL is added
- View saved reading entries
- Open chapters directly from the reading list
- Delete reading entries
- Persist reading data in PostgreSQL

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, SQLAlchemy
- **Web Scraping:** BeautifulSoup
- **Frontend:** HTML, CSS, JavaScript

## Architecture

```text
Frontend
   ↓
FastAPI REST API
   ↓
SQLAlchemy
   ↓
PostgreSQL
