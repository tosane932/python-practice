import pandas as pd
import os
import time
from google import genai
from newspaper import Article, Config
from googlenewsdecoder import decoderv1

# --- 設定：APIキー ---
client = genai.Client(api_key="あなたのAPIキー")

# ブラウザのふりをする設定
config = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
config.request_timeout = 20 # タイムアウトを少し長めに

def get_ai_summary(text):
    if not text or len(text) < 50:
        return f"本文取得失敗（現在 {len(text)} 文字）。サイト側で強固なブロックがかかっています。"
    
    try:
        prompt = f"以下の記事を読み、要点を3行でまとめてください。ニュース価値のない定型文などは無視してください。\n\n【本文】:\n{text[:2500]}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI要約エラー: {e}"

# --- メイン処理 ---
input_file = "ai_summary_news.xlsx"
output_file = "final_report_v4.xlsx"

if not os.path.exists(input_file):
    print("エラー：元ファイルが見つかりません。")
else:
    df = pd.read_excel(input_file)
    summaries = []

    print("GoogleニュースのURLをデコードして、記事本体に直接アプローチします...")

    for index, row in df.iterrows():
        google_url = row['URL']
        print(f"[{index+1}/{len(df)}] 潜入中: {str(row.get('タイトル', '無題'))[:15]}...")
        
        try:
            # 1. URLをデコード（文字列として受け取る）
            # もし辞書で返ってきても文字列で返ってきても対応できる書き方に変更
            decoded_res = decoderv1(google_url)
            
            if isinstance(decoded_res, dict):
                real_url = decoded_res.get('decoded_url', google_url)
            else:
                real_url = str(decoded_res) # 直接文字列が返ってきた場合

            # 2. 本文取得
            article = Article(real_url, config=config)
            article.download()
            article.parse()
            
            # 3. AIに要約を依頼
            summary = get_ai_summary(article.text)
            summaries.append(summary)
            
        except Exception as e:
            summaries.append(f"処理エラー: {e}")
        
        time.sleep(3) # 連続アクセス回避

    df['AI真の要約'] = summaries
    df.to_excel(output_file, index=False)
    print(f"\n完了！ '{output_file}' を確認してください。")