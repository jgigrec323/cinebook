import tkinter as tk
from datetime import datetime, timedelta
from modules.ticket_saver import save_ticket, ask_to_save_user

def start_booking_flow(root, movie, current_user, ask_login=False):
    booking = tk.Toplevel(root)
    booking.title("Book Your Ticket")
    booking.configure(bg="#1f1f1f")
    booking.geometry("600x700")

    selected_seat = tk.StringVar()
    selected_time = tk.StringVar()
    user_name = tk.StringVar(value=current_user.get("username", "Guest"))

    # === NAME ENTRY ===
    tk.Label(booking, text="Your Name", fg="white", bg="#1f1f1f", font=("Helvetica", 12)).pack(pady=5)
    name_entry = tk.Entry(booking, textvariable=user_name, width=30)
    name_entry.pack(pady=5)

    # === SEAT SELECTION ===
    tk.Label(booking, text="Choose Your Seat", fg="white", bg="#1f1f1f", font=("Helvetica", 12)).pack(pady=5)
    seat_frame = tk.Frame(booking, bg="#1f1f1f")
    seat_frame.pack(pady=5)

    selected_label = tk.Label(booking, text="", bg="#1f1f1f", fg="lightgreen", font=("Helvetica", 11))
    selected_label.pack(pady=5)

    def update_selected(seat_id):
        selected_seat.set(seat_id)
        selected_label.config(text=f"✅ Selected seat: {seat_id}")

    for r in range(5):
        for c in range(8):
            seat_id = f"{chr(65 + r)}{c + 1}"
            tk.Button(seat_frame, text=seat_id, width=3, command=lambda s=seat_id: update_selected(s)).grid(row=r, column=c, padx=2, pady=2)

    # === TIME SLOT SELECTION ===
    tk.Label(booking, text="Choose Time", fg="white", bg="#1f1f1f", font=("Helvetica", 12)).pack(pady=10)
    for t in ["15:00", "17:30", "20:00"]:
        tk.Radiobutton(booking, text=t, variable=selected_time, value=t, bg="#1f1f1f", fg="white").pack(anchor="w", padx=50)

    # === CONFIRMATION ===
    def confirm():
        now = datetime.now()
        ticket_info = {
            "user": user_name.get(),
            "movie": movie["Title"],
            "rating": movie.get("imdbRating", "N/A"),
            "year": movie.get("Year", "N/A"),
            "seat": selected_seat.get(),
            "time": selected_time.get(),
            "date": now.strftime("%Y-%m-%d"),
            "expires": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            "price": round(float(movie.get("imdbRating", 5)) * 10)
        }

        save_ticket(ticket_info)

        if ask_login:
            ask_to_save_user(user_name.get())

        booking.destroy()

    tk.Button(booking, text="🎟️ Confirm Booking", command=confirm).pack(pady=20)
    tk.Button(booking, text="❌ Cancel", command=booking.destroy).pack(pady=5)
