---
name: retro
description: 'Extract learnings from completed work. Trigger phrases: "run a retrospective", "extract learnings", "what did we learn", "lessons learned", "capture lessons", "create a retro".'
metadata:
  tier: knowledge
  dependencies:
    - vibe  # optional - can receive --vibe-results
---

# Retro Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Extract learnings from completed work, propose proactive improvements, and feed the knowledge flywheel.

## Execution Steps

Given `/retro [topic] [--vibe-results <path>]`:

### Step 1: Identify What to Retrospect

**If vibe results path provided:** Read and incorporate validation findings:
```
Tool: Read
Parameters:
  file_path: <vibe-results-path>
```

This allows post-mortem to pass validation context without re-running vibe.

**If topic provided:** Focus on that specific work.

**If no topic:** Look at recent activity:
```bash
# Recent commits
git log --oneline -10 --since="7 days ago"

# Recent issues closed
bd list --status closed --since "7 days ago" 2>/dev/null | head -5

# Recent research/plans
ls -lt .agents/research/ .agents/plans/ 2>/dev/null | head -5
```

### Step 2: Gather Context

Read relevant artifacts:
- Research documents
- Plan documents
- Commit messages
- Code changes

Use the Read tool and git commands to understand what was done.

### Step 3: Identify Learnings

**If vibe results were provided, incorporate them:**
- Extract learnings from CRITICAL and HIGH findings
- Note patterns that led to issues
- Identify anti-patterns to avoid

Ask these questions:

**What went well?**
- What approaches worked?
- What was faster than expected?
- What should we do again?

**What went wrong?**
- What failed?
- What took longer than expected?
- What would we do differently?
- (Include vibe findings if provided)

**What did we discover?**
- New patterns found
- Codebase quirks learned
- Tool tips discovered
- Debugging insights

### Step 4: Extract Actionable Learnings

For each learning, capture:
- **ID**: L1, L2, L3...
- **Category**: debugging, architecture, process, testing, security
- **What**: The specific insight
- **Why it matters**: Impact on future work
- **Confidence**: high, medium, low

### Step 5: Write Learnings

**Write to:** `.agents/learnings/YYYY-MM-DD-<topic>.md`

```markdown
# Learning: <Short Title>

**ID**: L1
**Category**: <category>
**Confidence**: <high|medium|low>

## What We Learned

<1-2 sentences describing the insight>

## Why It Matters

<1 sentence on impact/value>

## Source

<What work this came from>

---

# Learning: <Next Title>

**ID**: L2
...
```

### Step 6: Write Retro Summary

**Write to:** `.agents/retros/YYYY-MM-DD-<topic>.md`

```markdown
# Retrospective: <Topic>

**Date:** YYYY-MM-DD
**Scope:** <what work was reviewed>

## Summary
<1-2 sentence overview>

## What Went Well
- <thing 1>
- <thing 2>

## What Could Be Improved
- <improvement 1>
- <improvement 2>

## Learnings Extracted
- L1: <brief>
- L2: <brief>

See: `.agents/learnings/YYYY-MM-DD-<topic>.md`

## Proactive Improvement Agenda

| # | Area | Improvement | Priority | Horizon | Effort | Evidence |
|---|------|-------------|----------|---------|--------|----------|
| 1 | repo / execution / CI | <improvement> | P0/P1/P2 | now/next-cycle/later | S/M/L | <retro evidence> |

### Recommended Next /rpi
/rpi "<highest-value item>"

## Action Items
- [ ] <any follow-up needed>
```

### Step 6.5: Proactive Improvement Agenda (MANDATORY)

After writing the retro summary, use the full context you just gathered to propose concrete improvements.

Ask explicitly:
1. **Repo:** What should we improve in the codebase/contracts/docs to reduce future defects?
2. **Execution:** What should we improve in planning/implementation/review workflow to increase throughput?
3. **CI/Automation:** What should we improve in validation gates/tooling to reduce noise and catch regressions earlier?

Requirements:
- Propose at least **5** items total.
- Cover all three areas above (repo, execution, CI/automation).
- Include at least **1 quick win** (small, low-risk, same-session viable).
- For each item include: `priority` (P0/P1/P2), `horizon` (now/next-cycle/later), `effort` (S/M/L), and one-line rationale tied to retro evidence.
- Mark one item as **Recommended Next /rpi**.

Write this into the retro file under:
```markdown
## Proactive Improvement Agenda

| # | Area | Improvement | Priority | Horizon | Effort | Evidence |
|---|------|-------------|----------|---------|--------|----------|
| 1 | CI | <improvement> | P0 | now | S | <retro evidence> |

### Recommended Next /rpi
/rpi "<highest-value item>"
```

