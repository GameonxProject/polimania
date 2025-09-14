import requests
import json
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

# URL contoh jadwal voli di Naver Sports (ubah sesuai liga/event yang kamu mau)
NAVER_URL = "https://sports.news.naver.com/volleyball/schedule/index"

# File output JSON
OUTPUT_FILE = "naver.json"

def fetch_matches():
    """Ambil jadwal pertandingan dari Naver Sports"""
    resp = requests.get(NAVER_URL, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    matches = []
    now = datetime.now(timezone.utc)

    # Contoh scraping: cari elemen pertandingan (sesuaikan selector sesuai HTML Naver)
    for item in soup.select(".schedule_list li"):  # li = item pertandingan
        title = item.select_one(".team_area").get_text(strip=True) if item.select_one(".team_area") else "Match"
        time_str = item.select_one(".time").get_text(strip=True) if item.select_one(".time") else None

        if not time_str:
            continue

        # Parsing tanggal & waktu (Naver biasanya pakai format "09.15 14:30")
        try:
            today = datetime.now()
            dt = datetime.strptime(f"{today.year}.{time_str}", "%Y.%m.%d %H:%M")
            dt = dt.replace(tzinfo=timezone(timedelta(hours=9)))  # KST (UTC+9)
        except Exception as e:
            print("Gagal parsing waktu:", e)
            continue

        # Placeholder src & poster (kosong kalau belum live)
        src = ""  # nanti bisa diisi otomatis kalau sudah live
        poster = "https://gameonx.my.id/assets/logotvgonx.png"

        matches.append({
            "title": title,
            "start": dt.isoformat(),
            "src": src,
            "poster": poster
        })

    return matches

def save_json(matches):
    """Simpan data ke naver.json"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    print(f"✅ {OUTPUT_FILE} diperbarui: {len(matches)} pertandingan")

if __name__ == "__main__":
    try:
        matches = fetch_matches()
        save_json(matches)
    except Exception as e:
        print("❌ Error:", e)
