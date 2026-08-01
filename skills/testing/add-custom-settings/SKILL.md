---
name: add-custom-settings
description: 'Full workflow for adding custom settings: create model, wire to variant,
  test locally'
---

---
name: add-custom-settings
description: Full workflow for adding custom settings: create model, wire to variant, test locally
---

# Add Custom Settings

Complete workflow for adding custom settings to a Bottlerocket variant, from model creation through local testing.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., PLAN.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```python
import json
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
workspace = f"planning/add-custom-settings-{timestamp}"
bash(f"mkdir -p {workspace}", on_error="raise")

while True:
    result = bash(f"python3 skills/add-custom-settings/next-step.py {workspace}", on_error="raise")
    action = json.loads(result)

    if action["type"] == "done":
        final = fs_read("Line", f"{workspace}/FINAL.md", 1, -1)
        log(final)
        break

    if action["type"] == "gate_failed":
        log(f"Gate failed: {action['reason']}")
        break

    if action["type"] == "spawn":
        r = spawn(
            action["prompt"],
            context_files=action["context_files"],
            context_data=action.get("context_data", {}),
            allow_tools=True
        )
        write("create", f"{workspace}/{action['output_file']}", file_text=r.response)
```

## Handling Exceptions

The state machine handles the happy path. When things go wrong, **exercise judgment**:

| Exception | Response |
|-----------|----------|
| Spawn times out | Assess: retry with longer timeout? Report partial progress? |
| Spawn returns error | Report failure to state machine, let it track retries |
| Empty/invalid response | Treat as failure, report to state machine |

**Don't silently advance past failures.** Either retry, fail explicitly, or document gaps.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Read phase files yourself | Pass phase files via context_files to subagents |
| Decide what phase is next | State machine decides via next-step.py |
| Skip gates "because it looks done" | Always validate gates |
| Store state in your memory | State lives in progress.json |
| Silently advance past failures | Retry, fail, or document gaps |

## Phases

1. **PLAN**: Gather requirements (settings name, structure, target variant)
2. **CREATE-MODEL**: Execute create-settings-model skill
3. **WIRE-VARIANT**: Execute add-settings-to-variant skill
4. **TEST**: Execute test-settings-locally skill
5. **FINALIZE**: Create summary document

## Inputs

The orchestrator needs to create a workspace before starting. The PLAN phase will gather:
- Settings name and structure
- Target variant
- Any special requirements

## Outputs

Produces workspace at `planning/add-custom-settings-<timestamp>/` containing:
- `requirements.json` - Captured requirements
- `01-model.md` - Model creation output
- `02-variant.md` - Variant wiring output
- `03-test.md` - Testing output
- `FINAL.md` - Complete workflow summary
