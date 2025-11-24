import requests
import feedparser
import json
from datetime import datetime

# [설정] 본인의 GAS 웹 앱 URL을 여기에 넣으세요!
GAS_APP_URL = "https://script.google.com/macros/s/AKfycbz0gBzAsoQAFl96ZBk6m_hXCHysKr4dksflpXCuvnPD5VK1qiuXdGBUMYUqdGIOVEbJ/exec"

# 수집할 RSS 피드 목록
RSS_FEEDS = [
    {
        "source": "Google AI",
        "url": "http://googleaiblog.blogspot.com/atom.xml",
        "tag": "Google, AI, Tech"
    },
    {
        "source": "OpenAI",
        "url": "https://openai.com/blog/rss.xml",
        "tag": "OpenAI, LLM, GPT"
    },
    {
        "source": "MIT Tech Review",
        "url": "https://www.technologyreview.com/feed/",
        "tag": "Trend, News"
    }
]

def fetch_and_post():
    headers = {'Content-Type': 'application/json'}
    
    for feed_info in RSS_FEEDS:
        print(f"Checking {feed_info['source']}...")
        feed = feedparser.parse(feed_info['url'])
        
        # 각 피드에서 최신 글 1개만 가져오기 (중복 방지 로직은 GAS나 여기서 날짜 비교로 처리 가능)
        if feed.entries:
            entry = feed.entries[0] # 가장 최신 글
            
            # 오늘 올라온 글인지 확인 (선택 사항: 여기서는 일단 무조건 보냅니다)
            # 실제 운영 시에는 '어제 이후 작성된 글'만 필터링하는 로직 추가 권장
            
            payload = {
                "category": "news", # 'news' 카테고리로 자동 분류
                "title": entry.title,
                "link": entry.link,
                "tags": feed_info['tag'],
                "comment": f"[{feed_info['source']}] 자동 수집된 최신 아티클입니다.",
                "author": "NewsBot 🤖"
            }
            
            # GAS로 데이터 전송 (POST)
            try:
                response = requests.post(GAS_APP_URL, data=json.dumps(payload), headers=headers)
                print(f"Sent: {entry.title} -> {response.text}")
            except Exception as e:
                print(f"Error sending data: {e}")

if __name__ == "__main__":
    fetch_and_post()