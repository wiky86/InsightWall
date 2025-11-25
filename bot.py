import requests
import feedparser
import json
from datetime import datetime, timedelta

# [수정] SheetDB 제거 -> GAS API 사용
# index.html에 있는 URL과 동일하게 맞춤
GAS_API_URL = "https://script.google.com/macros/s/AKfycbz0gBzAsoQAFl96ZBk6m_hXCHysKr4dksflpXCuvnPD5VK1qiuXdGBUMYUqdGIOVEbJ/exec"

RSS_FEEDS = [
    {'url': 'https://news.google.com/rss/search?q=AI+Artificial+Intelligence&hl=ko&gl=KR&ceid=KR:ko', 'source': 'Google News (AI)', 'tag': 'AI, Tech', 'category': 'news'},
    {'url': 'http://www.aitimes.com/rss/all.xml', 'source': 'AI Times', 'tag': 'AI, Industry', 'category': 'news'},
    {'url': 'https://geeknews.geeknews.io/rss', 'source': 'GeekNews', 'tag': 'Tech, Dev', 'category': 'news'},
    {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCQNE2JmbasNYbjGAcuBiRRg', 'source': '조코딩 JoCoding', 'tag': 'AI, Dev, Video', 'category': 'youtube'},
    {'url': 'https://news.google.com/rss/search?q=AI+논문+OR+AI+보고서+OR+AI+트렌드&hl=ko&gl=KR&ceid=KR:ko', 'source': 'Google News (Paper/Report)', 'tag': 'AI, Paper, Report', 'category': 'paper'},
]

def fetch_and_post():
    print(f"🚀 [NewsBot-KR] GAS로 데이터 전송 시작...")
    
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

                # [GAS 형식] doPost가 기대하는 JSON 구조
                payload = {
                    "category": feed_info.get('category', 'news'),
                    "title": entry.title,
                    "link": entry.link,
                    "comment": f"[{feed_info['source']}] 자동 수집",
                    "author": "NewsBot 🤖",
                    "tags": feed_info['tag']
                }
                
                # GAS로 전송 (POST)
                # json=payload 대신 data=json.dumps(payload) 사용 (text/plain 처리)
                response = requests.post(GAS_API_URL, data=json.dumps(payload), headers=headers)
                
                if response.status_code == 200 or response.status_code == 201:
                    print(f"✅ Sent: {entry.title}")
                else:
                    print(f"❌ Fail: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_post()