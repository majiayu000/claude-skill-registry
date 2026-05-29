---
name: simplify
description: Review changed code along three axes — reuse, quality, efficiency — via parallel agents, then apply compress-op fixes. Use when the user says "simplify this diff/PR/branch", "tighten up", "compress these changes", or wants axis-decomposed simplification of a specific change-set; distinct from cleanup-codebase (opportunistic while-touching-nearby) and review (read-only, no fixes).
metadata:
  short-description: Three-axis compress pass on a diff
---

# Simplify — axis-decomposed compression pass on a diff

A deliberate `compress` op invoked on a specific change-set. Decompose simplification into three axes that fail independently and so can be reviewed independently: **reuse** (what already exists), **quality** (shape of the new code), **efficiency** (cost of the new code). Three parallel read-only review agents — one per axis — emit findings against the same diff; the orchestrator composes, audits, and applies fixes one rejection-ground class per atomic commit.

The three axes map directly onto ODIN's rejection grounds. **Reuse axis** primarily detects **Graft** (new code grafted where a utility already exists). **Quality axis** primarily detects **Excess** (unnecessary surface — params, state, comments-of-what) and **Sprawl** (structure without functional cause — wrappers, ladders, copy-paste variants). **Efficiency axis** primarily detects **Excess** (work that need not happen) and **Sprawl** (structure that bloats hot paths). The op-cell is `compress` and the patch rule is Minimal Sufficient Change: behavior is preserved, entropy is reduced.

**Axis prompts (verbatim, copy-pasteable):**
- `references/reuse.md` — Agent 1 prompt, three rules, Graft focus
- `references/quality.md` — Agent 2 prompt, eight patterns, Excess + Sprawl
- `references/efficiency.md` — Agent 3 prompt, seven patterns, Excess + Sprawl
- `references/orchestration.md` — single-message dispatch recipe, composition, Reviewer audit, fix-sequencing

## Mandates, not suggestions

1. **The op-cell is `compress`.** Every commit body carries `Op: compress`. Behavior preservation is a gate, not a guideline.
2. **Decompose by axis, never by file.** All three agents see the same diff and bring different lenses. Splitting the diff by file across agents defeats the design.
3. **The Reviewer audit is the single adjudication authority.** Review agents emit findings; the Reviewer validates them; the orchestrator applies the survivors. The orchestrator does not re-litigate findings the Reviewer accepted, and does not rescue findings the Reviewer rejected.
4. **Three agents in one tool-call message.** Sequential dispatch invalidates the parallel-launch contract.
5. **A simplify patch that introduces a new rejection ground is a regression.** Post-fix, audit against Excess / Graft / Sprawl per `~/.claude/claude/system-prompt-baseline.md` `<reject_patches>`. Any hit → revert and re-plan.

## When to Apply

- The user says "simplify this diff / PR / branch", "tighten up", "compress these changes", or asks for an axis-decomposed pass over a change-set.
- A diff exists and exceeds the trivial threshold (>30 LOC or >2 files) — enough surface area for axis decomposition to pay rent.
- The change just landed and is being compressed before merge.

## When NOT to Apply

- **Empty diff** after all fallbacks — exit 11, pass-through.
- **Single file <50 LOC** with an obvious shape problem — just edit directly.
- **Opportunistic cleanup while touching nearby code** — that is `cleanup-codebase`'s territory.
- **Public API removal with migration** — that is `refactor-break-bw-compat`'s territory.
- **Read-only assessment, no fix authorization** — use `review`.
- **Fix driven by an external verifier failure or findings file** — use `fix`. `simplify` is self-sourcing.

## Workflow

