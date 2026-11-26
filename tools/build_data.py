import json,re,math
from datetime import date,datetime
TODAY=date(2026,11,26)
D='data/'
# ---------- MARKET FIT ----------
imp=json.load(open(D+'imports.json'))
t={(rc,pc,hs,y):v for rc,pc,hs,y,v in imp}
CC={'CN':156,'US':842,'AE':784,'SA':682,'PH':608,'MY':458,'AU':36,'UK':826}
NAME={'CN':['China','จีน'],'US':['United States','สหรัฐอเมริกา'],'AE':['UAE','สหรัฐอาหรับเอมิเรตส์'],'SA':['Saudi Arabia','ซาอุดีอาระเบีย'],'PH':['Philippines','ฟิลิปปินส์'],'MY':['Malaysia','มาเลเซีย'],'AU':['Australia','ออสเตรเลีย'],'UK':['United Kingdom','สหราชอาณาจักร']}
FTA={'CN':(20,'ACFTA + RCEP in force','ACFTA + RCEP มีผลแล้ว'),
 'PH':(20,'ATIGA (ASEAN) + RCEP in force','ATIGA (อาเซียน) + RCEP มีผลแล้ว'),
 'MY':(20,'ATIGA (ASEAN) + RCEP in force','ATIGA (อาเซียน) + RCEP มีผลแล้ว'),
 'AU':(20,'TAFTA + AANZFTA + RCEP in force','TAFTA + AANZFTA + RCEP มีผลแล้ว'),
 'AE':(8,'No FTA in force yet; Thai–UAE CEPA talks concluded 7 Oct 2026, signing expected Q1 2027','ยังไม่มี FTA ที่มีผล; เจรจา CEPA ไทย–UAE จบแล้ว 7 ต.ค. 2026 คาดลงนามไตรมาส 1/2027'),
 'SA':(0,'No Thai FTA (GCC tariff applies)','ไม่มี FTA กับไทย (ใช้ภาษีศุลกากร GCC)'),
 'US':(0,'No Thai FTA (US tariff on Thai goods applies; check current rate)','ไม่มี FTA (ใช้ภาษีสหรัฐฯ กับสินค้าไทย ตรวจอัตราปัจจุบัน)'),
 'UK':(0,'No Thai FTA (UK Global Tariff applies)','ไม่มี FTA (ใช้ UK Global Tariff)')}
FTASRC={'AE':'https://www.wam.ae/en/article/c2n1hr9-uae-thailand-conclude-cepa-negotiations-opening'}
HALAL={'AE','SA','MY'}
mk={}
for k,rc in CC.items():
    row={'code':k,'name':NAME[k][0],'name_th':NAME[k][1],'hs':{}}
    tot=tot21=th=0;yrs=set()
    for hs in ['2009','2202','2008','0402']:
        y='2024' if (rc,0,hs,'2024') in t else '2023'
        w=t.get((rc,0,hs,y));w21=t.get((rc,0,hs,'2021'));tv=t.get((rc,764,hs,y),0)
        row['hs'][hs]={'year':y,'world':w,'w2021':w21,'thai':tv}
        if hs!='0402' and w:
            tot+=w;tot21+=(w21 or 0);th+=tv;yrs.add(y)
    row['bev_imports']=tot;row['bev_growth']=(tot/tot21-1) if tot21 else None;row['thai_share']=th/tot if tot else None;row['year']='/'.join(sorted(yrs))
    mk[k]=row
sizes=[math.log10(m['bev_imports']) for m in mk.values()]
lo,hi=min(sizes),max(sizes)
for k,m in mk.items():
    s=30*(math.log10(m['bev_imports'])-lo)/(hi-lo)
    g=25*min(max((m['bev_growth']+0.2)/1.0,0),1)
    f=15*min(m['thai_share']/0.30,1)
    a=FTA[k][0]
    m['parts']={'size':round(s,1),'growth':round(g,1),'thai':round(f,1),'access':a}
    m['fit']=round((s+g+f+a)/90*100)
    m['fta']=FTA[k][1];m['fta_th']=FTA[k][2];m['fta_src']=FTASRC.get(k,'https://www.thaifta.com/')
    m['halal']=k in HALAL
