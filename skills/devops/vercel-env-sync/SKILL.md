---
name: vercel-env-sync
description: Synchronize and verify environment variables between local files (.env.example, .env.local) and Vercel deployment configuration across production, preview, and development environments. Use when deploying to Vercel, managing environment variables, or ensuring deployment readiness.
---

# Vercel Environment Variables Sync

Esta skill proporciona scripts automatizados, funciones compartidas y patrones completos para gestionar variables de entorno en Vercel. Garantiza sincronización perfecta entre desarrollo local y todos los entornos de deployment.

## 🎯 When to Use This Skill

- **Pre-deployment validation**: Ensure all required env vars exist before deploying
- **Environment synchronization**: Push local .env values to Vercel or pull Vercel vars locally
- **Security audits**: Auto-detect and mark sensitive variables with `--sensitive` flag
- **Team onboarding**: Help new developers get correct environment configuration
- **CI/CD integration**: Automate env var validation in deployment pipelines
- **Multi-environment management**: Sync across production, preview, and development

## 📦 Skill Components

### Scripts (`./scripts/`)

1. **[env-push.sh](./scripts/env-push.sh)** - Push local vars to Vercel

   - Reads from `.env.local` and `.env` with fallback to `.env.example`
   - Auto-detects sensitive variables (DATABASE_URL, _\_SECRET, _\_KEY, etc.)
   - Supports `--dry-run`, `--force`, `--all-envs` flags
   - Uses modern `vercel env update` instead of deprecated `rm + add` pattern

2. **[env-pull.sh](./scripts/env-pull.sh)** - Pull Vercel vars to local file

   - Download env vars from Vercel to `.env.local` (or custom output)
   - Supports Git branch-specific variables (`--branch feature-x`)
   - Environment selection: production, preview, or development

3. **[env-audit.sh](./scripts/env-audit.sh)** - Comprehensive sync status report
   - Compare local `.env.example` with all Vercel environments
   - Table or JSON output format
   - Shows missing, extra, and synced variables per environment

### Libraries (`./lib/`)

- **[env-functions.sh](./lib/env-functions.sh)** - Shared bash functions:
  - `vercel::env::set()` - Create/update vars with auto `--sensitive` detection
  - `vercel::env::pull()` - Pull vars from Vercel
  - `vercel::env::validate_value()` - Validate var values (URLs, secrets length, etc.)
  - `vercel::env::is_sensitive()` - Detect sensitive variables
  - `vercel::env::health_check()` - Verify CLI, auth, and project config
  - Plus 15+ more helper functions

## 🚀 Quick Start

### Installation

```bash
# Navigate to workspace root
cd /path/to/project

# Make scripts executable
chmod +x .github/skills/vercel-env-sync/scripts/*.sh
chmod +x .github/skills/vercel-env-sync/lib/*.sh

# Verify Vercel CLI is installed
vercel --version

# Authenticate
vercel login

# Link project
vercel link
```

### Basic Workflow

```bash
# Shortcut: navigate to skill directory
cd .github/skills/vercel-env-sync

# 1. Health check
source lib/env-functions.sh
vercel::env::health_check

# 2. Audit current state
./scripts/env-audit.sh

# 3. Push missing variables (dry-run first)
./scripts/env-push.sh --all-envs --dry-run
./scripts/env-push.sh --all-envs

# 4. Pull variables for development
./scripts/env-pull.sh --env development

# 5. Verify sync
./scripts/env-audit.sh
```

## 📖 Core Patterns

### Pattern 1: Audit Before Deployment

**Objetivo**: Verify all required variables exist in all environments before deploying.

**Workflow**:

```bash
# Generate audit report
./scripts/env-audit.sh

# Output shows per-environment status:
# Variable                       Production   Preview      Development
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATABASE_URL                   ✓ Existe    ✓ Existe    ✓ Existe
# NEXT_PUBLIC_APP_URL            ✗ Falta     ✗ Falta     ✗ Falta
# BETTER_AUTH_SECRET             ✗ Falta     ✗ Falta     ✗ Falta
```

**Exit codes**:

- `0`: All variables synced
- `1`: Missing variables detected (blocks deployment)

### Pattern 2: Push Local Vars to Vercel (Modern Approach)

**Objetivo**: Sync `.env.local` values to Vercel using best practices.

**Script**: `env-push.sh`

**Key Improvements Over Legacy Scripts**:

- ✅ Uses `vercel env update` instead of `rm + add` (Vercel CLI v33+)
- ✅ Auto-detects sensitive variables and adds `--sensitive` flag
- ✅ Validates values before pushing (URL format, secret length, no placeholders)
- ✅ Supports dry-run mode
- ✅ Creates automatic backups before modifications

