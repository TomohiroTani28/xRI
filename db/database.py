import sqlite3
import logging
import os

async def check_and_update_post_history(content):
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
        logging.error(f"Database error: {e}")
        return False
