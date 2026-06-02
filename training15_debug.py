import feedparser
import pandas as pd
from google import genai
from newspaper import Article, Config
import time

# --- 設定 ---
client = genai.Client(api_key="あなたのAPIキー")
RSS_URL = "https://www.nhk.or.jp/rss/news/cat0.xml"

config = Config()
# 相手に嫌われないよう、より「本物のブラウザ」に近い設定にします
config.browser_user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'
config.request_timeout = 30

def get_ai_summary(text):
    if not text or len(text) < 50:
        return f"本文不足({len(text)}文字)"
    try:
        prompt = f"以下のニュースを3行で要約してください。\n\n{text[:2000]}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI要約エラー: {e}"

# --- 実行 ---
print("NHKニュースから直接、情報を抽出中...")
feed = feedparser.parse(RSS_URL)

if not feed.entries:
    print("RSSの取得自体に失敗しました。ネット接続かURLを確認してください。")
else:
    results = []
    for entry in feed.entries[:3]: # 慎重に3件だけでテスト
        print(f"解析中: {entry.title[:15]}...")
        try:
            article = Article(entry.link, config=config)
            article.download()
            article.parse()
            summary = get_ai_summary(article.text)
        except Exception as e:
            # ここで「何がダメだったか」を記録する
            summary = f"読み込み失敗の詳細: {e}"
        
        results.append({
            "タイトル": entry.title,
            "AI要約": summary,
            "URL": entry.link
        })
        time.sleep(5) # 5秒待機（相手のサーバーへの敬意）

    df = pd.DataFrame(results)
    df.to_excel("nhk_debug_report.xlsx", index=False)
    print("\n工程完了。Excelを確認してください。")