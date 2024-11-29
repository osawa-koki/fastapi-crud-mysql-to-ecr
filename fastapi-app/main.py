import os

from fastapi import FastAPI
from pydantic import BaseModel

import mysql.connector


class Item(BaseModel):
    name: str


app = FastAPI()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_items():
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items;")
    return {"items": cursor.fetchall()}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items WHERE id = %s;", (item_id,))
    return {"item": cursor.fetchone()}


@app.post("/items")
def create_item(item: Item):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s);", (item.name,))
    item_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT id, name FROM items WHERE id = %s;", (item_id,))
    return {"item": cursor.fetchone()}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name = %s WHERE id = %s;",
        (item.name, item_id)
    )
    conn.commit()

    cursor.execute("SELECT id, name FROM items WHERE id = %s;", (item_id,))
    return {"item": cursor.fetchone()}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()

    return {"item": None}


@app.get("/databases")
def get_databases():
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    return {"databases": cursor.fetchall()}
