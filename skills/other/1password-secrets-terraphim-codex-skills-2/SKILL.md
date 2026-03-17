---
name: 1password-secrets
description: |
  Secure secret management using 1Password CLI. Detect plaintext secrets in files
  and codebases, convert environment files to 1Password templates, inject secrets
  securely using op inject, and audit codebases for security compliance.
license: Apache-2.0
---

# 1Password Secret Management Skill

**Version:** 1.0.0
**Author:** Claude Code
**Purpose:** Secure secret management using 1Password CLI

## Overview and Purpose

This skill provides comprehensive secret management using 1Password CLI (`op`). It helps you:

- Detect plaintext secrets in files and codebases
- Convert environment files to 1Password templates
- Inject secrets securely using `op inject`
- Run commands with secrets using `op run --no-masking`
- Audit codebases for security compliance
- Integrate 1Password with systemd services

**Critical Mandate:** This skill enforces the principle: **never commit plaintext secrets, never overwrite .env files, always use 1Password CLI**.

## Prerequisites

### Required

1. **1Password CLI (`op`)** installed and configured
   ```bash
   # Check installation
   which op && op --version

   # Install if needed (macOS)
   brew install 1password-cli

   # Install if needed (Linux)
   curl -sSfO https://downloads.1password.com/linux/tar/stable/x86_64/1password-cli-latest.tar.gz
   tar -xf 1password-cli-latest.tar.gz
   sudo mv op /usr/local/bin/
   ```

2. **1Password Account** signed in
   ```bash
   # Sign in
   op signin

   # Verify session
   op whoami
   ```

3. **1Password Vault** for storing secrets
   ```bash
   # List vaults
   op vault list

   # Create vault if needed
   op vault create "ProjectSecrets"
   ```

### Optional

- `jq` for JSON parsing (usually available)
- Git for version control

## Workflow 1: Detect Secrets

**Purpose:** Scan files for plaintext secrets and report findings without displaying values.

### When to Use

- Before committing code to version control
- During code reviews
- When auditing security compliance
- After receiving new configuration files

### How It Works

1. User provides file path
2. Skill validates `op` CLI is installed
3. Skill reads file line by line
4. Skill applies secret detection patterns
5. Skill reports findings with location, type, and confidence
6. **Secret values are NEVER displayed**

### Usage Pattern

```
User: "Scan /path/to/.env for secrets"

Assistant Process:
1. Check op CLI: `which op`
2. Read pattern database: ~/.docs/1password-skill/secret-patterns.json
3. Read target file line by line
4. Apply regex patterns to each line
5. For each match:
   - Record file:line:type:confidence
   - NEVER store or display the actual secret value
6. Report findings

Example Output:
Found 3 secrets in .env:
  Line 1: GITHUB_CLIENT_SECRET (github_oauth_secret, HIGH confidence)
  Line 5: JWT_SHARED_KEY (jwt_secret, HIGH confidence)
  Line 12: DATABASE_PASSWORD (database_password, HIGH confidence)

⚠️  Secret values are masked for security.
Recommendation: Convert to 1Password template (see Workflow 2)
```

### Implementation Steps

**Step 1: Validate op CLI**
```bash
which op || echo "ERROR: 1Password CLI not installed"
op whoami || echo "ERROR: Not signed in to 1Password"
```

**Step 2: Load Secret Patterns**
```bash
cat ~/.docs/1password-skill/secret-patterns.json | jq -r '.patterns[]'
```

**Step 3: Scan File**
For each line in target file:
- Apply each pattern from database
- If match found and not in exclude_patterns:
  - Record finding (line number, type, confidence)
  - Mask the actual value (show only first/last 4 chars or "***")

**Step 4: Report Results**
- Group by confidence level
- Show file:line:type for each finding
- Never display actual secret values
- Provide remediation recommendations

### Security Guarantees

✓ **Secret values are NEVER displayed**
✓ **Secret values are NEVER logged**
✓ **Original files are NEVER modified**
✓ **All operations are read-only**

---

## Workflow 2: Generate Template

**Purpose:** Convert environment files to 1Password templates with `op://` references.

