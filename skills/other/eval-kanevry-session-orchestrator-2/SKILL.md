---
name: eval
description: Use this skill to run an honest session-process evaluation (Standard v1, aiat-llm-eval/1.0) — score the last completed orchestrator session against the pre-registered rubric-v1 dimensions, run /eval, evaluate this session, produce an eval report, or re-verify a stored eval run for reproducibility. Deterministic-first with an optional advisory LLM judge; never produces a global score.
metadata:
  user-invocable: "true"
  tags: eval, measurement, quality, meta, standard
  model: sonnet
  model-preference: sonnet
  model-preference-codex: gpt-5.4-mini
  model-preference-cursor: claude-sonnet-4-6
  args-schema: "[{\"flag\":\"--session\",\"description\":\"session_id to evaluate (default: last completed session via the resolution cascade)\"},{\"flag\":\"--no-write\",\"description\":\"Evaluate + report without appending to the eval journal (.orchestrator/metrics/eval.jsonl)\"},{\"flag\":\"--verify\",\"description\":\"Re-evaluate a stored run-id and diff per-dimension for scoring drift (exit 1 on drift)\"}]"
---

# eval

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/eval/SKILL.md`](../../../skills/eval/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
