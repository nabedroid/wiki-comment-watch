FROM python:3.12-slim

# OSパッケージのインストール
RUN apt-get update && apt-get install -y \
    bash \
    locales \
    && sed -i -e 's/# ja_JP.UTF-8 UTF-8/ja_JP.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8

#  Pythonライブラリのインストール
RUN pip install --no-cache-dir --upgrade pip beautifulsoup4 requests

WORKDIR /app

CMD ["python", "main.py"]
