---
name: fix-security
description: Apply security fixes based on scan findings
allowed-tools: Read, Edit, Write, Grep, Glob, Bash(git:*)
---

# Fix Security Issues

Apply fixes for security vulnerabilities identified by external scanners.

## Purpose

This skill is invoked during the remediation loop when external security scanners (Semgrep, ASH) have identified vulnerabilities. It reads the security context and applies targeted fixes.

## When This Skill Is Used

1. External Semgrep scan detected SAST issues
2. External Grype scan (via ASH) detected vulnerable dependencies
3. The orchestrator has injected security context into `state/security-context.md`

## Process

### Step 1: Read Security Context

Check `state/security-context.md` for the specific findings that need to be addressed.

### Step 2: Understand Each Finding

For each finding, identify:
- The file and line number
- The type of vulnerability
- The severity level
- The recommended fix

### Step 3: Apply Fixes

Use the appropriate fix pattern for each vulnerability type:

#### Hardcoded Secrets
```python
# Before (VULNERABLE)
API_KEY = "sk-abc123..."

# After (SECURE)
import os
API_KEY = os.getenv('API_KEY')
```

#### SQL Injection
```python
# Before (VULNERABLE)
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# After (SECURE)
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

#### Command Injection
```python
# Before (VULNERABLE)
os.system(f"ls {user_input}")

# After (SECURE)
import subprocess
import shlex
subprocess.run(['ls', shlex.quote(user_input)], check=True)
```

#### Path Traversal
```python
# Before (VULNERABLE)
with open(f"data/{filename}") as f:
    content = f.read()

# After (SECURE)
import os
safe_path = os.path.join("data", os.path.basename(filename))
if not os.path.abspath(safe_path).startswith(os.path.abspath("data")):
    raise ValueError("Invalid path")
with open(safe_path) as f:
    content = f.read()
```

#### Vulnerable Dependencies
```json
// Before (package.json)
{
  "dependencies": {
    "lodash": "4.17.15"  // Vulnerable version
  }
}

// After
{
  "dependencies": {
    "lodash": "^4.17.21"  // Patched version
  }
}
```

### Step 4: Verify Fixes

After applying fixes:
1. Run `/self-check` to validate
2. Ensure the fix doesn't break functionality
3. Add or update tests if needed

## Usage

```
/fix-security
```

This skill reads from `state/security-context.md` and applies fixes to the identified issues.

## Important Notes

- **Do NOT proceed with new features** until all security issues are resolved
- **Test your fixes** - security fixes can break functionality
- **Document the fix** - add comments explaining why the change was made
- **Update tests** - add test cases for the security scenarios
