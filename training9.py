import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime
import urllib.parse
from newspaper import Article # 本文抽出用の新しい道具

# --- 設定：検索したいキーワード ---
search_keywords = ["高市早苗", "大谷翔平", "トランプ","物流"]

def get_google_news_with_summary(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ja&gl=JP&ceid=JP:ja"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "xml")
    found_news = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 検索結果の上位3件だけを深く読みに行く（時間がかかるため最初は少なめに）
    items = soup.find_all('item')[:3] 

    for item in items:
        title = item.title.text
        link = item.link.text
        
        print(f"  - 本文を解析中: {title[:20]}...")
        
        try:
            # newspaper3kを使って本文を取得
            article = Article(link)
            article.download()
            article.parse()
            # 本文の最初の100文字を「簡易要約」とする
            summary = article.text[:100].replace('\n', ' ') + "..."
        except Exception as e:
            summary = "本文の取得に失敗しました。"

        found_news.append({
            "取得日時": current_time,
            "検索ワード": keyword,
            "タイトル": title,
            "本文抜粋": summary,
            "URL": link
        })
        # 連続アクセスで相手のサイトを驚かせないための休憩
        time.sleep(2)
    
    return found_news

# --- メイン処理 ---
all_results = []
for kw in search_keywords:
    print(f"「{kw}」の最新情報を深掘り中...")
    results = get_google_news_with_summary(kw)
    all_results.extend(results)

if all_results:
    df_new = pd.DataFrame(all_results)
    file_name = "ai_summary_news.xlsx"

    # 今回は実験用として、実行するたびに新しいファイルを作るか上書きします
    df_new.to_excel(file_name, index=False)
    print(f"\n完了！ '{file_name}' を確認してください。")
else:
    print("ニュースが見つかりませんでした。")