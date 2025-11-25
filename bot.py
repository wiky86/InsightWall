import requests
import feedparser
import json
from datetime import datetime, timedelta

# [수정] SheetDB 제거 -> GAS API 사용
# index.html에 있는 URL과 동일하게 맞춤
GAS_API_URL = "https://script.google.com/macros/s/AKfycbz0gBzAsoQAFl96ZBk6m_hXCHysKr4dksflpXCuvnPD5VK1qiuXdGBUMYUqdGIOVEbJ/exec"

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
    print(f"🚀 [NewsBot-KR] GAS로 뉴스 전송 시작...")
    
    # GAS 웹앱은 보통 CORS 문제나 리다이렉트 때문에 text/plain으로 보내는 게 안전함
    headers = {'Content-Type': 'text/plain; charset=utf-8'}

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

                # [GAS 형식] index.html의 modal-submit과 동일한 키 사용
                payload = {
                    "category": "news",
                    "title": entry.title,
                    "link": entry.link,
                    "comment": f"[{feed_info['source']}] 자동 수집됨",
                    "author": "NewsBot 🤖",
                    "tags": feed_info['tag']
                    # Date는 GAS 스크립트 내부에서 자동 생성됨 (보통)
                }
                
                # GAS로 전송 (POST)
                # GAS는 리다이렉트를 반환하므로 allow_redirects=True (기본값)
                response = requests.post(GAS_API_URL, data=json.dumps(payload), headers=headers)
                
                if response.status_code == 200 or response.status_code == 302:
                    print(f"✅ Sent: {entry.title}")
                else:
                    print(f"❌ Fail ({response.status_code}): {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_post()