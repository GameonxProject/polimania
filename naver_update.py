import requests
import json
from datetime import datetime, timedelta

# Endpoint API Naver
url = "https://api-gw.sports.naver.com/schedule/calendar"

# Ambil jadwal hari ini + besok
dates = [
    datetime.now().strftime("%Y-%m-%d"),
    (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
]

matches = []

for d in dates:
    params = {
        "superCategoryId": "volleyball",
        "categoryIds": "kovo,kwovo,volleyball,volleyballetc",
        "date": d
    }
    res = requests.get(url, params=params)
    data = res.json()

    for game in data.get("calendarGames", []):
        schedule = game.get("schedule", {})
        home = schedule.get("homeTeam", {}).get("name", "")
        away = schedule.get("awayTeam", {}).get("name", "")
        start = schedule.get("startTime", "")
        title = f"{home} vs {away}"

        # default kosong
        src = ""
        # ambil link live kalau ada
        onair = (
            schedule.get("relayUrl")
            or schedule.get("onAirPcUrl")
            or schedule.get("broadcastUrl")
        )
        if onair:
            src = onair

        matches.append({
            "title": title,
            "start": start,
            "src": src,
            "poster": "assets/logotvgonx.png"
        })

# Simpan ke naver.json (overwrite otomatis)
with open("naver.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

print("✅ naver.json diperbarui:", len(matches), "pertandingan (hari ini + besok)")
