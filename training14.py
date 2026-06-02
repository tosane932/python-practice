import pandas as pd
import os
import time
from google import genai
from newspaper import Article, Config
from googlenewsdecoder import decoderv1

# --- 設定：APIキー ---
client = genai.Client(api_key="あなたのAPIキー")

config = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
config.request_timeout = 20

def get_ai_summary(text):
    if not text or len(text) < 50:
        return f"本文取得失敗（現在 {len(text)} 文字）。サイト側の保護が強力です。"
    try:
        prompt = f"以下の記事を読み、要点を3行でまとめてください。\n\n【本文】:\n{text[:2500]}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI要約エラー: {e}"

# --- メイン処理 ---
input_file = "ai_summary_news.xlsx"
output_file = "final_report_v5.xlsx"

if not os.path.exists(input_file):
    print("エラー：元ファイルが見つかりません。")
else:
    df = pd.read_excel(input_file)
    summaries = []

    print("最終防衛ライン：URL修復モードで再解析を開始します...")

    for index, row in df.iterrows():
        google_url = row['URL']
        print(f"[{index+1}/{len(df)}] 解析中: {str(row.get('タイトル', '無題'))[:15]}...")
        
        try:
            # 1. URLの解読
            decoded_res = decoderv1(google_url)
            real_url = str(decoded_res.get('decoded_url')) if isinstance(decoded_res, dict) else str(decoded_res)

            # --- URL修復ロジック ---
            if real_url.startswith(':/'):
                real_url = 'https' + real_url
            elif not real_url.startswith('http'):
                # 明らかにURLとしておかしい場合は、元のGoogleニュースURLを試す
                real_url = google_url

            # 2. 記事の読み込み
            article = Article(real_url, config=config)
            article.download()
            article.parse()
            
            # 3. 要約
            summary = get_ai_summary(article.text)
            summaries.append(summary)
            
        except Exception as e:
            summaries.append(f"スキップ（解析不能）: {e}")
        
        time.sleep(3)

    df['AI真の要約'] = summaries
    df.to_excel(output_file, index=False)
    print(f"\n完了！ '{output_file}' を確認してください。")