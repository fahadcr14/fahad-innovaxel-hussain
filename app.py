from flask import Flask, request, jsonify, redirect, render_template
import hashlib
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import random
import string

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("SHORTURL_POSTGRES_DATABASE"),
        user=os.getenv("SHORTURL_POSTGRES_USER"),
        password=os.getenv("SHORTURL_POSTGRES_PASSWORD"),
        host=os.getenv("SHORTURL_POSTGRES_HOST"),
        port="5432",  
        sslmode="require"
    )
    return conn

def db_init():
    """Initializes the database"""
    with get_db_connection() as db_conn:
        db_cursor=db_conn.cursor()
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                shortCode TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                access_count INTEGER DEFAULT 0,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db_cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_shortCode ON urls (shortCode)
    """)
        db_conn.commit()
 
  

def return_json(row_data):
    
    row_json={'shortCode': row_data[0], 'original_url': row_data[1], 'access_count': row_data[2], 'createdAt': row_data[3], 'updatedAt': row_data[4]}
    if row_data:
        return row_json

def generate_shortCode(original_url):
    """
    Generates a short URL
    :param original_url: The original URL
    :return: The short URL
    Logic > By hashing the original URL and taking the first 6 characters of the hash,
    i am generating the short URL
    >> added salt because of original updated but short code same when original again post it gives error so use salt 
    """
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    hash_input = (original_url + salt).encode()

    return hashlib.md5(hash_input).hexdigest()[:6]

def is_url_exist(db_cursor,shorten_url="", original_url=""):
    """Check if the URL already exists in the database"""
    if shorten_url:
        db_cursor.execute("SELECT shortCode FROM urls WHERE shortCode = %s", (shorten_url,))
    else:
        db_cursor.execute("SELECT shortCode FROM urls WHERE original_url = %s", (original_url,))
    existing_shortCode = db_cursor.fetchone()
    if existing_shortCode:
        return existing_shortCode[0]
    return None
@app.route('/shorten', methods=['POST'])
def shorten():
    """Shortens a URL"""
    data = request.get_json()
    original_url = data['url']
    shortCode = f"{generate_shortCode(original_url)}"
    with get_db_connection() as db_conn:
        db_cursor=db_conn.cursor()
        try: 
            existing_shortCode = is_url_exist(db_cursor,original_url=original_url)
            if existing_shortCode:
                return jsonify({'shortCode': existing_shortCode,"message":"URL already exists"}),200
        except psycopg2.Error as e:
            return jsonify({'error': str(e)}), 500
        attempt=0
        while True:
            if attempt>10:
                return jsonify({'error': 'Failed to shorten the URL'}), 500
            try:
                db_cursor.execute("INSERT INTO urls (shortCode, original_url) VALUES (%s, %s)", (shortCode, original_url))
                db_conn.commit()
                db_cursor.execute("SELECT * FROM urls WHERE shortCode = %s", (shortCode,))
                row_data = db_cursor.fetchone()

                return jsonify(return_json(row_data)),201
            except psycopg2.IntegrityError:
                attempt+=1
                shortCode = f"{generate_shortCode(original_url)}"
                continue
            
        


@app.route('/<shorten_url>', methods=['GET'])
def redirect_to_original(shorten_url):
    """Redirects to the original URL"""
    with get_db_connection() as db_conn:
        db_cursor=db_conn.cursor()
        db_cursor.execute("SELECT original_url FROM urls WHERE shortCode = %s", (shorten_url,))
        original_url = db_cursor.fetchone()
        if original_url:
            db_cursor.execute("UPDATE urls SET access_count = access_count + 1 WHERE shortCode = %s", (shorten_url,))
            db_conn.commit()
            return redirect(original_url[0]),302
        return jsonify({'error': 'URL not found'}), 404


@app.route('/stats/<shorten_url>/' , methods=["GET"])
def get_stats_of_url(shorten_url):
    """
    Get the stats of a URL
    Takes the short url from url slug and returns the access count of the URL
    """
    with get_db_connection() as db_conn:
        db_cursor=db_conn.cursor()
        if not is_url_exist(db_cursor,shorten_url=shorten_url):
                return jsonify({'error': 'URL not exists'}),404
        db_cursor.execute("SELECT * FROM urls WHERE shortCode = %s", (shorten_url,))
        row_data = db_cursor.fetchone()
        # print(row_data)

        try:
            return return_json(row_data),200   
        except psycopg2.Error as e:
            return jsonify({'error': 'URL not found'}), 404

@app.route('/<shorten_url>/', methods=["DELETE"])
def delete_url(shorten_url):
    """
    Deletes a URL
    Takes the short url from url slug and deletes the URL from the database
    """
    with get_db_connection() as db_conn:
        db_cursor=db_conn.cursor()
        try:
            db_cursor.execute("DELETE FROM urls WHERE shortCode = %s", (shorten_url,))
            db_conn.commit()

            return  jsonify({'message': 'URL deleted'}),204
        except psycopg2.Error as e:
            return jsonify({'error': str(e)}), 500
    
@app.route("/shorten/<shorten_url>/", methods=["PUT"])
def update_url(shorten_url):
    """
    Updates a URL
    Takes the short url from url slug and updates the URL in the database
    """
    data = request.get_json()
    new_url = data['url']
    with get_db_connection() as db_conn:
        db_cursor=db_conn.cursor()
        try:
            if not is_url_exist(db_cursor,shorten_url=shorten_url):
                return jsonify({'error': 'URL not exists'}),404
            db_cursor.execute("""
            UPDATE urls 
            SET original_url = %s, updatedAt = %s 
            WHERE shortCode = %s
        """, (new_url, datetime.now(), shorten_url))
            db_conn.commit()
            db_cursor.execute("SELECT * FROM  urls WHERE shortCode = %s",(shorten_url,))
            row_data = db_cursor.fetchone()

            return jsonify(return_json(row_data)),200
        except psycopg2.Error as e:
            return jsonify({'error': str(e)}), 400
    
@app.route("/")
def index():
     return render_template('index.html')

if __name__ == '__main__':
    db_init()
    app.run(debug=True)