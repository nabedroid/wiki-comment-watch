#!/bin/bash

# 非公開のポートで起動
OLLAMA_HOST=127.0.0.1:11435 ollama serve &

# サーバーが完全に立ち上がるまで少し待機
echo "Waiting for Ollama server to start..."
while ! curl -s http://localhost:11435/api/tags > /dev/null; do
    sleep 1
done

# モデルの作成
echo "Creating ${CUSTOM_MODEL} model..."
## 環境変数を埋め込んだModelfileを作成
sed "s/\${BASE_MODEL}/${BASE_MODEL}/g" Modelfile > Modelfile.tmp
## カスタムモデルを作成
OLLAMA_HOST=127.0.0.1:11435 ollama create ${CUSTOM_MODEL} -f Modelfile.tmp
## 一時ファイルを削除
rm Modelfile.tmp

# 正規のポートで再起動
pkill ollama
exec ollama serve
