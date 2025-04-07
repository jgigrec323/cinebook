import tkinter as tk
from ttkbootstrap.widgets import Button
from modules.movie_loader import get_image_from_url

CARD_BG = "#2a2a2a"
POSTER_SIZE = (140, 200)

def render_movie_card(parent, movie, row, col, on_view_callback):
    poster_img = get_image_from_url(movie["Poster"], size=POSTER_SIZE)
    if not poster_img:
        return None

    card = tk.Frame(parent, bg=CARD_BG, width=160, height=300, highlightthickness=1, highlightbackground="#3a3a3a")
    card.grid(row=row, column=col, padx=10, pady=10)

    img_label = tk.Label(card, image=poster_img, bg=CARD_BG)
    img_label.image = poster_img
    img_label.pack(pady=5)

    title = movie["Title"][:25] + "..." if len(movie["Title"]) > 25 else movie["Title"]
    tk.Label(card, text=title, font=("Helvetica", 11, "bold"), bg=CARD_BG, fg="white", wraplength=140).pack()

    info_text = f"⭐ {movie.get('imdbRating', 'N/A')}   📅 {movie.get('Year', 'N/A')}"
    tk.Label(card, text=info_text, font=("Helvetica", 10), bg=CARD_BG, fg="#bbbbbb").pack(pady=3)

    Button(card, text="View", bootstyle="success-outline", command=on_view_callback).pack(pady=5)
    return card
