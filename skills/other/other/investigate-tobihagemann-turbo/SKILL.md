---
name: investigate
description: "Systematically investigate bugs, test failures, build errors, performance issues, or unexpected behavior by cycling through characterize-isolate-hypothesize-test steps. Use when the user asks to \"investigate this bug\", \"debug this\", \"figure out why this fails\", \"find the root cause\", \"why is this broken\", \"troubleshoot this\", \"diagnose the issue\", \"what's causing this error\", \"look into this failure\", \"why is this test failing\", or \"track down this bug\"."
argument-hint: "[problem description or error message]"
---

# Investigate

Systematic methodology for finding the root cause of bugs, failures, and unexpected behavior. Cycle through characterize-isolate-hypothesize-test steps, with oracle escalation for hard problems. Diagnose the root cause — do not apply fixes. Return results for the main agent to act on.

Optional: `$ARGUMENTS` contains the problem description or error message.

## Step 1: Characterize

Gather the symptom and establish what is actually happening:

1. **Collect evidence** — error message, stack trace, test output, log entries, or user description of unexpected behavior
2. **Classify the problem type**:

| Signal | Type |
|--------|------|
| Stack trace / exception | Runtime error |
| Test assertion failure | Test failure |
| Compilation / bundler / build error | Build failure |
| Type checker error (tsc, mypy, pyright) | Type error |
| Slow response / high CPU / memory growth | Performance |
| "It does X instead of Y" / no error | Unexpected behavior |

3. **Establish reproduction** — run the failing command, test, or operation. If the problem cannot be reproduced (intermittent, environment-specific), document the constraints and proceed with historical evidence.

Record the exact reproduction command and its output for verification.

## Step 2: Isolate

Narrow from "something is wrong" to "the problem is in this area." Read [references/problem-type-playbooks.md](references/problem-type-playbooks.md) for type-specific first moves and tool sequences.

### Git Archeology

For all problem types, check what changed recently near the failure point:

```bash
git log --oneline -20 -- <file>
git blame -L <start>,<end> <file>
```

If a known-good state exists (e.g., "this worked yesterday"), consider `git bisect` to pinpoint the breaking commit.

### Scope Narrowing

- **Stack traces**: Read the throwing function and its callers — full functions, not just the flagged line
- **Test failures**: Read both the test and the system under test
- **Build errors**: Read the config file and the referenced source
- **Unexpected behavior**: Trace the data flow from input to the unexpected output

## Step 3: Hypothesize

Generate 2-4 hypotheses ranked by likelihood. Each hypothesis must be **falsifiable** — specify what evidence would confirm or refute it.

Format:

```
H1 (most likely): [description] — confirmed if [X], refuted if [Y]
H2: [description] — confirmed if [X], refuted if [Y]
H3: [description] — confirmed if [X], refuted if [Y]
```

### Parallel Investigation

For complex problems with 3+ hypotheses and a non-obvious root cause, spawn parallel investigators simultaneously.

**Spawn condition**: 3+ hypotheses AND the problem is not a simple typo, missing import, or syntax error.

**Skip** when 1-2 hypotheses are obvious (e.g., stack trace points directly to the bug).

Launch in parallel (`model: "opus"`, do not set `run_in_background`):

1. **One subagent per hypothesis** — each receives the hypothesis, relevant file paths, what evidence to look for, and instructions to report **confirmed** / **refuted** / **inconclusive** with evidence. Budget: max 5 tool calls per subagent.
2. **Codex consultation** (read-only) — launch an agent that runs the `/consult-codex` skill with a focused prompt describing the problem, reproduction, and files examined. The multi-turn conversation allows it to dig deeper into patterns the hypothesis-driven subagents miss. Run the `/evaluate-findings` skill on its output.

After all investigators complete, merge results. Codex findings that overlap with a subagent's confirmed hypothesis reinforce confidence. Novel codex findings become additional hypotheses to test in Step 4.

## Step 4: Test

Verify each hypothesis with minimal, targeted actions:

| Action Type | Tool |
|-------------|------|
| Find usage or pattern | Grep |
| Read surrounding code | Read |
| Check recent changes | Bash (`git log`, `git blame`, `git diff`) |
| Run isolated test | Bash (specific test command) |
| Check dependency version | Bash (`npm ls`, `pip3 show`, etc.) |
| Inspect runtime state | Bash (add temporary logging, run, check output) |

Record each result:

| Hypothesis | Verdict | Evidence |
|------------|---------|----------|
| H1 | confirmed / refuted / inconclusive | [what was found] |
| H2 | confirmed / refuted / inconclusive | [what was found] |

### Iteration

If all hypotheses are refuted or inconclusive:

1. Document what was learned — each refuted hypothesis eliminates a possibility and narrows the search
2. Return to Step 2 with the new information to re-isolate
3. Generate new hypotheses in Step 3 based on updated understanding

**Cycle budget**: maximum 2 full cycles (hypothesize → test → learn → repeat) before escalating.

## Escalation

After 2 failed hypothesis cycles, offer escalation to `/consult-oracle` via `AskUserQuestion`:

```
Investigation stalled after [N] hypothesis cycles.

Tested: [summary of hypotheses and evidence]
Remaining unknowns: [what is still unclear]

Escalate to Oracle? (consults external model with full context)
```

Proceed only if the user approves.

## Investigation Report

Output results as text:

```
Investigation Report:

Problem: [one-line description]
Type: [runtime error | test failure | build failure | type error | performance | unexpected behavior]
Root cause: [confirmed cause, or "unresolved" with best hypothesis]

Evidence:
- [what confirmed the root cause]

Suggested fix: [description of what to change, or "needs further investigation"]
Reproduction command: [command to verify the fix once applied]

Hypotheses tested:
1. [hypothesis] — [confirmed/refuted/inconclusive] — [evidence]
2. [hypothesis] — [confirmed/refuted/inconclusive] — [evidence]

Escalation: [none | oracle]
```

## Rules

- If the problem turns out to be environmental (wrong Node version, missing dependency, OS-specific), report that clearly — it may not require a code fix.
- If the problem is in a dependency (not the project's code), document the dependency issue and suggest workaround options rather than patching the dependency.
