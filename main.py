"""
Anime Tracker - main application window.

Step 2: search box + results display, wired up to the AniList API.
"""

import tkinter as tk
from tkinter import messagebox

from api import search_anime


def perform_search():
    title = search_entry.get().strip()
    if not title:
        return

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Searching...")
    root.update_idletasks()  # show "Searching..." before the request blocks the UI

    try:
        result = search_anime(title)
    except Exception as e:
        result_text.delete("1.0", tk.END)
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
        return

    result_text.delete("1.0", tk.END)

    if result is None:
        result_text.insert(tk.END, f"No results found for '{title}'")
        return

    show_title = result["title"]["english"] or result["title"]["romaji"]
    episodes = result.get("episodes")
    episodes_display = episodes if episodes is not None else "Ongoing / unknown"
    genres = ", ".join(result.get("genres", []))
    description = (result.get("description") or "").replace("<br>", "")

    display = (
        f"Title: {show_title}\n"
        f"Score: {result.get('averageScore')}\n"
        f"Episodes: {episodes_display}\n"
        f"Genres: {genres}\n\n"
        f"Synopsis:\n{description}"
    )
    result_text.insert(tk.END, display)


# --- Build the window ---
root = tk.Tk()
root.title("Anime Tracker")
root.geometry("500x500")

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<Return>", lambda event: perform_search())  # Enter key also searches

search_button = tk.Button(search_frame, text="Search", command=perform_search)
search_button.pack(side=tk.LEFT)

result_text = tk.Text(root, wrap=tk.WORD, width=55, height=25)
result_text.pack(padx=10, pady=10)

root.mainloop()
