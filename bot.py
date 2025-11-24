import requests
import feedparser
import json
from datetime import datetime, timedelta

# [중요] 본인의 GAS 웹 앱 URL 확인!
GAS_APP_URL = "https://script.google.com/macros/s/AKfycbz0gBzAsoQAFl96ZBk6m_hXCHysKr4dksflpXCuvnPD5VK1qiuXdGBUMYUqdGIOVEbJ/exec"

# 한국 AI/IT 뉴스 소스 (엄선함)
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
    headers = {'Content-Type': 'application/json'}
    print(f"🚀 [NewsBot-KR] 한국 뉴스 수집 시작...")

    for feed_info in RSS_FEEDS:
        print(f"Checking {feed_info['source']}...")
        try:
            feed = feedparser.parse(feed_info['url'])
            
            # 각 소스에서 최신 글 2개씩만 가져오기 (도배 방지)
            for entry in feed.entries[:2]:
                
                # [필터링] 오늘/어제 글만 가져오기 (너무 옛날 글 제외)
                # published_parsed가 있는 경우만 체크
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - pub_date > timedelta(hours=48):
                        continue # 48시간 지난 뉴스는 패스

                payload = {
                    "category": "news", 
                    "title": entry.title,
                    "link": entry.link,
                    "tags": feed_info['tag'],
                    "comment": f"[{feed_info['source']}] 자동 수집 뉴스",
                    "author": "NewsBot 🤖"
                }
                
                # GAS로 전송
                response = requests.post(GAS_APP_URL, json=payload)
                print(f"✅ Sent: {entry.title}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_post()