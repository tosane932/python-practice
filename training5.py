## 今後、Pythonの勉強を再開するときは、ターミナルで python-practice フォルダに移動した後、
## source .venv/bin/activate を打ってから実行する癖をつける


import requests 
from bs4 import BeautifulSoup
import my_tools
import re
import csv  # CSV操作用の道具をインポート
from datetime import datetime # 日付取得用の道具

# 1. アクセス
url = "https://www.yahoo.co.jp/"
response = requests.get(url)

# 2. 解析
soup = BeautifulSoup(response.text, "html.parser")

# 3. 見出し抽出
print("--- Yahoo! Japan News Topics ---")
news_items = soup.find_all('a', href=re.compile("news.yahoo.co.jp/pickup"))

headlines_list = []
for i, item in enumerate(news_items[:15]):
    text = item.get_text().strip()
    if text:
        print(f"{i+1}: {text}")
        # 「番号」と「見出し」をセットにして保存する
        headlines_list.append([i+1, text])

# 4. CSVファイルへの保存（Excel自動処理への第一歩）
now = datetime.now().strftime("%Y%m%d_%H%M") # 現在時刻をファイル名に使う
filename = f"yahoo_news_{now}.csv"

with open(filename, mode='w', encoding='utf_8_sig', newline='') as f:
    writer = csv.writer(f)
    # ヘッダー（項目名）を書き込む
    writer.writerow(["No", "Headline"])
    # ニュースデータを書き込む
    writer.writerows(headlines_list)

print("\n--- Analysis & Save Result ---")
print(f"ファイル保存完了: {filename}")
print(f"Total headlines processed: {len(headlines_list)}")