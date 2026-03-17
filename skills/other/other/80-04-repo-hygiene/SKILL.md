---
name: 80-04-repo-hygiene
description: Deep audit and cleanup of repository clutter — stale worktrees, dead branches, orphan files, legacy artifact directories, disk hogs, and convention violations. Use when a repo feels messy, when disk space is low, or when asked to clean up / maintain a repository.
---

# 80.04 Repo Hygiene

Audit a repository for clutter, stale artifacts, and convention violations, then present an evidence-backed cleanup plan for human approval.

## When to Use

- Repository feels cluttered or disorganized
- Disk space is low and repo is suspiciously large
- Before open-sourcing or sharing a repo
- Periodic maintenance (monthly/quarterly)
- User asks to "clean up", "maintain", or "audit" a repo

## Process Overview

1. **Phase 1: Fast Survey** — Inventory everything in seconds
2. **Phase 2: Deep Oracle Dig** — Parallel agent investigates each suspect with evidence
3. **Phase 3: Present Report** — Evidence-backed table with classifications
4. **Phase 4: Execute** — On human approval, run cleanup commands

---

## Phase 1: Fast Survey

Run a quick inventory of the target repo. Collect raw data, do not classify yet.

```bash
cd <repo-root>

# Identity
git rev-parse --show-toplevel
git remote -v

# Worktrees
git worktree list

# Branches
git branch -a -v
git branch --merged main
git branch --no-merged main

# Git status
git status --short
git ls-files --others --exclude-standard

# Root files
ls -1

# Disk hogs
du -sh . target/ node_modules/ .worktrees/*/ 2>/dev/null

# Stale remote refs
git remote prune origin --dry-run 2>&1
```

Collect all output. Identify suspect items for Phase 2.

---

## Phase 2: Deep Oracle Dig

Delegate a single oracle worker to investigate ALL suspect items. The oracle MUST investigate each item with the full checklist — not guess by filename.

### Dispatch Template

Use `teams` to delegate:

```
teams(action: 'delegate', useWorktree: false, tasks: [{
  text: '<oracle prompt below>',
  assignee: 'oracle-repo-audit'
}])
```

### Oracle Prompt

Construct the oracle prompt with:

1. **Repo path** — absolute path
2. **Survey data** — paste ALL Phase 1 output
3. **Suspect items list** — every file, dir, worktree, branch that needs investigation
4. **The investigation checklist** (below)

### Investigation Checklist (per item)

For EACH suspect file or directory, the oracle MUST:

1. **Read actual content** — first 50 lines for files, `ls -la` for directories
2. **Check git history** — `git log --oneline -5 -- <path>` — when added, by whom, why
3. **Check if tracked** — `git ls-files <path>` — tracked or gitignored?
4. **Search for references** — `rg -l '<name>' --glob '!target' --glob '!node_modules'` — is anything using it?
5. **Check size** — `du -sh <path>`
6. **Compare duplicates** — if two similar items exist (e.g. justfile vs Makefile), diff them
7. **Classify** with evidence:
   - `SAFE_DELETE` — no references, gitignored or stale, evidence clear
   - `ARCHIVE_THEN_DELETE` — has value but superseded or obsolete
   - `NEEDS_HUMAN_DECISION` — active or ambiguous, provide context
   - `KEEP` — actively used, referenced, or essential
   - `CONVENTION_FIX` — not delete but needs restructuring

For worktrees:
1. Check if branch is merged into main
2. Check for uncommitted changes (`git status` in worktree)
3. Check target/node_modules size within worktree
4. Check last activity date

For branches:
1. Check if changes exist in main (merged, cherry-picked, squash-merged)
2. Check last commit date and age
3. Check for open PRs (`gh pr list` if available)

### Mandatory Audit Categories

The oracle MUST check for ALL of these, even if not in the initial suspect list:

#### Legacy Artifact Directories
Flag any of these directories — they should be `tk` tickets instead:
- `.oracle/` → should be tickets tagged `research,oracle`
- `.reviews/` → should be tickets tagged `review`
- `.plans/` → should be tickets tagged `plan`
- `.design-specs/` → should be tickets tagged `design-spec`
- `docs/postmortems/` → should be tickets tagged `postmortem`
- `docs/research/` → should be tickets tagged `research`

For each found: list contents, check if equivalent tickets exist, recommend migration path.

#### Disk Hogs
- `target/` (Rust), `node_modules/`, `.next/`, `dist/`, `build/` — in main repo AND all worktrees
- Database dumps, backups, large binary files
- Docker volumes / data directories

#### Convention Violations
- `config.toml` tracked alongside `config.template.toml` (local config should be gitignored)
- Duplicate build systems (justfile + Makefile, package.json scripts + Makefile)
- `.env` files tracked (should be gitignored with `.env.example` tracked)
- Lock files missing or extraneous

#### Root Clutter
- One-off test/debug scripts
- Evaluation/benchmark result files
- Backup files (`*.backup`, `*.bak`, `*.old`)
- Implementation plans, migration docs that belong in docs/ or tickets
- Empty directories

#### Stale Tickets
- Untracked `.tickets/` files
- Modified `.tickets/` files not committed
- `in_progress` tickets with no recent activity

### Second-Pass Check

After the main investigation, the oracle MUST do a second pass:

1. **Cross-reference findings** — did any "KEEP" item reference a "SAFE_DELETE" item?
2. **Check for orphaned chains** — if deleting X, does Y become orphaned?
3. **Verify no false positives** — re-read any item classified SAFE_DELETE that is git-tracked
4. **Size audit** — do the individual sizes add up to the total? Any hidden disk hogs missed?
5. **Pattern check** — are there categories of clutter not covered by the initial suspect list?

---

## Phase 3: Present Report

The oracle creates a ticket (tagged `research,oracle,maintenance`) with findings organized as:

### Report Structure

```markdown
# Repo Hygiene Audit: <repo-name>

## 1. IMMEDIATE SAFE DELETES
Per item: what, evidence, size, delete command

## 2. CONVENTION FIXES
Per item: what's wrong, what it should be, fix command

## 3. LEGACY ARTIFACT MIGRATION
Per directory: contents summary, recommended tk ticket tags, migration steps

## 4. ARCHIVE THEN DELETE
Per item: what, why archive first, size, commands

## 5. NEEDS HUMAN DECISION
Per item: what, context, options with trade-offs

## 6. KEEP
Per item: brief justification

## 7. DISK RECOVERY SUMMARY
Table: item | size | classification
Totals: immediate | with approval | total potential

## 8. CLEANUP COMMANDS
Ready-to-run bash script, split into:
- Safe (no confirmation needed)
- Needs confirmation (commented out)
```

---

## Phase 4: Execute

Present the report to the human. On approval:

1. Run safe deletes first
2. Ask about each human-decision item
3. Run convention fixes
4. Commit any tracked changes (`.gitignore` updates, file moves)
5. Report final disk recovery

Never execute cleanup without human approval. The report IS the deliverable — execution is optional.
