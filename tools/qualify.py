# Adds a qualification profile (requester type, size signals, worth-the-effort) to docs/data.json.
# AI assessment from public evidence only; unknown when not found.
import json,re
d=json.load(open('docs/data.json')); P=json.load(open('data/profiles.json'))
CN={'US':'usa|united states','AU':'australia','AE':'uae|united arab','SA':'saudi','PH':'philippines','MY':'malaysia','UK':'uk|united kingdom|england','CN':'china','PK':'pakistan','VN':'viet','MV':'maldives'}
SHORT_UNUSED={'https://importer.tradekey.com/buyoffer/Canned-Fruit-Cocktail-And-Pineapple-789103.html','https://importer.tradekey.com/buyoffer/Coconut-Water-Supplier-Required-2135369.html','https://importer.tradekey.com/buyoffer/Looking-For-Manufacturers-Of-Organic-Tender-Coconut-Water-For-Maldives-3870925.html'}
# ---- distributor size facts (from the linked public pages / LinkedIn company pages) ----
DS={
'Wismettac Asian Foods':['Founded 1912 (as Nishimoto Trading)','20 offices & branches (site)'],
'JFC International':['"A century of success" (site)'],
'Rhee Bros (Assi)':['40 years (site)','4,000+ products (site)'],
'KeHE Distributors':['19 distribution centers (site)'],
'Vasinee Food Corporation':['In business since 1987 (site)'],
'The Drinks Company (Miami)':['6 employees (LinkedIn)','Refrigerated truck fleet (LinkedIn)'],
'Wing Yip':['Since the 1970s','4 superstores; 4,500+ products (site)'],
'Delightful Brands (Digi East Wholesale)':['Founded 2024 (site)'],
'BKK Australia':['Established 1980 (site)'],
'Mur Thai Food Co':['DCs in Sydney, Melbourne, Brisbane (site)'],
'Oriental Merchant':['Since the 1970s; AU, NZ, SG, Europe, Canada sites'],
'Box World':['Since 2015; 25+ brands from 16 countries (site)'],
'Sea Millenium Trade':['Since 2001; 800+ products; 10,000+ customers (site)'],
'Best Marketing & Distribution':['Since 2014; 4,200+ foodservice outlets, 350+ retailers/wholesalers; 2,000+ products (site)'],
'SCC Group':['200+ brands; 170+ vehicles incl. 100 refrigerated (site)'],
'Sri Manisan':['30 years; 100+ products (site)'],
'SYSU International':['Since 1948; nationwide network (site)'],
'Fly Ace Corporation':['50+ years; 5 categories; 7,360 LinkedIn followers'],
'Grand Alliance Import Corp. (GAIC)':['In SM, Robinsons, Waltermart; YCH 3PL warehousing (site / WOFEX 2026)'],
'Hygenix General Trading':['Imports for UAE, Qatar, KSA, Bahrain (site)'],
'Ghori Trading':['1,500+ retail doors UAE/GCC (site)'],
'TAN Gulf':['3 hubs; 27 cities; 9,441+ channel reach points (site)'],
'Sunrise Distribution':['12 retail/marketplace/app partners; Riyadh HQ (site)'],
'Al-Sahah Foods':['400+ products (site)'],
'MultiBrands':['Founded 2006; 65 employees (LinkedIn); Riyadh, Dammam, Jeddah offices'],
'Binzagr Company':['Since 1881; 55 brands, 1,500+ SKUs; 859 trucks/day; 15K customers/day (site)'],
'Fantastic Thai Trading (Shanghai)':['2 employees (LinkedIn)'],
'COFCO W&W International':['1,000,000+ points of sale for IF (IFBH release, Sep 2025)'],
'Century Pacific Food':['Listed PH food group (site)'],
'Bidfood Australia':['National foodservice network (site)'],
'Metcash':['"Australia\'s leading wholesale distribution company" (site)'],
'Prompt Thai':['Founded 2000 (LinkedIn)'],
'Al Rasheed Trading':['Oriental-foods importer; Thai range listed (site)'],
'Ocado Retail (Taste of Thailand shop)':['Online grocer; dedicated Taste of Thailand shop (Thai Trade London post)'],
'EAT Thai Market':['2 employees (LinkedIn)'],
'Ettason':['Claims "#1 Asian Food Distributor in Australia" (site)'],
}
DFLAG={'EAT Thai Market':'Very small team (2 on LinkedIn)','Kassir Food & Beverage (Hydro Coco USA)':'Exclusive to a competing coconut-water brand','COFCO W&W International':'Tied to IF (direct Thai competitor)','Fantastic Thai Trading (Shanghai)':'Very small team (2 on LinkedIn)','Century Pacific Food':'Makes its own coconut lines (competitor)','Shanghai Pintai Supply Chain (上海品泰)':'Already sells competing Thai coconut water/juices'}
def dtype(t):
    t=t.lower()
    if t.startswith('buyer'): return 'Buyer (type not stated)'
    for k,v in [('retailer','Retailer'),('foodservice','Distributor (foodservice)'),('wholesal','Wholesaler'),('importer','Importer / distributor'),('distributor','Distributor'),('trading','Trader / importer'),('manufacturer','Manufacturer'),('agent','Agent'),('market expansion','Distributor (services)')]:
        if k in t: return v
    return 'Distributor'
