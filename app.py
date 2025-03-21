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



def generate_short_url(original_url):
    """Generates a short URL"""
    return hashlib.md5(original_url.encode()).hexdigest()[:6]


@app.route('/shorten', methods=['POST'])
def shorten():
    """Shortens a URL"""
    data = request.get_json()
    original_url = data['url']
    short_url = generate_short_url(original_url)
    db_conn=sqlite3.connect('urls.db')
    db_cursor=db_conn.cursor()
    db_cursor.execute("INSERT INTO urls (short_url, original_url) VALUES (?, ?)", (short_url, original_url))
    db_conn.commit()
    db_conn.close()
    return jsonify({'short_url': short_url})
