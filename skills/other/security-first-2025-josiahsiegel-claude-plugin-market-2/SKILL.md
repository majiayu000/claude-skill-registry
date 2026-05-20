---
name: security-first-2025
description: Security-first bash scripting patterns for 2025 (mandatory validation, zero-trust)
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Security-First Bash Scripting (2025)

## Overview

2025 security assessments reveal **60%+ of exploited automation tools lacked adequate input sanitization**. This skill provides mandatory security patterns.

## Critical Security Patterns

### 1. Input Validation (Non-Negotiable)

**Every input MUST be validated before use:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# ✅ REQUIRED: Validate all inputs
validate_input() {
    local input="$1"
    local pattern="$2"
    local max_length="${3:-255}"

    # Check empty
    if [[ -z "$input" ]]; then
        echo "Error: Input required" >&2
        return 1
    fi

    # Check pattern
    if [[ ! "$input" =~ $pattern ]]; then
        echo "Error: Invalid format" >&2
        return 1
    fi

    # Check length
    if [[ ${#input} -gt $max_length ]]; then
        echo "Error: Input too long (max $max_length)" >&2
        return 1
    fi

    return 0
}

# Usage
read -r user_input
if validate_input "$user_input" '^[a-zA-Z0-9_-]+$' 50; then
    process "$user_input"
else
    exit 1
fi
```

### 2. Command Injection Prevention

**NEVER use eval or dynamic execution with user input:**

```bash
# ❌ DANGEROUS - Command injection vulnerability
user_input="$(cat user_file.txt)"
eval "$user_input"  # NEVER DO THIS

# ❌ DANGEROUS - Indirect command injection
grep "$user_pattern" file.txt  # If pattern is "-e /etc/passwd"

# ✅ SAFE - Use -- separator
grep -- "$user_pattern" file.txt

# ✅ SAFE - Use arrays
grep_args=("$user_pattern" "file.txt")
grep "${grep_args[@]}"

# ✅ SAFE - Validate before use
if [[ "$user_pattern" =~ ^[a-zA-Z0-9]+$ ]]; then
    grep "$user_pattern" file.txt
fi
```

### 3. Path Traversal Prevention

**Sanitize and validate ALL file paths:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Sanitize path components
sanitize_path() {
    local path="$1"

    # Remove dangerous patterns
    path="${path//..\/}"     # Remove ../
    path="${path//\/..\//}"  # Remove /../
    path="${path#/}"         # Remove leading /

    echo "$path"
}

# Validate path is within allowed directory
is_safe_path() {
    local file_path="$1"
    local base_dir="$2"

    # Resolve to absolute paths
    local real_path real_base
    real_path=$(readlink -f "$file_path" 2>/dev/null) || return 1
    real_base=$(readlink -f "$base_dir" 2>/dev/null) || return 1

    # Check path starts with base
    [[ "$real_path" == "$real_base"/* ]]
}

# Usage
user_file=$(sanitize_path "$user_input")
if is_safe_path "/var/app/uploads/$user_file" "/var/app/uploads"; then
    cat "/var/app/uploads/$user_file"
else
    echo "Error: Access denied" >&2
    exit 1
fi
```

### 4. Secure Temporary Files

**Never use predictable temp file names:**

```bash
# ❌ DANGEROUS - Race condition vulnerability
temp_file="/tmp/myapp.tmp"
echo "data" > "$temp_file"  # Can be symlinked by attacker

# ❌ DANGEROUS - Predictable name
temp_file="/tmp/myapp-$$.tmp"  # PID can be guessed

# ✅ SAFE - Use mktemp
temp_file=$(mktemp)
chmod 600 "$temp_file"  # Owner-only permissions
echo "data" > "$temp_file"

# ✅ SAFE - Automatic cleanup
readonly TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT INT TERM

# ✅ SAFE - Temp directory
readonly TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT INT TERM
chmod 700 "$TEMP_DIR"
```

### 5. Secrets Management

**NEVER hardcode secrets or expose them:**

```bash
# ❌ DANGEROUS - Hardcoded secrets
DB_PASSWORD="supersecret123"

# ❌ DANGEROUS - Secrets in environment (visible in ps)
export DB_PASSWORD="supersecret123"

# ✅ SAFE - Read from secure file
if [[ -f /run/secrets/db_password ]]; then
    DB_PASSWORD=$(< /run/secrets/db_password)
    chmod 600 /run/secrets/db_password
else
    echo "Error: Secret not found" >&2
    exit 1
fi

# ✅ SAFE - Use cloud secret managers
get_secret() {
    local secret_name="$1"

    # AWS Secrets Manager
    aws secretsmanager get-secret-value \
        --secret-id "$secret_name" \
        --query SecretString \
        --output text
}

DB_PASSWORD=$(get_secret "production/database/password")

# ✅ SAFE - Prompt for sensitive data (no echo)
read -rsp "Enter password: " password
echo  # Newline after password
```

### 6. Privilege Management

**Follow least privilege principle:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Check not running as root
if [[ $EUID -eq 0 ]]; then
    echo "Error: Do not run as root" >&2
    exit 1
fi

# Drop privileges if started as root
drop_privileges() {
    local target_user="$1"

    if [[ $EUID -eq 0 ]]; then
        echo "Dropping privileges to $target_user" >&2
        exec sudo -u "$target_user" "$0" "$@"
    fi
}

# Run specific command with minimal privileges
run_privileged() {
    local command="$1"
    shift

    # Use sudo with minimal scope
    sudo --non-interactive \
         --reset-timestamp \
         "$command" "$@"
}

# Usage
drop_privileges "appuser"
```

### 7. Environment Variable Sanitization

**Clean environment before executing:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Clean environment
clean_environment() {
    # Unset dangerous variables
    unset IFS
    unset CDPATH
    unset GLOBIGNORE

    # Set safe PATH (absolute paths only)
    export PATH="/usr/local/bin:/usr/bin:/bin"

    # Set safe IFS
    IFS=$'\n\t'
}

# Execute command in clean environment
exec_clean() {
    env -i \
        HOME="$HOME" \
        USER="$USER" \
        PATH="/usr/local/bin:/usr/bin:/bin" \
        "$@"
}

# Usage
clean_environment
exec_clean /usr/local/bin/myapp
```

### 8. Absolute Path Usage (2025 Best Practice)

**Always use absolute paths to prevent PATH hijacking:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# ❌ DANGEROUS - Vulnerable to PATH manipulation
curl https://example.com/data
jq '.items[]' data.json

# ✅ SAFE - Absolute paths
/usr/bin/curl https://example.com/data
/usr/bin/jq '.items[]' data.json

# ✅ SAFE - Verify command location
CURL=$(command -v curl) || { echo "curl not found" >&2; exit 1; }
"$CURL" https://example.com/data
```

**Why This Matters:**
- Prevents malicious binaries in user PATH
- Standard practice in enterprise environments
- Required for security-sensitive scripts

### 9. History File Protection (2025 Security)

**Disable history for credential operations:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Disable history for this session
HISTFILE=/dev/null
export HISTFILE

# Or disable specific commands
HISTIGNORE="*password*:*secret*:*token*"
export HISTIGNORE

# Handle sensitive operations
read -rsp "Enter database password: " db_password
echo

# Use password (not logged to history)
/usr/bin/mysql -p"$db_password" -e "SELECT 1"

# Clear variable
unset db_password
```

## Security Checklist (2025)

Every script MUST pass these checks:

### Input Validation
- [ ] All user inputs validated with regex patterns
- [ ] Maximum length enforced on all inputs
- [ ] Empty/null inputs rejected
- [ ] Special characters escaped or rejected

### Command Safety
- [ ] No eval with user input
- [ ] No dynamic variable names from user input
- [ ] All command arguments use -- separator
- [ ] Arrays used instead of string concatenation

### File Operations
- [ ] All paths validated against directory traversal
- [ ] Temp files created with mktemp
- [ ] File permissions set restrictively (600/700)
- [ ] Cleanup handlers registered (trap EXIT)

### Secrets
- [ ] No hardcoded passwords/keys/tokens
- [ ] Secrets read from secure storage
- [ ] Secrets never logged or printed
- [ ] Secrets cleared from memory when done

### Privileges
- [ ] Runs with minimum required privileges
- [ ] Root execution rejected unless necessary
- [ ] Privilege drops implemented where needed
- [ ] Sudo scope minimized

### Error Handling
- [ ] set -euo pipefail enabled
- [ ] All errors logged to stderr
- [ ] Sensitive data not exposed in errors
- [ ] Exit codes meaningful

## Automated Security Scanning

### ShellCheck Integration

```bash
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  shellcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: ShellCheck
        run: |
          # Fail on security issues
          find . -name "*.sh" -exec shellcheck \
            --severity=error \
            --enable=all \
            {} +
```

### Custom Security Linting

```bash
#!/usr/bin/env bash
# security-lint.sh - Check scripts for security issues

set -euo pipefail

lint_script() {
    local script="$1"
    local issues=0

    echo "Checking: $script"

    # Check for eval
    if grep -n "eval" "$script"; then
        echo "  ❌ Found eval (command injection risk)"
        ((issues++))
    fi

    # Check for hardcoded secrets
    if grep -nE "(password|secret|token|key)\s*=\s*['\"][^'\"]+['\"]" "$script"; then
        echo "  ❌ Found hardcoded secrets"
        ((issues++))
    fi

    # Check for predictable temp files
    if grep -n "/tmp/[a-zA-Z0-9_-]*\\.tmp" "$script"; then
        echo "  ❌ Found predictable temp file"
        ((issues++))
    fi

    # Check for unquoted variables
    if grep -nE '\$[A-Z_]+[^"]' "$script"; then
        echo "  ⚠️  Found unquoted variables"
        ((issues++))
    fi

    if ((issues == 0)); then
        echo "  ✓ No security issues found"
    fi

    return "$issues"
}

# Scan all scripts
total_issues=0
while IFS= read -r -d '' script; do
    lint_script "$script" || ((total_issues++))
done < <(find . -name "*.sh" -type f -print0)

if ((total_issues > 0)); then
    echo "❌ Found security issues in $total_issues scripts"
    exit 1
else
    echo "✓ All scripts passed security checks"
fi
```

## Real-World Secure Script Template

```bash
#!/usr/bin/env bash
#
# Secure Script Template (2025)
#

set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Security: Reject root execution
if [[ $EUID -eq 0 ]]; then
    echo "Error: Do not run as root" >&2
    exit 1
fi

# Security: Clean environment
export PATH="/usr/local/bin:/usr/bin:/bin"
unset CDPATH GLOBIGNORE

# Security: Secure temp file
readonly TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"; exit' EXIT INT TERM
chmod 600 "$TEMP_FILE"

# Validate input
validate_input() {
    local input="$1"

    if [[ -z "$input" ]]; then
        echo "Error: Input required" >&2
        return 1
    fi

    if [[ ! "$input" =~ ^[a-zA-Z0-9_/-]+$ ]]; then
        echo "Error: Invalid characters in input" >&2
        return 1
    fi

    if [[ ${#input} -gt 255 ]]; then
        echo "Error: Input too long" >&2
        return 1
    fi

    return 0
}

# Sanitize file path
sanitize_path() {
    local path="$1"
    path="${path//..\/}"
    path="${path#/}"
    echo "$path"
}

# Main function
main() {
    local user_input="${1:-}"

    # Validate
    if ! validate_input "$user_input"; then
        exit 1
    fi

    # Sanitize
    local safe_path
    safe_path=$(sanitize_path "$user_input")

    # Process safely
    echo "Processing: $safe_path"
    # ... your logic here ...
}

main "$@"
```

## Compliance Standards (2025)

### CIS Benchmarks
- Use ShellCheck for automated compliance
- Implement input validation on all user data
- Secure temporary file handling
- Least privilege execution

### NIST Guidelines
- Strong input validation (NIST SP 800-53)
- Secure coding practices
- Logging and monitoring
- Access control enforcement

### OWASP Top 10
- A03: Injection - Prevent command injection
- A01: Broken Access Control - Path validation
- A02: Cryptographic Failures - Secure secrets

## Resources

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [ShellCheck Security Rules](https://www.shellcheck.net/wiki/)
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

---

**Security-first development is non-negotiable in 2025. Every script must pass all security checks before deployment.**
