# LLM triage — two-tier with context-supervisor

Phase 2 adds optional LLM-assisted triage on top of the deterministic
rule layer. The deterministic rules carry the security load; the LLM
compresses evidence and surfaces likely-FPs vs likely-TPs to the
human reviewer. **No finding is auto-suppressed without human review.**

## Iron Laws

1. **TRIAGE IS ADVISORY.** LLM verdicts adjust the *renderer's
   ordering and visual emphasis*, never the underlying severity in
   the NDJSON stream. Audit findings remain the source of truth.
2. **THRESHOLD-GATED.** Triage runs only when a package's weighted
   score exceeds 10 (BLOCK=10, WARN=3, INFO=1). Below threshold,
   the deterministic output is the final word.
3. **TWO-TIER MANDATORY.** Per-package triagers write JSON files;
   a `context-supervisor` (haiku) consolidates. Main skill reads
   ONLY the consolidated file. Reading per-package outputs directly
   in the main context blows the budget on 5+ packages.
4. **NO INVENTED FINDINGS.** Each verdict maps 1:1 to an input
   finding. Post-call validator drops verdicts whose `rule_id +
   file + line` triple isn't in the input set.

## Architecture

```
deps-audit body
    │
    ▼ score > 10 for package P?
    │
    ├─► YES → spawn hex-deps-triager (sonnet) for P
    │            ↓ writes triage/<pkg>-<ts>.json
    │
    ▼   (wait for all triagers)
context-supervisor (haiku)
    │
    ▼ reads triage/<pkg>-*.json files
    │
    ▼ writes triage/consolidated.md
    │
deps-audit body reads consolidated.md
```

## Two-tier rationale

A 20-package audit run produces ~3-5KB of findings.jsonl. Each
triager fetches 3-line diff windows × N findings — easily 50KB
context per package. Running 10 triagers in parallel and then
synthesizing in the main context exhausts the budget on
synthesize.

Splitting the work: per-package triager has its own context, writes
a small structured verdict (1-3KB). The supervisor's input is
N × 3KB ≈ 30KB even at 10 packages — well within haiku's window.
Main skill reads a single consolidated.md (<5KB).

## Triager spawn pattern

The skill body builds one input JSON per package, then spawns
triagers in parallel via the Task tool:

```bash
# Pseudocode — the skill's actual body uses Task() blocks
for pkg in $(jq -r 'keys[]' high_score.json); do
  build_triager_input "${pkg}" > "/tmp/triage-in-${pkg}.json"
  spawn_task --subagent_type hex-deps-triager \
             --prompt "Triage findings for ${pkg}.
                       Input: /tmp/triage-in-${pkg}.json
                       Output: .claude/deps-audit/triage/${pkg}-$(date +%s).json"
done
wait
```

After all triagers complete, the skill spawns `context-supervisor`:

```bash
spawn_task --subagent_type context-supervisor \
           --prompt "Consolidate triage verdicts.
                     Inputs: .claude/deps-audit/triage/*.json
                     Output: .claude/deps-audit/triage/consolidated.md
                     Group by verdict (likely_malicious, needs_human,
                     likely_benign). Surface model+confidence per
                     verdict. Sum across packages."
```

## Input JSON contract

See `hex-deps-triager.md` agent. Each input contains:

- `package`, `version`, `previous_version`
- `tarball_dir`, `previous_tarball_dir` (absolute paths)
- `findings[]` — list with `rule_id`, `file`, `line`, `snippet`,
  `message`, `diff_window` (3 lines context)
- `hex_metadata` — downloads, owners, release_publisher, inserted_at

Build via `mix run --no-mix-exs -e` over the existing findings.jsonl
plus the hex-api cache. Keep diff_window ≤200 chars per finding to
control input size.

## Output JSON contract

```json
{
  "package": "<pkg>",
  "version": "<version>",
  "model": "sonnet",
  "summary": "<one-line per-package summary>",
  "verdicts": [
    {
      "rule_id": <int>,
      "file": "<file>",
      "line": <int>,
      "confidence": <0.0..1.0>,
      "verdict": "likely_benign | needs_human | likely_malicious",
      "rationale": "<one paragraph>",
      "fp_reasons": ["<reason1>", "<reason2>"]
    }
  ]
}
```

Validation pass after each triager:

1. Verify the file parses as JSON.
2. Verify every `verdicts[].{rule_id, file, line}` triple appears
   in the input `findings[]`. Mismatches are dropped with a warning.
3. Verify `verdict` and `confidence` ranges. Out-of-range
   verdicts → `needs_human` with `confidence: 0.0`.

## Consolidated output

The `context-supervisor` produces a markdown file shaped like:

```markdown
# Triage Consolidated — N packages, M findings

## Summary
- Likely malicious: 1 (1 finding)
- Needs human review: 3 (5 findings)
- Likely benign: 7 (12 findings)

## Likely malicious (BLOCK by default)
### phoenix_extras 0.2.0 → 0.3.0 (score 22, sonnet conf 0.92)
- rule 3 (compile-time exec) at lib/init.ex:14 — System.cmd to
  unknown URL inside __before_compile__. New maintainer + 1mo old.

## Needs human review
...

## Likely benign (consider INFO downgrade)
...
```

The deps-audit renderer reads this and slots the sections above
the per-package findings tables.

## Token budget

| Component | Budget | Actual (10 pkg audit) |
|-----------|--------|----------------------|
| Per-triager input | ≤15KB | ~5-10KB |
| Per-triager output | ≤3KB | ~1-2KB |
| Consolidator input | 10 × 3KB | ~25KB |
| Consolidator output | ≤5KB | ~3KB |
| Main skill triage read | ≤5KB | ~3KB |

Compared to the naive approach (main reads 10 × 10KB = 100KB), the
two-tier flow saves ~95% of the post-triage context burn.

## When NOT to invoke LLM triage

- Package score ≤ 10 → deterministic output suffices.
- Mode A (`--preview`) on a single package not yet locked → user is
  exploring; the audit table is enough.
- `--no-llm` flag passed by the user.
- No `ANTHROPIC_API_KEY` available in the environment — fall back
  cleanly to deterministic output with a warning.
