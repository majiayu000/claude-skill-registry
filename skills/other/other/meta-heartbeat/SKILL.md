---
version: 1.0.0
name: meta-heartbeat
description: >
  Session startup ritual that loads context files, creates daily memory,
  checks for stale context, and surfaces documentation status. Runs
  automatically at the start of every session, or invoke manually with
  /meta-heartbeat to re-initialize context. Does NOT trigger for mid-session work.
disable-model-invocation: true
---

# Heartbeat — Session Startup

Execute the following steps in order. Do not skip steps. Do not ask permission.

## Step 1: Load Identity

1. Read `context/SOUL.md` — who you are, how you behave
2. Read `context/USER.md` — who you're helping and their preferences

## Step 2: Load Memory

3. Read `context/MEMORY.md` — long-term curated knowledge (main sessions only)
4. Read today's daily file: `context/memory/{YYYY-MM-DD}.md`
5. Read yesterday's daily file: `context/memory/{yesterday's date}.md`

If either daily file doesn't exist, that's fine — skip it silently.

## Step 3: Load Workflow Config

6. Read `workflow.json` if it exists — note the docs repo name and project type
7. If `workflow.json` exists, this is a workflow-enabled project:
   - Resolve the docs repo path: if `docsRepo` is `"."` this IS the docs repo;
     otherwise run `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>`
     to find the actual path (works in bare+worktree, agentsandbox, and normal clones)
   - Note the resolved docs repo path for later reference
   - Skills that generate documents will output to the docs repo
   - The `docs.output` paths in workflow.json are relative to the resolved docs repo root

## Step 4: Create or Append Daily Memory

8. If `context/memory/{YYYY-MM-DD}.md` does not exist, create it:

```markdown
# {YYYY-MM-DD}

## Session 1 — {HH:MM}

### Goal
[Pending — awaiting user goal]
```

If it already exists (second+ session today), append a new session header:

```markdown

## Session {N} — {HH:MM}

### Goal
[Pending — awaiting user goal]
```

## Step 5: Freshness Check

9. Check modification dates on all files in `context/`:
   - If any file is older than 30 days, flag it:
     "Your [filename] is from [date]. Want to refresh, or keep going?"
   - If `context/memory/` has daily files older than 30 days that aren't archived,
     suggest archiving them to `context/memory/archive/`.

## Step 6: Documentation Status (if workflow-enabled)

10. If `workflow.json` exists and has a `docsRepo` path:
    - Check what docs were recently created or modified in the docs repo
      (last 7 days: ADRs, RFCs, design docs, etc.)
    - Check recent session notes for decisions that might need an ADR
    - If any recent decisions lack a corresponding ADR, note it:
      "Decision from [date] about [topic] — should this be an ADR?"
    - Briefly list available document types: "You can generate PRDs, RFCs,
      ADRs, design docs, C4 diagrams, runbooks, post-mortems, and spike reports."

Only surface documentation status if there's something actionable. Don't list
document types every session — only on first session or if asked.

## Step 7: Skill Inventory

11. List available skills from `.claude/skills/` (names and one-line descriptions only).
    Note any skills that were recently added or modified.

## Step 8: Greet

12. Greet the user briefly. If recent daily files contain relevant context (open items,
    ongoing work), mention it. Keep it to 2-3 sentences max.

Example: "Morning. Yesterday you were working on the event sourcing migration —
left off at the projection rebuild. You also made a decision about caching strategy
that might need an ADR. Ready to continue, or something new?"
