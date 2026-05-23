---
name: buff-execute
description: This skill should be used when the user asks to "execute the plan", "start building", "implement the plan", "run /buff:execute", "begin development", "start coding from the plan", or wants to begin implementing a previously created buff plan. Reads .buff/plan.md and drives the full buff development loop.
version: 0.2.0
argument-hint: "[--skip-plan] [--patch] [phase number]"
allowed-tools: Read, Write, Edit, Bash, Glob, Agent
---

# buff-execute

The execute skill drives implementation from `.buff/plan.md` through the full buff dev loop: plan → code → test → validate. It enforces discipline by default and allows targeted overrides via flags.

## First action — always

Read `.buff/plan.md` as the very first step. If it does not exist:

```
No plan found at .buff/plan.md
Run /buff:plan first, or specify a plan file: /buff:execute --plan path/to/plan.md
```

Do not proceed without a plan. Do not ask clarifying questions — the plan is the specification.

## The buff dev loop

Execute phases in strict order by default:

```
1. Plan     → read .buff/plan.md (already done)
2. Code     → implement components from plan
3. Test     → generate and run tests for implemented code
4. Validate → run /buff:validate on all modified files
5. Commit   → git commit at logical boundaries (conventional format)
```

Each phase must complete before the next begins. If a phase fails, halt and report — do not skip ahead.

## Execution workflow

### Phase: Code

For each component in `.buff/plan.md`:

1. Read any existing files in the component's directory
2. Implement following the plan's specification
3. Apply buff coding standards (see buff-code skill)
4. Track modified files in `.buff/session.log`

Order of implementation:
1. Types / schemas / interfaces first
2. Core logic / domain layer second
3. API / transport layer third
4. UI / presentation layer last

### Phase: Test

After each component implementation:

1. Invoke buff-test workflow for the implemented files
2. Run tests immediately (in execute mode, --run is implicit)
3. If tests fail, fix implementation before continuing to next component
4. Do not leave failing tests and move on

### Phase: Validate

After all components are implemented and tested:

1. Invoke buff-validate on all files modified in this session (read from `.buff/session.log`)
2. Fix all high-severity findings immediately
3. Report medium/low findings to user — fix only if user confirms
4. Log validation results to `.buff/session.log`

### Phase: Commit

After each logical feature unit (not after every file):

```bash
git add [specific files — never git add .]
git commit -m "feat([scope]): [what was implemented]"
```

Log commit hash to `.buff/session.log`.

## Flags

### `--skip-plan`
Skip the plan read step. Use only when mid-flow and the plan is already in context. Still enforces code → test → validate order.

```bash
/buff:execute --skip-plan
```

### `--patch`
Quick-iteration mode. Skips plan read and test/validate phases. For small targeted fixes where the full loop is overkill. Logs `[PATCHED - loop skipped]` to `.buff/session.log` so Counterfeit can track discipline.

```bash
/buff:execute --patch
```

### `--phase N`
Start execution from a specific phase number (1-indexed from `.buff/plan.md` phases list).

```bash
/buff:execute --phase 2
```

### `--plan <path>`
Use an alternative plan file.

```bash
/buff:execute --plan .buff/plan/components.md
```

## Session log format

Append to `.buff/session.log` throughout execution:

```
[2024-01-15T14:23:00Z] execute started — plan: .buff/plan.md
[2024-01-15T14:23:05Z] code phase — implementing: AuthService
[2024-01-15T14:24:12Z] code phase — implementing: AuthRouter
[2024-01-15T14:24:30Z] test phase — 8 tests generated, 8 passed
[2024-01-15T14:25:01Z] validate phase — 0 high, 2 med, 3 low
[2024-01-15T14:25:15Z] commit — feat(auth): add JWT authentication layer (abc1234)
[2024-01-15T14:25:15Z] --skip-plan used (1 occurrence)
```

The log is Counterfeit's source of truth for session history.

## Progress reporting

Print a compact status line before each phase:

```
[execute] Phase 2/4 — Code · implementing AuthService
[execute] Phase 3/4 — Test · running 8 tests
[execute] Phase 4/4 — Validate · scanning 3 files
[execute] Done · 2 commits, 8 tests passing, 0 high findings
```

## Plan phase tracking

After completing each plan phase, mark it done in `.buff/plan.md`:

```markdown
### Phase 1 — Foundation ✓
- [x] Task 1
- [x] Task 2
```

This keeps `.buff/plan.md` as a live progress tracker, not just an initial document.

## Handling plan ambiguity

If the plan is underspecified for a component, do not guess — report:

```
Plan is ambiguous for [component]: [what's missing]
Proceeding with: [assumption made]
Update .buff/plan.md if this is wrong.
```

Log the assumption to `.buff/session.log`. Never silently deviate from the plan.

