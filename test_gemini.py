import os
from google import genai

# システムに設定したAPIキーを自動で読み込みます
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ エラー: GEMINI_API_KEY が設定されていません。ターミナルで export してください。")
    exit()

# Geminiのクライアントを初期化
client = genai.Client()

print("📡 Geminiにお伺いを立てています...")

try:
    # 2026年現在、最新の標準軽量モデル gemini-2.5-flash を使用します
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='「PythonとUbuntuの組み合わせは最高だね」という言葉を、少しおちゃめな相棒風に返事して。',
    )
    
    print("\n🤖 Geminiからの返答:")
    print(response.text)

except Exception as e:
    print(f"❌ エラーが発生しました: {e}")