import pandas as pd
import os
import time
from google import genai
from newspaper import Article, Config
from googlenewsdecoder import decoderv1 # 新しいURL解読器

# --- 設定：APIキー ---
client = genai.Client(api_key="あなたのAPIキー")

# ブラウザのふりをする設定
config = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

def get_ai_summary(text):
    if not text or len(text) < 50: # 50文字以下は流石に中身がないと判断
        return f"本文取得失敗（現在 {len(text)} 文字）。サイト側で強固なブロックがかかっています。"
    
    try:
        prompt = f"以下の記事を読み、要点を3行でまとめてください。\n\n【本文】:\n{text[:2000]}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI要約エラー: {e}"

# --- メイン処理 ---
input_file = "ai_summary_news.xlsx"
output_file = "final_report_v3.xlsx"

if not os.path.exists(input_file):
    print("エラー：元ファイルが見つかりません。")
else:
    df = pd.read_excel(input_file)
    summaries = []

    print("Googleニュースの暗号URLを解読しながら、潜入を開始します...")

    for index, row in df.iterrows():
        google_url = row['URL']
        print(f"[{index+1}/{len(df)}] 解析中: {str(row.get('タイトル', '無題'))[:15]}...")
        
        try:
            # 1. GoogleのURLを「真のURL」にデコード
            decoded_res = decoderv1(google_url)
            if decoded_res.get('status'):
                real_url = decoded_res['decoded_url']
            else:
                real_url = google_url # 失敗したらそのまま

            # 2. 真のURLにアクセスして本文取得
            article = Article(real_url, config=config)
            article.download()
            article.parse()
            
            # 3. AIに要約を依頼
            summary = get_ai_summary(article.text)
            summaries.append(summary)
            
        except Exception as e:
            summaries.append(f"読み込み失敗: {e}")
        
        time.sleep(3) # 連続アクセスでブロックされないよう慎重に

    df['AI真の要約'] = summaries
    df.to_excel(output_file, index=False)
    print(f"\n完了！ '{output_file}' を確認してください。")