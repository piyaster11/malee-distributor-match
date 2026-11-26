import json,time,urllib.request
B="https://comtradeapi.un.org/public/v1/preview/C/A/HS"
R="842,156,704,608,458,36,392,784,682,826,410,360,702,116,104,418,634,414"
def get(q):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(B+"?"+q,timeout=60))
        except Exception as e: print("retry",e); time.sleep(6)
out=[]
for hs in ["2009","2202","2008","0402"]:
  for y in ["2021","2023","2024"]:
    d=get(f"reporterCode={R}&period={y}&cmdCode={hs}&flowCode=M&partnerCode=0,764&customsCode=C00&motCode=0&partner2Code=0")
    rows=[(r['reporterCode'],r['partnerCode'],hs,y,r['primaryValue']) for r in d.get('data',[])]
    out+=rows; print(hs,y,len(rows)); time.sleep(1.5)
json.dump(out,open("imports.json","w"))
