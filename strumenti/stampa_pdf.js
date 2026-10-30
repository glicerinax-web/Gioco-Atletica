// Converte le pagine di stampabili/html/ nei PDF di stampabili/.
// Uso:  node strumenti/stampa_pdf.js   (dopo python3 strumenti/genera_stampabili.py)
// Richiede Playwright con Chromium (npm install playwright && npx playwright install chromium).
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const radice = path.join(__dirname, '..');
const sorgenti = path.join(radice, 'stampabili', 'html');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const file of fs.readdirSync(sorgenti).filter((f) => f.endsWith('.html')).sort()) {
    await page.goto('file://' + path.join(sorgenti, file), { waitUntil: 'load' });
    await page.waitForFunction(() => window.__pronto === true);
    await page.evaluate(() => document.fonts.ready);
    const pieni = await page.$$eval('[data-troppo-pieno]', (els) => els.length);
    if (pieni) console.warn(`  attenzione: ${pieni} carte con testo che non entra in ${file}`);
    const pdf = path.join(radice, 'stampabili', file.replace(/\.html$/, '.pdf'));
    await page.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
    console.log('scritto', path.relative(radice, pdf));
  }
  await browser.close();
})();