# ---------- DISTRIBUTORS ----------
# flags: j=juice/drinks seen, c=coconut water seen, a=Asian/Thai shelf, d=dairy, k=canned fruit, o=open to new brands/partners
# value True=seen on source, False=not seen on readable source, None=unknown (source not readable / not stated)
X=[
# US
('US','Wismettac Asian Foods','https://www.wismettacusa.com/','Importer/wholesaler',['Ethnic Asian','Wholesale'],dict(j=None,c=None,a=True,o=True),'Importer, wholesaler and distributor of Asian food in North America since 1912; site has a "Partner with us" call.',[]),
('US','JFC International','https://www.jfc.com/','Distributor',['Ethnic Asian','Retail','HoReCa'],dict(j=True,c=False,a=True),'"Leading distributor of Asian food, beverages & Japanese liquor"; Japan-led range.',[]),
('US','HF Foods Group','https://www.hffoodsgroup.com/','Foodservice distributor',['HoReCa'],dict(j=True,c=False,a=True),'Specialty food distributor focused on Asian restaurants; site lists beverages and chilled/frozen.',[]),
('US','Rhee Bros (Assi)','https://www.rheebros.com/','Importer/distributor',['Ethnic Asian','Retail','HoReCa'],dict(j=None,c=None,a=True),'"Source. Import. Distribute. If it\'s Pan-Asian food, we do it." 40-year Asian food importer.',[]),
('US','Sun Hing Foods','https://www.sunhingfoods.com/','Importer/distributor',['Ethnic Asian','E-commerce'],dict(j=True,c=True,a=True,d=True,k=True),'Asian food importer with coconut products, beverages, dairy and canned categories; sells on Amazon.',[]),
('US','KeHE Distributors','https://www.kehe.com/','Distributor',['Retail','E-commerce'],dict(j=None,c=None,a=False,o=True),'Natural/organic & specialty distributor, 19 DCs; says it helps "suppliers expand their reach".',[]),
('US','Vasinee Food Corporation','https://vasineefoodcorp.com/','Thai importer/distributor',['Ethnic Asian','Retail','HoReCa'],dict(j=True,c=True,a=True,d=True),'Family-owned importer of Thai foods since 1987; range shows Chaokoh and Foco coconut drinks.',['Chaokoh','Foco']),
('US','Sun Fat USA','https://sunfatusa.com/product-category/beverages/','Asian beverage wholesaler',['Ethnic Asian','Retail','HoReCa'],dict(j=True,c=True,a=True,d=True,k=True),'Asian beverages supplier: coconut water, tropical juices, Thai tea; carries Chaokoh, Foco, Mogu Mogu, UFC.',['Chaokoh','Foco','Mogu Mogu','UFC']),
('US',"Jan's Food",'https://www.jansfood.com/beverages','Importer/wholesaler',['Ethnic Asian','Wholesale'],dict(j=True,c=True,a=True,d=True),'Wholesale "Coconut Water & Asian Juices" range (Southeast Asian focus).',[]),
('US','Kassir Food & Beverage (Hydro Coco USA)','https://www.hydrococo-usa.com/learn-more','Brand distributor',['Retail','E-commerce'],dict(j=True,c=True,a=False),'US sole distributor of Hydro Coco coconut water — a direct competitor tie.',['Hydro Coco']),
('US','The Drinks Company (Miami)','https://linkedin.com/company/the-drinks-company-llc','Boutique beverage distributor',['HoReCa','Retail'],dict(j=True,c=True,a=False,o=True),'Distributes coconut water, kombucha etc. with refrigerated trucks; "constantly on the lookout for new and innovative brands".',[]),
# UK
('UK','Wing Yip','https://www.wingyip.com/','Oriental wholesaler/grocer',['Ethnic Asian','Wholesale','Retail'],dict(j=None,c=None,a=True),'"UK\'s leading Oriental grocer", 4,500+ products, 4 superstores (Birmingham, Manchester, Croydon, Cricklewood).',[]),
('UK','Chuanglee','https://chuanglee.co.uk/catalogue/soft-drink-asian','Asian foodservice wholesaler',['HoReCa','Ethnic Asian'],dict(j=True,c=True,a=True,d=True),'Asian soft-drink catalogue incl. Chaokoh and Foco coconut drinks; London + nationwide.',['Chaokoh','Foco']),
('UK','Chadha Oriental Foods','https://chadhaorientalfoods.co.uk/brands/foco/','Oriental importer/distributor',['Ethnic Asian','Wholesale'],dict(j=True,c=True,a=True),'Distributes Foco coconut water (330 ml, 1 L UHT) and Foco Thai fruit drinks (mango, guava, lychee…).',['Foco']),
('UK','Tazaki Foods','https://www.tazakifoods.com/','Importer/distributor',['HoReCa','Retail'],dict(j=True,c=False,a=True),'Importer and distributor of Japanese food (Yutaka); cash & carry.',[]),
('UK','Bestway Wholesale','https://www.bestwaywholesale.co.uk/','Cash & carry wholesaler',['Wholesale','Retail','HoReCa'],dict(j=True,c=None,a=None),'Large UK wholesaler serving independent retail and catering.',[]),
('UK','Delightful Brands (Digi East Wholesale)','https://www.delightfulbrands.co.uk/about-us','Distributor',['Retail','E-commerce'],dict(j=True,c=True,a=True),'London distributor (founded 2024) of East/Southeast Asian food & beverage to UK retailers.',[]),
('UK','Longdan','https://longdan.co.uk/','Asian retailer/wholesaler',['Ethnic Asian','Retail','E-commerce','Wholesale'],dict(j=True,c=True,a=True,d=True),'"Home of Asia" stores + online, with bulk-buy; Thai, Filipino, Malaysian ranges; carries Aroy-D.',['Aroy-D']),
# AU
('AU','BKK Australia','https://bkk.com.au/about-us/','Thai/Asian importer-wholesaler',['Ethnic Asian','Retail','HoReCa'],dict(j=True,c=True,a=True,d=True),'Since 1980; first to import Thai jasmine rice; beverages in range; Foco seen.',['Foco']),
('AU','Mur Thai Food Co','https://www.murthaifood.com.au/aboutus','Importer/distributor',['Ethnic Asian'],dict(j=True,c=None,a=True,o=True),'Asian importer with DCs in Sydney, Melbourne, Brisbane; invites suppliers seeking an Australian distributor.',[]),
('AU','Ma Siam','https://masiam.com.au/','Thai importer-wholesaler',['HoReCa','Ethnic Asian'],dict(j=None,c=None,a=True,o=True),'Brisbane Thai food wholesaler/importer; offers "import or create own brand".',[]),
('AU','Auspac Trading','https://www.auspactrading.com.au/about-us/','Thai importer-wholesaler',['Retail','Ethnic Asian'],dict(j=False,c=False,a=True,o=True),'Imports Thai grocery (Pomelo rice, sauces); sources and private-labels from Thailand for clients.',[]),
('AU','Ettason','https://www.ettason.com.au/','Asian food distributor',['Retail','HoReCa','Ethnic Asian'],dict(j=None,c=None,a=True),'"#1 Asian Food Distributor in Australia"; carries Aroy-D.',['Aroy-D']),
('AU','Oriental Merchant','https://www.orientalmerchant.com.au/','Asian food distributor',['Ethnic Asian','Retail'],dict(j=None,c=None,a=True),'Asian food specialist since the 1970s; operations in AU, NZ, SG, Europe, Canada.',['Yeo\'s']),
('AU','Bidfood Australia','https://www.bidfood.com.au/','Foodservice distributor',['HoReCa'],dict(j=True,c=None,a=False,d=True),'National foodservice distributor (beverages, dairy, chilled).',[]),
('AU','Metcash','https://www.metcash.com/','Wholesaler (IGA supply)',['Wholesale','Retail'],dict(j=None,c=None,a=False),'Australia\'s leading wholesale distributor (food, liquor, hardware).',[]),
# MY
('MY','Box World','https://boxworld.com.my/','Importer/distributor',['Retail'],dict(j=None,c=None,a=False,o=True),'FMCG importer representing 25+ global brands from 16 countries; aims to be largest importer by 2028.',[]),
('MY','Sea Millenium Trade','https://smtsb.com.my/','Importer/distributor',['Wholesale','Retail'],dict(j=True,c=False,a=None),'FMCG importer since 2001, 800+ products incl. "Drinks and Juice"; Peninsular coverage.',['F&N']),
('MY','Best Marketing & Distribution','https://www.bestmarketingdistribution.com/','F&B distributor',['HoReCa','Retail'],dict(j=True,c=False,a=None,o=True),'Serves 4,200+ foodservice operators; imports brands and helps them enter the Malaysian market; halal mentioned.',['Marigold']),
('MY','SCC Group','https://sccgroup.com.my/','Distributor',['Retail','HoReCa','E-commerce'],dict(j=True,c=False,a=None,d=True,o=True),'200+ third-party brands, 170 vehicles incl. 100 reefers; beverages incl. Yeo\'s, Bundaberg.',['Yeo\'s']),
('MY','Sri Manisan','https://srimanisan.com/','Fine-food importer',['HoReCa','Retail'],dict(j=True,c=False,a=False,d=True),'Importer of international ambient & chilled brands for hotels, bakeries, supermarkets; carries Rauch juices.',['Rauch']),
('MY','DKSH Malaysia','https://www.dksh.com/my-en/home','Market expansion services',['Retail','HoReCa'],dict(j=None,c=None,a=None,o=True),'Market-expansion services provider (distribution for principals).',[]),
# PH
('PH','SYSU International','https://www.sysuinc.com.ph/about/','Importer/exclusive distributor',['Retail'],dict(j=True,c=False,a=True),'Exclusive distributor of Tree Top juices, Lee Kum Kee, Smucker\'s etc.',['Tree Top']),
('PH','Fly Ace Corporation','https://ph.linkedin.com/company/fly-ace-corporation','Importer/distributor',['Retail','E-commerce'],dict(j=True,c=None,a=None,d=True,k=True),'50+ years; categories: canned fruit, juices, milk; brands incl. Welch\'s, Mott\'s, Old Orchard, Jolly.',['Welch\'s','Mott\'s']),
('PH','Grand Alliance Import Corp. (GAIC)','https://gaic.com.ph/pages/about-us','Importer/distributor',['Retail','HoReCa'],dict(j=True,c=False,a=False,d=True,o=True),'Imports juices (Fontana) and dairy into SM, Robinsons, Waltermart; "For International Brands: Let\'s Expand Together".',['Fontana']),
('PH','McAsia Foodtrade','https://mcasiafoodtrade.ph/','Asian food importer',['Retail','HoReCa','E-commerce'],dict(j=True,c=None,a=True,d=True),'"Home to your Asian cravings"; imports Asian incl. Thai brands for supermarkets.',[]),
('PH','Gold River Management','https://goldrivermanagement.com.ph/our-brands/','Beverage distributor',['Retail','HoReCa'],dict(j=True,c=True,a=True,o=True),'Beverage distributor ("we help FMCG brands thrive"); Thai drinks incl. Mogu Mogu.',['Mogu Mogu']),
('PH','Century Pacific Food','https://www.centurypacific.com.ph/','Food manufacturer/distributor',['Retail'],dict(j=False,c=True,a=False,d=True),'Large PH food group with coconut and milk lines (also coconut OEM exporter) — partly a competitor.',[]),
# AE
('AE','Hygenix General Trading','https://hygenixgt.com/','Asian food importer',['Retail','HoReCa','Ethnic Asian'],dict(j=None,c=True,a=True),'"Asian Food Importers in the UAE, Qatar, Saudi Arabia, Bahrain".',[]),
('AE','A Mart Foodstuff Trading','https://amartuae.com/','Asian importer',['Ethnic Asian'],dict(j=True,c=True,a=True),'Distributes Asian instant food & drinks from Korea, Thailand, Japan; carries IF coconut water.',['IF']),
('AE','Ghori Trading','https://ghoritrading.com/distribution/food-fmcg-distributor-uae','FMCG distributor',['Retail','HoReCa','E-commerce'],dict(j=True,c=False,a=False,d=True,o=True),'"Distribute your brand"; moves beverages & juices to 1,500+ doors in UAE/GCC.',[]),
('AE','Aldiqa Foodstuff Trading','https://aldiqatrading.com/','Importer/distributor',['Retail','Wholesale','HoReCa'],dict(j=True,c=False,a=False,d=True,o=True),'Santé no-sugar juices, Twist energy; "Become a Partner"; supplies private-label customers.',['Santé']),
('AE','Shams Al Aseel Foodstuff Trading','https://alaseelfoodstuff.com/','F&B trading',['Retail','HoReCa'],dict(j=True,c=False,a=False),'Beverage trading (Pepsi, Coca-Cola, Red Bull, Perrier, Voss per its brand pages).',[]),
('AE','Treasure Islands Food & Beverages','https://www.treasureislands.ae/','FMCG distributor',['Retail'],dict(j=True,c=False,a=False),'Dubai FMCG distributor; brands seen incl. Del Monte.',['Del Monte']),
('AE','Al Maya Group','https://www.almaya.ae/','Retailer + FMCG distributor',['Retail'],dict(j=None,c=None,a=None),'Supermarket chain and FMCG distribution across UAE, Bahrain, Kuwait, Qatar, Oman.',[]),
('AE','Transmed','https://www.transmed.com/','FMCG & foodservice distributor',['Retail','HoReCa'],dict(j=None,c=None,a=None),'Consumer goods + foodservice distribution across UAE, KSA, UK and others.',[]),
# SA
('SA','TAN Gulf','https://tangulf.com/','Distributor/brand builder',['Retail','HoReCa','E-commerce'],dict(j=True,c=False,a=False,o=True),'3 hubs (Riyadh/Jeddah/Dammam); imports Rubicon mango/guava/lychee drinks; "for international brands entering the Kingdom".',['Rubicon']),
('SA','Sunrise Distribution','https://sunrise-ksa.com/','FMCG importer',['Retail','E-commerce'],dict(j=True,c=False,a=False,o=True),'"Your route into Saudi Arabia" — import, SFDA, listing; juices & drinks category.',[]),
('SA','Al-Sahah Foods','https://alsahahfood.com/services','Importer/distributor',['HoReCa','Retail'],dict(j=True,c=None,a=True,o=True),'400+ products, imports Asian brands (Mama Suka, Hobe); supplies juices to HoReCa; "Become a supplier" form.',[]),
('SA','MultiBrands','https://linkedin.com/company/mbftcl','F&B trading',['Retail','HoReCa'],dict(j=True,c=False,a=False,d=True),'Riyadh F&B trader; dairy, juice, coffee; clients incl. Panda, Danube, Othaim, hotels.',[]),
('SA','Alnours','https://al-nours.com/','Distributor/e-shop',['Retail','E-commerce'],dict(j=True,c=False,a=False),'Official Domty distributor: mango, guava, cocktail nectars (200 ml) in Riyadh & Jeddah.',['Domty']),
('SA','Binzagr Company','https://www.binzagr.com/','FMCG distributor',['Retail','HoReCa'],dict(j=None,c=None,a=None,o=True),'One of KSA\'s largest FMCG distributors (since 1881); 55 brands, 1,500 SKUs; food-service network; works with "Principals".',[]),
# CN
('CN','Shanghai Pintai Supply Chain (上海品泰)','http://www.tangjiu.cn/z_zcpintai','Importer',['Wholesale'],dict(j=True,c=True,a=True),'Imports Thai juices (durian, mangosteen, watermelon) and coconut water (WILDCOCO); recruiting regional agents.',['WILDCOCO']),
('CN','Fantastic Thai Trading (Shanghai)','https://linkedin.com/company/fantastic-thai-trading-company','Importer/brand manager',['Retail','E-commerce'],dict(j=None,c=False,a=True,o=True),'Brand management, import & distribution (Walmart, Metro, Sam\'s, Tmall, JD); "exceptional partner to manufacturers".',[]),
('CN','Zhongke Muzhen (中科沐臻)','http://www.flce-asia.com/exhibition_news_1/show/582.html','China general agent',['Wholesale'],dict(j=True,c=True,a=True),'Mainland general agent for Thai MIRAMAR coconut water and aloe drinks (FLCEAsia 2025 exhibitor).',['MIRAMAR']),
('CN','COFCO W&W International','https://www.iffamily.com/news-activities/ifbh-limited-signed-strategic-partnership-contract-with-cofco-appointed-as-new-distributor-for-ifbh-coconut-water/','State trading distributor',['Retail','E-commerce'],dict(j=True,c=True,a=True),'Appointed IF coconut water distributor (Sep 2025), 1M+ points of sale — tied to a direct competitor.',['IF']),
('CN','Sinodis (西诺迪斯)','https://www.sinodis.com/','Foodservice importer',['HoReCa'],dict(j=None,c=False,a=False,d=True),'Imported bakery/dessert/beverage ingredients for China foodservice (fruit purées, dairy).',[]),
('CN','Classic Fine Foods China','https://www.classicfinefoods.com/','Fine-food distributor',['HoReCa','Retail'],dict(j=None,c=None,a=False),'Fine-food specialist for hotels/restaurants; chilled capability.',[]),
('CN','DKSH China','https://www.dksh.com/cn-en/home','Market expansion services',['Retail'],dict(j=None,c=None,a=None,o=True),'Market-expansion services provider (distribution for principals).',[]),
('UK','Prompt Thai','https://linkedin.com/company/prompt-thai','Thai/Oriental food importer-wholesaler',['Wholesale','Retail','HoReCa'],dict(j=True,c=None,a=True),'LinkedIn company page: wholesale importer of Thai & Oriental food and drink; lists "Drinks & Beverages" and "Coconut Products"; founded 2000, Peterborough.',[]),
('AE','EAT Thai Market','https://linkedin.com/company/eatthaimarket','Thai products importer/distributor',['Retail','E-commerce'],dict(j=True,c=None,a=True),'LinkedIn company page: Thai products importer/distributor in the UAE incl. fruit & vegetable juice.',[]),
('SA','Al Rasheed Trading','http://rasheedfoods.com/products/thai_products/','Oriental foods importer',['Retail','Wholesale'],dict(j=True,c=True,a=True),'Importer of Oriental foods; Thai range includes fruit cocktail and C-Light fruit drinks (pineapple, mixed fruit, orange, lychee, guava, mango) and a Pinoy coconut drink.',['C-Light','Pinoy']),
('MY','Village Grocer','https://halalexpo.com/events/thaifex-anuga-asia-2026','Retailer (supermarket chain)',['Retail'],dict(j=None,c=None,a=None),'Named as a confirmed 2026 THAIFEX-Anuga Asia hosted buyer (Halal Expo event page). Supermarket chain; no range data read.',[]),
('SA','Al Madina Group','https://thaifex-anuga.com/hosted-buyer-programme/','Retailer / importer (private-label buyer)',['Retail'],dict(j=None,c=None,a=None,o=True),'THAIFEX hosted-buyer testimonial (year not stated) by its Head of Imports & Private Label: retailers can "develop their private labels, as well as find specific brands or categories".',[]),
('UK','Surya Foods','https://thaifex-anuga.com/hosted-buyer-programme/','Buyer (business type not stated)',['Wholesale'],dict(j=None,c=None,a=True),'THAIFEX hosted-buyer testimonial (year not stated): "sources from over 50 suppliers at THAIFEX" and has attended 10+ times.',[]),
('AE','Golden Praxis','https://thaifex-anuga.com/hosted-buyer-programme/','Buyer (business type not stated)',['Retail'],dict(j=None,c=None,a=None),'THAIFEX hosted-buyer testimonial (year not stated), Dubai-based; gathered international business contacts as a hosted buyer.',[]),
('UK','Ocado Retail (Taste of Thailand shop)','https://www.linkedin.com/posts/thai-trade-london_ocadothai-tasteofthailand-thaikitchenoftheworld-activity-7507699662582145026-d_im','Online retailer',['Retail','E-commerce'],dict(j=True,c=None,a=True),'Taste of Thailand online shop (curry pastes, sauces, rice, snacks, beverages) with Thai brands onboarded via Thai Trade London (DITP).',[]),
]
dist=[]
for i,(c,n,u,typ,ch,f,ev,br) in enumerate(X):
    dist.append(dict(id=f'd{i+1}',country=c,name=n,url=u,type=typ,channels=ch,f=f,evidence=ev,brands=br))
