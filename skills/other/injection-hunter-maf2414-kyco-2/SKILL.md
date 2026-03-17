---
name: injection-hunter
description: Hunt for injection vulnerabilities including SQL injection, command injection, XSS, SSTI, path traversal, LDAP injection, and other input validation flaws. Use when auditing code that processes user input.
---

# Injection Vulnerability Hunter

## Purpose

Identify injection vulnerabilities by tracing user input from sources to dangerous sinks. Covers SQL injection, OS command injection, XSS, SSTI, path traversal, LDAP injection, and XML injection.

## Focus Areas

- **SQL Injection**: String concatenation in queries, ORM bypass
- **Command Injection**: Unsanitized input in system(), exec(), shell commands
- **XSS (Cross-Site Scripting)**: Reflected, stored, DOM-based
- **SSTI (Server-Side Template Injection)**: User input in templates
- **Path Traversal**: User input in file paths without sanitization
- **LDAP/XML/Header Injection**: Protocol-specific injection attacks

## Taint Analysis Approach

### 1. Identify Sources (User Input)
```
- request.params, request.body, request.query
- HTTP headers (Host, User-Agent, Referer, X-Forwarded-For)
- File uploads (filename, content)
- Database values (stored attacks)
- Environment variables (in some contexts)
- WebSocket messages
```

### 2. Track Flow Through Code
```
Follow data transformations:
- Variable assignments
- Function parameters
- Return values
- Object properties
```

### 3. Identify Dangerous Sinks
```
SQL:      db.query(), db.execute(), raw SQL strings
Command:  system(), exec(), popen(), spawn(), backticks
XSS:      innerHTML, document.write(), dangerouslySetInnerHTML
SSTI:     render(), template(), eval() with user data
Path:     open(), readFile(), fs.*, path.join() with user input
LDAP:     ldap.search() with user-controlled filter
```

## Output Format

```yaml
findings:
  - title: "SQL Injection in search endpoint"
    severity: critical
    attack_scenario: "Attacker injects SQL via 'query' parameter to extract database"
    preconditions: "None - public endpoint"
    reachability: public
    impact: "Full database compromise, data exfiltration"
    confidence: high
    cwe_id: "CWE-89"
    affected_assets:
      - "/api/search?query="
      - "src/handlers/search.rs:45"
    taint_path: "request.query['query'] -> format!() -> db.execute()"
```

## Key Patterns by Injection Type

### SQL Injection
```rust
// VULNERABLE - string concatenation
let query = format!("SELECT * FROM users WHERE name = '{}'", user_input);
db.execute(&query)?;

// SECURE - parameterized query
db.execute("SELECT * FROM users WHERE name = ?", &[user_input])?;
```

### Command Injection
```python
# VULNERABLE
os.system(f"convert {filename} output.png")  # filename = "; rm -rf /"

# SECURE
subprocess.run(["convert", filename, "output.png"])  # Array form
```

### XSS (Cross-Site Scripting)
```javascript
// VULNERABLE - direct HTML insertion
element.innerHTML = userInput;

// SECURE - text content only
element.textContent = userInput;
```

### Path Traversal
```go
// VULNERABLE
path := filepath.Join("/uploads", userInput)  // userInput = "../../../etc/passwd"

// SECURE
path := filepath.Join("/uploads", filepath.Base(userInput))  // Strip directory components
```

### SSTI (Server-Side Template Injection)
```python
# VULNERABLE
template = f"Hello {user_input}"  # user_input = "{{7*7}}" or worse
render_template_string(template)

# SECURE
render_template("hello.html", name=user_input)  # Template is static
```

## Severity Guidelines

| Type | Impact | Severity |
|------|--------|----------|
| SQL Injection | DB access | Critical |
| Command Injection | RCE | Critical |
| Stored XSS | Session hijack | High |
| Reflected XSS | Phishing | Medium |
| SSTI with RCE | RCE | Critical |
| Path Traversal (read) | Info disclosure | High |
| Path Traversal (write) | Code execution | Critical |

## Common Bypass Techniques to Consider

```
SQL: UNION, nested queries, time-based blind, error-based
CMD: &&, ||, ;, |, $(), backticks, newlines
XSS: Event handlers, data: URLs, SVG, encoding bypass
Path: ../, ..\\, URL encoding, double encoding, null bytes
```

## KYCo Integration

Register injection findings and import scanner results:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Register Finding
```bash
kyco finding create \
  --title "SQL Injection in search endpoint" \
  --project PROJECT_ID \
  --severity critical \
  --cwe CWE-89 \
  --attack-scenario "Attacker injects SQL via 'query' parameter to extract database" \
  --impact "Full database compromise, data exfiltration" \
  --assets "/api/search,src/handlers/search.rs:45"
```

### 3. Import Scanner Results
```bash
# Import SARIF output
kyco finding import scanner-results.sarif --project PROJECT_ID

# Import Semgrep JSON
kyco finding import semgrep-results.json --project PROJECT_ID -f semgrep
```

### Common CWE IDs for Injection
- CWE-89: SQL Injection
- CWE-78: OS Command Injection
- CWE-79: Cross-site Scripting (XSS)
- CWE-22: Path Traversal
- CWE-94: Code Injection
- CWE-1336: SSTI
