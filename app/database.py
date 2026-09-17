import sqlite3

class Database:

    def __init__(self,DataBaseName = "shiva.db"):
        self.DataBaseName = DataBaseName

    def create_tables(self):
        connection = sqlite3.connect(self.DataBaseName)

        cursor = connection.cursor()

        conversations = cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        summary TEXT DEFAULT '',
                        summary_message_id INTEGER DEFAULT 0,
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


    def create_conversation(self):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    INSERT INTO conversations (summary)
                    VALUES (?)""",
                    ("",))
        conversation_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return conversation_id

    def save_messages(self,conversation_id, role, content):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    INSERT INTO messages (conversation_id,role,content)
                    VALUES(?,?,?)
        """,(conversation_id,role,content))
        message_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return message_id


    def get_messages(self,conversation_id):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT id,role,content FROM messages WHERE conversation_id = ? ORDER BY id ASC
        """,(conversation_id,))
        messages = cursor.fetchall()
        connection.close()
        return messages

    def get_conversation(self,conversation_id):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT id,summary,created_at,updated_at FROM conversations WHERE id = ? 
        """,(conversation_id,))
        conversation = cursor.fetchone()
        connection.close()
        return conversation
    
    def get_all_conversations(self):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT id,summary,created_at,updated_at FROM conversations ORDER BY updated_at DESC
        """)
        conversations = cursor.fetchall()
        connection.close()
        return conversations


    def save_summary(self,conversation_id, summary,summary_message_id):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    UPDATE conversations SET summary = ? , summary_message_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
        """,(summary,summary_message_id,conversation_id))
        connection.commit()
        connection.close()

    def load_summary(self,conversation_id):
        connection = sqlite3.connect(self.DataBaseName)
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT summary,summary_message_id FROM conversations WHERE id = ?
        """,(conversation_id,))
        summary = cursor.fetchone()
        connection.close()
        if summary == None :
            raise ValueError(f"conversation with conversation id : {conversation_id} doesn't exist")
        return summary

database = Database()
database.create_tables()