### When to Use

- Migrating plaintext secrets to 1Password
- Setting up new projects with secure secret management
- Replacing hardcoded secrets in config files

### How It Works

1. User provides source file (e.g., `.env`)
2. Skill detects secrets (Workflow 1)
3. Skill creates `.env.template` with `op://` references
4. Skill generates migration guide with 1Password commands
5. Original file is NEVER modified

### Usage Pattern

```
User: "Generate 1Password template from /path/to/.env"

Assistant Process:
1. Run secret detection (Workflow 1)
2. Create output file: /path/to/.env.template
3. For each line:
   - If secret detected: Replace with op://Vault/Item/field
   - If non-secret: Copy as-is
   - If comment: Preserve
4. Generate migration guide
5. Show suggested 1Password vault structure

Example Output:
Created: /path/to/.env.template

Detected 3 secrets:
  GITHUB_CLIENT_SECRET → op://Terraphim/GitHub-OAuth/client_secret
  JWT_SHARED_KEY → op://Terraphim/JWT-Config/shared_key
  DATABASE_PASSWORD → op://Terraphim/Database/password

Migration Guide:
1. Create 1Password items:
   op item create --category=Login \
     --title="GitHub-OAuth" \
     --vault="Terraphim" \
     client_secret=<paste-value-here>

   op item create --category=Password \
     --title="JWT-Config" \
     --vault="Terraphim" \
     shared_key=<paste-value-here>

   op item create --category=Database \
     --title="Database" \
     --vault="Terraphim" \
     password=<paste-value-here>

2. Verify items created:
   op item list --vault="Terraphim"

3. Test injection (Workflow 3):
   op inject -i .env.template

4. Add to .gitignore:
   echo ".env" >> .gitignore
   echo ".env.local" >> .gitignore

5. Commit template:
   git add .env.template
   git commit -m "Add 1Password template for secrets"
```

### Template Format

**Input (.env):**
```env
# GitHub OAuth
GITHUB_CLIENT_ID=6182d53553cf86b0faf2
GITHUB_CLIENT_SECRET=952abb34b2f45f3e38f9e688f607a1e0e8b78cf4

# JWT Configuration
JWT_SHARED_KEY=terraphim-jwt-shared-key-5c28cc33679085bfd8189be4cbbaf913b5b83d389f41d9d76661e2d707e60abd

# Non-secret
PORT=8080
NODE_ENV=production
```

**Output (.env.template):**
```env
# GitHub OAuth
GITHUB_CLIENT_ID=6182d53553cf86b0faf2
GITHUB_CLIENT_SECRET=op://Terraphim/GitHub-OAuth/client_secret

# JWT Configuration
JWT_SHARED_KEY=op://Terraphim/JWT-Config/shared_key

# Non-secret
PORT=8080
NODE_ENV=production
```

### Naming Conventions

**Suggested 1Password Structure:**
- **Vault:** Project name (e.g., "Terraphim", "MyProject")
- **Item:** Service/component name (e.g., "GitHub-OAuth", "Database", "API-Keys")
- **Field:** Variable name in lowercase (e.g., "client_secret", "api_key", "password")

### Security Guarantees

✓ **Original .env file is NEVER modified**
✓ **Creates new .env.template file only**
✓ **Secret values shown in migration guide are for copy-paste only**
✓ **User must manually create 1Password items (not automated for security)**

---

## Workflow 3: Inject Secrets

**Purpose:** Populate templates with secrets from 1Password using `op inject`.

### When to Use

- Deploying applications locally or to servers
- Running services that need secrets
- Testing with real credentials
- CI/CD pipelines

### How It Works

1. User provides template file (`.env.template`)
2. Skill validates op session is active
3. Skill runs `op inject` to replace `op://` references with actual values
4. Skill outputs to specified location (NEVER overwrites original)
5. Skill reminds user to add output to `.gitignore`

### Usage Pattern

