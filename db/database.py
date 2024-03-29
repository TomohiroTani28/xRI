import sqlite3
import logging
import os

def check_and_update_post_history(content):
    db_path = os.getenv('DATABASE_PATH', './xri.db')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    content TEXT
                )
            """)
            # 類似コンテンツのチェック（ここはシンプルな例ですが、実際には類似度計算が必要）
            cur.execute("SELECT * FROM posts WHERE content = ?", (content,))
            if cur.fetchone():
                logging.info("Duplicate content detected in database.")
                return False
            cur.execute("INSERT INTO posts (content) VALUES (?)", (content,))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        logging.info("Duplicate content detected in database.")
        return False
    except Exception as e:
        logging.error("Database error: %s", e, exc_info=True)
        return False