**Usage**:

```bash
# Push to production only (default)
./scripts/env-push.sh

# Push to all environments
./scripts/env-push.sh --all-envs

# Preview changes without applying
./scripts/env-push.sh --all-envs --dry-run

# Force update existing variables
./scripts/env-push.sh --all-envs --force

# Specific environment
./scripts/env-push.sh --env preview
```

**Example Output**:

```
🚀 Sincronizando variables de entorno con Vercel...

🏥 Verificación de salud...
  ✓ Vercel CLI instalado
  ✓ Autenticado como: melosdev
  ✓ Proyecto vinculado: wispy-poetry-52762475
  ✓ .env.example existe (4 variables)

🎯 Configuración:
  Entornos: production preview development
  Forzar actualización: false
  Dry run: false
  Backup automático: true

💾 Creando backups...
✓ Backup guardado en .env.backup.production.20260114_153022

📦 Procesando entorno: production
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Creando DATABASE_URL en production... [SENSITIVE]
✓ DATABASE_URL creado en production
```

### Pattern 3: Pull Variables for Development

**Objetivo**: Download Vercel env vars to local `.env.local` for development.

**Script**: `env-pull.sh`

**Usage**:

```bash
# Pull development vars to .env.local
./scripts/env-pull.sh

# Pull production vars
./scripts/env-pull.sh --env production

# Pull to custom file
./scripts/env-pull.sh --output .env.ci --env preview

# Pull preview vars for specific Git branch
./scripts/env-pull.sh --env preview --branch feature-auth

# Overwrite without confirmation
./scripts/env-pull.sh --yes
```

**Example**:

```bash
$ ./scripts/env-pull.sh --env production

⬇️  Descargando variables de entorno desde Vercel...

🎯 Configuración:
  Entorno: production
  Archivo: .env.local

✅ Variables descargadas exitosamente

📁 Archivo: .env.local
📊 Variables: 4

💡 Próximos pasos:
   1. Revisar: cat .env.local
   2. Iniciar dev: vercel env run -- pnpm dev
```

### Pattern 4: Run Commands with Vercel Env (Modern)

**Objetivo**: Execute commands with Vercel environment variables without writing .env files.

**Command**: `vercel env run` (Vercel CLI native feature)

**Usage**:

```bash
# Run dev server with Vercel env vars
vercel env run -- pnpm dev

# Run tests with preview environment
vercel env run -e preview -- pnpm test

# Build with production vars
vercel env run -e production -- pnpm build

# Execute custom script
vercel env run -- node scripts/migrate.js
```

**Why This Pattern?**:

- ✅ No .env files in repository
- ✅ Always uses latest Vercel values
- ✅ Works in CI/CD without manual pulls
- ✅ Prevents stale local env files

### Pattern 5: Validate Values Before Push

**Objetivo**: Auto-validate environment variable values to prevent invalid configurations.

**Built into**: `env-push.sh` via `lib/env-functions.sh`

**Validations Applied**:

```bash
# Minimum secret length
BETTER_AUTH_SECRET: ≥ 32 characters
NEXTAUTH_SECRET: ≥ 32 characters
*_SECRET: ≥ 32 characters

# URL format
*_URL: Must start with http:// or https://
*_ENDPOINT: Must start with http:// or https://

# PostgreSQL connection string
DATABASE_URL: Must start with postgresql://

# Placeholder detection
Rejects: "your-", "changeme", "placeholder", "example"
```

**Example**:

```bash
$ vercel::env::validate_value "BETTER_AUTH_SECRET" "short"
❌ BETTER_AUTH_SECRET debe tener al menos 32 caracteres

$ vercel::env::validate_value "API_URL" "not-a-url"
⚠️  API_URL debería ser una URL válida (http:// o https://)

$ vercel::env::validate_value "DATABASE_URL" "mysql://..."
❌ DATABASE_URL debe ser una conexión PostgreSQL válida
```

### Pattern 6: Sensitive Variables Auto-Detection

**Objetivo**: Automatically mark sensitive variables with `--sensitive` flag.

**Implementation**: Built into `vercel::env::set()` function.

**Detection Rules**:

1. **Hardcoded list** (in `lib/env-functions.sh`):

   ```bash
   SENSITIVE_VARS=(
     "DATABASE_URL"
     "BETTER_AUTH_SECRET"
     "NEON_API_KEY"
     "GITHUB_TOKEN"
     "VERCEL_TOKEN"
     "NEXTAUTH_SECRET"
     "API_KEY"
     "API_SECRET"
     "PRIVATE_KEY"
     "SECRET_KEY"
   )
   ```

