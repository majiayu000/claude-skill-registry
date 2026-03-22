---
name: credential-cracking
description: >
  Offline credential and file cracking with hashcat and john. Use when any skill
  recovers hashes (NTLM, Kerberos TGS/AS-REP, shadow, MSCACHE2) or encrypted
  files (ZIP, Office, PDF, KeePass, SSH key, 7z, RAR). Trigger phrases: "crack
  this hash", "brute force the password", "offline crack", "john", "hashcat",
  "zip2john", "password-protected file". Do NOT use for online password attacks
  (spraying, brute force against services) — use password-spraying instead.
keywords:
  - crack
  - hash
  - hashcat
  - john
  - zip2john
  - office2john
  - keepass2john
  - ssh2john
  - ansible2john
  - ansible vault
  - rockyou
  - wordlist
  - offline
  - brute force
  - NTLM
  - Kerberos TGS
  - AS-REP
  - shadow
  - bcrypt
  - MSCACHE2
  - PKZIP
  - password-protected
tools:
  - hashcat
  - john
  - zip2john
  - office2john
  - pdf2john
  - keepass2john
  - ssh2john
  - 7z2john
  - rar2john
  - gpg2john
  - ansible2john
opsec: low
---

# Credential Cracking

You are helping a penetration tester with offline credential and file cracking.
This skill covers hash identification, extraction from encrypted files, and
cracking with hashcat or john. All operations are local — no target interaction.
All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[credential-cracking] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers offline hash cracking and encrypted file cracking only. It
does NOT cover:
- Online password attacks (spraying, brute force) -- use **password-spraying**
- Credential dumping from memory/registry -- use **credential-dumping**
- Password guessing against services -- use **password-spraying**

When cracking is complete, STOP and return to the orchestrator with cracked
credentials and recommendations for where to test them.

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Hashes or encrypted files from another skill or user-provided
- **hashcat** (preferred for GPU-accelerated cracking) or **john** (john-jumbo
  for `*2john` tools)
- Wordlists — check these locations in order:
  1. `/usr/share/wordlists/rockyou.txt` (Kali default — may be a symlink or compressed `.gz`)
  2. `/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt` (SecLists location)
  3. `/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz` (compressed — extract first: `tar xzf rockyou.txt.tar.gz`)
  4. `/opt/seclists/Passwords/` (legacy SecLists path)

  **Common issue**: `/usr/share/wordlists/rockyou.txt` is often a broken symlink
  pointing to `/opt/seclists/...` which doesn't exist. If the symlink is broken,
  check `/usr/share/seclists/` directly. If rockyou is only available as
  `.tar.gz`, extract to `$TMPDIR` before use.

  **If rockyou.txt is not found at ANY of the above locations** (including
  compressed variants), STOP immediately. Do not create custom wordlists or
  generate passwords. Report the failure:

  > [credential-cracking] STOPPED — no wordlist found. Checked:
  > /usr/share/wordlists/rockyou.txt, /usr/share/seclists/Passwords/,
  > /opt/seclists/Passwords/. Install SecLists or provide a wordlist path.

  Return to the orchestrator with this message. The operator must install a
  wordlist before cracking can proceed.

### Sandbox — Disable for All Cracking Commands

hashcat and john need write access to multiple locations: session files
(`~/.local/share/hashcat/sessions/`), potfile (`~/.local/share/hashcat/
hashcat.potfile`), restore files (CWD), and temp working files. Redirecting
each individually with `--session`, `--potfile-path`, `-o` flags is fragile
and often still fails.

**Always run hashcat and john with `dangerouslyDisableSandbox: true`.**
This is the only reliable approach in Claude Code's sandboxed environment.

```bash
# CORRECT — disable sandbox for all cracking commands
Bash(command="hashcat -m MODE hash.txt wordlist.txt --force",
     dangerouslyDisableSandbox=true)

Bash(command="john --wordlist=wordlist.txt hash.txt",
     dangerouslyDisableSandbox=true)

# Also for --show after cracking
Bash(command="hashcat -m MODE hash.txt --show",
     dangerouslyDisableSandbox=true)
```