```
User: "Inject secrets from .env.template to /tmp/app.env"

Assistant Process:
1. Validate op session: `op whoami`
2. Check template exists and has op:// refs
3. Execute: `op inject -i .env.template -o /tmp/app.env`
4. Verify output file created
5. Remind about .gitignore

Example Output:
✓ 1Password session active
✓ Template validated: .env.template
✓ Injecting secrets...
✓ Created: /tmp/app.env (3 secrets injected)

⚠️  IMPORTANT:
- Add /tmp/app.env to .gitignore
- Never commit files with injected secrets
- Use this file only for local development/testing
- For production, use Workflow 4 (op run) instead
```

### Common Patterns

**Pattern 1: Local Development**
```bash
op inject -i .env.template -o .env.local
# Add .env.local to .gitignore
# Application reads from .env.local
```

**Pattern 2: CI/CD**
```bash
op inject -i .env.template -o /tmp/secrets.env
source /tmp/secrets.env
# Run tests or deployment
rm /tmp/secrets.env  # Clean up
```

**Pattern 3: Docker**
```bash
op inject -i app.env.template -o /tmp/app.env
docker run --env-file /tmp/app.env myapp:latest
```

### Safety Checks

Before injection:
- Verify op session active
- Check template file exists
- Validate op:// reference syntax
- Confirm output path doesn't overwrite important files

