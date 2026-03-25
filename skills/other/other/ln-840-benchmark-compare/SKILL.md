---
name: ln-840-benchmark-compare
description: "Runs a balanced built-in vs hex-line benchmark with scenario manifests, activation checks, diff-based correctness, and a final comparison report."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Benchmark Compare

**Type:** L3 Worker
**Category:** 8XX Optimization -> 840 Benchmark

Run a clean A/B benchmark in Claude Code: one session with built-in tools only, one with `hex-line`. The benchmark is scenario-based, diff-validated, and manifest-driven. It measures activation, correctness, time, cost, and tokens.

---

## Input / Output

| Direction | Content |
|-----------|----------|
| **Input** | Repo checkout containing `mcp/hex-line-mcp/`, optional `references/goals.md`, optional `references/expectations.json` |
| **Output** | Comparison report in `skills-catalog/ln-840-benchmark-compare/results/{date}-comparison.md` |

---

## Prerequisites

- `claude --version` succeeds
- `git` succeeds
- `mcp/hex-line-mcp/server.mjs` exists
- `mcp/hex-line-mcp/hook.mjs` exists
- `skills-catalog/ln-840-benchmark-compare/references/goals.md` exists
- `skills-catalog/ln-840-benchmark-compare/references/expectations.json` exists

---

## Quick Run

```bash
bash skills-catalog/ln-840-benchmark-compare/scripts/run-benchmark.sh \
  [skills-catalog/ln-840-benchmark-compare/references/goals.md] \
  [skills-catalog/ln-840-benchmark-compare/references/expectations.json]
```

The runner handles:
- syntax preflight
- SessionStart preflight
- scenario extraction from `goals.md`
- isolated worktrees per scenario/session
- per-scenario diffs
- final comparison report

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

---

## Report Contract

`skills-catalog/ln-840-benchmark-compare/results/{date}-comparison.md` must answer:
- Did each scenario complete correctly?
- Did `hex-line` activate cleanly without discovery drift?
- What changed in wall time, API time, cost, output tokens, and total tool calls?
- Was the run valid?

Do not treat raw time/cost as sufficient without scenario correctness.

---

## Known Pitfalls

| Pitfall | Solution |
|---------|----------|
| SessionStart not present in hex-line run | Fail preflight and stop |
| Agent drifts into `ToolSearch` before hex-line use | Treat as activation problem and capture in report |
| Worktree already exists from prior crash | Remove it before adding a new one |
| Diff artifacts missing | Treat scenario correctness as failed |
| Simple scenario favors built-ins | Keep it in the suite if it is common; honesty beats cherry-picking |

---

## Definition of Done

- [ ] `goals.md` defines the canonical balanced suite
- [ ] `expectations.json` fully describes scenario correctness
- [ ] Runner passes syntax and SessionStart preflight
- [ ] Each scenario runs in two clean worktrees from the same commit
- [ ] Parser evaluates activation and scenario correctness from logs plus diffs
- [ ] Final report is saved to `skills-catalog/ln-840-benchmark-compare/results/`
- [ ] Temporary worktrees are removed

---

**Version:** 2.0.0
**Last Updated:** 2026-03-24
