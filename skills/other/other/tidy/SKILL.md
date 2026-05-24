---
name: tidy
description: ODIN's compress-operations dispatcher under the Compressor/Extender role. Invoke on "tidy", "clean up", "tidy this file/memory/workspace/git/docs", or when active context (current file, diff, stack, memory directory) has structural rot to resolve before touching behavior. Detects target domain from context and routes to the sibling skill. Requires explicit target or clear active-context signal — do not invoke speculatively.
---

# Tidy — ODIN's compress-operations dispatcher

Compress first. Before adding complexity, reduce coupling. Before changing behavior,
improve structure. This skill detects *what* needs tidying from context and routes
to the right sibling skill. Domain procedures live in the siblings — this skill
owns only scope detection, dispatch, and the output contract.

**Invariants:**
- Every tidy action is atomic and scoped to what is already in view.
- Tidy commits are always separate from behavior commits.
- No opportunistic sweeps beyond the declared or clearly active scope.

---

## Scope detection

Inspect context in priority order and dispatch to the first matching domain:

| Signal | Domain | Dispatch to |
|---|---|---|
| File path(s), active diff, or `cargo`/`dune` target named | **Code** | `cleanup-codebase` skill |
| `memory/` directory, `MEMORY.md`, or memory file(s) named | **Memory** | `memory-clean` then `memory-update` skills |
| `.outline/`, `/tmp` scratch, `*.tmp`, `*.bak`, repomix packs | **Workspace** | Inline (see below) |
| `git sl`, commit stack, commit message(s) named | **Git** | `git-branchless` skill + `atomic-commit` skill |
| Docs, comments, ADRs, READMEs, plan files named | **Docs** | Inline (see below) |
| User explicitly says "tidy ICM" or names an ICM topic | **ICM state** | Inline (see below) |
| No clear signal | — | Ask: "What are we tidying — code, memory, workspace, git, docs, or ICM?" |

---

## Inline procedures (workspace, docs, and ICM state)

These three domains are handled inline without a dedicated sibling skill.

### Workspace

1. Discover scratch artifacts in scope:
   ```sh
   fd -t f -E '.git' -E 'target' -E '_build' \
     '(\.(tmp|bak|outline)|repomix-output)' .
   fd -t f /tmp -g '<session-prefix>-*' 2>/dev/null
   ```
2. Confirm each is truly scratch (not referenced by any open plan, task, or active diff).
3. Remove with `rip` (not `rm`). Report count and paths.

### Docs

1. Scan in-scope file(s) for: stale `TODO`/`FIXME` (git-blame date > 6 months), comments contradicting current code, commented-out code blocks, multi-paragraph docstrings on non-API-surface functions, overclaims about external contracts.
2. Show the current text + proposed change for each candidate. Edit only on confirmation or for purely cosmetic fixes (whitespace, spelling).
3. Overclaims: annotate with `<!-- VERIFY -->` and surface to the user rather than deleting.

### ICM state

Run `icm list --sort recent | head -30`; for each stale entry show the current content plus the proposed replacement before calling `icm update`. For decisions made in this session not yet captured, show the proposed `icm store` call before executing. Write only on explicit user confirmation per entry.

---

## Output contract

After completing each domain, emit exactly:

```
Tidy — <domain>
  Removed:   N  (up to 5 paths/names; "…and M more" if larger)
  Fixed:     N
  Proposed:  N  (awaiting confirmation)
  Skipped:   N  (<one-phrase reason>)
  Next:      <one sentence, e.g. "Run build to verify" or "Nothing else in scope">
```

If nothing needed tidying: `Tidy — <domain>: nothing to do.`

---

## Constitutional rules

1. **Atomic commits** — tidy commits are always separate from behavior commits. No exceptions. Use `git move --fixup` when embedding alongside active work.
2. **Scope discipline** — never tidy beyond the explicit target or the currently active file/system. No opportunistic sweeps.
3. **Confirm before delete** — show evidence; never silently remove memories, commits, or files.
4. **No new abstractions** — tidying is net-deletion or net-simplification only. Introducing a new pattern is a separate task.
5. **Verify after** — after code or git tidy, run repo-native verification (build + tests + linter).
6. **ODIN baseline wins** — if any rule here conflicts with `~/.claude/claude/system-prompt-baseline.md`, the baseline wins.
