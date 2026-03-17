---
name: check-no-secrets
description: Scans codebase for accidentally committed secrets, credentials, API keys, and sensitive data to prevent security breaches
user-invocable: true
---

# Check for Secrets Skill

## Purpose
Scans codebase for accidentally committed secrets, credentials, API keys, and sensitive data. Prevents catastrophic security breaches.

## CLAUDE.md Compliance
- ✅ Enforces no hardcoded secrets
- ✅ Validates environment variable usage
- ✅ Checks git history for leaked credentials
- ✅ Security-critical validation

## Usage
Run this skill:
- Before every commit
- Before pull requests
- After adding new integrations
- Weekly security scans
- Before production deployments

## Prerequisites
- ripgrep (`rg`)
- git

## Commands

### Quick Secret Scan
```bash
# Run automated secret detection
./scripts/validate-no-secrets.sh
```

### Comprehensive Secret Detection
```bash
# 1. Check for API keys
echo "🔑 Checking for API keys..."
rg -i "api[_-]?key.*=.*['\"][a-zA-Z0-9]{20,}" src/ --type rust -n

# 2. Check for passwords
echo "🔒 Checking for hardcoded passwords..."
rg -i "password.*=.*['\"][^'\"]{8,}" src/ --type rust -n | grep -v "example"

# 3. Check for tokens
echo "🎫 Checking for access tokens..."
rg -i "token.*=.*['\"][a-zA-Z0-9]{40,}" src/ --type rust -n

# 4. Check for database URLs
echo "🗄️ Checking for database URLs..."
rg "postgres://|mysql://|mongodb://" src/ --type rust -n

# 5. Check for OAuth secrets
echo "🔐 Checking for OAuth client secrets..."
rg "client_secret.*=.*['\"]" src/ --type rust -n | grep -v "env\|config"

# 6. Check for encryption keys
echo "🔓 Checking for hardcoded encryption keys..."
rg "const.*KEY.*=.*['\"][A-Za-z0-9+/=]{32,}" src/ --type rust -n

# 7. Check for AWS credentials
echo "☁️ Checking for AWS credentials..."
rg "AKIA[0-9A-Z]{16}" . -n

# 8. Check for private keys
echo "🗝️ Checking for private keys..."
rg "BEGIN.*PRIVATE.*KEY|BEGIN RSA PRIVATE KEY" . -n
```

### Environment File Checks
```bash
# Check .env is not tracked
echo "📋 Checking .env files..."
git ls-files | rg "\.env$" && \
  echo "❌ .env file tracked in git!" || \
  echo "✓ No .env in git"

# Verify .env in .gitignore
grep -q "^\.env$" .gitignore && \
  echo "✓ .env in .gitignore" || \
  echo "⚠️  Add .env to .gitignore"

# Check for committed .env files
find . -name ".env" -type f | while read env_file; do
    if git ls-files --error-unmatch "$env_file" 2>/dev/null; then
        echo "❌ ALERT: $env_file is tracked in git!"
    fi
done
```

## Common Secret Patterns

### API Keys
```rust
// ❌ FORBIDDEN
const API_KEY: &str = "sk_live_51H9xK2...";
let api_key = "pk_test_abc123...";

// ✅ CORRECT
let api_key = env::var("API_KEY")
    .map_err(|_| ConfigError::MissingApiKey)?;
```

### OAuth Client Secrets
```rust
// ❌ FORBIDDEN
let client_secret = "your-client-secret-here";

// ✅ CORRECT
let client_secret = env::var("STRAVA_CLIENT_SECRET")
    .map_err(|_| ConfigError::MissingStravaSecret)?;
```

### Database URLs
```rust
// ❌ FORBIDDEN
const DATABASE_URL: &str = "postgres://user:password@localhost/db";

// ✅ CORRECT
let database_url = env::var("DATABASE_URL")
    .map_err(|_| ConfigError::MissingDatabaseUrl)?;
```

### Log Output Secret/PII Scanning
```bash
# Check for secrets/tokens logged without redaction
echo "📋 Checking log statements for leaked secrets..."

# Look for access_token, refresh_token, api_key, password logged directly
rg "(info!|warn!|error!|debug!|trace!)\(.*\{.*(access_token|refresh_token|api_key|password|client_secret|authorization)" src/ --type rust -n | \
  rg -v "redact|REDACTED|\\*\\*\\*|mask" && \
  echo "❌ SECURITY: Secrets in log statements without redaction!" || \
  echo "✓ No unredacted secrets in log statements"

# Check for PII in INFO+ level logs (should be DEBUG only)
echo "📋 Checking PII in log levels..."
rg "(info!|warn!|error!)\(.*\{.*(email|ip_address|user_agent)" src/ --type rust -n | \
  rg -v "redact|REDACTED|mask" && \
  echo "⚠️  PII in INFO+ logs (should be DEBUG or redacted)" || \
  echo "✓ PII properly handled in log levels"

# Verify redaction middleware is active
rg "redact|sanitize.*log|PiiRedact" src/ --type rust -n | wc -l
echo "Redaction function references (should be >0)"
```

## Success Criteria
- ✅ No API keys in source code
- ✅ No passwords in source code
- ✅ No OAuth secrets in source code
- ✅ No database URLs with credentials
- ✅ No encryption keys hardcoded
- ✅ .env files not tracked in git
- ✅ .env in .gitignore
- ✅ All secrets from environment variables
- ✅ Git history clean (no historical leaks)
- ✅ No unredacted secrets in log statements
- ✅ No PII in INFO+ log levels

## Related Files
- `scripts/validate-no-secrets.sh` - Secret detection script
- `.gitignore` - Excludes .env and sensitive files
- `.env.example` - Template for environment variables
- `book/src/configuration.md` - Configuration documentation

## Related Skills
- `validate-architecture` - Architectural validation
- `strict-clippy-check` - Code quality
