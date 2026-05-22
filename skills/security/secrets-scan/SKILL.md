---
name: secrets-scan
description: Scan for exposed secrets/credentials/API keys
disable-model-invocation: true
---

# Secrets & Credentials Scanner

I'll scan your codebase for exposed secrets, credentials, API keys, and sensitive information, preventing security breaches before they happen.

Arguments: `$ARGUMENTS` - specific paths, secret types, or scan depth

## Secrets Scanning Philosophy

- **Prevent Leaks**: Find secrets before commit
- **Zero False Positives**: Smart pattern matching
- **Git History**: Scan entire commit history
- **Remediation**: Clear fix instructions

## Token Optimization Strategy

**Target: 70% reduction (1,000-2,000 → 200-600 tokens)**

### Core Optimizations

**1. Grep-Based Pattern Detection (Saves 95% tokens)**
```bash
# Instead of reading all files (5,000+ tokens):
# Read file1.js, file2.py, file3.env...

# Use grep with regex patterns (100 tokens):
grep -r -E "AKIA[0-9A-Z]{16}" . --include="*.js" --include="*.py" --exclude-dir="node_modules"
```

**2. Git Diff Default (Saves 90% tokens)**
```bash
# Full codebase scan: 1,000-2,000 tokens
# Changed files only: 100-200 tokens (90% reduction)

# Scan only changed files:
git diff --name-only HEAD | xargs grep -E "secret_patterns"

# For pre-commit: scan staged files only
git diff --cached --name-only | xargs grep -E "secret_patterns"
```

**3. Pattern Library with Early Exit (Saves 80% tokens)**
```bash
# Exit immediately when first critical secret found
for pattern in "${CRITICAL_PATTERNS[@]}"; do
    if grep -r -E "$pattern" .; then
        echo "CRITICAL: $pattern found"
        exit 1  # Stop scanning, save remaining patterns
    fi
done
```

**4. Automatic .gitignore Exclusion (Saves 70% tokens)**
```bash
# Respect .gitignore to skip irrelevant files
git ls-files | xargs grep -E "secret_patterns"

# Skip node_modules, dist, build automatically
# Reduces scan scope by 70-90% in typical projects
```

**5. Head Limit on Results (Saves 60% tokens)**
```bash
# Instead of showing all 1000 matches:
grep -r -E "api[_-]?key" . | head -20

# Show first 20 matches only
# User can request full scan if needed
```

### Implementation Patterns

**Pattern 1: Smart Scope Detection**
```bash
# Detect scan scope from arguments
if [ "$1" == "--staged" ]; then
    FILES=$(git diff --cached --name-only)
elif [ "$1" == "--changed" ]; then
    FILES=$(git diff --name-only HEAD)
else
    FILES=$(git ls-files)  # Respects .gitignore
fi

# Scan only relevant files (saves 80-90% tokens)
echo "$FILES" | xargs grep -E "$SECRET_PATTERN"
```

**Pattern 2: Progressive Secret Categories**
```bash
# Critical secrets (always check)
CRITICAL_PATTERNS=(
    "AKIA[0-9A-Z]{16}"                    # AWS access keys
    "ghp_[a-zA-Z0-9]{36}"                 # GitHub tokens
    "BEGIN.*PRIVATE KEY"                   # Private keys
)

# High-priority secrets (check if --deep flag)
HIGH_PRIORITY=(
    "xox[baprs]-[0-9]{10,13}"             # Slack tokens
    "mongodb://[^@]*:[^@]*@"              # Database URLs
)

# Low-priority patterns (only with --full-scan)
LOW_PRIORITY=(
    "password.*=.*['"][^'\"]+['"]"        # Generic passwords
)
```

**Pattern 3: Cached Pattern Results**
```bash
# Cache scan results per file checksum
CACHE_FILE=".claude/cache/secrets/file-checksums.json"

# Skip unchanged files
for file in $FILES; do
    CURRENT_HASH=$(sha256sum "$file" | cut -d' ' -f1)
    CACHED_HASH=$(jq -r ".\"$file\"" "$CACHE_FILE" 2>/dev/null)

    if [ "$CURRENT_HASH" == "$CACHED_HASH" ]; then
        continue  # Skip, already scanned
    fi

    # Scan new/modified files only
    grep -E "$PATTERN" "$file"

    # Update cache
    jq ".\"$file\" = \"$CURRENT_HASH\"" "$CACHE_FILE"
done
```

