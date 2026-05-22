---
name: eval-harness-kit
description: "Build and run deterministic evaluation suites for agent workflows (single-turn or agentic). Use when you need reproducible eval runs with manifests, graders, metrics, and JSONL logs for capability or regression tracking."
---

# Eval Harness Kit

## Overview
Create eval manifests, run tasks through an agent or command harness, and grade outputs with deterministic checks and optional LLM rubrics. The harness writes trajectories, metrics, and summaries to disk for repeatable analysis.

## Quick start
1) Copy `templates/eval.manifest.json` and edit tasks.
2) Run: `python <CODEX_HOME>/skills/eval-harness-kit/scripts/run_eval.py --manifest <path> --run-id <id>`
3) Inspect outputs in `eval_runs/<run-id>/` and the summary JSON.
Replace `<CODEX_HOME>` with your installed skill root (for example, `~/.codex` or `C:\Users\you\.codex`).

## Single-turn vs agentic
- Single-turn: `run_cmd` writes a response file; graders check the output.
- Agentic: `run_cmd` invokes your agent harness; graders check output plus optional transcript files.

## LLM rubric graders (optional)
- Use `type: "llm_rubric"` to call an external judge.
- Provide `llm_judge_cmd` in the manifest or `judge_cmd` per task.
- The judge must print JSON: `{"passed": true|false, "score": 0.0-1.0, "details": "..."}`.

## Core Guidance
- Decide capability vs regression up front; keep regression suites near 100% pass rate.
- Prefer deterministic graders (exact/regex/json) and add LLM rubrics only when needed.
- Keep each trial isolated; write outputs and transcripts to the run directory.
- Log metrics for every trial: latency, exit code, stdout/stderr sizes, output size.
- Use files as the memory boundary; do not paste large outputs into chat.

## Trust / Permissions
- **Always**: Read local files, write run artifacts under `eval_runs/`.
- **Ask**: Any networked grader (LLM rubric), running commands that mutate state, or running tools outside the repo.
- **Never**: Exfiltrating credentials or running destructive commands without explicit user request.

## Resources
- `scripts/run_eval.py`: Execute evals from a manifest; writes JSONL results and summaries.
- `scripts/grade_response.py`: Grade a single output against expected data.
- `scripts/compare_runs.py`: Compare two results files and flag regressions.
- `templates/eval.manifest.json`: Example manifest with single-turn and agentic tasks.
- `references/eval-roadmap.md`: Guidance for building and maintaining eval suites.

## Validation
- Run the example manifest; confirm `eval_runs/<run-id>/summary.json` exists.
- Use `compare_runs.py` to compare two runs and verify regression detection.
