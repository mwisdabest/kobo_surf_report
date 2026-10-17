import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

URL = "https://www.swellnet.com/forecasts/australia/victoria/phillip-island"

html = requests.get(URL, timeout=10).text
soup = BeautifulSoup(html, "html.parser")

# Extract current conditions
current = soup.find("div", class_="current-conditions")
current_text = current.get_text("\n", strip=True) if current else "Current conditions unavailable."

# Extract 3-day forecast
forecast_days = soup.find_all("div", class_="forecast-day")
forecast_text = "\n\n".join(
    day.get_text("\n", strip=True) for day in forecast_days[:3]
) if forecast_days else "3‑day forecast unavailable."

# Kobo Aura resolution
WIDTH, HEIGHT = 758, 1024
img = Image.new("L", (WIDTH, HEIGHT), 255)
draw = ImageDraw.Draw(img)

font_title = ImageFont.load_default()
font_body = ImageFont.load_default()

y = 20
draw.text((20, y), "Phillip Island Surf", font=font_title, fill=0)
y += 40
draw.text((20, y), f"Updated: {datetime.now().strftime('%d %b %Y %H:%M')}", font=font_body, fill=0)
y += 40

draw.text((20, y), "Current conditions", font=font_title, fill=0)
y += 30
draw.multiline_text((20, y), current_text, font=font_body, fill=0, spacing=4)
y += 260

draw.text((20, y), "3‑day forecast", font=font_title, fill=0)
y += 30
draw.multiline_text((20, y), forecast_text, font=font_body, fill=0, spacing=4)

# Create public folder
os.makedirs("public", exist_ok=True)

# Save dashboard image
img.save("public/phillip_island_dashboard.png")