**Do not** attempt `$TMPDIR` workarounds first — go straight to sandbox
disable. Cracking is a local-only operation with no security implications
from disabling the sandbox.

### john-jumbo Requirement

Most `*2john` extraction tools ship with **john-jumbo**, not basic john. Check:

```bash
john --version 2>&1 | head -1
# Should show "John the Ripper" with "jumbo" in the version string
```

If john-jumbo is not installed:
```bash
# Debian/Ubuntu
sudo apt install john

# Or build from source (last resort)
git clone https://github.com/openwall/john.git
cd john/src && ./configure && make -s clean && make -sj$(nproc)
# Binary at ../run/john
```

The `*2john` tools are typically in `/usr/share/john/` or alongside the john
binary (e.g., `/opt/john/run/zip2john`). Check with:
```bash
find /usr -name "zip2john" 2>/dev/null
find /opt -name "zip2john" 2>/dev/null
```

## Step 1: Identify Hash Type

Determine what needs cracking. This comes from one of two sources:

### Source A: Hash from Another Skill

Hashes recovered during the engagement (check `get_state_summary()` Credentials section):

| Hash Prefix / Pattern | Type | Hashcat Mode | Notes |
|------------------------|------|-------------|-------|
| No prefix, 32 hex chars | NTLM | 1000 | From SAM/secretsdump |
| `username::domain:...` | NTLMv2 | 5600 | From Responder/relay |
| `$krb5tgs$23$*...` | Kerberos TGS (RC4) | 13100 | From kerberoasting |
| `$krb5tgs$17$*...` | Kerberos TGS (AES128) | 19600 | From kerberoasting |
| `$krb5tgs$18$*...` | Kerberos TGS (AES256) | 19700 | From kerberoasting |
| `$krb5asrep$23$...` | AS-REP | 18200 | From AS-REP roasting |
| `$6$...` | SHA-512 crypt | 1800 | From /etc/shadow (Linux) |
| `$5$...` | SHA-256 crypt | 7400 | From /etc/shadow |
| `$1$...` | MD5 crypt | 500 | From /etc/shadow (legacy) |
| `$2b$...` or `$2a$...` | bcrypt | 3200 | Web apps, htpasswd |
| `DCC2$...` or `$DCC2$...` | MSCACHE2 | 2100 | From cached domain creds |
| 32 hex chars (with salt context) | MD5 / MySQL / etc. | varies | Check hashcat examples |

If the hash type is unclear, use hashcat's built-in identification:
```bash
hashcat --identify hash.txt
```

Or john:
```bash
john --list=formats | grep -i <keyword>
```

### Source B: Encrypted File

Password-protected files found during the engagement:

| Format | Extraction Tool | Notes |
|--------|----------------|-------|
| ZIP | `zip2john` | Handles both PKZIP and AES-256 |
| Office 2007+ (docx/xlsx/pptx) | `office2john` | OOXML format |
| Office 97-2003 (doc/xls) | `office2john` | Legacy OLE format (auto-detected) |
| PDF | `pdf2john` | Adobe encrypted PDF |
| KeePass (kdbx) | `keepass2john` | KeePass 2.x database |
| SSH private key | `ssh2john` | Encrypted id_rsa / id_ed25519 |
| 7z | `7z2john` | 7-Zip archive |
| RAR | `rar2john` | RAR 3/5 archive |
| GPG | `gpg2john` | GPG-encrypted file |
| Ansible Vault | `ansible2john` | Ansible encrypted vars/files (john-jumbo) |

## Step 2: Extract Hash (File-Based Formats)

For file-based formats, extract the hash using the appropriate `*2john` tool.

### Extraction Commands

