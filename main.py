# main.py
import sys
from logic import calculate_delivery_time

def main():
    # コマンドライン引数が2つ（開始と終了）渡された場合
    if len(sys.argv) == 3:
        try:
            start = float(sys.argv[1])
            end = float(sys.argv[2])
            result = calculate_delivery_time(start, end)
            print(f"配送時間: {result:.2f} 時間")
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
            
        except ValueError as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()