After injection:
- Verify all secrets injected (no op:// refs remaining)
- Check file permissions (should be readable only by owner)
- Remind about .gitignore

### Security Guarantees

✓ **NEVER overwrites existing .env files**
✓ **Output only to explicitly specified paths**
✓ **Validates op session before injection**
✓ **Fails gracefully if secrets missing**

---

## Workflow 4: Run Commands with Secrets

**Purpose:** Execute commands with secrets using `op run --no-masking`.

### When to Use

- Starting services that need secrets
- Running systemd services
- Executing Docker Compose
- Running deployment scripts
- Any command that needs environment variables from 1Password

### How It Works

1. User provides command to execute
2. Skill wraps with `op run --no-masking -- <command>`
3. 1Password CLI injects environment variables from template
4. Command executes with secrets available
5. Exit code and output preserved

### Usage Pattern

```
User: "Start Caddy with 1Password secrets"

Assistant Process:
1. Validate op session
2. Check service file or template exists
3. Execute: op run --no-masking -- systemctl start caddy-terraphim
4. Show command output
5. Preserve exit code

Example Output:
✓ 1Password session active
✓ Environment template found
▶ Running: op run --no-masking -- systemctl start caddy-terraphim

[Command output...]

✓ Command succeeded (exit code: 0)
```

### Common Use Cases

**Use Case 1: Systemd Service**
```bash
op run --no-masking -- systemctl start myservice
op run --no-masking -- systemctl restart myservice
op run --no-masking -- systemctl reload myservice
```

**Use Case 2: Docker Compose**
```bash
op run --no-masking -- docker-compose up -d
op run --no-masking -- docker-compose restart api
```

**Use Case 3: Shell Script**
```bash
op run --no-masking -- ./deploy.sh
op run --no-masking -- ./run-tests.sh
```

**Use Case 4: Direct Binary**
```bash
op run --no-masking -- /usr/bin/myapp --config config.yaml
op run --no-masking -- python app.py
```

### Advantages over op inject

1. **No temporary files**: Secrets stay in memory only
2. **Automatic cleanup**: Secrets removed when process exits
3. **Simpler workflow**: One command instead of inject + run
4. **Better security**: No secret files on disk
5. **Works with systemd**: Can be used in ExecStart

### Environment Variable Loading

`op run` loads variables from:
1. `.env` file in current directory (if exists)
2. Files specified with `--env-file` flag
3. `op://` references are resolved automatically

### Security Guarantees

✓ **Secrets never written to disk**
✓ **Secrets cleared from memory after process exits**
✓ **Original commands run with same permissions**
✓ **Exit codes preserved for error handling**

---

## Workflow 5: Audit Codebase

**Purpose:** Scan entire codebase for plaintext secrets and generate compliance report.

### When to Use

- Before major releases
- During security audits
- When onboarding new team members
- After acquiring new codebases
- Regular security compliance checks

### How It Works

1. User specifies directory to audit
2. Skill finds all relevant files (using priority patterns)
3. Skill scans each file with secret detection
4. Skill generates comprehensive report (markdown or JSON)
5. Skill provides remediation guidance

### Usage Pattern

```
User: "Audit /home/alex/caddy_terraphim for secrets"

Assistant Process:
1. Find files to scan:
   - High priority: *.env, config.json, secrets.*, credentials.*
   - Medium priority: docker-compose.yml, *.service, *.conf
   - Low priority: *.js, *.py, *.sh (source code)
2. Scan each file (Workflow 1)
3. Generate report with:
   - Executive summary
   - Findings by file
   - Findings by type
   - Remediation steps
4. Export as markdown or JSON

Example Output:
═══════════════════════════════════════════════════════════
SECRET AUDIT REPORT
═══════════════════════════════════════════════════════════
Directory: /home/alex/caddy_terraphim
Scanned: 45 files
Duration: 2.3 seconds

EXECUTIVE SUMMARY
─────────────────────────────────────────────────────────
Critical Issues: 3
High Priority: 5
Medium Priority: 2
Total Secrets Found: 10

FINDINGS BY SEVERITY
─────────────────────────────────────────────────────────
CRITICAL (requires immediate action):
  ✗ caddy_complete.env:2
    Type: github_oauth_secret
    Context: GITHUB_CLIENT_SECRET=***...cf4
    Risk: OAuth credentials in plaintext
    Fix: Use Workflow 2 to convert to 1Password template

  ✗ caddy_complete.env:3
    Type: jwt_secret
    Context: JWT_SHARED_KEY=***...abd
    Risk: JWT signing key exposed
    Fix: Migrate to op://Terraphim/JWT-Config/shared_key

  ✗ github_runner.env:1
    Type: token
    Context: CI_TOKEN=***...xyz
    Risk: CI/CD token in plaintext
    Fix: Convert to 1Password reference

HIGH (should fix soon):
  ... (5 more findings)

FINDINGS BY FILE
─────────────────────────────────────────────────────────
caddy_complete.env: 3 secrets (CRITICAL)
github_runner.env: 1 secret (CRITICAL)
conf/Caddyfile_auth: 2 secrets (HIGH - bcrypt hashes, acceptable)
...

REMEDIATION PLAN
─────────────────────────────────────────────────────────
1. Immediate Actions (Critical):
   - Convert caddy_complete.env to template:
     Generate template: [see Workflow 2]
   - Create 1Password items for 3 secrets
   - Update systemd service to use op run

2. Short-term Actions (High):
   - Audit bcrypt hashes in Caddyfile_auth
   - Consider rotating exposed secrets
   - Add .env files to .gitignore

3. Long-term Actions:
   - Implement regular audits (monthly)
   - Train team on 1Password usage
   - Add pre-commit hooks for secret detection

FILES TO MIGRATE:
  1. caddy_complete.env → caddy_complete.env.template
  2. github_runner.env → github_runner.env.template

COMPLIANCE STATUS
─────────────────────────────────────────────────────────
✗ NOT COMPLIANT: 3 critical issues found
  Requirement: Zero plaintext secrets in production configs
  Current: 10 secrets found across 4 files
  Target: 0 secrets (all using 1Password)

═══════════════════════════════════════════════════════════
Report generated: 2025-12-29 14:30:00 UTC
Next audit due: 2026-01-29
═══════════════════════════════════════════════════════════
```

### Report Formats

**Markdown (default):**
- Human-readable format
- Includes severity highlighting
- Provides remediation steps
- Can be committed to repo (no secret values)

**JSON (for automation):**
```json
{
  "audit_date": "2025-12-29T14:30:00Z",
  "directory": "/home/alex/caddy_terraphim",
  "files_scanned": 45,
  "duration_seconds": 2.3,
  "summary": {
    "critical": 3,
    "high": 5,
    "medium": 2,
    "total": 10
  },
  "findings": [
    {
      "file": "caddy_complete.env",
      "line": 2,
      "type": "github_oauth_secret",
      "confidence": "high",
      "severity": "critical",
      "context": "GITHUB_CLIENT_SECRET=***...cf4",
      "remediation": "Convert to op://Terraphim/GitHub-OAuth/client_secret"
    }
  ],
  "compliance": {
    "status": "non_compliant",
    "target": 0,
    "current": 10
  }
}
```

### Audit Frequency Recommendations

- **Critical systems**: Weekly
- **Production environments**: Bi-weekly
- **Development**: Monthly
- **New projects**: Before first deployment
- **After incidents**: Immediately

### Security Guarantees

✓ **Read-only operations (no file modifications)**
✓ **Secret values never displayed in reports**
✓ **Reports are safe to commit to version control**
✓ **Findings include remediation guidance**

---

## Workflow 6: Systemd Integration

**Purpose:** Integrate 1Password with systemd services for secure secret management.

### When to Use

- Running production services
- Configuring auto-start services
- Managing long-running daemons
- Setting up system services with secrets

### Two Integration Patterns

#### Pattern A: EnvironmentFile with op inject (Not Recommended)

```systemd
[Unit]
Description=My Service with 1Password
After=network.target

[Service]
Type=simple
ExecStartPre=/bin/sh -c 'op inject -i /path/to/service.env.template -o /tmp/service.env'
EnvironmentFile=/tmp/service.env
ExecStart=/usr/bin/myservice
ExecStopPost=/bin/rm -f /tmp/service.env

[Install]
WantedBy=multi-user.target
```

**Pros:**
- Service file is straightforward
- Works with any service

**Cons:**
- Creates temporary file with secrets
- Requires cleanup in ExecStopPost
- Race condition possible
- More complex

#### Pattern B: op run wrapper (Recommended)

```systemd
[Unit]
Description=My Service with 1Password
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/op run --no-masking -- /usr/bin/myservice
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Pros:**
- Simpler service file
- No temporary files
- No cleanup needed
- More secure
- Recommended by 1Password

**Cons:**
- Requires op CLI available to systemd
- Need to ensure op session stays valid

### Real-World Example: Caddy with 1Password

**Current (bigbox, insecure):**
```systemd
[Service]
WorkingDirectory=/home/alex/caddy_terraphim
EnvironmentFile=/home/alex/caddy_terraphim/caddy_complete.env
ExecStart=/home/alex/caddy_terraphim/caddy run --config /home/alex/caddy_terraphim/conf/Caddyfile_auth
```

**After Migration (secure):**
```systemd
[Service]
WorkingDirectory=/home/alex/caddy_terraphim
ExecStart=/usr/bin/op run --no-masking -- /home/alex/caddy_terraphim/caddy run --config /home/alex/caddy_terraphim/conf/Caddyfile_auth
```

**Steps:**
1. Convert `caddy_complete.env` to `caddy_complete.env.template` (Workflow 2)
2. Create 1Password items for secrets
3. Update systemd service file (remove EnvironmentFile, add op run)
4. Reload systemd: `systemctl daemon-reload`
5. Restart service: `systemctl restart caddy-terraphim`
6. Verify: `systemctl status caddy-terraphim`

### op Session Management for Systemd

**Problem:** Systemd services run as different users, may not have op session.

**Solution 1: Service Account**
```bash
# Create service account token (lasts 30 days)
op signin --raw > /etc/1password/service-token

# Use in service
[Service]
Environment="OP_SERVICE_ACCOUNT_TOKEN=/etc/1password/service-token"
ExecStart=/usr/bin/op run --no-masking -- /usr/bin/myservice
```

**Solution 2: Connect Server (Best for Production)**
Set up 1Password Connect server for machine-to-machine authentication.

### Testing Systemd Integration

```bash
# 1. Test op run manually first
op run --no-masking -- /usr/bin/myservice --test

# 2. Test service file syntax
systemd-analyze verify myservice.service

# 3. Start service
systemctl start myservice

# 4. Check status
systemctl status myservice

# 5. View logs
journalctl -u myservice -f
```

### Security Guarantees

✓ **Secrets never stored in plain text service files**
✓ **No temporary secret files on disk (Pattern B)**
✓ **Standard systemd security features work (ProtectSystem, PrivateTmp)**
✓ **Automatic secret cleanup on service stop**

---

## Common Patterns

### Pattern 1: Docker Compose with Secrets

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  app:
    image: myapp:latest
    env_file:
      - app.env.template
```

**Deployment:**
```bash
# Method 1: Inject to temp file
op inject -i app.env.template -o /tmp/app.env
docker-compose --env-file /tmp/app.env up -d
rm /tmp/app.env

# Method 2: Use op run (simpler)
op run --no-masking -- docker-compose up -d
```

### Pattern 2: Shell Scripts with Secrets

**deploy.sh.template:**
```bash
#!/bin/bash
API_KEY="op://Production/API-Keys/deploy_key"
DB_PASSWORD="op://Production/Database/password"

# Script logic here
curl -H "Authorization: Bearer $API_KEY" ...
```

**Execution:**
```bash
op run --no-masking -- bash deploy.sh.template
```

### Pattern 3: CI/CD Integration

**GitHub Actions:**
```yaml
- name: Deploy with 1Password
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
  run: |
    op run --no-masking -- ./deploy.sh
```

### Pattern 4: Development vs Production

**Structure:**
```
.env.template              # Template with op:// refs (commit this)
.env.dev.template          # Dev-specific overrides (commit this)
.env.prod.template         # Prod-specific overrides (commit this)
.env.local                 # Generated locally (never commit)
```

**Usage:**
```bash
# Development
op inject -i .env.dev.template -o .env.local

# Production
op run --no-masking -- ./start-production.sh
```

---

## Troubleshooting

### Issue 1: op CLI Not Found

**Symptoms:**
```
bash: op: command not found
```

**Solution:**
```bash
# macOS
brew install 1password-cli

# Linux
curl -sSfO https://downloads.1password.com/linux/tar/stable/x86_64/1password-cli-latest.tar.gz
tar -xf 1password-cli-latest.tar.gz
sudo mv op /usr/local/bin/

# Verify
which op && op --version
```

### Issue 2: Not Signed In

**Symptoms:**
```
[ERROR] 2025/12/29 14:30:00 You are not currently signed in. Please run `op signin`
```

**Solution:**
```bash
op signin
# Follow prompts to sign in
op whoami  # Verify
```

### Issue 3: Session Expired

**Symptoms:**
```
[ERROR] 2025/12/29 14:30:00 Invalid session token
```

**Solution:**
```bash
op signin --force
# Or use biometric unlock if configured
```

### Issue 4: Secret Not Found

**Symptoms:**
```
[ERROR] 2025/12/29 14:30:00 item "GitHub-OAuth" not found in vault "Terraphim"
```

**Solution:**
```bash
# List vaults
op vault list

# List items in vault
op item list --vault="Terraphim"

# Create missing item
op item create --category=Login \
  --title="GitHub-OAuth" \
  --vault="Terraphim" \
  client_secret=<value>
```

### Issue 5: Invalid op:// Reference Syntax

**Symptoms:**
```
[ERROR] Unable to resolve op://Vault/Item/Field
```

**Solution:**
Check reference format:
```bash
# Correct formats:
op://VaultName/ItemName/FieldName
op://VaultName/ItemName/section/FieldName

# Common mistakes:
op://Vault Name/Item Name/field   # Spaces not escaped
op:\\VaultName\ItemName\Field      # Wrong slashes
op://vaultname/itemname/Field      # Case sensitivity issues
```

### Issue 6: Systemd Service Can't Access op

**Symptoms:**
```
systemctl status myservice
# Shows: op: command not found
```

**Solution:**
```systemd
[Service]
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/op run --no-masking -- /usr/bin/myservice
```

### Issue 7: Permissions Error

**Symptoms:**
```
Permission denied: /tmp/secrets.env
```

**Solution:**
```bash
# Check file permissions
ls -la /tmp/secrets.env

# Fix permissions
chmod 600 /tmp/secrets.env

# Or inject to user-writable location
op inject -i template -o ~/.config/app/secrets.env
```

---

## Security Best Practices

### 1. Never Commit Secrets

**Always:**
- Use `.env.template` files with `op://` references
- Commit templates to version control
- Add generated files to `.gitignore`

**Never:**
- Commit `.env` files with secrets
- Commit injected environment files
- Push plaintext secrets to Git

### 2. Use .gitignore Properly

**Add to .gitignore:**
```gitignore
# Environment files with secrets
.env
.env.local
.env.*.local
*.env

# But allow templates
!.env.template
!.env.*.template

# 1Password service tokens
service-token
*.service-token
```

### 3. Regular Audits

Run audits regularly:
```bash
# Weekly for critical systems
0 0 * * 0 cd /path/to/project && op run --no-masking -- ./audit-secrets.sh

# Monthly for development
0 0 1 * * cd /path/to/project && op run --no-masking -- ./audit-secrets.sh
```

### 4. Principle of Least Privilege

**1Password Vaults:**
- Separate vaults for different environments (dev, staging, prod)
- Grant access only to necessary team members
- Use service accounts for automation

**File Permissions:**
```bash
# Injected files should be readable only by owner
chmod 600 .env.local

# Templates can be readable by group
chmod 640 .env.template
```

### 5. Secret Rotation

**When to Rotate:**
- After security incidents
- When team members leave
- Quarterly for high-security systems
- Annually for standard systems

**How to Rotate:**
1. Generate new secret value
2. Update in 1Password
3. No code changes needed (op:// ref stays same)
4. Restart services to pick up new value

### 6. Monitoring and Alerting

**Set up alerts for:**
- Failed op signin attempts
- Expired service account tokens
- Secrets accessed from unusual locations
- Audit failures

### 7. Documentation

**Document for your team:**
- Which vault contains which secrets
- Naming conventions for items/fields
- How to request access to secrets
- Emergency access procedures
- Rotation schedule

### 8. Backup and Recovery

**1Password handles backups, but you should:**
- Keep secure backup of service account tokens
- Document vault structure
- Have recovery process for lost access
- Test recovery procedures quarterly

### 9. Development Workflow

**Recommended workflow:**
```bash
# 1. Clone repo
git clone repo

# 2. Get secrets template
git pull  # Gets .env.template

# 3. Request access to 1Password vault
# (Team admin grants access)

# 4. Inject secrets for local development
op inject -i .env.template -o .env.local

# 5. Add .env.local to .gitignore (if not already)
echo ".env.local" >> .gitignore

# 6. Start development
op run --no-masking -- npm start
```

### 10. Production Deployment

**Recommended workflow:**
```bash
# Never inject secrets on production servers
# Instead, use op run for all service starts

# 1. Deploy code
git pull

# 2. Update service to use op run
systemctl edit myservice
# Add: ExecStart=/usr/bin/op run --no-masking -- /usr/bin/myservice

# 3. Reload and restart
systemctl daemon-reload
systemctl restart myservice

# 4. Verify
systemctl status myservice
journalctl -u myservice -f
```

---

## Quick Reference

### Common Commands

```bash
# Detection
op whoami && cat file.env  # Manual scan

# Template Generation
# (Use Workflow 2 guidance)

# Injection
op inject -i template -o output

# Command Execution
op run --no-masking -- command

# Audit
# (Use Workflow 5 guidance)

# Systemd
systemctl edit myservice  # Add op run to ExecStart
systemctl daemon-reload
systemctl restart myservice
```

### Confidence Levels

- **HIGH**: Definitely a secret (AWS keys, GitHub tokens, private keys)
- **MEDIUM**: Likely a secret (generic tokens, hashes)
- **LOW**: Possibly a secret (short strings, ambiguous patterns)

### Exit Codes

- **0**: Success
- **1**: General error
- **2**: Invalid arguments
- **3**: 1Password session error
- **4**: Secret not found
- **5**: Validation failed

---

## Related Skills

- **Caddy Management Skill**: Uses this skill for secret management
- **Docker Skills**: Integration with container secrets
- **CI/CD Skills**: Integration with deployment pipelines

---

**Version History:**
- 1.0.0 (2025-12-29): Initial release with 6 core workflows

**Maintainer:** Claude Code
**License:** MIT
**Documentation:** This file