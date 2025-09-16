import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://halu.serv00.net/poli.php"
OUTPUT = "volleyballworld.json"

def parse_start(start_text):
    """Convert jadwal ke ISO 8601 (YYYY-MM-DDTHH:MM:SS) untuk JS"""
    start_text = start_text.strip()
    if "LIVE" in start_text.upper():
        # LIVE pakai waktu sekarang UTC
        return datetime.utcnow().isoformat()
    else:
        # Hapus nama hari dan zona jika ada
        for z in ["WIB", "WITA", "WIT"]:
            start_text = start_text.replace(z, "").strip()
        # Hapus nama hari (misal "Sel 16-09-2025 20:00" → "16-09-2025 20:00")
        if len(start_text.split()) > 1 and '-' in start_text.split()[0]:
            pass  # sudah format "16-09-2025 20:00"
        else:
            start_text = ' '.join(start_text.split()[1:])  # buang nama hari
        try:
            dt = datetime.strptime(start_text, "%d-%m-%Y %H:%M")
            return dt.isoformat()
        except ValueError:
            return start_text  # fallback

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

        # Judul
        title = img["alt"].strip() if img and img.has_attr("alt") else a.get_text(strip=True)

        # Link m3u8
        src = a["href"].strip() if a and a.has_attr("href") else ""
        if "/fM9jRrkN/" in src:
            src = src.replace("/fM9jRrkN/", "/fM9jRrkn/")

        # Poster
        poster = img["src"].strip() if img and img.has_attr("src") else ""
        if "width=320" in poster:
            poster = poster.replace("width=320", "width=1920")

        # Jadwal / LIVE
        start_text = small.get_text(strip=True) if small else ""
        start = parse_start(start_text)

        jadwal.append({
            "title": title,
            "start": start,
            "src": src,
            "poster": poster
        })

    # Simpan JSON → overwrite
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(jadwal, f, indent=2, ensure_ascii=False)

    print(f"[OK] {len(jadwal)} jadwal tersimpan ke {OUTPUT}")

if __name__ == "__main__":
    scrape()
