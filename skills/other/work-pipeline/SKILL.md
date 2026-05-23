---
name: work-pipeline
description: Triggers the WORK-PIPELINE when a user request starts with a [] tag (e.g., [new-feature], [bugfix], [WORK start]). Use this skill whenever you detect a [] tag at the beginning of a user message.
---

# WORK-PIPELINE Trigger

When the user's message starts with a `[]` tag, start the WORK-PIPELINE by reading `../skills/sdd-pipeline/references/agent-flow.md` and following the orchestration flow.

## Trigger Detection

Any message starting with `[...]` triggers this pipeline:
- `[new-feature]`, `[enhancement]`, `[bugfix]`, `[new-work]`, `[WORK start]`
- Or any custom tag in square brackets

## References Directory (CRITICAL)

When this skill is triggered, Claude Code provides the "Base directory for this skill" as an absolute path.
Derive the **REFERENCES_DIR** from it:

```
REFERENCES_DIR = {Base directory}/../sdd-pipeline/references
```

You MUST pass this absolute path to **every sub-agent invocation** (specifier, planner, scheduler, builder, verifier, committer).
Include it at the top of the prompt text:

```
REFERENCES_DIR={absolute_path}
```

Sub-agents need this path to read their reference files. Without it, they cannot find the files and will loop.

## Pipeline Flow

1. **Call specifier agent** — analyzes the requirement, creates `works/WORK-NN/Requirement.md`, determines execution-mode (direct/pipeline/full)
2. **⛔ STOP — Present the specifier's output summary to the user and WAIT for explicit approval.** Do NOT call the next agent until the user approves. Show what was created (Requirement.md, PLAN.md if direct mode, TASK files) and ask "Proceed?"
3. **Follow the execution-mode** returned by specifier:
   - `direct`: call builder → committer
   - `pipeline`: call builder → verifier → committer in sequence
   - `full`: call planner → **⛔ STOP for 2nd approval** → scheduler → [builder → verifier → committer] × N

## Auto Mode

If the user's message ends with "auto" or "자동으로", skip ALL approval steps and execute the entire pipeline automatically. This is the ONLY case where approval gates can be skipped.

## Arguments

User requirement: $ARGUMENTS
