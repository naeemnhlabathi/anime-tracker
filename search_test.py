"""
Step 1: just prove the API call works.
No GUI yet - search a title, print the data back.

Uses AniList's GraphQL API - no signup, no API key needed.
Docs: https://docs.anilist.co/
"""

import requests

ANILIST_URL = "https://graphql.anilist.co"

# GraphQL query: ask AniList for exactly the fields we need
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
    return data.get("data", {}).get("Media")  # None if no match found


if __name__ == "__main__":
    query = input("Search for an anime: ")
    result = search_anime(query)

    if result is None:
        print(f"No results found for '{query}'")
    else:
        title = result["title"]["english"] or result["title"]["romaji"]
        print()
        print("Title:", title)
        print("Score:", result.get("averageScore"))
        print("Episodes:", result.get("episodes"))
        print("Genres:", ", ".join(result.get("genres", [])))
        print()
        description = (result.get("description") or "").replace("<br>", "")
        print("Synopsis:", description[:300], "...")
