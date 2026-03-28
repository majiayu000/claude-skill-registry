---
name: phx:compound
description: Use after fixing any non-trivial bug, resolving a tricky issue, or when the user says "that worked" or "it is fixed". Also suggest proactively after successful /phx:review or /phx:investigate. Captures solved problems as searchable Elixir/Phoenix solution documentation for faster future debugging.
effort: low
argument-hint: [description of what was fixed]
---

# Compound — Capture Solutions as Knowledge

After fixing a problem, capture the solution as searchable
institutional documentation.

## Usage

```
/phx:compound Fixed N+1 query in user listing
/phx:compound Resolved LiveView timeout in dashboard
/phx:compound   # Auto-detects from recent session context
```

## Philosophy

> Each unit of engineering work should make subsequent units
> easier — not harder.

## Workflow

### Step 1: Detect Context

1. If `$ARGUMENTS` provided, use as description
2. If no args, check scratchpad DEAD-END/DECISION entries,
   `git diff`, `.claude/plans/{slug}/progress.md` for recent completions
3. If unclear, ask: "What problem did you just solve?"

**Only document non-trivial problems** that required investigation.

### Step 2: Search Existing Solutions

```bash
mkdir -p .claude/solutions
grep -rl "KEYWORD" .claude/solutions/ 2>/dev/null
```

If found: **Create new** (different root cause), **Update
existing** (same root cause, new symptom), or **Skip**.

### Step 3: Gather Details and Create Solution

Extract from session context: module, symptoms, investigation
steps, root cause, solution code, and prevention advice.

Validate frontmatter against `compound-docs/references/schema.md`,
then create file using `compound-docs/references/resolution-template.md`.

### Step 4: Decision Menu

1. **Continue** (default)
2. **Promote to Iron Law check** — Add to iron-law-judge
3. **Update skill reference** — Add to relevant skill
4. **Update CLAUDE.md** — Add prevention rule

## Auto-Trigger Phrases

When user says "that worked", "it's fixed", "problem solved",
"the fix was" — suggest `/phx:compound`.

## Iron Laws

1. **YAML frontmatter validates or STOP**
2. **Symptoms must be specific** — not "it broke"
3. **Root cause is WHY, not WHAT**
4. **One problem per file**
5. **NEVER document a fix before verifying it works** — run `mix compile && mix test` first; unverified solutions poison the knowledge base

## Integration with Workflow

```text
/phx:review → Complete → /phx:compound  ← YOU ARE HERE
                              │
                 .claude/solutions/{category}/{fix}.md
                              │
              /phx:investigate and /phx:plan search here
```

## References

- `${CLAUDE_SKILL_DIR}/references/compound-workflow.md` — Detailed step-by-step
- See also: `compound-docs` skill for schema and templates
