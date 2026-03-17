# John the Ripper Password Cracking

---
name: John the Ripper Password Cracking
description: This skill should be used when the user asks to "crack password hashes," "extract and crack encrypted file passwords," "perform dictionary attacks on hashes," "crack SSH or ZIP file passwords," or "use John the Ripper for penetration testing." It provides comprehensive guidance for using John the Ripper across multiple cracking modes and file formats.
version: 1.0.0
tags: [password-cracking, john-the-ripper, hash-cracking, penetration-testing, credential-recovery]
---

## Purpose

Provide systematic methodologies for cracking password hashes and encrypted file passwords using John the Ripper. This skill covers the three primary cracking modes (single, wordlist, incremental), hash format identification, file format extraction utilities (*2john tools), and optimized cracking strategies for various encryption types encountered during penetration testing.

## Inputs / Prerequisites

- **Target Hash File**: Text file containing username:hash pairs or extracted hashes
- **Hash Type Identification**: Knowledge of or auto-detection of hash format (MD5, SHA1, SHA256, etc.)
- **Wordlist Access**: Dictionary files such as rockyou.txt, password.lst, or custom wordlists
- **John the Ripper Installation**: Pre-installed on Kali Linux or installed from Openwall
- **Source Files (Optional)**: Encrypted files requiring hash extraction (ZIP, RAR, PDF, SSH keys, etc.)
- **System Access (Optional)**: Read access to /etc/passwd and /etc/shadow for Linux credential cracking

## Outputs / Deliverables

- **Cracked Credentials**: Plaintext passwords recovered from hash files
- **Session Files**: Saved cracking progress for session restoration
- **Extracted Hashes**: Hash values extracted from encrypted files using *2john utilities
- **Crack Report**: Summary of cracked credentials with usernames and passwords
- **Format Identification**: Detected or verified hash format types

## Core Workflow

### 1. Hash Acquisition and Preparation

#### Extract Linux User Credentials
```bash
# Method 1: Single user extraction
cat /etc/shadow | grep username > crack.txt

# Method 2: All users with unshadow utility
unshadow /etc/passwd /etc/shadow > crack.txt
```

#### Extract Hashes from Encrypted Files
```bash
# Locate available extraction utilities
locate *2john

# SSH private key extraction
ssh2john /path/to/id_rsa > ssh_hash.txt

# ZIP file extraction
zip2john file.zip > zip_hash.txt

# RAR file extraction
rar2john file.rar > rar_hash.txt

# 7-Zip file extraction
python 7z2john.py file.7z > 7z_hash.txt

# PDF file extraction
python pdf2john.py file.pdf > pdf_hash.txt

# KeePass database extraction
keepass2john database.kdb > keepass_hash.txt

# PuTTY private key extraction
putty2john file.ppk > putty_hash.txt

# Password Safe extraction
pwsafe2john file.psafe3 > pwsafe_hash.txt
```

### 2. Identify Hash Format

#### Auto-Detection
```bash
# John attempts automatic format detection
john hash.txt
```

#### Manual Format Specification
```bash
# List all supported formats
john --list=formats

# Specify format explicitly
john --format=raw-sha1 hash.txt
john --format=raw-md5 hash.txt
john --format=raw-sha256 hash.txt
```

#### Common Hash Formats
| Hash Type | Format Flag | Example Pattern |
|-----------|-------------|-----------------|
| MD4 | `raw-md4` | 32 hex characters |
| MD5 | `raw-md5` | 32 hex characters |
| SHA1 | `raw-sha1` | 40 hex characters |
| SHA256 | `raw-sha256` | 64 hex characters |
| SHA512 | `raw-sha512` | 128 hex characters |
| RIPEMD-128 | `ripemd-128` | 32 hex characters |
| Whirlpool | `whirlpool` | 128 hex characters |
| bcrypt | `bcrypt` | $2a$, $2b$, $2y$ prefix |
| Linux SHA512crypt | `sha512crypt` | $6$ prefix |

### 3. Select Cracking Mode

