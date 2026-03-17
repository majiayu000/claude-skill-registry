---
name: debug
description: Unified testing, debugging, and error-fixing skill for backend, database, and frontend. Use when investigating bugs, running tests, analyzing logs, or fixing errors. Consolidates systematic-debugging, testing-patterns, vulnerability-scanner, and webapp-testing principles.
allowed-tools:
  - run_command
  - browser_subagent
  - mcp_mcp-server-neon_run_sql
  - mcp_mcp-server-neon_list_slow_queries
  - mcp_sequential-thinking_sequentialthinking
---

# Debug Skill

> Unified debugging, testing, and error-fixing for full-stack applications.

## When to Use

| Trigger                  | Action                  |
| ------------------------ | ----------------------- |
| Bug report, error, crash | Start 4-phase debugging |
| Need tests               | Run biome + vitest      |
| Frontend broken          | Use agent-browser CLI   |
| Slow queries             | Use Neon MCP tools      |
| Deployment failed        | Check Railway logs      |

---

## Content Map

| Reference                                              | Purpose                        |
| ------------------------------------------------------ | ------------------------------ |
| [Testing Pyramid](references/testing-pyramid.md)       | Unit/Integration/E2E selection |
| [Debug Methodology](references/debug-methodology.md)   | 4-phase process, 5 Whys        |
| [Security Checklist](references/security-checklist.md) | OWASP Top 10 2025              |

---

## Decision Tree: Which Tool?

```
Problem Type?
├── Backend Error
│   ├── Type error → bun run check
│   ├── Logic error → bun test
│   └── API error → Check tRPC logs
├── Database Error
│   ├── Slow query → mcp_mcp-server-neon_list_slow_queries
│   ├── Schema issue → drizzle-kit push
│   └── Connection → Check DATABASE_URL
├── Frontend Error
│   ├── Visual bug → agent-browser snapshot/screenshot
│   ├── Interaction → agent-browser click/fill
│   └── Console error → browser_subagent
└── Deployment Error
    └── Railway → railway logs --filter="level:error"
```

---

## CLI Quick Reference

### Backend: Biome + Vitest

```bash
# Lint & type check
bun run check

# Run tests
bun test
bun test --coverage
bun test path/to/file.test.ts
```

### Frontend: agent-browser CLI

```bash
# Install (first time)
npm install -g agent-browser
agent-browser install

# Core workflow
agent-browser open http://localhost:3000   # Navigate
agent-browser snapshot                     # Get refs (a11y tree)
agent-browser click @e2                    # Click element by ref
agent-browser fill @e3 "test@example.com"  # Fill input
agent-browser get text @e1                 # Get text content
agent-browser screenshot page.png          # Capture state
agent-browser close                        # Cleanup
```

### Database: Neon MCP

```bash
# Via MCP (preferred)
mcp_mcp-server-neon_list_slow_queries  # Find slow queries
mcp_mcp-server-neon_run_sql            # Execute debug SQL
mcp_mcp-server-neon_explain_sql_statement  # Analyze query plan

# Via CLI
neonctl databases list --project-id <id>
```

### Deployment: Railway CLI

```bash
# View logs
railway logs

# Filter errors
railway logs --filter="level:error"

# Filter path + error
railway logs --filter="@path:/api level:error"

# SSH into service (interactive)
railway ssh --service <service-id>
```

---

## 4-Phase Debugging Process

### Phase 1: REPRODUCE

- [ ] Confirm minimum reproducible steps
- [ ] Document expected vs actual behavior
- [ ] Identify affected scope (file, component, route)

### Phase 2: ISOLATE

- [ ] Binary search to narrow location
- [ ] Add strategic logging
- [ ] Check recent changes (`git diff HEAD~5`)

### Phase 3: UNDERSTAND (Root Cause)

- [ ] Apply 5 Whys technique
- [ ] Trace data flow
- [ ] Check state at each step

### Phase 4: FIX & VERIFY

- [ ] Implement fix
- [ ] Run `bun run check` (no type errors)
- [ ] Run `bun test` (tests pass)
- [ ] Verify in browser (`agent-browser`)
- [ ] Document fix in commit message

---

## 5 Whys Template

```markdown
**Problem**: [Describe error]

1. Why? → [First cause]
2. Why? → [Deeper cause]
3. Why? → [Underlying issue]
4. Why? → [Systemic reason]
5. Why? → [Root cause]

**Root Cause**: [Final determination]
**Fix**: [Solution implemented]
```

---

## Testing Pyramid

```
        /\
       /E2E\       ← Few, slow, high confidence
      /------\
     / Integ. \    ← Some, medium speed
    /----------\
   /   Unit     \  ← Many, fast, isolated
  /--------------\
```

| Layer       | Tool          | When                   |
| ----------- | ------------- | ---------------------- |
| Unit        | Vitest        | Business logic, utils  |
| Integration | Vitest + tRPC | API routes, DB queries |
| E2E         | agent-browser | User flows, UI         |

---

## Security Quick Check (OWASP 2025)

| #   | Vulnerability          | Check                      |
| --- | ---------------------- | -------------------------- |
| 1   | Broken Access Control  | Verify auth on all routes  |
| 2   | Cryptographic Failures | Check secrets not exposed  |
| 3   | Injection              | Parameterized queries only |
| 4   | Insecure Design        | Review auth flow           |
| 5   | Security Misconfig     | Check CORS, headers        |

---

## Scripts

| Script                                         | Purpose               |
| ---------------------------------------------- | --------------------- |
| [`run_tests.sh`](scripts/run_tests.sh)         | Run biome + vitest    |
| [`fetch_logs.sh`](scripts/fetch_logs.sh)       | Aggregate error logs  |
| [`frontend_test.sh`](scripts/frontend_test.sh) | agent-browser testing |

---

## Anti-Patterns

❌ **Don't** skip reproduction steps
❌ **Don't** fix symptoms without root cause
❌ **Don't** ignore type errors
❌ **Don't** deploy without tests passing
❌ **Don't** use console.log in production

---

## Output Template

When debugging is complete, document:

```markdown
## Debug Report

**Issue**: [Description]
**Root Cause**: [5 Whys result]
**Fix**: [What was changed]
**Verification**:

- [ ] `bun run check` ✅
- [ ] `bun test` ✅
- [ ] Browser verified ✅
      **Files Changed**: [list]
```