def need_py(x):
    f=x['f'];s=0
    if f.get('j') is True:s+=25
    if f.get('a') is True:s+=15
    if f.get('j') is True and f.get('c') is False:s+=15
    elif f.get('c') is True:s+=8 if x['brands'] else 10
    if f.get('o') is True:s+=20
    if f.get('k') is True:s+=5
    s+=min(len(x['channels'])*5,15)
    if x.get('signals'):s+=10
    return min(s,100)
for x in d['distributors']:
    size=DS.get(x['name'],[]); n=need_py(x); fl=[DFLAG[x['name']]] if x['name'] in DFLAG else []
    reasons=[f'Need {n}/100 from evidence']
    if size: reasons.append('Size evidence: '+size[0])
    else: reasons.append('No public size data found')
    if x['f'].get('o'): reasons.append('Publicly invites new brands')
    if fl: w='Low' if 'competitor' in fl[0].lower() or 'Tied' in fl[0] or 'Exclusive' in fl[0] else 'Verify first'
    elif n>=55 and size and not any('employees' in z and re.search(r'\b[1-9] employees',z) for z in size): w='High'
    elif n>=40: w='Medium'
    else: w='Low'
    if w=='High' and 'Company page' not in x.get('st',[]) and not x['f'].get('o'): w='Medium'; reasons.append('Capped at Medium: evidence is from a directory/trade-show/embassy post, not its own site')
    x['q']=dict(rtype=dtype(x['type']),rtypeEv=x['type']+' — per its own site',size=size,role='Not posted',worth=w,reasons=reasons,flags=fl)
