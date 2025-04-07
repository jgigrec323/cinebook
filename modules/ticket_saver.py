# === modules/ticket_saver.py ===
import json
import os
import uuid
import qrcode
from PIL import Image
from tkinter import messagebox
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
import webbrowser

TICKET_FILE = "data/tickets.json"
USER_FILE = "data/users.json"
PDF_DIR = "data/tickets"

os.makedirs(PDF_DIR, exist_ok=True)

def save_ticket(ticket):
    if not os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "w") as f:
            json.dump([], f)
    with open(TICKET_FILE, "r") as f:
        tickets = json.load(f)

    ticket['id'] = str(uuid.uuid4())
    tickets.append(ticket)

    with open(TICKET_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

    pdf_path = generate_ticket_pdf(ticket)
    open_pdf(pdf_path)

def load_user_tickets(username):
    if not os.path.exists(TICKET_FILE):
        return []
    with open(TICKET_FILE, "r") as f:
        all_tickets = json.load(f)
    return [t for t in all_tickets if t.get("user") == username]

def save_user_info(username):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump([], f)
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    if username not in users:
        users.append(username)
        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

def ask_to_save_user(username):
    answer = messagebox.askyesno("Save User Info", f"Do you want to save the name '{username}' for future bookings?")
    if answer:
        save_user_info(username)

def generate_ticket_pdf(ticket):
    pdf_path = os.path.join(PDF_DIR, f"ticket_{ticket['id']}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A5)
    width, height = A5

    padding = 30
    y = height - padding

    c.setFont("Helvetica-Bold", 18)
    c.drawString(padding, y, "🎟️  CineBook Ticket")
    y -= 35

    c.setFont("Helvetica", 12)
    line_spacing = 22
    lines = [
        f"👤 Name: {ticket['id']}",
        f"👤 Name: {ticket['user']}",
        f"🎬 Movie: {ticket['movie']}",
        f"⭐ Rating: {ticket['rating']}    📅 Year: {ticket['year']}",
        f"📍 Seat: {ticket['seat']}",
        f"📅 Date: {ticket['date']}    ⏰ Time: {ticket['time']}",
        f"💰 Price: {ticket['price']} TRY",
        f"🕓 Expires: {ticket['expires']}",
        f"💵 This ticket will be paid at the door"
    ]

    for line in lines:
        c.drawString(padding, y, line)
        y -= line_spacing

    # === QR CODE ===
    qr_data = f"{ticket['user']} | {ticket['movie']} | Seat: {ticket['seat']} | {ticket['date']} {ticket['time']} | ID: {ticket['id']}"
    qr_img = qrcode.make(qr_data)
    qr_temp_path = os.path.join(PDF_DIR, f"qr_{ticket['id']}.png")
    qr_img.save(qr_temp_path)

    c.drawImage(qr_temp_path, width - 150, 60, width=100, height=100)

    c.save()
    os.remove(qr_temp_path)
    print(f"✅ PDF generated: {pdf_path}")
    return pdf_path

def open_pdf(path):
    try:
        webbrowser.open_new(path)
    except Exception as e:
        print(f"Could not open PDF: {e}")
