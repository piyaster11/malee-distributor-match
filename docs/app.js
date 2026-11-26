'use strict';
let D,L=localStorage.getItem('mdm_lang')||'en';
const T={
en:{},
th:{kicker:'มาลี กรุ๊ป · เครื่องมือฝ่ายขายต่างประเทศ · v1',title:'จับคู่ผู้จัดจำหน่าย: ใครต้องการมาลี และที่ไหน',sub:'Push = ตลาดไหนเหมาะกับพอร์ตสินค้ามาลี (ข้อมูลการค้า) · Pull = ผู้นำเข้า/ผู้จัดจำหน่ายจริงรายไหนต้องการสินค้าแบบมาลี (หลักฐานสาธารณะ + ผู้ซื้อที่ประกาศเอง) ทุกบริษัทมีลิงก์แหล่งที่มา',
nLeads:'🔥 ลีดร้อน',nMarkets:'ตลาด (push)',nMatch:'จับคู่ผู้จัดจำหน่าย (pull)',nTrip:'วางแผนทริป',nAdd:'เพิ่มผู้จัดจำหน่าย',nMethod:'วิธีให้คะแนน',
leadsH:'🔥 ลีดร้อน — ผู้ซื้อที่บอกเองว่าต้องการ',leadsL:'โพสต์สาธารณะที่ผู้นำเข้า/ผู้จัดจำหน่ายขอสินค้าแบบมาลี หรือเปิดรับแบรนด์พาร์ทเนอร์ใหม่ ข้อมูลระดับบริษัทเท่านั้น ติดต่อผ่านแพลตฟอร์มต้นทาง ไม่มีการแต่งข้อมูล ประเทศไหนมีน้อยคือจำนวนจริง',
csv:'ส่งออก CSV',thDate:'วันที่',thCountry:'ประเทศ',thType:'ประเภท',thSaid:'สิ่งที่เขาบอก',thLead:'สินค้าที่ควรเสนอ',thSrc:'แหล่งที่มา',
mktH:'ตลาด — คะแนน push',mktL:'มูลค่านำเข้าจาก UN Comtrade: HS 2009 (น้ำผลไม้), 2202 (เครื่องดื่มไม่มีแอลกอฮอล์อื่น ๆ รวมเครื่องดื่มชูกำลัง จึงสูงกว่าตลาดเนคต้าจริง) และ 2008 (ผลไม้แปรรูป/กระป๋อง) ปีล่าสุดที่รายงาน เทียบการเติบโตกับปี 2021',
matchH:'จับคู่ผู้จัดจำหน่าย — pull × push',matchL:'คะแนนความต้องการเป็นการประเมินโดย AI จากหลักฐานสาธารณะที่แสดงเท่านั้น "ไม่ทราบ" คือแหล่งข้อมูลไม่ได้ระบุ ไม่ใช่ "ไม่มี"',onlyWarm:'เฉพาะที่มีสัญญาณผู้ซื้อ/หาพาร์ทเนอร์',
tripH:'วางแผนทริป',tripL:'เลือกประเทศที่จะไป: 10 ผู้จัดจำหน่ายที่ควรนัดพบ พร้อมลีดร้อนของประเทศนั้น พิมพ์หรือบันทึกเป็น PDF ได้',print:'พิมพ์ / PDF',
addH:'เพิ่มผู้จัดจำหน่ายที่ได้พบ',addL:'บันทึกไว้ในเบราว์เซอร์นี้เท่านั้น (localStorage) ให้คะแนนแบบเดียวกัน และแสดงในรายการจับคู่และแผนทริป',fName:'ชื่อบริษัท *',fCountry:'ประเทศ *',fUrl:'เว็บไซต์ / ลิงก์แหล่งที่มา',fNote:'บันทึก (สิ่งที่เขาพูด)',cJ:'ขายน้ำผลไม้/เครื่องดื่ม',cC:'มีน้ำมะพร้าว',cA:'มีชั้นสินค้าเอเชีย/ไทย',cO:'อยากได้แบรนด์ใหม่',cW:'บอกว่าต้องการสินค้าแบบมาลี',save:'บันทึกและให้คะแนน',methH:'วิธีให้คะแนน'}};
const W={en:{all:'All',allC:'All countries',allT:'All signal types',allP:'All Malee products',allF:'Any freshness',other:'Other countries',product:'Product request',partner:'Partner seeking',oem:'OEM / private label',otherT:'Other',fresh:'Fresh ≤90d',recent:'≤12 months',stale:'Stale >12m',standing:'Standing page (undated)',coco:'Malee Coco 100% coconut water',juice:'Malee 100% juice / nectar',canned:'Malee canned fruit',dairy:'Malee UHT dairy',oemP:'OEM / private label',nameHidden:'Name hidden by platform',signals:'signals',total:'Total signals',fit:'Market fit',need:'Need (AI)',match:'Match',unknown:'unknown',seen:'seen',notseen:'not seen',why:'Why this match',pitch:'Pitch / lead SKUs',evidence:'Evidence',source:'Source',warm:'🔥 Expressed signal',cat:'Any category',ch:'Any channel',imports:'Imports (juice+drinks+prep. fruit)',growth:'Growth vs 2021',thai:'Thailand share',access:'Trade access',halal:'Halal-majority market: lead with halal-certified SKUs',dists:'distributors',top10:'Top distributors to meet',leadsFor:'Warm leads in this country',none:'None found yet — honest count.',del:'Remove',yours:'Added by you',unkList:'Unknown from source',fitH:'Fit',noLeads:'No real public signals found for this filter.'},
th:{all:'ทั้งหมด',allC:'ทุกประเทศ',allT:'ทุกประเภทสัญญาณ',allP:'สินค้ามาลีทั้งหมด',allF:'ทุกช่วงเวลา',other:'ประเทศอื่น ๆ',product:'ขอซื้อสินค้า',partner:'หาพาร์ทเนอร์',oem:'OEM / แบรนด์ลูกค้า',otherT:'อื่น ๆ',fresh:'ใหม่ ≤90 วัน',recent:'≤12 เดือน',stale:'เก่า >12 เดือน',standing:'หน้าเว็บประจำ (ไม่มีวันที่)',coco:'มาลี โคโค่ น้ำมะพร้าว 100%',juice:'น้ำผลไม้ 100% / เนคต้า มาลี',canned:'ผลไม้กระป๋องมาลี',dairy:'นม UHT มาลี',oemP:'OEM / แบรนด์ลูกค้า',nameHidden:'แพลตฟอร์มซ่อนชื่อ',signals:'สัญญาณ',total:'สัญญาณทั้งหมด',fit:'ความเหมาะของตลาด',need:'ความต้องการ (AI)',match:'คะแนนจับคู่',unknown:'ไม่ทราบ',seen:'พบ',notseen:'ไม่พบ',why:'ทำไมจับคู่นี้',pitch:'แนวทางเสนอขาย / SKU นำ',evidence:'หลักฐาน (ภาษาต้นฉบับ)',source:'แหล่งที่มา',warm:'🔥 มีสัญญาณชัดเจน',cat:'ทุกหมวดสินค้า',ch:'ทุกช่องทาง',imports:'มูลค่านำเข้า (น้ำผลไม้+เครื่องดื่ม+ผลไม้แปรรูป)',growth:'เติบโตเทียบปี 2021',thai:'ส่วนแบ่งไทย',access:'สิทธิทางการค้า',halal:'ตลาดมุสลิม: นำด้วย SKU ที่มีฮาลาล',dists:'ผู้จัดจำหน่าย',top10:'ผู้จัดจำหน่ายที่ควรนัดพบ',leadsFor:'ลีดร้อนในประเทศนี้',none:'ยังไม่พบ — นับตามจริง',del:'ลบ',yours:'คุณเพิ่มเอง',unkList:'แหล่งข้อมูลไม่ระบุ',fitH:'ความเหมาะ',noLeads:'ไม่พบสัญญาณสาธารณะจริงสำหรับตัวกรองนี้'}};
const w=k=>(W[L]&&W[L][k])||W.en[k]||k;
const CN={PK:['Pakistan','ปากีสถาน'],VN:['Vietnam','เวียดนาม'],MV:['Maldives','มัลดีฟส์']};
const cname=c=>D.markets[c]?(L==='th'?D.markets[c].name_th:D.markets[c].name):(CN[c]?CN[c][L==='th'?1:0]:c);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const pname=p=>w(p==='oem'?'oemP':p);
const typeKey=t=>t==='other'?'otherT':t;
function applyI18n(){document.documentElement.lang=L;document.querySelectorAll('[data-i]').forEach(e=>{const k=e.dataset.i;if(!e.dataset.en)e.dataset.en=e.innerHTML;e.innerHTML=L==='th'&&T.th[k]?T.th[k]:e.dataset.en});document.getElementById('lenBtn').classList.toggle('on',L==='en');document.getElementById('lthBtn').classList.toggle('on',L==='th')}
// ---------- scoring ----------
function need(d){const f=d.f||{};let s=0,why=[],unk=[];
 if(f.j===true){s+=25;why.push(L==='th'?'ขายน้ำผลไม้/เครื่องดื่มอยู่แล้ว':'Already sells juice/drinks')} else if(f.j==null) unk.push(L==='th'?'หมวดเครื่องดื่ม':'drinks range');
 if(f.a===true){s+=15;why.push(L==='th'?'มีชั้นสินค้าเอเชีย/ไทย — แหล่งผลิตไทยเป็นจุดขาย':'Asian/Thai shelf — Thai origin is a selling point')} else if(f.a==null) unk.push(L==='th'?'ชั้นสินค้าเอเชีย':'Asian shelf');
 const br=(d.brands||[]).join(', ');
 if(f.j===true&&f.c===false){s+=15;why.push(L==='th'?'ไม่พบน้ำมะพร้าวในรายการ — ช่องว่างที่มาลี โคโค่เติมได้':'No coconut water seen — a gap Malee Coco can fill')}
 else if(f.c===true){s+=br?8:10;why.push(L==='th'?('หมวดน้ำมะพร้าวพิสูจน์แล้ว'+(br?' (มีคู่แข่ง: '+br+') — เสนอเป็นแบรนด์ที่สอง':'')):('Coconut water already proven here'+(br?' (competitor: '+br+') — pitch as second brand':'')))}
 else if(f.c==null) unk.push(L==='th'?'น้ำมะพร้าว':'coconut water');
 if(f.o===true){s+=20;why.push(L==='th'?'ประกาศเปิดรับแบรนด์/ซัพพลายเออร์ใหม่':'Publicly invites new brands/suppliers')}
 if(f.k===true){s+=5;why.push(L==='th'?'มีหมวดผลไม้กระป๋อง':'Carries canned fruit')}
 const ch=(d.channels||[]).length;s+=Math.min(ch*5,15);
 if((d.signals||[]).length||d.w){s+=10;why.push(L==='th'?'มีสัญญาณผู้ซื้อ/หาพาร์ทเนอร์ชัดเจน':'Has an expressed buyer/partner signal')}
 return {s:Math.min(100,s),why,unk}}
