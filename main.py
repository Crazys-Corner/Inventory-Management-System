from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3 
import database

#added client data

app = FastAPI()

class Item(BaseModel):
    id: int     
    name: str
    value: float
    isInUse: bool
    client: str

class Clientell(Item):
    id: int
    firstname: str
    lastname: str
    address: str
    city: str
    state: str
    zipcode: str


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
               );
            CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                    first_name TEXT NOT NULL
                    last_name TEXT NOT NULL
                    address TEXT NOT NULL
                    city TEXT NOT NULL
                    state TEXT NOT NULL
                    zip_code TEXT NOT NULL
                            )
               '''
               )
    database.conn.commit()
    database.cursor.execute('''
    INSERT INTO items (name, value, inuse, client) VALUES ('laptop', 2000, 0, 'bob');
    INSERT INTO clients (first_name, last_name, address, city, state, zip_code) VALUES ('rando', 'lastname', 'some address', 'coralsprings', 'fl', 9999)
                             ''')
    database.conn.commit()
    rows = database.cursor.execute("SELECT * FROM items").fetchall()

    rows2 = database.cursor.execute("SELECT * FROM clients").fetchall()
    items = [
        {
            "id": row[0],
            "name": row[1],
            "value": row[2],
            "isInUse": bool(row[3]),
            "client": row[4]
        } for row in rows
    ]
    clientell = [
        {
            "first_name": row2[0],
            "last_name": row2[1],
            "address": row2[2],
            "city" : row2[3],
            "state": row2[4],
            "zip_code": row2[5]
        } for row2 in rows2
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


@app.get("/inventory/clients", response_model=List[Clientell])
def read_clients():
    rows2 = database.cursor.execute("SELECT * FROM clients").fetchall()
    clientell = [
        {
            "first_name": row2[0],
            "last_name": row2[1],
            "address": row2[2],
            "city" : row2[3],
            "state": row2[4],
            "zip_code": row2[5]
        } for row2 in rows2
    ]
    return clientell

@app.post("/inventory/items")
def add_item(item: Item):
    database.cursor.execute(
        "INSERT INTO items (name, value, inuse, client) VALUES (?, ?, ?, ?)",
        (item.name, item.value, item.isInUse, item.client)
    )
    database.conn.commit()
    return {"Result": "Success",
            "Message": f"Added: {item.name}"}


@app.post("/inventory/clients")
#add clients 
def add_client(client: Clientell):
    database.cursor.execute(
        "INSERT INTO clients (first_name, last_name, address, city, state, zip_code) VALUES (?, ?, ?, ?, ?, ?)",
        (client.firstname, client.lastname, client.address, client.city, client.state, client.zipcode)
    )
    database.conn.commit()
    return {"Result": "Success",
            "Message": f"Added: {client.firstname}"}

@app.delete("/inventory/items/{item_id}")
def delete_item(item_id: int):
    database.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = database.cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    database.cursor.execute("DELETE FROM items WHERE id = ? ", (item_id,))
    database.conn.commit()
    return {"result": "success", "message": f"Item with ID {item_id} deleted"}



@app.delete("/inventory/clients/{client_id}")
def delete_item(client_id: int):
    database.cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    item = database.cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="Client not found")
    database.cursor.execute("DELETE FROM clients WHERE id = ? ", (client_id,))
    database.conn.commit()
    return {"result": "success", "message": f"Client with ID {client_id} deleted"}



@app.put('/inventory/items/{item_id}')
def update_item(item_id: int, item: Item):
    database.cursor.execute(
        "UPDATE items SET name = ?, value = ?, inuse = ?, client = ? WHERE id = ?",
        (item.name, item.value, item.isInUse, item.client, item_id)
    )
    database.conn.commit()

    rows = database.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchall()
    itemContent = [
        {
            "id": row[0],
            "name": row[1],
            "value": row[2],
            "isInUse": bool(row[3]),
            "client": row[4]
        } for row in rows
    ]
    return {
        "result": "success",
        "message": f"Updated {item.name}",
        "content": itemContent
    }



@app.put('/inventory/clients/{client_id}')
def update_client(client_id: int, client: Clientell):
    database.cursor.execute(
        "UPDATE clients SET first_name = ?, last_name = ?, address = ?, city = ?, state = ?, zip_code WHERE id = ?",
        (client.firstname, client.lastname, client.address, client.city, client.state, client.zipcode)
    )
    database.conn.commit()

    rows2 = database.cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchall()
    clientell_content = [
        {
            "first_name": row2[0],
            "last_name": row2[1],
            "address": row2[2],
            "city" : row2[3],
            "state": row2[4],
            "zip_code": row2[5]
        } for row2 in rows2
    ]
    return {
        "result": "success",
        "message": f"Updated {client.name}",
        "content": clientell_content
    }
