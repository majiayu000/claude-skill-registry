---
name: alerts
description: |
  System health and alerts reporting skill. This skill should be used at session
  start to surface pending alerts, or anytime the user wants to check system health.
  Triggers: "alerts", "check alerts", "what needs attention", "system health",
  "show warnings", "pending issues". Default mode (--limited) checks Code Health,
  Security, and Session Context. Use --full for comprehensive reporting including
  Documentation Health and Roadmap/Planning.
---

# Alerts

## Overview

This skill provides comprehensive system health reporting by aggregating alerts
from multiple sources. It surfaces issues that would otherwise be hidden in
collapsed hook output or scattered across multiple files.

## Usage

```
/alerts           # Limited mode (default) - quick health check
/alerts --full    # Full mode - comprehensive reporting
```

## Modes

### Limited Mode (Default)

Quick health check covering the most critical categories:

1. **Code Health** - Test failures, TypeScript errors, ESLint, pattern
   violations
2. **Security** - npm audit vulnerabilities, security patterns, secrets status
3. **Session Context** - MCP memory status, cross-session warnings, pending
   TODOs

### Full Mode (--full)

Comprehensive reporting including everything in Limited plus:

4. **Current Alerts** - Deferred PR items, Backlog S0/S1/S2, encrypted secrets
5. **Documentation Health** - Orphaned docs, stale docs, CANON violations
6. **Roadmap/Planning** - Overdue items, blocked tasks, stale SESSION_CONTEXT

## Workflow

To run alerts check:

1. Determine mode (limited or full based on user request)
2. Run the appropriate checks using the script
3. Present results in a clear, actionable format
4. Offer to help resolve any issues found

## Alert Categories

### 1. Code Health

| Check              | Command/Source                | Severity |
| ------------------ | ----------------------------- | -------- |
| Test failures      | `npm test 2>&1`               | Error    |
| TypeScript errors  | `npm run type-check 2>&1`     | Error    |
| ESLint warnings    | `npm run lint 2>&1`           | Warning  |
| Pattern violations | `npm run patterns:check 2>&1` | Warning  |
| Circular deps      | `npm run check:circular 2>&1` | Warning  |

### 2. Security

| Check                   | Command/Source                | Severity |
| ----------------------- | ----------------------------- | -------- |
| npm audit high/critical | `npm audit --json 2>&1`       | Error    |
| Security patterns       | `npm run security:check 2>&1` | Warning  |
| Encrypted secrets       | `.env.local.encrypted` exists | Warning  |
| Exposed secrets         | Search for hardcoded tokens   | Error    |

### 3. Session Context

| Check                 | Source                       | Severity |
| --------------------- | ---------------------------- | -------- |
| MCP memory status     | `mcp__memory__read_graph()`  | Info     |
| Cross-session warning | `.claude/session-state.json` | Warning  |
| Unfinished TODOs      | Previous session state       | Info     |

### 4. Current Alerts (Full Mode)

| Check             | Source                            | Severity |
| ----------------- | --------------------------------- | -------- |
| Deferred PR items | `docs/AI_REVIEW_LEARNINGS_LOG.md` | Warning  |
| Backlog S0 items  | `docs/AUDIT_FINDINGS_BACKLOG.md`  | Error    |
| Backlog S1 items  | `docs/AUDIT_FINDINGS_BACKLOG.md`  | Warning  |
| Backlog S2 items  | `docs/AUDIT_FINDINGS_BACKLOG.md`  | Info     |

### 5. Documentation Health (Full Mode)

| Check                 | Command/Source                | Severity |
| --------------------- | ----------------------------- | -------- |
| Orphaned docs         | `npm run docs:orphans 2>&1`   | Info     |
| Stale docs (>30 days) | File modification dates       | Warning  |
| CANON violations      | `npm run validate:canon 2>&1` | Warning  |
| Cross-doc violations  | `npm run crossdoc:check 2>&1` | Warning  |

### 6. Roadmap/Planning (Full Mode)

| Check                 | Source                       | Severity |
| --------------------- | ---------------------------- | -------- |
| Overdue roadmap items | `ROADMAP.md` dates           | Warning  |
| Blocked tasks         | `ROADMAP.md` blocked markers | Warning  |
| Stale SESSION_CONTEXT | File modification date       | Info     |

## Output Format

Present alerts grouped by severity:

```
## System Health Report

### Errors (must fix)
- [Code] 3 TypeScript errors in src/components/...
- [Security] 2 high vulnerabilities found

### Warnings (should address)
- [Code] 5 ESLint warnings
- [Alerts] 4 deferred PR items (2 aging)

### Info (for awareness)
- [Session] MCP memory is empty
- [Docs] 12 orphaned documentation files
```

## Scripts

### scripts/run-alerts.js

Main script that runs all checks and outputs JSON results. Usage:

```bash
node .claude/skills/alerts/scripts/run-alerts.js --limited
node .claude/skills/alerts/scripts/run-alerts.js --full
```

The script outputs JSON that can be parsed and presented to the user.

## Integration

This skill integrates with the Session Start Protocol in `claude.md`. At session
start, Claude should:

1. Run `/alerts` (limited mode) automatically
2. Present any errors or warnings to the user
3. Offer to run `/alerts --full` for comprehensive check
