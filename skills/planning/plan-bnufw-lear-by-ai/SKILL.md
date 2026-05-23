---
name: plan
description: Draft a repo-local plan using the plan skill template and optionally save it.
metadata:
  short-description: Repo plan + issues contract
---

# Plan (Repo)

Draft structured plans for this repository and optionally save them to `plan/`.

## Core rules
- Use `assets/_template.md` as the plan structure and fill every section.
- Do not edit code while planning.
- Draft the plan in chat first; ask for confirmation before writing a plan file.
- Save plans to the repo `plan/` directory, not `~/.codex/plans`.
- Use the naming pattern: `plan/YYYY-MM-DD_HH-mm-ss-<slug>.md`.
- The plan must include a matching Issue CSV path: `issues/YYYY-MM-DD_HH-mm-ss-<slug>.csv`.
- When selecting MCP tools, reference `docs/mcp-tools.md` for the correct `server:tool` names.

## Clarifications
- Ask up to 2 questions if the task is unclear; otherwise state assumptions and proceed.
- If the task continues across turns, re-invoke this skill to keep the rules active.

## Plan workflow
1) Restate the task and assumptions.
2) Draft the plan body in chat (no frontmatter) using the template.
3) Ask: "Reply CONFIRM to write the plan file."
4) On confirmation, write the plan file with frontmatter via:
   - `python3 .codex/skills/plan/scripts/create_plan.py --task "<short title>" --complexity <simple|medium|complex>`
   - Provide the body via stdin or `--body-file`, or use `--template` for a starter.
5) If you need to inspect existing plans:
   - List: `python3 .codex/skills/plan/scripts/list_plans.py`
   - Read frontmatter: `python3 .codex/skills/plan/scripts/read_plan_frontmatter.py <plan.md>`

## Issue CSV
- Generate the Issue CSV after the plan is reviewed/approved.
- Use `assets/_template.csv` and fill **all** required fields.
- Follow `issues/README.md` for column meanings and CSV formatting.
- Use `docs/mcp-tools.md` to populate the `Tools` column with valid `server:tool` names.
- Validate with: `python3 .codex/skills/plan/scripts/validate_issues_csv.py <issues.csv>`.
- If validation fails, fix and re-run until it passes.
