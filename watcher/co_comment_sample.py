# コメント/CO報告掲示板 から違反コメントと報告内容のサンプルを取得する
import re
from typing import Iterator

import requests
import bs4

COMMENT_CO_URL = 'https://stellasora.wikiru.jp/index.php?%E3%82%B3%E3%83%A1%E3%83%B3%E3%83%88/CO%E5%A0%B1%E5%91%8A%E6%8E%B2%E7%A4%BA%E6%9D%BF'

class CoComment:
  def __init__(self, violation_type: str, violation_page: str, violation_comment: str, violation_description: str) -> None:
    self.violation_type = violation_type
    self.violation_page = violation_page
    self.violation_comment = violation_comment
    self.violation_description = violation_description

  def __str__(self) -> str:
    return f'{self.violation_type} / {self.violation_page} / {self.violation_comment} / {self.violation_description}'

def comment_iterator(soup: bs4.BeautifulSoup) -> Iterator[CoComment]:
  trees = soup.select('div#body li')
  for tree in trees:
    # 木の枝を取得
    branches = tree.select('li')
    # 枝がある＝管理人とのやり取りや修正があったコメントなのでスキップ
    if len(branches) > 0: continue
    # フォーマットに完全一致する報告のみを抽出
    text = tree.get_text(strip=True)
    match = re.match(r'^【ルール違反】(.+)【ページ名】(.+)【該当コメント】(.+) -- .+【違反の詳細】(.+) -- .+$', text)
    if not match: continue
    yield CoComment(
      violation_type=match.group(1),
      violation_page=match.group(2),
      violation_comment=match.group(3),
      violation_description=match.group(4),
    )

if __name__ == '__main__':
  res = requests.get(COMMENT_CO_URL)
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  print('| 判定対象コメント | is_violation | violation_type | violation_description |')
  print('| --- | --- | --- | --- |')
  for comment in comment_iterator(soup):
    print(f'| {comment.violation_comment} | True | {comment.violation_type} | {comment.violation_description} |')