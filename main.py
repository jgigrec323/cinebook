import tkinter as tk
from ttkbootstrap import Window
from ttkbootstrap.widgets import Button, Entry
from modules.movie_loader import load_movies
from modules.card_renderer import render_movie_card
from modules.movie_detail import show_movie_detail

# Global user session
current_user = {"username": "Guest"}

# === APP SETUP ===
app = Window(themename="darkly")
app.title("CineBook 🎬")
app.geometry("1200x700")

BG_COLOR = "#1f1f1f"
MOVIES_PER_LOAD = 21
movie_offset = 0

main_frame = tk.Frame(app, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

# === SIDEBAR ===
sidebar = tk.Frame(main_frame, width=250, bg="#222")
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
sidebar_inner = tk.Frame(sidebar, bg="#222")
sidebar_inner.pack(fill="both", expand=True, padx=20, pady=30)
tk.Label(sidebar_inner, text="🎬", font=("Helvetica", 32), bg="#222", fg="#ff6600").pack(anchor="w", pady=(0, 40))

def create_sidebar_link(text):
    return tk.Label(sidebar_inner, text=text, font=("Helvetica", 14), bg="#222", fg="white", anchor="w", padx=5)

create_sidebar_link("Movies").pack(fill="x", pady=10)
create_sidebar_link("My Bookings").pack(fill="x", pady=10)
create_sidebar_link("Settings").pack(fill="x", pady=10)

# === MAIN CONTENT ===
content = tk.Frame(main_frame, bg=BG_COLOR)
content.pack(side="left", fill="both", expand=True)

# === TOP BAR ===
top_bar = tk.Frame(content, bg=BG_COLOR)
top_bar.pack(fill="x", pady=30, padx=20)

search_var = tk.StringVar()
search_entry = Entry(top_bar, font=("Helvetica", 12), width=40, textvariable=search_var)
search_entry.pack(side="left", padx=10)
search_entry.insert(0, "Search a movie...")

def clear_placeholder(event):
    if search_entry.get() == "Search a movie...":
        search_entry.delete(0, tk.END)

def restore_placeholder(event):
    if not search_entry.get():
        search_entry.insert(0, "Search a movie...")

search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", restore_placeholder)

tk.Label(top_bar, text=f"👤 {current_user['username']}", font=("Helvetica", 14), bg=BG_COLOR, fg="white").pack(side="right", padx=10)

tk.Label(content, text="Welcome to CineBook", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="white").pack(anchor="w", padx=20, pady=(0, 20))

# === MOVIE GRID ===
grid_canvas = tk.Canvas(content, bg=BG_COLOR, highlightthickness=0)
grid_canvas.pack(side="top", fill="both", expand=True)

scroll_y = tk.Scrollbar(content, orient="vertical", command=grid_canvas.yview)
scroll_y.pack(side="right", fill="y")

grid_canvas.configure(yscrollcommand=scroll_y.set)
movie_frame = tk.Frame(grid_canvas, bg=BG_COLOR)
grid_canvas.create_window((0, 0), window=movie_frame, anchor="nw")
movie_frame.bind("<Configure>", lambda e: grid_canvas.configure(scrollregion=grid_canvas.bbox("all")))

movie_widgets = []
all_movies = load_movies()

def display_movies():
    global movie_offset
    visible_movies = all_movies[movie_offset:movie_offset + MOVIES_PER_LOAD]
    cols = 7
    for index, movie in enumerate(visible_movies):
        row, col = (movie_offset + index) // cols, (movie_offset + index) % cols
        card = render_movie_card(movie_frame, movie, row, col, lambda m=movie: show_movie_detail(app, m, current_user, ask_login=True))
        if card:
            movie_widgets.append(card)
    movie_offset += MOVIES_PER_LOAD

display_movies()
Button(movie_frame, text="Load More", bootstyle="secondary", command=display_movies).grid(columnspan=7, pady=30)

app.mainloop()
