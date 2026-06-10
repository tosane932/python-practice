import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime
import urllib.parse

# --- 設定：検索したいキーワード ---
search_keywords = ["青切符", "バス事故", "違反", "自転車", "法改正", "ながらスマホ", "あおり運転", "実質賃金", "春闘 回答", "賃上げ 見通し", "最低賃金 改定", "議員歳費 削減", "身を切る改革", "文通費 改正", "保育園 保育士", "育児放棄", "ライドシェア", "物流の2024年問題", "自動運転", "電気代 値上げ", "投資信託", "AIスマホ", "経済"]

def get_google_news(keyword):
    # Googleニュースの検索結果をRSS形式で取得するURL
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ja&gl=JP&ceid=JP:ja"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    # RSSはXML形式なので、xmlパーサーを使用します
    soup = BeautifulSoup(response.text, "xml")
    found_news = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # RSS内の各記事は <item> タグで囲まれています
    for item in soup.find_all('item'):
        title = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text # 記事の公開日時
        
        found_news.append({
            "取得日時": current_time,
            "検索ワード": keyword,
            "タイトル": title,
            "公開日時": pub_date,
            "URL": link
        })
    
    return found_news

# --- メイン処理 ---
all_results = []
for kw in search_keywords:
    print(f"Googleニュースで「{kw}」を検索中...")
    results = get_google_news(kw)
    print(f"  -> {len(results)} 件の最新記事を捕捉")
    all_results.extend(results)
    time.sleep(1)

if all_results:
    df_new = pd.DataFrame(all_results)
    file_name = "google_research_history.xlsx"

    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_new_unique = df_new[~df_new["URL"].isin(df_old["URL"])]
        if not df_new_unique.empty:
            df_final = pd.concat([df_old, df_new_unique], ignore_index=True)
            print(f"新着を {len(df_new_unique)} 件追加。")
        else:
            df_final = df_old
            print("新しい記事はありません。")
    else:
        df_final = df_new
        print(f"新しいファイル '{file_name}' を作成しました。")

    df_final.to_excel(file_name, index=False)
    print(f"現在の蓄積数：合計 {len(df_final)} 件")
else:
    print("ニュースが見つかりませんでした。")