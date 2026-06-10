def calculate_delivery_time(start_time, end_time):
    if not isinstance(start_time, (int, float)) or not isinstance(end_time, (int, float)):
        raise ValueError("時間は数値で入力してください！")
    if end_time < start_time:
        raise ValueError("終了時間は開始時間より後にしてください！")
    return end_time - start_time

def calculate_breakdown(total_hours):
    # 休憩時間：1時間（固定）
    break_time = 1.0
    # 運行時間：約5時間（固定）
    driving_time = 5.0
    # 作業時間：合計 - 休憩 - 運行
    work_time = total_hours - break_time - driving_time
    
    return {
        "break": break_time,
        "driving": driving_time,
        "work": max(0, work_time) # マイナスにならないように調整
    }