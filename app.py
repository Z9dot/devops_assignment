from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = 'sample.db'

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Simple App</title></head>
<body>
    <h1>Welcome to the Sample App</h1>
    <form action="/add" method="post">
        <input type="text" name="item" placeholder="Enter item" required>
        <button type="submit">Add</button>
    </form>
    <ul>
        {% for item in items %}
            <li>{{ item[1] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
'''

def get_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    return conn

@app.route('/', methods=['GET'])
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template_string(HTML, items=items)

@app.route('/add', methods=['POST'])
def add():
    item = request.form['item']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (item,))
    conn.commit()
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