DST={'Prompt Thai':['Directory'],'EAT Thai Market':['Directory'],'Al Rasheed Trading':['Company page'],'Village Grocer':['Trade show'],'Al Madina Group':['Trade show'],'Surya Foods':['Trade show'],'Golden Praxis':['Trade show'],'Ocado Retail (Taste of Thailand shop)':['Embassy-TTC']}
for d in dist: d['st']=DST.get(d['name'],['Company page'])
# ---------- SIGNALS ----------
def prods(s):
    s=s.lower();p=[]
    if 'coconut' in s: p.append('coco')
    if re.search(r'juice|nectar|tropical|mango|guava|beverage|drink|tetra',s): p.append('juice')
    if re.search(r'canned|syrup|cocktail|pineapple',s): p.append('canned')
    if re.search(r'uht milk|dairy|milk drink',s): p.append('dairy')
    if re.search(r'private label|own brand|oem|labelling|labeling',s): p.append('oem')
    return p or ['juice']
def stype(s):
    return 'oem' if re.search(r'private label|own brand|oem|labelling',s.lower()) else 'product'
COMP=r'(ltd|llc|l\.l\.c|pty|inc\b|co\.|corp|trading|foods?\b|company|juicery|organic|produce|club|group|intl|international|agencies|tea company)'
BAD=r'^(company|no company|privet|private|broker|skincare)$'
sig=[]
SC={'china':'CN','usa':'US','united-states':'US','uae':'AE','united-arab-emirates':'AE','saudi-arabia':'SA','philippines':'PH','malaysia':'MY','australia':'AU','uk':'UK','united-kingdom':'UK'}
tk=json.load(open(D+'sig/tk_keep.json'))
R=r'juice|coconut water|canned fruit|fruit in syrup|beverage|nectar|tetra|fruit cocktail|drinks|private label'
XX=r'rani|rane|energy drink|cups|glasses|basil|aloe|jagua|icey|trop pop|slimming|lemon juice|pomegranate|carpet|yak|aluminium|machine|exporters|watermelon|organic beverages|raw coconut|young coconut|fresh quick|cart|aronia|cold pressed|south america|hexamine|food products$'
for o in tk:
    tt=o['title']
    if not re.search(R,tt.lower()) or re.search(XX,tt.lower()): continue
    if 'key west' in o.get('loc','').lower(): continue
    b=o['buyer'].strip()
    comp=b if (re.search(COMP,b,re.I) and not re.search(BAD,b,re.I)) else ''
    title=re.sub(r',\s*(Food & Beverage|Agriculture|Canned Food|Home & Garden).*$','',tt).strip()
    sig.append(dict(src='TradeKey',type=stype(tt),country=SC[o['page']],company=comp,said=title,date=o['iso'],url=o['url'],prods=prods(tt)))
