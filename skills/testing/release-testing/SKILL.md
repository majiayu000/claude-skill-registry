---
name: release-testing
description: Comprehensive guide for testing Orient releases. Use this skill when asked to "test the release", "verify installation", "run release tests", "check v0.x.x", "validate installer", or when preparing a new version for release. Covers unit tests, installer E2E tests, CLI verification, integration tests, eval tests, and success criteria validation.
---

# Orient Release Testing

Test releases systematically before shipping.

## Quick Test (5 min)

```bash
pnpm test:unit                    # Should pass 240+ tests
orient doctor && orient status    # If installed
curl -s http://localhost:4098/health
```

## Full Release Testing Sequence

### Phase 1: Unit Tests

```bash
pnpm test:unit
```

**Expected**: ~244 passed, ~33 skipped
**Acceptable**: Docker tests may fail if Docker isn't running (environment issue, not code bug)

### Phase 2: Local Installer E2E

```bash
./installer/install-local.sh
```

This will:

1. Check prerequisites (Node 20+, pnpm, PM2)
2. Clean and rebuild all packages
3. Copy to `~/.orient/`
4. Initialize SQLite database
5. Start services via PM2
6. Open dashboard

### Phase 3: Verify Installation

```bash
# Load into current shell
export ORIENT_HOME="$HOME/.orient"
export PATH="$ORIENT_HOME/bin:$PATH"

# Run all checks
orient doctor        # All services should show online
orient status        # PM2 status table
orient version       # Should show correct version
orient logs --lines 5 --nostream  # Should show recent logs

# HTTP checks
curl -s http://localhost:4098/health | jq .  # {"status":"ok"}
curl -s -o /dev/null -w "%{http_code}" http://localhost:4098/     # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:4098/qr/  # 200

# Database verification
ls -la ~/.orient/data/sqlite/
sqlite3 ~/.orient/data/sqlite/orient.db ".tables"  # Should list 30+ tables
```

### Phase 4: Integration Tests

```bash
./run.sh dev start
sleep 60  # Wait for services
INTEGRATION_TESTS=true pnpm test:integration
./run.sh dev stop
```

**Expected**: ~43 tests passing

### Phase 5: Eval Tests

```bash
# Without API key (graceful skip)
pnpm test:eval  # Should pass with skip message

# With dev server running (full eval infrastructure test)
./run.sh dev start
ANTHROPIC_API_KEY=xxx pnpm test:eval
./run.sh dev stop
```

**Requirements**:

1. `ANTHROPIC_API_KEY` environment variable
2. Dev server running (`./run.sh dev start`) for OpenCode at localhost:4099

**Known Limitation**: The eval/OpenCode agent routing integration needs work. The eval infrastructure (loading, filtering, running) works correctly, but actual agent invocations through OpenCode may fail with session errors. Test will pass while logging a warning about this.

## Success Criteria

| Check             | Pass              | Fail                             |
| ----------------- | ----------------- | -------------------------------- |
| Unit tests        | 230+ passed       | <200 passed or critical failures |
| Integration tests | 40+ passed        | <35 passed                       |
| Services start    | PM2 shows online  | errored/stopped status           |
| Health endpoint   | `{"status":"ok"}` | Connection refused or error      |
| Dashboard HTTP    | 200               | 4xx/5xx                          |
| QR endpoint HTTP  | 200               | 4xx/5xx                          |
| Database          | 30+ tables        | Missing tables or errors         |
| `orient doctor`   | All green         | Red status                       |
| CLI commands      | All work          | Any command fails                |

## Cleanup

```bash
# Stop services
orient stop

# Full uninstall
orient uninstall --force

# Or manual cleanup
pm2 delete orient
rm -rf ~/.orient
```

## Troubleshooting

**Port 4098 in use**: `lsof -i :4098` then `kill <PID>`

**PM2 not starting**: Check logs with `pm2 logs orient --lines 50`

**Database errors**: Delete and reinitialize:

```bash
rm ~/.orient/data/sqlite/orient.db*
cd ~/.orient/orient && pnpm --filter @orientbot/database run db:push:sqlite
```

**Build failures**: Clean rebuild:

```bash
find packages -name "dist" -type d -maxdepth 2 -exec rm -rf {} +
rm -rf .turbo node_modules/.cache
pnpm install && pnpm run build:all
```
