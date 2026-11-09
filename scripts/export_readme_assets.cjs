// Optional PNG export: PLAYWRIGHT_MODULE may point to an external installation.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const path = require('node:path');
const fs = require('node:fs');
const {pathToFileURL} = require('node:url');
(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage({deviceScaleFactor: 2, viewport: {width: 1328, height: 768}});
  const checks = [];
  try {
    for (const name of ['hero', 'architecture', 'workflow', 'portability']) {
      await page.setViewportSize({width:1328,height:768});
      await page.goto(pathToFileURL(path.join(root, 'docs/diagrams', name + '.html')).href, {waitUntil:'networkidle'});
      const size = await page.locator('svg').evaluate(svg => ({width: svg.viewBox.baseVal.width, height: svg.viewBox.baseVal.height}));
      const fonts = await page.evaluate(async () => {
        await Promise.all([document.fonts.load('40px "Instrument Serif"'),document.fonts.load('600 16px Geist'),document.fonts.load('12px "Geist Mono"')]);
        await document.fonts.ready;
        return [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family);
      });
      if (!['Instrument Serif','Geist','Geist Mono'].every(name=>fonts.some(f=>f.replaceAll('"','')===name))) throw new Error('Missing expected web fonts');
      const overflow = await page.locator('svg').evaluate(svg => [...svg.querySelectorAll('text')].filter(t => {
        const b=t.getBBox(); return b.x<0 || b.y<0 || b.x+b.width>svg.viewBox.baseVal.width || b.y+b.height>svg.viewBox.baseVal.height;
      }).map(t=>t.textContent));
      if (overflow.length) throw new Error(name+': text outside canvas: '+overflow.join(', '));
      await page.locator('svg').screenshot({path: path.join(root,'docs/assets',name+'.png')});
      await page.setViewportSize({width:390,height:844});
      const mobile = await page.evaluate(()=>({pageOverflow:document.documentElement.scrollWidth>390,localScroll:document.querySelector('.diagram-container').scrollWidth>document.querySelector('.diagram-container').clientWidth}));
      if (mobile.pageOverflow || !mobile.localScroll) throw new Error(name+': mobile scroll boundary failed');
      checks.push({asset:name, ...size, textOverflow:0, fonts:[...new Set(fonts)], mobile});
    }
    fs.mkdirSync(path.join(root,'.local'),{recursive:true});
    fs.writeFileSync(path.join(root,'.local/asset-render-check.json'),JSON.stringify(checks,null,2));
    console.log(JSON.stringify(checks));
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode=1;});
