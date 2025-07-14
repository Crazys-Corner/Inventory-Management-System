from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import database

app = FastAPI()

class Item(BaseModel):
    name: str
    value: float
    isInUse: bool
    client: str



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/seed")
def read_seed():
    database.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               value REAL NOT NULL,
               inuse BOOLEAN NOT NULL,
               client TEXT NOT NULL
               )
               '''
               )
    database.conn.commit()
    database.cursor.execute('''
    INSERT INTO items (name, value, inuse, client) VALUES ('laptop', 2000, 0, 'bob')
                            ''')
    database.conn.commit()
    rows = database.cursor.execute("SELECT * FROM items").fetchall()
    items = [
        {
            "id": row[0],
            "name": row[1],
            "value": row[2],
            "isInUse": bool(row[3]),
            "client": row[4]
        } for row in rows
    ]
    return items

@app.get("/inventory/items", response_model=List[Item])
def read_items():
    rows = database.cursor.execute("SELECT * FROM items").fetchall()
    items = [
        {
            "id": row[0],
            "name": row[1],
            "value": row[2],
            "isInUse": bool(row[3]),
            "client": row[4]
        } for row in rows
    ]
    return items

@app.post("/inventory/items")
def add_item(item: Item):
    database.cursor.execute(
        "INSERT INTO items (name, value, inuse, client) VALUES (?, ?, ?, ?)",
        (item.name, item.value, item.isInUse, item.client)
    )
    database.conn.commit()
    return {"Result": "Success",
            "Message": f"Added: {item.name}"}

