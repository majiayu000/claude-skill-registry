---
name: session-compounding
description: Reviews a work session's output to detect improvable patterns, classify improvements, and execute the highest-priority one. Use at the end of significant work sessions to ensure the COMPOUND phase of the enforcement loop happens. Without explicit compounding, improvement never happens.
protocol_id: PROTO-ORG-5
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-verify, organon-health, organon-find]
loads:
  - CLAUDE.md
  - book-llms/patterns.md
  - book-llms/workflow-authoring.md
  - organon/observations/README.md
---

# Session Compounding Workflow

> Implements PROTO-ORG-5 from `organon/protocols/PROTOCOLS.md`. Converts session learnings into durable improvements.

---

## When to Use This Skill

Use this skill when:
- **Ending a significant work session** — substantial changes were made
- **After completing a multi-step task** — new patterns may have emerged
- **After encountering friction** — something was harder than it should have been
- **Periodically** — even smooth sessions may reveal optimization opportunities

**Purpose:** The methodology warns: "Without explicit time allocation, improvement never happens." This workflow makes the COMPOUND step actionable.

---

## Context Loading

1. Load project constraints:
   - Read `CLAUDE.md` (project-level guidance and decision heuristics)
2. Load pattern references:
   - Read `book-llms/patterns.md` (Recursive Collaboration + Observation Accumulation sections)
   - Read `book-llms/workflow-authoring.md` (workflow quality attributes for evaluating workflow improvements)
3. Load recent observations:
   - Read `organon/observations/README.md` (index of existing observation files)
   - Read the most recent observation file listed in the README (for context on prior findings)

---

## Steps

### Step 1: Review Session Work

Examine what happened during the session:

```bash
git diff --stat HEAD~N  # where N = number of commits in this session
git log --oneline -N    # recent commits
```

List:
- Files created or modified
- Types of changes (organon content, tooling, skills, documentation)
- Patterns in the work (what was repeated, what was manual)

### Step 2: Detect Patterns

Review the most recent observation file to check whether this session's findings relate to previously recorded observations. Look for recurrence — the same friction appearing again strengthens a signal into a pattern.

Look for these improvement signals:

| Signal | Example | Indicates |
|--------|---------|-----------|
| **Repeated manual steps** | "I ran `organon validate` then `organon verify` then `organon health` every time" | Tool candidate (composite command) |
| **Unclear workflow** | "I wasn't sure which skill to use for this task" | Workflow gap or unclear naming |
| **New heuristic discovered** | "I learned that scopes.md always needs updating after ETHOS.md changes" | Heuristic addition to CLAUDE.md or ETHOS.md |
| **Awkward tool usage** | "I had to run the same command 3 different ways to get what I needed" | Tool improvement (better defaults, new flag) |
| **Missing context** | "I needed to read 5 files before starting but the skill only listed 3" | Workflow context update |
| **Terminology confusion** | "I kept saying 'skill' when I meant 'workflow'" | Terminology cleanup needed |
| **Error without guidance** | "The tool failed but I didn't know how to fix it" | Error recovery table addition |

### Step 3: Classify Improvements

For each finding, categorize it:

| Category | Description | Where to Implement |
|----------|-------------|-------------------|
| **Tool candidate** | Repeated operation that could be automated | `packages/tools/` — new command or flag |
| **Protocol update** | Procedure followed but not documented | `organon/protocols/PROTOCOLS.md` — new or updated protocol |
| **Heuristic addition** | Decision made repeatedly in same way | `CLAUDE.md` or `organon/ETHOS.md` — new heuristic row |
| **Workflow refinement** | Existing workflow that was awkward or incomplete | `.claude/skills/<name>/SKILL.md` — update steps, context, or error recovery |
| **Documentation gap** | Information needed but not findable | `book-llms/` or `book-humans/` — new content |

### Step 4: Prioritize

Rank improvements by frequency x impact:

```
Priority = How often does this recur? × How much friction does it cause?
```

| Frequency | Impact | Priority |
|-----------|--------|----------|
| Every session | Blocks work | Highest — do now |
| Weekly | Slows work | High — do this session |
| Monthly | Annoying | Medium — create RFC or TODO |
| Rare | Minor | Low — note for future |

### Step 5: Generate Improvement Plan

For the top-priority improvement, draft:
1. **What** — specific change to make
2. **Where** — exact file(s) to modify
3. **Why** — what problem this solves
4. **How to verify** — how to confirm the improvement works

### Step 6: Execute Improvement

With user confirmation, implement the highest-priority improvement:
- If tool candidate → create RFC (use `domain-feature-design` skill)
- If protocol update → edit PROTOCOLS.md
- If heuristic addition → edit CLAUDE.md or organon/ETHOS.md
- If workflow refinement → edit the skill file
- If documentation gap → create or update the relevant file

### Step 7: Record Observations (Optional)

If this session produced observations worth preserving beyond the immediate session, record them:

**Decision:**
- An active observation file covers this topic → **add to it** (new O-entry in the Observations section)
- No relevant file exists → **create new** `organon/observations/NNN-descriptive-name.md`

**What to record:** Each observation needs Signal (what happened), Implication (what it means), Suggested Action (what to do). See the [Observation Accumulation Pattern](book-llms/patterns.md#observation-accumulation-pattern) for the convention.

**When NOT to record:**
- Single-occurrence friction you already fixed (just a bug fix)
- Opinions without evidence
- Observations already captured in methodology guidance
- Session-specific context that won't generalize

**Not every session produces observations — that's fine.** Only record when the session revealed something worth remembering across sessions.

### Step 8: Check for Stale Terminology

Search ALL files for terminology that may have become inconsistent during the session:

Use the Grep tool to search all files for the term:

```
Grep pattern="<term-to-check>" path="." glob="*.md"
```

Also check organon files by name:

```bash
cd packages/tools && npx organon find --name "<term-to-check>"
```

Check common drift points:
- `CLAUDE.md` vs `organon/ETHOS.md` (must stay in sync)
- Skill descriptions vs actual skill content
- Protocol names vs workflow names

### Step 9: Run Verification

```bash
cd packages/tools && npx organon verify
cd packages/tools && npx organon health
```

Confirm no regressions from the improvement.

---

## Verification

- [ ] At least one improvement identified and classified
- [ ] Highest-priority improvement either executed or documented
- [ ] `organon verify` passes after any changes
- [ ] `organon health` score has not decreased
- [ ] No stale terminology found

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| No patterns detected | Session may have been too small or too routine. Note for next session. Consider: was the session too short, or is the workflow already well-optimized? |
| Improvement breaks verification | Revert the improvement. Re-analyze the approach — the improvement may need a different implementation strategy. |
| User declines execution | Document the improvement as a TODO comment in the relevant file, or create an RFC for larger improvements. |
| Too many improvements found | Don't try to do everything. Execute only the highest-priority one. Document the rest for future sessions. |
| Improvement requires RFC | Use `domain-feature-design` skill to create the RFC. Don't implement without proper design for significant changes. |
