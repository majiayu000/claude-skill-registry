---
name: autodev
description: 'Manage the PROGRAM.md operational contract that bounds autonomous development loops. Use when setting up or validating PROGRAM.md/AUTODEV.md, choosing between autodev and evolve, or turning a repeated postmortem -> analyze -> plan -> pre-mortem -> implement -> validate cycle into the v2 autonomous workflow.'
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: task
  intel_scope: topic
metadata:
  tier: execution
  dependencies:
    - evolve
    - rpi
output_contract: "validated PROGRAM.md/AUTODEV.md contract or clear evolve/RPI execution handoff"
---

# /autodev

`/autodev` manages the repo-local operational contract for autonomous development.
It does not replace `/evolve` or `/rpi`.

- `PROGRAM.md` or `AUTODEV.md` defines the contract: mutable scope, immutable
  scope, experiment unit, validation commands, decision policy, escalation rules,
  and stop conditions.
- `ao autodev` creates, inspects, and validates that contract.
- `ao evolve` runs the v2 autonomous improvement loop.
- `ao rpi` runs one research -> plan -> implement -> validate lifecycle.

## Routing

Use this split when the user asks whether the old evolve flow should become a
new command or skill:

| Intent | Action |
|--------|--------|
| define or repair the repo-local autonomous policy | use `/autodev` and `ao autodev` |
| run the autonomous improvement loop | use `/evolve` or `ao evolve` |
| run one bounded lifecycle | use `/rpi` or `ao rpi` |

`PROGRAM.md` takes precedence over `AUTODEV.md`. Treat `AUTODEV.md` as the
compatibility alias.

## Execution Steps

### Step 1: Detect the contract

```bash
if [ -f PROGRAM.md ]; then
  PROGRAM_PATH=PROGRAM.md
elif [ -f AUTODEV.md ]; then
  PROGRAM_PATH=AUTODEV.md
else
  PROGRAM_PATH=
fi
```

If a contract exists, validate before using it:

```bash
ao autodev validate --json ${PROGRAM_PATH:+--file "$PROGRAM_PATH"}
```

If no contract exists and the user asked to initialize or define the loop, create
one:

```bash
ao autodev init "<objective>"
```

Infer the objective from the user request when it is clear. Ask only when the
objective cannot be discovered from repo context and inventing it would make the
contract misleading.

### Step 2: Repair or explain validation failures

When validation fails, inspect the missing fields and patch the program file if
the user asked to create or fix the contract. Required sections:

- `Objective`
- `Mutable Scope`
- `Immutable Scope`
- `Experiment Unit`
- `Validation Commands`
- `Decision Policy`
- `Escalation Rules`
- `Stop Conditions`

Prefer narrow mutable scope and concrete validation commands. If the needed work
crosses immutable scope, create or update a bead instead of silently widening the
contract.

### Step 3: Hand off to the loop

After `ao autodev validate` passes:

- For one lifecycle, run `/rpi "<goal>"` or `ao rpi ...`.
- For the repeated autonomous loop, run `/evolve` or `ao evolve --max-cycles <n>`.
- If both `PROGRAM.md` and `GOALS.md` exist, `GOALS.md` is strategic fitness and
  `PROGRAM.md` is the operational execution layer.

Do not mark an autonomous cycle successful only because the main tests pass. The
program validation bundle and stop conditions must also be satisfied.

## Examples

```text
User: turn this postmortem/analyze/plan/pre-mortem/implement/validate loop into
a v2 command.
Agent: Explain that `ao evolve` runs the loop, then create or validate
`PROGRAM.md` with `/autodev` so the loop has explicit scope and gates.
```

```bash
ao autodev init "Continuously improve AgentOps skills within explicit scope."
ao autodev validate
ao evolve --max-cycles 1
```

## Troubleshooting

| Problem | Response |
|---------|----------|
| `PROGRAM.md not found` | Run `ao autodev init "<objective>"` when setup is requested. |
| validation reports missing sections | Patch the missing required sections, then rerun `ao autodev validate --json`. |
| requested work is outside immutable scope | Stop direct edits and create a bead or ask for an explicit contract change. |
| user asks "is this evolve?" | Answer: `autodev` defines the loop contract; `evolve` runs the loop. |
