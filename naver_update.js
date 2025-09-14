const fs = require("fs");
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const page = await browser.newPage();
  await page.goto("https://sports.news.naver.com/volleyball/schedule/index", {
    waitUntil: "networkidle2",
  });

  const matches = await page.evaluate(() => {
    const rows = document.querySelectorAll(".sch_tb tbody tr");
    const data = [];
    rows.forEach((row) => {
      const teams = row.querySelectorAll("span.team");
      const timeEl = row.querySelector("span.time");
      if (teams.length === 2 && timeEl) {
        const home = teams[0].innerText.trim();
        const away = teams[1].innerText.trim();
        const timeStr = timeEl.innerText.trim();

        data.push({
          title: `${home} vs ${away}`,
          start: new Date().toISOString(), // TODO: parse timeStr ke ISO
          src: "",
          poster: "assets/logotvgonx.png",
        });
      }
    });
    return data;
  });

  await browser.close();
  fs.writeFileSync("naver.json", JSON.stringify(matches, null, 2), "utf-8");
  console.log(`✅ naver.json diperbarui: ${matches.length} pertandingan`);
})();
