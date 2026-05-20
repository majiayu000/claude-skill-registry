---
name: release
description: Release readiness checklist for shipping. Use after execution completes, when the user says "release" or "ship", or before deploying to production.
---

# Release — Pre-Ship Gate

Final verification before shipping. Maps to Protocol P12 (Release Readiness) and P13 (Security Gate).

> **Pattern:** This skill runs after all beads are closed. It verifies all work is done, security is clean, and the system is ready to ship.

## When This Applies

| Signal | Action |
|--------|--------|
| All beads closed | Run release checklist |
| User says "/release" or "ship" | Run release checklist |
| Before production deployment | Run release checklist |

---

## Prerequisites

Before running /release:
1. All execution phases complete (or user explicitly skipping)
2. No beads in `in_progress` status
3. Agent Mail available (if multi-agent)

---

## Tool Reference

### Verification Commands
| Command | Purpose |
|---------|---------|
| `bd list --json` | Verify all beads closed |
| `bv --robot-summary` | Check for orphaned/blocked beads |
| `bv --robot-alerts` | Surface any issues |
| `ubs --staged` | Security scan (MANDATORY) |
| `pytest` / `npm test` | Run test suite |
| `git status` | Check for uncommitted changes |
| `git log --oneline -10` | Recent commit history |

### Agent Mail (MCP)
| Tool | Purpose |
|------|---------|
| `fetch_inbox(agent_name, urgent_only=True)` | Check for unresolved urgent messages |
| `release_file_reservations(project_key, agent_name)` | Release any held reservations |
| `send_message(subject="[RELEASE READY]")` | Announce release readiness |

### Message Subjects
| Pattern | When |
|---------|------|
| `[RELEASE READY] Project Name` | All checks passed |
| `[RELEASE BLOCKED] Project Name` | Blockers found |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      RELEASE ORCHESTRATOR                        │
│  You are here. You:                                              │
│  - Verify all beads closed                                       │
│  - Run security scan                                             │
│  - Check for uncommitted work                                    │
│  - Validate against rigor tier                                   │
│  - Generate release report                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Bead Status    │  │  Security Gate  │  │  Multi-Agent    │
│  bd list        │  │  ubs --staged   │  │  Cleanup        │
│  bv --robot-*   │  │  Language audits│  │  Agent Mail     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Release Report │ → Present to operator
                    │  GO / NO-GO     │
                    └─────────────────┘
```

---

## Execution Flow

### Step 1: Setup

```markdown
1. Identify rigor tier from North Star Card:
   - Read PLAN/00_north_star.md (or project config)
   - Determine Tier 1, 2, or 3

2. Initialize TodoWrite with release phases:
   - [ ] Verify beads complete
   - [ ] Run security scan
   - [ ] Check git state
   - [ ] Multi-agent cleanup
   - [ ] Generate report
```

### Step 2: Verify Beads Complete

```bash
# Check for incomplete beads
bd list --json | jq '.[] | select(.status != "closed")'

# Get summary
bv --robot-summary

# Check for alerts
bv --robot-alerts
```

**Blocking if:**
- Any P0 beads not closed
- Any beads in `in_progress` status (orphaned work)

### Step 3: Security Gate (MANDATORY)

```bash
# Run security scan
ubs --staged

# For Java code (72% OWASP failure rate)
# ADDITIONAL manual SQL injection review required

# For web code (JS/TS)
# ADDITIONAL manual XSS output encoding review required
```

**Blocking if:**
- Any high/critical findings
- Medium findings without documented justification

### Step 4: Run Tests

```bash
# Run test suite (project-specific)
pytest                    # Python
npm test                  # Node.js
go test ./...             # Go
cargo test                # Rust
```

**Blocking if:**
- Any test failures

### Step 5: Check Git State

```bash
# Uncommitted changes?
git status

# Recent commits look right?
git log --oneline -10

# On correct branch?
git branch --show-current
```

**Blocking if:**
- Uncommitted changes (unless intentional)
- On wrong branch

### Step 6: Multi-Agent Cleanup

```python
# Check for unresolved urgent messages
urgent = fetch_inbox(
    project_key=PROJECT_PATH,
    agent_name=AGENT_NAME,
    urgent_only=True
)

if urgent:
    # Handle or acknowledge before release
    for msg in urgent:
        acknowledge_message(project_key, AGENT_NAME, msg.id)

# Release any file reservations
release_file_reservations(
    project_key=PROJECT_PATH,
    agent_name=AGENT_NAME
)

# Announce release readiness
send_message(
    project_key=PROJECT_PATH,
    sender_name=AGENT_NAME,
    to=["Coordinator"],  # or all agents
    subject="[RELEASE READY] Project Name",
    body_md="""
Release verification complete.

**Status:** READY TO SHIP
**Beads:** X closed, Y blocked
**Security:** Clean
**Tests:** Passing
    """,
    importance="high"
)
```

### Step 7: Generate Release Report

Present to operator:

```markdown
## Release Readiness Report

