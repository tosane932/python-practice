import feedparser
import pandas as pd
from google import genai
from newspaper import Article, Config
import time

# --- 設定 ---
client = genai.Client(api_key="AIzaSyCdX_bRqKKPwABUqFsfXmO4r7-0SpuKFmA")
RSS_URL = "https://www.nhk.or.jp/rss/news/cat0.xml"

config = Config()
config.browser_user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'
config.request_timeout = 30

def get_ai_summary(text):
    if not text or len(text) < 50:
        return f"本文不足({len(text)}文字)"
    
    try:
        # 文字列を明示的に整形し、エンコードエラーを回避
        target_text = str(text[:2000])
        prompt = f"以下のニュースを3行で日本語で要約してください。\n\n{target_text}"
        
        # contentsに直接文字列を渡す
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        # エラーが出た場合、その内容を表示
        return f"AI要約エラー（詳細）: {str(e)}"

# --- 実行 ---
print("日本語エンコードを修正し、NHKニュースの要約を開始します...")
feed = feedparser.parse(RSS_URL)

if not feed.entries:
    print("RSSの取得に失敗しました。")
else:
    results = []
    for entry in feed.entries[:3]:
        print(f"解析中: {entry.title[:15]}...")
        try:
            article = Article(entry.link, config=config)
            article.download()
            article.parse()
            summary = get_ai_summary(article.text)
        except Exception as e:
            summary = f"取得失敗: {str(e)}"
        
        results.append({
            "タイトル": entry.title,
            "AI要約": summary,
            "URL": entry.link
        })
        time.sleep(3)

    df = pd.DataFrame(results)
    df.to_excel("nhk_final_test.xlsx", index=False)
    print("\n工程完了。Excelに『AIの言葉』が刻まれているか確認してください。")