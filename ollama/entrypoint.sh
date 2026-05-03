#!/bin/bash

# 非公開のポートで起動
OLLAMA_HOST=127.0.0.1:11435 ollama serve &

# サーバーが完全に立ち上がるまで少し待機
echo "Waiting for Ollama server to start..."
while ! curl -s http://localhost:11435/api/tags > /dev/null; do
    sleep 1
done

# モデルのダウンロード
echo "Pulling ${OLLAMA_MODEL} model..."
OLLAMA_HOST=127.0.0.1:11435 ollama pull ${OLLAMA_MODEL}

# 正規のポートで再起動
pkill ollama
exec ollama serve
