 import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB_FILE = "secure_app.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'ExampleSecurePass123!'))
        conn.commit()
        conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html><html><head><title>Vulnerable Login</title>
<style>body{background:#f4f4f4;font-family:sans-serif;} .container{max-width:400px;margin:50px auto;background:#fff;padding:20px;border-radius:8px;box-shadow: 0 2px 5px rgba(0,0,0,0.1);}</style>
</head><body><div class="container">
<h2>Vulnerable Login Portal</h2>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username" required style="width:100%;margin-bottom:10px;"><br>
<input type="password" name="password" placeholder="Password" required style="width:100%;margin-bottom:10px;"><br>
<input type="submit" value="Log In">
</form>
{% if message %}<p>{{ message }}</p>{% endif %}
</div></body></html>"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Broken concatenation logic
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template_string(HTML_TEMPLATE, message=f"Welcome, {user}!")
    else:
        return render_template_string(HTML_TEMPLATE, message="Invalid credentials.")

if __name__ == '__main__':
    init_db()
    # Accept connections across your home network router
    app.run(host='0.0.0.0', port=8080)