function fit(c){return D.markets[c]?D.markets[c].fit:null}
function match(d){const n=need(d).s,f=fit(d.country);return f==null?null:Math.round(Math.sqrt(n*f))}
function pitch(d){const f=d.f||{},p=[];const th=L==='th';
 if(f.c===false||f.c==null)p.push(th?'มาลี โคโค่ น้ำมะพร้าว 100% (330 มล./1 ลิตร UHT ไม่เติมน้ำตาล)':'Malee Coco 100% coconut water (330 ml / 1 L UHT, no sugar added)');
 if(f.c===true)p.push(th?'มาลี โคโค่ เป็นแบรนด์ที่สอง — เน้นราคา/แพ็ก/แหล่งผลิตไทย':'Malee Coco as a second brand — compete on price, pack and Thai origin');
 if(f.a===true)p.push(th?'น้ำผลไม้ 100% และเนคต้ารสเขตร้อน (มะม่วง ฝรั่ง ลิ้นจี่ สับปะรด)':'100% juices & tropical nectars (mango, guava, lychee, pineapple)');
 else if(f.j===true)p.push(th?'น้ำผลไม้ 100% มาลี 1 ลิตร สำหรับโมเดิร์นเทรด':'Malee 100% juice 1 L for modern trade');
 if(f.k===true||(d.channels||[]).includes('HoReCa'))p.push(th?'ผลไม้กระป๋อง/ฟรุตค็อกเทล และแพ็ก 1 ลิตรสำหรับ HoReCa':'Canned fruit/fruit cocktail and 1 L packs for HoReCa');
 if(f.o===true)p.push(th?'ติดต่อผ่านหน้า "หาแบรนด์/ซัพพลายเออร์" ของเขาโดยตรง':'Approach through their brand/supplier partner page');
 if(D.markets[d.country]&&D.markets[d.country].halal)p.push(w('halal'));
 return p}
