print("修行開始。智慧之王（ラファエル)と共に。")

# 自分の好きな言葉を一つ出力してみましょう
print("Step by step, I am evolving.")

# 修行：変数と演算
name = "藤本"
level = 1
exp = 100

# 経験値を２倍にする計算
doubled_exp = exp * 2

print(f"{name}の現在のレベル: {level}")
print(f"獲得経験値（２倍)：{doubled_exp}")

# 修行：条件分岐(if文)
name = "藤本"
level = 1
exp =200 # 現在の経験値

print(f"現在の状態 --- 名前: {name} / 経験値: {exp}")

# もし経験値が200以上なら、レベルを上げる
if exp >= 200:
    print("告知。経験値が規定値に達しました。")
    level = level + 1
    print(f"レベルアップ！現在のレベルは{level}です。")
else:
    print("経験値が不足しています。修行を継続してください。")

print("判定終了。")