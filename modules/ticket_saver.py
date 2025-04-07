# === modules/ticket_saver.py ===
import json
import os
import uuid
from tkinter import messagebox

TICKET_FILE = "data/tickets.json"
USER_FILE = "data/users.json"

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
