# `simplify` — orchestration recipe

Dispatch shape, composition rule, Reviewer audit contract, fix sequencing, and behavior gate for the `simplify` skill. Read alongside `SKILL.md` Phase 1 / 2 / 3.

## Phase 1 — diff scope resolution (shell snippet)

```bash
# Resolve a base ref. Print "" and exit 1 if none resolves.
resolve_base() {
  for candidate in \
    "$(git merge-base HEAD origin/main 2>/dev/null)" \
    "$(git merge-base HEAD origin/master 2>/dev/null)" \
    "$(git merge-base HEAD main 2>/dev/null)" \
    "$(git merge-base HEAD master 2>/dev/null)" \
    "$(git rev-parse '@{upstream}' 2>/dev/null)"; do
    if [ -n "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

# Primary path.
if base="$(resolve_base)"; then
  diff="$(git --no-pager diff "$base")"
elif git rev-parse --verify HEAD >/dev/null 2>&1; then
  if git rev-parse --verify 'HEAD^' >/dev/null 2>&1; then
    # Committed history exists, no base resolves -> abort.
    printf 'simplify: committed history exists but no base ref resolves\n' >&2
    printf '  re-invoke with explicit base: simplify against <ref>\n' >&2
    exit 2
  else
    # HEAD is the root commit -> working tree only is the full scope.
    printf 'simplify: scope: working-tree only, on root commit\n' >&2
    diff="$(git --no-pager diff HEAD)"
  fi
else
  # Unborn HEAD or no git context -> caller supplies files.
  diff=""
fi

# Empty diff after all valid resolutions -> exit 11.
[ -z "$diff" ] && exit 11
```

**Explicit-base override** — when the user invokes `simplify against <ref>`, the orchestrator bypasses `resolve_base` and runs `git --no-pager diff "<ref>"` directly. The `<ref>` is any revision spec git accepts (`HEAD~5`, a SHA, a branch name, a tag).

## Phase 2 — single-message dispatch shape

The orchestrator issues **one** tool-call message containing three Agent invocations — never three sequential messages. Each invocation receives a prompt built as:

```
<axis prompt from references/<axis>.md, verbatim>

---

DIFF:
<captured diff from Phase 1>
```

Independence argument the orchestrator must include in the spawn message:

> "Three agents dispatched in parallel. Axes are disjoint by construction: reuse-axis owns Graft (existing-utility detection), quality-axis owns Excess + Sprawl on code shape, efficiency-axis owns Excess + Sprawl on execution cost. All three agents are read-only; none edits files; none reads or writes shared mutable state."

Agent type for each invocation: `Explore` (read-only).

## Phase 3 — composition, audit, fix

### Composition

After all three findings lists return, merge by `{file, line}`. Tag each finding with its axis. When two axes report the same `{file, line}` with structurally identical patterns, deduplicate — keep the finding once, attribute to the first reporter, note the second axis as a co-signer.

### Reviewer audit (single adjudication authority)

Dispatch a Reviewer agent (also `Explore`-typed, read-only) with:
- the composed findings list,
- the original diff,
- the axis prompts from `references/{reuse,quality,efficiency}.md`.

Reviewer audit charter — four checks:
1. **Completeness** — did the three axes between them cover every diff hunk that warrants attention? Flag systematic blind spots.
2. **Consistency** — do any findings contradict each other (e.g., "extract this into a helper" vs "inline this helper")? Flag and resolve.
3. **Accuracy** — for each finding, verify the citation. Discard findings whose `path:line` does not match the diff or whose `existing-utility` does not exist.
4. **Scope** — flag findings that propose changes outside the diff's blast radius. Discard.

The Reviewer's output is the **validated survivor set**. The orchestrator applies survivors and drops non-survivors — no re-litigation in either direction.

If the survivor set is empty after a non-empty raw findings list, exit 12.

### Fix sequencing

Group survivors by `rejection-ground`. Apply in this order — one atomic commit per class:

1. **Graft commit** — apply all reuse-axis survivors (and any other axis survivors flagged `rejection-ground: graft`).
2. **Excess commit** — apply all quality-axis + efficiency-axis survivors flagged `rejection-ground: excess`.
3. **Sprawl commit** — apply all quality-axis + efficiency-axis survivors flagged `rejection-ground: sprawl`.

Each commit body carries `Op: compress` per the SKILL.md "Op trailer present" gate. Commit message format follows the ODIN baseline `<git>` charter (`<type>(scope): <description>`); recommended:

```
refactor(simplify): remove <class> from <scope>

<2-4 lines describing the survivors applied in this commit, citing
file:line pairs>

Op: compress
```

A commit that would bundle survivors from more than one class is split before merge (exit 15).

## Behavior gate (after every commit)

After each fix commit, run the repo-native verifier per the matrix in `fix/references/verifiers.md` — typically `just test`, `cargo test`, `pytest`, `npm test`, `dune runtest`, or the equivalent for the current language. On red:

```bash
git revert HEAD --no-edit
```

Surface the failure mode (exit 13) and stop the simplify run for the affected commit. Other class commits already landed remain.

## Post-fix audit (no new rejection ground)

After the final commit, audit the simplify patch itself against `~/.claude/claude/system-prompt-baseline.md` `<reject_patches>` — Excess / Graft / Sprawl. Any hit → revert the entire simplify chain via `git revert <first-simplify-commit>..HEAD --no-edit` and exit 14. The orchestrator may re-plan and re-invoke.

## Exit code summary (matches SKILL.md)

| Code | Trigger |
|---|---|
| 0 | Survivors applied, behavior gate green, no new rejection ground |
| 11 | Empty diff after all Phase 1 resolutions |
| 12 | Survivor set empty after Reviewer audit |
| 13 | Behavior gate red on a fix commit — that commit reverted |
| 14 | Post-fix audit caught a new rejection ground — chain reverted |
| 15 | Mixed-class commit detected — split required before merge |
