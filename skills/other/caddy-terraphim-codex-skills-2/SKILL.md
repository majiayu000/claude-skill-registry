---
name: caddy
description: |
  Comprehensive Caddy web server management across multiple environments.
  Handles multi-server operations, zero-downtime deployments, secret management
  with 1Password, custom builds with plugins, and systemd service management.
license: Apache-2.0
---

# Caddy Server Management Skill

**Version:** 1.0.0
**Author:** Claude Code
**Purpose:** Comprehensive Caddy web server management across multiple environments

## Overview and Purpose

This skill provides enterprise-grade Caddy server management across local development and production environments. It handles:

- **Multi-server operations**: Manage Caddy on local (macOS), bigbox (production), and registry (production) servers
- **Zero-downtime deployments**: Graceful reloads with automatic validation
- **Secret management**: Integrated 1Password support for secure credential handling
- **Custom builds**: Build Caddy with required plugins (security, cloudflare, cgi, tlsredis)
- **Systemd management**: Proper service lifecycle management
- **Log analysis**: Parse and analyze JSON logs for troubleshooting
- **Pattern library**: Ready-to-use configurations for common use cases

**Critical Mandates:**
- **Zero-Downtime**: Always use graceful reloads, never kill processes
- **Validation-First**: Mandatory syntax validation before any deployment
- **Secret Safety**: Never display plaintext secrets, always use 1Password
- **Backup-First**: Always create timestamped backups before modifications

## Prerequisites

### Required

1. **Server Access**
   - Local: macOS with mdfind available
   - bigbox: SSH access configured (`ssh bigbox`)
   - registry: SSH access configured (`ssh registry`)

2. **Caddy Installation**
   ```bash
   # Check Caddy on servers
   ssh bigbox "which caddy && caddy version"
   ssh registry "which caddy && caddy version"
   ```

3. **1Password CLI** (for secret management)
   ```bash
   # Verify 1Password skill is available
   which op && op --version
   # See: ~/.claude/skills/1password-secrets.md
   ```

4. **Systemd** (on production servers)
   ```bash
   # Verify systemd available
   ssh bigbox "systemctl --version"
   ssh registry "systemctl --version"
   ```

### Optional

- **xcaddy**: For building custom Caddy binaries
- **jq**: For JSON log parsing (usually available)
- **Go toolchain**: Required for xcaddy builds

## Server Configuration

This skill operates across 3 servers with different characteristics:

### Local (Development)
- **Platform**: macOS
- **Search**: mdfind (fast Spotlight search)
- **Caddy**: Not running (development configs only)
- **Use Cases**: Testing configs, pattern development

### bigbox (Production - Migration Required)
- **Platform**: Linux
- **Caddy Version**: v2.6.4 (custom build)
- **Binary**: `/home/alex/caddy_terraphim/caddy`
- **Active Config**: `/home/alex/caddy_terraphim/conf/Caddyfile_auth`
- **Status**: Currently running in tmux (needs systemd migration)
- **Plugins**: caddy-security, caddy-tlsredis, cloudflare, cgi
- **⚠️ Action Required**: Migrate to systemd + 1Password

### registry (Production - Best Practice)
- **Platform**: Linux
- **Caddy Version**: v2.10.2 (standard)
- **Binary**: `/usr/bin/caddy`
- **Active Config**: `/etc/caddy/Caddyfile`
- **Status**: Properly managed via systemd
- **✓ Reference**: Clean 41-line config with snippets

Server configuration details: `~/.docs/caddy-skill/servers.json`

---

## Workflow 1: Discover Caddyfiles

**Purpose:** Find all Caddyfiles across servers quickly (<5 seconds).

### When to Use

- Auditing Caddyfile locations
- Before making configuration changes
- Identifying active vs backup configs
- Searching for specific configuration patterns

### How It Works

1. User specifies server(s): `local`, `bigbox`, `registry`, or `all`
2. Skill loads server configuration from servers.json
3. Skill executes fast search command (mdfind locally, find remotely)
4. Skill filters out backup files (*.backup.*, *.bak)
5. Skill identifies active configuration (from systemd service)
6. Skill displays sorted results (active first, then by modification time)

### Usage Patterns

