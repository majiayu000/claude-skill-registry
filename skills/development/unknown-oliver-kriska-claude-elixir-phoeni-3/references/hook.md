# PreToolUse `deps-audit-gate.sh` — tiered fast-path

Phase 3 wires the audit into the hot loop: every `mix deps.get`,
`mix deps.update`, and `mix deps.compile` runs through a tiered hook
before mix actually executes. The hook must stay invisible on the
common path (sub-second), block on real risk, and never lock users out
of their own machine.

## Why tiered

A non-tiered hook would either:

- **Run the full pipeline** (30-90s) on every `mix deps.get` — unusable
  during feature work where `deps.get` runs hourly.
- **Cache the full audit** — but cache-fills are still 30-90s, and the
  first `mix deps.get` after a `mix.lock` change is the highest-anxiety
  moment.

Three tiers split the workload so each `mix deps.*` invocation pays
only for what changed:

| Tier | Budget | Work | Exit |
|------|--------|------|------|
| 0 | <200ms | lock-SHA cache lookup | 0 silent |
| 1 | <2s | bidi grep + `:git`/`:path` diff | 0 with hint, or 2 to block |
| 2 | unbounded | full Phase 2 pipeline (only `:full` mode) | 0 or 2 |

## Tier 0: cache hit

Read `.claude/deps-audit/last-run.json`. If the lock-SHA matches the
cached run AND `audit_passed: true` AND the policy mode is unchanged,
exit 0 immediately. Cost: one `shasum` + one `jq` per dep operation.

The policy-mode equality check is necessary because a user who flipped
from `false` to `:strict` between runs must not get a stale "passed"
from the warn-only era.

## Tier 1: deterministic fast rules

Only two Phase 1 rules run inline:

- **Rule 1 — bidi/RLO chars in `mix.lock`.** One `perl` scan over a
  small file. Either present or not.
- **Rule 5 — new `:git` or `:path` deps in `mix.exs`.** Git-diffs
  against `${PHX_DEPS_AUDIT_BASE:-origin/main}` to isolate ADDED
  non-Hex deps. Re-locks of existing `:git` deps are ignored.

Both rules are **zero false positive** by design and produce stable
NDJSON findings compatible with the Phase 2 differ output. If both
rules return clean, the gate prints a one-line stderr hint
("`Run /phx:deps-audit for full pipeline`") and exits 0.

Rules 2, 3, 4, 7, 8 are intentionally deferred to Tier 2 — they
require unpacking tarballs and lose the <2s budget on the very first
new package.

## Tier 2: full pipeline (opt-in only)

Tier 2 invocation is NOT chained from the hook. When `block_on_unvetted`
is `:full`, the hook still only runs Tiers 0+1, blocks on Tier 1
findings, and points the user at `/phx:deps-audit` for the full Tier 2
pipeline. Reason: hook-budget exhaustion via the Bash 600s timeout is
worse UX than an explicit "run the audit" message.

The `/phx:deps-audit` skill body owns Tier 2 — when invoked manually,
it can take 30-90s, run subagents, and update `last-run.json` so the
next hook invocation gets a Tier 0 hit.

## Policy enforcement

The hook reads `policy.block_on_unvetted` from `hex_vet.exs` (see
`deps-vet/references/hex-vet.md` for the tri-mode schema) and gates
findings accordingly:

| Mode | On Tier 1 findings |
|------|--------------------|
| `false` | Print summary, exit 0 (warn-only) |
| `:new_only` (default) | Block ONLY on rule 1 (bidi) and rule 5 (new dep). Both ARE "new" signals by definition. |
| `:strict` | Block on any Tier 1 finding |
| `:full` | Same as `:strict` for hook scope; full pipeline runs via skill body |

Override: `PHX_SKIP_DEPS_AUDIT=1 mix deps.get` bypasses the gate
entirely. The escape hatch is critical for emergency unblocks and CI
environments where the audit runs separately.

## Latency budget rationale

- **Tier 0 cache hit**: dominant case during feature work where
  `mix.lock` doesn't change between calls. Target: <200ms p95 so the
  hook is invisible to the developer.
- **Tier 1**: target <2s p95. Bidi grep on `mix.lock` is ~50ms.
  Rule 5's `git show` + `comm` against a 100-line `mix.exs` is ~200ms.
  Slowest path is git-fetch when `PHX_DEPS_AUDIT_BASE` is stale; users
  should pre-fetch in pre-commit or CI.
- **Tier 2**: explicitly unbounded; only reached on user opt-in via
  `/phx:deps-audit`.

## Failure modes

- **No `mix.lock`** → exit 0 (no deps to audit yet; first `deps.get`).
- **No `hex_vet.exs`** → mode defaults to `false` (warn-only). Hook
  still runs Tiers 0+1, prints findings as warnings, never blocks. The
  user gets visibility without the friction.
- **Corrupt `last-run.json`** → Tier 0 returns false, Tier 1 runs.
  Worst case: 2s of work, then a fresh `last-run.json` overwrites.
- **`PHX_DEPS_AUDIT_BASE` unreachable** → Rule 5 treats whole `mix.exs`
  as new (false-positive favored over silent-pass). Set the env to a
  local ref (`HEAD~1`) for offline work.

## Hook registration

In `hooks/hooks.json`, the gate runs under `PreToolUse → Bash`
alongside `block-dangerous-ops.sh`. The `if: "Bash(*mix deps.*)"`
condition keeps the script silent on non-deps commands — the script
itself also re-checks the command, defense-in-depth.

```json
{
  "type": "command",
  "if": "Bash(*mix deps.*)",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/deps-audit-gate.sh",
  "timeout": 5,
  "statusMessage": "Tiered deps audit..."
}
```

The 5-second timeout caps Tier 1 hard. If the hook itself runs over,
the exit code propagates as "hook failed" — the user sees the timeout,
not a stuck `mix` invocation.

## CI usage

In CI, set `PHX_SKIP_DEPS_AUDIT=1` for `mix deps.get` steps and run
`mix phx.deps_audit --ci` as a separate job — CI wants determinism
and full Tier 2 output, not the fast-path hook.

See `ci-integration.md` for sample workflows.
