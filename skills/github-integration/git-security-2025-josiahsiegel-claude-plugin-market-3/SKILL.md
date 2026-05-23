---
name: git-security-2025
description: Git security best practices for 2025 including signed commits, zero-trust workflows, secret scanning, and verification
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

# Git Security Best Practices 2025

## Zero-Trust Security Model (2025 Standard)

**What:** Every developer identity must be authenticated and authorized explicitly. All Git operations are logged, signed, and continuously monitored.

**Core Principles:**
1. **Never trust, always verify** - Every commit verified
2. **Least privilege access** - Minimal permissions required
3. **Continuous monitoring** - All operations logged and audited
4. **Assume breach** - Defense in depth strategies

### Implementing Zero-Trust for Git

**1. Mandatory Signed Commits:**
```bash
# Global requirement
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Enforce via branch protection (GitHub/GitLab/Azure DevOps)
# Repository Settings → Branches → Require signed commits
```

**2. Identity Verification:**
```bash
# Every commit must verify identity
git log --show-signature -10

# Reject unsigned commits in CI/CD
# .github/workflows/verify.yml
- name: Verify all commits are signed
  run: |
    git log --pretty="%H" origin/main..HEAD | while read commit; do
      if ! git verify-commit "$commit" 2>/dev/null; then
        echo "ERROR: Unsigned commit $commit"
        exit 1
      fi
    done
```

**3. Continuous Audit Logging:**
```bash
# Enable Git audit trail
git config --global alias.audit 'log --all --pretty="%H|%an|%ae|%ad|%s|%GK" --date=iso'

# Export audit log
git audit > git-audit.log

# Monitor for suspicious activity
git log --author="*" --since="24 hours ago" --pretty=format:"%an %ae %s"
```

**4. Least Privilege Access:**
```yaml
# GitHub branch protection (zero-trust model)
branches:
  main:
    protection_rules:
      required_pull_request_reviews: true
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
      required_approving_review_count: 2
      require_signed_commits: true
      enforce_admins: true
      restrictions:
        users: []  # No direct push
        teams: ["security-team"]
```

**5. Continuous Monitoring:**
```bash
# Monitor all repository changes
# .github/workflows/security-monitor.yml
name: Security Monitoring
on: [push, pull_request]
jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for unsigned commits
        run: git verify-commit HEAD || echo "::warning::Unsigned commit detected"

      - name: Scan for secrets
        run: gitleaks detect --exit-code 1

      - name: Check commit author
        run: |
          AUTHOR=$(git log -1 --format='%an <%ae>')
          echo "Commit by: $AUTHOR"
          # Log to SIEM/security monitoring
```

## Signed Commits (Mandatory in 2025)

**Why:** Cryptographically verify commit authorship, prevent impersonation, ensure audit trail.

**Industry Trend:** Signed commits increasingly required in 2025 workflows.

### GPG Signing (Traditional)

**Setup:**

```bash
# Generate GPG key
gpg --full-generate-key
# Choose: RSA and RSA, 4096 bits, expires in 2y

# List keys
gpg --list-secret-keys --keyid-format=long

# Example output:
# sec   rsa4096/ABC123DEF456 2025-01-15 [SC] [expires: 2027-01-15]
# uid                 [ultimate] Your Name <your.email@example.com>
# ssb   rsa4096/GHI789JKL012 2025-01-15 [E] [expires: 2027-01-15]

# Configure Git
git config --global user.signingkey ABC123DEF456
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Export public key for GitHub/GitLab
gpg --armor --export ABC123DEF456
# Copy output and add to GitHub/GitLab/Bitbucket

# Sign commits
git commit -S -m "feat: add authentication"

# Verify signatures
git log --show-signature
git verify-commit HEAD
git verify-tag v1.0.0
```

**Troubleshooting:**

```bash
# GPG agent not running
export GPG_TTY=$(tty)
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc

# Cache passphrase longer
echo 'default-cache-ttl 34560000' >> ~/.gnupg/gpg-agent.conf
echo 'max-cache-ttl 34560000' >> ~/.gnupg/gpg-agent.conf
gpg-connect-agent reloadagent /bye

# Test signing
echo "test" | gpg --clearsign
```

### SSH Signing (Modern Alternative - 2023+)

**Why SSH:** Simpler, reuse existing SSH keys, no GPG required.

**Setup:**

```bash
# Check if SSH key exists
ls -la ~/.ssh/id_ed25519.pub

# Generate if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Configure Git to use SSH signing
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Add public key to GitHub
cat ~/.ssh/id_ed25519.pub
# GitHub Settings → SSH and GPG keys → New SSH key → Key type: Signing Key

# Sign commits (automatic with commit.gpgsign=true)
git commit -m "feat: add feature"

# Verify
git log --show-signature
```