**Pattern 1: Find on Single Server**
```
User: "Find all Caddyfiles on bigbox"

Assistant Process:
1. Load bigbox config from servers.json
2. Execute via SSH: find /home/alex/caddy_terraphim /home/alex/infrastructure -name 'Caddyfile*' ! -name '*.backup.*' -type f
3. Identify active config from systemd service
4. Sort results (active first)
5. Display with metadata

Example Output:
Found 14 Caddyfiles on bigbox:

ACTIVE:
  ✓ /home/alex/caddy_terraphim/conf/Caddyfile_auth (324 lines, modified 2 days ago)
    Service: caddy-terraphim (currently tmux-based)
    Status: Running (PID 24566, 35+ days uptime)

INACTIVE:
  /home/alex/infrastructure/atomic-server-turso/Caddyfile.enhanced (112 lines)
  /home/alex/infrastructure/atomic-server-turso/Caddyfile.production (86 lines)
  /home/alex/caddy_terraphim/conf/Caddyfile_auth2 (63 lines)
  ... (10 more files)

💡 Tip: Use 'Validate' workflow to check syntax before deployment
```

**Pattern 2: Find on All Servers**
```
User: "Find all Caddyfiles across all servers"

Assistant Process:
1. Load all server configs
2. Execute searches in parallel (local + SSH to bigbox + SSH to registry)
3. Aggregate results by server
4. Mark active configs
5. Display grouped by server

Example Output:
Found 28 Caddyfiles across 3 servers:

LOCAL (14 files):
  /Users/alex/projects/zestic-ai/charm/charm-impact/infrastructure/Caddyfile.production (167 lines)
  /Users/alex/projects/zestic-ai/charm/charm-impact/infrastructure/Caddyfile_docker (31 lines)
  ... (12 more)

BIGBOX (14 files):
  ✓ ACTIVE: /home/alex/caddy_terraphim/conf/Caddyfile_auth (324 lines)
  /home/alex/infrastructure/atomic-server-turso/Caddyfile.enhanced (112 lines)
  ... (12 more)

REGISTRY (1 file):
  ✓ ACTIVE: /etc/caddy/Caddyfile (41 lines)

⚠️  bigbox: Migration to systemd + 1Password recommended
✓  registry: Properly configured (reference implementation)
```

**Pattern 3: Search with Pattern**
```
User: "Find Caddyfiles with 'auth' in the name on bigbox"

Assistant Process:
1. Load bigbox config
2. Add pattern filter: -name '*auth*'
3. Execute search
4. Display results

Example Output:
Found 3 Caddyfiles matching 'auth' on bigbox:
  ✓ /home/alex/caddy_terraphim/conf/Caddyfile_auth (ACTIVE, 324 lines)
  /home/alex/caddy_terraphim/conf/Caddyfile_auth2 (63 lines)
  /home/alex/caddy_terraphim/conf/Caddyfile_localauth (123 lines)
```

### Implementation Details

**Step 1: Load Server Configuration**
```bash
# Read servers.json
cat ~/.docs/caddy-skill/servers.json | jq -r '.servers.bigbox'
```

**Step 2: Execute Search**

For local (macOS):
```bash
mdfind -name Caddyfile | grep -v ".backup\." | head -20
```

For remote servers (Linux):
```bash
ssh bigbox "find /home/alex/caddy_terraphim /home/alex/infrastructure \
  -name 'Caddyfile*' ! -name '*.backup.*' ! -name '*~' -type f"
```

**Step 3: Identify Active Configuration**
```bash
# Check systemd service for active config
ssh bigbox "systemctl show caddy-terraphim --property=ExecStart"
# Parse output to extract config path
```

**Step 4: Get File Metadata**
```bash
# For each file, get line count and modification time
ssh bigbox "wc -l /path/to/Caddyfile; stat -c %y /path/to/Caddyfile"
```

**Step 5: Sort and Display**
- Active configs first
- Then by modification time (newest first)
- Show metadata: lines, modification date, status

### Performance Optimization

- **Local search**: mdfind is instant (Spotlight index)
- **Remote search**: find with path limits (<5 seconds)
- **Parallel execution**: Search all servers concurrently
- **Caching**: Results cached for 60 seconds (optional)

### Error Handling

**SSH Connection Failed:**
```
✗ Error: Cannot connect to bigbox
  Check: ssh bigbox "echo test"
  Solution: Verify SSH config and connectivity
```

**No Caddyfiles Found:**
```
ℹ No Caddyfiles found on local
  Searched paths: /Users/alex/projects/
  Tip: Caddyfiles may be in different locations
```

