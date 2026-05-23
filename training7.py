import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime
import urllib.parse

# --- 設定：検索したいキーワード ---
search_keywords = ["高市早苗", "大谷翔平", "トランプ"]

def get_news_from_search(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    # 検索URL（最新順に並ぶように設定）
    url = f"https://news.yahoo.co.jp/search?p={encoded_keyword}&ei=utf-8&sort=recent"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    found_news = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # より広範囲に記事を拾うための汎用的なセレクタに変更
    # aタグの中から、ニュース項目と思われるクラスを探す
    for item in soup.find_all('a'):
        title_tag = item.find(['h1', 'h2', 'h3', 'div'], class_=lambda x: x and 'title' in x.lower())
        link = item.get('href')
        
        if title_tag and link and "news.yahoo.co.jp/articles" in link:
            title = title_tag.text.strip()
            found_news.append({
                "取得日時": current_time,
                "検索ワード": keyword,
                "タイトル": title,
                "URL": link
            })
    
    # 重複を排除（同じページ内で同じ記事が複数ヒットすることがあるため）
    unique_news = list({v['URL']: v for v in found_news}.values())
    return unique_news

# --- 以下、保存処理は前回と同じ ---
all_results = []
for kw in search_keywords:
    print(f"「{kw}」を検索中...")
    results = get_news_from_search(kw)
    print(f"  -> {len(results)} 件発見")
    all_results.extend(results)
    time.sleep(1)

if all_results:
    df_new = pd.DataFrame(all_results)
    file_name = "my_research_history.xlsx"

    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_new_unique = df_new[~df_new["URL"].isin(df_old["URL"])]
        if not df_new_unique.empty:
            df_final = pd.concat([df_old, df_new_unique], ignore_index=True)
            print(f"新着ニュースを {len(df_new_unique)} 件追加しました。")
        else:
            df_final = df_old
            print("新しいニュースはありませんでした。")
    else:
        df_final = df_new
        print(f"新しいファイル '{file_name}' を作成しました。")

    df_final.to_excel(file_name, index=False)
    print(f"現在の蓄積数：合計 {len(df_final)} 件")
else:
    print("ニュースが見つかりませんでした。検索条件を再確認してください。")