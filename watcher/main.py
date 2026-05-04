import hashlib
import locale
import re
import sqlite3
import sys
import time
from datetime import datetime
from typing import Iterator

import requests
import bs4

from comments import Comment, Comments
from ollama_service import OllamaService
from discord_service import DiscordService

WIKI_URL = 'https://stellasora.wikiru.jp/?%E3%82%B3%E3%83%A1%E3%83%B3%E3%83%88/%E9%9B%91%E8%AB%87%E6%8E%B2%E7%A4%BA%E6%9D%BF'

def comment_iterator(soup: bs4.BeautifulSoup) -> Iterator[Comment]:
  """雑談掲示板からコメントを抽出する"""
  li_list = soup.select('div#body li')
  for li in li_list:
    # コメント -- [ID] 形式のテキストを取得
    texts = li.find_all(string=True, recursive=False)
    if not texts: continue
    text = ''.join(texts).strip().replace('\n', '')
    match = re.match(r'^(.+) -- \[(.+)\]', text)
    if not match: continue
    comment = match.group(1)
    date_userid = match.group(2)
    # data-mtime 属性から投稿日時を取得
    span_date = li.select_one('span[data-mtime]')
    if not span_date: continue
    date = datetime.fromisoformat(span_date['data-mtime'])
    yield Comment(date_userid, comment, 'コメント/雑談掲示板', date)

def main() -> None:
  """メイン処理"""
  ollama = OllamaService()
  discord = DiscordService()
  db = Comments()
  db.init_db()
  print(f"取得開始: {datetime.now()}")
  # 30分ごとに雑談掲示板を取得し、新規コメントをチェックする
  while True:
    try:
      # 雑談掲示板のHTMLを取得
      res = requests.get(WIKI_URL)
      res.raise_for_status()
    except requests.exceptions.RequestException as e:
      print(f"エラー: {e}")
      sys.exit(-1)
    # HTMLをパース
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # コメントを抽出
    for comment in comment_iterator(soup):
      # 既に処理済みのコメントはスキップ
      if db.exists(comment): continue
      # 新規コメントを処理
      print('処理中のコメント: ', comment)
      # Ollamaで判定
      ollama_response = ollama.post(comment)
      print('判定結果: ', ollama_response.is_violation, ollama_response.violation_type, ollama_response.violation_description)
      # ルール違反の場合はDiscordに通知
      if ollama_response.is_violation and discord.is_available:
        content = '\n'.join(['',
          f'【ルール違反】{ollama_response.violation_type}',
          f'【違反ページ】{comment.page}',
          f'【該当コメント】{comment.comment}',
          f'【違反の詳細】{ollama_response.violation_description}',
        ])
        discord.post(content)
      # データベースにコメントを保存
      db.insert(comment)
    # 30分待機
    time.sleep(60 * 30)

if __name__ == '__main__':
  """エントリポイント"""
  # 日本語ロケールを設定
  locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
  main()