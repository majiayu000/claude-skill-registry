---
name: ship-loop
description: 'Bot-paired fast-lane cycle for coherent-arc internal PRs (one closable bead or small-epic slice): claim → test → impl → pre-push → push → squash auto-merge → close.'
practices:
- continuous-delivery
- xp
- tdd
- bdd
- pragmatic-programmer
hexagonal_role: driving-adapter
consumes:
- beads
- rpi
- post-mortem
produces:
- git-changes
- merged-prs
context_rel:
- kind: customer-of
  with: rpi
- kind: customer-of
  with: post-mortem
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: execution
  dependencies:
  - beads
  - rpi
  stability: experimental
  triggers:
  - ship loop
  - ship this
  - fast lane PR
  - land a small fix
  - bot-paired PR
  - close a harvested item
output_contract: merged PR on origin/main + closed bead
---

# /ship-loop — Bot-paired fast lane PR cycle

> **Lane choice:** use this skill for **coherent-arc internal PRs** — one closable bead, or one small-epic slice (≤5 child beads of the same surface), with paired tests. The PR is the *atomic-revert unit*: bundle scenarios that ship-or-revert together; split scenarios with independent rollback. For fork-based OSS contributions, use the `/pr-*` family (`pr-research`, `pr-plan`, `pr-implement`, etc.; tier `contribute`). For large epics (15+ child beads) or multi-wave work, use `/crank`. See `CLAUDE.md ## Workflow` for the canonical unit-of-PR rule.

