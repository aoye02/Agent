import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="chat.db"):
        self.conn = sqlite3.connect(db_path)
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

    def get_messages(self, conv_id):
        self.cursor.execute(
            "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id",
            (conv_id,)
        )
        return self.cursor.fetchall()