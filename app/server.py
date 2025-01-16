import os
import sys

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    if 'pytest' in sys.modules:
        db_name = "test.db"
    else:
        db_name = "prod.db"
    os.makedirs(app.instance_path, exist_ok=True)
    conn = sqlite3.connect(os.path.join(app.instance_path, db_name))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todo').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.json['title']
        conn = get_db_connection()
        conn.execute('INSERT INTO todo (title) VALUES (?)', (title,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todo WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()  # Initialize the in-memory database
    app.run(debug=True)
