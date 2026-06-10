import os

def calculate_summary():
    # 現在のファイル（summary.py）と同じ場所にある delivery_log.txt を指定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(base_dir, "delivery_log.txt")
    
    total_hours = 0.0
    count = 0
    
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            for line in f:
                target_text = line.split("|")[-1] 
                parts = target_text.split(":")
                if len(parts) >= 2:
                    time_str = parts[1].replace("時間", "").strip()
                    total_hours += float(time_str)
                    count += 1
        
        if count > 0:
            average_hours = total_hours / count
            print(f"--- 配送実績サマリー ---")
            print(f"記録回数: {count} 回")
            print(f"合計配送時間: {total_hours:.2f} 時間")
            print(f"平均配送時間: {average_hours:.2f} 時間")
        else:
            print("記録が見当たりませんでした！")
            
    except FileNotFoundError:
        print("ファイルが見つかりません。")

if __name__ == "__main__":
    calculate_summary()