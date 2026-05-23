import feedparser # RSS読み込み用の軽い道具
import pandas as pd
from google import genai
from newspaper import Article, Config
import time

# --- 設定 ---
client = genai.Client(api_key="AIzaSyCdX_bRqKKPwABUqFsfXmO4r7-0SpuKFmA")
# NHKの主要ニュースRSS
RSS_URL = "https://www.nhk.or.jp/rss/news/cat0.xml"

config = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

def get_ai_summary(text):
    if not text or len(text) < 100:
        return f"本文不足（{len(text)}文字）"
    try:
        prompt = f"以下のニュースを3行で要約してください。\n\n{text[:2000]}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except:
        return "要約エラー"

# --- 実行 ---
print("NHKニュースから直接、情報を抽出中...")
feed = feedparser.parse(RSS_URL)
results = []

for entry in feed.entries[:5]: # まずは最新5件で実験
    print(f"解析中: {entry.title[:20]}...")
    try:
        article = Article(entry.link, config=config)
        article.download()
        article.parse()
        summary = get_ai_summary(article.text)
    except:
        summary = "読み込み失敗"
    
    results.append({
        "タイトル": entry.title,
        "AI要約": summary,
        "URL": entry.link
    })
    time.sleep(2)

df = pd.DataFrame(results)
df.to_excel("nhk_ai_report.xlsx", index=False)
print("\n完了！ 'nhk_ai_report.xlsx' を確認してください。")