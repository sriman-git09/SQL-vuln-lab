import os
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)
DB_FILE = "kingdom_lab.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('guest_user', 'guest123'))
        
        cursor.execute("CREATE TABLE kingdom (user_id TEXT, pass TEXT, role TEXT)")
        cursor.execute("INSERT INTO kingdom (user_id, pass, role) VALUES (?, ?, ?)", ('admin@demo-sql.com', 'you_are_hacker-1234', 'admin'))
        cursor.execute("INSERT INTO kingdom (user_id, pass, role) VALUES (?, ?, ?)", ('manager@demo-sql.com', 'mgrPass987!', 'manager'))
        conn.commit()
        conn.close()

# Universal error-free layout wrapper
PAGE_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>Kingdom Secure Portal</title>
    <style>
        body { background: #1e1e24; color: #fff; font-family: sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 650px; margin: 40px auto; background: #2a2a35; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #3a3a45; box-sizing: border-box; }
        h2, h3 { color: #00ffcc; text-shadow: 0 0 5px rgba(0,255,204,0.3); margin-top: 0; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 10px 0; background: #121214; border: 1px solid #444; color: #fff; border-radius: 6px; box-sizing: border-box; font-size: 14px; display: block; }
        input[type="submit"], .btn { background: #00ffcc; color: #121214; padding: 12px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; text-decoration: none; display: block; margin-top: 15px; font-size: 14px; width: 100%; box-sizing: border-box; text-align: center; }
        input[type="submit"]:hover, .btn:hover { background: #00ccaa; }
        .data-box { background: #121214; padding: 15px; border-radius: 6px; border-left: 4px solid #ff3366; font-family: monospace; font-size: 14px; margin-top: 15px; white-space: pre-wrap; color: #eee; }
        .flag { background: #224422; border: 2px dashed #00ff00; padding: 15px; color: #00ff00; font-size: 18px; text-align: center; border-radius: 6px; font-weight: bold; margin-top: 15px; }
        .error { color: #ff3366; font-weight: bold; margin-top: 10px; display: block; }
    </style>
</head>
<body>
    <div class="container">
        {{ body_content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <h2>Kingdom System Gateway</h2>
    <p>Enter your authorization tokens to connect to the internal kingdom registries.</p>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username / Handle" required>
        <input type="password" name="password" placeholder="Access Cipher" required>
        <input type="submit" value="Authenticate Gateway">
    </form>
    """
    if request.args.get('error'):
        content += f"<p class='error'>Database Exception: {request.args.get('error')}</p>"
    if request.args.get('message'):
        content += f"<p class='error'>{request.args.get('message')}</p>"
    return render_template_string(PAGE_LAYOUT, body_content=content)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('home', message="Invalid credentials."))
    except Exception as e:
        conn.close()
        return redirect(url_for('home', error=str(e)))

@app.route('/dashboard')
def dashboard():
    content = """
    <h2>SYSTEM COMPROMISED - GATEWAY GRANTED</h2>
    <p>Welcome! Your entry payload successfully disrupted query structure restrictions.</p>
    <h3>Database Diagnostic Schema Metadata</h3>
    <div class="data-box">
DATABASE NAME: kingdom_lab.db (Active alias context: 'kingdom')

TABLE STRUCT FOUND:
â””â”€â”€ [TABLE] users
â””â”€â”€ [TABLE] kingdom
     â”œâ”€â”€ [COLUMN] user_id
     â”œâ”€â”€ [COLUMN] pass
     â””â”€â”€ [COLUMN] role

DUMPING CONTEXT DATA 'kingdom':
   â–º [ROLE: manager] user_id: manager@demo-sql.com | pass: mgrPass987!
   â–º [ROLE: admin  ] user_id: admin@demo-sql.com   | pass: you_are_hacker-1234
    </div>
    <p style="margin-top:20px;">Use the leaked administrator credentials above to access the master administrative tier.</p>
    <a href="/admin-login" class="btn">Proceed to Admin Login Control</a>
    """
    return render_template_string(PAGE_LAYOUT, body_content=content)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kingdom WHERE user_id = ? AND pass = ? AND role = 'admin'", (user_id, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            return redirect(url_for('flag_page'))
            
        content = """
        <h2 class="error">Authentication Rejected</h2>
        <p>The administrative terminal did not accept those specific credentials.</p>
        <a href="/admin-login" class="btn">Try Again</a>
        """
        return render_template_string(PAGE_LAYOUT, body_content=content)

    # FINAL PERFECTED HTML FORM STRINGS WITH EXPLICIT VALUES AND INTEGRATED SUBMIT BUTTON
    content = """
    <h2>Master Administrative Console</h2>
    <p>Restricted access point. Enter high-level manager or administrative credentials.</p>
    <form method="POST" action="/admin-login">
        <input type="text" name="user_id" placeholder="Admin User ID" required>
        <input type="password" name="password" placeholder="Administrative Keyphrase" required>
        <input type="submit" value="Authenticate Admin">
    </form>
    """
    return render_template_string(PAGE_LAYOUT, body_content=content)

@app.route('/flag')
def flag_page():
    content = """
    <h2>ðŸ‘‘ LEVEL COMPLETE - ADMINISTRATIVE CONTROL GAINED</h2>
    <p>You have successfully extracted keys from the backend database environment using web analysis techniques.</p>
    <div class="flag">
        SUCCESS FLAG: SQL{your_database_hacked}
    </div>
    <br>
    <a href="/" class="btn">Reset Lab Gateway</a>
    """
    return render_template_string(PAGE_LAYOUT, body_content=content)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
