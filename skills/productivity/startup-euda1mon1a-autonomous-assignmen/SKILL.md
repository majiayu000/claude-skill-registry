---
name: startup
description: Review essential documentation and context at session start. Use when beginning a new session to load AI rules, git state, and pending tasks.
model_tier: haiku
parallel_hints:
  can_parallel_with: [check-codex]
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 40
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "divergent.*history"
    reason: "Git history issues require human intervention"
  - pattern: "behind.*main"
    reason: "Branch sync decisions need human input"
---

# Session Startup Skill

> **Purpose:** Review essential documentation and context at the start of each session
> **Created:** 2025-12-27
> **Trigger:** `/startup` command or session start
> **Aliases:** `/session-start`, `/ready`

---

## When to Use

Run `/startup` at the beginning of every session to:
- Review AI Rules of Engagement
- Check current git state and branch
- Review pending tasks from HUMAN_TODO.md
- Identify blockers or in-progress work
- Confirm readiness to work

---

## Required Actions

When this skill is invoked, Claude MUST:

### 1. Review Core Documentation

Read these files in order:

```
1. CLAUDE.md                                    # Project guidelines
2. docs/development/AI_RULES_OF_ENGAGEMENT.md   # Git/PR workflow rules
3. HUMAN_TODO.md                                # Current tasks and priorities
4. docs/development/DEBUGGING_WORKFLOW.md       # Debugging methodology (skim)
5. docs/development/CI_CD_TROUBLESHOOTING.md    # Common CI issues (skim)
```

### 2. Check Git Context

Run these commands:

```bash
# Current branch
git branch --show-current

# Recent commits on this branch
git log --oneline -5

# Check for uncommitted changes
git status --porcelain

# Check for other AI branches in progress
git branch -r | grep -E 'claude/|codex/|ai/' | head -5

# Check if behind origin/main
git fetch origin main && git rev-list --count HEAD..origin/main
```

### 3. Check Codex Feedback (if PR exists)

If current branch has an open PR, check for Codex feedback. Codex (GitHub AI) reviews PRs and is **the rate-limiting step before merge**.

```bash
PR_NUMBER=$(gh pr view --json number -q '.number' 2>/dev/null)
if [ -n "$PR_NUMBER" ]; then
  REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
  CODEX_COUNT=$(gh api repos/${REPO}/pulls/${PR_NUMBER}/comments \
    --jq '[.[] | select(.user.login == "chatgpt-codex-connector[bot]")] | length' 2>/dev/null || echo "0")

  if [ "$CODEX_COUNT" -gt 0 ]; then
    echo "Codex Feedback: ${CODEX_COUNT} comment(s) pending - run /check-codex"
  fi
fi
```

### 4. Check System Health (Optional)

If Docker is running:

```bash
# Container status
docker compose ps 2>/dev/null || echo "Docker not running"

# Backend health
curl -s http://localhost:8000/health 2>/dev/null || echo "Backend not available"
```

### 5. Check MCP/RAG Health (CRITICAL)

**Without MCP, Claude Code loses access to RAG and 30+ scheduling tools.**

```bash
# Check MCP container
MCP_STATUS=$(docker inspect scheduler-local-mcp --format '{{.State.Health.Status}}' 2>/dev/null || echo "not running")
if [ "$MCP_STATUS" != "healthy" ]; then
  echo "⚠️  WARNING: MCP container is $MCP_STATUS"
  echo "   Claude Code has NO RAG access and NO MCP tools!"
  echo "   Run: ./scripts/start-local.sh"
fi
```

Then verify RAG is accessible by calling `mcp__residency-scheduler__rag_health`.

**If RAG check fails with 401 or connection error:**
```
⚠️  CRITICAL: RAG/MCP NOT AVAILABLE
   - Cannot search knowledge base
   - Cannot use scheduling MCP tools
   - Cannot validate ACGME compliance via MCP

   Fix: ./scripts/start-local.sh (starts all services including MCP)
```

### 6. Check Resilience Status (REQUIRED)

**If MCP is available, ALWAYS check system resilience:**

```python
# Get current defense level
mcp__residency-scheduler__get_defense_level_tool(coverage_rate=0.95)
```

**Interpret results:**
- **GREEN (Level 1-2):** Normal operations, proceed with work
- **YELLOW (Level 3):** Increased monitoring, be cautious with changes
- **ORANGE (Level 4):** Elevated risk, avoid schedule modifications
- **RED (Level 5):** Critical issues, escalate to human

Include defense level in session output. If ORANGE or RED, flag as blocker.

### 7. Check API Type Staleness (Hydra's Heads)

**Generated types must match backend schemas.** Check for drift:

