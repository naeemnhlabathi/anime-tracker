"""
Anime Tracker - main application window.

Step 5: cover images, a watch-status tag, and cleaner spacing.
"""

import base64
import io

import tkinter as tk
from tkinter import messagebox, ttk

import requests
from PIL import Image, ImageTk

from api import search_anime
from tracker import load_list, save_show, remove_show

STATUS_OPTIONS = ["Plan to Watch", "Watching", "Completed"]

current_result = None  # holds the last searched show, so Save knows what to save
cover_image = None  # keeps a reference to the current PhotoImage (Tkinter needs this or it gets garbage collected)


def fetch_cover_image(url):
    """Download a cover image and return it as a Tkinter-displayable image, or None if it fails.

    AniList cover images are JPEGs, which Tkinter's built-in PhotoImage can't decode
    (it only understands GIF/PNG) - so this goes through Pillow instead.
    """
    if not url:
        return None
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        image.thumbnail((120, 170))  # keep it a reasonable size next to the results box
        return ImageTk.PhotoImage(image)
    except Exception:
        # A missing/broken cover image shouldn't break the whole search
        return None


def perform_search():
    global current_result, cover_image
    title = search_entry.get().strip()
    if not title:
        messagebox.showinfo("Nothing to search", "Type a title first.")
        return

    current_result = None
    cover_image = None
    cover_label.config(image="", text="")
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

    # Cover image (best-effort - falls back to no image if the URL is missing or download fails)
    cover_url = (result.get("coverImage") or {}).get("medium")
    cover_image = fetch_cover_image(cover_url)
    if cover_image:
        cover_label.config(image=cover_image, text="")
    else:
        cover_label.config(image="", text="(no cover)")

    # Stash what we need to save, separate from the raw API result
    current_result = {
        "title": show_title,
        "episodes": episodes_display,
        "genres": genres,
        "status": status_var.get(),
    }


def save_current():
    if current_result is None:
        messagebox.showinfo("Nothing to save", "Search for a show first.")
        return

    # Pick up whatever status is selected right now, in case they changed it after searching
    current_result["status"] = status_var.get()

    added = save_show(current_result)
    if added:
        messagebox.showinfo("Saved", f"'{current_result['title']}' added as \"{current_result['status']}\".")
    else:
        messagebox.showinfo("Already saved", f"'{current_result['title']}' is already on your list.")


def open_my_list():
    list_window = tk.Toplevel(root)
    list_window.title("My List")
    list_window.geometry("420x420")

    shows = load_list()

    if not shows:
        tk.Label(list_window, text="No shows saved yet.", pady=20).pack()
        return

    for show in shows:
        row = tk.Frame(list_window, relief=tk.GROOVE, borderwidth=1)
        row.pack(fill=tk.X, padx=10, pady=5)

        info_frame = tk.Frame(row)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, pady=6)

        title_text = f"{show['title']}  ({show['episodes']} eps)"
        tk.Label(info_frame, text=title_text, anchor="w", wraplength=250, justify=tk.LEFT, font=("TkDefaultFont", 10, "bold")).pack(
            anchor="w"
        )

        status = show.get("status", "Plan to Watch")  # older saved entries won't have a status yet
        tk.Label(info_frame, text=status, anchor="w", fg="gray30").pack(anchor="w")

        def make_remove_handler(title):
            def handler():
                remove_show(title)
                list_window.destroy()
                open_my_list()  # refresh the window
            return handler

        tk.Button(row, text="Remove", command=make_remove_handler(show["title"])).pack(side=tk.RIGHT, padx=8)


# --- Build the window ---
root = tk.Tk()
root.title("Anime Tracker")
root.geometry("520x650")

search_frame = tk.Frame(root)
search_frame.pack(pady=12)

search_entry = tk.Entry(search_frame, width=35)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<Return>", lambda event: perform_search())  # Enter key also searches

search_button = tk.Button(search_frame, text="Search", command=perform_search)
search_button.pack(side=tk.LEFT, padx=(0, 10))

status_var = tk.StringVar(value=STATUS_OPTIONS[0])
status_dropdown = ttk.Combobox(search_frame, textvariable=status_var, values=STATUS_OPTIONS, width=13, state="readonly")
status_dropdown.pack(side=tk.LEFT)

content_frame = tk.Frame(root)
content_frame.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)

cover_label = tk.Label(content_frame, width=15, height=8, bg="gray90")
cover_label.pack(side=tk.LEFT, anchor="n", padx=(0, 10))

result_text = tk.Text(content_frame, wrap=tk.WORD, width=45, height=22)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

save_button = tk.Button(button_frame, text="Save to My List", command=save_current)
save_button.pack(side=tk.LEFT, padx=5)

my_list_button = tk.Button(button_frame, text="View My List", command=open_my_list)
my_list_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
