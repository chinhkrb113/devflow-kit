// HTTP response ordering fixtures; never write to the server database.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.argv[2]||'http://127.0.0.1:8176/';
(async()=>{
 const browser=await chromium.launch({headless:true}),checks=[];
 try{
  for(const stale of ['success','error']){
   const page=await browser.newPage();let reads=0,release,held,done;
   const gate=new Promise(r=>release=r),firstHeld=new Promise(r=>held=r),firstDone=new Promise(r=>done=r);
   const active={id:'race-fixture',date:'2030-11-04',slot:'09:00',note:'Kịch bản phản hồi trễ',status:'active'};
   await page.route('**/api/**',async route=>{
    const url=route.request().url(),method=route.request().method();
    const fulfill=(obj,status=200)=>route.fulfill({status,contentType:'application/json',body:JSON.stringify(obj)});
    if(url.includes('/slots'))return fulfill({date:'2030-11-04',slots:[{time:'09:00',available:true}]});
    if(method==='POST')return fulfill({booking:{...active,status:'cancelled'}});
    reads++;
    if(reads===1){held();await gate;await fulfill(stale==='success'?{bookings:[active]}:{error:'Phản hồi cũ bị lỗi'},stale==='success'?200:500);done();return;}
    return fulfill({bookings:[{...active,status:reads===2?'active':'cancelled'}]});
   });
   try{
    await page.goto(base);await page.getByRole('button',{name:'Lịch của tôi',exact:true}).click();await firstHeld;
    await page.getByRole('button',{name:'Lịch của tôi',exact:true}).click();await page.getByRole('button',{name:'Hủy lịch',exact:true}).click();
    await page.getByText('Đã hủy',{exact:true}).waitFor();release();await firstDone;
    // Allow the deliberately released old response to reach the renderer.
    await page.waitForTimeout(200);
    assert.equal(await page.getByText('Đã hủy',{exact:true}).count(),1,'Stale '+stale+' response overwrote current cancellation');
    assert.equal(await page.getByRole('button',{name:'Hủy lịch',exact:true}).count(),0);
    assert(!(await page.getByRole('status').innerText()).includes('Phản hồi cũ bị lỗi'));
    checks.push({name:'stale-'+stale+'-after-cancellation',result:'pass'});
   }catch(e){release();checks.push({name:'stale-'+stale+'-after-cancellation',result:'fail',error:e.message});process.exitCode=1;}
   finally{await page.close();}
  }
 }finally{await browser.close();fs.writeFileSync(path.join(__dirname,'evidence','race-browser.json'),JSON.stringify({executedAt:new Date().toISOString(),transport:'intercepted synthetic HTTP responses',checks},null,2));console.log(JSON.stringify(checks,null,2));}
})();
