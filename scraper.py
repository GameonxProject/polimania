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
    for card in soup.select("div.card"):
        a = card.find("a")
        img = card.find("img")
        small = card.find("small")

        title = img["alt"].strip() if img and "alt" in img.attrs else a.get_text(strip=True)
        src = a["href"] if a else ""
        poster = img["src"] if img else ""
        start_text = small.get_text(strip=True) if small else ""

        # kalau ada tulisan LIVE → pakai waktu sekarang
        if "LIVE" in start_text.upper():
            start = datetime.utcnow().isoformat()
        else:
            start = start_text or datetime.utcnow().isoformat()

        # Fix otomatis path dan resolusi
        if "/fM9jRrkN/" in src:
            src = src.replace("/fM9jRrkN/", "/fM9jRrkn/")
        if "width=320" in poster:
            poster = poster.replace("width=320", "width=1920")

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
