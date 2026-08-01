---
name: ca-threat-model
description: Opt-in lightweight STRIDE pass for a sensitive feature before implementation. Not a routine gate — invoke it when a change warrants security thought.
argument-hint: "<scope description>"
---

# $ca-threat-model — STRIDE pass (opt-in)

Optional, lightweight pre-implementation security review for a sensitive change — new external endpoints, new secrets-handling paths, new auth/authz flows. **Opt-in, not a routine gate**: nothing routes here automatically. Invoke it when a change warrants the thought; skip it otherwise. Read-only — modifies no file. Describe what the component does, what data it handles, and which actors interact with it.

## Routes to

`security-architecture` (`${CLAUDE_PLUGIN_ROOT}/routines/security-architecture/SKILL.md`). The skill reads:

- `<project-root>/.codearbiter/security-controls.md` — compliance requirements.
- `<project-root>/.codearbiter/decisions/` — existing security-relevant ADRs.

## Output

```
## Scope
<what is being analyzed>

## STRIDE findings
| Threat | Category    | Likelihood | Impact | Control                      |
|--------|-------------|------------|--------|------------------------------|
| ...    | S/T/R/I/D/E | H/M/L      | H/M/L  | <control or NONE — needs one> |

## Recommended controls before implementation
- <control 1>

## Clearance
CLEAR TO IMPLEMENT | BLOCKED — resolve findings first
```

## When NOT to use

- Reviewing already-written code → `$ca-review`.
- A full cross-cutting review → `$ca-checkpoint`.
- A security question → `$ca-btw`.

## Hard gate

Read-only — modifies no file. This is an advisory pass, not a routine gate; it never runs unless
invoked.
