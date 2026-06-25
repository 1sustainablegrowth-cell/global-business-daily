import json
import feedparser
from datetime import datetime
from email_sender import send_email
from config import GEMINI_API_KEY
import requests

# ========== 读取RSS源 ==========
def load_sources():
    with open("rss_sources.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ========== 抓取RSS ==========
def fetch_rss(url):
    try:
        feed = feedparser.parse(url)
        entries = []
        for entry in feed.entries[:5]:
            entries.append({
                "title": entry.title,
                "summary": getattr(entry, "summary", ""),
                "link": entry.link
            })
        return entries
    except:
        return []

# ========== 汇总数据 ==========
def collect_data():
    sources = load_sources()
    all_data = []

    for category, urls in sources.items():
        for url in urls:
            items = fetch_rss(url)
            for item in items:
                item["category"] = category
                all_data.append(item)

    return all_data

# ========== 调用Gemini ==========
def summarize_with_gemini(data):
    prompt = open("prompt.txt", "r", encoding="utf-8").read()

    content = json.dumps(data, ensure_ascii=False)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt + "\n\n数据如下：\n" + content
            }]
        }]
    }

    res = requests.post(url, json=payload)
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

# ========== 主流程 ==========
def main():
    data = collect_data()
    report = summarize_with_gemini(data)

    today = datetime.now().strftime("%Y-%m-%d")

    send_email(
        subject=f"全球商业创新情报日报 | {today}",
        content=report
    )

if __name__ == "__main__":
    main()
