---
name: mux-subagent
description: "MUX subagent protocol enforcer. Activates file-based communication protocol, blocks TaskOutput tool, enforces return code convention (0=success), and ensures signal file creation. Load as MANDATORY FIRST ACTION in all MUX-delegated subagents."
project-agnostic: true
hooks:
  PreToolUse:
    - matcher: "TaskOutput"
      hooks:
        - type: command
          command: "uv run --no-project --script ${CLAUDE_PLUGIN_ROOT}/skills/mux-subagent/hooks/mux-subagent-guard.py"
---

# MUX Subagent Protocol

## MANDATORY COMPLIANCE

You are operating under MUX delegation protocol. These rules are NON-NEGOTIABLE.

## Return Code Convention

Your FINAL response to the orchestrator MUST be EXACTLY: `0`

- `0` = success (like bash exit codes)
- Any other return = PROTOCOL VIOLATION
- ALL substantive content goes into your report file

## File-Based Communication

- Write ALL findings/results to the report file path given in your task prompt
- Report files are your ONLY output channel
- The orchestrator NEVER reads your report directly — it uses extract-summary tool

## Signal File Creation (MANDATORY)

BEFORE returning `0`, you MUST create a signal file:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/mux/tools/signal.py <signal-path> --path <your-report-path> --status success
```

If you fail to create a signal, the orchestrator cannot verify your completion.
This is a SESSION DEATH violation if skipped.

## Report Format

**CRITICAL**: The orchestrator reads ONLY the Table of Contents + Executive Summary (via extract-summary.py). It NEVER reads your full report. Write the Executive Summary as if it's the only thing that determines what happens next — because it is.

```markdown
# <Report Title>

## Table of Contents
(all markdown headers — orchestrator uses this to understand report structure)

## Executive Summary

- **Finding/Result**: keyword-dense bullet, no prose
- **Finding/Result**: keyword-dense bullet, no prose
- (max 5-7 bullets — ruthlessly concise)

### Next Steps
- **Recommended action**: what the orchestrator should do with this report
- **Dependencies**: files/reports this connects to (use full paths)
- **Routing hint**: which agent type should consume this next, and why

## <Sections>
(your actual detailed content — only downstream agents read this)
```

### Executive Summary Rules

- Bullets ONLY — no paragraphs, no prose
- Each bullet: `**Label**: keyword-dense value` format
- Information density over readability — the orchestrator is an LLM, not a human
- Include file paths, counts, status codes, concrete findings
- NEVER vague ("several issues found") — ALWAYS specific ("3 critical gaps: auth, validation, error handling")

### Next Steps Rules

- ALWAYS include this subsection — it is MANDATORY
- Tell the orchestrator exactly what to do next with actionable guidance
- Reference specific file paths the next agent should read
- Suggest agent type (researcher, auditor, writer, etc.) if relevant
- Flag blockers or decisions that need user input

## What NOT to Do

- NEVER return verbose text as your final response
- NEVER skip signal file creation
- Load mux-subagent FIRST, then load any other skills needed for your task
- NEVER use TaskOutput

## Pre-Return Checklist

Before returning `0`, verify:

- [ ] Report written to specified file path
- [ ] Report has Executive Summary section (bullets only, keyword-dense)
- [ ] Executive Summary has ### Next Steps subsection
- [ ] Signal file created via signal.py
- [ ] No substantive content in final response
