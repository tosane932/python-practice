import sys
import datetime
import os
from logic import calculate_delivery_time

def main():
    # 現在のファイル（main.py）がある場所（deliveryフォルダ）を基準にパスを作る
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(base_dir, "delivery_log.txt")

    # 記録用の補助関数を定義
    def save_log(result):
        today = datetime.date.today()
        weekday = today.strftime("%a")  # 曜日を取得 (Mon, Tue, etc.)
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"{today}({weekday}) | 配送時間: {result:.2f} 時間\n")

    # コマンドライン引数が2つ（開始と終了）渡された場合
    if len(sys.argv) == 3:
        try:
            start = float(sys.argv[1])
            end = float(sys.argv[2])
            result = calculate_delivery_time(start, end)
            print(f"配送時間: {result:.2f} 時間")
            save_log(result)
            print(f"記録を {log_file_path} に保存しました！")
        except ValueError as e:
            print(f"エラー: {e}")
    
    # 引数がない場合は対話形式で動かす
    else:
        try:
            print("--- 配送時間計算ツール ---")
            start = float(input("開始時間を入力してください (例: 4.25): "))
            end = float(input("終了時間を入力してください (例: 8.5): "))
            
            result = calculate_delivery_time(start, end)
            print(f"本日の配送時間は {result:.2f} 時間です！")
            
            save_log(result)
            print("記録を delivery_log.txt に保存しました！")

        except ValueError as e:
            print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()