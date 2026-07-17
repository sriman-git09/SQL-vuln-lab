import sqlite3
import base64
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'vault_os_secure_key_2026'

REAL_FLAG = "SQL{TRU5T_N0_D4T4_FR0M_TH3_DB}"
ENCODED_FLAG = base64.b64encode(REAL_FLAG.encode()).decode()
DB_NAME = "vault_bank.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
 
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, is_admin INTEGER)")
    
    c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
              ('admin', '73884351992_sup3r_s3cur3_h4sh!', 1))
    
    conn.commit()
    conn.close()


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Vault/OS | Corporate Banking</title>
    <style>
        :root { --bg: #050505; --card: #111; --border: #333; --accent: #00f0ff; --text: #eee; --danger: #ff0055; }
        body { background: var(--bg); color: var(--text); font-family: 'SF Mono', 'Segoe UI Mono', monospace; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        
        .interface { width: 450px; border: 1px solid var(--border); padding: 40px; border-radius: 4px; box-shadow: 0 0 40px rgba(0,0,0,0.8); background: var(--card); position: relative; overflow: hidden; }
        
        h1 { font-size: 1.2rem; letter-spacing: 2px; text-transform: uppercase; border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-top: 0; display: flex; justify-content: space-between; color: var(--accent); }
        
        /* Forms */
        .input-group { margin-bottom: 20px; }
        label { display: block; font-size: 0.7rem; color: #666; margin-bottom: 8px; text-transform: uppercase; }
        input { width: 100%; background: #000; border: 1px solid #333; color: #fff; padding: 15px; font-family: inherit; box-sizing: border-box; transition: 0.2s; }
        input:focus { border-color: var(--accent); outline: none; }
        
        button { width: 100%; background: var(--text); color: #000; border: none; padding: 15px; font-weight: bold; cursor: pointer; font-family: inherit; text-transform: uppercase; letter-spacing: 1px; }
        button:hover { background: var(--accent); }
        
        .secondary-btn { background: transparent; border: 1px solid #333; color: #666; margin-top: 10px; }
        .secondary-btn:hover { border-color: var(--text); color: var(--text); background: transparent; }

        /* Status & Logs */
        .status-bar { margin-top: 30px; padding: 15px; background: #0a0a0a; border: 1px solid #222; font-size: 0.75rem; color: #555; }
        .highlight { color: var(--accent); }
        .error { color: var(--danger); }
        
        /* Admin Panel */
        .admin-panel { text-align: center; border: 1px solid var(--accent); padding: 30px; margin-top: 20px; background: rgba(0, 240, 255, 0.05); }
        .blur-flag { filter: blur(4px); user-select: none; }
    </style>
</head>
<body>

    <div class="interface">
        <h1>Vault/OS <span>v9.0</span></h1>

        {% if session_user %}
            <!-- LOGGED IN DASHBOARD -->
            <p>USER_ID: <strong style="color:#fff">{{ session_user }}</strong></p>
            <p>ROLE: 
                {% if is_admin %}
                    <span style="color:var(--accent); font-weight:bold;">SUPER_ADMIN</span>
                {% else %}
                    <span style="color:#666;">STANDARD_USER</span>
                {% endif %}
            </p>

            {% if is_admin %}
                <div class="admin-panel">
                    <h3>// CRITICAL ASSET //</h3>
                    <p>DECRYPTED FLAG:</p>
                    <div style="font-size: 1.2rem; margin: 20px 0; color: var(--accent);">{{ flag }}</div>
                    <p style="font-size: 0.7rem;">System Compromised.</p>
                </div>
            {% else %}
                <div class="status-bar">
                    ACCESS DENIED to Core System.<br>
                    Only 'admin' can view the flag.
                </div>
            {% endif %}

            <div style="margin-top: 40px; border-top: 1px solid #333; padding-top: 20px;">
                <label>Security Settings: Reset Password</label>
                <form method="POST" action="/change_password">
                    <input type="text" name="new_password" placeholder="Enter New Password">
                    <button type="submit" style="margin-top:10px;">UPDATE CREDENTIALS</button>
                </form>
            </div>
            
            <a href="/logout"><button class="secondary-btn">TERMINATE SESSION</button></a>

        {% else %}
            <!-- LOGIN / REGISTER -->
            <div id="auth-forms">
                <!-- Login Form -->
                <form method="POST" action="/login">
                    <div class="input-group">
                        <label>Identity</label>
                        <input type="text" name="username" placeholder="username">
                    </div>
                    <div class="input-group">
                        <label>Key</label>
                        <input type="password" name="password" placeholder="••••••">
                    </div>
                    <button type="submit">Authenticate</button>
                </form>

                <div style="text-align: center; margin: 20px 0; font-size: 0.8rem; color: #444;">— OR —</div>

                <!-- Register Form -->
                <form method="POST" action="/register">
                    <div class="input-group">
                        <input type="text" name="reg_username" placeholder="New Username" style="border-style: dashed;">
                    </div>
                    <div class="input-group">
                        <input type="password" name="reg_password" placeholder="New Password" style="border-style: dashed;">
                    </div>
                    <button type="submit" class="secondary-btn">Initialize New Identity</button>
                </form>
            </div>
        {% endif %}

        <!-- System Log Output -->
        {% if msg %}
            <div class="status-bar">
                SYSTEM_MSG: <span class="{{ msg_type }}">{{ msg }}</span>
            </div>
        {% endif %}
    </div>

</body>
</html>
"""


@app.route('/')
def home():
    user = session.get('username')
    is_admin = False
    flag = None
    
    if user:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT is_admin FROM users WHERE username = ?", (user,))
        row = c.fetchone()
        conn.close()
        
        if row and row[0] == 1:
            is_admin = True
            flag = REAL_FLAG
            
    return render_template_string(HTML, session_user=user, is_admin=is_admin, flag=flag, msg=request.args.get('msg'), msg_type=request.args.get('type'))

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pw = request.form.get('password')
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pw))
    account = c.fetchone()
    conn.close()
    
    if account:
        session['username'] = user
        return redirect('/')
    else:
        return redirect('/?msg=Invalid Credentials&type=error')

@app.route('/register', methods=['POST'])
def register():
    user = request.form.get('reg_username')
    pw = request.form.get('reg_password')
    
    if not user or not pw:
        return redirect('/?msg=Fields cannot be empty&type=error')

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, 0)", (user, pw))
        conn.commit()
        conn.close()
        return redirect('/?msg=Identity Created. Please Login.&type=highlight')
    except sqlite3.IntegrityError:
        return redirect('/?msg=Username already exists.&type=error')

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' not in session: return redirect('/')
    
    new_pw = request.form.get('new_password')
    current_user = session['username']
    
    sql = f"UPDATE users SET password = '{new_pw}' WHERE username = '{current_user}'"
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        
        c.executescript(sql)
        conn.commit()
        msg = f"Credentials updated for {current_user}"
    except Exception as e:
        msg = f"Database Error: {e}"
    conn.close()
    
   
    session.clear()
    return redirect(f'/?msg={msg}&type=highlight')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    print("[+] Vault/OS Running on your local network")
    app.run(host='0.0.0.0', port=8093, debug=True)
