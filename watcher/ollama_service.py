import json
import os
import requests
from datetime import datetime

from comments import Comment
from ollama import Client

CUSTOM_MODEL = os.getenv('CUSTOM_MODEL')

class OllamaServiceResponse:
  def __init__(self, is_violation: bool, violation_type: str, violation_description: str) -> None:
    self._is_violation = is_violation
    self._violation_type = violation_type
    self._violation_description = violation_description

  @property
  def is_violation(self) -> bool: return self._is_violation
  
  @property
  def violation_type(self) -> str: return self._violation_type
  
  @property
  def violation_description(self) -> str: return self._violation_description

  def __str__(self) -> str:
    return f'{self.is_violation}: {self.violation_type}: {self.violation_description}'


class OllamaService:
  def __init__(self, model: str = None, ollama_url: str = 'http://ollama:11434') -> None:
    self._client: Client = Client(
      host=ollama_url,
    )
    self._model: str = model if model is not None else CUSTOM_MODEL
  
  def post(self, comment: Comment) -> OllamaServiceResponse:
    response = self._client.generate(
      model=self._model,
      prompt=comment.comment,
      stream=False,
      format={
        'type': 'object',
        'properties': {
          'is_violation': {
            'type': 'boolean',
          },
          'violation_type': {
            'type': 'string',
          },
          'violation_description': {
            'type': 'string',
          },
        },
        'required': ['is_violation', 'violation_type', 'violation_description'],
      },
      options={
        # 回答のランダム性をなくす
        'temperature': 0,
        # コンテキストサイズを多めに確保
        'num_ctx': 4096,
      }
    )
    # トークン数を表示（num_ctx と同じようなら num_ctx を増やす）
    # print(response.prompt_eval_count)
    # プロンプトの回答部分だけを取り出す
    response_dict = json.loads(response.response)
    result = OllamaServiceResponse(
      is_violation=response_dict['is_violation'],
      violation_type=response_dict['violation_type'],
      violation_description=response_dict['violation_description'],
    )   
    return result

if __name__ == '__main__':
  import locale
  locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
  ollama = OllamaService()
  comment = Comment('UxwGBCa8ARM', '信者様乙ｗ', 'コメント/雑談掲示板', datetime.now())
  print(ollama.post(comment))
  comment = Comment('UxwGBCa8ARM', '正直、対抗戦とか対人戦をメインコンテンツにするんじゃなくて、塔の方をメインにして高難易度ダンジョンを臨機応変にビルドを組みながら攻略するってゲーム性の方が流行ってたと思うの・・・', 'コメント/雑談掲示板', datetime.now())
  print(ollama.post(comment))
