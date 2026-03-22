---
name: dotenvx
version: "1.0.0"
description: dotenvx - secure environment variable management with encryption. Use for encrypting .env files, multi-environment configuration, cross-platform secret management, and migrating from plaintext dotenv.
---

# dotenvx Skill

dotenvx is a **secure dotenv** from the creator of the original dotenv package. It adds encryption, multi-environment support, and cross-platform compatibility to environment variable management. Think of it as "dotenv with encryption" - your secrets are encrypted at rest and can be safely committed to version control.

**Core Value Proposition**: Encrypt your .env files so they can be safely committed to git, while keeping decryption keys separate and secure.

## When to Use This Skill

This skill should be triggered when:
- Setting up secure environment variable management
- Encrypting .env files for version control
- Managing secrets across multiple environments (dev, staging, production)
- Migrating from plaintext .env to encrypted secrets
- Deploying applications with encrypted configuration
- Configuring dotenvx in CI/CD pipelines
- Troubleshooting dotenvx encryption/decryption issues

## When NOT to Use This Skill

- For basic dotenv usage without encryption (use standard dotenv docs)
- For cloud-native secrets managers (AWS Secrets Manager, HashiCorp Vault)
- For Kubernetes secrets management (use k8s secrets/sealed-secrets)

---

## Core Concepts

### The Security Problem

Traditional `.env` files are plaintext - if committed to git or exposed, all secrets are compromised. dotenvx solves this by:

1. **Encrypting** secrets with AES-256 and Secp256k1 elliptic curve cryptography
2. **Separating** the encrypted file (safe to commit) from the decryption key (kept secure)
3. **Decrypting** automatically at runtime when the private key is available

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    dotenvx WORKFLOW                          │
└─────────────────────────────────────────────────────────────┘

   .env (plaintext)              .env.keys (NEVER commit)
   ┌──────────────────┐          ┌──────────────────────────┐
   │ HELLO=World      │          │ DOTENV_PRIVATE_KEY=...   │
   │ API_KEY=secret   │          │ DOTENV_PUBLIC_KEY=...    │
   └────────┬─────────┘          └────────────┬─────────────┘
            │                                  │
            ▼  dotenvx encrypt                 │
   ┌──────────────────┐                        │
   │ HELLO="encrypted:│◄───────────────────────┘
   │   BE9Y5L..."     │     Uses public key to encrypt
   │ API_KEY="encrypt │
   │   ed:CGY8..."    │
   └────────┬─────────┘
            │
            ▼  Safe to commit to git!
   ┌──────────────────┐
   │   Git Repository │
   └────────┬─────────┘
            │
            ▼  dotenvx run (at runtime)
   ┌──────────────────┐
   │ Decrypts using   │◄── Private key from:
   │ private key      │    - .env.keys file
   │                  │    - DOTENV_PRIVATE_KEY env var
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ process.env.HELLO│
   │ = "World"        │
   └──────────────────┘
```

### Key Files

| File | Purpose | Git? |
|------|---------|------|
| `.env` | Development environment variables | ✅ Yes (when encrypted) |
| `.env.production` | Production environment variables | ✅ Yes (when encrypted) |
| `.env.keys` | Private decryption keys | ❌ Never |
| `.env.local` | Local overrides | ❌ No |

---

## Installation

### npm (Recommended for Node.js projects)

```bash
npm install @dotenvx/dotenvx --save
```

### Homebrew (macOS/Linux global install)

```bash
brew install dotenvx/brew/dotenvx
```

### Shell Script (Universal)

```bash
curl -sfS https://dotenvx.sh | sh
```

### Docker

```bash
docker run -it --rm -v $(pwd):/app dotenv/dotenvx help
```

### Windows

```powershell
winget install dotenvx
```

### npx (No install)

```bash
npx @dotenvx/dotenvx help
```

---

## CLI Commands Reference

### run - Inject Environment Variables

Run any command with environment variables injected:

```bash
# Basic usage
dotenvx run -- node index.js

# Specify environment file
dotenvx run -f .env.production -- node index.js

# Multiple files (earlier takes precedence)
dotenvx run -f .env.local -f .env -- node index.js

# Use framework conventions (Next.js, etc.)
dotenvx run --convention=nextjs -- npm run build

# Override existing environment variables
dotenvx run --overload -- node index.js
```

### encrypt - Encrypt .env Files

Convert plaintext .env to encrypted format:

```bash
# Encrypt default .env file
dotenvx encrypt

# Encrypt specific file
dotenvx encrypt -f .env.production

# Encrypt all .env* files
dotenvx encrypt -f .env*
```

**Result**: Creates/updates `.env.keys` with encryption keys.

### decrypt - Decrypt .env Files

Revert encrypted .env to plaintext:

```bash
# Decrypt default .env file
dotenvx decrypt