#### Single Crack Mode (Fastest)
Uses username-based password mutations:
```bash
john --single --format=raw-sha1 crack.txt
# Abbreviated: john -si crack.txt -form=raw-sha1
```

#### Wordlist Crack Mode (Most Common)
```bash
# Using default wordlist
john --wordlist=/usr/share/john/password.lst --format=raw-sha1 crack.txt

# Using rockyou wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-md5 crack.txt

# Abbreviated syntax
john -w=/usr/share/wordlists/rockyou.txt crack.txt -form=raw-md5
```

#### Incremental Mode (Brute Force)
```bash
# Full brute force with character set
john --incremental crack.txt

# Specify incremental mode type
john --incremental=digits crack.txt
john --incremental=alpha crack.txt
```

### 4. Execute Cracking

#### Basic Cracking Session
```bash
# Start cracking with wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-sha256 crack.txt

# Crack multiple files simultaneously (same format)
john --format=raw-md5 crack.txt md5_hashes.txt
```

#### Session Management
```bash
# Interrupt session: Press 'q' or Ctrl+C

# Resume interrupted session
john --restore

# Show cracked passwords
john --show crack.txt

# Show cracked passwords for specific format
john --show --format=raw-sha256 crack.txt
```

### 5. Post-Cracking Analysis

#### View Results
```bash
# Display all cracked passwords
john --show crack.txt

# Count cracked vs remaining
john --show crack.txt | wc -l
```

## Quick Reference Commands

### Hash Format Cracking

| Hash Type | Command |
|-----------|---------|
| MD4 | `john -w=rockyou.txt --format=raw-md4 hash.txt` |
| MD5 | `john -w=rockyou.txt --format=raw-md5 hash.txt` |
| SHA1 | `john -w=rockyou.txt --format=raw-sha1 hash.txt` |
| SHA256 | `john -w=rockyou.txt --format=raw-sha256 hash.txt` |
| Whirlpool | `john -w=rockyou.txt --format=whirlpool hash.txt` |
| RIPEMD-128 | `john -w=rockyou.txt --format=ripemd-128 hash.txt` |

### File Format Cracking Workflow

| File Type | Extract Command | Crack Command |
|-----------|-----------------|---------------|
| SSH Key | `ssh2john id_rsa > hash.txt` | `john -w=rockyou.txt hash.txt` |
| ZIP | `zip2john file.zip > hash.txt` | `john -w=rockyou.txt hash.txt` |
| RAR | `rar2john file.rar > hash.txt` | `john -w=rockyou.txt hash.txt` |
| 7z | `7z2john.py file.7z > hash.txt` | `john -w=rockyou.txt hash.txt` |
| PDF | `pdf2john.py file.pdf > hash.txt` | `john -w=rockyou.txt hash.txt` |
| KeePass | `keepass2john db.kdb > hash.txt` | `john -w=rockyou.txt hash.txt` |
| PuTTY | `putty2john key.ppk > hash.txt` | `john -w=rockyou.txt hash.txt` |
| Password Safe | `pwsafe2john file.psafe3 > hash.txt` | `john -w=rockyou.txt hash.txt` |

### Option Abbreviations

| Full Option | Abbreviation |
|-------------|--------------|
| `--single` | `-si` |
| `--format` | `-form` |
| `--wordlist` | `-w` |

## Constraints and Limitations

### Operational Boundaries
- Requires extracted hash file in correct format (username:hash or hash-only)
- Wordlist attacks limited by dictionary completeness
- Incremental mode extremely time-consuming for complex passwords
- Some formats require additional Python utilities (7z2john, pdf2john)
- Hash extraction utilities may not be pre-installed

### Performance Considerations
- Cracking speed depends on hash type (MD5 faster than bcrypt)
- GPU acceleration available via John the Ripper Jumbo
- Large wordlists increase memory usage
- Multiple hash files can be processed simultaneously if same format

### Legal Requirements
- Only use on systems with explicit authorization
- Penetration testing requires written consent
- Credential recovery must be documented and approved

## Examples

