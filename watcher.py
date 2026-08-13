import os, json, hashlib, re
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

K=json.load(open("config.json",encoding="utf-8"))
SOURCES=[
("柏市","rss","https://www.city.kashiwa.lg.jp/shinchaku/shimin.xml"),
("流山市","rss","https://www.city.nagareyama.chiba.jp/news.rss"),
("取手市","html","https://www.city.toride.ibaraki.jp/"),
("常磐線（JR東日本）","html","https://traininfo.jreast.co.jp/train_info/line.aspx?gid=1&lineid=jobanline")
]
STATE="state.json"

def get(u):
    return urlopen(Request(u,headers={"User-Agent":"OhagiDisasterWatch/1.0"}),timeout=20).read()

def plain(b):
    s=b.decode("utf-8","ignore")
    s=re.sub(r"<script.*?</script>"," ",s,flags=re.S|re.I)
    s=re.sub(r"<style.*?</style>"," ",s,flags=re.S|re.I)
    s=re.sub(r"<[^>]+>"," ",s)
    return re.sub(r"\s+"," ",s).strip()

def level(text,src):
    if any(x.lower() in text.lower() for x in K["urgent"]): return "🔴 緊急"
    if src.startswith("常磐線") and any(x.lower() in text.lower() for x in K["transport"]): return "🔵 交通"
    if any(x.lower() in text.lower() for x in K["warning"]): return "🟠 警戒"
    return None

def send(msg):
    token=os.getenv("TELEGRAM_BOT_TOKEN"); chat=os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat: print("Telegram secrets未設定"); return
    import urllib.parse
    u=f"https://api.telegram.org/bot{token}/sendMessage"
    d=urllib.parse.urlencode({"chat_id":chat,"text":msg,"disable_web_page_preview":"true"}).encode()
    urlopen(Request(u,data=d),timeout=20).read()

try: state=json.load(open(STATE,encoding="utf-8"))
except: state={"seen":[]}

for name,typ,url in SOURCES:
    try:
        data=get(url)
        if typ=="rss":
            root=ET.fromstring(data)
            items=root.findall(".//item")
            for it in items:
                title=it.findtext("title",""); link=it.findtext("link",""); desc=it.findtext("description","")
                txt=f"{title} {desc}"; lv=level(txt,name)
                if not lv: continue
                fp=hashlib.sha256(f"{name}|{title}|{link}".encode()).hexdigest()
                if fp in state["seen"]: continue
                send(f"{lv}【おはぎ防災ウォッチ】\n{name}\n{title}\n{link}")
                state["seen"].append(fp)
        else:
            txt=plain(data)
            lv=level(txt,name)
            if lv:
                # 試作版ではページ内容のハッシュで重複を抑制
                fp=hashlib.sha256(f"{name}|{txt[:30000]}".encode()).hexdigest()
                if fp not in state["seen"]:
                    send(f"{lv}【おはぎ防災ウォッチ】\n{name}\n公式ページに重要キーワードを検出しました。\n{url}")
                    state["seen"].append(fp)
    except Exception as e:
        print(name,e)

state["seen"]=state["seen"][-500:]
json.dump(state,open(STATE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(datetime.now(timezone.utc).isoformat(),"checked")
