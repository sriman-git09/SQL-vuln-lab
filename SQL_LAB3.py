import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- Configuration ---
FLAG = "SQL{BL1ND_SQL_1NJ3CT!0N}"  # The secret they need to steal
DB_NAME = "kingdom_lab.db"

# --- Database Setup ---
def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, secret_data TEXT)''')
        
        # Check if admin exists
        c.execute("SELECT * FROM users WHERE username = 'admin'")
        if not c.fetchone():
            # Inject the flag into the database so it can be stolen via SQLi
            c.execute("INSERT INTO users (username, password, secret_data) VALUES (?, ?, ?)", 
                      ('admin', 'super_secure_p4ss', FLAG))
            c.execute("INSERT INTO users (username, password, secret_data) VALUES (?, ?, ?)", 
                      ('guest', 'guest', 'nothing_here'))
            conn.commit()
            print(f"[+] Database initialized. The Flag is hidden in the 'secret_data' column.")
        conn.close()
    except Exception as e:
        print(f"[-] Database Error: {e}")

# --- Modern UI Template ---
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab 3: The Blind Oracle</title>
    <style>
        :root {
            --bg: #0a0a0f;
            --card: #13131f;
            --accent: #00f3ff; /* Cyan Neon */
            --danger: #ff0055;
            --success: #00ff88;
            --text: #e0e0e0;
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000 100%);
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: rgba(19, 19, 31, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid #333;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 0 40px rgba(0, 243, 255, 0.05);
            animation: fadeIn 0.8s ease-out;
        }
        h1 { margin: 0 0 5px 0; font-weight: 300; letter-spacing: 2px; color: #fff; }
        h2 { font-size: 0.9rem; color: #666; text-transform: uppercase; margin-bottom: 2rem; letter-spacing: 1px; }
        
        .panel {
            background: #0f0f16;
            border: 1px solid #2a2a35;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            position: relative;
        }
        .panel-title {
            position: absolute;
            top: -10px;
            left: 15px;
            background: var(--bg);
            padding: 0 10px;
            font-size: 0.75rem;
            color: var(--accent);
            text-transform: uppercase;
            font-weight: bold;
        }

        /* Forms */
        input[type="text"] {
            width: 100%;
            background: #1a1a22;
            border: 1px solid #333;
            color: #fff;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            box-sizing: border-box;
            transition: all 0.3s;
            font-family: monospace;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
        }
        button {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.1s;
        }
        .btn-query { background: #222; color: var(--accent); border: 1px solid var(--accent); }
        .btn-query:hover { background: rgba(0, 243, 255, 0.1); }
        .btn-submit { background: var(--accent); color: #000; }
        .btn-submit:hover { opacity: 0.9; }

        /* Status Indicators */
        .status {
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
            font-size: 0.9rem;
            text-align: center;
        }
        .status-yes { background: rgba(0, 255, 136, 0.1); color: var(--success); border: 1px solid var(--success); }
        .status-no { background: rgba(255, 0, 85, 0.1); color: var(--danger); border: 1px solid var(--danger); }

        /* Victory Screen */
        .victory-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 999;
            animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .trophy { font-size: 4rem; margin-bottom: 1rem; filter: drop-shadow(0 0 20px var(--success)); }
        .win-text { font-size: 2rem; color: var(--success); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 5px; }
        .flag-display { background: #111; padding: 1rem 2rem; border: 1px solid var(--success); font-family: monospace; font-size: 1.2rem; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes popIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    </style>
</head>
<body>

    <!-- SUCCESS OVERLAY (Only shows if solved) -->
    {% if success %}
    <div class="victory-overlay">
        <div class="trophy">🏆</div>
        <div class="win-text">System Compromised</div>
        <p style="color: #888;">You have successfully extracted the secret.</p>
        <div class="flag-display">{{ success_flag }}</div>
        <br>
        <a href="/" style="color: #666; text-decoration: none;">Return to Lab</a>
    </div>
    {% endif %}

    <div class="container">
        <h1>SQL LAB <span style="color:var(--accent)">03</span></h1>
        <h2>Blind Injection / Extraction</h2>

        <!-- PART 1: THE VULNERABLE ORACLE -->
        <div class="panel">
            <span class="panel-title">The Oracle</span>
            <p style="font-size: 0.85rem; color: #888; margin-top: 0;">
                The database will verify if a user exists, but it will <strong>never</strong> show you the data. 
                <br><em>Ask True/False questions to steal the 'secret_data' column.</em>
            </p>
            <form method="GET" action="/check">
                <input type="text" name="query" placeholder="e.g. admin' AND 1=1 --" value="{{ query_val }}">
                <button type="submit" class="btn-query">QUERY SYSTEM</button>
            </form>

            {% if oracle_response == 'YES' %}
                <div class="status status-yes">Permissions: <strong>GRANTED</strong> (True)</div>
            {% elif oracle_response == 'NO' %}
                <div class="status status-no">Permissions: <strong>DENIED</strong> (False)</div>
            {% endif %}
        </div>

        <!-- PART 2: THE VERIFICATION -->
        <div class="panel" style="margin-bottom: 0;">
            <span class="panel-title">Decryptor</span>
            <p style="font-size: 0.85rem; color: #888; margin-top: 0;">
                Enter the extracted secret to claim the flag.
            </p>
            <form method="POST" action="/solve">
                <input type="text" name="flag_attempt" placeholder=" ">
                <button type="submit" class="btn-submit">VERIFY FLAG</button>
            </form>
            {% if fail_msg %}
                <div style="color: var(--danger); text-align: center; margin-top: 10px; font-size: 0.8rem;">{{ fail_msg }}</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# --- Routes ---

@app.route('/')
def home():
    return render_template_string(HTML, query_val="")

@app.route('/check', methods=['GET'])
def check_oracle():
    user_query = request.args.get('query', '')
    oracle_status = None
    
    if user_query:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # VULNERABLE BLIND QUERY
        # Vulnerability: f-string injection
        sql = f"SELECT * FROM users WHERE username = '{user_query}'"
        
        try:
            print(f"[DEBUG] Executing: {sql}")
            cursor.execute(sql)
            result = cursor.fetchone()
            
            # The "Oracle" Logic:
            # We return YES (True) or NO (False). We DO NOT return the data.
            if result:
                oracle_status = "YES"
            else:
                oracle_status = "NO"
                
        except sqlite3.Error:
            # SQL Errors are treated as "NO" (Common in blind scenarios)
            oracle_status = "NO"
        finally:
            conn.close()

    return render_template_string(HTML, oracle_response=oracle_status, query_val=user_query)

@app.route('/solve', methods=['POST'])
def solve_challenge():
    attempt = request.form.get('flag_attempt', '')
    
    # Check if the user submitted the correct flag
    if attempt.strip() == FLAG:
        return render_template_string(HTML, success=True, success_flag=FLAG)
    else:
        return render_template_string(HTML, fail_msg="ACCESS DENIED: Incorrect Flag")

if __name__ == '__main__':
    init_db()
    # Runs on localhost only
    app.run(host='0.0.0.0', port=8083, debug=True)
