---
name: diagnose
description: "Investigate unexpected behavior and mysterious bugs. Use when the cause of a problem is unknown and the user needs to understand WHY something is happening — symptoms like: sudden unexplained changes in metrics or behavior, works locally but not in staging/production, inconsistent or intermittent failures, correct code producing wrong results, operations succeeding but having no effect, environment-specific failures, duplicate executions, stale data, or any \"why did this change?\" or \"why is this happening?\" situation. Covers infrastructure anomalies (cache hit rates dropping, latency spikes, queue behavior shifts) as well as code bugs. The key signal is confusion about root cause, not a request to implement a known fix. Do NOT use for feature requests, known fixes, planning, or documentation tasks."
argument-hint: bug-description
---

Think harder.

## Process

Check conversation context and skip completed steps.

### 1. Understand the symptom
- Read the bug report, errors, logs, and surrounding code carefully
- Clarify reproduction steps, expected behavior, and environment when they are unclear
- **Separate confirmed facts from working assumptions.** List them explicitly:
  - `Fact (confirmed):` the server returns 200
  - `Assumption (unconfirmed):` the client receives the full HTML body
  Misidentifying an assumption as a fact is the most common source of wasted investigation.

### 2. Build hypotheses
- Form 2-4 plausible root-cause hypotheses that are **mechanistically distinct** — different failure layers (e.g., server render vs. client hydration vs. network layer), not variations of the same idea
- Rank them by likelihood
- For each hypothesis, state both sides:
  - `Confirm if:` [what observation would prove this is the cause]
  - `Eliminate if:` [what observation would rule this out]

  A hypothesis you can't falsify in both directions is too vague to test.

### 3. Choose the lightest evidence method
Start with the cheapest source of truth that can kill hypotheses:
- existing logs, traces, stack traces, metrics, and error output
- static code inspection around the suspected path
- config, environment, deploy, cache, queue, and permissions state that could explain the symptom
- targeted reproduction in the relevant environment

Only add new instrumentation when existing evidence is insufficient.
- If you need runtime probes, read `diagnose/references/runtime-debugging.md`
- Use `#region agent log` / `#endregion` markers for any instrumentation you add
- Tag each log point with the relevant `hypothesisId`
- Log only the minimum fields needed to discriminate between hypotheses; never log secrets, tokens, passwords, cookies, or full sensitive payloads
- If runtime probes require starting the local debug server, ask the user before launching it
- For browser/UI bugs, combine with the `agent-browser` skill when reproduction or inspection needs it

### 4. Gather evidence and iterate
- Use existing logs, traces, failing tests, or artifacts before asking for a fresh reproduction
- When reproduction is needed, ask the user to trigger the bug — tie each request to the hypothesis it tests
- Correlate each finding with the hypothesis it supports or eliminates; narrow based on evidence, not confidence
- If ambiguity remains, refine hypotheses and add narrower probes — but stop and report when another round is unlikely to produce new discriminating evidence

### 5. Report the diagnosis

Output structured diagnosis:

```
## Diagnosis: [Issue Title]

### Symptoms
- [What was observed]

### Evidence
- [Finding] — `file:line` or runtime source — hypothesis X
- ...

### Root Cause
[Confirmed or most likely cause, with evidence]

### Hypotheses Tested
| # | Hypothesis | Confirm if | Eliminate if | Result |
|---|-----------|-----------|-------------|--------|
| A | ... | [what observation would prove this] | [what observation would rule this out] | Confirmed/Eliminated/Inconclusive |

### Recommended Next Steps
- [What to do next — usually hand off to `/fix` with this diagnosis]

### Active Instrumentation
- [List files with `#region agent log` blocks still in place, or `None`]
```

## Constraints

- NO fixing — investigation and diagnosis only. "Recommended Next Steps" hands off to `/fix` with the diagnosis; it does **not** prescribe specific parameter values, code snippets, or step-by-step implementation instructions.
- Evidence over assumptions — if the code looks wrong but runtime evidence says otherwise, trust the runtime
- If you add `#region agent log` blocks, leave them in place for `/fix` to verify the repair and call them out in the final report

## Bug

<bug>$ARGUMENTS</bug>