```bash
# ZIP
zip2john protected.zip > hash.txt
# Remove the filename prefix if feeding to hashcat:
# zip2john output: archive.zip/file.txt:$pkzip$...
# hashcat needs: $pkzip$...

# Office (2007+ and 97-2003 auto-detected)
office2john protected.docx > hash.txt

# PDF
pdf2john protected.pdf > hash.txt

# KeePass
keepass2john database.kdbx > hash.txt

# SSH key
ssh2john id_rsa > hash.txt

# 7z
7z2john archive.7z > hash.txt

# RAR
rar2john archive.rar > hash.txt

# GPG
gpg2john encrypted.gpg > hash.txt

# Ansible Vault (tool name varies by installation)
ansible2john vault.yml > hash.txt
# Or: ansible2john.py, ansible-vault2john
# Common locations: /usr/share/john/, /opt/john/, alongside john binary
# If the tool is a Python script: python3 /path/to/ansible2john.py vault.yml > hash.txt
#
# For inline vault blocks (not standalone files), extract the block first:
# Copy the $ANSIBLE_VAULT;1.1;AES256 block (hex lines) to a file, then:
# ansible2john extracted_vault.yml > hash.txt
```

### Post-Extraction

1. Verify the hash was extracted successfully:
   ```bash
   cat hash.txt
   ```
2. For hashcat, strip the filename prefix (everything before the `$` or hash):
   ```bash
   # Example: strip "archive.zip/file.txt:" prefix
   sed 's/^[^:]*://' hash.txt > hash_clean.txt
   ```
3. Save to engagement evidence:
   ```bash
   cp hash.txt engagement/evidence/<format>-hash.txt
   ```

## Step 3: STOP -- Confirm Cracking Approach

**Hard stop — never auto-crack.** Do not skip this step.

Present the following to the user:

```
Hash type:     <identified type>
Hash count:    <number of hashes>
Source:        <file name or skill that produced it>

Recommended cracking approach:
  Tool:      <hashcat -m MODE | john --format=FORMAT>
  Wordlist:  <path to wordlist>
  Rules:     <if applicable>
  Command:   <exact command that will be run>

Options:
  a) Crack locally with the command above
  b) Export hash -- save to engagement/evidence/ for external cracking rig
```

Wait for the user to choose before proceeding. If the user chooses (b), save
the hash file, print its path, and return to the orchestrator.

## Step 4: Crack

Run the cracking tool chosen by the user.

**Sandbox reminder:** All hashcat and john commands MUST use
`dangerouslyDisableSandbox: true`. See Prerequisites for details.

**CPU-only systems:** If no GPU is available, hashcat requires `--force`
to run on CPU. Detect this upfront — don't wait for an OpenCL error:

```bash
# Check for GPU
hashcat -I 2>&1 | head -5
# If "No devices found" or only CPU listed, always add --force
```

### Hashcat (GPU-Preferred)

Hashcat is preferred for most hash types due to GPU acceleration.

**Common hash modes:**

| Hash Type | Mode | Command |
|-----------|------|---------|
| NTLM | 1000 | `hashcat -m 1000 hash.txt wordlist.txt` |
| NTLMv2 | 5600 | `hashcat -m 5600 hash.txt wordlist.txt` |
| Kerberos TGS (RC4) | 13100 | `hashcat -m 13100 hash.txt wordlist.txt` |
| Kerberos TGS (AES128) | 19600 | `hashcat -m 19600 hash.txt wordlist.txt` |
| Kerberos TGS (AES256) | 19700 | `hashcat -m 19700 hash.txt wordlist.txt` |
| AS-REP | 18200 | `hashcat -m 18200 hash.txt wordlist.txt` |
| SHA-512 crypt ($6$) | 1800 | `hashcat -m 1800 hash.txt wordlist.txt` |
| SHA-256 crypt ($5$) | 7400 | `hashcat -m 7400 hash.txt wordlist.txt` |
| MD5 crypt ($1$) | 500 | `hashcat -m 500 hash.txt wordlist.txt` |
| bcrypt | 3200 | `hashcat -m 3200 hash.txt wordlist.txt` |
| MSCACHE2 | 2100 | `hashcat -m 2100 hash.txt wordlist.txt` |
| PKZIP (compressed) | 17200 | `hashcat -m 17200 hash.txt wordlist.txt` |
| PKZIP (uncompressed) | 17210 | `hashcat -m 17210 hash.txt wordlist.txt` |
| PKZIP (mixed) | 17220 | `hashcat -m 17220 hash.txt wordlist.txt` |
| PKZIP (multi-file) | 17225 | `hashcat -m 17225 hash.txt wordlist.txt` |
| WinZip (AES) | 13600 | `hashcat -m 13600 hash.txt wordlist.txt` |
| Office 2013+ | 9600 | `hashcat -m 9600 hash.txt wordlist.txt` |
| Office 2010 | 9500 | `hashcat -m 9500 hash.txt wordlist.txt` |
| Office 2007 | 9400 | `hashcat -m 9400 hash.txt wordlist.txt` |
| PDF 1.7 (AES-256) | 10700 | `hashcat -m 10700 hash.txt wordlist.txt` |
| PDF 1.4-1.6 (AES/RC4) | 10500 | `hashcat -m 10500 hash.txt wordlist.txt` |
| KeePass | 13400 | `hashcat -m 13400 hash.txt wordlist.txt` |
| SSH key (RSA/DSA) | 22911 | `hashcat -m 22911 hash.txt wordlist.txt` |
| SSH key (EC) | 22921 | `hashcat -m 22921 hash.txt wordlist.txt` |

