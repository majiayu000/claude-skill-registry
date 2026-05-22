---
name: fresh-install-testing
description: 'Test Orient from a clean clone to validate the full development setup and test suite'
---

# Fresh Install Testing

Test Orient from a clean clone to validate the full development setup and test suite.

## Triggers

- "fresh install test"
- "test from clean clone"
- "validate clean setup"
- "run full test suite on fresh clone"

## Clone Location

```bash
cd /Users/tombensim/code/tombensim
git clone https://github.com/orient-bot/orient.git orient-fresh-test
cd orient-fresh-test
```

**Note**: The remote URL is `https://github.com/orient-bot/orient.git` (not the personal fork).

## Phase 1: Environment Setup

### Pre-flight Checks

```bash
# Verify LFS binaries are fetched (not pointers)
git lfs pull

# Verify bundled binary checksums match
./installer/install-local.sh --check
```

### Run Doctor

```bash
./run.sh doctor --fix
```

This will:

- Validate Node.js >= 20.0.0, pnpm >= 9.0.0, Docker
- Create `.env` from `.env.example` if missing
- Create `.mcp.config.local.json` from template
- Run `pnpm install` automatically

### Copy Credentials from Main Repo

```bash
cp /Users/tombensim/code/tombensim/orient/.env /Users/tombensim/code/tombensim/orient-fresh-test/.env
```

This copies Slack credentials and other secrets needed for live testing.

### Build Packages

```bash
pnpm build:packages
```

Builds all 16 workspace packages. Required before running tests.

## Phase 2: Dev Mode Startup

### Start Dev-Local Mode (SQLite, no Docker)

```bash
./run.sh dev-local
```

This starts the development environment using SQLite (no PostgreSQL required).

### Stop Dev Mode

```bash
./run.sh stop
```

## Phase 3: Run Test Suite

### Test Categories

| Category    | Command                                        | Expected Tests |
| ----------- | ---------------------------------------------- | -------------- |
| Unit        | `pnpm test:unit`                               | ~243           |
| Integration | `INTEGRATION_TESTS=true pnpm test:integration` | ~43            |
| Contract    | `pnpm vitest run tests/contracts/`             | ~20            |
| Config      | `pnpm vitest run tests/config/`                | ~22            |
| Services    | `pnpm vitest run tests/services/`              | ~22            |
| E2E         | `E2E_TESTS=true pnpm test:e2e`                 | ~50            |
| Eval        | `pnpm test:eval`                               | ~53            |
| Docker      | `pnpm test:docker:build` (optional, slow)      | ~10            |

### Interpreting Results

**Timeouts vs Failures**:

- Timeout errors (120s, 90s) are usually due to OpenCode server response times under load, not functional failures
- These are acceptable in fresh install testing
- True failures will show assertion errors with specific file/line references

**Expected Skips**:

- Some tests are skipped by default (e.g., Slack live tests without tokens)
- Eval tests: 15 passing, ~38 failing is expected (ongoing refinement)

## Phase 4: Slack Bot Live Testing

### Export Credentials for Test Runner

The test runner doesn't automatically read `.env`. Export credentials explicitly:

```bash
cd /Users/tombensim/code/tombensim/orient-fresh-test
export SLACK_BOT_TOKEN=$(grep SLACK_BOT_TOKEN .env | cut -d= -f2)
export SLACK_USER_TOKEN=$(grep SLACK_USER_TOKEN .env | cut -d= -f2)
E2E_TESTS=true RUN_SLACK_LIVE_TESTS=true \
  SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" \
  SLACK_USER_TOKEN="$SLACK_USER_TOKEN" \
  pnpm vitest run tests/e2e/slack-live.e2e.test.ts
```

**Note**: `source .env` often fails due to comments or special characters in .env files.

## Phase 5: WhatsApp Bot Testing

### Start Dev Mode with WhatsApp

```bash
./run.sh dev-local
```

### Scan QR Code

