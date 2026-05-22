---
name: survey-patterns
description: "Survey the codebase for analogous features, reusable utilities, and existing patterns relevant to a proposed change. Returns structured findings without writing code. Use when the user asks to \"survey patterns\", \"find existing patterns\", \"look for analogous features\", \"check how similar things are done\", \"find prior art for this change\", or needs pattern context before planning a change."
---

# Survey Patterns

Search the codebase for analogous features and reusable building blocks before planning a change. Returns structured findings. Does not write code or plans.

## Step 1: Identify the Task

Determine what the change is about:

- If a task description was passed in, use it
- Otherwise, derive it from conversation context (the user's latest request)

State the task back in one sentence to confirm scope before searching.

## Step 2: Spawn Pattern Survey Subagent

Spawn a single subagent (`model: "opus"`, do not set `run_in_background`). The subagent's prompt must include:

1. The confirmed task description from Step 1
2. An instruction to read [references/pattern-surveyor.md](references/pattern-surveyor.md) for survey guidelines, categories, and output format before searching

The subagent covers all three categories (Analogous Features, Reusable Utilities, Convention Anchors) in one sweep and returns a single structured report.

## Step 3: Output Findings

Output the subagent's report verbatim. Do not reformat or re-synthesize — `references/pattern-surveyor.md` specifies the exact output format the subagent produces.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Do not write files.
- Do not propose implementation steps.
