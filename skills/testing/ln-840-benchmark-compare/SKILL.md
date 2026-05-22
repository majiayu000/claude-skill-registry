---
name: ln-840-benchmark-compare
description: "Use when benchmarking hex-line MCP against Claude built-in tools with scenario manifests, activation checks, and diff-based correctness."
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Benchmark Compare

**Type:** L3 Worker
**Category:** 8XX Optimization -> 840 Benchmark

Run a clean A/B benchmark in Claude Code: one session with built-in tools only, one with `hex-line`. The benchmark is scenario-based, diff-validated, manifest-driven, and runtime-backed. It measures activation, correctness, time, cost, and tokens. The current runner is intentionally scoped to this internal A/B. It does not, by itself, prove best-in-class against external alternatives.

---

## Input / Output

| Direction | Content |
|-----------|----------|
| **Input** | Repo checkout containing `mcp/hex-line-mcp/`, optional `references/goals.md`, optional `references/expectations.json` |
| **Output** | Comparison report in `skills-catalog/ln-840-benchmark-compare/results/{date}-comparison.md` plus machine-readable benchmark summary artifact |

---

## Prerequisites

- `claude --version` succeeds
- `git` succeeds
- `mcp/hex-line-mcp/server.mjs` exists
- `mcp/hex-line-mcp/hook.mjs` exists
- `skills-catalog/ln-840-benchmark-compare/references/goals.md` exists
- `skills-catalog/ln-840-benchmark-compare/references/expectations.json` exists
- `skills-catalog/ln-840-benchmark-compare/references/mcp-bench.json` exists

---

## Quick Run

```bash
bash skills-catalog/ln-840-benchmark-compare/scripts/run-benchmark.sh \
  [skills-catalog/ln-840-benchmark-compare/references/goals.md] \
  [skills-catalog/ln-840-benchmark-compare/references/expectations.json]
```

Optional extra session profile:

```bash
EXTRA_SESSION_ID=other-mcp \
EXTRA_SESSION_LABEL="Other MCP" \
EXTRA_MCP_CONFIG=/abs/path/to/other-mcp.json \
EXTRA_SETTINGS='{"disableAllHooks":true}' \
bash skills-catalog/ln-840-benchmark-compare/scripts/run-benchmark.sh
```

### Monitor Integration (Claude Code 2.1.98+)

**MANDATORY READ:** Load `shared/references/monitor_integration_pattern.md`

Stream benchmark progress:
`Monitor(command="bash skills-catalog/ln-840-benchmark-compare/scripts/run-benchmark.sh 2>&1 | grep --line-buffered -E 'scenario|PASS|FAIL|error|session'", timeout_ms=3600000, description="benchmark run")`

Fallback: `Bash(run_in_background=true)`.

The runner handles:
- syntax preflight
- SessionStart preflight
- scenario extraction from `goals.md`
- isolated worktrees per scenario/session
- per-scenario diffs
- final comparison report

Current scope:
- built-in Claude session
- Claude plus `hex-line`
- optional third Claude-compatible session profile through `EXTRA_SESSION_*` environment variables

External baseline note:
- use the same `goals.md` and `expectations.json`
- do not rewrite scenarios to fit the external tool
- do not make "top tool" claims from the internal A/B alone
- the optional third session profile is only valid when it can emit the same `stream-json` log shape and diff artifacts

---

## Workflow

### Phase 1: Define The Canonical Suite

Use one canonical pair owned by this skill:
- `skills-catalog/ln-840-benchmark-compare/references/goals.md`
- `skills-catalog/ln-840-benchmark-compare/references/expectations.json`

Rules:
- The suite must be a balanced mix of common engineering scenarios.
- Do not design the suite to favor `hex-line`.
- Every scenario in `goals.md` must have a matching entry in `expectations.json`.
- `expectations.json` is the source of truth for correctness.
- The same pair must be reused unchanged for any future external baseline.

Supported expectation fields per scenario:

| Field | Meaning |
|-------|---------|
| `id` | Scenario identifier used in result filenames |
| `expectedChangedFiles` | Files that must change |
| `forbiddenChangedFiles` | Files that must not change |
| `requiredDiffPatterns` | Regex patterns required in the saved diff |
| `forbiddenDiffPatterns` | Regex patterns that must not appear in the diff |
| `requiredResultPatterns` | Regex patterns required in the final assistant result text |
| `requiredCommands` | Regex patterns that must match at least one Bash command |
| `exactChangedFiles` | If `true`, no extra changed files are allowed |

### Phase 2: Preflight

The runner must pass:
- `node --check server.mjs`
- `node --check hook.mjs`
- `node --check extract-scenarios.mjs`
- `node --check parse-results.mjs`
- SessionStart smoke check from `hook.mjs`

If preflight fails, the benchmark is invalid and must stop before scenarios run.

### Phase 3: Execute Per Scenario

For each `##` scenario in `goals.md`:
1. generate a standalone prompt file
2. create two clean worktrees from the same commit
3. run built-in Claude session
4. run hex-line Claude session
5. save `.jsonl` logs and `.diff.txt` artifacts
6. remove both worktrees

Built-in session:
- no MCP
- hooks disabled

Hex-line session:
- resolved MCP config pointing to `server.mjs`
- `outputStyle: "hex-line"`
- `PreToolUse` hook through `hook.mjs`