### John the Ripper

John is preferred when `*2john` extraction was used -- john reads the output
format directly without stripping prefixes.

```bash
# Basic wordlist attack
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# With format specification (if auto-detect fails)
john --format=<format> --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Show cracked passwords
john --show hash.txt
```

Common john formats: `NT`, `netntlmv2`, `krb5tgs`, `krb5asrep`, `sha512crypt`,
`bcrypt`, `PKZIP`, `Office`, `PDF`, `keepass`, `SSH`, `7z`, `RAR5`.

### Wordlists

Locate rockyou.txt (the most common general-purpose wordlist):

```bash
# Find rockyou — check all common locations
for f in /usr/share/wordlists/rockyou.txt \
         /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt \
         /opt/seclists/Passwords/Leaked-Databases/rockyou.txt; do
    [ -f "$f" ] && echo "[+] Found: $f" && break
done

# Check for compressed versions if not found
ls /usr/share/wordlists/rockyou.txt.gz \
   /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz \
   2>/dev/null

# Extract if compressed
# .gz:     gunzip /usr/share/wordlists/rockyou.txt.gz
# .tar.gz: tar xzf /usr/share/seclists/.../rockyou.txt.tar.gz -C $TMPDIR
```

SecLists passwords (for targeted cracking):

```bash
# Find seclists base directory
SECLISTS=$([ -d /usr/share/seclists ] && echo /usr/share/seclists || echo /opt/seclists)

# Useful wordlists:
# $SECLISTS/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
# $SECLISTS/Passwords/darkweb2017-top10000.txt
# $SECLISTS/Passwords/xato-net-10-million-passwords-1000000.txt
```

### Escalation Strategy

If a straight wordlist attack fails, escalate. All commands below require
`dangerouslyDisableSandbox: true` and `--force` on CPU-only systems.

1. **Wordlist only** (fastest):
   ```bash
   hashcat -m MODE hash.txt /usr/share/wordlists/rockyou.txt --force
   ```

2. **Wordlist + rules** (catches mutations like `Password1!`):
   ```bash
   # best64 — fast, covers common mutations
   hashcat -m MODE hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

   # dive.rule — comprehensive, slower
   hashcat -m MODE hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/dive.rule

   # OneRuleToRuleThemAll (download if not present)
   hashcat -m MODE hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/OneRuleToRuleThemAll.rule
   ```

   John equivalent:
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt --rules=best64 hash.txt
   ```

3. **Mask attack** (for known patterns):
   ```bash
   # 8-char lowercase + digit + special
   hashcat -m MODE hash.txt -a 3 '?l?l?l?l?l?l?d?s'

   # Company name + digits
   hashcat -m MODE hash.txt -a 3 'Company?d?d?d?d'

   # Capitalize first, lowercase, digits, special
   hashcat -m MODE hash.txt -a 3 '?u?l?l?l?l?l?d?d?s'
   ```

4. **Combination attack** (two wordlists combined):
   ```bash
   hashcat -m MODE hash.txt -a 1 wordlist1.txt wordlist2.txt
   ```

### Monitoring Progress

```bash
# Hashcat: press 's' for status during run, or:
hashcat -m MODE hash.txt wordlist.txt --status --status-timer=30

