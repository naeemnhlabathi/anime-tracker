"""
Tracker layer - handles saving/loading the personal watchlist.

Kept separate from the GUI (main.py) for the same reason api.py is separate:
this is "talk to a file" logic, not "draw a window" logic.
"""

import json
import os

LIST_FILE = "watchlist.json"


def load_list():
    """Return the saved watchlist as a list of dicts. Empty list if none saved yet."""
    if not os.path.exists(LIST_FILE):
        return []

    with open(LIST_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_show(show):
    """Add a show (dict) to the watchlist and write it to disk. Skips duplicates by title."""
    shows = load_list()

    if any(s["title"] == show["title"] for s in shows):
        return False  # already saved, nothing to do

    shows.append(show)
    _write_list(shows)
    return True


def remove_show(title):
    """Remove a show by title and write the updated list to disk."""
    shows = load_list()
    shows = [s for s in shows if s["title"] != title]
    _write_list(shows)


def _write_list(shows):
    with open(LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(shows, f, indent=2)
