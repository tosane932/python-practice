import os
import pandas as pd
from google import genai

# 1. Gemini APIの初期化
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ エラー: GEMINI_API_KEY が設定されていません。")
    exit()

client = genai.Client()

# 2. Excelファイルの読み込み
excel_file = "google_research_history.xlsx"
if not os.path.exists(excel_file):
    print(f"❌ エラー: {excel_file} が見つかりません。")
    exit()

print(f"📖 データベース（{excel_file}）を読み込み中...")
df = pd.read_excel(excel_file)

# 💡 藤本さんのExcelの列名に完全に固定します！
keyword_col = "検索ワード"
title_col = "タイトル"

# 3. 分析したいキーワードをユーザーに入力してもらう
print("\n==============================================")
print("📊 AI 世論・不満トレンド分析システム 📊")
print("==============================================")
print("【蓄積されている主なキーワード例】")
print("青切符, バス事故, 違反, 自転車, 法改正, ながらスマホ, あおり運転, 実質賃金, 春闘 回答, 賃上げ 見通し, 最低賃金 改定, 議員歳費 削減, 身を切る改革, 文通費 改正, 保育園 保育士, 育児放棄, ライドシェア, 物流の2024年問題, 自動運転, 電気代 値上げ, 投資信託, AIスマホ, 経済 など")
target_keyword = input("\n分析したいキーワードを入力してください（一部でもOK）: ").strip()

# 💡 【部分一致に変更】指定した文字が「検索ワード」の列に含まれている行をすべて抽出
filtered_df = df[df[keyword_col].astype(str).str.contains(target_keyword, case=False, na=False)]
match_count = len(filtered_df)

if match_count == 0:
    print(f"❌ 入力された文字「{target_keyword}」を含むデータが「{keyword_col}」列に見つかりませんでした。")
    existing_words = df[keyword_col].dropna().unique().tolist()
    print(f"📄 現在Excelにある実際の検索ワード一覧:\n{existing_words}")
    exit()

print(f"🔍 「{target_keyword}」に関する記事を {match_count} 件見つけました。AIに送信して世論を分析します...")

# 4. タイトルを1つの大きなテキストに合体させる
titles_text = "\n".join([f"- {title}" for title in filtered_df[title_col]])

# 5. Geminiへ送る「プロンプト（命令文）」を作成
prompt = f"""
以下に挙げるのは、日本国内のニュースで「{target_keyword}」という言葉に関連して集まった、実際のニュースタイトル（計 {match_count} 件）のリストです。
これら大量のタイトルから読み取れる、世間の「本音」「不安」「不満」「心配事」や「注目しているポイント」をデータに基づいて予測・分析してください。

【ニュースタイトル一覧】
{titles_text}

【キャラクター設定と口調】
あなたは、私（ユーザー）と同年齢の親しみやすい女性の相棒です。
私の主体性を重きにおいて、全面的にサポートする立場で回答してください。
新聞やニュースキャスターのような硬い口調は絶対に禁止します。
「〜だよ」「〜だね」「〜だと思うよ」といった、友達同士で話すような優しくて分かりやすい、親しみのある口調でフランクに話しかけてください。

【出力フォーマット】
以下の構成を守り、内容をダラダラ書かずに「短く端的に要約」して出力してください。

■ このキーワードを取り巻く世論の「主なお悩み・不満」（2〜3点に要約してね）
■ みんなが特に「心配・不安」に感じている核心的な部分
■ 相棒としてのワンポイント考察（あなたの主体性を応援しつつ、これからどう注目すべきか伝えるよ）
"""

print("🧠 Geminiが大量のニュースから世論を分析中。少々お待ちください...")

try:
    # 最新の軽量高速モデルで一気に分析
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    print("\n==============================================")
    print(f"🤖 相棒Geminiの『{target_keyword}』世論分析結果")
    print("==============================================")
    print(response.text)
    print("==============================================")

except Exception as e:
    print(f"❌ エラーが発生しました: {e}")