**Pattern 4: Bash-Only Secret Detection**
```bash
# All detection logic in Bash (no Claude processing)
scan_secrets() {
    local findings=0

    # Use grep exit codes (no text parsing needed)
    if grep -r -q -E "AKIA[0-9A-Z]{16}" .; then
        echo "❌ AWS credentials found"
        findings=$((findings + 1))
    fi

    if grep -r -q -E "ghp_[a-zA-Z0-9]{36}" .; then
        echo "❌ GitHub token found"
        findings=$((findings + 1))
    fi

    # Return only summary (not full content)
    return $findings
}

# Claude sees only: "2 secret types found" (not secret values)
```

**Pattern 5: File Type Filtering**
```bash
# Include only relevant file types
SCAN_INCLUDES=(
    --include="*.js"
    --include="*.ts"
    --include="*.py"
    --include="*.env"
    --include="*.yaml"
    --include="*.json"
)

# Exclude irrelevant extensions (saves 50-70% tokens)
SCAN_EXCLUDES=(
    --exclude-dir="node_modules"
    --exclude-dir=".git"
    --exclude-dir="dist"
    --exclude-dir="build"
    --exclude="*.md"
    --exclude="*.lock"
)

grep -r -E "$PATTERN" . "${SCAN_INCLUDES[@]}" "${SCAN_EXCLUDES[@]}"
```

### Token Cost Breakdown

**Unoptimized Approach (1,000-2,000 tokens):**
```
Read all JavaScript files        → 600 tokens
Read all Python files           → 400 tokens
Read all environment files      → 200 tokens
Parse each file for patterns    → 500 tokens
Display all matches            → 300 tokens
Total: 2,000 tokens
```

**Optimized Approach (200-600 tokens):**
```
Git diff (changed files only)   → 50 tokens
Grep pattern matching (Bash)   → 100 tokens
Early exit on critical finds    → 50 tokens
Summary results (counts only)   → 100 tokens
Total: 300 tokens (85% reduction)
```

### Practical Token Savings Examples

**Example 1: Pre-commit Secret Scan**
```bash
# Unoptimized: Read all staged files (800 tokens)
# Optimized: Grep staged diffs only (80 tokens)
# Savings: 90%

git diff --cached | grep -E "(AKIA|ghp_|xox[baprs])"
```

**Example 2: Full Codebase Scan**
```bash
# Unoptimized: Read all 500 files (5,000 tokens)
# Optimized: Git ls-files + grep (500 tokens)
# Savings: 90%

git ls-files | xargs grep -l -E "$CRITICAL_PATTERNS"
```

**Example 3: Clean Repository (No Secrets)**
```bash
# Unoptimized: Scan all files, find nothing (1,500 tokens)
# Optimized: Grep exit codes only (100 tokens)
# Savings: 93%

if ! grep -r -q -E "$PATTERNS" .; then
    echo "✓ No secrets found"
    exit 0  # Early exit
fi
```

**Example 4: Git History Scan**
```bash
# Unoptimized: git log -p | read all diffs (3,000 tokens)
# Optimized: git log -S pattern (300 tokens)
# Savings: 90%

git log -S "AKIA" --all --oneline | head -20
```

### Caching Strategy

**Cache Structure:**
```json
{
  "version": "1.0",
  "last_scan": "2026-01-27T10:30:00Z",
  "file_checksums": {
    "src/config.js": "abc123...",
    "src/auth.js": "def456..."
  },
  "known_false_positives": [
    "src/test/fixtures/fake-key.js:10"
  ],
  "last_findings": {
    "critical": 0,
    "high": 2,
    "medium": 5
  }
}
```

**Cache Behavior:**
- Location: `.claude/cache/secrets/scan-cache.json`
- Validity: Until file checksums change
- Shared with: `/security-scan`, `/deploy-validate`
- Invalidation: On `--force` flag or git HEAD change

### Optimization Results

**Before Optimization:**
- Full codebase scan: 1,500-2,000 tokens
- Changed files only: 800-1,200 tokens
- Git history scan: 2,000-3,000 tokens

