---
name: stress-tester
version: "1.0"
description: Comprehensive stress testing skill for FlowState. Runs reliability, backup, container, security, and performance tests. Use before releases, after major refactoring, or when reliability is questioned.
triggers:
  - "stress test"
  - "run stress tests"
  - "test reliability"
  - "security audit"
  - "container health"
  - "backup verification"
  - "performance test"
  - "before release"
  - "system health check"
---

# Stress Testing Skill

**TASK-338** | **Priority: P0 Critical**

Rigorously test FlowState to find issues that other testing and agents missed. Covers reliability, backup systems, container stability, security, and data integrity.

---

## Quick Start

```bash
# Run all stress tests
npm run test:stress

# Quick smoke test (5 min)
npm run test:stress -- --grep "@quick"

# Full test suite
npm run test:stress -- --timeout=120000

# By category
npm run test:stress -- --grep "Security"
npm run test:stress -- --grep "Data Integrity"
npm run test:stress -- --grep "Restore"
```

---

## Pre-Flight Checks

Before running stress tests, verify prerequisites:

```bash
# 1. Dev server running
curl -s http://localhost:5546 > /dev/null && echo "OK: Dev server" || echo "FAIL: Run npm run dev"

# 2. Docker containers healthy
docker ps --filter "name=supabase" --format "{{.Names}}: {{.Status}}" 2>/dev/null | head -3

# 3. Recent backup exists
ls -la public/shadow-latest.json 2>/dev/null || echo "WARN: No shadow backup"
```

---

## Test Categories

### 1. Data Integrity Tests (`data-integrity.spec.ts`)

| Test | Description | Command |
|------|-------------|---------|
| Rapid Task Creation | Create 20 tasks rapidly, verify no duplicates | `--grep "Rapid Creation"` |
| Canvas Position | Drag, refresh, verify position persists | `--grep "Position Persistence"` |
| Concurrent Edits | Edit same task in 2 tabs simultaneously | `--grep "Concurrent Edit"` |
| Network Instability | Create tasks offline, verify sync on reconnect | `--grep "Network Instability"` |

### 2. Security Tests (`security.spec.ts`)

| Test | Description | Command |
|------|-------------|---------|
| XSS Script Tag | Inject `<script>` in task title | `--grep "Script Tag"` |
| XSS Event Handler | Inject `onerror`, `onclick` handlers | `--grep "Event Handler"` |
| XSS Rich Text | Test TipTap editor for XSS | `--grep "Rich Text Editor"` |
| Input Length | 100KB input stress test | `--grep "Input Length"` |
| SQL Injection | Test search with SQL payloads | `--grep "SQL Injection"` |

### 3. Restore Verification Tests (`restore-verification.spec.ts`)

| Test | Description | Command |
|------|-------------|---------|
| Backup Accessible | Verify backup system is reachable | `--grep "accessible"` |
| Golden Backup | Verify golden backup has valid structure | `--grep "Golden backup"` |
| Checksum Valid | Verify backup checksum integrity | `--grep "Checksum"` |
| Full Restore Cycle | Create -> backup -> delete -> restore -> verify | `--grep "Full restore"` |
| Shadow Backup | Verify shadow-latest.json is valid | `--grep "Shadow backup"` |

### 4. Container Stability Tests (`container-stability.spec.ts`)

| Test | Description | Command |
|------|-------------|---------|
| Docker Health | Verify Supabase containers healthy | `--grep "Docker"` |
| DB Restart | Kill DB container, verify app recovers | `--grep "DB Restart"` |
| Full Stack Restart | Restart entire stack, verify no data loss | `--grep "Full Stack"` |
| App Reconnection | Verify app auto-reconnects after container restart | `--grep "Reconnection"` |

### 5. Performance Benchmarks (`store-operations.bench.ts`)

| Benchmark | Target | Command |
|-----------|--------|---------|
| Create 100 tasks | < 100ms | `npm run test:bench` |
| Filter 10k tasks | < 50ms | |
| Sort 1k tasks | < 20ms | |
| Find by ID (10k) | < 5ms | |
| JSON serialize 1k | < 50ms | |
| Canvas viewport filter | < 10ms | |

---

## Test Matrix: Completed TASKs Coverage

This matrix maps completed tasks to their stress test coverage:

| TASK | Description | Test Coverage |
|------|-------------|---------------|
| TASK-131 | Position reset during session | `data-integrity.spec.ts: Position Persistence` |
| TASK-142 | Position reset on refresh | `data-integrity.spec.ts: Position Persistence` |
| TASK-255 | Canvas geometry invariants | `geometry-invariants.test.ts` |
| TASK-256 | Canvas geometry tests | `geometry-invariants.test.ts` |
| TASK-309-B | Undo/redo system | `qa-testing: Memory Leak Check` |
| TASK-334 | Completion protocol | Enforced via hooks |
| TASK-335 | Canvas distribution | `data-integrity.spec.ts` |
| TASK-365 | Restore verification | `restore-verification.spec.ts` |

---

## Running the Full Suite

```bash
# 1. Ensure dev server is running
npm run dev &

# 2. Run all stress tests
npm run test:stress

# 3. Run benchmarks
npm run test:bench

# 4. Generate report
npm run test:stress:report
```

---

## Report Generation

After running tests, a report is generated at `reports/stress-test-report/index.html`.

**Report contents:**
- Test pass/fail counts by category
- Timing metrics
- Screenshots of failures
- Console error captures
- Recommendations

---

## Integration with QA Testing

This skill extends `qa-testing` with:
- **Deeper coverage**: Multi-tab scenarios, network partitions
- **Container testing**: Docker/Supabase health checks
- **Security focus**: XSS, SQL injection, input fuzzing
- **Performance baselines**: Benchmarks with thresholds

**Chaining:**
```
stress-tester (finds issues) -> dev-debugging (fixes) -> qa-testing (verifies fix)
```

---

## Failure Response Protocol

### Critical Failure (Tier 1)
- Data loss, security vulnerability, container crash
- **Action**: STOP release, fix immediately

### High Failure (Tier 2)
- Performance regression, UI glitches under stress
- **Action**: Schedule fix within sprint

### Medium Failure (Tier 3)
- Edge case failures, minor memory growth
- **Action**: Add to backlog

---

## Manual Testing Checklist

For issues that can't be automated:

### Container Resilience
- [ ] `docker kill supabase_db_flow-state` -> app shows error, auto-reconnects when container restarts
- [ ] `npx supabase stop && npx supabase start` -> no data loss

### Multi-Device Sync
- [ ] Open app in Chrome and Firefox simultaneously
- [ ] Create task in Chrome -> appears in Firefox within 5s
- [ ] Edit same task in both -> last-write-wins, no duplicates

### Long Session Stability
- [ ] Leave app running 4 hours with periodic activity
- [ ] Memory growth < 100MB
- [ ] No console errors accumulating

---

## Files

```
tests/stress/
├── playwright.stress.config.ts    # Playwright config for stress tests
├── data-integrity.spec.ts         # CRUD, position, concurrent edits
├── security.spec.ts               # XSS, SQL injection, input fuzzing
├── restore-verification.spec.ts   # Backup/restore cycle tests
├── container-stability.spec.ts    # Docker/Supabase health tests
└── store-operations.bench.ts      # Performance benchmarks

scripts/
├── run-stress-tests.sh            # Full test runner
└── generate-stress-report.cjs     # Report generator
```

---

## Version History

- v1.0 (Jan 2026): Initial release with full test suite
