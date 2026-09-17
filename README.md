# Anime Tracker

A desktop app to search for anime and build a personal watchlist, using the AniList GraphQL API.

## Status

✅ Core features complete — search, save, view, and remove all working. Polishing from here.

## Features

- [x] Search for an anime by title and view its details (score, episodes, genres, synopsis, cover image)
- [x] Save a show to a personal watchlist, with a watch status (Plan to Watch / Watching / Completed)
- [x] View saved watchlist
- [x] Remove a show from the watchlist

## Built with

- Python
- [AniList API](https://docs.anilist.co) (GraphQL)
- `requests` for API calls (POST requests to a GraphQL endpoint)
- `Pillow` for decoding and displaying cover images (Tkinter alone can't handle JPEGs)
- Tkinter for the GUI
- JSON for local storage

## Project structure

- `main.py` — the GUI window and all its event handling
- `api.py` — talks to the AniList API, returns plain data (no GUI code in here)
- `tracker.py` — reads/writes the local watchlist file (no GUI code in here either)

Kept as three separate files on purpose, so each piece can be understood, tested, or changed on its own.

## How to run

1. Clone this repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   python main.py
   ```

## Why I built this

Personal project to practice working with external APIs and local data storage — skills my university coursework hasn't covered yet.
