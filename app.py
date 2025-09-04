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

# Route add Buku
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun_terbit = request.form['tahun_terbit']
        conn = get_db_connection()
        conn.execute('INSERT INTO Buku (judul, penulis, tahun_terbit) VALUES (?, ?, ?)',
                     (judul, penulis, tahun_terbit))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Buku WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Edit Route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    buku = conn.execute('SELECT * FROM Buku WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun_terbit = request.form['tahun_terbit']
        conn.execute('UPDATE Buku SET judul = ?, penulis = ?, tahun_terbit = ? WHERE id = ?',
                     (judul, penulis, tahun_terbit, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit.html', buku=buku)
    
 
# main method for flask
if __name__ == '__main__':
    app.run(debug=True)