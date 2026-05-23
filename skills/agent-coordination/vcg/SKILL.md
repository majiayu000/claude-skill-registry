---
name: vcg
description: Short, explicit alias for vc-router. Use only when the user explicitly invokes `use vcg:` and wants the shortest reliable router command.
---

# VCG (VC Go Alias)

## VC Defaults

- Prefer fast iteration and shipping a working baseline over perfection.
- Make safe default choices without pausing; record assumptions briefly.
- Ask questions only after delivering an initial result, unless the workflow requires confirmation for safety/legal reasons.
- Keep outputs concise, actionable, and easy to extend.
- Assume the user is non-technical; avoid long explanations and provide copy/paste steps when actions are required.
- Treat non-explicit triggers (e.g., "vc go") as normal text; ask the user to rephrase using `use vcg:`.

## VC Fast Path

- Classify the task in one pass.
- Select a single best-fit skill; avoid chaining unless required.
- Execute immediately; collect assumptions and questions for the end.
- If the task is multi-step or open-ended, default to a finish-style workflow.

## Sub-Agent Assist (Optional)

If the request is **large/ambiguous** and collaboration tools are available, spawn **1–2 sub-agents** to parallelize:
- Repo scan (within scope roots): locate relevant files/config and constraints
- Risk/validation scan: test strategy, edge cases, safety concerns

Rules:
- Timebox and keep outputs short.
- Sub-agents report findings only; main agent decides routing and applies changes.

## VC Quick Invoke

- `use vcg: <goal>`

## Scope Lock (Required)

- Before any file search, determine scope roots:
  1. If a `.vc-scope` file exists in the current directory or any parent, use the closest one.
     - Each non-empty, non-comment line is an allowed path.
     - Relative paths are resolved from the `.vc-scope` file directory.
  2. Else, if inside a git repo, use the repo root.
  3. Else, use the current working directory.
- Only run `rg`, `find`, or any filesystem scans inside the scope roots.
- Never scan `$HOME` or `/` unless the user explicitly asks.

## Routing Rules

- This repo intentionally ships only `vc*` skills.
- Finish-to-end requests: route to `vc-phase-loop`.
- Planning/execution loops: route to `vc-phase-loop`.
- Everything else: route to `vc-phase-loop` as the safe default.

## Execution Rules

- Read only the selected skill's SKILL.md and follow its defaults.
- Keep the user flow simple: deliver a first pass, then ask for corrections.
- If uncertain between two skills, pick the one with narrower scope.
- If the user did not explicitly invoke `use vcg:`, ask them to rephrase using `use vcg:` and stop.
