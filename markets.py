"""Fetch public market quotes without API credentials. Never fabricate values."""
import datetime as dt, json, urllib.request, urllib.parse, csv, io, time
from pathlib import Path
ROOT=Path(__file__).parent
SYMBOLS={'NVDA':'NVIDIA','AMD':'AMD','AVGO':'Broadcom','MSFT':'Microsoft','AMZN':'Amazon','GOOGL':'Alphabet','CRWV':'CoreWeave','VRT':'Vertiv','SU.PA':'Schneider Electric','DELL':'Dell','ETN':'Eaton','ANET':'Arista Networks'}
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; VoltaIntelligence/1.0)','Accept':'application/json,text/csv,*/*'})
 with urllib.request.urlopen(req,timeout=12) as r:return r.read(500000).decode('utf-8')
def yahoo(symbol):
 url='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(symbol,safe='')+'?interval=1d&range=7d'
 d=json.loads(get(url))['chart']['result'][0]; meta=d['meta'];closes=d['indicators']['quote'][0]['close'];valid=[v for v in closes if isinstance(v,(int,float))]
 if not valid:return None
 price=valid[-1];prev=meta.get('chartPreviousClose') or (valid[-2] if len(valid)>1 else None)
 if len(valid)>1:prev=valid[-2]
 return {'price':round(price,2),'changePercent':round((price/prev-1)*100,2) if prev else None,'currency':meta.get('currency','USD'),'asOf':dt.datetime.fromtimestamp(d['timestamp'][-1],dt.timezone.utc).isoformat(),'provider':'Yahoo Finance public chart (unofficial, delayed)'}
def stooq(symbol):
 if '.' in symbol:return None
 url='https://stooq.com/q/d/l/?s='+urllib.parse.quote(symbol.lower()+'.us')+'&i=d&d1='+(dt.date.today()-dt.timedelta(days=12)).strftime('%Y%m%d')+'&d2='+dt.date.today().strftime('%Y%m%d')
 rows=list(csv.DictReader(io.StringIO(get(url))))
 if not rows:return None
 price=float(rows[-1]['Close']);prev=float(rows[-2]['Close']) if len(rows)>1 else None
 return {'price':round(price,2),'changePercent':round((price/prev-1)*100,2) if prev else None,'currency':'USD','asOf':rows[-1]['Date']+'T21:00:00+00:00','provider':'Stooq daily close (delayed)'}
def main():
 path=ROOT/'data/markets.json';old=json.loads(path.read_text()) if path.exists() else {}; prior={x['symbol']:x for x in old.get('quotes',[])};quotes=[]
 for symbol,name in SYMBOLS.items():
  data=None
  for provider in (yahoo,stooq):
   try:
    data=provider(symbol)
    if data:break
   except Exception as e:print('WARN',symbol,provider.__name__,str(e)[:100])
  if data:quotes.append({'symbol':symbol,'name':name,**data});print('OK',symbol)
  elif symbol in prior:
   quotes.append({**prior[symbol],'stale':True});print('STALE',symbol)
  else:quotes.append({'symbol':symbol,'name':name,'price':None,'changePercent':None,'asOf':None,'provider':None});print('UNAVAILABLE',symbol)
  time.sleep(.15)
 path.write_text(json.dumps({'updated':dt.datetime.now(dt.timezone.utc).isoformat(),'quotes':quotes},indent=2)+'\n')
if __name__=='__main__':main()