g4=json.load(open(D+'sig/g4_keep.json'))
for o in g4:
    if o['age']>365: continue
    tt=o['title'].replace('Wanted : ','Wanted: ')
    if re.search(r'pomegranate|apple|fizzy|matcha',tt.lower()): pass
    desc=o['desc']
    m=re.search(r'(Type ?: ?[^:]{3,120}?)(?: Quantity| Material| Usage| Note| HS| Purpose| Packaging|$)',desc)
    said=tt+((' — '+m.group(1).strip()) if m else '')
    sig.append(dict(src='go4WorldBusiness',type=stype(desc+tt),country=SC[o['page']],company='',said=said,date=o['iso'],url=o['url'],prods=prods(tt+' '+desc)))
# manual verified (shortlist + partner pages)
M=[
('TradeKey','product','PK','Venus Foods (Lahore)','Importer with national distribution; main lines pineapple, fruit cocktail and pure juices "mainly from Thailand"; wants a canner ONLY from Thailand/Malaysia; 30 FCLs.','2026-08-09','https://importer.tradekey.com/buyoffer/Canned-Prineapple-And-Fruit-Cocktail-725248.html',['canned','juice']),
('TradeKey','product','PK','','Urgently needs canned fruit cocktail and canned pineapple, 3 containers a month.','2026-11-06','https://importer.tradekey.com/buyoffer/Canned-Fruit-Cocktail-And-Pineapple-789103.html',['canned']),
('TradeKey','oem','PH','','Coconut water supplier required: 33,000 L monthly, UHT 330 ml/500 ml/1 L twist cap; "can provide own brand labelling".','2026-09-10','https://importer.tradekey.com/buyoffer/Coconut-Water-Supplier-Required-2135369.html',['coco','oem']),
('TradeKey','product','VN','HAMOON Co., Ltd','Needs original coconut water, no sugar, 330 ml PET or paper pack; wants to move fast.','2026-11-08','https://importer.tradekey.com/buyoffer/Buy-About-Coconut-Water-Beverage-3492353.html',['coco']),
('TradeKey','product','MV','','Adding organic tender coconut water to a regional wholesale range; opening order then scalable replenishment; pilot lot, FOB/CIF.','2026-11-18','https://importer.tradekey.com/buyoffer/Looking-For-Manufacturers-Of-Organic-Tender-Coconut-Water-For-Maldives-3870925.html',['coco']),
('Tradewheel','product','CN','','Beverage distribution company seeks 100% natural coconut water, UHT/NFC, no added sugar, Brix 4.5–5.5, 330 ml/1 L Tetra Pak or aseptic bulk; monthly.','2026-03-06','https://www.tradewheel.com/buyers/need-bulk-supply-of-coconut-water-from-beverage/943748/',['coco']),
('Company website','partner','PH','Grand Alliance Import Corp. (GAIC)','"For International Brands: Let\'s Expand Together" — full-service entry into PH (import, regulatory, retail distribution); juices & beverages.','','https://gaic.com.ph/pages/about-us',['juice','coco']),
('Company website','partner','SA','TAN Gulf','"One partner from regulatory approval to shelf … for international brands entering the Kingdom"; imports Rubicon tropical juice drinks.','','https://tangulf.com/',['juice','coco']),
('Company website','partner','SA','Sunrise Distribution','"Your route into Saudi Arabia" for brand owners & exporters; juices and drinks category.','','https://sunrise-ksa.com/',['juice','coco']),
('Company website','partner','AU','Mur Thai Food Co','"If you are a supplier … looking for a distributor … in the Australian market we would like to hear from you."','','https://www.murthaifood.com.au/aboutus',['coco','juice','canned']),
('LinkedIn','partner','US','The Drinks Company (Miami)','"Constantly on the lookout for new and innovative brands to add to our portfolio" (coconut water, kombucha…).','','https://linkedin.com/company/the-drinks-company-llc',['coco','juice']),
('Company website','partner','AE','Ghori Trading','"Distribute your brand" — moves beverages & juices to 1,500+ retail doors in UAE/GCC.','','https://ghoritrading.com/distribution/food-fmcg-distributor-uae',['juice']),
('Company website','partner','AE','Aldiqa Foodstuff Trading','"Become a Partner"; supplies juices/beverages and serves private-label customers across ME, Africa, Asia.','','https://aldiqatrading.com/',['juice']),
('Company website','partner','SA','Al-Sahah Foods','"Become a supplier — join our network of trusted suppliers"; supplies juices to hotels/restaurants.','','https://alsahahfood.com/services',['juice']),
('Company website','partner','MY','Best Marketing & Distribution','Imports brands and assists them "in entering the local market"; 4,200+ foodservice outlets.','','https://www.bestmarketingdistribution.com/',['juice','dairy']),
('LinkedIn','partner','CN','Fantastic Thai Trading (Shanghai)','"Will continue to be an exceptional partner to manufacturers … helping excellent brands to achieve success in China" (Walmart, Sam\'s, Tmall, JD).','','https://linkedin.com/company/fantastic-thai-trading-company',['coco','juice']),
('Company website','partner','AU','Ma Siam','Brisbane Thai importer offering "Import or Create Own Brand" packaging for clients.','','https://masiam.com.au/',['oem','juice']),
('ThaiTradeUSA (DITP)','other','US','DITP Thailand–U.S. Online Business Matching','US buyers matched with Thai suppliers of coconut water & canned pineapple (Malee International listed). Ask Thai Trade Center LA which buyers registered.','2026-04-28','https://thaitradeusa.com/events/179',['coco','canned']),
]
for s,ty,c,co,said,d,u,p in M:
    sig.append(dict(src=s,type=ty,country=c,company=co,said=said,date=d,url=u,prods=p,manual=True))