// ---------- leads ----------
function opt(sel,arr,val){sel.innerHTML=arr.map(([v,t])=>`<option value="${v}">${esc(t)}</option>`).join('');if(val!=null)sel.value=val}
const ST={lc:'',lt:'',lp:'',lf:'',mc:'',mcat:'',mch:'',tc:'PH'};
function leadsFiltered(){return D.signals.filter(s=>(!ST.lc||(ST.lc==='OTHER'?!D.markets[s.country]:s.country===ST.lc))&&(!ST.lt||s.type===ST.lt)&&(!ST.lp||s.prods.includes(ST.lp))&&(!ST.lf||s.fresh===ST.lf)).sort((a,b)=>(b.fit-a.fit)||((a.age??400)-(b.age??400)))}
function leadRow(s){const co=s.company?esc(s.company):`<span class="muted">${w('nameHidden')}</span>`;
 return `<tr><td>${s.date||'—'}<br><span class="tag f-${s.fresh}">${w(s.fresh)}</span></td><td>${esc(cname(s.country))}</td><td><span class="tag t-${s.type}">${w(typeKey(s.type))}</span><br><span class="small fit${s.fit}">${w('fitH')} ${'●'.repeat(s.fit)}${'○'.repeat(3-s.fit)}</span></td><td><b>${co}</b><br>${esc(s.said)}</td><td>${s.prods.map(p=>`<span class="tag">${esc(pname(p))}</span>`).join('')}</td><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.src)}</a></td></tr>`}
