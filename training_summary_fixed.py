from google import genai
import pandas as pd
from newspaper import Article

# ==========================================
# 【設定項目】
# ==========================================
API_KEY = "AIzaSyCPa99NFSFXNweExQWl_F48AbazQ0mGgXQ"
EXCEL_FILE = "google_research_history.xlsx"

# 最新のクライアント初期化
client = genai.Client(api_key=API_KEY)
# ==========================================

def summarize_first_article():
    print(f"Excel読み込み中: {EXCEL_FILE}")
    
    try:
        df = pd.read_excel(EXCEL_FILE)
        target_url = df.iloc[0, 4] 
        print(f"対象URL: {target_url}")

        # 1. 記事抽出
        article = Article(target_url, language='ja')
        article.download()
        article.parse()
        
        content = article.text if article.text else f"URL: {target_url}\nこのニュースを要約して。"

        # 2. Geminiに依頼（最新モデル gemini-2.0-flash を使用）
        print("Gemini-2.0に要約を依頼中...")
        
        # モデル名を 2.0 に更新
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"以下のニュースを3行で要約して。日本語で。\n\n{content}"
        )

        print("\n" + "="*50)
        print(f"【要約結果】:\n{response.text}")
        print("="*50)
        print("\nついに成功です！")

    except Exception as e:
        print(f"\nエラー詳細: {e}")

if __name__ == "__main__":
    summarize_first_article()
