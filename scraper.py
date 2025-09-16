import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://halu.serv00.net/poli.php"
OUTPUT = "volleyballworld.json"

def scrape():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    data = []
    for item in soup.find_all("div", class_="match-item"):  # sesuaikan dengan struktur asli
        title = item.find("h3").get_text(strip=True)
        start = item.get("data-start")  # atau ambil dari span/judul
        src = item.find("iframe")["src"] if item.find("iframe") else ""
        poster = item.find("img")["src"] if item.find("img") else "assets/logotvgonx.png"

        # fix url otomatis
        if "/fM9jRrkN/" in src:
            src = src.replace("/fM9jRrkN/", "/fM9jRrkn/")
        if "width=320" in src:
            src = src.replace("width=320", "width=1920")

        data.append({
            "title": title,
            "start": start,
            "src": src,
            "poster": poster
        })

    # sort by start time
    try:
        data.sort(key=lambda x: datetime.fromisoformat(x["start"]))
    except:
        pass

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape()