2. **Pattern matching**:
   - Any variable containing: `SECRET`, `PASSWORD`, `KEY`, `TOKEN`, `PRIVATE`

**Result**:

```bash
# Automatically adds --sensitive flag
printf "%s\n" "$value" | vercel env add DATABASE_URL production --sensitive
```

### Pattern 7: Automated Backups

**Objetivo**: Create automatic backups before modifying Vercel env vars.

**Usage**:

```bash
# Manual backup
source lib/env-functions.sh
vercel::env::backup production
# Output: .env.backup.production.20260114_153022

# Automatic (built into env-push.sh)
./scripts/env-push.sh --all-envs
# Creates backups automatically before any changes
```

**Restore from Backup**:

```bash
# Manual restore
vercel env pull .env.backup.production.20260114_153022
# Review changes
cat .env.backup.production.20260114_153022
# Apply manually if needed
```

## 🔧 Advanced Patterns

### Pattern 8: CI/CD Integration

**GitHub Actions Example**:

```yaml
name: Verify Environment Variables

on:
  pull_request:
    paths:
      - ".env.example"
  workflow_dispatch:

jobs:
  env-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Audit Environment Variables
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          cd .github/skills/vercel-env-sync
          chmod +x scripts/*.sh lib/*.sh

          # Link project with token
          vercel link --yes --token $VERCEL_TOKEN

          # Run audit
          ./scripts/env-audit.sh --json > audit-result.json

          # Check exit code
          if [ $? -ne 0 ]; then
            echo "❌ Environment variables not synced"
            cat audit-result.json
            exit 1
          fi

      - name: Comment PR
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ Environment variables need sync. Run: `.github/skills/vercel-env-sync/scripts/env-push.sh --all-envs`'
            })
```

### Pattern 9: Git Branch-Specific Variables

**Objetivo**: Use different env vars for different Git branches (feature branches).

**Usage**:

```bash
# Auto-detect current branch
CURRENT_BRANCH=$(git branch --show-current)

# Pull vars for current branch
./scripts/env-pull.sh --env preview --branch "$CURRENT_BRANCH"

# Run dev with branch-specific vars
vercel env run -e preview --git-branch="$CURRENT_BRANCH" -- pnpm dev
```

**Vercel Setup**:

1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Click on variable → Edit → Git Branch → Select specific branch
3. Now that variable only applies to deployments from that branch

### Pattern 10: JSON Output for Programmatic Use

**Objetivo**: Generate machine-readable audit reports.

**Usage**:

```bash
# Generate JSON report
./scripts/env-audit.sh --json > env-status.json

# Parse with jq
jq '.local_vars[] | select(.environments.production == false)' env-status.json

# Example output:
{
  "timestamp": "2026-01-14T15:30:22+00:00",
  "project": "wispy-poetry-52762475",
  "local_vars": [
    {
      "name": "DATABASE_URL",
      "environments": {
        "production": true,
        "preview": true,
        "development": true
      }
    },
    {
      "name": "BETTER_AUTH_SECRET",
      "environments": {
        "production": false,
        "preview": false,
        "development": false
      }
    }
  ]
}
```

## 🐛 Troubleshooting

### Error: "Not authenticated"

**Cause**: Vercel CLI not logged in.

**Solution**:

```bash
vercel login

# Or use token
export VERCEL_TOKEN="your-token"
vercel whoami
```

### Error: "No project linked"

**Cause**: Local project not connected to Vercel.

**Solution**:

```bash
vercel link --yes

# Verify
cat .vercel/project.json
```

### Error: Variable Not Updating

**Cause**: Using old `rm + add` pattern fails sometimes.

**Solution**: Scripts now use `vercel env update`:

```bash
# Old (deprecated)
vercel env rm VAR production --yes
echo "value" | vercel env add VAR production

# New (recommended) - used in env-push.sh
printf "%s\n" "value" | vercel env update VAR production --yes
```

### Warning: "Validation failed"

**Cause**: Variable value doesn't meet validation rules.

**Example**:

```bash
❌ BETTER_AUTH_SECRET debe tener al menos 32 caracteres
```

**Solution**: Generate valid secret:

```bash
# Generate 32+ character secret
openssl rand -base64 32

# Update .env.local
echo "BETTER_AUTH_SECRET=$(openssl rand -base64 32)" >> .env.local

# Push again
./scripts/env-push.sh --env production
```

### Error: "Permission denied" on scripts

**Cause**: Scripts don't have execute permissions.

**Solution**:

```bash
chmod +x .github/skills/vercel-env-sync/scripts/*.sh
chmod +x .github/skills/vercel-env-sync/lib/*.sh
```

### Issue: Git Bash on Windows

**Symptoms**: Array errors, variable parsing issues.

