import sqlite3
import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
# The Final Flag (Decoded version of the Base64 string you gave)
REAL_FLAG = "SQL{WAF_BYP4SS_M4ST3R}" 
# The Base64 string stored in the DB (U1FMe1dBRl9CWVA0U1NfTTRTVDNSfQo=)
ENCODED_FLAG = base64.b64encode(REAL_FLAG.encode()).decode()

DB_NAME = "aegis_secure.db"

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # TABLE 1: STAFF (The Decoy)
    # Contains the SHA1 hash you requested.
    c.execute("DROP TABLE IF EXISTS staff")
    c.execute("CREATE TABLE staff (id INTEGER, name TEXT, password_hash TEXT)")
    c.execute("INSERT INTO staff VALUES (1, 'Admin', '23d42f5f3f66498b2c8ff4c20b8c5ac826e47146')")
    c.execute("INSERT INTO staff VALUES (2, 'Guest', '356a192b7913b04c54574d18c28d46e6395428ab')")

    # TABLE 2: VAULT (The Target)
    # Contains the Base64 string.
    c.execute("DROP TABLE IF EXISTS vault")
    c.execute("CREATE TABLE vault (id INTEGER, artifact TEXT, data TEXT)")
    c.execute("INSERT INTO vault VALUES (1, 'CRITICAL_ASSET', ?)", (ENCODED_FLAG,))
    
    conn.commit()
    conn.close()

# --- WAF LOGIC (Firewall) ---
def firewall(payload):
    if not payload:
        return False, "OK"

    p = payload.upper()

    blocked = [
        "--",
        "/*",
        "*/"
    ]

    for b in blocked:
        if b in p:
            return True, f"BLOCKED: {b}"

    return False, "CLEAN"