**Configure allowed signers file (for verification):**

```bash
# Create allowed signers file
echo "your.email@example.com $(cat ~/.ssh/id_ed25519.pub)" > ~/.ssh/allowed_signers

# Configure Git
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers

# Verify commits
git verify-commit HEAD
```

## Secret Scanning & Prevention

### GitHub Secret Scanning (Push Protection)

**Enable in repository:**
- Settings → Code security → Secret scanning → Enable
- Enable push protection (blocks secrets at push time)

**AI-powered detection (2025):**
- AWS credentials
- Azure service principals
- Google Cloud keys
- GitHub tokens
- Database connection strings
- API keys (OpenAI, Stripe, Anthropic, etc.)
- Private keys
- OAuth tokens
- Custom patterns

**Example blocked push:**

```bash
$ git push
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote:
remote: - Push cannot contain secrets
remote:
remote:   Resolve the following violations before pushing again
remote:
remote:   — AWS Access Key
remote:     locations:
remote:       - config.py:12
remote:
remote:   (Disable push protection: https://github.com/settings/security_analysis)
remote:
To github.com:user/repo.git
 ! [remote rejected] main -> main (push declined due to repository rule violations)
```

**Fix:**

```bash
# Remove secret from file
# Use environment variable instead
echo "AWS_ACCESS_KEY=your_key" >> .env
echo ".env" >> .gitignore

# Remove from history if already committed
git rm --cached config.py
git commit -m "Remove secrets"

# If in history, use filter-repo
git filter-repo --path config.py --invert-paths
git push --force
```

### Gitleaks (Local Scanning)

**Install:**

```bash
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# Windows
choco install gitleaks
```

**Usage:**

```bash
# Scan entire repository
gitleaks detect

# Scan uncommitted changes
gitleaks protect

# Scan specific directory
gitleaks detect --source ./src

# Generate report
gitleaks detect --report-format json --report-path gitleaks-report.json

# Use in CI/CD
gitleaks detect --exit-code 1
```

**Pre-commit hook:**

```bash
# .git/hooks/pre-commit
#!/bin/bash
gitleaks protect --staged --verbose
if [ $? -ne 0 ]; then
    echo "⚠️  Gitleaks detected secrets. Commit blocked."
    exit 1
fi
```

### Git-secrets (AWS-focused)

```bash
# Install
brew install git-secrets  # macOS
# or
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install

# Initialize in repository
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'password\s*=\s*[^\s]+'
git secrets --add 'api[_-]?key\s*=\s*[^\s]+'

# Scan
git secrets --scan
git secrets --scan-history
```

## Enforce Signed Commits

### Branch Protection Rules

**GitHub:**

```
Repository → Settings → Branches → Branch protection rules
☑ Require signed commits
☑ Require linear history
☑ Require status checks to pass
```

**GitLab:**

```
Repository → Settings → Repository → Protected branches
☑ Allowed to push: No one
☑ Allowed to merge: Maintainers
☑ Require all commits be signed
```

**Azure DevOps:**

```
Branch Policies → Add policy → Require signed commits
```

### Pre-receive Hook (Server-side enforcement)

```bash
#!/bin/bash
# .git/hooks/pre-receive (on server)

zero_commit="0000000000000000000000000000000000000000"

while read oldrev newrev refname; do
  # Skip branch deletion
  if [ "$newrev" = "$zero_commit" ]; then
    continue
  fi

  # Check all commits in push
  for commit in $(git rev-list "$oldrev".."$newrev"); do
    # Verify commit signature
    if ! git verify-commit "$commit" 2>/dev/null; then
      echo "Error: Commit $commit is not signed"
      echo "All commits must be signed. Configure with:"
      echo "  git config commit.gpgsign true"
      exit 1
    fi
  done
done

exit 0
```

## Security Configuration

### Recommended Git Config

```bash
# Enforce signed commits
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Use SSH signing (modern)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub

# Security settings
git config --global protocol.version 2
git config --global transfer.fsckobjects true
git config --global fetch.fsckobjects true
git config --global receive.fsckobjects true

# Prevent credential leaks
git config --global credential.helper cache --timeout=3600
# Or use system credential manager
git config --global credential.helper wincred  # Windows
git config --global credential.helper osxkeychain  # macOS

# Line ending safety
git config --global core.autocrlf true  # Windows
git config --global core.autocrlf input  # macOS/Linux

# Editor safety (avoid nano/vim leaks)
git config --global core.editor "code --wait"
```

