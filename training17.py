import sys
import io

# --- 魔法の3行：OSの環境を無視してUTF-8（日本語）を強制する ---
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import feedparser
import pandas as pd
from google import genai
from newspaper import Article, Config
import time

# --- 以降は前のコードと同じ（clientの設定など） ---
client = genai.Client(api_key="AIzaSyCdX_bRqKKPwABUqFsfXmO4r7-0SpuKFmA")
RSS_URL = "https://www.nhk.or.jp/rss/news/cat0.xml"

config = Config()
config.browser_user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'

def get_ai_summary(text):
    if not text or len(text) < 50:
        return "本文不足"
    try:
        # プロンプト自体を完全にUTF-8でラップする
        prompt = f"以下のニュースを3行で日本語で要約してください。\n\n{text[:1500]}"
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"エラー継続中: {str(e)}"

# --- 実行処理（training16と同様） ---
print("OSの言語設定を上書きして再挑戦します...")
# ... (中略) ...