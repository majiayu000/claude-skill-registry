---
name: continuity_ledger
description: Create or update continuity ledger for state preservation across clears
---

# Continuity Ledger

Maintain a ledger file that survives `/clear` for long-running sessions. Unlike handoffs (cross-session), ledgers preserve state within a session.

**Why clear instead of compact?** Each compaction is lossy compression—after several compactions, you're working with degraded context. Clearing + loading the ledger gives you fresh context with full signal.

## When to Use

- Before running `/clear`
- Context usage approaching 70%+
- Multi-day implementations
- Complex refactors you pick up/put down
- Any session expected to hit 85%+ context

## When NOT to Use

- Quick tasks (< 30 min)
- Simple bug fixes
- Single-file changes
- Already using handoffs for cross-session transfer

## Process

### 1. Determine Ledger File

Check if a ledger already exists:
```bash
ls thoughts/ledgers/CONTINUITY_CLAUDE-*.md 2>/dev/null
```

- **If exists**: Update the existing ledger
- **If not**: Create new file: `thoughts/ledgers/CONTINUITY_CLAUDE-<session-name>.md`
  - First ensure directory exists: `mkdir -p thoughts/ledgers`
  - Use kebab-case for session name (e.g., `auth-refactor`, `api-migration`)

### 2. Create/Update Ledger

Use this template structure:

```markdown
# Session: <name>
Updated: <ISO timestamp>

## Goal
<Success criteria - what does "done" look like?>

## Constraints
<Tech requirements, patterns to follow, things to avoid>

## Key Decisions
<Choices made with brief rationale>
- Decision 1: Chose X over Y because...
- Decision 2: ...

## State
- Done: <completed items>
- Now: <current focus - ONE thing only>
- Next: <queued items in priority order>

## Open Questions
- UNCONFIRMED: <things needing verification after clear>
- UNCONFIRMED: <assumptions that should be validated>

## Working Set
<Active files, branch, test commands>
- Branch: `feature/xyz`
- Key files: `src/auth/`, `tests/auth/`
- Test cmd: `npm test -- --grep auth`
- Build cmd: `npm run build`
```

### 3. Update Guidelines

**When to update the ledger:**
- Session start: Read and refresh
- After major decisions
- Before `/clear`
- At natural breakpoints
- When context usage >70%

**What to update:**
- Move completed items from "Now" to "Done"
- Update "Now" with current focus
- Add new decisions as they're made
- Mark items as UNCONFIRMED if uncertain

### 4. After Clear Recovery

When resuming after `/clear`:

1. **Ledger loads automatically** (SessionStart hook)
2. **Review UNCONFIRMED items**
3. **Ask 1-3 targeted questions** to validate assumptions
4. **Update ledger** with clarifications
5. **Continue work** with fresh context

## Template Response

After creating/updating the ledger, respond:

```
Continuity ledger updated: thoughts/ledgers/CONTINUITY_CLAUDE-<name>.md

Current state:
- Done: <summary>
- Now: <current focus>
- Next: <upcoming>

Ready for /clear - ledger will reload on resume.
```

## Comparison with Other Tools

| Tool | Scope | Fidelity |
|------|-------|----------|
| CLAUDE.md | Project | Always fresh, stable patterns |
| TodoWrite | Turn | Survives compaction, but understanding degrades |
| CONTINUITY_CLAUDE-*.md | Session | External file—never compressed, full fidelity |
| Handoffs | Cross-session | External file—detailed context for new session |

## Example

```markdown
# Session: auth-refactor
Updated: 2025-01-15T14:30:00Z

## Goal
Replace JWT auth with session-based auth. Done when all tests pass and no JWT imports remain.

## Constraints
- Must maintain backward compat for 2 weeks (migration period)
- Use existing Redis for session storage
- No new dependencies

## Key Decisions
- Session tokens: UUID v4 (simpler than signed tokens for our use case)
- Storage: Redis with 24h TTL (matches current JWT expiry)
- Migration: Dual-auth period, feature flag controlled

## State
- Done: Session model, Redis integration, login endpoint
- Now: Logout endpoint and session invalidation
- Next: Middleware swap, remove JWT, update tests

## Open Questions
- UNCONFIRMED: Does rate limiter need session awareness?

## Working Set
- Branch: `feature/session-auth`
- Key files: `src/auth/session.ts`, `src/middleware/auth.ts`
- Test cmd: `npm test -- --grep session`
```

## Additional Notes

- **Keep it concise** - Brevity matters for context
- **One "Now" item** - Forces focus, prevents sprawl
- **UNCONFIRMED prefix** - Signals what to verify after clear
- **Update frequently** - Stale ledgers lose value quickly
- **Clear > compact** - Fresh context beats degraded context
