import json
import requests
import os
from datetime import datetime

from ollama import OllamaResponse

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

class Discord:
  def __init__(self) -> None:
    self._webhook_url = WEBHOOK_URL

  def post(self, response: 'OllamaResponse') -> bool:
    """
    AIの判定結果をDiscordに投稿する
    """
    content = '\n'.join([
      f'【違反有無】{'違反あり' if response.is_violation else '違反なし'}',
      f'【ルール違反】{response.violation_type}',
      f'【違反ページ】{response.violation_page}',
      f'【該当コメント】{response.violation_comment}',
      f'【違反の詳細】{response.violation_description}',
    ])
    try:
      res = requests.post(
        self._webhook_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
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
  import locale
  locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

  discord = Discord()
  response = OllamaResponse(True, 'test', 'test', 'test', 'test')
  discord.post(response)