function renderLeads(){const all=D.signals;const by=t=>all.filter(s=>s.type===t).length;
 document.getElementById('leadKpis').innerHTML=[[w('total'),all.length],[w('product'),by('product')],[w('partner'),by('partner')],[w('oem'),by('oem')],[w('fresh'),all.filter(s=>s.fresh==='fresh').length]].map(([l,v])=>`<div class="kpi"><div class="l">${l}</div><div class="v">${v}</div></div>`).join('')+
 `<div class="kpi" style="grid-column:1/-1"><div class="l">${w('signals')} / ${L==='th'?'ประเทศ':'country'}</div><div class="small">${Object.keys(D.markets).concat(['PK','VN','MV']).map(c=>`${esc(cname(c))}: <b>${all.filter(s=>s.country===c).length}</b>`).join(' · ')}</div></div>`;
 const r=leadsFiltered();document.getElementById('leadRows').innerHTML=r.length?r.map(leadRow).join(''):`<tr><td colspan="6" class="muted">${w('noLeads')}</td></tr>`;
 document.getElementById('leadNote').textContent=L==='th'?`แสดง ${r.length} รายการ เรียงตามความเหมาะแล้วตามความใหม่ บอร์ด B2B มักซ่อนชื่อผู้ซื้อ — ติดต่อผ่านแพลตฟอร์ม และตรวจว่าประกาศยังเปิดอยู่ ข้อมูล ณ ${D.built}`:`Showing ${r.length}, ranked by fit then recency. B2B boards often hide buyer names — reply through the platform and confirm the post is still open. Data as of ${D.built}. Stale (>12 months) posts are excluded at build time.`}
