---
name: crypto-analysis
description: Cryptographic assessment — cipher identification, TLS auditing, hash analysis, key strength evaluation, side-channel detection, crypto implementation review
metadata:
  type: offensive
  phase: analysis
  tools: openssl, testssl, hashcat, john, hashid, rsactftool
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
