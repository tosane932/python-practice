# main.py
from logic import calculate_delivery_time

def main():
    try:
        start = float(input("開始時間を入力してください (例: 4.25): "))
        end = float(input("終了時間を入力してください (例: 8.5): "))
        
        result = calculate_delivery_time(start, end)
        print(f"本日の配送時間は {result:.2f} 時間です！")
        
    except ValueError as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()