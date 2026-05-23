---
name: personal-crypto-secrets-management
description: 'Diagnose and resolve AES-256-GCM crypto key mismatches in the Orient secrets service'
---

# Crypto Secrets Management

Guide for diagnosing and resolving crypto key mismatches in the Orient secrets service.

## Overview

The Orient uses AES-256-GCM encryption to store secrets in PostgreSQL. The encryption key is derived from `ORIENT_MASTER_KEY` using scrypt with a fixed salt.

**Key files:**

- `packages/core/src/crypto.ts` - Encryption/decryption functions
- `packages/database-services/src/secretsService.ts` - Database operations for secrets
- `scripts/load-secrets.ts` - Load secrets as shell exports
- `scripts/migrate-secrets-to-db.ts` - Migrate .env secrets to database

## Common Error

```
Error: Unsupported state or unable to authenticate data
    at Decipheriv.final (node:internal/crypto/cipher:184:29)
    at decryptSecret (packages/core/src/crypto.ts:47:25)
```

This error means the current `ORIENT_MASTER_KEY` does not match the key used to encrypt the secrets in the database.

## Diagnosing the Problem

### 1. Check if secrets exist in database

```bash
psql $DATABASE_URL -c "SELECT key, category, updated_at FROM secrets ORDER BY key;"
```

### 2. Verify ORIENT_MASTER_KEY is set

```bash
# Check if key is set (don't print the value!)
[ -n "$ORIENT_MASTER_KEY" ] && echo "Key is set (${#ORIENT_MASTER_KEY} chars)" || echo "Key is NOT set"
```

### 3. Test decryption

```bash
# This will show which secrets fail to decrypt
npx tsx scripts/load-secrets.ts 2>&1
```

### 4. Check development vs production key

In development, if `ORIENT_MASTER_KEY` is not set, the code uses a default dev key:

```typescript
const DEV_MASTER_KEY = 'orient-dev-master-key-do-not-use-in-production-32chars';
```

If secrets were encrypted with the dev key but `ORIENT_MASTER_KEY` is now set (or vice versa), decryption will fail.

## Resolution Options

### Option 1: Use the correct key

If you know which key was used to encrypt the secrets:

```bash
# Set the correct key and restart
export ORIENT_MASTER_KEY="the-original-key-that-was-used"
./run.sh dev restart
```

### Option 2: Clear and re-migrate secrets (development only)

If you don't need the existing secrets or this is a fresh dev setup:

```bash
# 1. Clear existing secrets
psql $DATABASE_URL -c "DELETE FROM secrets;"
psql $DATABASE_URL -c "DELETE FROM secrets_audit_log;"

# 2. Ensure ORIENT_MASTER_KEY matches your .env or unset for dev key
unset ORIENT_MASTER_KEY  # Use dev key
# OR
export ORIENT_MASTER_KEY="your-new-32-char-key-here"

# 3. Re-migrate secrets from .env
npx tsx scripts/migrate-secrets-to-db.ts

# 4. Restart services
./run.sh dev restart
```

### Option 3: Re-encrypt with new key (key rotation)

To re-encrypt all secrets with a new key:

```bash
# 1. Export secrets with OLD key
export ORIENT_MASTER_KEY="old-key"
npx tsx scripts/load-secrets.ts > /tmp/secrets-backup.sh

# 2. Clear database
psql $DATABASE_URL -c "DELETE FROM secrets;"

# 3. Re-import with NEW key
export ORIENT_MASTER_KEY="new-32-char-key-here-minimum"
source /tmp/secrets-backup.sh
npx tsx scripts/migrate-secrets-to-db.ts

# 4. Securely delete backup
rm /tmp/secrets-backup.sh

# 5. Update .env with new key
echo "ORIENT_MASTER_KEY=new-32-char-key-here-minimum" >> .env
```

### Option 4: Skip database secrets temporarily

For debugging, you can set secrets directly in the environment to bypass the database:

```bash
# Export required secrets directly
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
# etc.
```

## Prevention

### 1. Document your master key

Store the `ORIENT_MASTER_KEY` securely:

- Password manager
- Encrypted notes
- `.env` file (gitignored)

### 2. Use consistent keys across environments

Each environment (dev, staging, prod) should have its own consistent key:

- Development: Can use default dev key (unset `ORIENT_MASTER_KEY`)
- Production: Must set a secure `ORIENT_MASTER_KEY`

### 3. Check before migrating secrets

```bash
# Verify key before encrypting secrets
echo "Using key: ${ORIENT_MASTER_KEY:0:4}...${ORIENT_MASTER_KEY: -4} (${#ORIENT_MASTER_KEY} chars)"
```

## Database Schema

```sql
CREATE TABLE secrets (
    key TEXT PRIMARY KEY,           -- e.g., SLACK_BOT_TOKEN
    encrypted_value TEXT NOT NULL,  -- AES-256-GCM encrypted
    iv TEXT NOT NULL,               -- Initialization vector
    auth_tag TEXT NOT NULL,         -- Authentication tag
    category TEXT,                  -- Optional grouping
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE secrets_audit_log (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL,
    action TEXT NOT NULL,           -- created, updated, deleted
    changed_by TEXT,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Quick Commands

```bash
# List all secrets (keys only, not values)
psql $DATABASE_URL -c "SELECT key, category FROM secrets ORDER BY key;"

# Count secrets
psql $DATABASE_URL -c "SELECT COUNT(*) FROM secrets;"

# View audit log
psql $DATABASE_URL -c "SELECT * FROM secrets_audit_log ORDER BY changed_at DESC LIMIT 20;"

# Delete a specific secret
psql $DATABASE_URL -c "DELETE FROM secrets WHERE key = 'SECRET_NAME';"

# Clear all secrets (dangerous!)
psql $DATABASE_URL -c "DELETE FROM secrets; DELETE FROM secrets_audit_log;"
```

## Related Issues

- **Billing page 502 errors**: Often caused by crypto mismatch preventing API key loading
- **Service startup failures**: "Failed to load secrets from database" warnings
- **Integration connection failures**: OAuth tokens can't be decrypted