# ---- THAIFEX / embassy / trade-promotion sources (t392u/t393u): (stype,type,country,company,said,date,url,prods,kind) ----
M2=[
('Trade show','other','US','Wismettac Asian Foods','Named as a confirmed 2026 THAIFEX-Anuga Asia hosted buyer (Halal Expo event page, hosted-buyer list).','2026-05-26','https://halalexpo.com/events/thaifex-anuga-asia-2026',['juice'],'buyer'),
('Trade show','other','MY','DKSH Malaysia','DKSH (group-level) named as a confirmed 2026 THAIFEX-Anuga Asia hosted buyer; the hosted-buyer list does not say which country office.','2026-05-26','https://halalexpo.com/events/thaifex-anuga-asia-2026',['juice'],'buyer'),
('Trade show','other','MY','Village Grocer','Named as a confirmed 2026 THAIFEX-Anuga Asia hosted buyer (supermarket chain).','2026-05-26','https://halalexpo.com/events/thaifex-anuga-asia-2026',['juice'],'buyer'),
('Trade show','oem','SA','Al Madina Group','Hosted-buyer testimonial (year not stated): Saudi retailer wants to "develop their private labels" and "find specific brands or categories".',None,'https://thaifex-anuga.com/hosted-buyer-programme/',['oem'],'buyer'),
('Trade show','other','UK','Surya Foods','Hosted-buyer testimonial (year not stated): UK buyer "sources from over 50 suppliers" at THAIFEX; attended 10+ times.',None,'https://thaifex-anuga.com/hosted-buyer-programme/',['juice'],'buyer'),
('Trade show','other','AE','Golden Praxis','Hosted-buyer testimonial (year not stated): Dubai-based buyer met international suppliers at THAIFEX.',None,'https://thaifex-anuga.com/hosted-buyer-programme/',['juice'],'buyer'),
('Embassy-TTC','partner','UK','Ocado Retail (Taste of Thailand shop)','Thai Trade London: Thai products "coming soon" to Ocado Retail\'s Taste of Thailand online shop; range includes beverages. Ask TTC London how to get a Malee line listed. Post is dated only "2 months ago" (about Sep 2026).','2026-09-26','https://www.linkedin.com/posts/thai-trade-london_ocadothai-tasteofthailand-thaikitchenoftheworld-activity-7507699662582145026-d_im',['juice','coco'],'buyer'),
('Embassy-TTC','other','US','Kroger','Royal Thai Consulate-General New York met Kroger (US Midwest retailer) to discuss Thai imports incl. coconut water. Older than 12 months.','2025-08-28','https://newyork.thaiembassy.org/en/content/discussion-on-thai-imports-with-kroger-a-leading-r',['coco'],'buyer'),
('Embassy-TTC','other','UK','Thai Trade London (DITP): online business matching','TTC London invites UK importers to online business matching with Thai F&B suppliers (FOODER 2026 programme closed 23 Oct 2026; F&B matching Mar 2026). Route to ask for the registered-buyer list.','2026-10-01','https://www.thaitradelondon.com/online-business-matching-obm-fooder-2026/',['juice'],'route'),
('Embassy-TTC','other','US','Thai Trade USA (DITP): F&B online business matching','Second DITP US business-matching round for Thai food & beverage (event 176). Route to ask Thai Trade Center for buyer lists.','2026-03-24','https://thaitradeusa.com/events/176',['juice','coco'],'route'),
('Trade show','other','US','Summer Fancy Food Show 2026 (New York)','Royal Thai Consulate NY / Thai Trade Center visited 13 Thai exporters at Summer Fancy Food 2026 (29 Jun); range incl. coconut water. Importer names not published.','2026-06-29','https://www.mfa.go.th/en/content/newyork-080726-2',['coco'],'route'),
('Embassy-TTC','other','AE','Gulfood 2026 Thailand Pavilion (Thai Trade Center Dubai)','Thailand Pavilion at Gulfood 2026 (Dubai, Jan 2026) positioned as a key export platform for halal-certified Thai F&B. Route into UAE/GCC importers.','2026-01-27','https://gulfnews.com/business/corporate-news/thailand-showcases-halal-excellence-and-culinary-innovation-at-gulfood-2026-1.500421848',['juice'],'route'),
('Embassy-TTC','other','SA','Thai Trade Centre Middle East','DITP Thai Trade Centre Middle East LinkedIn page: contact point for Saudi/GCC importer matching. No specific buyer named.',None,'https://linkedin.com/company/thaitradecentre-middleeast',['juice'],'route'),
('Embassy-TTC','other','PH','Thai Trade Center Manila (DITP)','Manila TTC says it "regularly facilitates business matching" for Philippine importers, "even on demand". Older than 12 months.','2025-10-24','https://www.philstar.com/business/biz-memos/2025/10/24/2481953/thai-trade-center-business-bridge-connecting-filipino-entrepreneurs-enhance-trade-opportunities-thailand',['juice'],'route'),
]
for st,ty,c,co,said,d,u,p,kind in M2:
    sig.append(dict(src={'Trade show':'Trade show','Embassy-TTC':'Embassy / TTC'}[st],type=ty,country=c,company=co,said=said,date=d,url=u,prods=p,manual=True,stype=st,kind=kind))
