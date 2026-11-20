"""Best-effort market snapshots. Missing observations remain null, never guessed."""
import json, os, urllib.request, urllib.parse, datetime, xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'briefings.json'
KST=ZoneInfo('Asia/Seoul')
TODAY=datetime.datetime.now(KST).date().isoformat()
WATCH=[('KODEX 미국AI소프트웨어TOP10','KR',''),('TIGER 미국S&P500','KR','360750.KS'),('KODEX 미국S&P500','KR','379800.KS'),('KODEX 미국나스닥100','KR','379810.KS'),('KODEX 미국반도체','KR',''),('KODEX 미국AI전력핵심인프라','KR',''),('TIGER 미국필라델피아반도체나스닥','KR','381180.KS'),('QQQ','US','QQQ'),('SCHD','US','SCHD'),('VIG','US','VIG')]
# Empty symbols deliberately require manual official-issuer ticker confirmation.
INDEX=[('S&P 500','^GSPC'),('Nasdaq','^IXIC'),('SOX','^SOX'),('US 10Y yield','^TNX'),('USD/KRW','KRW=X')]
UA={'User-Agent':'Mozilla/5.0 ETFStudyDashboard/1.0','Accept':'application/json'}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=18) as r:return r.read()
def quote(symbol):
    if not symbol:return {'status':'symbol_unverified','price':None,'change_pct':None}
    try:
        url='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(symbol,safe='')+'?range=10d&interval=1d'
        j=json.loads(get(url))['chart']['result'][0]
        arr=[(t,v) for t,v in zip(j.get('timestamp',[]),j['indicators']['quote'][0]['close']) if v is not None]
        if len(arr)<2:raise ValueError('fewer than two closes')
        (t0,p0),(t1,p1)=arr[-2:]
        return {'status':'unofficial_yahoo_daily','price':round(p1,4),'change_pct':round((p1/p0-1)*100,3),'asof':datetime.datetime.fromtimestamp(t1,datetime.timezone.utc).date().isoformat(),'source_url':'https://finance.yahoo.com/quote/'+urllib.parse.quote(symbol,safe='')+'/history/'}
    except Exception as e:return {'status':'unavailable','price':None,'change_pct':None,'error':str(e)[:100]}
def headlines():
    # Headlines are context, not proof of causation. Links point to Google News RSS article pages.
    q=urllib.parse.quote('AI semiconductor NVIDIA data center finance when:2d')
    try:
        root=ET.fromstring(get('https://news.google.com/rss/search?q='+q+'&hl=en-US&gl=US&ceid=US:en'))
        result=[]
        for x in root.findall('./channel/item')[:5]:
            title=x.findtext('title','').strip();link=x.findtext('link','').strip();date=x.findtext('pubDate','').strip()
            if title and link:result.append({'title':title,'url':link,'published':date})
        return result
    except Exception:return []
def main():
    try:old=json.loads(OUT.read_text(encoding='utf-8'))
    except (FileNotFoundError,ValueError):old=[]
    etfs=[{'name':n,'market':m,'symbol':s or None,**quote(s)} for n,m,s in WATCH]
    indices=[{'name':n,'symbol':s,**quote(s)} for n,s in INDEX]
    verified=sum(x['price'] is not None for x in etfs)
    entry={'date':TODAY,'title':f'{TODAY} ETF 시장 점검','summary':f'ETF {len(etfs)}종 중 {verified}종의 비공식 일별 시세 확인. 미확인 수치는 표시하지 않습니다. 뉴스 헤드라인은 검증된 인과관계가 아닙니다.','topics':['ETF','금리','환율','AI','반도체'],'study':'오늘의 개념: 서로 다른 시장의 종가와 환율 기준시각이 다르면 ETF 수익률을 직접 비교하면 안 됩니다.','sourceStatus':'Yahoo Finance 비공식 차트 API·Google News RSS. 지연·누락 가능. 투자판단 전 거래소/운용사 확인 필요.','etfs':etfs,'indices':indices,'news':headlines(),'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    bydate={x['date']:x for x in old if isinstance(x,dict) and 'date' in x}
    bydate[TODAY]=entry
    OUT.write_text(json.dumps(sorted(bydate.values(),key=lambda x:x['date'],reverse=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{TODAY}: {verified}/10 ETF prices; {len(entry["news"])} headlines; saved {OUT}')
if __name__=='__main__':main()
