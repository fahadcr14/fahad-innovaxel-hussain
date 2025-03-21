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
    """
    Generates a short URL
    :param original_url: The original URL
    :return: The short URL
    Logic > By hashing the original URL and taking the first 6 characters of the hash,
    i am generating the short URL
    
    """
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


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original(short_url):
    """Redirects to the original URL"""
    db_conn=sqlite3.connect('urls.db')
    db_cursor=db_conn.cursor()
    db_cursor.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
    original_url = db_cursor.fetchone()
    if original_url:
        db_cursor.execute("UPDATE urls SET access_count = access_count + 1 WHERE short_url = ?", (short_url,))
        db_conn.commit()
        db_conn.close()
        return redirect(original_url[0])
    db_conn.close() #closing the connection
    return jsonify({'error': 'URL not found'}), 404

