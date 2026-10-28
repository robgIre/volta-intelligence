"""Public FRED CSV risk series; no API key. No synthetic readings."""
import csv,datetime as dt,io,json,urllib.request
from pathlib import Path
SERIES={'BAMLH0A0HYM2':('US high-yield option-adjusted spread','percentage points'),'BAMLC0A0CM':('US investment-grade option-adjusted spread','percentage points'),'DGS10':('US 10-year Treasury yield','percent'),'VIXCLS':('VIX volatility index','index points')}
rows=[]
for sid,(label,unit) in SERIES.items():
 try:
  url='https://fred.stlouisfed.org/graph/fredgraph.csv?id='+sid
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 VoltaPublicIntelligence/1.0'})
  with urllib.request.urlopen(req,timeout=15) as r: raw=r.read(500000).decode('utf-8-sig')
  vals=[]
  for row in csv.DictReader(io.StringIO(raw)):
   try: vals.append((row.get('DATE') or row.get('observation_date'),float(row[sid])))
   except (ValueError,TypeError,KeyError): pass
  if vals:
   day,val=vals[-1];prev=vals[-6][1] if len(vals)>=6 else None
   rows.append({'id':sid,'label':label,'unit':unit,'value':round(val,3),'asOf':day,'change5Observations':round(val-prev,3) if prev is not None else None,'source':'Federal Reserve Bank of St. Louis (FRED)','url':'https://fred.stlouisfed.org/series/'+sid})
  print('OK',sid)
 except Exception as e: print('WARN',sid,str(e)[:150])
p=Path(__file__).parent/'data/risk.json';p.write_text(json.dumps({'updated':dt.datetime.now(dt.timezone.utc).isoformat(),'indicators':rows},indent=2)+'\n')