1. **Phase 1 — Detect diff scope.** The diff must capture **all branch state under review** — every commit since the branch diverged from its base, plus staged, plus unstaged. The orchestrator does not guess the base; it resolves an explicit anchor, or errors. Resolve via the first base ref that exists, then run `git diff <base>` (no `..HEAD`, so working-tree changes are included):
   1. `git merge-base HEAD origin/main`
   2. `git merge-base HEAD origin/master`
   3. `git merge-base HEAD main`
   4. `git merge-base HEAD master`
   5. `@{upstream}` (the branch's configured upstream tracking ref, full divergence)

   If none of the five resolve, gate the working-tree-only fallback on **two ordered checks** — first that HEAD exists as a commit at all, then that it has no parent:
   - **Check A** — `git rev-parse --verify HEAD 2>/dev/null`. If it **fails**, HEAD is unborn (fresh `git init`, no commits yet). Skip `git diff` entirely and fall through to the user-named-files / no-git-context path below. Do not run `git diff HEAD` on an unborn HEAD — it errors and would mask the unborn state.
   - **Check B** — only if Check A succeeded, run `git rev-parse --verify HEAD^ 2>/dev/null`. If it **fails**, HEAD is the repo's root commit (real commit, no parent), so there is no committed history that could be silently dropped — the entire scope IS the working tree. Use `git diff HEAD`. Surface a one-line note: "scope: working-tree only, on root commit".
   - **Otherwise** — both checks succeeded, so committed history exists but no base ref resolves to anchor it. **Error explicitly**: print "committed history exists but no base ref resolves (none of origin/main, origin/master, main, master, @{upstream} found); re-invoke with explicit base: `simplify against <ref>`" and abort. Do **not** fall back to `git diff HEAD` — on a local-only `main`/`master`/`trunk`/`develop` with committed work, that would silently drop the committed work, and the scope contract requires capturing every commit since branch divergence plus staged plus unstaged.

   If there is no git context at all (no `.git/`), or HEAD is unborn per Check A, fall back to user-named files supplied in the invocation. Empty after all valid resolutions → exit 11. See `references/orchestration.md` for the exact resolution shell snippet and the explicit-base override syntax.
2. **Phase 2 — Dispatch three review agents in one message.** Single tool-call message containing three Agent invocations. Each agent receives `<axis-prompt from references/> + "\n\n---\n\nDIFF:\n" + <captured diff>`. Agents are read-only — no edits, disjoint axes, independence asserted in the spawn message. See `references/orchestration.md` for the concrete dispatch shape.
3. **Phase 3 — Audit, then apply.** Wait for all three. Aggregate findings by `{axis, file, line, rejection-ground}`; dedupe identical cross-axis findings. Dispatch a Reviewer agent to audit the composed list against completeness / consistency / accuracy / scope; the Reviewer's output is the **validated survivor set**. The orchestrator applies the survivors directly — one rejection-ground class per atomic commit (`Op: compress` trailer) — and drops non-survivors without comment. No re-adjudication in either direction. Re-run repo-native tests after each commit; on red, auto-revert via `git revert HEAD --no-edit`.

## Constitutional Rules (Non-Negotiable)

1. **Op-cell is `compress`. Behavior preservation is a gate, not a guideline.** A test regression between pre- and post-simplify is an automatic `git revert HEAD --no-edit`. No `# type: ignore`, no disabling of guards to make tests pass.
2. **The Reviewer audit is the single adjudication authority.** Review agents emit findings; the Reviewer validates them and returns the survivor set; the orchestrator applies the survivors and drops non-survivors without re-litigation in either direction. Arguing with the Reviewer's survivor set in prose is Excess.
3. **Three agents in one tool-call message.** The reuse / quality / efficiency agents are independent by construction — same diff, disjoint rejection-ground subsets, read-only. Sequential dispatch is rejected at the validation gate.
4. **One rejection-ground class per atomic commit.** Excess fixes, Graft fixes, and Sprawl fixes ride in separate commits per `~/.claude/claude/system-prompt-baseline.md` `<git>` charter "one concern per commit" rule. Mixed-class commits trip exit 15.
5. **A simplify patch that introduces a new rejection ground is a regression.** Post-commit, audit the patch itself against `<reject_patches>`. Any hit → revert and re-plan. If any rule here conflicts with `~/.claude/claude/system-prompt-baseline.md`, the baseline wins.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Diff scope detected | `git diff` (or staged / user-named fallback) produced a non-empty change-set | Yes — exit 11 if empty |
| Single-message dispatch | All three review agents launched in one tool-call message | Yes |
| Independence asserted | Spawn message documents the independence argument (disjoint axes, read-only) | Yes |
| Reviewer audit | Composed findings passed completeness / consistency / accuracy / scope check before fixes begin | Yes |
| Behavior preserved | Repo-native tests green after every fix commit | Yes — auto-revert on red, exit 13 |
| No new rejection ground | Post-fix audit shows no Excess / Graft / Sprawl introduced by the simplify patch | Yes — exit 14 |
| Atomic per class | Each commit contains exactly one rejection-ground class (Excess OR Graft OR Sprawl) | Yes — exit 15 if mixed |
| Op trailer present | Every commit body carries `Op: compress` | Yes |

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Clean — simplification landed, all fix commits green, no rejection ground introduced |
| 11 | No changes detected — diff empty after all fallbacks; pass-through, no work to do |
| 12 | False-positive-only findings — agents emitted findings but none survived the Reviewer audit; report attached, no patch needed |
| 13 | Behavior regression on a fix — tests went red; offending commit auto-reverted via `git revert HEAD --no-edit` |
| 14 | New rejection ground introduced — post-fix audit caught Excess / Graft / Sprawl in the simplify patch; reverted, re-plan required |
| 15 | Mixed-concern commit — a fix commit bundled more than one rejection-ground class; must split before merging |

## See also

- **cleanup-codebase** — opportunistic deletion of dead fields / wrappers / configs while touching nearby code. `simplify` is the deliberate axis-decomposed pass on a specific diff. Cleanup runs inside a file you already had to open; simplify runs over a change-set you intend to compress.
- **parallel-launch** — general-purpose decomposer for independent concerns. `simplify` is a specialized invocation of this pattern with a fixed three-axis decomposition (reuse / quality / efficiency). See `parallel-launch/references/delegation-scenarios.md` for the underlying parallelism rules.
- **review** — read-only assessment of the active branch; does not edit. `simplify` also applies the fixes its review agents found.
- **fix** — polymorphic iterative repair loop driven by an external failure (verifier output, findings file, bug spec). `simplify` is self-sourcing: it generates its own findings via parallel review agents and consumes them in the same skill invocation.
- **refactor-break-bw-compat** — public API removal with consumer migration. `simplify` never breaks public contracts; it is compress-only.
