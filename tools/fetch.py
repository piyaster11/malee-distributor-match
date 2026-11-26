import csv,subprocess,json,re,html,concurrent.futures as cf
rows=[l.rstrip('\n').split('\t') for l in open('cands.tsv') if l.strip()]
def f(r):
    c,n,u=r
    try:
        p=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','-w','\n%{http_code}',u],capture_output=True,timeout=40)
        out=p.stdout.decode('utf-8','ignore'); body,code=out.rsplit('\n',1)
    except Exception as e: body,code='','ERR'
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S|re.I)
    t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
    return dict(country=c,name=n,url=u,code=code,text=t[:20000])
with cf.ThreadPoolExecutor(12) as ex: res=list(ex.map(f,rows))
json.dump(res,open('fetched.json','w'))
for r in res: print(r['code'],len(r['text']),r['country'],r['name'])
