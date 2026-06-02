import pandas as pd
import os
import time
from google import genai
from newspaper import Article, Config # Configを追加

# --- 設定：APIキー ---
client = genai.Client(api_key="あなたのAPIキー")

# ブラウザのふりをするための設定
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 15

def get_ai_summary(text):
    # 判定を100文字から30文字に緩和
    if not text or len(text) < 30:
        return f"取得できた文字が少なすぎます（{len(text)}文字）。サイトの保護によりブロックされた可能性があります。"
    
    try:
        prompt = f"以下のニュース記事を読み、要点を3行で簡潔にまとめてください。ニュース価値のない定型文などは無視してください。\n\n【本文】:\n{text[:2500]}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"AI要約エラー: {e}"

# --- メイン処理 ---
input_file = "ai_summary_news.xlsx"
output_file = "final_report_v2.xlsx"

if not os.path.exists(input_file):
    print("エラー：元ファイルが見つかりません。")
else:
    df = pd.read_excel(input_file)
    summaries = []

    print("AIによる『壁突破』要約作業を開始します...")

    for index, row in df.iterrows():
        url = row['URL']
        print(f"[{index+1}/{len(df)}] 潜入開始: {str(row.get('タイトル', '無題'))[:20]}...")
        
        try:
            # config（ブラウザのふり）を適用してダウンロード
            article = Article(url, config=config)
            article.download()
            article.parse()
            
            # 要約実行
            summary = get_ai_summary(article.text)
            summaries.append(summary)
        except Exception as e:
            summaries.append(f"読み込み失敗: {e}")
        
        time.sleep(3) # 相手を驚かせないよう少し長めに休憩

    df['AI真の要約'] = summaries
    df.to_excel(output_file, index=False)
    print(f"\n完了！ '{output_file}' を確認してください。")