// ---------- markets ----------
function renderMarkets(){const M=Object.values(D.markets).sort((a,b)=>b.fit-a.fit);
 document.getElementById('mktCards').innerHTML=M.map(m=>{const n=D.distributors.filter(d=>d.country===m.code).length,sg=D.signals.filter(s=>s.country===m.code).length;
 return `<div class="card"><h3>${esc(L==='th'?m.name_th:m.name)} <span class="muted small">· ${n} ${w('dists')} · ${sg} ${w('signals')}</span></h3>
 <div class="score"><div><b>${m.fit}</b><small>${w('fit')} /100</small></div></div>
 <div class="small">${w('imports')}: <b>$${(m.bev_imports/1e6).toFixed(0)}M</b> (${m.year})</div>
 <div class="small">${w('growth')}: <b>${m.bev_growth>=0?'+':''}${(m.bev_growth*100).toFixed(0)}%</b> · ${w('thai')}: <b>${(m.thai_share*100).toFixed(1)}%</b></div>
 <div class="small">${w('access')}: <a href="${esc(m.fta_src)}" target="_blank" rel="noopener">${esc(L==='th'?m.fta_th:m.fta)}</a></div>
 ${m.halal?`<div class="small" style="color:var(--green)">${w('halal')}</div>`:''}
 <div class="small muted" style="margin-top:6px">${L==='th'?'ขนาด':'Size'} ${m.parts.size}/30 · ${L==='th'?'เติบโต':'Growth'} ${m.parts.growth}/25 · ${L==='th'?'ไทยมีฐาน':'Thai foothold'} ${m.parts.thai}/15 · ${L==='th'?'FTA':'Access'} ${m.parts.access}/20</div></div>`}).join('')}
// ---------- distributors ----------
function mine(){try{return JSON.parse(localStorage.getItem('mdm_mine')||'[]')}catch(e){return[]}}
function allDist(){return D.distributors.concat(mine())}
function flagTxt(v){return v===true?`<span style="color:var(--green)">${w('seen')}</span>`:v===false?`<span class="muted">${w('notseen')}</span>`:`<span class="unk">${w('unknown')}</span>`}
function distCard(d){const n=need(d),m=match(d),f=fit(d.country);const warm=(d.signals||[]).length||d.w;
 const sigs=(d.signals||[]).map(id=>D.signals.find(s=>s.id===id)).filter(Boolean);
 return `<div class="card ${warm?'warm':''}"><h3>${esc(d.name)} ${d.mine?`<span class="tag">${w('yours')}</span>`:''}</h3>
 <div class="small muted">${esc(cname(d.country))} · ${esc(d.type||'')} · ${(d.channels||[]).map(esc).join(', ')}</div>
 ${warm?`<div><span class="tag t-partner">${w('warm')}</span>${sigs.map(s=>`<span class="tag t-${s.type}">${w(typeKey(s.type))}</span>`).join('')}</div>`:''}
 <div class="score"><div><b>${m??'—'}</b><small>${w('match')}</small></div><div><b>${f??'—'}</b><small>${w('fit')}</small></div><div><b>${n.s}</b><small>${w('need')}</small></div></div>
 <div class="bar"><i style="width:${m||0}%"></i></div>
 <div class="small"><b>${w('why')}:</b><ul class="why">${n.why.map(x=>`<li>${esc(x)}</li>`).join('')||'<li class="muted">—</li>'}</ul></div>
 <div class="small"><b>${w('pitch')}:</b><ul class="why">${pitch(d).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>
 <div class="small muted">${L==='th'?'น้ำผลไม้':'Juice/drinks'}: ${flagTxt(d.f.j)} · ${L==='th'?'น้ำมะพร้าว':'Coconut water'}: ${flagTxt(d.f.c)} · ${L==='th'?'เอเชีย/ไทย':'Asian/Thai'}: ${flagTxt(d.f.a)}</div>
 ${n.unk.length?`<div class="small unk">${w('unkList')}: ${n.unk.map(esc).join(', ')}</div>`:''}
 <div class="small" style="margin-top:6px"><b>${w('evidence')}:</b> ${esc(d.evidence||'')}${(d.brands||[]).length?` <span class="muted">[${d.brands.map(esc).join(', ')}]</span>`:''}</div>
 ${sigs.map(s=>`<div class="small" style="margin-top:4px">🔥 “${esc(s.said)}” — <a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.src)}</a></div>`).join('')}
 <div class="small" style="margin-top:6px">${d.url?`<a href="${esc(d.url)}" target="_blank" rel="noopener">${w('source')} ↗</a>`:''} ${d.mine?`<button class="btn" data-del="${d.id}">${w('del')}</button>`:''}</div></div>`}
