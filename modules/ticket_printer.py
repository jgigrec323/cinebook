def save_ticket_to_file(info):
    filename = f"{info['name'].replace(' ', '_')}_{info['movie'].replace(' ', '_')}_ticket.txt"
    content = f"""
=========== 🎟️ YOUR MOVIE TICKET 🎟️ ===========
👤 Name:     {info['name']}
🎬 Movie:    {info['movie']}
⭐ Rating:   {info['rating']}   📅 Year: {info['year']}

📍 Seat:     {info['seat']}
🕓 Time:     {info['time']}
📅 Date:     {info['date']}  (Expires: {info['expires']})

💵 Price:    {info['price']} TRY
📌 Note:     Payment due at the door

===============================================
Enjoy your movie!
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✅] Ticket saved as {filename}")