# dedupe by url
seen=set();S=[]
for s in sig:
    k=(s['url'],s['company'] if s.get('stype') in ('Trade show',) else '')
    if k in seen: continue
    seen.add(k);S.append(s)
for i,s in enumerate(S):
    s['id']=f's{i+1}'
    if 'stype' not in s: s['stype']={'TradeKey':'Buyer board','go4WorldBusiness':'Buyer board','Tradewheel':'Buyer board','Company website':'Company page','LinkedIn':'Company page','ThaiTradeUSA (DITP)':'Embassy-TTC'}[s['src']]
    s.setdefault('kind','route' if s['src']=='ThaiTradeUSA (DITP)' else 'buyer')
    tx=(s['said']+' '+' '.join(s['prods'])).lower()
    s['fit']=3 if re.search(r'coco|canned|oem|tropical|mango|guava|pineapple|lychee|nectar|tetra|cocktail|asian|thai',tx) else (1 if re.search(r'apple|pomegranate|orange|organic|blueberry',tx) else 2)
    if s['date']:
        age=(TODAY-datetime.strptime(s['date'],'%Y-%m-%d').date()).days
        s['age']=age;s['fresh']='fresh' if age<=90 else ('recent' if age<=365 else 'stale')
    else: s['age']=None;s['fresh']='standing'
# link partner signals to distributors
byname={d['name'].split(' (')[0].lower():d for d in dist}
for s in S:
    if s['company']:
        k=s['company'].split(' (')[0].lower()
        for nm,d in byname.items():
            if k==nm or k in nm or nm in k:
                d.setdefault('signals',[]).append(s['id']);s['dist']=d['id']
                if s['stype'] not in d['st']: d['st'].append(s['stype'])
json.dump(dict(markets=mk,distributors=dist,signals=S,built='2026-11-26'),open('docs/data.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print('dist',Counter(d['country'] for d in dist))
print('sig',Counter(s['country'] for s in S));print(Counter(s['src'] for s in S));print(Counter(s['type'] for s in S));print(Counter(s['fresh'] for s in S))
for k,m in mk.items(): print(k,m['fit'],m['parts'],round(m['bev_imports']/1e6),round((m['bev_growth'] or 0)*100),round(m['thai_share']*100,1),m['year'])
print([ (d['name'],d.get('signals')) for d in dist if d.get('signals')])