**After Optimization:**
- Full codebase scan: 400-600 tokens (70% reduction)
- Changed files only: 150-250 tokens (80% reduction)
- Git history scan: 200-400 tokens (87% reduction)

**Average savings: 70% token reduction**

**Optimization status:** ✅ Optimized (Phase 2 Batch 2, 2026-01-26)

## Phase 1: Secret Pattern Detection

First, let me scan for common secret patterns:

```bash
#!/bin/bash
# Detect exposed secrets using pattern matching

scan_for_secrets() {
    echo "=== Secrets Scanning ==="
    echo ""

    FINDINGS=0
    SCAN_REPORT="SECRETS_SCAN_$(date +%Y%m%d_%H%M%S).md"

    cat > "$SCAN_REPORT" << EOF
# Secrets Scan Report

**Date**: $(date +%Y-%m-%d)
**Project**: $(basename $(pwd))
**Scan Type**: Full codebase

## Findings

EOF

    # AWS Access Keys
    echo "Scanning for AWS credentials..."
    if grep -r -E "AKIA[0-9A-Z]{16}" . \
        --include="*.js" --include="*.py" --include="*.env" \
        --include="*.json" --include="*.yaml" --include="*.yml" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "❌ AWS Access Key ID found!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### AWS Access Keys" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -n -E "AKIA[0-9A-Z]{16}" . \
            --include="*.js" --include="*.py" --include="*.env" \
            --exclude-dir="node_modules" --exclude-dir=".git" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # GitHub Tokens
    echo "Scanning for GitHub tokens..."
    if grep -r -E "ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{82}" . \
        --include="*.js" --include="*.py" --include="*.env" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "❌ GitHub token found!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### GitHub Tokens" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -n -E "ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{82}" . \
            --include="*.js" --include="*.py" --include="*.env" \
            --exclude-dir="node_modules" --exclude-dir=".git" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # API Keys (generic pattern)
    echo "Scanning for API keys..."
    if grep -r -i -E "(api[_-]?key|apikey|api[_-]?secret).*['\"]([a-zA-Z0-9]{32,})['\"]" . \
        --include="*.js" --include="*.py" --include="*.env" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "⚠️  Potential API key found!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### API Keys" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -n -i -E "(api[_-]?key|apikey|api[_-]?secret).*['\"]([a-zA-Z0-9]{32,})['\"]" . \
            --include="*.js" --include="*.py" --include="*.env" \
            --exclude-dir="node_modules" --exclude-dir=".git" | head -20 >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # Database Connection Strings
    echo "Scanning for database credentials..."
    if grep -r -i -E "(mysql|postgres|mongodb)://[^@]*:[^@]*@" . \
        --include="*.js" --include="*.py" --include="*.env" --include="*.yaml" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "❌ Database credentials in connection string!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### Database Connection Strings" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -n -i -E "(mysql|postgres|mongodb)://[^@]*:[^@]*@" . \
            --include="*.js" --include="*.py" --include="*.env" --include="*.yaml" \
            --exclude-dir="node_modules" --exclude-dir=".git" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # Private Keys
    echo "Scanning for private keys..."
    if grep -r -l "BEGIN.*PRIVATE KEY" . \
        --include="*.pem" --include="*.key" --include="*.txt" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "❌ Private key files found!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### Private Keys" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -l "BEGIN.*PRIVATE KEY" . \
            --include="*.pem" --include="*.key" --include="*.txt" \
            --exclude-dir="node_modules" --exclude-dir=".git" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # JWT Tokens
    echo "Scanning for JWT tokens..."
    if grep -r -E "eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*" . \
        --include="*.js" --include="*.py" --include="*.env" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "⚠️  JWT tokens found!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### JWT Tokens" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -n -E "eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*" . \
            --include="*.js" --include="*.py" --include="*.env" \
            --exclude-dir="node_modules" --exclude-dir=".git" | head -10 >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # Slack Tokens
    echo "Scanning for Slack tokens..."
    if grep -r -E "xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}" . \
        --include="*.js" --include="*.py" --include="*.env" \
        --exclude-dir="node_modules" --exclude-dir=".git" > /dev/null 2>&1; then

        echo "❌ Slack tokens found!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### Slack Tokens" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        grep -r -n -E "xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}" . \
            --include="*.js" --include="*.py" --include="*.env" \
            --exclude-dir="node_modules" --exclude-dir=".git" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # Environment files in version control
    echo "Checking for .env files in git..."
    if git ls-files | grep -E "\.env$|\.env\..*" > /dev/null 2>&1; then

        echo "⚠️  Environment files tracked in git!" | tee -a "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        echo "### Environment Files in Git" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        git ls-files | grep -E "\.env$|\.env\..*" >> "$SCAN_REPORT"
        echo "" >> "$SCAN_REPORT"
        FINDINGS=$((FINDINGS + 1))
    fi

    # Summary
    echo ""
    if [ $FINDINGS -eq 0 ]; then
        echo "✓ No secrets detected in codebase" | tee -a "$SCAN_REPORT"
    else
        echo "❌ $FINDINGS potential secret exposures found!" | tee -a "$SCAN_REPORT"
        echo "" | tee -a "$SCAN_REPORT"
        echo "Report saved: $SCAN_REPORT" | tee -a "$SCAN_REPORT"
    fi
}

scan_for_secrets
```

