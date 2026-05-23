import os
from google import genai

# --- 1. APIキーの設定 ---
client = genai.Client(api_key="AIzaSyCdX_bRqKKPwABUqFsfXmO4r7-0SpuKFmA")

def test_ai():
    print("AIへの最終通信テストを開始します...")
    
    # 2. 日本語の依頼
    prompt = "「スライムがエンジニアを目指す物語」のタイトルを3つ考えてください。日本語でお願いします。"
    
    try:
        # 3. AIに送信（モデル名をシンプルに指定）
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        # 4. 結果を表示
        print("\n--- AIからの回答 ---")
        if response.text:
            print(response.text)
            print("--------------------\n")
            print("【祝】大成功です！AIとの双方向通信が完全に確立されました！")
        else:
            print("返答が空でした。")
        
    except Exception as e:
        # 万が一エラーが出た場合、詳細を表示
        print(f"\n× エラーが発生しました: {e}")

if __name__ == "__main__":
    test_ai()