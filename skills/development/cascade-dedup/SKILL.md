---
name: cascade-dedup
description: 'Strip duplicate and conflicting directives across the system-prompt cascade family: the canonical baseline, the six output-style embeds, and the two external harness embeds.'
disable-model-invocation: true
metadata:
  short-description: 'Cascade-family directive dedup and drift repair'
---

# Cascade dedup

The cascade family replicates one canonical prompt across three harnesses. Dedup means: verify the intentional replication byte-for-byte, strip the accidental repetition, and resolve conflicts with the canonical as winner.

| File | Role | Zones |
|---|---|---|
| `/home/alpha/.claude/claude/system-prompt-baseline.md` | Canonical; wins every conflict | Whole file is the source of truth |
| `output-styles/{axiom-mode,builder,duet,linus,odin,benchmark}.md` | Style embeds | Persona prefix **above** the charter `<role>` (the second `<role>` per file) = strip zone. Tail **from** the charter `<role>` = byte-identity invariant zone, never a dedup target |
| `output-styles/benchmark.md` auto-gen preamble (margin-runner header) | Generated | Never touch. Repairs to benchmark.md's cascade tail require explicit user authorization first |
| `/home/alpha/.omp/agent/AGENTS.md`, `/home/alpha/.codex/AGENTS.md` | Harness embeds | Harness-adapted tool sections are legitimate divergence; targets are internal duplication and accidental drift. Outside the repo: editable, never committable |

## Step 1 — Verify the invariant before dedup

Extract the canonical: `cp system-prompt-baseline.md /tmp/canon.md` (its charter `<role>` is line 1, so the canonical is the whole file). Per output-style:

```bash
diff -q /tmp/canon.md <(tail -c "$(wc -c < /tmp/canon.md)" output-styles/X.md)
```

Drift here is a sync bug, not duplication. Repair means replacing the file's entire tail (from its charter `<role>` to EOF) with the canonical content, as one block; dedup edits inside the invariant zone stay forbidden. For `benchmark.md`, get explicit user authorization before repairing.

**Completion criterion:** 6/6 byte-identical (after repair where needed), each diff result recorded.

## Step 2 — Strip-zone scan (persona prefixes)

`benchmark.md` has no eligible strip zone — its entire persona prefix sits inside the auto-generated margin-runner block — so Step 2 covers the five hand-authored styles and skips `benchmark.md` completely. Classify every sentence of each persona prefix as `voice | duplicate | conflict | unique-directive`:

- Normalize (lowercase tokens, stopwords removed). Jaccard >= 0.65 against a baseline rule → **duplicate**: strip it; the baseline copy stands.
- Jaccard >= 0.45 plus opposing modal verbs (must/never, always/must-not) → **conflict**: the baseline wins; delete or rewrite the prefix line.
- Persona voice — identity, tone, register — is not a directive: keep.
- Unique directives (persona-specific rules with no baseline pair): keep.

**Completion criterion:** every prefix sentence classified; every strip cites its baseline pair.

## Step 3 — Harness embeds

Per external file (`~/.omp/agent/AGENTS.md`, `~/.codex/AGENTS.md`):

1. **Internal duplication** within the file, same thresholds as Step 2.
2. **Directive-level comparison against the baseline.** Classify each divergence:
   - `harness-adaptation` — names that harness's tools or commands: keep.
   - `accidental drift` — same rule, mutated wording: align to the baseline wording.
   - `conflict` — the baseline wins, unless the divergence exists to fit harness-specific tooling.

**Completion criterion:** a divergence ledger with exactly one classification per divergence — none unclassified.

## Step 4 — Apply and verify

1. Repo files: one atomic commit. Any `benchmark.md` change (tail repair included) ships only with explicit user authorization recorded in this run. Re-run the Step 1 diffs after editing; run `prek run --all-files`.
2. Strips and conflict resolutions are doctrine changes → patch-bump all three manifest version fields (`plugin.json` `.version`, `marketplace.json` `.version` and `.plugins[0].version`) from the origin/main base in the same commit. A run that only re-syncs an embedded baseline, zero strips, is a pure sync change → no bump.
3. External files: edit in place, never commit; end the report with an explicit warning listing every externally edited path for user review.
4. Output styles load at session start — smoke-test doctrine effects in a fresh session.

**Completion criterion:** final report contains strips per file with citations, conflicts resolved with the winner named, kept harness-adaptations, externally edited paths, the `prek` result, and the invariant re-verified 6/6.
