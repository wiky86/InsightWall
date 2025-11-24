import requests
import feedparser
import json
from datetime import datetime, timedelta

# [수정] 멍청한 GAS 대신 똑똑한 SheetDB 주소 사용
# 사용자님이 주신 SheetDB API URL입니다.
SHEET_DB_URL = "https://sheetdb.io/api/v1/d11klu94k8ypq"

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
    print(f"🚀 [NewsBot-KR] SheetDB로 뉴스 전송 시작...")
    
    headers = {'Content-Type': 'application/json'}

    for feed_info in RSS_FEEDS:
        print(f"Checking {feed_info['source']}...")
        try:
            feed = feedparser.parse(feed_info['url'])
            
            for entry in feed.entries[:2]:
                # 48시간 이내 글만 필터링
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - pub_date > timedelta(hours=48):
                        continue

                # [SheetDB 형식] "data" 키 안에 배열로 넣거나, 그냥 객체로 보내도 됨
                # 시트의 헤더 이름(Date, Category, Title...)과 정확히 일치해야 합니다.
                payload = {
                    "data": [
                        {
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Category": "news",
                            "Title": entry.title,
                            "Link": entry.link,
                            "Comment": f"[{feed_info['source']}] 자동 수집",
                            "Author": "NewsBot 🤖",
                            "Tags": feed_info['tag']
                        }
                    ]
                }
                
                # SheetDB로 전송 (POST)
                response = requests.post(SHEET_DB_URL, json=payload, headers=headers)
                
                if response.status_code == 201 or response.status_code == 200:
                    print(f"✅ Sent: {entry.title}")
                else:
                    print(f"❌ Fail: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_post()