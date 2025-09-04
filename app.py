import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

DATABASE = 'buku.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS Buku (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        penulis TEXT NOT NULL,
        tahun_terbit INTEGER NOT NULL
    )''')
    conn.commit()
    
# Route Home
@app.route('/')
def index():
    conn = get_db_connection()
    buku = conn.execute('SELECT * FROM Buku').fetchall()
    conn.close()
    return render_template('index.html', buku=buku)
    
# main method for flask
if __name__ == '__main__':
    app.run(debug=True)