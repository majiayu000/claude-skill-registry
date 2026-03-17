---
name: database-backup
description: "Backup database before tests, migrations, or other database operations"
---

# Database Backup

## Core Principle

Create a backup before running any operation that could modify or destroy database data.

## When to Use

Before running:
- Tests (`npm test`, `pytest`, `php artisan test`)
- Migrations (`php artisan migrate`, `prisma migrate`)
- Seeders (`php artisan db:seed`)
- Any destructive queries

## Quick Start

```bash
# Create backup
./scripts/backup-database.sh

# Run tests with automatic backup
./scripts/safe-test.sh npm test

# Run migrations with automatic backup
./scripts/safe-migrate.sh php artisan migrate

# Restore if needed
./scripts/restore-database.sh --latest
```

## Why This Matters

Real incidents that informed this practice:
- Tests running against production database wiped 6 months of data
- `migrate:fresh` in wrong terminal reset staging database

A backup takes seconds. Recovery without one can take hours or be impossible.

## Protocol

### Step 1: Check Your Database Connection

```bash
# Verify which database you're connected to
cat .env | grep DB_
```

If you see production credentials, stop and switch to a test database.

### Step 2: Create Backup

```bash
./scripts/backup-database.sh
```

Or use the safe wrappers which backup automatically:
```bash
./scripts/safe-test.sh [your test command]
./scripts/safe-migrate.sh [your migration command]
```

### Step 3: Run Your Operation

After backup is confirmed, proceed with your operation.

### Step 4: Verify

If something went wrong:
```bash
./scripts/restore-database.sh --latest
```

## Safety Scripts

| Script | Purpose |
|--------|---------|
| `backup-database.sh` | Create timestamped backup |
| `restore-database.sh` | Restore from backup |
| `safe-test.sh` | Backup + run tests |
| `safe-migrate.sh` | Backup + run migrations |

See `scripts/README.md` for detailed usage.

## Checklist

Before database operations:
- [ ] Verified database connection (not production)
- [ ] Created backup or using safe wrapper
- [ ] Know how to restore if needed

## Tips

- Use `.env.testing` for test database configuration
- Keep backups for at least a few days
- Test your restore process occasionally
- For production, use your hosting provider's backup features
