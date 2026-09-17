# Anime Tracker

A simple desktop app to search for anime and build a personal watchlist, using the AniList GraphQL API.

## Status

🚧 In progress — currently on: basic API search (step 1)

## Features

- [x] Search for an anime by title and view its details (score, episodes, genres, synopsis)
- [ ] Save a show to a personal watchlist
- [ ] View saved watchlist
- [ ] Remove a show from the watchlist

## Built with

- Python
- [AniList API](https://docs.anilist.co) (GraphQL)
- `requests` for API calls (POST requests to a GraphQL endpoint)
- Tkinter for the GUI
- JSON for local storage

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
