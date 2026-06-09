def calculate_delivery_time(start_time, end_time):
    if not isinstance(start_time, (int, float)) or not isinstance(end_time, (int, float)):
        raise ValueError("時間は数値で入力してください！")
    if end_time < start_time:
        raise ValueError("終了時間は開始時間より後にしてください！")
    return end_time - start_time