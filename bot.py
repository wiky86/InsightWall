import requests
import feedparser
import json
from datetime import datetime, timedelta

# [중요] 본인의 GAS 웹 앱 URL 확인
GAS_APP_URL = "https://script.google.com/macros/s/AKfycbz0gBzAsoQAFl96ZBk6m_hXCHysKr4dksflpXCuvnPD5VK1qiuXdGBUMYUqdGIOVEbJ/exec"

RSS_FEEDS = [
    {
        "source": "Google News (AI)",
        "url": "https://news.google.com/rss/search?q=인공지능+when:1d&hl=ko&gl=KR&ceid=KR:ko",
        "tag": "News, AI"
    },
    {
        "source": "AI Times",
        "url": "http://www.aitimes.com/rss/all.xml",
        "tag": "AI, Industry"
    },
    {
        "source": "GeekNews",
        "url": "http://feeds.feedburner.com/geeknews-feed",
        "tag": "Tech, Dev"
    }
]

def fetch_and_post():
    print(f"🚀 [NewsBot-KR] 한국 뉴스 수집 시작...")
    
    # 헤더 설정 (GAS가 JSON을 잘 받도록)
    headers = {'Content-Type': 'application/json'}

    for feed_info in RSS_FEEDS:
        print(f"Checking {feed_info['source']}...")
        try:
            feed = feedparser.parse(feed_info['url'])
            
            for entry in feed.entries[:2]:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - pub_date > timedelta(hours=48):
                        continue

                # [수정 핵심] 시트 헤더(Row 1)와 대소문자까지 정확히 일치시켜야 함
                payload = {
                    "Date": datetime.now().strftime("%Y-%m-%d"), # 날짜 직접 생성
                    "Category": "news",  # 카테고리 명시
                    "Title": entry.title,
                    "Link": entry.link,
                    "Comment": f"[{feed_info['source']}] 자동 수집",
                    "Author": "NewsBot 🤖",
                    "Tags": feed_info['tag']
                }
                
                # GAS로 전송
                response = requests.post(GAS_APP_URL, json=payload, headers=headers)
                print(f"✅ Sent: {entry.title} -> Code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_post()