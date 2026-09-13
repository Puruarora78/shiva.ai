import sqlite3

DataBaseName = "shiva.db"


def create_tables():
    connection = sqlite3.connect(DataBaseName)

    cursor = connection.cursor()

    conversations = cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
    messages = cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                    )
                """)

    connection.commit()
    connection.close()


def create_conversation():
    connection = sqlite3.connect(DataBaseName)
    cursor = connection.cursor()
    cursor.execute("""
                INSERT INTO conversations (summary)
                VALUES (?)""",
                   ("",))
    conversation_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return conversation_id

def save_messages(conversation_id, role, content):
    connection = sqlite3.connect(DataBaseName)
    cursor = connection.cursor()
    cursor.execute("""
                INSERT INTO messages (conversation_id,role,content)
                VALUES(?,?,?)
    """,(conversation_id,role,content))
    connection.commit()
    connection.close()


def get_messages(conversation_id):
    connection = sqlite3.connect(DataBaseName)
    cursor = connection.cursor()
    cursor.execute("""
                SELECT role,content FROM messages WHERE conversation_id = ? ORDER BY id ASC
    """,(conversation_id,))
    messages = cursor.fetchall()
    connection.close()
    return messages

def get_conversation(conversation_id):
    connection = sqlite3.connect(DataBaseName)
    cursor = connection.cursor()
    cursor.execute("""
                SELECT id,summary,created_at,updated_at FROM conversations WHERE id = ? 
    """,(conversation_id,))
    conversation = cursor.fetchone()
    connection.close()
    return conversation

def save_summary(conversation_id, summary):
    connection = sqlite3.connect(DataBaseName)
    cursor = connection.cursor()
    cursor.execute("""
                UPDATE conversations SET summary = ? , updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """,(summary,conversation_id))
    connection.commit()
    connection.close()

def load_summary(conversation_id):
    connection = sqlite3.connect(DataBaseName)
    cursor = connection.cursor()
    cursor.execute("""
                SELECT summary FROM conversations WHERE id = ?
    """,(conversation_id,))
    summary = cursor.fetchone()
    connection.close()
    if summary == None :
        raise ValueError(f"conversation with conversation id : {conversation_id} doesn't exist")
    return summary[0] 