# Decrypt specific file
dotenvx decrypt -f .env.production
```

### set - Set Encrypted Variables

Add or update encrypted variables:

```bash
# Set a variable (encrypts automatically)
dotenvx set HELLO World

# Set in specific environment
dotenvx set HELLO production -f .env.production

# Set from stdin (for sensitive values)
echo "supersecret" | dotenvx set API_KEY
```

### get - Retrieve Variable Values

```bash
# Get single variable
dotenvx get HELLO

# Get from specific file
dotenvx get HELLO -f .env.production

# Get all variables as JSON
dotenvx get --all --format json
```

### keypair - Manage Encryption Keys

```bash
# Show public/private key pair
dotenvx keypair

# Show for specific environment
dotenvx keypair -f .env.production
```

---

## Multi-Environment Setup

### Recommended Structure

```
project/
├── .env                    # Development (encrypted)
├── .env.production         # Production (encrypted)
├── .env.staging            # Staging (encrypted)
├── .env.local              # Local overrides (not committed)
├── .env.keys               # All private keys (NEVER commit)
└── .gitignore
```

### .gitignore Configuration

```gitignore
# Never commit private keys
.env.keys

# Never commit local overrides
.env.local
.env.*.local

# DO commit encrypted .env files
# (remove these from .gitignore if present)
# .env
# .env.production
# .env.staging
```

### Environment-Specific Keys

Each environment gets its own key pair:

```bash
# .env.keys after encrypting multiple environments
DOTENV_PRIVATE_KEY="ec9d6..."           # For .env
DOTENV_PRIVATE_KEY_PRODUCTION="a]c8..."  # For .env.production
DOTENV_PRIVATE_KEY_STAGING="3d5f..."     # For .env.staging
```

### Loading Order with Conventions

```bash
# Next.js convention loads in this order:
# .env.local → .env.development → .env
dotenvx run --convention=nextjs -- npm run dev
```

---

## Integration Examples

### Node.js Application

**package.json:**
```json
{
  "scripts": {
    "dev": "dotenvx run -- node index.js",
    "start": "dotenvx run -f .env.production -- node index.js"
  }
}
```

**index.js:**
```javascript
// Option 1: Use dotenvx as drop-in replacement
require('@dotenvx/dotenvx').config()
console.log(process.env.HELLO)

// Option 2: Use dotenvx.get() for explicit access
const dotenvx = require('@dotenvx/dotenvx')
dotenvx.config()
console.log(dotenvx.get('HELLO'))
```

### Next.js

**package.json:**
```json
{
  "scripts": {
    "dev": "dotenvx run --convention=nextjs -- next dev",
    "build": "dotenvx run -f .env.production -- next build",
    "start": "dotenvx run -f .env.production -- next start"
  }
}
```

### Docker

**Dockerfile:**
```dockerfile
FROM node:20-alpine

# Install dotenvx
RUN curl -sfS https://dotenvx.sh | sh

WORKDIR /app
COPY . .
RUN npm install

# Run with dotenvx (provide DOTENV_PRIVATE_KEY at runtime)
CMD ["dotenvx", "run", "--", "node", "index.js"]
```

**docker-compose.yml:**
```yaml
services:
  app:
    build: .
    environment:
      - DOTENV_PRIVATE_KEY_PRODUCTION=${DOTENV_PRIVATE_KEY_PRODUCTION}
```

### GitHub Actions

```yaml
name: Deploy
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dotenvx
        run: curl -sfS https://dotenvx.sh | sh

      - name: Build with secrets
        env:
          DOTENV_PRIVATE_KEY_PRODUCTION: ${{ secrets.DOTENV_PRIVATE_KEY_PRODUCTION }}
        run: dotenvx run -f .env.production -- npm run build
```

### Vercel

1. Encrypt production secrets:
```bash
dotenvx set API_KEY "production-secret" -f .env.production
```

2. Add private key to Vercel:
```bash
vercel env add DOTENV_PRIVATE_KEY_PRODUCTION
# Paste the key from .env.keys
```

3. Update build command in vercel.json:
```json
{
  "buildCommand": "dotenvx run -f .env.production -- npm run build"
}
```

---

## .env File Syntax

### Basic Format

```bash
# Comments start with #
HELLO=World
DATABASE_URL=postgres://localhost/mydb

# Quoted values
MESSAGE="Hello, World!"
SINGLE_QUOTED='No $expansion here'

# Multiline with backticks
PRIVATE_KEY=`-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----`
```

### Variable Expansion

```bash
# Reference other variables
BASE_URL=https://api.example.com
API_ENDPOINT=${BASE_URL}/v1

# Default values
PORT=${PORT:-3000}

