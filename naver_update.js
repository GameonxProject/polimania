// naver_update.js
import fs from "fs";
import puppeteer from "puppeteer";

async function scrapeNaver() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  // URL jadwal voli di Naver Sports (contoh, bisa kamu sesuaikan)
  const url = "https://sports.naver.com/volleyball/schedule/index";

  await page.goto(url, { waitUntil: "networkidle2" });

  // Ambil elemen pertandingan
  const matches = await page.evaluate(() => {
    const items = [];
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);

    function formatDate(d) {
      return d.toISOString().split("T")[0]; // YYYY-MM-DD
    }

    const validDates = [formatDate(today), formatDate(tomorrow)];

    document.querySelectorAll(".sch_tb tbody tr").forEach((row) => {
      const dateCell = row.closest("table").querySelector("caption")?.innerText;
      if (!dateCell) return;

      // Contoh caption di Naver: "2025.09.15 (월)"
      const dateMatch = dateCell.match(/(\d{4})\.(\d{2})\.(\d{2})/);
      if (!dateMatch) return;

      const matchDate = `${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}`;
      if (!validDates.includes(matchDate)) return;

      const time = row.querySelector(".time")?.innerText.trim();
      const teams = row.querySelector(".team")?.innerText.trim();
      const title = teams || "Pertandingan Voli";

      let startISO = "";
      if (time) {
        const [hh, mm] = time.split(":");
        const dt = new Date(`${matchDate}T${hh}:${mm}:00+09:00`); // KST (UTC+9)
        startISO = dt.toISOString();
      }

      items.push({
        title,
        start: startISO,
        src: "",
        poster: "assets/logotvgonx.png",
      });
    });

    return items;
  });

  await browser.close();

  // Simpan ke naver.json
  fs.writeFileSync("naver.json", JSON.stringify(matches, null, 2), "utf-8");

  console.log(`✅ naver.json diperbarui: ${matches.length} pertandingan`);
}

scrapeNaver().catch((err) => {
  console.error("❌ Error scraping:", err);
  process.exit(1);
});
