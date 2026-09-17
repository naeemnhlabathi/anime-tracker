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
  }
}
"""


def search_anime(title):
    """Search for an anime by title, return the top match as a dict (or None)."""
    variables = {"search": title}

    response = requests.post(
        ANILIST_URL,
        json={"query": SEARCH_QUERY, "variables": variables},
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("data", {}).get("Media")