byid={x['id']:x for x in d['distributors']}
def lead_q(s):
    p=P.get(s['url'],{}); det=p.get('detail',''); t=(s['said']+' '+det+' '+p.get('buyerOf','')).lower()
    # requester type
    if re.search(r'cement|cosmetic|meat|seed|honey|salt|rice|carpet|vegetable, chicken',t) and len(re.findall(r',',det))>=3: rt,ev='Trader / broker','Asks for many unrelated goods'
    elif re.search(r'print my brand|own brand|custom packaged|private label|brand it|labelling',t): rt,ev='Brand owner (OEM buyer)','Post asks for supply under its own brand'
    elif re.search(r'from importer|we are importers|importer',t): rt,ev='Importer','Post states an importer requirement'
    elif re.search(r'distribution|distributor|wholesale',t): rt,ev='Distributor / wholesaler','Post mentions distribution/wholesale use'
    elif re.search(r'producer|manufactur|bottling|beverage manufacturing',t): rt,ev='Manufacturer','Post mentions production use'
    elif re.search(r'retail|store|shop|cafe|restaurant|market',t): rt,ev='Retailer','Post mentions retail/store use'
    else: rt,ev='Unknown','Post does not say'
    size=[];vol=0
    q=p.get('qty','')
    if q: size.append('Stated quantity: '+q)
    m=re.search(r'(\d[\d,]*)\s*(l|liter|litre|litter)s?\b',t)
    if re.search(r'less than container|lcl',t+q.lower()): vol=1
    elif re.search(r'container|fcl|contanier|twenty-foot|40ft|20ft',t+q.lower()): vol=2
    elif m and int(m.group(1).replace(',',''))>=10000: vol=2
    elif q or m: vol=1
    if p.get('freq') and p['freq'] not in ('Other',''): size.append('Buying frequency: '+p['freq']); vol=min(2,vol+1) if p['freq'] in('Monthly','Weekly','Daily') else vol
    if p.get('pay'): size.append('Payment terms: '+p['pay'])
    if p.get('port'): size.append('Destination port: '+p['port'])
    if p.get('verified'): size.append('go4WorldBusiness: VERIFIED buyer')
    if p.get('memberSince'): size.append('Tradewheel member since '+p['memberSince']+(' · trust '+p['trust'] if p.get('trust') else ''))
    if p.get('buyerOf'): size.append('Buyer of: '+p['buyerOf'])
    legit=0; flags=[]
    if p.get('verified'): legit+=1
    if s.get('company'): legit+=1; size.insert(0,'Company named on post: '+s['company'])
    if len(det)>120 or re.search(r'brix|ml\b|packag|tetra|uht|pet bottle',t): legit+=1
    if re.search(r'l/c|\blc\b',p.get('pay','').lower()): legit+=1
    sc=p.get('statedCountry','')
    if sc and not re.search(CN.get(s['country'],'zzz'),sc.lower()): flags.append(f'Country inconsistent (listing vs profile: {sc})')
    if det and (len(det)<25 or not re.search(r'[aeiou]{1}.*[aeiou]',det.lower()) or re.search(r'(\w)\1{3,}|bbv|we can buy',det.lower())): flags.append('Vague or one-line post')
    if rt=='Trader / broker': flags.append('Looks like a trader reselling many goods')
    if re.search(r'organic|raw|not heat|fresh green|young coconut|glass',t) and 'coco' in s['prods']: flags.append('Spec may not match Malee (organic/raw/glass)')
    if re.search(r'enlarge my business|direct deposit|western union|money ?gram',det.lower()): flags.append('Small/individual buyer language or risky payment')
    if re.search(r'coconut cream|coconut milk',t) and 'coconut water' not in t: flags.append('Asks for cooking coconut cream/milk — check if in Malee range')
    if re.search(r'\b(2 kg|pallet|200-300|100 box)\b',t): flags.append('Small volume')
    if not p.get('fetched') and s['src']!='Company website': flags.append('Detail page not readable — listing only')
    rec=1 if s['fresh']=='fresh' else 0
    score=(s['fit']-1)+vol+min(legit,3)+rec-len(flags)
    named=bool(s.get('company')) or p.get('verified')
    if any('inconsistent' in f or 'Vague' in f for f in flags): w='Verify first' if score>=3 else 'Low'
    elif score>=6 and named and s['fit']==3: w='High'
    elif score>=5: w='Verify first' if not named else 'Medium'
    elif score>=3: w='Medium'
    else: w='Low'
    if flags and w=='High': w='Medium'
    reasons=[f"Fit to Malee: {'●'*s['fit']}{'○'*(3-s['fit'])}", f"Volume: {['not stated','some','container-scale or recurring'][vol]}", f"Legitimacy signals: {legit}/4", 'Posted ≤90 days ago' if rec else f"Posted {s.get('age','?')} days ago"]
    pend=(s['src'] in ('TradeKey','Tradewheel')) and not s.get('company')
    return dict(rtype=rt,rtypeEv=ev,size=size,role='Not posted',worth=w,reasons=reasons,flags=flags,detail=det,namePending=pend and s['src']=='TradeKey',score=score)
