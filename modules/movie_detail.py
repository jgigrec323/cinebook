import tkinter as tk
from ttkbootstrap.widgets import Button
from modules.movie_loader import get_image_from_url
from modules.booking_flow import start_booking_flow

def show_movie_detail(root, movie, current_user, ask_login=False):
    detail_win = tk.Toplevel(root)
    detail_win.title(movie["Title"])
    detail_win.configure(bg="#1f1f1f")
    detail_win.geometry("600x400")

    # === Poster ===
    poster = get_image_from_url(movie["Poster"], size=(180, 260), rounded=False)
    if poster:
        tk.Label(detail_win, image=poster, bg="#1f1f1f").pack(side="left", padx=20, pady=20)
        detail_win.poster_ref = poster

    # === Info Frame ===
    info_frame = tk.Frame(detail_win, bg="#1f1f1f")
    info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=20)

    def detail_label(text, bold=False):
        font = ("Helvetica", 11, "bold") if bold else ("Helvetica", 11)
        return tk.Label(info_frame, text=text, bg="#1f1f1f", fg="white", font=font, wraplength=350, justify="left")

    detail_label(movie["Title"], bold=True).pack(anchor="w", pady=(0, 10))
    detail_label(f"📅 Year: {movie.get('Year', 'N/A')}").pack(anchor="w")
    detail_label(f"⭐ Rating: {movie.get('imdbRating', 'N/A')}").pack(anchor="w")
    detail_label(f"🎭 Genre: {movie.get('Genre', 'N/A')}").pack(anchor="w")
    detail_label(f"🎬 Director: {movie.get('Director', 'N/A')}").pack(anchor="w", pady=(10, 0))
    detail_label(f"Description: {movie.get('Plot', 'N/A')}").pack(anchor="w", pady=(10, 0))

    # === Buttons Section ===
    btn_frame = tk.Frame(info_frame, bg="#1f1f1f")
    btn_frame.pack(pady=20)

    Button(btn_frame, text="🎟️ Book Now", bootstyle="success", width=20,
           command=lambda: start_booking_flow(root, movie, current_user, ask_login)).pack(pady=5)

    Button(btn_frame, text="❌ Close", bootstyle="danger", width=20,
           command=detail_win.destroy).pack()
