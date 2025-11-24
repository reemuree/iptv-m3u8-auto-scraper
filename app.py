import requests
from bs4 import BeautifulSoup
import re
import json

URL = "http://172.16.29.28/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": URL,
    "Origin": "http://172.16.29.28"
}

session = requests.Session()

def clean_channel_name(url):
    """Link থেকে সুন্দর চ্যানেল নাম বানায়"""
    raw = url.split("/")[-1]            # fubosports.m3u8
    raw = raw.replace(".m3u8", "")      # fubosports
    raw = raw.replace("-", " ")         # somoy-tv → somoy tv
    raw = raw.replace("_", " ")         # star_sports → star sports
    raw = re.sub(r'\s+', ' ', raw).strip()
    return raw.title()                  # Fubosports, Somoy Tv, Star Sports 1 Hd

def get_all_m3u8_links():
    all_streams = set()
    
    try:
        print("[+] পেজ লোড করা হচ্ছে...")
        response = session.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print("পেজ লোড করতে সমস্যা হয়েছে:", e)
        return

    m3u8_links = re.findall(r'[(?:"\' )](https?://[^"\']+\.m3u8[^"\']*)[)\'" >]', html)
    for link in m3u8_links:
        all_streams.add(link.strip())

    js_urls = re.findall(r'<script[^>]+src=["\']([^"\']+\.js)["\']', html)
    for js_url in js_urls:
        if not js_url.startswith('http'):
            js_url = URL.rstrip('/') + '/' + js_url.lstrip('/')
        try:
            js_resp = session.get(js_url, headers=headers, timeout=10)
            js_links = re.findall(r'"(https?://[^"]+\.m3u8[^"]*)"', js_resp.text)
            for link in js_links:
                all_streams.add(link)
        except:
            pass

    json_matches = re.findall(r'var\s+\w*playlist\w*\s*=\s*(\[.*?\]);', html, re.DOTALL)
    for match in json_matches:
        try:
            data = json.loads(match)
            for item in data:
                if isinstance(item, dict):
                    url = item.get("file") or item.get("url") or item.get("src")
                    if url and ".m3u8" in url:
                        full_url = url if url.startswith("http") else URL.rstrip("/") + "/" + url.lstrip("/")
                        all_streams.add(full_url)
                elif isinstance(item, str) and ".m3u8" in item:
                    all_streams.add(item)
        except:
            continue

    playlist_urls = re.findall(r'["\'](data/playlists?\.[^"\']+\.json|[^"\']+\.m3u8|[^"\']*playlist[^"\']*\.(json|js))["\']', html, re.IGNORECASE)
    for purl in playlist_urls:
        purl = purl[0]
        if not purl.startswith('http'):
            purl = URL.rstrip('/') + '/' + purl.lstrip('/')
        try:
            resp = session.get(purl, headers=headers, timeout=10)
            if 'json' in purl or resp.headers.get('content-type','').startswith('application/json'):
                data = resp.json()
                def extract_urls(obj):
                    if isinstance(obj, dict):
                        for k,v in obj.items():
                            if isinstance(v, str) and '.m3u8' in v:
                                all_streams.add(v if v.startswith('http') else URL.rstrip('/') + '/' + v.lstrip('/'))
                            elif isinstance(v, (dict,list)):
                                extract_urls(v)
                    elif isinstance(obj, list):
                        for x in obj:
                            extract_urls(x)
                extract_urls(data)
            else:
                links = re.findall(r'(https?://[^\s\'"]+\.m3u8)', resp.text)
                for l in links:
                    all_streams.add(l)
        except:
            pass

    return all_streams


# ==================== মূল কাজ ====================
streams = get_all_m3u8_links()

if not streams:
    print("কোনো m3u8 লিংক পাওয়া যায়নি!")
else:
    print(f"মোট {len(streams)} টি m3u8 লিংক পাওয়া গেছে!")

    with open("iptv_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for link in sorted(streams):
            channel_name = clean_channel_name(link)
            f.write(f"#EXTINF:-1,{channel_name}\n")
            f.write(f"{link}\n")

    print("সেভ হয়েছে → iptv_playlist.m3u")
