---
name: Static Vulnerability Analysis
description: Methodical approach to finding security vulnerabilities through source code review and static analysis
when_to_use: When source code is available, before dynamic testing, or when performing security code review of applications
version: 1.0.0
languages: c, c++, java, python, javascript, php
---

# Static Vulnerability Analysis

## Overview

Static analysis examines source code without executing it, identifying security vulnerabilities through pattern matching, data flow analysis, and manual code review. This technique is essential for finding logic flaws, authentication bypasses, and subtle vulnerabilities that automated tools might miss.

**Core principle:** Combine automated tools with manual review. Tools find patterns; humans find logic flaws.

## Common Vulnerability Patterns

### Memory Safety Issues (C/C++)

```c
// Buffer Overflow
char buffer[256];
strcpy(buffer, user_input);  // ❌ Unsafe
strncpy(buffer, user_input, sizeof(buffer)-1);  // ✓ Safer

// Integer Overflow
size_t alloc = user_count * item_size;  // ❌ Can overflow
void *ptr = malloc(alloc);

// Use After Free
free(ptr);
ptr->field = value;  // ❌ Use after free

// Double Free
free(ptr);
free(ptr);  // ❌ Double free
```

### Injection Vulnerabilities

```python
# SQL Injection
query = f"SELECT * FROM users WHERE name = '{user_input}'"  # ❌
cursor.execute(query)

# Safe: Parameterized queries
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))  # ✓

# Command Injection
os.system(f"ping {user_input}")  # ❌

# Safe: Use subprocess with list
subprocess.run(["ping", user_input])  # ✓

# Path Traversal
filepath = f"/data/{user_filename}"  # ❌ ../../../etc/passwd
open(filepath, 'r')

# Safe: Validate and use os.path.join with validation
```

### Authentication and Authorization

```python
# Broken Authentication
if username == "admin" and password == config.ADMIN_PASSWORD:  # ❌ Timing attack
    grant_access()

# Better: Use constant-time comparison
import hmac
if hmac.compare_digest(username, "admin") and \
   hmac.compare_digest(password, config.ADMIN_PASSWORD):
    grant_access()

# Authorization Bypass
def get_user_data(user_id):
    # ❌ No authorization check
    return database.get_user(user_id)

# Better: Check authorization
def get_user_data(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        raise UnauthorizedException()
    return database.get_user(user_id)
```

## Automated Tools

```bash
# Semgrep - Pattern-based analysis
semgrep --config=auto /path/to/source

# Bandit - Python security linter
bandit -r /path/to/python/code

# ESLint with security plugins - JavaScript
eslint --plugin security /path/to/js

# Brakeman - Ruby on Rails
brakeman /path/to/rails/app

# FindSecBugs - Java
# SpotBugs with FindSecBugs plugin

# SonarQube - Multi-language
sonar-scanner
```

## Manual Review Checklist

- [ ] Input validation on all user-controlled data
- [ ] Authentication mechanisms (session management, password storage)
- [ ] Authorization checks (IDOR, privilege escalation)
- [ ] Cryptographic implementations (weak algorithms, hardcoded keys)
- [ ] Error handling (information disclosure)
- [ ] Business logic flaws
- [ ] Race conditions and time-of-check-time-of-use
- [ ] Sensitive data exposure (logs, error messages)

## Data Flow Analysis

```python
# Trace tainted data from source to sink
# SOURCE: User input
# SINK: Dangerous operation

# Example:
user_input = request.GET['file']  # SOURCE
# ... no validation ...
content = open(user_input).read()  # SINK

# Finding: Path traversal vulnerability
# No validation between source and sink
```

## Integration with Other Skills

- skills/analysis/zero-day-hunting - Comprehensive vulnerability research
- skills/exploitation/exploit-dev-workflow - Exploitation of found vulnerabilities
- skills/documentation/* - Document findings
