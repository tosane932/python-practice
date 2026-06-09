# delivery.py

def calculate_delivery_time(start_time, end_time):
    if not isinstance(start_time, (int, float)) or not isinstance(end_time, (int, float)):
        raise ValueError("時間は数値で入力してください！")
    if end_time < start_time:
        raise ValueError("終了時間は開始時間より後にしてください！")
    return end_time - start_time

# --- ユーザー入力を受け付ける処理を追加 ---
if __name__ == "__main__":
    try:
        start = float(input("開始時間を入力してください (例: 4.25): "))
        end = float(input("終了時間を入力してください (例: 8.5): "))
        
        result = calculate_delivery_time(start, end)
        print(f"本日の配送時間は {result:.2f} 時間です！")
        
    except ValueError as e:
        print(f"エラーが発生しました: {e}")