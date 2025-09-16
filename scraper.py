import requests
from bs4 import BeautifulSoup
import json

URL = "https://halu.serv00.net/poli.php"
OUTPUT = "volleyballworld.json"

def scrape():
    res = requests.get(URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    matches = []
    cards = soup.select(".card")
    for card in cards:
        a = card.find("a")
        img = card.find("img")
        small = card.find("small")

        if not (a and img and small):
            continue

        src = a["href"].replace("/fM9jRrkN/", "/fM9jRrkn/")
        poster = img["src"].replace("width=320", "width=1920")
        title = img.get("alt", "").strip()
        start = small.get_text(strip=True)

        match = {
            "title": title,
            "start": start,
            "src": src,
            "poster": poster
        }
        matches.append(match)

    # Simpan JSON
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(matches)} jadwal tersimpan ke {OUTPUT}")

if __name__ == "__main__":
    scrape()
