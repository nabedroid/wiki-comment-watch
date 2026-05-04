import hashlib
import sqlite3
from datetime import datetime

DB_NAME = 'comments.db'

class Comment:
  def __init__(self, date_userid: str, comment: str, page: str, posted_at: datetime) -> None:
    seed = f'{date_userid}:{comment}:{page}:{posted_at.isoformat()}'
    # 流動量の少ない掲示板なら16文字でも衝突しないと判断
    self._id = hashlib.sha256(seed.encode()).hexdigest()[:16]
    self._date_userid = date_userid
    self._comment = comment
    self._page = page
    self._posted_at = posted_at
  
  def __str__(self) -> str:
    return f'{self.date_userid}: {self.comment} ({self.posted_at})'

  @property
  def id(self) -> str: return self._id
  
  @property
  def date_userid(self) -> str: return self._date_userid
  
  @property
  def comment(self) -> str: return self._comment
  
  @property
  def page(self) -> str: return self._page
  
  @property
  def posted_at(self) -> datetime: return self._posted_at

class Comments:
  def __init__(self, db_name: str = DB_NAME) -> None:
    self._db_name = db_name

  def init_db(self) -> None:
    """データベースの初期化"""
    with sqlite3.connect(self._db_name) as conn:
      conn.execute('''
        CREATE TABLE IF NOT EXISTS processed_comments (
          id TEXT PRIMARY KEY,
          date_userid TEXT,
          comment TEXT,
          page TEXT,
          posted_at TIMESTAMP,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
      conn.commit()

  def insert(self, comment: Comment) -> None:
    with sqlite3.connect(self._db_name) as conn:
      conn.execute('''
        INSERT INTO processed_comments (id, date_userid, comment, page, posted_at)
        VALUES (?, ?, ?, ?, ?)
      ''', (comment.id, comment.date_userid, comment.comment, comment.page, comment.posted_at.isoformat()))
      conn.commit()

  def exists(self, comment: Comment) -> bool:
    with sqlite3.connect(self._db_name) as conn:
      cursor = conn.execute('''
        SELECT 1 FROM processed_comments WHERE id = ?
      ''', (comment.id,))
      return cursor.fetchone() is not None

  def insert_ignore(self, comment: Comment) -> bool:
    if self.exists(comment):
      return False
    self.insert(comment)
    return True

  def delete(self, comment: Comment) -> bool:
    with sqlite3.connect(self._db_name) as conn:
      cursor = conn.execute('''
        DELETE FROM processed_comments WHERE id = ?
      ''', (comment.id,))
      conn.commit()
      return cursor.rowcount > 0

  def select(self, id: str) -> Comment | None:
    with sqlite3.connect(self._db_name) as conn:
      cursor = conn.execute('''
        SELECT date_userid, comment, page, posted_at FROM processed_comments WHERE id = ?
      ''', (id,))
      row = cursor.fetchone()
      if row is None:
        return None
      return Comment(row[0], row[1], row[2], datetime.fromisoformat(row[3]))

  def select_all(self, limit: int = 100) -> list[Comment]:
    with sqlite3.connect(self._db_name) as conn:
      cursor = conn.execute('''
        SELECT id, date_userid, comment, page, posted_at FROM processed_comments ORDER BY posted_at DESC LIMIT ?
      ''', (limit,))
      return [Comment(row[1], row[2], row[3], datetime.fromisoformat(row[4])) for row in cursor.fetchall()]

  def count(self) -> int:
    with sqlite3.connect(self._db_name) as conn:
      cursor = conn.execute('''
        SELECT COUNT(*) FROM processed_comments
      ''')
      return cursor.fetchone()[0]

if __name__ == '__main__':
  # テストコード
  comment = Comment('test', 'test', 'test', datetime.now())
  db = Comments()
  db.init_db()
  count = db.count()
  print(f'count: {count}')
  db.insert(comment)
  print(f'count: {count == db.count() - 1}')
  select_comment = db.select(comment.id)
  print(f'select: {select_comment and comment.id == select_comment.id}')
  print(f'insert_ignore: {db.insert_ignore(comment) == False}')
  print(f'count: {count == db.count() - 1}')
  print(f'delete: {db.delete(comment) == True}')
  print(f'count: {count == db.count()}')
