# IPTV M3U8 Auto Scraper

Automatically scans any IPTV webpage and extracts **all .m3u8 streaming links** (from HTML, JS, JSON, hidden playlist sources, AJAX calls, etc.) and generates a clean **M3U playlist file**.

✔ Auto channel name detection  
✔ Extracts direct m3u8 links from HTML  
✔ Extracts from JavaScript files  
✔ Extracts from JSON playlists  
✔ Auto cleans, formats and builds final iptv_playlist.m3u  
✔ Works with private LAN IPTV servers (172.x / 192.x / 10.x)  

---

## 🚀 Features

- Detects **all m3u8 links** from a given URL  
- Converts filename → **Clean Channel Name**  
  - Example:  
    - `fubosports.m3u8 → Fubosports`  
    - `star_sports_1_hd.m3u8 → Star Sports 1 HD`  
- Creates a proper **M3U file** compatible with:
  - VLC Player  
  - Kodi  
  - Tivimate  
  - GSE IPTV  
  - OTT Navigator  
  - Smart IPTV  

---

## 📌 How to Use

1. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
