---
name: continuity-kernel
version: 0.2.0
description: OpenClaw continuity kernel for fail-open llm_input injection, deterministic runtime contracts, and shadow-mode eval receipts.
author: CacheForge
license: MIT
homepage: https://github.com/cacheforge-ai/cacheforge-skills
user-invocable: true
tags:
  - cacheforge
  - openclaw
  - continuity
  - memory
  - hooks
  - fail-open
  - reliability
  - evals
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://github.com/cacheforge-ai/cacheforge-skills","requires":{"bins":["python3"]}}}
---

## When to use this skill

Use this skill when the user wants to:
- Inject bounded continuity context into `llm_input` without manual configuration
- Persist Soul Card + Mission Ticket state with deterministic runtime contracts (durable default SQLite path, zero-config)
- Keep agent behavior fail-open if continuity logic or storage has an error
- Generate reproducible runtime proof receipts for audits and reviews
- Run shadow-mode evals and append chunk-level quality snapshots

## Commands

```bash
# Run full test suite
python3 -m unittest discover -s tests/continuity-kernel -p 'test_*.py'

# Generate deterministic runtime contract proof artifact
python3 skills/continuity-kernel/generate_runtime_contract_proof.py

# SC-02 core-shadow gate (trace optional, synthetic allowed for this suite)
python3 skills/continuity-kernel/run_shadow_eval.py --layer 'Soul Card' --chunk 'SC-02' --suite core-shadow --runs 100 --append artifacts/continuity-kernel/p0-evals.json

# SC-02 perturb robustness gate (trace-backed, deterministic selector + size_only)
python3 skills/continuity-kernel/run_shadow_eval.py --layer 'Soul Card' --chunk 'SC-02' --suite memoryarena-mini-perturb --perturb-profile deletion --selector-mode deterministic --compaction-policy size_only --runs 100 --trace-jsonl tests/continuity-kernel/fixtures/shadow_eval_trace_memoryarena_mini_perturb.jsonl --append artifacts/continuity-kernel/p0-evals.json

# SC-02 perturb robustness gate (trace-backed, dual-route + attention-preserving)
python3 skills/continuity-kernel/run_shadow_eval.py --layer 'Soul Card' --chunk 'SC-02' --suite memoryarena-mini-perturb --perturb-profile deletion --selector-mode dual_route_experimental --compaction-policy attention_preserving_experimental --runs 100 --trace-jsonl tests/continuity-kernel/fixtures/shadow_eval_trace_memoryarena_mini_perturb.jsonl --append artifacts/continuity-kernel/p0-evals.json
```

## Options

`run_shadow_eval.py` options:
- `--layer TEXT` — Active P0 layer name
- `--chunk TEXT` — Active chunk id/name
- `--suite core-shadow|memoryarena-mini|memoryarena-mini-perturb` — Task suite for eval scoring
- `--perturb-profile none|deletion|noise_injection|reorder` — Deterministic perturb profile for `memoryarena-mini-perturb`
- `--selector-mode deterministic|dual_route_experimental` — Selector mode tag for A/B eval receipts
- `--compaction-policy size_only|attention_preserving_experimental` — Compaction policy label for dropped-field A/B eval comparison
- `--runs N` — Number of evaluated shadow runs (default: 100)
- `--trace-jsonl PATH` — JSONL file containing observed shadow outcomes (repeatable)
- `--trace-dir PATH` — Directory scanned for `*.jsonl` observed shadow outcomes (repeatable)
- `--append PATH` — JSON file path to append snapshot results
- `--allow-synthetic` — Permit synthetic fallback for non-core suites when traces are unavailable (forced `pass=false`)
- `--artifacts-root PATH` — Directory for summary receipts (default: `~/.cache/continuity-kernel/p0-evals`)

Runtime persistence defaults:
- `ContinuityHookAdapter()` uses `~/.local/state/continuity-kernel/continuity.db`
- Override default path with `CONTINUITY_KERNEL_DB_PATH`
- Use `:memory:` only as explicit opt-in test mode