function distFiltered(c){return allDist().filter(d=>(!c||d.country===c)&&(!ST.mcat||(ST.mcat==='coco'?d.f.c===true:ST.mcat==='juice'?d.f.j===true:ST.mcat==='asian'?d.f.a===true:ST.mcat==='open'?d.f.o===true:true))&&(!ST.mch||(d.channels||[]).includes(ST.mch))&&(!document.getElementById('mwarm').checked||(d.signals||[]).length||d.w)).sort((a,b)=>(match(b)||0)-(match(a)||0))}
function renderDist(){document.getElementById('distCards').innerHTML=distFiltered(ST.mc).map(distCard).join('')||`<p class="muted">${w('none')}</p>`}
// ---------- trip ----------
function renderTrip(){const c=ST.tc,top=distFiltered(c).slice(0,10),ls=D.signals.filter(s=>s.country===c).sort((a,b)=>(b.fit-a.fit)||((a.age??400)-(b.age??400))).slice(0,15);const m=D.markets[c];
 document.getElementById('tripOut').innerHTML=`<div class="card"><h3>${esc(cname(c))} — ${w('fit')} ${m.fit}/100 · ${esc(L==='th'?m.fta_th:m.fta)}</h3>
 <h3 style="margin-top:10px">${w('top10')}</h3><div class="tw"><table><thead><tr><th>#</th><th>${L==='th'?'บริษัท':'Company'}</th><th>${w('match')}</th><th>${w('pitch')}</th><th>${w('source')}</th></tr></thead><tbody>${top.map((d,i)=>`<tr><td>${i+1}</td><td><b>${esc(d.name)}</b>${(d.signals||[]).length||d.w?' 🔥':''}<br><span class="small muted">${esc(d.type||'')}</span></td><td>${match(d)}</td><td class="small">${pitch(d).slice(0,2).map(esc).join('<br>')}</td><td><a href="${esc(d.url||'#')}" target="_blank" rel="noopener">↗</a></td></tr>`).join('')}</tbody></table></div>
 <h3 style="margin-top:12px">${w('leadsFor')} (${ls.length})</h3>${ls.length?`<div class="tw"><table><tbody>${ls.map(leadRow).join('')}</tbody></table></div>`:`<p class="muted">${w('none')}</p>`}</div>`}
