import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="chat.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                title TEXT DEFAULT '新对话',
                created_at TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT,
                content TEXT,
                created_at TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                conversation_id INTEGER PRIMARY KEY,
                summary TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        # ★ 加上这一行：给 conversation_id 创建索引（如果不存在的话）
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_id ON messages(conversation_id)")
        self.conn.commit()

    def new_conversation(self, username, title="新对话"):
        """新建对话，返回 conversation_id"""
        self.cursor.execute(
            "INSERT INTO conversations (username, title, created_at) VALUES (?, ?, ?)",
            (username, title, datetime.now().isoformat())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_conversations(self, username):
        """读某用户的所有对话"""
        self.cursor.execute(
            "SELECT id, title FROM conversations WHERE username=? ORDER BY id DESC",
            (username,)
        )
        return self.cursor.fetchall()

    def update_title(self, conv_id, title):
        self.cursor.execute(
            "UPDATE conversations SET title=? WHERE id=?",
            (title, conv_id)
        )
        self.conn.commit()

    def add_message(self, conv_id, role, content):
        self.cursor.execute(
            "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (conv_id, role, content, datetime.now().isoformat())
        )
        self.conn.commit()

    def get_messages(self, conv_id, before_id=None, limit=None): # ★ limit 默认值必须是 None
        if limit:
            # 如果有 limit，就按 limit 查
            if before_id is None:
                self.cursor.execute("SELECT id, role, content FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT ?", (conv_id, limit))
            else:
                self.cursor.execute("SELECT id, role, content FROM messages WHERE conversation_id=? AND id < ? ORDER BY id DESC LIMIT ?", (conv_id, before_id, limit))
            rows = self.cursor.fetchall()
            return rows[::-1]
        else:
            # 如果没传 limit，全量拿
            self.cursor.execute("SELECT id, role, content FROM messages WHERE conversation_id=? ORDER BY id", (conv_id,))
            return self.cursor.fetchall()

    # ★★★ 新增：记忆分层相关 ★★★
    def get_summary(self, conv_id):
        """读某对话的摘要"""
        self.cursor.execute(
            "SELECT summary FROM summaries WHERE conversation_id=?",
            (conv_id,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else ""

    def save_summary(self, conv_id, summary):
        """存/更新摘要"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO summaries (conversation_id, summary) VALUES (?, ?)",
            (conv_id, summary)
        )
        self.conn.commit()

    def count_messages(self, conv_id):
        """消息数量"""
        self.cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE conversation_id=?",
            (conv_id,)
        )
        return self.cursor.fetchone()[0]