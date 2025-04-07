import json
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO

def load_movies():
    with open("data/movies.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_image_from_url(url, size=(160, 240), rounded=True):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).resize(size)

        if rounded:
            image = image.convert("RGBA")
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, *size), radius=20, fill=255)
            image.putalpha(mask)

        return ImageTk.PhotoImage(image)
    except:
        return None