// ---------- csv ----------
function csv(rows,name){const s=rows.map(r=>r.map(x=>'"'+String(x??'').replace(/"/g,'""')+'"').join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['\ufeff'+s],{type:'text/csv'}));a.download=name;a.click()}
// ---------- method ----------
function renderMethod(){const th=L==='th';document.getElementById('methBody').innerHTML=th?`
<p><b>คะแนนจับคู่ = ค่าเฉลี่ยเรขาคณิตของ (ความเหมาะของตลาด × ความต้องการของผู้จัดจำหน่าย)</b> ถ้าด้านใดต่ำ คะแนนรวมจะต่ำด้วย</p>
<p><b>ความเหมาะของตลาด (0–100):</b> ขนาดนำเข้า (30, สเกล log) + การเติบโตเทียบปี 2021 (25) + ส่วนแบ่งไทยที่มีอยู่ (15 — แสดงว่าตลาดยอมรับสินค้าไทย) + FTA (20 ถ้ามีผล, 8 ถ้าเจรจาจบแต่ยังไม่มีผล, 0 ถ้าไม่มี) ข้อมูล UN Comtrade</p>
<p><b>ความต้องการของผู้จัดจำหน่าย (0–100, ประเมินโดย AI จากหลักฐานที่แสดง):</b> ขายเครื่องดื่มอยู่แล้ว 25 · มีชั้นสินค้าเอเชีย/ไทย 15 · ไม่พบน้ำมะพร้าว (ช่องว่าง) 15 หรือมีน้ำมะพร้าวแล้ว 8–10 · ประกาศรับแบรนด์ใหม่ 20 · ผลไม้กระป๋อง 5 · ช่องทาง 5 ต่อช่องทาง (สูงสุด 15) · มีสัญญาณผู้ซื้อ/หาพาร์ทเนอร์ +10 ข้อมูลที่ไม่ทราบไม่ได้คะแนน และแสดงเป็น "ไม่ทราบ"</p>
<p><b>ลีดร้อน:</b> ดึงจาก TradeKey, go4WorldBusiness, Tradewheel, หน้าเว็บบริษัทที่เปิดรับแบรนด์, LinkedIn และ DITP ตัดโพสต์เก่ากว่า 12 เดือน จัดอันดับตามความเหมาะกับสินค้ามาลีแล้วตามความใหม่</p>
<p><b>การอัปเดต:</b> รัน <code>build_data.py</code> ใหม่หลังดึงหน้า buyer-board ของแต่ละประเทศ (ดู README) แนะนำทุกสัปดาห์ — สามารถตั้ง routine อัตโนมัติได้ภายหลัง</p>`:`
<p><b>Match = geometric mean of Market fit × Distributor need.</b> If either side is weak, the match is weak.</p>
<p><b>Market fit (0–100):</b> import size (30, log scale) + growth vs 2021 (25) + Thailand's existing share (15 — shows Thai goods are accepted) + trade access (20 if a Thai FTA is in force, 8 if concluded but not in force, 0 if none). Source: UN Comtrade public API.</p>
<p><b>Distributor need (0–100) — AI assessment from the listed evidence only:</b> already sells juice/drinks 25 · Asian/Thai shelf 15 · no coconut water seen (gap) 15, or coconut water already proven 8–10 · publicly invites new brands 20 · canned fruit 5 · 5 per channel (max 15) · expressed buyer/partner signal +10. Unknown inputs score 0 and are shown as "unknown", never guessed.</p>
<p><b>Warm leads:</b> TradeKey, go4WorldBusiness, Tradewheel buyer requests; company "brands wanted / partner with us" pages; LinkedIn company pages; DITP business-matching. Posts older than 12 months are dropped. Ranked by fit to Malee products (●●● coconut water, canned fruit, tropical/OEM; ●○○ apple/pomegranate/organic only) then recency.</p>
<p><b>Refresh:</b> re-run the fetch + <code>build_data.py</code> in the repo's README weekly (a routine can automate this later).</p>`}
// ---------- init ----------
function selects(){const cs=Object.keys(D.markets);
 opt(lc,[['',w('allC')]].concat(cs.map(c=>[c,cname(c)])).concat([['OTHER',w('other')]]),ST.lc);
 opt(lt,[['',w('allT')],['product',w('product')],['partner',w('partner')],['oem',w('oem')],['other',w('otherT')]],ST.lt);
 opt(lp,[['',w('allP')],['coco',w('coco')],['juice',w('juice')],['canned',w('canned')],['oem',w('oemP')]],ST.lp);
 opt(lf,[['',w('allF')],['fresh',w('fresh')],['recent',w('recent')],['standing',w('standing')]],ST.lf);
 opt(mc,[['',w('allC')]].concat(cs.map(c=>[c,cname(c)])),ST.mc);
 opt(mcat,[['',w('cat')],['juice',L==='th'?'มีน้ำผลไม้':'Has juice/drinks'],['coco',L==='th'?'มีน้ำมะพร้าว':'Has coconut water'],['asian',L==='th'?'ชั้นเอเชีย/ไทย':'Asian/Thai shelf'],['open',L==='th'?'เปิดรับแบรนด์ใหม่':'Invites new brands']],ST.mcat);
 opt(mch,[['',w('ch')],['Retail','Retail'],['HoReCa','HoReCa'],['Ethnic Asian','Ethnic Asian'],['E-commerce','E-commerce'],['Wholesale','Wholesale']],ST.mch);
 opt(tc,cs.map(c=>[c,cname(c)]),ST.tc);opt(fc,cs.map(c=>[c,cname(c)]))}
function renderAll(){applyI18n();selects();renderLeads();renderMarkets();renderDist();renderTrip();renderMethod();
 document.getElementById('mine').innerHTML=mine().map(distCard).join('');
 document.getElementById('foot').innerHTML=L==='th'?`ข้อมูล ณ ${D.built} · การค้า: UN Comtrade · บริษัท: หน้าเว็บสาธารณะที่ลิงก์ไว้ · คะแนนความต้องการเป็นการประเมินโดย AI ไม่ใช่การตรวจสอบสถานะบริษัท ไม่เผยแพร่ข้อมูลติดต่อส่วนบุคคล`:`Data as of ${D.built} · Trade: UN Comtrade · Companies: linked public pages · Need scores are AI assessments, not due diligence · No personal contact details published.`}
const $=id=>document.getElementById(id);const lc=$('lc'),lt=$('lt'),lp=$('lp'),lf=$('lf'),mc=$('mc'),mcat=$('mcat'),mch=$('mch'),tc=$('tc'),fc=$('fc');
[['lc',renderLeads],['lt',renderLeads],['lp',renderLeads],['lf',renderLeads],['mc',renderDist],['mcat',renderDist],['mch',renderDist],['tc',renderTrip]].forEach(([k,fn])=>$(k).addEventListener('change',e=>{ST[k]=e.target.value;fn()}));
$('mwarm').addEventListener('change',renderDist);
$('lenBtn').onclick=()=>{L='en';localStorage.setItem('mdm_lang',L);renderAll()};$('lthBtn').onclick=()=>{L='th';localStorage.setItem('mdm_lang',L);renderAll()};
$('leadCsv').onclick=()=>csv([['date','freshness','country','type','company','what they said','Malee products','source','url']].concat(leadsFiltered().map(s=>[s.date,s.fresh,cname(s.country),s.type,s.company||'(hidden by platform)',s.said,s.prods.map(p=>W.en[p==='oem'?'oemP':p]).join('; '),s.src,s.url])),'malee-warm-leads.csv');
$('distCsv').onclick=()=>csv([['country','company','type','channels','match','market fit','need (AI)','why','pitch','unknown','evidence','source']].concat(distFiltered(ST.mc).map(d=>{const n=need(d);return[cname(d.country),d.name,d.type,(d.channels||[]).join('; '),match(d),fit(d.country),n.s,n.why.join(' | '),pitch(d).join(' | '),n.unk.join('; '),d.evidence,d.url]})),'malee-distributor-shortlist.csv');
$('addForm').addEventListener('submit',e=>{e.preventDefault();const f=new FormData(e.target);const d={id:'m'+Date.now(),mine:true,name:f.get('name').trim(),country:f.get('country'),url:f.get('url'),type:L==='th'?'เพิ่มเอง':'Added by sales',channels:f.getAll('ch'),evidence:f.get('note')||'',brands:[],w:!!f.get('w'),f:{j:f.get('j')?true:null,c:f.get('c')?true:null,a:f.get('a')?true:null,o:f.get('o')?true:null}};
 if(!d.name)return;const m=mine();m.push(d);localStorage.setItem('mdm_mine',JSON.stringify(m));e.target.reset();renderAll();$('mine').scrollIntoView({behavior:'smooth'})});
document.addEventListener('click',e=>{const id=e.target.dataset&&e.target.dataset.del;if(id){localStorage.setItem('mdm_mine',JSON.stringify(mine().filter(x=>x.id!==id)));renderAll()}});
fetch('data.json').then(r=>r.json()).then(j=>{D=j;renderAll()});
