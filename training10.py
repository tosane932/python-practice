import pandas as pd
import os
import time
import google.generativeai as genai
from newspaper import Article

# --- 設定：Gemini APIキーをここに貼り付け ---
GOOGLE_API_KEY = "AIzaSyCdX_bRqKKPwABUqFsfXmO4r7-0SpuKFmA"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_summary(text):
    if not text or len(text) < 100:
        return "本文が短すぎるため要約をスキップしました。"
    
    prompt = f"""
    以下のニュース記事の本文を読み、要点を3行で簡潔にまとめてください。
    
    【本文】:
    {text[:2000]}  # 2000文字程度をAIに送る
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI要約エラー: {e}"

# --- メイン処理（training9の結果を読み込む） ---
input_file = "ai_summary_news.xlsx"
output_file = "final_report.xlsx"

if not os.path.exists(input_file):
    print(f"エラー：{input_file} が見つかりません。training9を先に実行してください。")
else:
    df = pd.read_excel(input_file)
    summaries = []

    print("AIによる要約作業を開始します（これには少し時間がかかります）...")

    for index, row in df.iterrows():
        url = row['URL']
        print(f"[{index+1}/{len(df)}] 記事を熟読中: {row['タイトル'][:20]}...")
        
        try:
            # 改めて本文を全力で取得
            article = Article(url)
            article.download()
            article.parse()
            
            # AIに要約を依頼
            summary = get_ai_summary(article.text)
            summaries.append(summary)
        except:
            summaries.append("記事の読み込みに失敗しました。")
        
        # APIの制限に配慮して少し待機
        time.sleep(2)

    # 新しい列として「AI要約」を追加
    df['AI真の要約'] = summaries
    df.to_excel(output_file, index=False)
    print(f"\n全ての工程が完了しました！ '{output_file}' を確認してください。")