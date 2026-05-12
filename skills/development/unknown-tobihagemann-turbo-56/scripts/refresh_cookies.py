#!/usr/bin/env python3
"""Extract ChatGPT cookies from Chrome and write to ~/.oracle/cookies.json.

Reads encrypted cookies from Chrome's SQLite DB, decrypts them using the
Chrome Safe Storage key from macOS Keychain, validates the session against
ChatGPT's API, and writes the result.

Configuration (via ~/.turbo/config.json):
  oracle.chromeProfile  Chrome profile directory name (default: "Default")

Requirements: cryptography (pip3 install cryptography)
Note: macOS Keychain will prompt for password to access Chrome Safe Storage.
"""

import sqlite3, subprocess, json, os, sys, urllib.request


def load_config():
    """Load ~/.turbo/config.json and return the oracle section."""
    config_path = os.path.expanduser('~/.turbo/config.json')
    if not os.path.isfile(config_path):
        return {}
    with open(config_path) as f:
        return json.load(f).get('oracle', {})


config = load_config()

chrome_profile = config.get('chromeProfile', 'Default')

# Derive AES-128-CBC key from Chrome Safe Storage password
safe_storage_key = subprocess.check_output(
    ['security', 'find-generic-password', '-s', 'Chrome Safe Storage', '-w']
).strip()

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

kdf = PBKDF2HMAC(algorithm=hashes.SHA1(), length=16, salt=b'saltysalt', iterations=1003)
key = kdf.derive(safe_storage_key)


def decrypt_cookie(encrypted_value):
    if encrypted_value[:3] != b'v10':
        return encrypted_value.decode('utf-8', errors='ignore')
    data = encrypted_value[3:]
    iv = b' ' * 16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()
    # Remove PKCS7 padding
    pad_len = decrypted[-1]
    if 0 < pad_len <= 16:
        decrypted = decrypted[:-pad_len]
    # Strip 32-byte hash prefix (Chromium >= 124)
    if len(decrypted) >= 32:
        decrypted = decrypted[32:]
    return decrypted.decode('utf-8')


# Read cookies from Chrome profile
db_path = os.path.expanduser(
    f'~/Library/Application Support/Google/Chrome/{chrome_profile}/Cookies'
)
if not os.path.exists(db_path):
    print(f'ERROR: Cookie DB not found at {db_path}')
    print(f'Check ORACLE_CHROME_PROFILE (current: "{chrome_profile}").')
    print('Available profiles:')
    chrome_dir = os.path.expanduser('~/Library/Application Support/Google/Chrome')
    for entry in sorted(os.listdir(chrome_dir)):
        if entry.startswith(('Default', 'Profile')):
            print(f'  {entry}')
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.execute(
    "SELECT name, encrypted_value, host_key, path, is_httponly, is_secure "
    "FROM cookies WHERE host_key LIKE '%chatgpt%'"
)

cookies = []
failures = 0
for name, ev, domain, path, httponly, secure in cursor:
    try:
        value = decrypt_cookie(ev)
        cookies.append({
            'name': name, 'value': value,
            'domain': domain, 'path': path,
            'httpOnly': bool(httponly), 'secure': bool(secure)
        })
    except Exception as e:
        failures += 1
        if failures == 1:
            print(f'WARNING: Cookie decryption failed for {name}: {e}', file=sys.stderr)
conn.close()
if failures:
    print(f'WARNING: {failures} cookie(s) failed to decrypt.', file=sys.stderr)

if not cookies:
    print('ERROR: No cookies decrypted. Check Keychain access.')
    sys.exit(1)

# Validate session
cookie_str = '; '.join(f'{c["name"]}={c["value"]}' for c in cookies)
req = urllib.request.Request('https://chatgpt.com/api/auth/session')
req.add_header('Cookie', cookie_str)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
req.add_header('Referer', 'https://chatgpt.com/')

try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    expires = data.get('expires', 'unknown')
    print(f'Session valid. Expires: {expires}')
except Exception:
    print('WARNING: Cookies extracted but session validation failed. '
          'They may be expired - log into ChatGPT in Chrome first.')
    sys.exit(2)

# Write cookies
out_path = os.path.expanduser('~/.oracle/cookies.json')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(cookies, f, indent=2)
print(f'Wrote {len(cookies)} cookies to {out_path}')
