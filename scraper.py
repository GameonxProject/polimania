import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta, timezone

URL = "https://halu.serv00.net/poli.php"
OUTPUT = "volleyballworld.json"

# Map zona text dari sumber ke offset
ZONE_OFFSET = {
    "WIB": 7,
    "WITA": 8,
    "WIT": 9
}

def parse_start(start_text):
    """Convert jadwal ke ISO 8601 dengan offset sehingga JS bisa parse"""
    start_text = start_text.strip()
    if "LIVE" in start_text.upper():
        # LIVE pakai UTC sekarang
        return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    
    # Tentukan offset berdasarkan WIB/WITA/WIT
    tz_hours = 7  # default WIB
    for z, h in ZONE_OFFSET.items():
        if z in start_text:
            tz_hours = h
            start_text = start_text.replace(z, "").strip()
            break

    # Hapus nama hari (misal "Sel 16-09-2025 20:00" → "16-09-2025 20:00")
    parts = start_text.split()
    if len(parts) > 1 and '-' in parts[0]:
        date_str = start_text  # sudah benar
    else:
        date_str = ' '.join(parts[1:])

    try:
        dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
        tz = timezone(timedelta(hours=tz_hours))
        dt = dt.replace(tzinfo=tz)
        return dt.isoformat()
    except ValueError:
        # fallback jika parsing gagal
        return start_text

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