# Alternate if set
DEBUG_MODE=${DEBUG:+enabled}
```

### Command Substitution

```bash
# Embed command output
HOSTNAME=$(hostname)
USER=$(whoami)
TIMESTAMP=$(date +%s)
```

### Encrypted Values

After running `dotenvx encrypt`:

```bash
#/-------------------[DOTENV_PUBLIC_KEY]--------------------/
#/            public-key encryption for .env files          /
#/       [how it works](https://dotenvx.com/encryption)     /
#/----------------------------------------------------------/
DOTENV_PUBLIC_KEY="034a..."

# Encrypted values
HELLO="encrypted:BE9Y5L3OxAOOmfq..."
API_KEY="encrypted:CGY8BDMHfq..."
```

---

## Security Best Practices

### Key Management

1. **Never commit `.env.keys`** - Add to `.gitignore` immediately
2. **Store private keys in secrets manager** - GitHub Secrets, Vercel Env, AWS SSM
3. **Rotate keys periodically** - Re-encrypt with new keys
4. **Use environment-specific keys** - Different keys for dev/staging/production

### CI/CD Security

```bash
# Set private key as environment variable
export DOTENV_PRIVATE_KEY_PRODUCTION="your-private-key"

# dotenvx automatically uses it for decryption
dotenvx run -f .env.production -- npm run build
```

### Team Workflow

```bash
# Developer 1: Encrypts new secret
dotenvx set NEW_API_KEY "secret123"
git add .env
git commit -m "Add NEW_API_KEY (encrypted)"
git push

# Developer 2: Pulls and runs (has .env.keys locally)
git pull
dotenvx run -- npm run dev  # Works automatically
```

### Sharing Keys Securely

```bash
# Option 1: Secure channel (1Password, Signal, etc.)
cat .env.keys | pbcopy  # Copy to clipboard

# Option 2: In-person/video call

# Option 3: Company secrets manager
# Store DOTENV_PRIVATE_KEY in vault
```

---

## Troubleshooting

### "Missing private key"

```
Error: Missing private key for .env.production
```

**Solution**: Set the private key:
```bash
# Option 1: Create/restore .env.keys file
echo 'DOTENV_PRIVATE_KEY_PRODUCTION="abc123..."' > .env.keys

# Option 2: Set environment variable
export DOTENV_PRIVATE_KEY_PRODUCTION="abc123..."
```

### "Cannot decrypt"

**Cause**: Wrong private key or corrupted encrypted value

**Solution**:
```bash
# Verify key matches
dotenvx keypair -f .env.production

# Re-encrypt if needed
dotenvx decrypt -f .env.production  # If you have the right key
dotenvx encrypt -f .env.production
```

### Variables Not Loading

```bash
# Debug: Show what dotenvx is loading
dotenvx run --debug -- node -e "console.log(process.env)"

# Check file is being read
dotenvx run -f .env.production --verbose -- echo "loaded"
```

### Encrypted Values in Wrong File

```bash
# Check which file has encrypted values
grep "encrypted:" .env*

# Ensure matching .env.keys entries
cat .env.keys
```

---

## Migration from dotenv

### Step 1: Install dotenvx

```bash
npm install @dotenvx/dotenvx --save
npm uninstall dotenv
```

### Step 2: Update Code

```javascript
// Before
require('dotenv').config()

// After (drop-in replacement)
require('@dotenvx/dotenvx').config()
```

### Step 3: Encrypt Existing .env

```bash
# Encrypt current .env file
dotenvx encrypt

# Verify encryption worked
cat .env  # Should show encrypted: values

# Save .env.keys somewhere secure!
cat .env.keys
```

### Step 4: Update Scripts

```json
{
  "scripts": {
    "dev": "dotenvx run -- node index.js",
    "start": "dotenvx run -f .env.production -- node index.js"
  }
}
```

---

## Resources

### Official Documentation
- [dotenvx Docs](https://dotenvx.com/docs/)
- [GitHub Repository](https://github.com/dotenvx/dotenvx)
- [Encryption Details](https://dotenvx.com/encryption)

### Integrations
- [Vercel Guide](https://dotenvx.com/docs/platforms/vercel)
- [Heroku Guide](https://dotenvx.com/docs/platforms/heroku)
- [Docker Guide](https://dotenvx.com/docs/platforms/docker)
- [GitHub Actions](https://dotenvx.com/docs/cis/github-actions)

### Language Support
- Node.js, Python, Ruby, Go, PHP, Rust, Java
- Frameworks: Next.js, Express, Flask, Rails, Laravel

---

## Version History

- **1.0.0** (2026-01-11): Initial skill release
  - Complete dotenvx overview and installation
  - CLI commands reference (run, encrypt, decrypt, set, get, keypair)
  - Multi-environment configuration
  - Integration examples (Node.js, Next.js, Docker, CI/CD)
  - .env file syntax reference
  - Security best practices
  - Migration guide from dotenv
