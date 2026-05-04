import json
import requests
import os

# 環境変数から WEBHOOK_URL を取得
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

class DiscordService:
  def __init__(self) -> None:
    self._webhook_url = WEBHOOK_URL

  def is_available(self) -> bool:
    return self._webhook_url is not None

  def post(self, content: str) -> bool:
    """判定結果をDiscordに投稿する"""
    try:
      res = requests.post(
        self._webhook_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
          # embed は面倒なので使わない
          'content': content
        }),
        timeout=10,
      )
      res.raise_for_status()
      return True
    except requests.RequestException as e:
      print(f"Discord投稿エラー: {e}")
      return False

if __name__ == '__main__':
  discord = DiscordService()
  content = '\n'.join([
    '---',
    f'【ルール違反】ルール違反の項目名',
    f'【違反ページ】コメント/雑談掲示板',
    f'【該当コメント】コメント本文',
    f'【違反の詳細】違反の詳細',
  ])
  discord.post(content)
