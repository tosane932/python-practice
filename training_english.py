from google import genai
import os

# APIキーを直接書くのは危険なため、本来は環境変数から取得しますが、
# 今回は動くことを優先して、修正した形でセットします。
API_KEY = "AIzaSyCPa99NFSFXNweExQWl_F48AbazQ0mGgXQ" # セキュリティ上、後で隠す方法を教えますね
client = genai.Client(api_key=API_KEY)

def test_ai_english():
    print("Starting AI Communication Test...")
    
    try:
        # 【修正ポイント】modelには文字列だけを渡し、contentsを正しく設定します
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Give me 3 cool names for a robot character."
        )
        
        print("\n--- AI Response ---")
        # 取得したテキストを表示します
        if response.text:
            print(response.text)
            print("\nSUCCESS: Connection established!")
        else:
            print("\nError: Received an empty response.")

    except Exception as e:
        # エラーの内容を詳細に出力します
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    test_ai_english()