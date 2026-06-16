# Python復習記録

## 概要
Python学習を本格的に開始し、スクレイピングからWebアプリケーション開発までを目指す成長の記録です。

## ディレクトリ構成
- `scraping202605/`: スクレイピングおよび自動化ツールの検証記録
    - [動作デモ動画](https://youtu.be/PVfwmYn7mlY)
- `delivery/`: 配送時間記録・集計ツール
    - `main.py`: 開始・終了時間から配送時間を算出し、`delivery_log.txt`に日付・曜日付きで記録（コマンドライン引数・対話入力の両方に対応）
    - `logic.py`: 配送時間の計算ロジック
    - `summary.py`: 記録した配送ログを集計し、合計・平均配送時間を表示
    - `weekly_summary.py`: 配送ログを曜日別に集計し、合計・平均時間をテキストグラフ付きで表示
    - `test_delivery.py`: `unittest`によるロジック部分のユニットテスト

## 開発環境
- OS: Ubuntu 24.04 LTS (Lubuntu)
- Language: Python 3.12
- Editor: VS Code

## 今後の目標
- Python基礎・自動化からWebフレームワーク（Flask/Django）への展開
- CI（GitHub Actions等）でのテスト自動実行など、開発フローのさらなる強化