**Project:** [name]
**Rigor Tier:** [1/2/3]
**Date:** [timestamp]
**Agent:** [agent_name]

### Verification Summary

| Check | Status | Details |
|-------|--------|---------|
| Beads Complete | ✓/✗ | X/Y closed |
| Security (ubs) | ✓/✗ | Clean / N findings |
| Tests | ✓/✗ | All passing / N failures |
| Git State | ✓/✗ | Clean / uncommitted |
| Agent Mail | ✓/✗ | No urgent / N unresolved |

### Blockers
[List any blocking issues, or "None"]

### Recommendation
**[READY TO SHIP]** or **[BLOCKED - see above]**

### Next Steps
- [ ] Operator sign-off
- [ ] Tag release: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
- [ ] Deploy to [environment]
- [ ] Monitor logs/metrics
```

---

## Release Checklist by Rigor Tier

### Tier 1 (Personal/Hobby)

| Check | Required |
|-------|----------|
| All planned beads closed | ✓ |
| `ubs --staged` clean | ✓ |
| Basic smoke test | ✓ |
| No uncommitted changes | ✓ |

### Tier 2 (Startup MVP / Business Tool)

| Check | Required |
|-------|----------|
| All P0/P1 beads closed | ✓ |
| All tests passing | ✓ |
| `ubs --staged` clean | ✓ |
| Medium findings documented | ✓ |
| No secrets in codebase | ✓ |
| P0 requirements verified | ✓ |
| Basic observability | ✓ |
| Operator sign-off | ✓ |

### Tier 3 (Enterprise)

| Check | Required |
|-------|----------|
| All beads closed | ✓ |
| Full test suite passing | ✓ |
| `ubs --staged` zero findings | ✓ |
| Language-specific audits | ✓ |
| All REQ-* traced to tests | ✓ |
| Threat model reviewed | ✓ |
| Observability complete | ✓ |
| Rollback plan tested | ✓ |
| Audit trail complete | ✓ |
| Stakeholder sign-off | ✓ |

---

## Agent Mail Protocol

| Subject | Sender | Recipients | When |
|---------|--------|------------|------|
| `[RELEASE READY] Project` | Release Agent | Coordinator, All | All checks passed |
| `[RELEASE BLOCKED] Project` | Release Agent | Coordinator | Blockers found |

---

## Error Handling

### Beads Not Complete

1. List incomplete beads with `bd list --json`
2. Present to operator: complete or descope?
3. If descoping: document decision, update requirements
4. Re-run release check

### Security Findings

1. List findings from `ubs --staged`
2. For high/critical: MUST fix before release
3. For medium: document justification or fix
4. Re-run after fixes

### Test Failures

1. List failing tests
2. Fix failures or document known issues
3. Known issues require operator sign-off
4. Re-run after fixes

### Orphaned File Reservations

1. Check for stale reservations
2. Force release if agents are inactive
3. Document in release notes

---

## Post-Release

After shipping:

```bash
# Tag the release
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# Update beads (if any tracking beads remain)
bd close <release-bead-id> --reason "Released v1.0.0"
```

```python
# Notify team
send_message(
    project_key=PROJECT_PATH,
    sender_name=AGENT_NAME,
    to=["all"],
    subject="[RELEASED] v1.0.0",
    body_md="Release complete. Monitoring for issues.",
    importance="high"
)
```

---

## Mandatory Rules (2025 Research)

| Rule | Why | Evidence |
|------|-----|----------|
| **`ubs --staged` mandatory** | ~40% of LLM code has vulnerabilities | `research/052-llm-security-vulnerabilities.md` |
| **Java: extra SQL review** | 72% OWASP failure rate | `research/061-llm-security-2025.md` |
| **JS/TS: XSS review** | Only 14% XSS caught | `research/061-llm-security-2025.md` |
| **Human verification for P0** | AI helps most when human understands domain | `research/051-metr-rct.md` |

---

## Evidence Base

| Research | Finding |
|----------|---------|
| `research/021-swe-bench-plus.md` | Benchmark hygiene matters; don't trust passing tests alone |
| `research/047-humaneval-pro.md` | Progressive verification catches drift |
| `research/044-iris.md` | Security verification is essential |
| `research/052-llm-security-vulnerabilities.md` | ~40% of LLM code has vulnerabilities |
| `research/061-llm-security-2025.md` | Language-specific vulnerability rates |
| `research/051-metr-rct.md` | Human verification required for production |

---

## See Also

- `/calibrate` — Run if drift detected before release
- `/prime` — Worker startup (for re-verification)
- `docs/workflow/PROTOCOLS.md` — P12: Release Readiness, P13: Security Gate
- `docs/workflow/IDEATION_TO_PRODUCTION.md` — Stage 10
- `advance/` — Bead lifecycle details
