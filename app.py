from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT,
        short TEXT UNIQUE,
        clicks INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()


def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.json
    original_url = data.get("url")

    short_code = generate_code()

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO urls (original, short) VALUES (?, ?)",
              (original_url, short_code))
    conn.commit()
    conn.close()

    return jsonify({
        "short_url": f"http://localhost:5000/{short_code}"
    })


@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT original, clicks FROM urls WHERE short=?", (short_code,))
    row = c.fetchone()

    if not row:
        return jsonify({"message": "Not found"}), 404

    original_url, clicks = row

    c.execute("UPDATE urls SET clicks=? WHERE short=?",
              (clicks + 1, short_code))
    conn.commit()
    conn.close()

    return redirect(original_url)


@app.route("/stats/<short_code>")
def stats(short_code):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT original, clicks FROM urls WHERE short=?", (short_code,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "Not found"}), 404

    return jsonify({
        "original_url": row[0],
        "clicks": row[1]
    })


if __name__ == "__main__":
    app.run(debug=True)