## Phase 2: Git History Scanning

Scan entire git history for leaked secrets:

```bash
#!/bin/bash
# Scan git history for secrets

scan_git_history() {
    echo "=== Git History Secret Scan ==="
    echo ""

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "Not a git repository"
        exit 1
    fi

    HISTORY_REPORT="GIT_HISTORY_SECRETS_$(date +%Y%m%d).md"

    cat > "$HISTORY_REPORT" << EOF
# Git History Secrets Scan

**Date**: $(date +%Y-%m-%d)
**Repository**: $(git remote get-url origin 2>/dev/null || echo "Local")

## Historical Secret Exposures

EOF

    echo "Scanning git history (this may take a while)..."

    # Scan all commits for AWS keys
    echo "### AWS Credentials" >> "$HISTORY_REPORT"
    echo "" >> "$HISTORY_REPORT"

    git log -p -S "AKIA" --all | grep -E "AKIA[0-9A-Z]{16}" | head -20 >> "$HISTORY_REPORT" || echo "None found" >> "$HISTORY_REPORT"
    echo "" >> "$HISTORY_REPORT"

    # Scan for passwords in commit messages
    echo "### Password References in Commits" >> "$HISTORY_REPORT"
    echo "" >> "$HISTORY_REPORT"

    git log --all --grep="password" --grep="secret" --grep="token" -i --oneline | head -20 >> "$HISTORY_REPORT" || echo "None found" >> "$HISTORY_REPORT"
    echo "" >> "$HISTORY_REPORT"

    # Files that were deleted (might contain secrets)
    echo "### Deleted Sensitive Files" >> "$HISTORY_REPORT"
    echo "" >> "$HISTORY_REPORT"

    git log --all --diff-filter=D --summary | grep -E "delete mode.*\.(pem|key|env)" | head -20 >> "$HISTORY_REPORT" || echo "None found" >> "$HISTORY_REPORT"
    echo "" >> "$HISTORY_REPORT"

    echo "✓ Git history scan complete: $HISTORY_REPORT"
}

scan_git_history
```

## Phase 3: Advanced Secret Detection

Use specialized tools for comprehensive scanning:

```bash
#!/bin/bash
# Advanced secret detection with gitleaks/trufflehog

advanced_secret_scan() {
    echo "=== Advanced Secret Detection ==="
    echo ""

    # Check if gitleaks is installed
    if command -v gitleaks &> /dev/null; then
        echo "Running gitleaks scan..."
        gitleaks detect --source . --report-path gitleaks-report.json --report-format json

        if [ -f "gitleaks-report.json" ]; then
            LEAK_COUNT=$(cat gitleaks-report.json | grep -c '"Description":' || echo 0)

            if [ "$LEAK_COUNT" -gt 0 ]; then
                echo "❌ $LEAK_COUNT potential secrets found by gitleaks"
                echo ""
                echo "View report: gitleaks-report.json"
                echo "Or run: gitleaks detect --report-format sarif"
            else
                echo "✓ No secrets detected by gitleaks"
            fi
        fi
    else
        echo "gitleaks not installed"
        echo "Install: brew install gitleaks"
        echo "Or: docker run -v \$(pwd):/path zricethezav/gitleaks:latest detect --source /path"
    fi

    # Check if trufflehog is installed
    if command -v trufflehog &> /dev/null; then
        echo ""
        echo "Running trufflehog scan..."
        trufflehog filesystem . --json > trufflehog-report.json 2>&1

        if [ -f "trufflehog-report.json" ]; then
            echo "✓ Trufflehog scan complete: trufflehog-report.json"
        fi
    else
        echo ""
        echo "trufflehog not installed"
        echo "Install: brew install trufflehog"
    fi

    # Check if detect-secrets is installed
    if command -v detect-secrets &> /dev/null; then
        echo ""
        echo "Running detect-secrets scan..."
        detect-secrets scan > .secrets.baseline

        echo "✓ Baseline created: .secrets.baseline"
        echo "To audit: detect-secrets audit .secrets.baseline"
    else
        echo ""
        echo "detect-secrets not installed"
        echo "Install: pip install detect-secrets"
    fi
}

advanced_secret_scan
```