1. Open http://localhost:4098/qr/
2. Open WhatsApp on phone > Settings > Linked Devices > Link a Device
3. Scan the QR code

### Verify Connection

```bash
curl -s http://localhost:4098/qr/status | jq .
# Should show: {"qrGenerated":true,"connected":true,"state":"open"}
```

### Troubleshooting WhatsApp Session Conflicts

**Symptom**: Phone shows "logging in" but never completes, or immediately logs out.

**Cause**: Session conflict with another instance using the same WhatsApp account.

**Solution**:

1. Check logs for "loggedOut" reason:
   ```bash
   grep -E "(loggedOut|logged out)" .dev-data/instance-0/logs/*.log
   ```
2. If logged out, a new QR code is automatically generated
3. Wait for "QR Code received" message in logs
4. Scan the fresh QR code

**Log Locations**:

- Main log: `.dev-data/instance-0/logs/dashboard.log`
- WhatsApp debug: `.dev-data/instance-0/logs/whatsapp-*.log`

## Phase 6: Health Verification

### API Health

```bash
curl -s http://localhost:4098/health | jq .
# Should return: {"status":"ok","timestamp":"..."}
```

### Dashboard Accessibility

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:4098/
# Should return: 200
```

### WhatsApp QR Status

```bash
curl -s http://localhost:4098/qr/status | jq .
# Should return: {"qrGenerated":true,"connected":true,"state":"open"}
```

### Database Verification

```bash
sqlite3 .dev-data/instance-0/orient.db "SELECT COUNT(*) FROM agents;"
# Should return: 5 (or more)
```

## Phase 7: Mac Installer Testing

### Method 1: Local bundled binary

```bash
./installer/install-local.sh --check   # Verify versions/checksums
./installer/install-local.sh           # Install to ~/.orient/bin/
```

### Method 2: Full installer script

```bash
# Clean slate
rm -rf ~/.orient

# Run installer
bash installer/install.sh

# Verify
orient doctor
orient start
curl -s http://localhost:4098/health | jq .
orient stop
```

### Method 3: Docker simulation (cleanest environment)

```bash
pnpm test:installer:docker
```

### CLI Command Verification

After installer:

```bash
orient --help      # Shows help
orient doctor      # All checks pass
orient start       # Starts services
orient status      # Shows "online" status
orient logs        # Shows logs
orient stop        # Stops services
orient config      # Opens config in editor
orient version     # Shows 0.2.0
```

## Cleanup

```bash
cd /Users/tombensim/code/tombensim/orient-fresh-test
./run.sh stop
cd ..
rm -rf orient-fresh-test
```

## Quick Reference: Full Test Run

```bash
# Clone and setup
cd /Users/tombensim/code/tombensim
rm -rf orient-fresh-test
git clone https://github.com/orient-bot/orient.git orient-fresh-test
cd orient-fresh-test
git lfs pull
./run.sh doctor --fix
cp ../orient/.env .env
pnpm build:packages

# Start dev-local mode
./run.sh dev-local

# Run all tests
pnpm test:unit
INTEGRATION_TESTS=true pnpm test:integration
pnpm vitest run tests/contracts/
pnpm vitest run tests/config/
pnpm vitest run tests/services/
E2E_TESTS=true pnpm test:e2e
pnpm test:eval

# Verify health
curl -s http://localhost:4098/health | jq .

# Cleanup
./run.sh stop
```

## Expected Results (v0.2.0 baseline)

| Category    | Tests Passed | Notes                          |
| ----------- | ------------ | ------------------------------ |
| Unit        | ~243         |                                |
| Integration | ~43          |                                |
| Contract    | ~20          |                                |
| Config      | ~22          |                                |
| Services    | ~22          |                                |
| E2E         | ~50          | Timeout failures acceptable    |
| Eval        | ~15          | 38 known failures (acceptable) |
| Slack Live  | ~9           | Requires credential export     |
| **Total**   | **~380+**    |                                |
