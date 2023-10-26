import sqlite3
from sqlite3 import Error

DATABASE_NAME = 'notes.db'

def create_connection():
    """ Создает соединение с базой данных SQLite """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except Error as e:
        print(e)
    return conn

def init_db():
    """ Инициализирует базу данных """
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT
            )
        """)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def add_note(title, content):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(title, content) VALUES (?, ?)", (title, content))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_all_notes():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM notes")
        return cursor.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def search_notes(keyword):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM notes WHERE content LIKE ?", ('%' + keyword + '%',))
        return cursor.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_note_content(title):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM notes WHERE title=?", (title,))
        return cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def delete_note(title):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE title=?", (title,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def close():
    conn = create_connection()
    if conn:
        conn.close()