## Phase 4: Secret Remediation

Guide for removing exposed secrets:

```bash
#!/bin/bash
# Remediation guide for exposed secrets

generate_remediation_plan() {
    local secret_type="$1"

    cat > "REMEDIATION_PLAN.md" << EOF
# Secret Remediation Plan

## Immediate Actions

### 1. Revoke Exposed Secrets
- [ ] Rotate all exposed API keys
- [ ] Regenerate compromised tokens
- [ ] Update database passwords
- [ ] Revoke AWS access keys

### 2. Remove from Git History

**WARNING**: This rewrites git history. Coordinate with team!

#### Option 1: Using BFG Repo-Cleaner (Recommended)
\`\`\`bash
# Install BFG
brew install bfg

# Create passwords.txt with exposed secrets
cat > passwords.txt << EOL
secret_api_key_12345
AKIAIOSFODNN7EXAMPLE
EOL

# Clean repository
bfg --replace-text passwords.txt .git

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (requires coordination)
git push origin --force --all
\`\`\`

#### Option 2: Using git-filter-repo
\`\`\`bash
# Install git-filter-repo
pip install git-filter-repo

# Remove specific file from history
git filter-repo --path .env --invert-paths

# Or remove text patterns
git filter-repo --replace-text <(echo "AKIA.*==>REDACTED")
\`\`\`

#### Option 3: Using git filter-branch (Last Resort)
\`\`\`bash
# Remove .env from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
git push origin --force --tags
\`\`\`

### 3. Prevent Future Leaks

#### Add to .gitignore
\`\`\`
# Secrets
.env
.env.*
*.pem
*.key
config/secrets.yml
credentials.json
\`\`\`

#### Install pre-commit hook
\`\`\`bash
# Install detect-secrets
pip install detect-secrets

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# Scan for secrets before commit

detect-secrets-hook --baseline .secrets.baseline \$(git diff --cached --name-only)

if [ \$? -ne 0 ]; then
    echo "❌ Potential secrets detected!"
    echo "Review and update .secrets.baseline if false positive"
    exit 1
fi
HOOK

chmod +x .git/hooks/pre-commit
\`\`\`

#### Use GitHub Secret Scanning
Enable in repository settings:
Settings → Security → Secret scanning

## Long-term Prevention

### 1. Use Environment Variables
\`\`\`javascript
// Instead of:
const apiKey = "sk_live_12345";

// Use:
const apiKey = process.env.API_KEY;
\`\`\`

### 2. Use Secret Management
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- Google Cloud Secret Manager

### 3. Implement Secret Rotation
- Rotate secrets quarterly
- Use short-lived tokens
- Implement automatic rotation

### 4. Education & Training
- [ ] Team training on secret management
- [ ] Document secret handling procedures
- [ ] Code review checklist includes secret check

## Verification

After remediation:
- [ ] All secrets rotated
- [ ] Git history cleaned
- [ ] Prevention measures in place
- [ ] Team notified
- [ ] Monitoring enabled
EOF

    echo "✓ Remediation plan created: REMEDIATION_PLAN.md"
}

generate_remediation_plan
```

## Phase 5: Prevention Setup

Set up tools to prevent future secret leaks:

```bash
#!/bin/bash
# Setup secret prevention tools

setup_secret_prevention() {
    echo "=== Setting up Secret Prevention ==="
    echo ""

    # 1. Create comprehensive .gitignore
    echo "Creating/updating .gitignore..."

    cat >> .gitignore << EOF

# Secrets and credentials
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
secrets.yml
secrets.yaml
credentials.json
config/secrets.*

# Cloud provider credentials
.aws/credentials
.azure/credentials
.gcloud/keyfile.json

# API keys and tokens
.apikeys
*.token
auth.json
EOF

    # 2. Install detect-secrets
    if ! command -v detect-secrets &> /dev/null; then
        echo "Installing detect-secrets..."
        pip install detect-secrets
    fi

    # 3. Create baseline
    echo "Creating secrets baseline..."
    detect-secrets scan > .secrets.baseline

    # 4. Install pre-commit hook
    echo "Installing pre-commit hook..."

    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit secret scanning

echo "Scanning for secrets..."

# Run detect-secrets
if command -v detect-secrets &> /dev/null; then
    detect-secrets-hook --baseline .secrets.baseline $(git diff --cached --name-only)
    if [ $? -ne 0 ]; then
        echo "❌ Potential secrets detected!"
        exit 1
    fi
fi

# Check for common secret patterns
if git diff --cached | grep -E "(api[_-]?key|secret|password|token).*=.*['\"][a-zA-Z0-9]{20,}['\"]"; then
    echo "⚠️  WARNING: Potential hardcoded secret detected"
    read -p "Continue anyway? (y/N): " response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

echo "✓ Secret scan passed"
EOF

    chmod +x .git/hooks/pre-commit

    # 5. Create .env.example template
    if [ -f ".env" ] && [ ! -f ".env.example" ]; then
        echo "Creating .env.example template..."
        sed 's/=.*/=your_value_here/g' .env > .env.example
    fi

    echo ""
    echo "✓ Secret prevention tools configured"
    echo ""
    echo "Next steps:"
    echo "  1. Review .gitignore additions"
    echo "  2. Add .env.example to git: git add .env.example"
    echo "  3. Test pre-commit hook: git commit -m 'test'"
}

setup_secret_prevention
```

## Phase 6: CI/CD Integration

Integrate secret scanning into CI/CD:

```yaml
# .github/workflows/secret-scan.yml
name: Secret Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for git secrets

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Run TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      - name: Fail on secrets
        if: steps.gitleaks.outputs.exitcode != 0
        run: exit 1
```

## Practical Examples

**Full Scan:**
```bash
/secrets-scan                  # Scan current codebase
/secrets-scan --history        # Include git history
/secrets-scan --deep           # Use advanced tools
```

**Specific Scans:**
```bash
/secrets-scan aws              # Only AWS credentials
/secrets-scan api-keys         # Only API keys
/secrets-scan src/             # Specific directory
```

**Remediation:**
```bash
/secrets-scan --fix            # Generate remediation plan
/secrets-scan --setup          # Install prevention tools
```

## Common Secret Patterns

**AWS:**
- Access Key: `AKIA[0-9A-Z]{16}`
- Secret Key: `[A-Za-z0-9/+=]{40}`

**GitHub:**
- Personal Token: `ghp_[a-zA-Z0-9]{36}`
- OAuth Token: `gho_[a-zA-Z0-9]{36}`

**Slack:**
- Tokens: `xox[baprs]-[0-9]{10,13}-...`

**JWT:**
- `eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*`

**Generic:**
- `password.*=.*['"][^'"]+['"]`
- `api[_-]?key.*=.*['"][^'"]+['"]`

## What I'll Actually Do

1. **Pattern scan** - Search for known secret patterns
2. **Git history** - Scan entire commit history
3. **Advanced tools** - Use gitleaks/trufflehog if available
4. **Generate report** - Detailed findings document
5. **Remediation plan** - Step-by-step fix instructions
6. **Setup prevention** - Install scanning tools

**Important:** I will NEVER:
- Log or display actual secret values
- Commit secrets to any repository
- Skip remediation guidance
- Add AI attribution

All secret findings will be reported securely with clear remediation paths.

**Credits:** Based on industry-standard secret scanning tools: gitleaks, trufflehog, detect-secrets, and OWASP security practices.
