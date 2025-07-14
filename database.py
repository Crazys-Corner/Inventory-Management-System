import sqlite3

conn = sqlite3.connect('test.db', check_same_thread=False) # Unsafe for production use, use fastapi depends 

cursor = conn.cursor()


__all__ = ["conn", "cursor"]