Capture of the discipline that landed 8/9 internal PRs in the 2026-05-18 session at 19.5-min median time-to-merge. Five named failure modes (F1–F5); four closed mechanically. The full rationale lives in [`docs/learnings/2026-05-18-xp-bdd-tdd-workflow-synthesis.md`](https://github.com/boshu2/agentops/blob/main/docs/learnings/2026-05-18-xp-bdd-tdd-workflow-synthesis.md).

## Overview / When to Use

Run this skill at the START of each PR you intend to ship to your own `main` branch. The skill enforces the cycle as a sequence; each step has a clear done-state and gate.

**Pair partner:** `claude-review` (GitHub App workflow at `.github/workflows/claude.yml`) auto-fires on `pull_request: opened/synchronize`. No `@claude` mention is required. Operator does the edits; bot does the review check.

## The 9-step cycle

1. **Claim.** `bd ready` → pick the highest-severity unblocked item, OR read `.agents/rpi/next-work.jsonl` for harvested follow-ups. **`bd update <id> --claim`** atomically.
2. **Branch off fresh main.** `git checkout main && git pull --rebase`. Then `git checkout -b <type>/<slug>-<bead-id>`. NEVER stack off a sibling branch; auto-merge handles serialization via update-branch.
3. **Write the FIRST FAILING TEST.** BDD scenario (Gherkin) for behavior; unit test for invariants. The test must fail for the *right reason* (asserting expected behavior, not just "doesn't crash"). See [references/test-shape.md](references/test-shape.md).
4. **Minimal implementation.** Smallest code change that makes the test green. Resist scope creep. Refer to the project's standards (`.claude/rules/{go,python}.md`).
5. **`scripts/ship.sh`** (recommended) — auto-detects inventory-touching changes and runs the regen sweep (sync-skill-counts, codex-hashes, domain-map, context-map, registry, sync-hooks) preemptively. **This is the mechanical fix for anti-pattern #1** — removes the operator's choice to skip the rule. CI (`.github/workflows/validate.yml`) is the sole authoritative push gate per `docs/contracts/local-pre-push-gate-retirement.md` (soc-g2r9, PR #357); the previous `scripts/pre-push-gate.sh` local mirror was retired because per-incident drift cost dominated the per-push wait. For per-tool sanity before push, run only what your diff touches: `cd cli && make test`, `bats tests/scripts/<file>.bats`, `scripts/regen-codex-hashes.sh`. If a pre-existing blocker appears in unchanged-from-base content (visible in CI now), **file an atomic side-quest fix PR first** — don't bundle. See [references/anti-patterns.md](references/anti-patterns.md). **For PRs that change gate/validator/CI behavior**: capture the targeted output line and include it verbatim in the PR body as `Evidence:`; the `validate-pr-evidence-claims` CI job (`scripts/verify-gate-claim.sh`, soc-o5kq + soc-eqjd) verifies each Evidence line against the workflow run's logs and blocks the PR if any claim is absent (mechanical enforcement of anti-pattern #7).
6. **Commit with conventional-commit scope.** `feat(<scope>):`, `fix(<scope>):`, `docs(<scope>):`. Body explains the failure mode the test reproduces and how the fix removes it.
7. **Push + `gh pr create`.** Body cites the bead, the validation results, and links to the learning anchor in the script body (NOT a `.agents/learnings/` file existence — that breaks in CI's fresh clone).
8. **`gh pr merge <num> --squash --auto`.** Immediately. The bot fires `claude-review` automatically on PR open. When all required checks pass, merge fires without operator action.
9. **Close the bead.** `bd close <id> --reason "Merged via PR #<num>"`. The coherent-arc rule should keep concurrent PR count low (typically 1-2); when a large-epic split puts multiple PRs in flight against the same main, invoke [`scripts/gh-merge-chain.sh`](references/gh-merge-chain.md) on the chain.

## Gate sequence (what each enforces)

| Gate | Enforces |
|---|---|
| Per-tool local checks (optional) | `cd cli && make test` for Go; `bats tests/scripts/<file>.bats` for shell; `scripts/regen-codex-hashes.sh` for codex parity. Run only what your diff touches. |
| `claude-review` (auto on PR open) | Reviewer pair — the bot half |
| `.github/workflows/validate.yml` | **Sole authoritative push gate** (soc-g2r9, PR #357). 60+ job suite on PR head: cli-docs-parity, embedded-sync, skill-frontmatter, registry-check, security-toolchain, validate-pr-evidence-claims (AP#7), plus the F-mode closures |
| `gh pr merge --squash --auto` | Auto-merge when all required checks pass |
| `scripts/gh-merge-chain.sh` (optional) | Chain N PRs through auto-merge with `update-branch` on each successor when a predecessor merges (closes F3) |

## Failure-mode mapping

| ID | Failure | Mechanical guard |
|---|---|---|
| **F1** | Script rewrite leaves dead variables; `--fast` shellcheck misses them | Unconditional shellcheck on staged `.sh` (PR #326) |
| **F2** | Pre-existing blocker compounds across concurrent branches | **Open.** Rule: fix as an atomic side-quest PR FIRST; don't bundle. See [references/anti-patterns.md](references/anti-patterns.md). |
| **F3** | `gh pr merge --auto` doesn't auto-rebase BEHIND branches | `scripts/gh-merge-chain.sh` (PR #329) |
| **F4** | Bot trigger doc claimed mention-only; actual trigger is auto on PR open | Doc corrected (PR #327) |
| **F5** | Stale `~/.config/evolve/KILL` silently blocks /evolve | `EVOLVE_KILL_TTL_DAYS=7` auto-expire (PR #328) |
| **meta** | Tests assert local-only file existence; fail in CI | `grep -q '<slug>' "$SCRIPT"` instead of `[ -f .agents/learnings/<x>.md ]`. See [references/test-shape.md](references/test-shape.md). |

## Anti-patterns

Read [references/anti-patterns.md](references/anti-patterns.md) for the full list with examples. Headline anti-patterns:

1. **Running `--fast` pre-push on an inventory-touching PR** — new skill, contract, or schema → use FULL gate; `--fast` skips ~15 inventory validators
2. **Bundling pre-existing fixes** — file each as its own atomic PR
3. **Keeping copied variables after a rewrite** — after a script rewrite, the first self-check is "are all variable declarations used?"
4. **Asserting local-only state in CI tests** — grep the reference, don't check the file
5. **Branches off out-of-date main** — `git checkout main && git pull --rebase` at branch creation
6. **Skipping the failing-test-first step** — adding a test after the fix gives false confidence

## Session scope (sister rule to coherent-arc)

Coherent-arc governs the *shape* of a single PR; session-scope governs the *count* of consecutive PRs in an autonomous session.

- **Default: 2-4 PRs per autonomous session.** Both arcs ship cleanly and merge.
- **≥5 PRs in flight or merged in one session triggers a mandatory post-mortem before continuing.** Diminishing returns and reactive-PR spirals (PR-fixes-fallout-from-prior-PR) are the dominant failure mode in the back-half of long sessions.
- **Post-mortem shape (1-2 sentences each):** Which PRs were planned vs reactive? How many self-corrections? Was the marginal PR discovery or churn?

**Derivation:** the 2026-05-19 cron-loop session shipped 6 PRs with 3 self-corrections; PRs #5–#6 each fixed fallout from #1–3. Visible reactivity by PR #5; the cron-loop kept nudging "keep going" without surfacing the post-mortem signal. Mechanical enforcement ships as `hooks/session-pr-counter.sh` — a PreToolUse Bash hook on `gh pr create` that fires at `count >= threshold-1` (default 5) and emits the post-mortem prompts via `additionalContext`, with optional hard-block via `AGENTOPS_SESSION_PR_BLOCK=1` (soc-1aou, PR #362). (soc-waxr)

## Pair mechanics (claude-review)

- `claude-review` fires automatically on `pull_request: opened` and `synchronize`. No `@claude` mention required.
- If `claude-review` is `IN_PROGRESS`, wait — don't poke. The bot does NOT respond to its own comments (anti-loop protection).
- If `claude-review` is silent after PR open, the workflow may need permission upgrades (see `docs/contracts/claude-bot-delegation.md` Gotchas 1-4) — surface to operator, do not retry.
- If you hit the self-revert loop (PR #270 case — bot reverting its own forward-port of `claude.yml`), rebase the branch locally onto fresh main and force-push.

## Examples

**Closing a harvested next-work item:**

```
1. /post-mortem ran; .agents/rpi/next-work.jsonl has an unclaimed "medium" item
2. /ship-loop picks the item: branch fix/<slug>-<bead> off main
3. Write the failing test that proves the failure mode exists
4. Add the minimal fix
5. Pre-push --fast → green
6. Push → gh pr create → gh pr merge --squash --auto
7. claude-review auto-runs; validate.yml runs; auto-merge fires
8. bd close <id>
```

**Shipping a chain of PRs:**

```
1-9. Run the cycle for each PR (off main, not stacked)
10. After all PRs are open with auto-merge enabled:
    scripts/gh-merge-chain.sh <pr1> <pr2> <pr3>
11. Helper polls + update-branches each successor as the predecessor merges
```

See [references/examples.md](references/examples.md) for full walkthroughs.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Auto-merge stalls | `claude-review` IN_PROGRESS or branch BEHIND | Wait for review; if BEHIND, `gh api repos/<o>/<r>/pulls/<n>/update-branch -X PUT` or use `gh-merge-chain.sh` |
| `claude-review` never fires | Workflow lacks trigger or perms | Check `.github/workflows/claude.yml` `on:` block and permissions; may require `workflows: write` upgrade |
| Pre-push --fast blocks on unchanged content | Pre-existing F2-class blocker | File the fix as an atomic side-quest PR first; rebase your branch onto the side-quest's merge |
| Self-revert loop on a stale branch | Bot reverting its own forward-port | Rebase locally onto fresh main; force-push with `--force-with-lease` |
| Test asserts local file in CI | `.agents/` is gitignored | Change to `grep -q '<slug>' "$SCRIPT"` (reference assertion, not file existence) |

## See Also

- [pr-implement](../pr-implement/SKILL.md) — fork-based OSS contribution (different tier; different use case)
- [crank](../crank/SKILL.md) — multi-wave epic execution
- [rpi](../rpi/SKILL.md) — full lifecycle orchestrator (ship-loop is the per-PR mechanics inside RPI's implementation phase)
- [post-mortem](../post-mortem/SKILL.md) — harvests next-work items that ship-loop consumes
- [beads](../beads/SKILL.md) — task tracker that drives the claim step

## References

- [references/anti-patterns.md](references/anti-patterns.md)
- [references/examples.md](references/examples.md)
- [references/gh-merge-chain.md](references/gh-merge-chain.md)
- [references/test-shape.md](references/test-shape.md)
- Durable rationale: [docs/learnings/2026-05-18-xp-bdd-tdd-workflow-synthesis.md](https://github.com/boshu2/agentops/blob/main/docs/learnings/2026-05-18-xp-bdd-tdd-workflow-synthesis.md)
