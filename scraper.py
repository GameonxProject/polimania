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

        # Title ambil dari alt atau text <a>
        title = img["alt"].strip() if img and img.has_attr("alt") else a.get_text(strip=True)

        # Link m3u8
        src = a["href"].strip() if a and a.has_attr("href") else ""

        # Poster
        poster = img["src"].strip() if img and img.has_attr("src") else ""

        # Jadwal atau status LIVE
        start_text = small.get_text(strip=True) if small else ""
        if "LIVE" in start_text.upper():
            start = datetime.utcnow().isoformat()  # kalau LIVE pakai waktu sekarang
        else:
            start = start_text

        # 🔧 Perbaikan otomatis
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

    # Simpan JSON baru → overwrite (biar kalau sumber hapus, JSON juga ikut hapus)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(jadwal, f, indent=2, ensure_ascii=False)

    print(f"[OK] {len(jadwal)} jadwal tersimpan ke {OUTPUT}")

if __name__ == "__main__":
    scrape()
