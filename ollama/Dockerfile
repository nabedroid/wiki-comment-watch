FROM ollama/ollama

# 実行に必要な curl をインストール（サーバー待機チェック用）
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG OLLAMA_MODEL
ENV OLLAMA_MODEL=${OLLAMA_MODEL}

# スクリプトをコピーして実行権限を与える
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# ポート開放
EXPOSE 11434

# 自作の entrypoint を実行
ENTRYPOINT ["/app/entrypoint.sh"]