"""
API layer - handles all communication with AniList.

Kept separate from the GUI (main.py) so the search logic isn't tangled
up with window/button code - it could be tested or reused on its own.
"""

import requests

ANILIST_URL = "https://graphql.anilist.co"

SEARCH_QUERY = """
query ($search: String) {
  Media (search: $search, type: ANIME) {
    title {
      romaji
      english
    }
    averageScore
    episodes
    genres
    description(asHtml: false)
    coverImage {
      medium
    }
  }
}
"""


def search_anime(title):
    """Search for an anime by title, return the top match as a dict (or None).

    Raises a plain-English RuntimeError on network problems, so the GUI
    can show something a user can actually understand instead of a
    raw requests/connection traceback.
    """
    variables = {"search": title}

    try:
        response = requests.post(
            ANILIST_URL,
            json={"query": SEARCH_QUERY, "variables": variables},
            timeout=10,
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("The request timed out. Check your internet connection and try again.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Couldn't reach AniList. Check your internet connection.")

    if response.status_code == 429:
        raise RuntimeError("Too many searches too quickly - wait a few seconds and try again.")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError(f"AniList returned an error (status {response.status_code}). Try again in a moment.")

    data = response.json()
    return data.get("data", {}).get("Media")
