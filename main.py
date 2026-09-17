"""
Anime Tracker - main application window.

Step 3: search + save shows to a personal watchlist (stored in watchlist.json).
"""

import tkinter as tk
from tkinter import messagebox

from api import search_anime
from tracker import load_list, save_show, remove_show

current_result = None  # holds the last searched show, so Save knows what to save


def perform_search():
    global current_result
    title = search_entry.get().strip()
    if not title:
        messagebox.showinfo("Nothing to search", "Type a title first.")
        return

    current_result = None
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Searching...")
    search_button.config(state=tk.DISABLED)  # avoid double-clicks firing overlapping requests
    root.update_idletasks()  # show "Searching..." before the request blocks the UI

    try:
        result = search_anime(title)
    except RuntimeError as e:
        # Friendly errors raised deliberately in api.py (bad connection, rate limit, etc.)
        result_text.delete("1.0", tk.END)
        messagebox.showerror("Search failed", str(e))
        return
    except Exception as e:
        # Anything unexpected we didn't plan for
        result_text.delete("1.0", tk.END)
        messagebox.showerror("Unexpected error", f"Something went wrong:\n{e}")
        return
    finally:
        search_button.config(state=tk.NORMAL)

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

    # Stash what we need to save, separate from the raw API result
    current_result = {
        "title": show_title,
        "episodes": episodes_display,
        "genres": genres,
    }


def save_current():
    if current_result is None:
        messagebox.showinfo("Nothing to save", "Search for a show first.")
        return

    added = save_show(current_result)
    if added:
        messagebox.showinfo("Saved", f"'{current_result['title']}' added to your list.")
    else:
        messagebox.showinfo("Already saved", f"'{current_result['title']}' is already on your list.")


def open_my_list():
    list_window = tk.Toplevel(root)
    list_window.title("My List")
    list_window.geometry("400x400")

    shows = load_list()

    if not shows:
        tk.Label(list_window, text="No shows saved yet.").pack(pady=20)
        return

    for show in shows:
        row = tk.Frame(list_window)
        row.pack(fill=tk.X, padx=10, pady=4)

        label_text = f"{show['title']}  ({show['episodes']} eps)"
        tk.Label(row, text=label_text, anchor="w", wraplength=260, justify=tk.LEFT).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )

        def make_remove_handler(title):
            def handler():
                remove_show(title)
                list_window.destroy()
                open_my_list()  # refresh the window
            return handler

        tk.Button(row, text="Remove", command=make_remove_handler(show["title"])).pack(side=tk.RIGHT)


# --- Build the window ---
root = tk.Tk()
root.title("Anime Tracker")
root.geometry("500x550")

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<Return>", lambda event: perform_search())  # Enter key also searches

search_button = tk.Button(search_frame, text="Search", command=perform_search)
search_button.pack(side=tk.LEFT)

result_text = tk.Text(root, wrap=tk.WORD, width=55, height=22)
result_text.pack(padx=10, pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

save_button = tk.Button(button_frame, text="Save to My List", command=save_current)
save_button.pack(side=tk.LEFT, padx=5)

my_list_button = tk.Button(button_frame, text="View My List", command=open_my_list)
my_list_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
