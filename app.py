from flask import Flask, request, jsonify, redirect, url_for
import hashlib
import sqlite3

app = Flask(__name__)




def db_init():
    """Initializes the database"""
    db_conn=sqlite3.connect('urls.db')
    db_cursor=db_conn.cursor()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, short_url TEXT UNIQUE, original_url TEXT, access_count INTEGER DEFAULT 0)")
    db_conn.commit()
    db_conn.close()
