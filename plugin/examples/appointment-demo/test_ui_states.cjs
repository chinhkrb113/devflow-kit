const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.argv[2]||'http://127.0.0.1:8176/';
const out=path.join(__dirname,'evidence','ui-redesign');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true}),checks=[];
 const run=async(name,fn,mode='mock')=>{const page=await browser.newPage({viewport:{width:1440,height:900},locale:'vi-VN'}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  try{await page.goto(base+(mode==='mock'?'?mock=1':''));await page.getByLabel('Ngày hẹn',{exact:true}).fill('2030-11-04');await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();await fn(page);assert.deepEqual(errors,[]);checks.push({name,result:'pass'});}
  catch(e){checks.push({name,result:'fail',error:e.message});process.exitCode=1;}
  finally{await page.close();}
 };
 await run('switch-identity-clears-private-draft',async page=>{
  await page.getByLabel('Bạn muốn trao đổi điều gì?').fill('Ghi chú riêng của An');
  await page.getByLabel('Đang thử với').selectOption('binh');
  assert.equal(await page.locator('#note').inputValue(),'');
 });
 await run('empty-date-cannot-be-booked',async page=>{
  await page.getByLabel('Ngày hẹn',{exact:true}).fill('');
  await page.waitForTimeout(180);
  assert.equal(await page.locator('#slots button:not(:disabled)').count(),0);
  assert(await page.locator('#submit').isDisabled());
  assert.match(await page.locator('#message').innerText(),/ngày/i);
 });
 await run('reset-disabled-during-mutation',async page=>{
  await page.getByRole('button',{name:'09:00 còn trống',exact:true}).click();
  await page.getByLabel('Bạn muốn trao đổi điều gì?').fill('Đặt lịch đang gửi');
  assert(await page.evaluate(()=>{document.getElementById('submit').click();return document.getElementById('reset-mock').disabled;}));
 });
 await run('quick-date-summary-keyboard-and-inline-error',async page=>{
  await page.locator('#quick-dates button').nth(2).focus();await page.keyboard.press('Enter');
  assert(await page.locator('#quick-dates button').nth(2).evaluate(el=>el===document.activeElement),'Quick-date activation must retain keyboard focus');
  await page.getByRole('button',{name:'09:30 còn trống',exact:true}).waitFor();
  assert.equal(await page.locator('#quick-dates [aria-pressed=true]').count(),1);
  await page.getByRole('button',{name:'09:30 còn trống',exact:true}).focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#selection').innerText(),'09:30');
  const date=await page.locator('#date').inputValue();assert((await page.locator('#selection-date').innerText()).includes(date.split('-').reverse().join('/')));
  await page.locator('#submit').click();assert.equal(await page.locator('#note').getAttribute('aria-invalid'),'true');assert(await page.locator('#note').evaluate(el=>el===document.activeElement));
  await page.locator('#note').fill('Góp ý ý tưởng sản phẩm');assert.equal(await page.locator('#note').getAttribute('aria-invalid'),'false');
  assert.equal(await page.locator('#message').innerText(),'','Resolved field error must also clear its stale summary');
  assert.equal(await page.locator('#note-count').innerText(),'22/80');
  for(const width of [1440,768,390,320]){
   await page.setViewportSize({width,height:900});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Horizontal overflow at '+width);
   await page.screenshot({path:path.join(out,'mock-'+width+'.png'),fullPage:true});
  }
 });
 await run('all-slots-unavailable-and-recover',async page=>{
  await page.evaluate(()=>localStorage.setItem('so-hen-nho-prototype-v1',JSON.stringify(['09:00','09:30','10:00','10:30','14:00','14:30'].map((slot,i)=>({id:'full-'+i,owner:'binh',date:'2030-11-04',slot,note:'Lịch mẫu',status:'active'})))));
  await page.locator('#book-tab').click();await page.getByText('Ngày này không còn khung trống.',{exact:false}).waitFor();
  assert.equal(await page.locator('#availability').innerText(),'0/6 khung còn trống');assert(await page.locator('#submit').isDisabled());
  await page.getByLabel('Ngày hẹn',{exact:true}).fill('2030-11-05');await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();
 });
 await run('corrupt-mock-reset-recovery',async page=>{
  await page.evaluate(()=>localStorage.setItem('so-hen-nho-prototype-v1','invalid-json'));
  await page.locator('#book-tab').click();await page.getByRole('status').filter({hasText:'Dữ liệu mock không đọc được'}).waitFor();
  await page.locator('#reset-mock').click();await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();
 });
 await run('http-slot-error-retry-and-denied-list',async page=>{
  await page.route('**/api/slots?*',route=>route.abort());await page.getByLabel('Ngày hẹn',{exact:true}).fill('2030-11-05');
  await page.locator('#retry-slots').waitFor();assert(await page.locator('#submit').isDisabled());
  await page.unroute('**/api/slots?*');await page.locator('#retry-slots').click();await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();
  await page.route('**/api/bookings',route=>route.fulfill({status:403,contentType:'application/json',body:JSON.stringify({error:'Bạn không có quyền xem lịch này.'})}));
  await page.locator('#mine-tab').click();await page.getByRole('status').filter({hasText:'không có quyền'}).waitFor();assert.equal(await page.locator('.appointment').count(),0);
  await page.unroute('**/api/bookings');await page.locator('#refresh').click();await page.waitForFunction(()=>document.getElementById('bookings').getAttribute('aria-busy')==='false');
  assert.equal(await page.getByRole('status').innerText(),'');
 },'real');
 await browser.close();fs.writeFileSync(path.join(out,'ui-states.json'),JSON.stringify({executedAt:new Date().toISOString(),checks},null,2));console.log(JSON.stringify(checks,null,2));
})();
