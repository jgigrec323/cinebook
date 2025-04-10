import tkinter as tk
from ttkbootstrap import Window
from ttkbootstrap.widgets import Button, Entry, Combobox
from modules.movie_loader import load_movies
from modules.card_renderer import render_movie_card
from modules.movie_detail import show_movie_detail
from fuzzywuzzy import fuzz

# === GLOBAL STATE ===
current_user = {"username": "Guest"}
BG_COLOR = "#1f1f1f"
MOVIES_PER_LOAD = 21
movie_offset = 0


# === APP SETUP ===
app = Window(themename="darkly")
app.title("CineBook 🎬")
app.geometry("1200x700")

selected_genre = tk.StringVar()
selected_sort = tk.StringVar()


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
top_bar.pack(fill="x", pady=25, padx=20)

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

reset_btn = Button(top_bar, text="Reset", bootstyle="danger-outline", command=lambda: reset_search())
reset_btn.pack(side="left", padx=(10, 0))

# tk.Label(top_bar, text=f"👤 {current_user['username']}", font=("Helvetica", 14), bg=BG_COLOR, fg="white").pack(side="right", padx=10)

tk.Label(content, text="Welcome to CineBook", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="white").pack(anchor="w", padx=20, pady=(0, 10))

# === FILTER BAR ===
filter_bar = tk.Frame(content, bg=BG_COLOR)
filter_bar.pack(fill="x", padx=20, pady=10)

# Load movies and extract genres dynamically
original_movies = load_movies()
all_movies = original_movies.copy()

genre_set = set()
for movie in original_movies:
    genres = movie.get("Genre", "").split(", ")
    genre_set.update(genres)

genre_list = ["All"] + sorted(genre_set)

tk.Label(filter_bar, text="🎭 Genre:", bg=BG_COLOR, fg="white", font=("Helvetica", 10)).pack(side="left", padx=(0, 5))
genre_box = Combobox(filter_bar, textvariable=selected_genre, values=genre_list, width=20)
genre_box.current(0)
genre_box.pack(side="left", padx=(0, 20))

tk.Label(filter_bar, text="⬇ Sort by:", bg=BG_COLOR, fg="white", font=("Helvetica", 10)).pack(side="left", padx=(0, 5))
sort_box = Combobox(filter_bar, textvariable=selected_sort, values=["Default", "Rating High → Low", "Year New → Old"], width=20)
sort_box.current(0)
sort_box.pack(side="left")

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
no_results_label = tk.Label(movie_frame, text="😢 No movies found", font=("Helvetica", 14), fg="white", bg=BG_COLOR)

def refresh_display():
    for widget in movie_widgets:
        widget.destroy()
    movie_widgets.clear()
    no_results_label.pack_forget()
    display_movies()

def reset_search():
    search_var.set("")
    search_entry.delete(0, tk.END)
    search_entry.insert(0, "Search a movie...")
    selected_genre.set("All")
    genre_box.current(0)
    selected_sort.set("Default")
    sort_box.current(0)
    search_movies()

def search_movies(event=None):
    global all_movies, movie_offset
    query = search_var.get().strip().lower()
    selected = selected_genre.get()
    sort_type = selected_sort.get()
    movie_offset = 0

    filtered = original_movies

    if query and query != "search a movie...":
        filtered = [m for m in filtered if fuzz.partial_ratio(query, m["Title"].lower()) >= 60]

    if selected != "All":
        filtered = [m for m in filtered if selected.lower() in m.get("Genre", "").lower()]

    if sort_type == "Rating High → Low":
        filtered.sort(key=lambda m: float(m.get("imdbRating", "0")), reverse=True)
    elif sort_type == "Year New → Old":
        filtered.sort(key=lambda m: int(m.get("Year", "0")), reverse=True)

    all_movies.clear()
    all_movies.extend(filtered)
    refresh_display()

search_var.trace_add("write", lambda *args: search_movies())
selected_genre.trace_add("write", lambda *args: search_movies())
selected_sort.trace_add("write", lambda *args: search_movies())

def display_movies():
    global movie_offset
    visible_movies = all_movies[movie_offset:movie_offset + MOVIES_PER_LOAD]
    if not visible_movies:
        no_results_label.pack(pady=20)
        return

    cols = 7
    for index, movie in enumerate(visible_movies):
        row, col = (movie_offset + index) // cols, (movie_offset + index) % cols
        delay = index * 40  # Animation delay
        card = render_movie_card(movie_frame, movie, row, col, lambda m=movie: show_movie_detail(app, m, current_user, ask_login=True), delay)
        if card:
            movie_widgets.append(card)
    movie_offset += MOVIES_PER_LOAD

# === INIT ===
display_movies()
Button(movie_frame, text="Load More", bootstyle="secondary", command=display_movies).grid(columnspan=7, pady=30)

# === RUN ===
app.mainloop()
