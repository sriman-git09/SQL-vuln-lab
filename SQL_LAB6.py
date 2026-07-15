import sqlite3
import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
REAL_FLAG = "SQL{w0w_y0u_c4ack_1t_db}"
# Encoded Flag: U1FMe3cwM195MHVfYzRhY2tfMXRfZGJ9
ENCODED_FLAG = base64.b64encode(REAL_FLAG.encode()).decode()

DB_NAME = "bigbasket_replica.db"

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. PUBLIC TABLE: Products (The Shop)
    c.execute("DROP TABLE IF EXISTS products")
    c.execute("CREATE TABLE products (id INTEGER, name TEXT, price TEXT, image TEXT)")
    c.execute("INSERT INTO products VALUES (1, 'Fresh Onion (1kg)', '₹45', '🧅')")
    c.execute("INSERT INTO products VALUES (2, 'Organic Apple (6pcs)', '₹120', '🍎')")
    c.execute("INSERT INTO products VALUES (3, 'Farm Toned Milk', '₹32', '🥛')")
    c.execute("INSERT INTO products VALUES (4, 'Whole Wheat Bread', '₹40', '🍞')")
    c.execute("INSERT INTO products VALUES (5, 'Dozen Eggs', '₹80', '🥚')")

    # 2. THE TARGET TABLE: member_member (Based on the real breach)
    # This table is hidden. Normal users cannot see it.
    c.execute("DROP TABLE IF EXISTS member_member")
    c.execute("CREATE TABLE member_member (member_id INTEGER, full_name TEXT, email TEXT, password_hash TEXT, internal_notes TEXT)")
    
    # Dummy Data (The 20 million users simulation)
    c.execute("INSERT INTO member_member VALUES (101, 'Admin User', 'admin@bigbasket.com', '7c4a8d09ca3762af61e59520943dc26494f8941b', 'sys_admin_access')")
    c.execute("INSERT INTO member_member VALUES (102, 'Rahul Kumar', 'rahul.k@gmail.com', 'f7c3bc1d808e04732adf679965ccc34ca7ae3441', 'customer_standard')")
    
    # THE FLAG LOCATION
    # The user asked for "sriman.txt". We put it in the 'internal_notes' column.
    c.execute("INSERT INTO member_member VALUES (999, 'System Backup', 'backup@internal.local', 'auth_disabled', 'FILE: sriman.txt | CONTENT: " + ENCODED_FLAG + "')")
    
    conn.commit()
    conn.close()

