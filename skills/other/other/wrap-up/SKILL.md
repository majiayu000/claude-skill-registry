---
name: wrap-up
description: End-of-session routine — commit, memory review, self-improvement. Run before closing terminal.
user-invocable: true
disable-model-invocation: true
---

# Session Wrap-Up

Run three phases in order before ending the session. Auto-apply all changes without asking. Present a consolidated report at the end.

**When to run:** Before closing terminal, ending a work session, or when you're done for the day. Runs BEFORE the automatic Stop hooks (evaluate-session.sh) fire.

## Phase 1: Ship It

**1.1 Commit check:**
- Run `git status` — if uncommitted changes exist:
  - Stage relevant files (NOT `.env*`, credentials, or generated files)
  - Commit with descriptive message following `<type>: <description>` convention
  - Push to remote

**1.2 File placement check:**
- If any files were created this session, verify they follow naming conventions from `.claude/rules/conventions.md`
- Auto-fix misplaced files (e.g., docs in src/, skills without SKILL.md)

**1.3 Task cleanup:**
- If beads tasks were worked on: `bd update <id> --append-notes "session wrap-up: <status>"`
- If task is complete: `bd close <id>`
- If task has remaining work: note what's left in the update

**1.4 Worktree check:**
- If the current worktree's feature branch is fully merged, remind user to clean up:
  ```
  Worktree cleanup available: git worktree remove ~/worktrees/property-tracker/<name>
  ```

## Phase 2: Remember It

Review what was learned during the session. Use this decision framework:

| Knowledge Type | Destination | Example |
|---------------|-------------|---------|
| Permanent project convention | `CLAUDE.md` or `.claude/rules/` | "Always use writeProcedure for mutations" |
| Scoped to specific file types | `.claude/rules/<topic>.md` with relevant path context | "Drizzle v0.45 requires .returning()" |
| Pattern Claude discovered | Auto memory (`~/.claude/projects/.../memory/`) | "This API returns 403 without User-Agent" |
| Personal/ephemeral context | `CLAUDE.local.md` (not committed) | "Currently debugging the billing webhook" |
| Duplicates existing content | Skip — or add `@import` reference | Already in anti-patterns.md |

**Actions:**
1. Check if any debugging insights, user corrections, or conventions should persist
2. If something belongs in auto memory, update `MEMORY.md` (keep under 200 lines)
3. If a CLAUDE.md rule is needed, add it to the appropriate scoped file
4. **Staleness check:** Scan MEMORY.md for references to PRs, branches, files, or features that may be stale. Look for:
   - PR references — check if merged/closed with `gh pr view <num> --json state`
   - Branch references — check if branch still exists with `git branch -a | grep <name>`
   - "IN PROGRESS" items — verify if actually still in progress or completed
   - File paths — spot-check 2-3 referenced paths still exist
   - Mark stale entries for cleanup or update them
5. If nothing worth persisting: say "No new learnings to persist"

## Phase 3: Review & Apply

Analyze the conversation for self-improvement findings. If the session was short or routine, say "Nothing to improve" and skip to the report.

**Focus areas (in priority order):**

1. **Mistakes & near-misses** — What went wrong? What took multiple attempts? What did the user have to correct? *(Most valuable — don't skip this)*
2. **Friction** — Repeated manual steps that should be automatic
3. **Skill gaps** — Things Claude struggled with or got wrong
4. **Automation candidates** — Repetitive patterns that could become skills or hooks

**For each finding, auto-apply:**

| Finding Type | Action |
|-------------|--------|
| Convention Claude didn't know | Add to appropriate `.claude/rules/` file |
| Recurring manual step | Note as skill/hook candidate in `~/.claude/projects/.../memory/` |
| Debugging insight | Save to auto memory |
| User preference discovered | Add to auto memory |

**Conflict check:** Before adding any new rule or instinct, search existing rules and instincts for contradictions. If "always do X" already exists and you're about to add "never do X in context Y", explicitly note the scoping difference.

**Report format:**

```
## Wrap-Up Report

### Ship It
- [x] Committed: <commit hash> "<message>"
- [x] Pushed to origin/<branch>
- [ ] No beads tasks active

### Remember It
- [x] Added "<insight>" to auto memory
- [ ] No CLAUDE.md updates needed

### Review & Apply
Applied:
1. ✅ Near-miss: <description> → [destination] Added <what>
2. ✅ Friction: <description> → [destination] Added <what>

No action needed:
3. Already documented in anti-patterns.md

### Session Stats
- Duration: ~Xh
- Files modified: N
- Commits: M
```

## Important Notes

- This skill runs BEFORE the Stop hook. The Stop hook (`evaluate-session.sh`) will separately extract instincts from tool usage — that's complementary, not duplicative.
- Do NOT auto-commit to main/develop. Only commit to the current feature branch.
- If there are failing tests, do NOT wrap up — fix tests first or note them as blockers.
- Keep the report concise. The value is in the actions taken, not the report itself.