### Phase 4: Parse Results

`parse-results.mjs` evaluates each scenario for both sessions.

Scenario pass requires:
- valid run
- successful session completion
- changed files match expectations
- diff patterns match expectations
- result text patterns match expectations
- required commands were actually executed

### Phase 5: Read The Report

The final report has these sections:
- Scenario Outcomes
- Activation
- Time
- Cost
- Tokens
- Tool Totals
- Validity

Interpretation rules:
- `invalid run` means setup/adoption failure, not product performance
- scenario `FAIL` means correctness contract was not met
- activation is part of product quality for `hex-line`, not external noise
- this report is necessary for internal A/B evaluation, but not sufficient for best-alternative claims

---

## Report Contract

`skills-catalog/ln-840-benchmark-compare/results/{date}-comparison.md` must answer:
- Did each scenario complete correctly?
- Did `hex-line` activate cleanly without discovery drift?
- What changed in wall time, API time, cost, output tokens, and total tool calls?
- Was the run valid?

Do not treat raw time/cost as sufficient without scenario correctness.

## External Baseline Policy

- This skill owns the canonical suite, not a universal leaderboard.
- If maintainers compare `hex-line` against external alternatives, they must reuse the same `goals.md`, `expectations.json`, and diff-based evaluation rules.
- External runs may use different harnesses, but they must preserve the same task text, starting commit, and correctness contract.
- If an external tool cannot satisfy the contract format, record that as a harness limitation instead of rewriting the suite to accommodate it.
- A report that only covers built-in Claude vs `hex-line` must say so explicitly.

---

## Runtime Contract

**MANDATORY READ:** Load shared/references/benchmark_worker_runtime_contract.md, shared/references/coordinator_summary_contract.md

Runtime CLI:

```bash
node shared/scripts/benchmark-worker-runtime/cli.mjs start --skill ln-840-benchmark-compare --identifier suite-default --manifest-file <file>
node shared/scripts/benchmark-worker-runtime/cli.mjs checkpoint --skill ln-840-benchmark-compare --identifier suite-default --phase PHASE_0_CONFIG --payload '{...}'
node shared/scripts/benchmark-worker-runtime/cli.mjs record-summary --skill ln-840-benchmark-compare --identifier suite-default --payload '{...}'
node shared/scripts/benchmark-worker-runtime/cli.mjs complete --skill ln-840-benchmark-compare --identifier suite-default
```

Required state fields:
- `report_ready`
- `summary_recorded`
- `final_result`
- `self_check_passed`

Domain checkpoints:
- `PHASE_0_CONFIG`
- `PHASE_1_PREFLIGHT`
- `PHASE_2_LOAD_SUITE`
- `PHASE_3_RUN_SCENARIOS`
- `PHASE_4_PARSE_RESULTS`
- `PHASE_5_WRITE_REPORT`
- `PHASE_6_WRITE_SUMMARY`
- `PHASE_7_SELF_CHECK`

Guard rules:
- do not advance without checkpointing the current phase
- do not complete before `benchmark-worker` summary is recorded
- do not complete before self-check passes

### Runtime Coordination

- Managed runs may pass deterministic `runId` and exact `summaryArtifactPath`.
- Standalone runs are supported. If both are omitted, runtime creates a standalone run and writes the default summary artifact path for the `benchmark-worker` family.

---

## Runtime Summary Artifact

**MANDATORY READ:** Load shared/references/coordinator_summary_contract.md

Emit a `benchmark-worker` summary envelope after the comparison report is written.

Managed mode:
- write to the exact `summaryArtifactPath`

Standalone mode:
- write `.hex-skills/runtime-artifacts/runs/{run_id}/benchmark-worker/ln-840-benchmark-compare--{identifier}.json`

Recommended payload:
- `scenarios_total`
- `scenarios_passed`
- `scenarios_failed`
- `activation_valid`
- `validity_verdict`
- `report_path`
- `warnings`
- `metrics`

---

## Known Pitfalls

| Pitfall | Solution |
|---------|----------|
| SessionStart not present in hex-line run | Fail preflight and stop |
| Agent drifts into `ToolSearch` before hex-line use | Treat as activation problem and capture in report |
| Worktree already exists from prior crash | Remove it before adding a new one |
| Diff artifacts missing | Treat scenario correctness as failed |
| Simple scenario favors built-ins | Keep it in the suite if it is common; honesty beats cherry-picking |
| External comparison uses edited scenarios or relaxed expectations | Treat the comparison as invalid |

---

## Definition of Done

- [ ] `goals.md` defines the canonical balanced suite
- [ ] `expectations.json` fully describes scenario correctness
- [ ] Runner passes syntax and SessionStart preflight
- [ ] Each scenario runs in two clean worktrees from the same commit
- [ ] Parser evaluates activation and scenario correctness from logs plus diffs
- [ ] Final report is saved to `skills-catalog/ln-840-benchmark-compare/results/`
- [ ] `benchmark-worker` summary artifact is written to the managed or standalone runtime path
- [ ] Temporary worktrees are removed
- [ ] Report states clearly whether it is internal A/B only or includes additional external baselines

---

**Version:** 2.0.0
**Last Updated:** 2026-03-24
