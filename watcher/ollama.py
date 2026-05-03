import json
import os
import requests
from datetime import datetime

from comments import Comment

OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')

class OllamaResponse:
  def __init__(self, is_violation: bool, violation_type: str, violation_page: str, violation_comment: str, violation_description: str) -> None:
    self._is_violation = is_violation
    self._violation_type = violation_type
    self._violation_page = violation_page
    self._violation_comment = violation_comment
    self._violation_description = violation_description

  @property
  def is_violation(self) -> bool: return self._is_violation
  
  @property
  def violation_type(self) -> str: return self._violation_type
  
  @property
  def violation_page(self) -> str: return self._violation_page
  
  @property
  def violation_comment(self) -> str: return self._violation_comment
  
  @property
  def violation_description(self) -> str: return self._violation_description

  def __str__(self) -> str:
    return f'{self.is_violation}: {self.violation_type}: {self.violation_page}: {self.violation_comment}: {self.violation_description}'


class Ollama:
  def __init__(self, model: str = None, ollama_url: str = 'http://ollama:11434', rules_path: str = 'rules.md') -> None:
    self._model = model if model is not None else OLLAMA_MODEL
    self._ollama_url = ollama_url
    with open(rules_path, 'r', encoding='utf-8') as f:
      self._rules = f.read()
  
  def post(self, comment: Comment) -> OllamaResponse:
    prompt = f'{self._rules}\n\n# 判定対象コメント\n- コメント: {comment.comment}\n- date-userid: {comment.date_userid}\n- 投稿日時: {comment.posted_at.strftime('%Y-%m-%d (%a) %H:%M:%S')}'
    res = requests.post(f'{self._ollama_url}/api/generate', json={
      'model': self._model,
      'prompt': prompt,
      'stream': False,
      'format': 'json',
    }, timeout=120)
    res.raise_for_status()
    data = res.json()
    response = json.loads(data['response'])
    result = OllamaResponse(
      is_violation=response['is_violation'],
      violation_type=response['violation_type'],
      violation_page=response['violation_page'],
      violation_comment=response['violation_comment'],
      violation_description=response['violation_description'],
    )   
    return result

if __name__ == '__main__':
  import locale
  locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
  ollama = Ollama()
  comment = Comment('UxwGBCa8ARM', 'CO信者乙', datetime.now())
  print(ollama.post(comment))