# --- E-COMMERCE UI (No Comments/Hints) ---
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BigGrocery | Fresh Online Store</title>
    <style>
        :root { --primary: #84c225; --dark: #333; --light: #f4f4f4; --white: #fff; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #f9f9f9; color: var(--dark); }
        
        /* Navbar */
        .navbar { background: var(--white); padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-bottom: 3px solid var(--primary); }
        .logo { font-size: 24px; font-weight: bold; color: var(--dark); display: flex; align-items: center; gap: 5px; }
        .logo span { color: var(--primary); }
        
        /* Search Bar (The Vector) */
        .search-container { display: flex; width: 500px; }
        .search-input { width: 100%; padding: 10px; border: 1px solid #ccc; border-right: none; border-radius: 4px 0 0 4px; outline: none; }
        .search-btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 0 4px 4px 0; cursor: pointer; font-weight: bold; }
        .search-btn:hover { background: #6da51b; }

        /* Product Grid */
        .container { padding: 40px 50px; }
        .section-title { font-size: 22px; margin-bottom: 20px; border-left: 5px solid var(--primary); padding-left: 10px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
        .product-card { background: white; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center; transition: transform 0.2s; }
        .product-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .emoji { font-size: 50px; margin-bottom: 10px; display: block; }
        .price { color: var(--dark); font-weight: bold; display: block; margin: 5px 0; }
        .add-btn { background: #fff; border: 1px solid var(--primary); color: var(--primary); padding: 5px 15px; border-radius: 4px; cursor: pointer; margin-top: 5px; }
        .add-btn:hover { background: var(--primary); color: white; }

        /* Footer / Bounty Panel */
        .footer { background: #222; color: #aaa; padding: 40px 50px; margin-top: 50px; }
        .bounty-panel { background: #333; padding: 20px; border-radius: 8px; border: 1px solid #444; max-width: 600px; margin: 0 auto; }
        .bounty-title { color: #fff; border-bottom: 1px solid #555; padding-bottom: 10px; margin-bottom: 15px; }
        
        .verify-input { background: #000; border: 1px solid #555; color: #0f0; padding: 10px; width: 70%; font-family: monospace; }
        .verify-btn { background: #444; color: #fff; border: none; padding: 11px 20px; cursor: pointer; }
        
        /* Alerts */
        .alert { padding: 10px; margin-bottom: 20px; border-radius: 4px; }
        .error { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
        .success-modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: flex; justify-content: center; align-items: center; z-index: 1000; flex-direction: column; }
        .trophy { font-size: 80px; margin-bottom: 20px; }
    </style>
</head>
<body>

    <!-- Navbar -->
    <div class="navbar">
        <div class="logo"><span>Big</span>Grocery</div>
        <form method="GET" action="/" class="search-container">
            <input type="text" class="search-input" name="search" placeholder="Search for vegetables, fruits..." value="{{ query }}">
            <button type="submit" class="search-btn">SEARCH</button>
        </form>
        <div style="font-weight: bold;">Login / Sign Up</div>
    </div>

    <!-- Success Modal -->
    {% if win %}
    <div class="success-modal">
        <div class="trophy">🏆</div>
        <h1 style="color: #4caf50; font-size: 40px;">BOUNTY AWARDED</h1>
        <p style="color: white; font-size: 18px;">Breach Replicated. Flag Verified.</p>
        <a href="/" style="color: #aaa; margin-top: 20px;">Close</a>
    </div>
    {% endif %}

    <!-- Main Content -->
    <div class="container">
        
        {% if error_msg %}
        <div class="alert error">
            <strong>Database Error:</strong> An error occurred while processing your search query.
        </div>
        {% endif %}

        <div class="section-title">Best Sellers</div>
        
        <div class="grid">
            {% if products %}
                {% for p in products %}
                <div class="product-card">
                    <span class="emoji">{{ p[3] }}</span> <!-- Image Column -->
                    <strong>{{ p[1] }}</strong> <!-- Name Column -->
                    <span class="price">{{ p[2] }}</span> <!-- Price Column -->
                    <button class="add-btn">ADD</button>
                </div>
                {% endfor %}
            {% else %}
                <p>No products found.</p>
            {% endif %}
        </div>
    </div>

    <!-- Footer / Researcher Panel -->
    <div class="footer">
        <div class="bounty-panel">
            <div class="bounty-title">🛡️ Security Research / Bug Bounty Program</div>
            <p style="font-size: 0.9rem;">
                If you have identified a vulnerability (e.g., Database Leak), submit the verification token (flag) found in the internal files.
            </p>
            <form method="POST" action="/verify">
                <input type="text" name="flag" class="verify-input" placeholder="Enter Flag (SQL{...})">
                <button type="submit" class="verify-btn">SUBMIT REPORT</button>
            </form>
            {% if verify_fail %}
                <p style="color: #ff5252; margin-top: 10px;">[!] Invalid Flag. Submission Rejected.</p>
            {% endif %}
        </div>
        <br>
        <center>&copy; 2020-2026 BigGrocery Ltd. All rights reserved.</center>
    </div>

</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def home():
    query = request.args.get('search', '')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    products = []
    error_msg = None

    if query:
        # VULNERABLE SEARCH QUERY
        # The breach happened because of concatenation like this.
        # It allows UNION based injection.
        # The 'products' table has 4 columns. The UNION must match 4 columns.
        sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    else:
        sql = "SELECT * FROM products"

    try:
        # We catch errors but don't show specific SQL details to simulate a production site
        # However, the UNION results will render in the product cards.
        cursor.execute(sql)
        products = cursor.fetchall()
    except Exception as e:
        # In a real attack, seeing the error helps. We show a generic error but the existence of it proves injection.
        error_msg = True
        products = []
    
    conn.close()
    return render_template_string(HTML, products=products, query=query, error_msg=error_msg)

@app.route('/verify', methods=['POST'])
def verify():
    user_flag = request.form.get('flag', '').strip()
    if user_flag == REAL_FLAG:
        return render_template_string(HTML, win=True, products=[])
    else:
        return render_template_string(HTML, verify_fail=True, products=[])

if __name__ == '__main__':
    init_db()
    # Running on port 8090
    app.run(host='0.0.0.0', port=8090, debug=True)
