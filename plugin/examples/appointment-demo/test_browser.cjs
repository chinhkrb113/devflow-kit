const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base=process.argv[2]||'http://127.0.0.1:8175/?mock=1';
const stage=process.argv[3]||'prototype';
const dir=path.join(__dirname,'evidence');fs.mkdirSync(dir,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:900},locale:'vi-VN'});
 const errors=[],checks=[];page.on('pageerror',e=>errors.push(e.message));
 const pass=name=>checks.push({name,result:'pass'});
 try{
  await page.goto(base);if(stage==='prototype'){await page.evaluate(()=>localStorage.clear());await page.reload();}
  await page.getByLabel('Ngày hẹn').fill('2030-11-04');await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();pass('AC-01: slots load');
  const tabInk=await page.locator('#book-tab').evaluate(el=>getComputedStyle(el).color);
  await page.locator('#book-tab').hover();assert.equal(await page.locator('#book-tab').evaluate(el=>getComputedStyle(el).color),tabInk);
  const contrast=await page.locator('#book-tab').evaluate(el=>{
    const rgb=s=>(s.match(/[\d.]+/g)||[]).slice(0,3).map(Number);
    const lum=c=>c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((a,x,i)=>a+x*[.2126,.7152,.0722][i],0);
    let bg='rgb(255,255,255)';for(let x=el;x;x=x.parentElement){const c=getComputedStyle(x).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent'){bg=c;break;}}
    const a=lum(rgb(getComputedStyle(el).color)),b=lum(rgb(bg));return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  });assert(contrast>=4.5);pass('AC-08: active tab hover contrast >= 4.5');
  await page.getByRole('button',{name:'09:00 còn trống',exact:true}).click();
  await page.getByRole('button',{name:'Xác nhận đặt lịch'}).click();await page.getByRole('status').filter({hasText:'Nhập nội dung'}).waitFor();pass('AC-04: blank input rejected');
  await page.getByLabel('Bạn muốn trao đổi điều gì?').fill('Thử luồng đặt lịch');
  await page.getByRole('button',{name:'Xác nhận đặt lịch'}).click();await page.getByText('Thử luồng đặt lịch',{exact:true}).waitFor();pass('AC-02: booking confirmation and list');
  const id=await page.locator('.appointment').first().getAttribute('data-id');
  await page.reload();await page.getByRole('button',{name:'Lịch của tôi',exact:true}).click();await page.getByText('Thử luồng đặt lịch',{exact:true}).waitFor();pass('AC-06: reload persistence');
  await page.getByLabel('Đang thử với').selectOption('binh');await page.getByText('Bạn chưa có lịch hẹn.',{exact:false}).waitFor();pass('AC-05: own list isolation');
  await page.getByRole('button',{name:'Đặt lịch',exact:true}).click();await page.getByLabel('Ngày hẹn').fill('2030-11-04');
  await page.getByRole('button',{name:'09:00 đã bận',exact:true}).waitFor();assert(await page.getByRole('button',{name:'09:00 đã bận',exact:true}).isDisabled());pass('AC-03: occupied slot disabled for other user');
  if(stage==='system'){
    const denied=await page.evaluate(async id=>{const r=await fetch('/api/bookings/'+id+'/cancel',{method:'POST',headers:{Authorization:'Bearer demo-binh','Content-Type':'application/json'},body:'{}'});return r.status;},id);assert.equal(denied,403);pass('AC-05: direct cross-owner mutation denied');
  }
  await page.getByLabel('Đang thử với').selectOption('an');await page.getByRole('button',{name:'Lịch của tôi',exact:true}).click();await page.getByRole('button',{name:'Hủy lịch',exact:true}).click();await page.getByText('Đã hủy',{exact:true}).waitFor();pass('AC-07: owner cancellation');
  await page.getByRole('button',{name:'Đặt lịch',exact:true}).click();await page.getByLabel('Ngày hẹn').fill('2030-11-04');await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();pass('AC-07: cancellation releases slot');
  await page.getByRole('button',{name:'09:30 còn trống',exact:true}).focus();await page.keyboard.press('Enter');assert((await page.locator('#selection').innerText()).startsWith('09:30'));pass('AC-08: keyboard selection');
  await page.screenshot({path:path.join(dir,stage+'-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:path.join(dir,stage+'-mobile.png'),fullPage:true});pass('AC-08: mobile no horizontal overflow');
  if(stage==='system'){
    await page.route('**/api/slots?*',route=>route.abort('failed'));await page.getByLabel('Ngày hẹn').fill('2030-11-05');await page.getByRole('status').filter({hasText:'Không kết nối được'}).waitFor();assert(await page.getByRole('button',{name:'Xác nhận đặt lịch'}).isDisabled());pass('AC-08: network failure shown and stale action disabled');
    await page.unroute('**/api/slots?*');await page.getByLabel('Ngày hẹn').fill('2030-11-04');await page.getByRole('button',{name:'09:00 còn trống',exact:true}).waitFor();pass('AC-08: recovery after network failure');
  }
  assert.deepEqual(errors,[]);pass('AC-08: no uncaught JavaScript errors');
 }catch(e){checks.push({name:'execution',result:'fail',error:e.stack});process.exitCode=1;await page.screenshot({path:path.join(dir,stage+'-failure.png'),fullPage:true}).catch(()=>{});}
 finally{fs.writeFileSync(path.join(dir,stage+'-browser.json'),JSON.stringify({base,stage,executedAt:new Date().toISOString(),checks,errors},null,2));await browser.close();console.log(JSON.stringify({stage,checks,errors},null,2));}
})();
