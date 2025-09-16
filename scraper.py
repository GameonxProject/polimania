import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://halu.serv00.net/poli.php"
OUTPUT = "volleyballworld.json"

def scrape():
    print(f"[INFO] Fetching {URL} ...")
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    jadwal = []
    cards = soup.find_all("div", class_="card")  # sesuaikan class sesuai sumber
    for card in cards:
        title = card.find("h3").get_text(strip=True) if card.find("h3") else "No title"
        src = card.find("a")["href"] if card.find("a") else ""
        poster = card.find("img")["src"] if card.find("img") else ""
        start = card.get("data-start") or datetime.utcnow().isoformat()

        # Fix otomatis path dan resolusi
        if "/fM9jRrkN/" in src:
            src = src.replace("/fM9jRrkN/", "/fM9jRrkn/")
        if "width=320" in src:
            src = src.replace("width=320", "width=1920")

        jadwal.append({
            "title": title,
            "start": start,
            "src": src,
            "poster": poster
        })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(jadwal, f, indent=2, ensure_ascii=False)

    print(f"[OK] {len(jadwal)} jadwal tersimpan ke {OUTPUT}")

if __name__ == "__main__":
    scrape()
