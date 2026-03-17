---
name: opi
description: |
  Extract learnings from recent git commits, current conversation, and security reviews.
  Captures both reactive fixes (what went wrong) and preventive patterns (what to always do).
  Routes learnings to global or skill-specific files so all future Claude sessions benefit.

  Use when:
  - User says "/opi" or "opi"
  - "What did we learn?"
  - "Extract learnings" / "Update learnings"
  - End of session reflection
  - After a security review or audit
  - After creating reusable components/patterns that other skills should know about

  Triggers: "opi", "learn", "oppia", "mitä opittiin", "extract learnings", "add learning"
---

# Opi - Learning Extractor

Extract learnings from recent work to improve future Claude sessions. Captures **two types**:

1. **Reactive** — What went wrong and how it was fixed (bugs, corrections, failed attempts)
2. **Preventive** — Reusable patterns that prevent future problems (safe components, conventions, security defaults)

## Workflow

### Step 1: Gather Sources

```bash
# Recent commits (last 20)
git log --oneline -20

# Today's commits with details
git log --since="midnight" --format="%h %s"

# Fix/refactor/security commits
git log --oneline -50 | grep -iE "(fix|korja|refactor|bugfix|secur|safe|harden)"
```

Also check:
- Current conversation for corrections, discoveries, new patterns
- Recent security reviews or audit results
- New reusable components or utilities created this session

### Step 2: Classify Each Finding

For each potential learning, determine the **type**:

| Type | Signal | Example |
|------|--------|---------|
| **Reactive fix** | Bug fixed, user corrected, test failed | "useEffect infinite loop — wrap in useCallback" |
| **Preventive pattern** | New convention, safe default, reusable component | "Use SafeTextarea for user-facing text inputs" |
| **Security hardening** | Vulnerability found, RLS gap, input validation | "Always enforce maxLength on text inputs" |
| **Anti-pattern** | Repeatedly wrong approach discovered | "Don't use bare Textarea without maxLength" |

### Step 3: Route to Destination

See [references/learnings-router.md](references/learnings-router.md) for the full routing table.

Quick reference:

| Learning Domain | Destination |
|----------------|-------------|
| React/TypeScript, Supabase/DB, CSS, i18n | `.claude/LEARNINGS.md` |
| Security patterns, input validation | `.claude/LEARNINGS.md` (Security section) |
| CI/CD | `ci-doctor/references/learnings.md` |
| Lint/formatting | `lint-fixer/references/learnings.md` |
| Tests | `test-writer/references/learnings.md` |
| Security audits, RLS | `security-auditor/references/learnings.md` |
| Supabase migrations | `supabase-migration-writer/references/learnings.md` |
| Other skill-specific | `[skill]/references/learnings.md` |

### Step 4: Format Learnings

**Reactive fix format:**
```markdown
### [Issue Title]
- **Pattern:** What triggers this mistake
- **Wrong:** ❌ The incorrect approach
- **Right:** ✅ The correct approach
- **Why:** Root cause
```

**Preventive pattern format:**
```markdown
### [Convention Title]
- **Rule:** Always do X when Y
- **Wrong:** ❌ The old/unsafe way
- **Right:** ✅ The new/safe way
- **Why:** What this prevents
- **Since:** date or commit ref
```

**Recent Corrections table row:**
```markdown
| Date | Issue | Fix | Applies To |
```

### Step 5: Propose & Write

1. Present all proposed learnings grouped by destination file
2. User approves/rejects each
3. Write approved learnings to files
4. Commit changes

## Learning Quality Criteria

Only propose learnings that are:

- **Non-obvious** — Claude wouldn't know without being told
- **Actionable** — Concrete wrong/right examples, not vague advice
- **Recurring** — Likely to come up again in this codebase
- **Preventive OR Corrective** — Either prevents future bugs or fixes repeated mistakes

**Skip:** Typo fixes, one-off configs, project-specific constants, things Claude already knows.

## Preventive Patterns to Watch For

When analyzing commits, specifically look for these signals that indicate a preventive learning:

| Signal in Commit | Learning Type |
|-----------------|---------------|
| New reusable component created | "Always use X instead of Y" convention |
| Security hardening (maxLength, validation, RLS) | Security default rule |
| `feat(security):` or `fix(security):` prefix | Security learning |
| Wrapper/helper replacing bare primitive | Anti-pattern (bare primitive) + convention (use wrapper) |
| Migration adding constraints/checks | DB convention |
| New utility extracted from repeated code | "Use X utility" convention |

## Commands Reference

```bash
# Commits since specific date
git log --since="2025-01-10" --oneline

# Commits by pattern
git log --all --oneline | grep -i "fix"

# Show specific commit
git show <hash> --name-only

# Diff for a commit
git diff <hash>^..<hash>

# Security-related commits
git log --oneline -50 | grep -iE "(secur|rls|grant|xss|valid|sanitiz|safe|harden)"
```
