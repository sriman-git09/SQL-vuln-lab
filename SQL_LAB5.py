import sqlite3
import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
REAL_FLAG = "SQL{JS0N_STRUCTUR3_HACK3R}"
# Encrypt the flag to Base64 so it appears as "U1FMe0pTM...=" in the DB
ENCODED_FLAG = base64.b64encode(REAL_FLAG.encode()).decode()

DB_NAME = "saas_logs.db"

# --- DATABASE SETUP (Modern JSON) ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS app_logs")
    # Modern DBs store JSON in TEXT columns
    c.execute('''CREATE TABLE app_logs 
                 (id INTEGER PRIMARY KEY, event_type TEXT, payload TEXT)''')
    
    # 1. Normal Logs (Decoys)
    c.execute("INSERT INTO app_logs (event_type, payload) VALUES (?, ?)", 
              ('login', '{"user": "alice", "ip": "10.0.0.1", "status": "success"}'))
    c.execute("INSERT INTO app_logs (event_type, payload) VALUES (?, ?)", 
              ('purchase', '{"user": "bob", "item": "premium_tier", "cost": 50}'))
    
    # 2. THE TARGET (Hidden inside JSON, Encoded)
    c.execute("INSERT INTO app_logs (event_type, payload) VALUES (?, ?)", 
              ('system_backup', f'{{"admin": "root", "secret_key": "{ENCODED_FLAG}"}}'))
    
    conn.commit()
    conn.close()


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SaaS // Log Explorer</title>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --success: #22c55e; --text: #e2e8f0; --border: #334155; }
        body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; height: 100vh; margin: 0; overflow-y: auto; }
        
        .container { width: 900px; margin-top: 50px; padding-bottom: 50px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .badge { background: #0f172a; border: 1px solid var(--accent); color: var(--accent); padding: 5px 10px; border-radius: 99px; font-size: 0.8rem; }
        
        .card { background: var(--card); padding: 25px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin-bottom: 20px; border: 1px solid var(--border); }
        
       
        .editor { background: #0b1120; padding: 20px; border-radius: 8px; font-family: 'Menlo', monospace; border: 1px solid #334155; }
        .key { color: #7dd3fc; }
        
        input[type="text"] { background: transparent; border: none; border-bottom: 2px solid var(--accent); color: #fff; font-family: inherit; font-size: 1rem; width: 200px; outline: none; text-align: center; }
        
        button { background: var(--accent); color: #0f172a; font-weight: bold; border: none; padding: 10px 25px; border-radius: 6px; cursor: pointer; margin-top: 15px; transition: 0.2s; }
        button:hover { opacity: 0.9; }

      
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { text-align: left; color: #94a3b8; border-bottom: 1px solid #334155; padding: 10px; }
        td { padding: 10px; border-bottom: 1px solid #334155; font-family: monospace; color: #cbd5e1; font-size: 0.9rem; }
        .json-highlight { color: #86efac; word-break: break-all; }

       
        .verify-box { border-color: var(--success); }
        .verify-btn { background: var(--success); color: #fff; }
        
       
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; animation: fadeIn 0.5s; }
        .win-text { font-size: 3rem; color: var(--success); text-shadow: 0 0 20px var(--success); margin-bottom: 10px; }
        
        @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
    </style>
</head>
<body>

    {% if win %}
    <div class="overlay">
        <div class="win-text">SYSTEM HACKED</div>
        <p>Flag Verified: {{ flag }}</p>
        <a href="/" style="color: #666; margin-top: 20px;">Return</a>
    </div>
    {% endif %}

    <div class="container">
        <div class="header">
            <h1>Log Explorer</h1>
            <span class="badge">API v3.0 (JSON-Native)</span>
        </div>

        <div class="card">
            <h3>1. Query Logs</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">Filter the <code>payload</code> JSON column by user.</p>
            
            <form method="GET" action="/api/logs">
                <div class="editor">
                    <span class="key">SELECT</span> * <span class="key">FROM</span> app_logs<br>
                    <span class="key">WHERE</span> json_extract(payload, '$.user') = 
                    "<input type="text" name="user" value="{{ val }}" placeholder="alice">"
                </div>
                <button type="submit">EXECUTE QUERY</button>
            </form>
        </div>

        {% if rows %}
        <div class="card">
            <h4 style="margin-top:0; color:#94a3b8;">Query Results:</h4>
            <table>
                <thead><tr><th>ID</th><th>Type</th><th>JSON Payload</th></tr></thead>
                <tbody>
                    {% for r in rows %}
                    <tr>
                        <td>{{ r[0] }}</td>
                        <td>{{ r[1] }}</td>
                        <td class="json-highlight">{{ r[2] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}

        
        <div class="card verify-box">
            <h3>2. Verify Credentials</h3>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                Found a hidden <code>secret_key</code>
            </p>
            <form method="POST" action="/verify">
                <input type="text" name="flag_attempt" placeholder="SQL{...}" style="border-color: var(--success); width: 300px;">
                <br>
                <button type="submit" class="verify-btn">VERIFY FLAG</button>
            </form>
            {% if error %}
                <div style="color: #ef4444; margin-top: 10px;">{{ error }}</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, val="alice")

@app.route('/api/logs', methods=['GET'])
def get_logs():
    user_input = request.args.get('user', 'alice')
    
    # VULNERABILITY: JSON SQL INJECTION
    # We are injecting ' OR '1'='1 directly into the JSON value string.
    sql = f"SELECT * FROM app_logs WHERE json_extract(payload, '$.user') = '{user_input}'"
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute(sql)
        results = c.fetchall()
    except:
        results = []
    conn.close()
    
    return render_template_string(HTML, rows=results, val=user_input)

@app.route('/verify', methods=['POST'])
def verify_flag():
    attempt = request.form.get('flag_attempt', '').strip()
    
    if attempt == REAL_FLAG:
        return render_template_string(HTML, win=True, flag=REAL_FLAG)
    else:
        return render_template_string(HTML, error="[!] ACCESS DENIED: Incorrect Flag")

if __name__ == '__main__':
    init_db()
    # Runs on port 8088
    app.run(host='0.0.0.0', port=8088, debug=True)
