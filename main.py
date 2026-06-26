import json
import feedparser
from datetime import datetime
from email_sender import send_email
from config import GEMINI_API_KEY
import requests
import sys

# ========== 读取RSS源 ==========
def load_sources():
    with open("rss_sources.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ========== 抓取RSS ==========
def fetch_rss(url):
    print(f"读取RSS：{url}")

    try:
        feed = feedparser.parse(url)

        entries = []

        for entry in feed.entries[:5]:
            entries.append({
                "title": entry.title,
                "summary": getattr(entry, "summary", ""),
                "link": entry.link
            })

        print(f"成功获取 {len(entries)} 条")

        return entries

    except Exception as e:
        print("RSS错误：", e)
        return []

# ========== 汇总 ==========
def collect_data():
    sources = load_sources()

    all_data = []

    for category, urls in sources.items():
        print(f"\n开始分类：{category}")

        for url in urls:
            items = fetch_rss(url)

            for item in items:
                item["category"] = category
                all_data.append(item)

    print(f"\n总共收集：{len(all_data)} 条新闻")

    return all_data

# ========== Gemini ==========
def summarize_with_gemini(data):

    print("开始调用 Gemini...")

    prompt = open(
        "prompt.txt",
        "r",
        encoding="utf-8"
    ).read()

    content = json.dumps(
        data,
        ensure_ascii=False
    )

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-1.5-flash:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt + "\n\n数据如下：\n" + content
            }]
        }]
    }

    try:
        res = requests.post(
            url,
            json=payload,
            timeout=60
        )

        print("Gemini状态码：", res.status_code)

        res.raise_for_status()

        result = res.json()

        print("Gemini调用成功")

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("Gemini错误：")
        print(e)

        if 'res' in locals():
            print(res.text)

        sys.exit(1)

# ========== 主流程 ==========
def main():

    print("========== 开始 ==========")

    data = collect_data()

    print("RSS完成")

    report = summarize_with_gemini(data)

    print("开始发送邮件...")

    today = datetime.now().strftime("%Y-%m-%d")

    send_email(
        subject=f"全球商业创新情报日报 | {today}",
        content=report
    )

    print("邮件发送完成")

    print("========== 全部完成 ==========")

if __name__ == "__main__":
    main()
