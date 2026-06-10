from google import genai

client = genai.Client(api_key="あなたのAPIキー")

print("現在、あなたの環境で利用可能なモデル一覧:")
for model in client.models.list():
    print(f" - {model.name}")