# Builds data/profiles.json from saved lead detail pages (run tools with DETAIL dir of curl'd pages).
# Publishes no personal names, emails or phone numbers.
import re,html,hashlib,json,os,sys
DET=sys.argv[1] if len(sys.argv)>1 else '../detail'
d=json.load(open('docs/data.json'))
def txt(u):
    fn=os.path.join(DET,hashlib.md5(u.encode()).hexdigest()+'.html')
    if not os.path.exists(fn): return ''
    f=open(fn,encoding='utf-8',errors='ignore').read()
    if 'Temporarily Unavailable' in f: return ''
    f=re.sub(r'<script.*?</script>|<style.*?</style>','',f,flags=re.S|re.I)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',f)))
def clean(s):
    s=re.sub(r'(?<!Product )\bName\s*:.*?(?=Email|Buying Products|Country|Mobile|$)','',s)
    s=re.sub(r'(Email|Mobile|Phone|Tel)\s*:\s*\S+','',s)
    s=re.sub(r'Contact\s*:.*?(?=Buyer Of|File a complaint|$)','',s)
    s=re.sub(r'[\w.+-]+@[\w.-]+','',s); s=re.sub(r'\+?\d[\d\s\-()]{7,}\d','',s); s=re.sub(r'[\d*][\d*\s\-]{6,}[\d*]','',s); s=re.sub(r'\*{3,}','',s)
    s=re.sub(r'(^|\s)\d{4,}(?=\s+Buying Products)','',s)
    return re.sub(r'\s+',' ',s).strip()
P={}
for s in d['signals']:
    if s['src'] not in ('TradeKey','go4WorldBusiness','Tradewheel'): continue
    t=txt(s['url']); p={'fetched':bool(t)}
    if s['src']=='TradeKey' and 'RFQ Details' in t:
        head=t[t.find('Posted on:'):t.find('RFQ Details')] if 'Posted on:' in t else ''
        body=t[t.find('RFQ Details')+11:]
        body=re.split(r'People who quote|Refine by popular tags|Recommended RFQs|Home Premium Services',body)[0]
        p['detail']=clean(body)[:420]
        m=re.search(r'Country:\s*([A-Za-z .]+?)(?:\s{1}|$)',body); p['statedCountry']=m.group(1).strip() if m else ''
        for k,r in [('freq',r'Buying Frequency:\s*(\w+)'),('qty',r'Quantity Required:\s*(.+?)(?= Last Updated| Posted| Buying| Payment| Destination| Quote|$)'),('pay',r'Payment Terms:\s*(.+?)(?= Shipping| Destination| Quote|$)'),('port',r'Destination Port:\s*(.+?)(?= Quote| Buying|$)')]:
            m=re.search(r,head+' '+t[:t.find('RFQ Details')]) ; 
            if m: p[k]=m.group(1).strip()[:80]
    elif s['src']=='go4WorldBusiness' and 'Wanted' in t:
        mm=re.search(r'Wanted : .{0,200}?Buyer From',t); i=mm.start() if mm else t.find('Wanted :'); seg=t[i:t.find('File a complaint',i)] if 'File a complaint' in t[i:] else t[i:i+1500]
        p['verified']=' VERIFIED ' in seg[:300]
        for k,r in [('qty',r'Quantity Required:\s*(.+?)(?= Payment)'),('pay',r'Payment Terms:\s*(.+?)(?= Shipping| Looking)')]:
            m=re.search(r,seg); 
            if m: p[k]=m.group(1).strip()[:80]
        m=re.search(r'Buyer Of ([^\n]+?)(?= Contact Buyer| Add to|$)',t[i:i+4000]); p['buyerOf']=m.group(1).strip()[:120] if m else ''
        m=re.search(r'Product Description:\s*(.*)',seg); p['detail']=clean(m.group(1))[:420] if m else ''
    elif s['src']=='Tradewheel':
        m=re.search(r'Member since\s*(\w+ \d{4})',t); p['memberSince']=m.group(1) if m else ''
        m=re.search(r'TRUST SCORE\s*(\d+)/100',t); p['trust']=m.group(1)+'/100' if m else ''
        m=re.search(r'Buy Offer Details:\s*(.*?)(?=Tips for Sellers|Additional Details)',t); p['detail']=clean(m.group(1))[:420] if m else ''
    P[s['url']]=p
json.dump(P,open('data/profiles.json','w'),ensure_ascii=False,indent=0)
print(len(P),sum(1 for p in P.values() if p.get('detail')))