### .gitignore Security

```gitignore
# Secrets
.env
.env.*
*.pem
*.key
*.p12
*.pfx
*_rsa
*_dsa
*_ecdsa
*_ed25519
credentials.json
secrets.yaml
config/secrets.yml

# Cloud provider
.aws/
.azure/
.gcloud/
gcloud-service-key.json

# Databases
*.sqlite
*.db

# Logs (may contain sensitive data)
*.log
logs/

# IDE secrets
.vscode/settings.json
.idea/workspace.xml

# Build artifacts (may contain embedded secrets)
dist/
build/
node_modules/
vendor/
```

## Credential Management

### SSH Keys

```bash
# Generate secure SSH key
ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/id_ed25519_work

# Use ed25519 (modern, secure, fast)
# Avoid RSA < 4096 bits
# Avoid DSA (deprecated)

# Configure SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_work

# Test connection
ssh -T git@github.com

# Use different keys for different services
# ~/.ssh/config
Host github.com
  IdentityFile ~/.ssh/id_ed25519_github

Host gitlab.com
  IdentityFile ~/.ssh/id_ed25519_gitlab
```

### HTTPS Credentials

```bash
# Use credential manager (not plaintext!)

# Windows
git config --global credential.helper wincred

# macOS
git config --global credential.helper osxkeychain

# Linux (libsecret)
git config --global credential.helper /usr/share/git/credential/libsecret/git-credential-libsecret

# Cache for limited time (temporary projects)
git config --global credential.helper 'cache --timeout=3600'
```

### Personal Access Tokens (PAT)

**GitHub:**
- Settings → Developer settings → Personal access tokens → Fine-grained tokens
- Set expiration (max 1 year)
- Minimum scopes needed
- Use for HTTPS authentication

**Never commit tokens:**

```bash
# Use environment variable
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
git clone https://$GITHUB_TOKEN@github.com/user/repo.git

# Or use Git credential helper
gh auth login  # GitHub CLI method
```

## CodeQL & Security Scanning

### GitHub CodeQL

**.github/workflows/codeql.yml:**

```yaml
name: "CodeQL Security Scan"

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly scan

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript', 'python', 'java' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}
        queries: security-and-quality

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
      with:
        category: "/language:${{ matrix.language }}"
```

**Detects:**
- SQL injection
- XSS vulnerabilities
- Path traversal
- Command injection
- Insecure deserialization
- Authentication bypass
- Hardcoded secrets

## Audit Trail

### Enable detailed logging

```bash
# Log all Git operations
git config --global alias.ll 'log --all --graph --decorate --oneline --show-signature'

# Check commit verification
git log --show-signature -10

# Export audit log
git log --pretty=format:"%H,%an,%ae,%ad,%s" --date=iso > git-audit.csv

# Verify all commits in branch
git log --show-signature main..HEAD
```

## Security Checklist

**Repository Setup:**
- ☑ Enable branch protection
- ☑ Require signed commits
- ☑ Enable secret scanning with push protection
- ☑ Enable CodeQL or similar scanning
- ☑ Configure Dependabot/Renovate
- ☑ Require 2FA for all contributors

**Developer Workstation:**
- ☑ Use GPG or SSH commit signing
- ☑ Configure credential manager (never plaintext)
- ☑ Install and configure gitleaks
- ☑ Create comprehensive .gitignore
- ☑ Enable fsckobjects for transfers
- ☑ Use SSH keys with passphrase

**Workflow:**
- ☑ Never commit secrets
- ☑ Review changes before commit
- ☑ Verify signatures on pull/merge
- ☑ Regular security audits
- ☑ Rotate credentials periodically
- ☑ Use environment variables for secrets

## Incident Response

**Secret leaked in commit:**

```bash
# 1. Rotate compromised credentials IMMEDIATELY
# 2. Remove from latest commit (if not pushed)
git reset HEAD~1
# Edit files to remove secret
git add .
git commit -m "Remove secrets"

# 3. If pushed, remove from history
git filter-repo --path config/secrets.yml --invert-paths
git push --force

# 4. Notify team to re-clone
# 5. Enable push protection to prevent future leaks
```

**Unsigned commits detected:**

```bash
# Identify unsigned commits
git log --show-signature | grep "No signature"

# Re-sign commits (if you authored them)
git rebase --exec 'git commit --amend --no-edit -n -S' -i HEAD~10

# Force push (with team coordination)
git push --force-with-lease
```

## Resources

- [Git Signing Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [CodeQL Documentation](https://codeql.github.com/docs/)
