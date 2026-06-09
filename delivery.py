def calculate_delivery_time(start_time, end_time):
    """
    配送の開始時間と終了時間から、作業時間を計算する関数
    (引数：整数または浮動小数点数)
    """
    if not isinstance(start_time, (int, float)) or not isinstance(end_time, (int, float)):
        raise ValueError("時間は数値で入力してください！")
    
    return end_time - start_time

# テストしてみる
try:
    print(f"本日の配送時間: {calculate_delivery_time(4.25, 8.5)} 時間")
except ValueError as e:
    print(f"エラー発生: {e}")