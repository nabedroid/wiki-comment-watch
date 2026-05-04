# 概要

「ステラソラ攻略有志 Wiki」のコメント/雑談掲示板を監視し、ルール違反コメントを自動検知して Discord に通知するツール。

# 主な機能

- **Wiki コメントの自動取得**: 定期的（デフォルト 30 分）に Wiki の掲示板をスクレイピングし、新しいコメントを取得する
- **AI による違反コメント判定**: あらかじめ設定したルールに基づいてコメントが「キャラへの誹謗中傷」「性的表現」「他アプリとの比較」などに該当するかを判定する
- **Discord 通知**: ルール違反が検知された場合、違反内容の詳細とともに Discord チャンネルに通知を送信する

# 前提条件

動作には以下の環境が必要です。

- **OS**: Docker が動作する環境 (Windows, Linux 等)
- **GPU**: NVIDIA 製 GPU (LLM の実行に使用します)
- **ソフトウェア**:
  - Docker / Docker Compose
  - NVIDIA Container Toolkit (Docker で GPU を使用するために必要)
- **その他**:
  - 通知先の Discord Webhook URL

# 使い方

## 1. リポジトリの準備
リポジトリをクローンまたはダウンロードします。

## 2. 環境変数の設定
`.env.sample` をコピーして `.env` ファイルを作成し、必要な情報を記入します。

```bash
cp .env.sample .env
```

`.env` 内の各項目：
- `BASE_MODEL`: 使用するベースモデル名 (例: `gemma4:e4b`)
- `CUSTOM_MODEL`: プロジェクトで使用するカスタムモデル名
- `DISCORD_WEBHOOK_URL`: Discord の Webhook 連携で取得した URL

## 3. 起動
Docker Compose を使用してサービスを起動します。

```bash
docker compose up
```

起動後、`watcher` コンテナが Wiki の監視を開始します。

# ルールの調整
`ollama/Modelfile` を編集することで、ルールを調整できます。
編集後、`docker compose up --build` を実行してカスタムモデルを再構築してください。

# 構成

- **ollama/**: LLM サーバー。Wiki のルールを組み込んだカスタムモデルを生成して実行する
- **watcher/**: 監視プログラム本体。Python で記述されており、スクレイピングと判定指示、通知を行う
- **compose.yaml**: 全体のサービス構成定義

## 注意事項

- 本ツールは特定の Wiki (ステラソラ攻略有志 Wiki) の構造に最適化されています。他の Wiki で使用する場合は `watcher/main.py` のスクレイピング部分の修正が必要です。
- AI による判定は 100% 正確ではありません。最終的な判断は人間が行うことを推奨します。