for s in d['signals']:
    if s.get('kind')=='route' and s['src']!='ThaiTradeUSA (DITP)':
        stale=s['fresh']=='stale'
        s['q']=dict(rtype='Trade-promotion office / programme',rtypeEv='Government/organiser channel, not a buyer',size=['Gateway to registered importers; no buyer list published'],role='Not posted',worth='Low' if stale else 'Medium',reasons=['Route to buyers rather than a buyer','Ask the office for the registered-buyer list or an introduction']+(['Older than 12 months'] if stale else []),flags=['Older than 12 months'] if stale else [])
    elif s.get('stype') in ('Trade show','Embassy-TTC') and s['src'] in ('Trade show','Embassy / TTC') and not s.get('dist'):
        stale=s['fresh']=='stale'
        s['q']=dict(rtype='Retailer',rtypeEv='Retailer named by Thai consulate',size=['US Midwest retail chain (consulate page)'],role='Not posted',worth='Verify first',reasons=['Asked about Thai imports incl. coconut water','Older than 12 months — confirm still relevant'],flags=['Older than 12 months'] if stale else [])
    elif s.get('dist') and s['src'] in ('Trade show','Embassy / TTC'):
        x=byid[s['dist']]; q=dict(x['q'])
        undated=not s.get('date')
        q['reasons']=x['q']['reasons']+(['Hosted-buyer testimonial; year not stated'] if undated else (['Named hosted buyer at THAIFEX 2026 (26-30 May)'] if s['stype']=='Trade show' else ['Retailer onboarding Thai products via TTC London']))
        if (undated or not x['f'].get('o')) and q['worth']=='High': q['worth']='Medium'
        q['flags']=list(q.get('flags',[]))+(['Year of statement not stated'] if undated else [])
        s['q']=q
    elif s.get('dist'):
        x=byid[s['dist']]; q=dict(x['q']); q['reasons']=x['q']['reasons']+['Standing "we want brands" page — no volume stated']; s['q']=q
    elif s['src']=='ThaiTradeUSA (DITP)':
        s['q']=dict(rtype='Trade-promotion program',rtypeEv='DITP business matching for US buyers',size=['Government-run; buyer list via Thai Trade Center LA'],role='Not posted',worth='Medium',reasons=['Buyers pre-screened by DITP','Event already held Apr 2026 — follow up for the buyer list'],flags=[],detail='')
    else: s['q']=lead_q(s)
# manual overrides for shortlist leads with richer evidence
for s in d['signals']:
    if 'Venus Foods' in (s.get('company') or ''):
        s['q'].update(rtype='Importer / distributor',rtypeEv='"We are importers with strong distribution network in all major cities of Pakistan"',worth='High',flags=[],reasons=['Exact fit: canned pineapple, fruit cocktail, juices "mainly from Thailand"','Volume: 30 FCLs stated','Named company with street address on post','Posted 9 Aug 2026 (TradeKey page date) — confirm still active'])
        s['q']['size']=['Company named on post: Venus Foods (Lahore)','Stated quantity: 30 FCLs','"Strong distribution network in all major cities of Pakistan" (post)']
    if 'HAMOON' in (s.get('company') or ''):
        s['q'].update(rtype='Importer (company named)',rtypeEv='"My company is HAMOON CO.,LTD, from VietNam"')
from collections import Counter
print('dist',Counter(x['q']['worth'] for x in d['distributors']))
print('lead',Counter(s['q']['worth'] for s in d['signals']))
print('rtype',Counter(s['q']['rtype'] for s in d['signals']))
json.dump(d,open('docs/data.json','w'),ensure_ascii=False,indent=0)
for s in sorted([s for s in d['signals'] if s['q']['worth']=='High'],key=lambda s:(-s['q'].get('score',9),s.get('age') or 0))[:14]:
    print(s['country'],s['date'],s.get('company') or '-',s['said'][:70],'|',s['q']['rtype'],'|',s['q']['size'][:3],s['q']['flags'])
