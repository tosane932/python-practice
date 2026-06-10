import os
from collections import defaultdict

def calculate_weekly_summary():
    # 現在のファイルと同じ場所にある delivery_log.txt を指定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(base_dir, "delivery_log.txt")
    
    weekly_total = defaultdict(float)
    weekly_count = defaultdict(int)
    
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "(" in line and ")" in line:
                    weekday = line.split("(")[1].split(")")[0]
                    target_text = line.split("|")[-1]
                    time_val = float(target_text.split(":")[1].replace("時間", "").strip())
                    
                    weekly_total[weekday] += time_val
                    weekly_count[weekday] += 1
        
        print("--- 曜日別配送実績 ---")
        order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in order:
            if day in weekly_total:
                total = weekly_total[day]
                avg = total / weekly_count[day]
                bar = "*" * int(total / 2)
                print(f"{day}: {total:5.1f}h (平均 {avg:4.1f}h) | {bar}")
                
    except FileNotFoundError:
        print("記録ファイルが見つかりません。")

if __name__ == "__main__":
    calculate_weekly_summary()