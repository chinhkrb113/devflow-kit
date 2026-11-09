const $ = id => document.getElementById(id);
const mock = new URLSearchParams(location.search).get('mock') === '1';
const times = ['09:00','09:30','10:00','10:30','14:00','14:30'];
const state = {user:'an',selected:null,view:'book',busy:false,generation:0,listGeneration:0};
const today = () => new Date(Date.now()+7*3600000).toISOString().slice(0,10);
const tomorrow = new Date(Date.now()+7*3600000+86400000).toISOString().slice(0,10);
const mockKey = 'so-hen-nho-prototype-v1';
const displayDate = date => date.split('-').reverse().join('/');
function validDate(date){
  if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||date<today())return false;
  const d=new Date(date+'T12:00:00Z');
  return !Number.isNaN(d.getTime())&&d.toISOString().slice(0,10)===date;
}
function message(text='',error=false){$('message').textContent=text;$('message').classList.toggle('error',error);}
function noteError(text=''){$('note-error').textContent=text;$('note-error').hidden=!text;$('note').setAttribute('aria-invalid',String(Boolean(text)));}
function noteChanged(){const previousError=$('note-error').textContent;$('note-count').textContent=$('note').value.length+'/80';noteError();if(previousError&&$('message').textContent===previousError)message();}
function clearDraft(){$('note').value='';noteChanged();state.selected=null;selection();}
function isPast(date,time){return new Date(`${date}T${time}:00+07:00`).getTime()<=Date.now();}
async function request(path,body){
  const user=state.user;
  if(mock){
    await new Promise(resolve=>setTimeout(resolve,100));
    let rows;
    try{rows=JSON.parse(localStorage.getItem(mockKey)||'[]');if(!Array.isArray(rows)||rows.some(r=>!r||typeof r.id!=='string'||typeof r.date!=='string'||typeof r.note!=='string'))throw Error();}
    catch{throw Error('Dữ liệu mock không đọc được. Chọn Xóa dữ liệu mock để bắt đầu lại.');}
    if(path.startsWith('/slots')){
      const date=new URLSearchParams(path.split('?')[1]).get('date');
      if(!validDate(date))throw Error('Chọn ngày hợp lệ từ hôm nay trở đi.');
      return {date,slots:times.map(time=>({time,available:!isPast(date,time)&&!rows.some(r=>r.date===date&&r.slot===time&&r.status==='active')}))};
    }
    if(path==='/bookings'&&!body)return {bookings:rows.filter(r=>r.owner===user)};
    if(path==='/bookings'){
      const note=body.note.trim();
      if(!validDate(body.date)||!note||note.length>80||!times.includes(body.slot)||isPast(body.date,body.slot))throw Error('Thông tin lịch hẹn chưa hợp lệ.');
      if(rows.some(r=>r.date===body.date&&r.slot===body.slot&&r.status==='active'))throw Error('Khung giờ vừa được đặt. Hãy chọn giờ khác.');
      const booking={id:crypto.randomUUID(),owner:user,...body,note,status:'active'};rows.push(booking);localStorage.setItem(mockKey,JSON.stringify(rows));return {booking};
    }
    const row=rows.find(r=>r.id===path.split('/')[2]);
    if(!row||row.owner!==user)throw Error('Bạn không có quyền hủy lịch này.');
    row.status='cancelled';localStorage.setItem(mockKey,JSON.stringify(rows));return {booking:row};
  }
  let response;
  try{response=await fetch('/api'+path,{method:body?'POST':'GET',headers:{Authorization:'Bearer demo-'+user,...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})});}
  catch{throw Error('Không kết nối được. Kiểm tra server rồi thử lại.');}
  let data;try{data=await response.json();}catch{throw Error('Phản hồi chưa đọc được. Hãy thử lại.');}
  if(!response.ok)throw Error(data.error||'Không xử lý được yêu cầu.');return data;
}
function lock(busy){
  state.busy=busy;
  for(const id of ['identity','date','note','refresh','reset-mock','book-tab','mine-tab','retry-slots'])$(id).disabled=busy;
  for(const b of $('quick-dates').children)b.disabled=busy;
  for(const b of $('slots').querySelectorAll('button'))b.disabled=busy||b.dataset.available!=='true';
  for(const b of $('bookings').querySelectorAll('button'))b.disabled=busy;
  $('submit').textContent=busy?'Đang xử lý…':'Xác nhận đặt lịch';
  $('booking-form').setAttribute('aria-busy',String(busy));selection();
}
function selection(){
  $('selection').textContent=state.selected||'Chưa chọn khung giờ';
  $('selection-date').textContent=state.selected?displayDate($('date').value)+' / UTC+07:00':'Chọn một giờ còn trống để tiếp tục.';
  $('submit').disabled=state.busy||!state.selected||!validDate($('date').value);
}
function renderDates(){
  const focusedDate=$('quick-dates').contains(document.activeElement)?document.activeElement.dataset.date:null;
  $('quick-dates').replaceChildren();
  for(let i=0;i<7;i++){
    const d=new Date(today()+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+i);const date=d.toISOString().slice(0,10);
    const b=document.createElement('button');b.type='button';b.className='day';b.dataset.date=date;b.classList.toggle('selected',date===$('date').value);b.setAttribute('aria-pressed',String(date===$('date').value));b.setAttribute('aria-label','Chọn ngày '+displayDate(date)+(i===0?', hôm nay':''));b.disabled=state.busy;
    const weekday=document.createElement('span'),number=document.createElement('strong');weekday.textContent=['CN','Th 2','Th 3','Th 4','Th 5','Th 6','Th 7'][d.getUTCDay()];number.textContent=d.getUTCDate();b.append(weekday,number);
    b.onclick=()=>{if(state.busy)return;$('date').value=date;message();refreshSlots();};$('quick-dates').append(b);
  }
  if(focusedDate){const target=Array.from($('quick-dates').children).find(b=>b.dataset.date===focusedDate);if(target)target.focus({preventScroll:true});}
}
async function refreshSlots(){
  const generation=++state.generation;state.selected=null;selection();renderDates();$('availability').textContent='';$('retry-slots').hidden=true;$('date').min=today();
  if(!validDate($('date').value)){$('slots').replaceChildren();$('slots').setAttribute('aria-busy','false');message('Chọn ngày hợp lệ từ hôm nay trở đi.',true);return;}
  $('slots').setAttribute('aria-busy','true');$('slots').textContent='Đang tải khung giờ…';
  try{
    const data=await request('/slots?date='+encodeURIComponent($('date').value));if(generation!==state.generation)return;
    $('slots').replaceChildren();const available=data.slots.filter(s=>s.available).length;$('availability').textContent=available+'/'+data.slots.length+' khung còn trống';
    for(const slot of data.slots){
      const b=document.createElement('button');b.type='button';b.className='slot';b.dataset.available=String(slot.available);b.disabled=state.busy||!slot.available;b.setAttribute('aria-label',slot.time+(slot.available?' còn trống':' đã bận'));b.setAttribute('aria-pressed','false');
      const time=document.createElement('span'),caption=document.createElement('span');time.className='slot-time';time.textContent=slot.time;caption.className='slot-state';caption.textContent=slot.available?'Còn trống':'Không khả dụng';b.append(time,caption);
      b.onclick=()=>{if(state.busy)return;state.selected=slot.time;for(const x of $('slots').querySelectorAll('button')){x.classList.remove('active');x.setAttribute('aria-pressed','false');x.querySelector('.slot-state').textContent=x.dataset.available==='true'?'Còn trống':'Không khả dụng';}b.classList.add('active');b.setAttribute('aria-pressed','true');caption.textContent='Đã chọn';selection();message();};$('slots').append(b);
    }
    if(!available){const p=document.createElement('p');p.className='slot-empty';p.textContent='Ngày này không còn khung trống. Hãy chọn ngày khác.';$('slots').append(p);}
  }catch(e){if(generation!==state.generation)return;$('slots').textContent='Chưa tải được khung giờ.';$('retry-slots').hidden=false;message(e.message,true);}
  finally{if(generation===state.generation)$('slots').setAttribute('aria-busy','false');}
}
async function refreshBookings(){
  const user=state.user,generation=++state.listGeneration;$('bookings').textContent='Đang tải lịch…';$('bookings').setAttribute('aria-busy','true');$('mine-description').textContent='Các cuộc hẹn của '+(user==='an'?'An':'Bình')+'.';
  try{
    const data=await request('/bookings');if(user!==state.user||generation!==state.listGeneration)return;$('bookings').replaceChildren();
    if(!data.bookings.length){
      const box=document.createElement('div'),h=document.createElement('h2'),p=document.createElement('p'),b=document.createElement('button');box.className='empty';h.textContent='Bạn chưa có lịch hẹn.';p.textContent='Một cuộc trao đổi bắt đầu từ khoảng thời gian phù hợp.';b.textContent='Chọn giờ đặt lịch';b.onclick=async()=>{await view('book');$('date').focus();};box.append(h,p,b);$('bookings').append(box);
    }
    for(const row of data.bookings){
      const card=document.createElement('article');card.className='appointment'+(row.status==='cancelled'?' cancelled':'');card.dataset.id=row.id;
      const stamp=document.createElement('div'),day=document.createElement('strong'),month=document.createElement('span');stamp.className='appointment-date';stamp.setAttribute('aria-hidden','true');day.textContent=row.date.slice(8);month.textContent='Tháng '+Number(row.date.slice(5,7));stamp.append(day,month);
      const info=document.createElement('div'),h=document.createElement('h3'),p=document.createElement('p'),s=document.createElement('small');info.className='appointment-info';h.textContent=`${row.slot} / ${displayDate(row.date)}`;p.textContent=row.note;s.textContent=row.status==='active'?'Đã đặt · 30 phút':'Đã hủy';info.append(h,p,s);card.append(stamp,info);
      if(row.status==='active'){
        const b=document.createElement('button');b.textContent='Hủy lịch';b.className='cancel-button';b.disabled=state.busy;
        b.onclick=async()=>{if(state.busy)return;lock(true);try{await request('/bookings/'+row.id+'/cancel',{});message('Đã hủy lịch. Khung giờ đã được mở lại.');await refreshBookings();$('mine-heading').focus();}catch(e){message(e.message,true);}finally{lock(false);}};card.append(b);
      }
      $('bookings').append(card);
    }
  }catch(e){if(user!==state.user||generation!==state.listGeneration)return;$('bookings').textContent='Chưa tải được danh sách. Dùng Tải lại danh sách để thử lại.';message(e.message,true);}
  finally{if(user===state.user&&generation===state.listGeneration)$('bookings').setAttribute('aria-busy','false');}
}
async function view(name){
  state.view=name;if(name!=='mine')state.listGeneration++;else state.generation++;
  $('book-view').hidden=name!=='book';$('mine-view').hidden=name!=='mine';
  for(const n of ['book','mine']){$(n+'-tab').classList.toggle('selected',n===name);$(n+'-tab').setAttribute('aria-pressed',String(n===name));}
  if(name==='book')await refreshSlots();else await refreshBookings();
}
$('book-tab').onclick=()=>{if(!state.busy){message();view('book');}};
$('mine-tab').onclick=()=>{if(!state.busy){message();view('mine');}};
$('refresh').onclick=()=>{message();refreshBookings();};
$('retry-slots').onclick=()=>{message();refreshSlots();};
$('identity').onchange=()=>{state.user=$('identity').value;clearDraft();$('bookings').replaceChildren();message();view(state.view);};
$('date').min=today();$('date').value=tomorrow;$('date').onchange=()=>{message();refreshSlots();};
$('note').oninput=noteChanged;
$('booking-form').onsubmit=async event=>{
  event.preventDefault();if(state.busy)return;const note=$('note').value.trim();
  if(!note){const text='Nhập nội dung cuộc hẹn trước khi đặt.';noteError(text);message(text,true);$('note').focus();return;}
  if(note.length>80){noteError('Nội dung tối đa 80 ký tự.');$('note').focus();return;}
  if(!validDate($('date').value)){message('Chọn ngày hợp lệ từ hôm nay trở đi.',true);$('date').focus();return;}
  if(!state.selected){message('Chọn một khung giờ còn trống.',true);return;}
  const body={date:$('date').value,slot:state.selected,note};lock(true);message('Đang lưu lịch…');
  try{await request('/bookings',body);clearDraft();message('Đã đặt lịch. Bạn có thể xem hoặc hủy bên dưới.');await view('mine');$('mine-heading').focus();}
  catch(e){message(e.message,true);await refreshSlots();}
  finally{lock(false);}
};
if(mock){
  $('mode').textContent='Mock tương tác · Dữ liệu mẫu trong trình duyệt';$('reset-mock').hidden=false;
  $('reset-mock').onclick=()=>{if(state.busy)return;try{localStorage.removeItem(mockKey);clearDraft();message('Đã xóa dữ liệu mock.');view(state.view);}catch{message('Không thể xóa dữ liệu mock trong trình duyệt này.',true);}};
}
refreshSlots();
