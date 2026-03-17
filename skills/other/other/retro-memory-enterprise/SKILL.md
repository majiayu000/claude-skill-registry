---
name: retro-memory-enterprise
description: "Enterprise post-session retrospective: writes evidence-ledger, delegates to retro-auditor subagent (isolated context), updates .claude/rules, runs validations."
argument-hint: "[full|light] (default: full)"
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Enterprise Retro Memory (governed)

ARGUMENTS: $ARGUMENTS

## Mode
- full (default): evidence-ledger + update all .claude/rules/*.md + run validate_rules.sh
- light: evidence-ledger + update only active-context.md + run validate_rules.sh

## Guardrails (anti-hallucination)
- Use ONLY information from the current conversation + existing repo files.
- Anything not explicit must be marked as Assumption (confidence: high/med/low), or excluded.
- Any inferred rule MUST include "Evidence:" referencing what in the chat supports it.
- Never store secrets/tokens/credentials. If found, redact and add "[REDACTED]".

## Step A — Create Evidence Ledger (main context)
1) Ensure directories exist:
   - ./.claude/retro/
2) Write a new file: ./.claude/retro/<timestamp>-evidence.md
   Use format: YYYY-MM-DDTHH-MM (e.g. 2026-02-17T14-30-evidence.md)

   Include sections:
   - ## Decisions & Agreements (explicit only)
   - ## Preferences (explicit only)
   - ## Failure Modes Observed (repeated problems)
   - ## Inefficient Loops to Avoid
   - ## Effective Patterns to Repeat
   - ## Open Questions / Unknowns
   - ## Assumptions (minimize; include confidence)
   - ## Redactions (if any)

3) Keep it short but evidence-rich. Use bullet points. Short quoted fragments (<= 1 line each).

## Step B — Delegate to isolated subagent
Use the retro-auditor agent and pass:
- ledger path
- mode

Prompt: "Use the retro-auditor agent to process ./.claude/retro/<timestamp>-evidence.md in MODE=<full|light> and update ./.claude/rules accordingly."

## Step C — Validate & Fix
Run:
```bash
bash .claude/skills/retro-memory-enterprise/scripts/validate_rules.sh
```
If warnings/errors occur, fix and re-run until clean.

## Step D — Return summary
Output in chat:
- Ledger path created
- Files updated (list)
- Top 5 rule changes
- Assumptions introduced (if any)
- Contradictions resolved (if any)