### Example 1: Crack Linux Shadow Passwords
```bash
# Combine passwd and shadow files
unshadow /etc/passwd /etc/shadow > linux_hashes.txt

# Crack using wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt linux_hashes.txt

# View results
john --show linux_hashes.txt
```

### Example 2: Crack SSH Private Key Passphrase
```bash
# Extract hash from SSH key
ssh2john ~/.ssh/id_rsa > ssh_hash.txt

# Crack with dictionary attack
john --wordlist=/usr/share/wordlists/rockyou.txt ssh_hash.txt

# Expected output: password123 (id_rsa)
```

### Example 3: Crack Password-Protected ZIP File
```bash
# Extract hash from ZIP
zip2john protected.zip > zip_hash.txt

# Crack the hash
john --wordlist=/usr/share/wordlists/rockyou.txt zip_hash.txt

# View cracked password
john --show zip_hash.txt
```

### Example 4: Crack Multiple MD5 Hashes
```bash
# Create hash file with format: username:md5hash
echo "admin:5f4dcc3b5aa765d61d8327deb882cf99" > md5_hashes.txt
echo "user1:827ccb0eea8a706c4c34a16891f84e7b" >> md5_hashes.txt

# Crack with format specification
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt md5_hashes.txt

# Results: admin:password, user1:12345
```

### Example 5: Session Management During Long Crack
```bash
# Start long-running crack
john --wordlist=/usr/share/wordlists/rockyou.txt --format=bcrypt bcrypt_hashes.txt

# Press 'q' to interrupt and save session

# Resume later
john --restore

# Check progress
john --show bcrypt_hashes.txt
```

### Example 6: Single Crack Mode for Quick Wins
```bash
# Hash file format: username:hash
echo "administrator:0d107d09f5bbe40cade3de5c71e9e9b7" > quick.txt

# Single crack mode uses username variations
john --single --format=raw-md5 quick.txt
# Tries: administrator, ADMINISTRATOR, Administrator1, admin1strator, etc.
```

## Troubleshooting

### Issue: "No password hashes loaded"
**Cause**: Format mismatch or incorrect file structure
**Solution**:
```bash
# Verify hash format
cat hash.txt
# Specify format explicitly
john --format=raw-sha1 hash.txt
# Check supported formats
john --list=formats | grep -i sha
```

### Issue: Session Won't Restore
**Cause**: Corrupted session file or different working directory
**Solution**:
```bash
# Check for session files
ls ~/.john/
# Remove corrupted session
rm ~/.john/john.rec
# Start fresh
john --wordlist=rockyou.txt hash.txt
```

### Issue: *2john Utility Not Found
**Cause**: External utilities not installed or not in PATH
**Solution**:
```bash
# Locate utilities
locate *2john
find /usr -name "*2john*"
# For Python-based utilities, download from John repository
wget https://raw.githubusercontent.com/openwall/john/bleeding-jumbo/run/pdf2john.py
python pdf2john.py file.pdf > hash.txt
```

### Issue: Cracking Too Slow
**Cause**: Complex hash algorithm or weak hardware
**Solution**:
```bash
# Use smaller targeted wordlist
john --wordlist=targeted.txt hash.txt
# Try single mode first (fastest)
john --single hash.txt
# Check if hash is bcrypt/scrypt (slow by design)
john --list=formats | grep -i bcrypt
```

### Issue: Hash Not Cracking
**Cause**: Password not in wordlist or too complex
**Solution**:
```bash
# Try multiple wordlists
john -w=/usr/share/wordlists/rockyou.txt hash.txt
john -w=/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt hash.txt
# Enable rules for mutations
john -w=rockyou.txt --rules hash.txt
# Use incremental for short passwords
john --incremental=digits hash.txt
```

### Issue: ZIP/RAR Extraction Fails
**Cause**: Corrupted archive or unsupported encryption
**Solution**:
```bash
# Verify archive integrity
unzip -t file.zip
unrar t file.rar
# Try alternative extraction method
zip2john file.zip 2>&1 | head -20
# Check for AES encryption (may require different tool)
```