**Cause**: Git Bash has limited bash 3.x compatibility.

**Solution**: Scripts are tested and compatible with Git Bash. If issues persist:

```bash
# Use WSL instead
wsl bash ./scripts/env-audit.sh

# Or use PowerShell equivalent (create wrapper)
```

## 📚 Best Practices

### 1. Never Commit .env Files

```gitignore
# .gitignore
.env
.env.local
.env.*.local
.env.backup.*
```

### 2. Keep .env.example Updated

```bash
# After adding new variable
echo "NEW_VAR=example-value" >> .env.example

# Commit .env.example (without real values)
git add .env.example
git commit -m "Add NEW_VAR to env config"
```

### 3. Use Secure Secrets

```bash
# Good: Random 32+ characters
openssl rand -base64 32

# Good: Random hex
openssl rand -hex 32

# Bad: Weak password
changeme123
```

### 4. Separate Environments

```bash
# Development: localhost
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Production: real domain
NEXT_PUBLIC_APP_URL=https://thesimpson.webcode.es
```

### 5. Validate Before Deploy

```bash
# Pre-deploy checklist
./scripts/env-audit.sh && vercel --prod
```

### 6. Use vercel env run for Dev

```bash
# Instead of maintaining .env.local
vercel env run -- pnpm dev

# Always uses latest Vercel values
```

### 7. Backup Before Mass Changes

```bash
# Auto-backup (default in env-push.sh)
./scripts/env-push.sh --all-envs

# Manual backup
source lib/env-functions.sh
vercel::env::backup production
vercel::env::backup preview
vercel::env::backup development
```

## 📖 Quick Reference

### Essential Commands

```bash
# Health check
source lib/env-functions.sh && vercel::env::health_check

# Audit all environments
./scripts/env-audit.sh

# Push to all environments
./scripts/env-push.sh --all-envs

# Pull for development
./scripts/env-pull.sh

# Dry-run sync
./scripts/env-push.sh --all-envs --dry-run

# Force update existing vars
./scripts/env-push.sh --all-envs --force

# JSON output
./scripts/env-audit.sh --json

# Backup specific environment
source lib/env-functions.sh && vercel::env::backup production
```

### Vercel CLI Commands (Modern)

```bash
# List variables
vercel env ls
vercel env ls production
vercel env ls preview --json

# Create variable
echo "value" | vercel env add VAR_NAME production
echo "value" | vercel env add VAR_NAME production --sensitive

# Update variable (Vercel CLI 33+)
echo "new-value" | vercel env update VAR_NAME production --yes
printf "%s\n" "new-value" | vercel env update VAR_NAME production --sensitive --yes

# Remove variable
vercel env rm VAR_NAME production --yes

# Pull to local file
vercel env pull .env.local
vercel env pull .env.local --environment=production
vercel env pull .env.local --environment=preview --git-branch=feature-x

# Run command with env vars
vercel env run -- pnpm dev
vercel env run -e production -- pnpm build
```

### Function Library

```bash
# Source functions
source .github/skills/vercel-env-sync/lib/env-functions.sh

# Verification
vercel::check_cli                    # Verify Vercel CLI installed
vercel::authenticated                # Check if logged in
vercel::project_linked               # Check if project linked
vercel::env::health_check            # Complete health check

# Environment variable operations
vercel::env::get_local_value VAR     # Read from .env.local/.env
vercel::env::get_local_vars          # List all vars in .env.example
vercel::env::exists VAR production   # Check if var exists in Vercel
vercel::env::is_sensitive VAR        # Check if var is sensitive
vercel::env::validate_value VAR val  # Validate value format
vercel::env::set VAR val production  # Create/update var
vercel::env::remove VAR production   # Delete var
vercel::env::pull .env.local dev     # Download vars
vercel::env::diff production         # Compare local vs Vercel
vercel::env::backup production       # Create backup
```

## 🔗 Related Skills

- **[vercel-cli-management](../vercel-cli-management/SKILL.md)** - General Vercel CLI usage
- **[nextjs16-proxy-middleware](../nextjs16-proxy-middleware/SKILL.md)** - Middleware using env vars
- **[neon-database-management](../neon-database-management/SKILL.md)** - DATABASE_URL management

## 📚 References

- [Vercel CLI Environment Variables](https://vercel.com/docs/cli/env)
- [Vercel Environment Variables Docs](https://vercel.com/docs/projects/environment-variables)
- [Agent Skills Standard](https://agentskills.io/)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

---

**Last Updated**: January 14, 2026  
**Version**: 2.0 (Modern Vercel CLI)  
**Compatibility**: Vercel CLI 33+, Bash 4+, Git Bash (Windows)