**Permission Denied:**
```
✗ Error: Permission denied accessing /etc/caddy/Caddyfile
  Solution: Add sudo to remote command or adjust permissions
```

### Security Guarantees

✓ **Read-only operations** (no file modifications)
✓ **SSH uses existing configuration** (no password prompts)
✓ **No secrets displayed** (even if found in configs)
✓ **Respects file permissions** (won't force access)

---

## Workflow 2: Validate Configuration

**Purpose:** Validate Caddyfile syntax before deployment to prevent downtime.

### When to Use

- Before deploying configuration changes
- After editing Caddyfiles
- When troubleshooting syntax errors
- As part of CI/CD pipeline

### How It Works

1. User provides Caddyfile path and server
2. Skill reads server configuration
3. Skill executes `caddy validate --config <path>`
4. Skill parses validation output for errors
5. Skill checks for environment variables (coordinates with 1Password skill if needed)
6. Skill reports results with clear error messages

### Usage Patterns

**Pattern 1: Validate Single File**
```
User: "Validate /home/alex/caddy_terraphim/conf/Caddyfile_auth on bigbox"

Assistant Process:
1. Load bigbox server config
2. Check Caddy binary exists
3. Execute: ssh bigbox "/home/alex/caddy_terraphim/caddy validate --config /home/alex/caddy_terraphim/conf/Caddyfile_auth"
4. Parse output
5. Check for undefined environment variables
6. Report results

Example Output (Valid):
✓ Configuration is valid
  File: /home/alex/caddy_terraphim/conf/Caddyfile_auth
  Lines: 324
  Binary: /home/alex/caddy_terraphim/caddy (v2.6.4)
  Validation time: 0.8s

Environment variables detected:
  ⚠️  GITHUB_CLIENT_ID (defined in caddy_complete.env)
  ⚠️  GITHUB_CLIENT_SECRET (plaintext in caddy_complete.env)
  ⚠️  JWT_SHARED_KEY (plaintext in caddy_complete.env)

Recommendation: Migrate secrets to 1Password
  See: Workflow "Migrate Secrets" or 1Password skill
```

**Pattern 2: Validate with Errors**
```
Example Output (Invalid):
✗ Configuration has errors

Error 1 (Line 45):
  /home/alex/caddy_terraphim/conf/Caddyfile_auth:45
  parsing Caddyfile tokens: missing closing brace

  Context:
  43: reverse_proxy localhost:3000 {
  44:     header_up X-Real-IP {remote_host}
  45:     # Missing closing brace here
  46:
  47: handle /api {

Fix: Add closing brace after line 44

Error 2 (Line 102):
  Unrecognized directive: 'auth_portal'
  Did you mean: 'authentication portal' ?

Recommendation: Fix these 2 errors before deployment
```

**Pattern 3: Validate Before Deployment**
```
User: "Validate the active Caddyfile on bigbox before I deploy changes"

Assistant Process:
1. Identify active config (Workflow 1)
2. Validate current active config
3. If user modified a file, validate that too
4. Compare and report

Example Output:
✓ Current active config is valid
  File: /home/alex/caddy_terraphim/conf/Caddyfile_auth
  Status: Currently running, no errors in logs

✓ Modified config is valid
  File: /home/alex/caddy_terraphim/conf/Caddyfile_auth
  Changes: 15 lines modified (comparing to last backup)

Validation Summary:
  - Syntax: ✓ Valid
  - Directives: ✓ All recognized
  - Env vars: ⚠️  3 plaintext secrets detected
  - Conflicts: ✓ No port conflicts

Ready for deployment: Yes
Recommendation: Deploy with 'Workflow 4: Deploy Changes'
```

### Implementation Details

**Step 1: Check Caddy Binary**
```bash
# Verify Caddy is available
ssh bigbox "which /home/alex/caddy_terraphim/caddy && /home/alex/caddy_terraphim/caddy version"
```

**Step 2: Execute Validation**
```bash
# Validate Caddyfile
ssh bigbox "/home/alex/caddy_terraphim/caddy validate --config /path/to/Caddyfile --adapter caddyfile"
```

**Step 3: Parse Output**
```bash
# Validation successful if exit code 0
# Parse stderr for error messages
# Extract line numbers and error types
```

**Step 4: Check Environment Variables**
```bash
# Scan Caddyfile for {env.VAR_NAME} or {$VAR_NAME} syntax
grep -oP '\{(env\.)?\$?[A-Z_]+\}' Caddyfile

# Check if variables defined in env file or 1Password template
cat caddy_complete.env | grep "VAR_NAME="
```

**Step 5: Detect Secrets**
```bash
# Coordinate with 1Password skill to detect plaintext secrets
# See: ~/.claude/skills/1password-secrets.md Workflow 1
```

### Validation Checks

**Syntax Validation:**
- Valid Caddyfile format
- Matching braces and brackets
- Recognized directives
- Valid matcher syntax
- Proper nesting

**Semantic Validation:**
- No duplicate site blocks
- No conflicting matchers
- Valid port bindings (not in use)
- Valid upstream addresses
- Proper TLS configuration

**Environment Validation:**
- All referenced variables defined
- No plaintext secrets (warn if found)
- Env file readable if specified

**Security Validation:**
- Secrets in 1Password (recommended)
- No exposed credentials
- Proper TLS configuration
- Security headers present (recommended)

### Error Messages

**Syntax Errors:**
```
Line 45: Missing closing brace
  Expected '}' to close block started at line 43

  43: reverse_proxy localhost:3000 {
  44:     header_up X-Real-IP {remote_host}
  45:     # Missing '}'
```

**Directive Errors:**
```
Line 102: Unrecognized directive 'auth_portal'
  Available in module: http.handlers.authentication
  Suggestion: authentication portal myportal
  Documentation: https://caddyserver.com/docs/...
```

**Environment Errors:**
```
Line 15: Undefined environment variable 'API_KEY'
  Referenced as: {env.API_KEY}
  Solution 1: Define in caddy_complete.env
  Solution 2: Migrate to 1Password: op://Vault/Item/api_key
```

### Safety Guarantees

✓ **Read-only validation** (no file changes)
✓ **No service disruption** (validation only)
✓ **No secret exposure** (secrets masked in output)
✓ **Detailed error reporting** (line numbers, context)

---

## Workflow 3: Format Caddyfile

**Purpose:** Format Caddyfile for consistent style and readability.

### When to Use

- After manual edits
- Before committing to version control
- When adopting team style standards
- After merging configuration changes

### How It Works

1. User provides Caddyfile path and server
2. Skill creates timestamped backup
3. Skill executes `caddy fmt --overwrite <path>`
4. Skill validates formatted output
5. Skill shows diff (before/after) if requested
6. Skill provides rollback instructions

### Usage Pattern

```
User: "Format /home/alex/caddy_terraphim/conf/Caddyfile_auth on bigbox"

Assistant Process:
1. Load bigbox config
2. Create backup: Caddyfile_auth.backup.20251229_143000
3. Execute: caddy fmt --overwrite Caddyfile_auth
4. Validate formatted file
5. Show summary

Example Output:
✓ Caddyfile formatted successfully
  File: /home/alex/caddy_terraphim/conf/Caddyfile_auth
  Backup: /home/alex/caddy_terraphim/conf/Caddyfile_auth.backup.20251229_143000
  Changes: Indentation normalized, spacing adjusted

Validation: ✓ Formatted file is valid

To rollback:
  ssh bigbox "cp /home/alex/caddy_terraphim/conf/Caddyfile_auth.backup.20251229_143000 \
              /home/alex/caddy_terraphim/conf/Caddyfile_auth"

Recommendation: Review changes before deployment
```

### Implementation Details

**Step 1: Create Backup**
```bash
# Timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp Caddyfile_auth Caddyfile_auth.backup.$TIMESTAMP
```

**Step 2: Format**
```bash
# Execute format with overwrite
caddy fmt --overwrite /path/to/Caddyfile
```

**Step 3: Validate**
```bash
# Ensure formatting didn't break syntax
caddy validate --config /path/to/Caddyfile
```

**Step 4: Show Diff (Optional)**
```bash
# Compare before/after
diff -u Caddyfile_auth.backup.$TIMESTAMP Caddyfile_auth
```

### Safety Guarantees

✓ **Always creates backup** before formatting
✓ **Validates after formatting** to ensure no breakage
✓ **Provides rollback instructions** immediately
✓ **Never formats active config** without confirmation

---

## Workflow 4: Deploy Changes (Graceful Reload)

**Purpose:** Deploy Caddyfile changes with zero downtime using graceful reload.

### When to Use

- After validating configuration changes
- Deploying new site configurations
- Updating TLS settings
- Modifying reverse proxy rules

### How It Works

1. Pre-deployment checks (validation, service status, secret detection)
2. Create backup of current config
3. Detect deployment method (systemd reload or caddy reload API)
4. Execute graceful reload
5. Post-deployment verification (service status, logs, endpoint tests)
6. Automatic rollback on failure

### Usage Pattern

```
User: "Deploy Caddyfile changes to bigbox"

Assistant Process:
1. Pre-deployment Checks:
   ✓ Validate configuration
   ✓ Check service is running
   ⚠️  Detect 3 plaintext secrets (recommend 1Password migration)
   ✓ Create backup

2. Deployment:
   Method: systemd reload (zero-downtime)
   Command: ssh bigbox "systemctl reload caddy-terraphim"
   Status: ✓ Reload initiated

3. Verification:
   ✓ Service status: active (running)
   ✓ No errors in logs (last 50 lines)
   ✓ Test endpoint: https://alpha.truthforge.terraphim.cloud/health → 200 OK
   ✓ Requests dropped during reload: 0

Deployment Summary:
  - Status: ✓ Success
  - Duration: 2.3 seconds
  - Downtime: 0 seconds (graceful reload)
  - Backup: Caddyfile_auth.backup.20251229_143500

⚠️  Recommendation: Migrate secrets to 1Password for enhanced security
    See: 1Password skill or Workflow "Migrate Secrets"
```

### Pre-Deployment Checks

**Check 1: Validate Configuration**
```bash
# Must pass validation
caddy validate --config /path/to/Caddyfile
```

**Check 2: Service Running**
```bash
# Verify Caddy is running
systemctl is-active caddy-terraphim
# Or check process for tmux-based
ps aux | grep caddy | grep -v grep
```

**Check 3: Detect Secrets**
```bash
# Scan for plaintext secrets (coordinate with 1Password skill)
# Warn user but don't block deployment
```

**Check 4: Create Backup**
```bash
# Always backup current active config
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp /path/to/Caddyfile /path/to/Caddyfile.backup.$TIMESTAMP
```

### Deployment Methods

**Method 1: Systemd Reload (Recommended)**
```bash
# Graceful reload via systemd
systemctl reload caddy-terraphim

# Benefits:
# - Zero downtime (in-place reload)
# - No dropped connections
# - Automatic rollback on failure
# - Logs in journalctl
```

**Method 2: Caddy Reload API**
```bash
# Direct reload via Caddy admin API
curl -X POST http://localhost:2019/load \
  -H "Content-Type: application/json" \
  -d @config.json

# Benefits:
# - Finer control
# - Can preview config before apply
# - Works without systemd
```

**Method 3: Signal Reload**
```bash
# Send USR1 signal (for tmux-based or non-systemd)
kill -USR1 $(cat /var/run/caddy.pid)

# Note: Less reliable, use systemd if possible
```

### Post-Deployment Verification

**Step 1: Check Service Status**
```bash
systemctl status caddy-terraphim --no-pager
# Verify: active (running), no recent errors
```

**Step 2: Check Recent Logs**
```bash
# Last 50 log lines for errors
journalctl -u caddy-terraphim -n 50 --no-pager | grep -i error
```

**Step 3: Test Endpoints**
```bash
# Test configured domains
curl -f https://alpha.truthforge.terraphim.cloud/health
curl -f https://ci.terraphim.cloud/health

# Verify: 200 OK responses
```

**Step 4: Check Dropped Requests**
```bash
# Parse logs for any dropped connections during reload
# Caddy's graceful reload should have 0 drops
```

### Rollback on Failure

If deployment fails (validation error, service won't start, endpoints down):

```bash
# Automatic rollback process:
1. Restore backup:
   cp Caddyfile.backup.20251229_143500 Caddyfile

2. Reload with backup config:
   systemctl reload caddy-terraphim

3. Verify rollback successful:
   systemctl status caddy-terraphim
   curl -f https://domain.com/health

4. Report failure details to user with logs
```

### Safety Guarantees

✓ **Zero-downtime reloads** (graceful, no dropped requests)
✓ **Always validates** before deployment
✓ **Always creates backup** before changes
✓ **Automatic rollback** on failure
✓ **Post-deployment verification** confirms success

---

## Workflow 5: Check Status

**Purpose:** Check Caddy service health and current configuration.

### Usage Pattern

```
User: "Check Caddy status on bigbox"

Assistant Process:
1. Query systemd service status
2. Check process details (PID, uptime, memory)
3. Verify listening ports
4. Check recent log entries
5. Test configured endpoints

Example Output:
Caddy Status on bigbox:

Service: caddy-terraphim
  Status: ✓ active (running)
  PID: 24566
  Uptime: 35 days 14 hours
  Memory: 27.6 MB
  User: caddy

Configuration:
  Active: /home/alex/caddy_terraphim/conf/Caddyfile_auth (324 lines)
  Loaded: 3 hours ago
  Last reload: 2 hours ago (successful)

Listening Ports:
  ✓ :80 (HTTP)
  ✓ :443 (HTTPS)

Recent Activity (last 10 minutes):
  - 245 requests processed
  - 0 errors
  - Average response time: 45ms

Domains Configured:
  ✓ alpha.truthforge.terraphim.cloud (responding)
  ✓ ci.terraphim.cloud (responding)
  ✓ logs.terraphim.cloud (responding)

Health: ✓ All systems operational

⚠️  Note: Service running in tmux, migration to systemd recommended
```

### Implementation

```bash
# Service status
systemctl status caddy-terraphim

# Process details
ps aux | grep caddy | grep -v grep

# Listening ports
ss -tulpn | grep caddy

# Recent logs
journalctl -u caddy-terraphim --since "10 minutes ago"

# Test endpoints
curl -sf https://domain.com/health
```

---

## Integration with 1Password Skill

This skill coordinates with the 1Password Secret Management Skill for secure credential handling.

### Secret Detection

When scanning Caddyfiles, this skill detects:
- Environment variable references: `{env.VAR_NAME}`
- Plaintext secrets in env files
- Basic auth credentials
- API keys and tokens

Then coordinates with 1Password skill (Workflow 1: Detect Secrets) to:
- Identify secret types
- Calculate confidence scores
- Recommend migration to op:// references

### Secret Migration

For bigbox migration, this skill will:
1. Detect plaintext secrets in `caddy_complete.env`
2. Use 1Password skill (Workflow 2: Generate Template) to create `.env.template`
3. Guide user to create 1Password items
4. Update systemd service to use `op run --no-masking`
5. Verify migration successful

See: `~/.claude/skills/1password-secrets.md` for detailed secret management workflows.

---

## Quick Reference

### Common Commands

```bash
# Discovery
"Find all Caddyfiles on bigbox"
"Find Caddyfiles with 'auth' in name on all servers"

# Validation
"Validate /path/to/Caddyfile on bigbox"
"Validate the active Caddyfile before deployment"

# Format
"Format /path/to/Caddyfile on registry"

# Deploy
"Deploy Caddyfile changes to bigbox"

# Status
"Check Caddy status on registry"
```

### Server Names

- `local`: Local development machine (macOS)
- `bigbox`: Production server (migration needed)
- `registry`: Production server (reference implementation)
- `all`: All servers

### File Locations

- **Local**: `/Users/alex/projects/*/infrastructure/Caddyfile*`
- **bigbox**: `/home/alex/caddy_terraphim/conf/Caddyfile_auth` (active)
- **registry**: `/etc/caddy/Caddyfile` (active)

---

## Related Skills

- **1Password Secret Management**: `~/.claude/skills/1password-secrets.md`
- **Systemd Management**: For service lifecycle operations
- **SSH Management**: For remote server access

---

**Version History:**
- 1.0.0 (2025-12-29): Initial release with core workflows (Discovery, Validation, Format, Deploy, Status)

**Maintainer:** Claude Code
**License:** MIT
**Documentation:** This file
**Server Configuration:** `~/.docs/caddy-skill/servers.json`
**Pattern Library:** `~/.docs/caddy-skill/patterns/` (coming soon)

---

**Next Workflows Coming Soon:**
- Workflow 6: Build Custom Caddy (xcaddy with plugins)
- Workflow 7: Analyze Logs (JSON parsing, error detection)
- Workflow 8: Extract Snippets (DRY principle, pattern identification)
- Workflow 9: Migrate to Systemd (bigbox migration with 1Password)
- Workflow 10: Pattern Library (reverse proxy, auth, WebSocket, security headers)
