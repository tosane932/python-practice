import pandas as pd
from newspaper import Article
from google import genai
import requests

# ==========================================
# 【設定項目】
# ==========================================
API_KEY = "AIzaSyCPa99NFSFXNweExQWl_F48AbazQ0mGgXQ"
EXCEL_FILE = "google_research_history.xlsx"
# ==========================================

client = genai.Client(api_key=API_KEY)

def summarize_first_article():
    print(f"Excelファイル '{EXCEL_FILE}' を読み込んでいます...")
    
    try:
        df = pd.read_excel(EXCEL_FILE)
        target_url = df.iloc[0, 4] 
        print(f"対象URL: {target_url}")

        # 1. ニュース記事の本文を抽出
        print("\n記事の内容を抽出中...")
        article = Article(target_url, language='ja')
        article.download()
        article.parse()
        
        # 本文が取れなかった場合の特別対応
        content = article.text
        if not content:
            print("警告: 本文の直接抽出に失敗しました。URLから直接要約を試みます。")
            content = f"記事のURL: {target_url}\n(本文の直接取得に失敗したため、このリンク先の内容を推測または参照して要約してください)"

        # 2. Geminiに要約を依頼
        print("Geminiに要約を依頼しています...")
        prompt = f"以下のニュース記事について、3行の箇条書きで要約してください。日本語で出力してください。\n\n{content}"
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        # 3. 結果表示
        print("\n" + "="*50)
        print(f"【元記事タイトル】: {article.title if article.title else 'タイトル不明'}")
        print("-" * 50)
        print("【AIによる要約結果】:")
        print(response.text)
        print("="*50)
        print("\n成功しました！")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    summarize_first_article()