```bash
# Quick staleness check (compares timestamps)
BACKEND_SCHEMA_TIME=$(stat -f %m backend/app/schemas/*.py 2>/dev/null | sort -rn | head -1 || echo "0")
GENERATED_TYPES_TIME=$(stat -f %m frontend/src/types/api-generated.ts 2>/dev/null || echo "0")

if [ "$BACKEND_SCHEMA_TIME" -gt "$GENERATED_TYPES_TIME" ]; then
  echo "⚠️  WARNING: API types may be stale"
  echo "   Backend schemas modified after types were generated"
  echo "   Run: cd frontend && npm run generate:types"
fi
```

**If backend is running, do full drift check:**
```bash
cd frontend && npm run generate:types:check
```

**Include in session output:**
- **Types:** In sync / ⚠️ Stale (regenerate needed)

**Why this matters:** Schema drift caused 47+ wiring disconnects. See CLAUDE.md "OpenAPI Type Contract" section.

---

## Output Format

Provide a concise summary in this format:

```markdown
## Session Ready

**Branch:** `claude/current-task`
**Status:** Clean working tree / X uncommitted changes
**Behind main:** 0 commits / X commits (rebase needed)

### Codex Feedback
- **Status:** [N] comment(s) pending (run `/check-codex` for details)
- **Or:** No Codex feedback yet (typically 1-10 min after PR)
- **Or:** No PR for current branch

### Key Rules Acknowledged
- origin/main is sacred - PRs only
- Backup before database modifications
- Run linters before PR (ruff, npm lint)

### Current Priorities (from HUMAN_TODO.md)
1. [Priority item 1]
2. [Priority item 2]
3. [Priority item 3]

### Blockers/In-Progress
- [Any blocked items or WIP from previous sessions]
- [Codex P1 issues flagged as blockers if present]

### System Status
- Backend: Running/Not running
- Database: X assignments in Block Y
- MCP: healthy/unhealthy/not running
- RAG: X documents indexed / unavailable
- Types: In sync / ⚠️ Stale (run `cd frontend && npm run generate:types`)

**⚠️ If MCP unavailable:** Run `./scripts/start-local.sh`
**⚠️ If Types stale:** Run `cd frontend && npm run generate:types`

Ready to work. What's the task?
```

---

## Key Rules to Acknowledge

Every startup should confirm understanding of:

### Git Workflow
- `origin/main` is the single source of truth
- Always create feature branches from `origin/main`
- Never push directly to main - use PRs
- Never force push without explicit approval

### MCP Safety
- Database-modifying operations require backup + approval
- Read-only operations are always safe

### Code Quality
- Run `ruff check --fix` and `ruff format .` before PRs
- Run `npm run lint:fix` for frontend
- Tests must pass before commit

### Debugging Approach
- Explore first, fix second
- Write failing tests before fixing bugs
- Use "think hard" / "ultrathink" for complex issues

---

## Quick Reference Card

```
HARD STOPS (ask user):
- Divergent histories
- Force push required
- Protected branch modification
- Merge conflicts

SAFE COMMANDS (always OK):
git status, git diff, git log, git branch, git fetch

BEFORE EVERY COMMIT:
cd backend && ruff check . --fix && pytest
cd frontend && npm run lint:fix && npm test
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `check-codex` | View detailed Codex feedback (rate-limiting step before merge) |
| `session-documentation` | End of session handoff |
| `systematic-debugger` | Complex bug investigation |
| `safe-schedule-generation` | Before schedule modifications |
| `pr-reviewer` | Before creating PRs |

---

## Related Protocols

| Protocol | When to Use |
|----------|-------------|
| [CCW Burn Protocol](../../protocols/CCW_BURN_PROTOCOL.md) | Before running parallel CCW task burns (20+ tasks) |
| [PLAN_PARTY Protocol](../../protocols/PLAN_PARTY.md) | Complex task planning (after reconnaissance or standalone) |

**CCW Burn Key Points:**
- Validate every 20 tasks (build + type-check gate)
- Watch for token concatenation bugs (`await sawait ervice`)
- Pre-burn: `npm run build && npm run type-check` must pass

---

## Example Invocation

**User:** `/startup`

**Claude:**
```markdown
## Session Ready

**Branch:** `claude/fix-mcp-namespace-collision`
**Status:** Clean working tree
**Behind main:** 0 commits

### Codex Feedback
- **Status:** 2 comment(s) pending (run `/check-codex` for details)

### Key Rules Acknowledged
- origin/main is sacred - PRs only
- Backup before database modifications
- Run linters before PR

### Current Priorities (from HUMAN_TODO.md)
1. UI/UX: Frozen headers on schedule grid
2. Heatmap: Add block navigation
3. Backend: Fix faculty rotation_template_id assignment

### Blockers/In-Progress
- FastMCP upgrade blocked on URI template changes (see MCP_FASTMCP_UPGRADE_NEEDED.md)
- Codex feedback pending (2 comments) - address before merge

### System Status
- Backend: Running (Docker)
- Database: 87 assignments in Block 10

Ready to work. What's the task?
```

---

*This skill ensures every session starts with proper context and rule awareness.*
