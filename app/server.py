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
    todos = conn.execute('SELECT * FROM todo ORDER BY position ASC').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']  # Use request.form to get form data instead of JSON. 
        # Alternative is to update the frontend to support JSON request i.e. AJAX 
        # or fetch with custom payload
        conn = get_db_connection()
        latestTodo = conn.execute('SELECT * FROM todo ORDER BY position DESC LIMIT 1').fetchone()
        # New inserts will + 1 to the last one. Not really ideal in multithreaded applications but
        # will do for a small sample app
        position = 1 if latestTodo is None else latestTodo['position'] + 1
        conn.execute('INSERT INTO todo (title, position) VALUES (?, ?)', (title, position))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/move/<int:id>/<string:direction>', methods=(['GET']))
def move(id, direction):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()
    
    if todo is None:
        conn.close()
        return redirect(url_for('index'))
    
    if direction == 'up':
        # Get the previous todo by position
        previousTodo = conn.execute('SELECT * FROM todo WHERE position < ? ORDER BY position DESC LIMIT 1', (todo['position'],)).fetchone()
        if (previousTodo is None): # If there is no previous todo, do nothing
            conn.close()
            return redirect(url_for('index'))
        conn.execute('BEGIN TRANSACTION')
        conn.execute('UPDATE todo SET position = ? WHERE id = ?', (todo['position'], previousTodo['id']))
        conn.execute('UPDATE todo SET position = ? WHERE id = ?', (previousTodo['position'], todo['id']))
        conn.commit()
    elif direction == 'down':
        # Get the next todo by position
        nextTodo = conn.execute('SELECT * FROM todo WHERE position > ? ORDER BY position ASC LIMIT 1', (todo['position'],)).fetchone()
        if (nextTodo is None): # If there is no next todo, do nothing
            conn.close()
            return redirect(url_for('index'))
        conn.execute('BEGIN TRANSACTION')
        conn.execute('UPDATE todo SET position = ? WHERE id = ?', (todo['position'], nextTodo['id']))
        conn.execute('UPDATE todo SET position = ? WHERE id = ?', (nextTodo['position'], todo['id']))
        conn.commit()
    else:
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return redirect(url_for('index'))

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
