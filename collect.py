"""Collect public RSS/Atom articles with stdlib only; no API key required."""
import datetime as dt, email.utils, hashlib, html, json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).parent
QUERIES={
 'Volta & Partners':'Volta AI infrastructure Fortum Anthropic partnership',
 'Customers & Offtake':'Anthropic OpenAI AI infrastructure capacity offtake contract',
 'Competitors':'CoreWeave Nebius Nscale Lambda Fluidstack Crusoe Applied Digital',
 'Supply Chain & Technology':'NVIDIA AMD Broadcom Dell Supermicro HBM AI server supply',
 'Power Land & Construction':'data center grid connection transformer land permits construction',
 'Bond Markets & Credit':'AI data center high yield bond credit spreads CDS financing',
 'AI Bubble & Stability':'AI infrastructure circular financing debt GPU rental prices cash burn',
 'Real World AI Returns':'enterprise AI productivity return on investment operating profit EBIT',
 'Delivery & Commissioning':'hyperscale data center commissioning rack deployment network turn up',
 'AI Research & Technology':'AI inference efficiency frontier models custom silicon TPU',
 'Policy & Geopolitics':'AI data center export controls energy regulation tariffs permitting',
 'Executive Signals':'AI data center acquisition bankruptcy executive appointment litigation'
}
PODCASTS={
 'Latent Space':'https://www.latent.space/feed',
 'Practical AI':'https://feeds.transistor.fm/practical-ai-machine-learning-data-science',
 'The Cognitive Revolution':'https://feeds.megaphone.fm/THC7723012857'
}
KEYWORDS={'anthropic':24,'volta':30,'openai':18,'coreweave':16,'power':9,'grid':10,'commissioning':14,'transformer':12,'liquid cooling':12,'nvidia':10,'data center':12,'datacenter':12,'financing':12,'capacity':8,'construction':8,'delay':10,'debt':8}
def txt(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',s or ''))).strip()[:450]
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'VoltaPublicIntelligence/1.0 (RSS reader)'})
 with urllib.request.urlopen(req,timeout=18) as r:return r.read(1500000)
def children(node,name):return node.findall(name)
def val(node,*names):
 for name in names:
  el=node.find(name)
  if el is not None and el.text:return el.text.strip()
 return ''
def parse(xml):
 root=ET.fromstring(xml);items=root.findall('.//item') or root.findall('{http://www.w3.org/2005/Atom}entry');out=[]
 for it in items:
  title=val(it,'title','{http://www.w3.org/2005/Atom}title');link=val(it,'link');
  if not link:
   e=it.find('{http://www.w3.org/2005/Atom}link');link=e.get('href','') if e is not None else ''
  rawdate=val(it,'pubDate','{http://www.w3.org/2005/Atom}published','{http://www.w3.org/2005/Atom}updated')
  try:published=email.utils.parsedate_to_datetime(rawdate).astimezone(dt.timezone.utc).isoformat()
  except Exception:
   try:published=dt.datetime.fromisoformat(rawdate.replace('Z','+00:00')).isoformat()
   except Exception:published=dt.datetime.now(dt.timezone.utc).isoformat()
  if title and link:out.append(dict(title=txt(title),url=link,published=published,summary=txt(val(it,'description','{http://www.w3.org/2005/Atom}summary'))))
 return out
def main():
 p=ROOT/'data/feed.json';old=json.loads(p.read_text()) if p.exists() else {};stories={x['id']:x for x in old.get('stories',[]) if 'id' in x};podcasts={x['id']:x for x in old.get('podcasts',[]) if 'id' in x};now=dt.datetime.now(dt.timezone.utc)
 for cat,q in QUERIES.items():
  url='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q+' when:7d','hl':'en-GB','gl':'GB','ceid':'GB:en'})
  try:
   for x in parse(fetch(url)):
    key=hashlib.sha256(x['title'].lower().encode()).hexdigest()[:20];score=min(100,20+sum(v for k,v in KEYWORDS.items() if k in (x['title']+' '+x['summary']).lower()));x.update(id=key,category=cat,source='Google News RSS',score=score);stories[key]=x
   print('OK',cat)
  except Exception as e:print('WARN',cat,str(e))
 for source,url in PODCASTS.items():
  try:
   for x in parse(fetch(url))[:15]:
    key=hashlib.sha256(x['url'].encode()).hexdigest()[:20];x.update(id=key,source=source);podcasts[key]=x
   print('OK podcast',source)
  except Exception as e:print('WARN podcast',source,str(e))
 def recent(x,days):
  try:return dt.datetime.fromisoformat(x['published'].replace('Z','+00:00'))>now-dt.timedelta(days=days)
  except:return False
 out={'updated':now.isoformat(),'stories':sorted((x for x in stories.values() if recent(x,30)),key=lambda x:x['published'],reverse=True)[:1000],'podcasts':sorted((x for x in podcasts.values() if recent(x,90)),key=lambda x:x['published'],reverse=True)[:100]};p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(len(out['stories']),'stories',len(out['podcasts']),'episodes')
if __name__=='__main__':main()