# --- MODERN UI ---
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AEGIS // SECURITY OPERATIONS</title>
    <style>
        :root {
            --bg: #050505;
            --panel: #111;
            --border: #333;
            --accent: #00bcd4; /* Cyan */
            --danger: #ff3d00;
            --success: #00e676;
            --text: #e0e0e0;
        }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            display: grid;
            grid-template-rows: auto 1fr auto;
            width: 800px;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            box-shadow: 0 0 40px rgba(0,0,0,0.8);
            overflow: hidden;
        }
        
        /* HEADER */
        .header {
            background: #0a0a0a;
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .brand { font-size: 1.2rem; font-weight: bold; letter-spacing: 2px; color: var(--accent); }
        .badge { font-size: 0.7rem; padding: 4px 8px; border-radius: 4px; background: #222; border: 1px solid #444; }
        
        /* CONTENT */
        .content { padding: 30px; display: grid; gap: 30px; }
        
        /* QUERY PANEL */
        .panel { background: #0a0a0a; border: 1px solid var(--border); padding: 20px; border-radius: 6px; }
        .panel h3 { margin-top: 0; font-size: 0.9rem; color: #888; text-transform: uppercase; }
        
        input[type="text"] {
            width: 100%;
            background: #111;
            border: 1px solid #444;
            color: var(--accent);
            padding: 10px;
            font-family: monospace;
            box-sizing: border-box;
            margin-bottom: 10px;
        }
        input:focus { outline: none; border-color: var(--accent); }
        
        button {
            width: 100%;
            padding: 10px;
            background: var(--accent);
            color: #000;
            border: none;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover { opacity: 0.9; }

        /* LOG WINDOW */
        .log-window {
            height: 150px;
            background: #000;
            border: 1px solid #333;
            padding: 10px;
            font-family: monospace;
            font-size: 0.85rem;
            overflow-y: auto;
            color: #bbb;
        }
        .row { border-bottom: 1px solid #222; padding: 4px 0; display: flex; justify-content: space-between; }
        .val { color: var(--accent); }
        .alert { color: var(--danger); font-weight: bold; }

        /* DECODER / VERIFY SECTION */
        .verify-section {
            border-top: 1px solid var(--border);
            padding: 20px;
            background: #080808;
        }
        
        .success-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 100;
            animation: fadeIn 0.5s;
        }
        .win-msg { font-size: 3rem; color: var(--success); text-shadow: 0 0 20px var(--success); }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    </style>
</head>
<body>

    <!-- SUCCESS SCREEN -->
    {% if win %}
    <div class="success-overlay">
        <div class="win-msg">ACCESS GRANTED</div>
        <p style="color: #fff; font-size: 1.2rem;">Flag Verified: {{ win_flag }}</p>
        <a href="/" style="color: #888; margin-top: 20px;">Return</a>
    </div>
    {% endif %}

    <div class="container">
        <div class="header">
            <div class="brand">AEGIS // WAF</div>
            <div class="badge">SECURE MODE: ACTIVE</div>
        </div>

        <div class="content">
<!-- INJECTION VECTOR -->
<div class="panel">
    <h3>Staff Directory Search</h3>

    <form method="GET" action="/search">
        <input type="text"
               name="id"
               placeholder="Enter Staff ID"
               value="{{ q_val }}"
               autocomplete="off">

        <button type="submit">QUERY DATABASE</button>
    </form>

    <br>

    <a href="/hints" style="text-decoration:none;">
        <button type="button"
                style="background:#222;color:#fff;border:1px solid #444;">
            💡 View Hints
        </button>
    </a>

    <br><br>

    <div class="log-window">
        {% if waf_error %}
            <div class="alert">[!] FIREWALL BLOCKED REQUEST</div>
            <div class="alert">Reason: {{ waf_error }}</div>

        {% elif rows %}
            <div style="color: #666; margin-bottom: 5px;">
                Results Found:
            </div>

            {% for r in rows %}
            <div class="row">
                <span>ID: {{ r[0] }}</span>
                <span>{{ r[1] }}</span>
                <span class="val">{{ r[2] }}</span>
            </div>
            {% endfor %}

        {% else %}
            <div style="color: #444;">
                System Ready... Waiting for input.
            </div>
        {% endif %}
    </div>
</div>
            
            <!-- VERIFICATION MODULE -->
            <div class="panel" style="border-color: #444;">
                <h3>Decryption Verification</h3>
                <p style="font-size: 0.8rem; color: #666;">
                    If you recovered an encoded asset, decode it and paste the plaintext flag below.
                </p>
                <form method="POST" action="/verify">
                    <input type="text" name="flag_attempt" placeholder="SQL{...}" style="color: var(--success); border-color: #333;">
                    <button type="submit" style="background: #222; color: #fff; border: 1px solid #444;">VERIFY FLAG</button>
                </form>
                {% if verify_fail %}
                    <div style="color: var(--danger); font-size: 0.8rem; margin-top: 10px; text-align: center;">INVALID FLAG</div>
                {% endif %}
            </div>
        </div>
    </div>

</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(HTML, q_val="")

@app.route('/search', methods=['GET'])
def search():
    user_input = request.args.get('id', '')
    
    # 1. FIREWALL CHECK
    is_blocked, reason = firewall(user_input)
    if is_blocked:
        return render_template_string(HTML, waf_error=reason, q_val=user_input)

    # 2. VULNERABLE QUERY
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # VULNERABLE LINE
        # Selects ID, Name, Password_Hash from Staff
        # To get the flag, user must UNION SELECT id, artifact, data FROM vault
        sql = f"SELECT id, name, password_hash FROM staff WHERE id = {user_input}"
        
        c.execute(sql)
        results = c.fetchall()
        conn.close()
        
        return render_template_string(HTML, rows=results, q_val=user_input)
        
    except Exception as e:
        return render_template_string(HTML, waf_error=f"DB Error: {e}", q_val=user_input)

@app.route('/verify', methods=['POST'])
def verify():
    attempt = request.form.get('flag_attempt', '')
    if attempt.strip() == REAL_FLAG:
        return render_template_string(HTML, win=True, win_flag=REAL_FLAG)
    else:
        return render_template_string(HTML, verify_fail=True)
# ---------------------------
# HINT SYSTEM
# ---------------------------
HINTS = [
    "Hint 1: The Staff ID field is vulnerable to SQL Injection.",
    "Hint 2: More than one table exists in the database.",
    "Hint 3: The table containing the flag is named 'vault'.",
    "Hint 4: The encoded asset is stored in the 'data' column.",
    "Hint 5: The original query returns three columns.",
    "Hint 6: The recovered value is Base64 encoded.",
    "Hint 7: Decode the Base64 string and submit the plaintext flag."
]

@app.route("/hints")
def hints():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AEGIS Challenge Hints</title>
        <style>
            body{
                background:#050505;
                color:#e0e0e0;
                font-family:'Segoe UI',sans-serif;
                margin:0;
                display:flex;
                justify-content:center;
                align-items:center;
                min-height:100vh;
            }

            .container{
                width:800px;
                background:#111;
                border:1px solid #333;
                border-radius:8px;
                padding:30px;
                box-shadow:0 0 30px rgba(0,0,0,.8);
            }

            h1{
                color:#00bcd4;
                text-align:center;
                margin-bottom:25px;
            }

            .hint{
                background:#0b0b0b;
                border-left:4px solid #00bcd4;
                padding:15px;
                margin:12px 0;
                border-radius:4px;
            }

            a{
                color:#00bcd4;
                text-decoration:none;
            }

            .back{
                text-align:center;
                margin-top:25px;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>Challenge Hints</h1>

    """

    for hint in HINTS:
        html += f'<div class="hint">{hint}</div>'

    html += """

            <div class="back">
                <a href="/">⬅ Return to Challenge</a>
            </div>

        </div>

    </body>
    </html>
    """

    return html
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8087, debug=True)
