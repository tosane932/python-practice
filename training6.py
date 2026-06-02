import requests
from bs4 import BeautifulSoup
import pandas as pd # 表形式のデータを扱うためのライブラリです
import os # ファイルの存在確認など、システム操作のために必要です
from datetime import datetime

# 1. Yahoo!ニュースのトップページにアクセス
url = "https://www.yahoo.co.jp/"
response = requests.get(url)

# インターネット通信の結果を確認。200なら成功です
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # ニュースの項目（タイトルとリンクが含まれる場所）を探します
    # Yahooの構造に合わせて、role='heading'を持つspanを探し、その親のaタグを見つけます
    news_list = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 修正版のループ（aタグの中からテキストがあるものだけ抽出）
    for a_tag in soup.select('section ul li a'):
        title = a_tag.text
        link = a_tag.get('href')
        
        if title and link:
            news_list.append({
                "取得日時": current_time,
                "タイトル": title,
                "URL": link
            })

    # デバッグ用：何件見つかったか必ず表示するように外に出す
    print(f"解析終了：{len(news_list)} 件のニュースを見つけました。")

# 2. データの整理と保存
    if news_list:
        df_new = pd.DataFrame(news_list)
        file_name = "yahoo_news_history.xlsx"

        if os.path.exists(file_name):
            df_old = pd.read_excel(file_name)
            
            # 【重要】URLを基準に、まだ保存されていないニュースだけを抽出
            # 既存のURLリストに含まれていない(isinの逆)ものだけを残す
            df_new_unique = df_new[~df_new["URL"].isin(df_old["URL"])]
            
            if not df_new_unique.empty:
                df_final = pd.concat([df_old, df_new_unique], ignore_index=True)
                print(f"新規ニュースを {len(df_new_unique)} 件追加します。")
            else:
                df_final = df_old
                print("新しいニュースはありませんでした。")
        else:
            df_final = df_new
            print(f"新しいファイル '{file_name}' を作成しました。")

        # Excelとして保存
        df_final.to_excel(file_name, index=False)
        print(f"現在の蓄積数：合計 {len(df_final)} 件")

else:
    print(f"エラー: サイトにアクセスできませんでした（Status: {response.status_code}）")