# John: press any key for status during run, or:
john --status
```

## Step 5: Post-Crack

### Record Results

1. Save cracked credentials to evidence:
   ```bash
   # Hashcat
   hashcat -m MODE hash.txt --show > engagement/evidence/cracked-passwords.txt

   # John
   john --show hash.txt > engagement/evidence/cracked-passwords.txt
   ```

2. Report cracked credentials in your return summary:
   ```markdown
   ## Credentials
   - admin:P@ssw0rd1 (cracked from NTLM, source: SAM dump on 10.10.10.5)
   - svc_sql:Summer2024! (cracked from kerberoasting TGS)
   ```

### Recommend Next Steps

Return to the orchestrator with:
- **Cracked credentials** and where they came from
- **Recommended testing**: which services/hosts to test them against (from the engagement state)
- **Suggested skills**:
  - Credentials work on SMB/WinRM/RDP -> **pass-the-hash** or **password-spraying**
  - Domain credentials recovered -> **ad-discovery** for further enumeration
  - SSH key decrypted -> direct SSH access, then **linux-discovery**
  - File decrypted (ZIP/Office/KeePass) -> examine contents for more credentials or sensitive data

## Troubleshooting

### hashcat: No devices found / OpenCL error
hashcat requires GPU drivers. If no GPU is available:
- Use `--force` to run on CPU (slow but works): `hashcat -m MODE hash.txt wordlist.txt --force`
- **Better:** detect this upfront in Step 4 with `hashcat -I` and always
  include `--force` on CPU-only systems. Don't wait for the error.
- Or switch to john (CPU-native): `john --wordlist=wordlist.txt hash.txt`

### hashcat: Permission denied / session file errors in sandbox
Do NOT try to work around with `--session $TMPDIR` or `--potfile-path`.
Use `dangerouslyDisableSandbox: true` on ALL hashcat/john commands. See
Prerequisites → "Sandbox" section.

### john: Unknown ciphertext format
- Specify format explicitly: `john --format=<format> hash.txt`
- List available formats: `john --list=formats`
- Ensure john-jumbo is installed (basic john has limited format support)

### rockyou.txt not found
```bash
# Check all common locations (including broken symlinks)
find /usr/share /opt -name "rockyou*" 2>/dev/null
ls -la /usr/share/wordlists/rockyou.txt  # Check if it's a broken symlink

# SecLists location (most reliable on non-Kali systems)
ls /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt*

# If only .tar.gz exists
tar xzf /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz -C $TMPDIR
# Then use: $TMPDIR/rockyou.txt

# If only .gz exists
gunzip /usr/share/wordlists/rockyou.txt.gz

# If missing entirely (Debian/Ubuntu)
sudo apt install wordlists seclists
```

### zip2john / office2john not found
These tools ship with john-jumbo. Check:
```bash
# Debian/Ubuntu package location
ls /usr/share/john/zip2john
ls /usr/share/john/office2john.py

# Custom john build
ls /opt/john/run/zip2john

# Or find them
find / -name "zip2john" 2>/dev/null
```

If the `*2john` tools are Python scripts, run them with python3:
```bash
python3 /usr/share/john/office2john.py protected.docx > hash.txt
```

### Hash format mismatch (hashcat)
```
Line-length exception / Token length exception / Separator unmatched
```
- The hash may have a filename prefix from `*2john` -- strip it
- Wrong hashcat mode -- verify with `hashcat --identify hash.txt`
- Hash may be truncated -- re-extract from source

### Cracking is too slow
- `$6$` (SHA-512 crypt), bcrypt, Office 2013+, and KeePass are intentionally
  slow hashes. Even with GPU, expect low speeds.
- Try a smaller, targeted wordlist first (top 10k passwords)
- Use mask attack if you know the password policy
- Consider exporting to a dedicated cracking rig
