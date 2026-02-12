const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
  });
  const page = await context.newPage();

  const pages = [
    { url: 'https://rayter.tw/', filename: 'homepage.png' },
    { url: 'https://rayter.tw/product-category/%e9%86%ab%e5%ad%b8%e7%be%8e%e5%ae%b9/', filename: 'cat-medical-aesthetics.png' },
    { url: 'https://rayter.tw/product-category/%e9%96%8b%e5%88%80%e6%88%bf/', filename: 'cat-operating-room.png' },
    { url: 'https://rayter.tw/about/', filename: 'about.png' },
    { url: 'https://rayter.tw/contact/', filename: 'contact.png' },
  ];

  const outputDir = '/Users/JoeyLiao/Joey-AI-Agent/rayter-backup/screenshots/mobile';

  for (const p of pages) {
    console.log(`Navigating to ${p.url}...`);
    await page.goto(p.url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    const filepath = `${outputDir}/${p.filename}`;
    await page.screenshot({ fullPage: true, path: filepath, type: 'png' });
    console.log(`Saved: ${filepath}`);
  }

  await browser.close();
  console.log('Done! All mobile screenshots saved.');
})();