### Step 7: Feed the Knowledge Flywheel (auto-extract)

```bash
# If ao available, index via forge and apply task feedback
if command -v ao &>/dev/null; then
  ao forge markdown .agents/learnings/YYYY-MM-DD-*.md 2>/dev/null
  echo "Learnings indexed in knowledge flywheel"

  # Apply feedback from completed tasks to associated learnings
  ao task-feedback 2>/dev/null
  echo "Task feedback applied"
else
  # Learnings are already written to .agents/learnings/ by Step 5.
  # Without ao CLI, grep-based search in /research, /knowledge, and /inject
  # will find them directly — no copy to pending needed.

  # Build lightweight keyword index for faster search
  mkdir -p .agents/ao
  for f in .agents/learnings/YYYY-MM-DD-*.md; do
    [ -f "$f" ] || continue
    TITLE=$(head -1 "$f" | sed 's/^# //')
    echo "{\"file\": \"$f\", \"title\": \"$TITLE\", \"keywords\": [], \"timestamp\": \"$(date -Iseconds)\"}" >> .agents/ao/search-index.jsonl
  done
  echo "Learnings indexed locally (ao CLI not available — grep-based search active)"
fi
```

This auto-extraction step ensures every retro feeds the flywheel without requiring the user to remember manual commands.

### Step 8: Report to User

Tell the user:
1. Number of learnings extracted
2. Key insights (top 2-3)
3. Location of retro and learnings files
4. Knowledge has been indexed for future sessions
5. Top proactive improvements (top 3) + recommended next `/rpi`

## Key Rules

- **Be specific** - "auth tokens expire" not "learned about auth"
- **Be actionable** - learnings should inform future decisions
- **Cite sources** - reference what work the learning came from
- **Write both files** - retro summary AND detailed learnings
- **Be proactive** - always produce repo + execution + CI improvements from gathered context
- **Index knowledge** - make it discoverable

## The Flywheel

Learnings feed future research:
```
Work → /retro → improvements + learnings → ao forge markdown → /research finds it
```

Future sessions start smarter because of your retrospective.

## Examples

### Retrospective After Implementation

**User says:** `/retro`

**What happens:**
1. Agent looks at recent activity via `git log --oneline -10`
2. Agent finds 8 commits related to authentication refactor
3. Agent reads commit messages, code changes, and related issue in beads
4. Agent asks: What went well? What went wrong? What was discovered?
5. Agent identifies 4 learnings: L1 (token expiry pattern), L2 (middleware ordering matters), L3 (test coverage caught edge case), L4 (documentation prevents support load)
6. Agent writes learnings file to `.agents/learnings/2026-02-13-auth-refactor.md`
7. Agent writes retro summary to `.agents/retros/2026-02-13-auth-refactor.md`
8. Agent runs `ao forge markdown` to add learnings to knowledge base

**Result:** 4 learnings extracted and indexed, retro summary documents what went well and improvements needed.

### Post-Mortem with Vibe Results

**User says:** `/retro --vibe-results .agents/council/2026-02-13-vibe-api.md`

**What happens:**
1. Agent reads vibe results file showing 2 CRITICAL and 3 HIGH findings
2. Agent extracts learnings from validation findings (race condition pattern, missing input validation)
3. Agent reviews recent commits for context
4. Agent creates 6 learnings: 2 from vibe findings (what to avoid), 4 from successful patterns (what to repeat)
5. Agent writes both learnings and retro files
6. Agent indexes knowledge automatically via ao forge

**Result:** Vibe findings incorporated into learnings, preventing same issues in future work.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No recent activity found | Clean git history or work not committed yet | Ask user what to retrospect. Accept manual topic: `/retro "planning process improvements"`. Review uncommitted changes if needed. |
| Learnings too generic | Insufficient analysis or surface-level review | Dig deeper into code changes. Ask "why" repeatedly. Ensure learnings are actionable (specific pattern, not vague principle). Check confidence level. |
| ao forge markdown fails | ao CLI not installed or .agents/ structure wrong | Graceful fallback: index learnings locally to `.agents/ao/search-index.jsonl`. Notify user ao not available. Learnings still in `.agents/learnings/` and discoverable via grep-based search. |
| Duplicate learnings extracted | Same insight from multiple sources | Deduplicate before writing. Check existing learnings with grep. Merge duplicates into single learning with multiple source citations. |
