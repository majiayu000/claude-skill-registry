---
name: loop
description: Start autonomous iteration loop. Triggers on "loop", "keep going", "continue until done", "implement feature", "fix all", "loop status", "cancel loop".
model: opus
---

# Role

EXECUTE. Decompose work into waves of atomic items. Verify each, iterate
until done. Observable evidence over assumed completion. Retry with context,
not from scratch.

## Principles

1. **Every criterion maps to ≥1 work item** — If a criterion from shape
   has no corresponding work item, the decomposition is incomplete.
2. **Retry with feedback, not from scratch** — When an item fails
   verification, carry it to the next wave with `[VERIFY] FAIL: [reason]`
   so the retry transforms with context, not blindly repeats.
3. **Never ship on assumption alone** — Execution output and measurements
   are sufficient evidence. Code review ships with monitoring. Assumptions
   block until verified.
4. **mustNot violations are hard stops** — These are inviolable constraints
   from shape. When violated, stop immediately and surface to user.
5. **Holdout separation** — Generation subagents see criteria[] + mustNot[]
   (guidance + prevention). holdout[] is reserved for an independent
   verification subagent. The generator never sees the holdout set.
6. **Surface what the wave revealed** — Every wave ends with
   `[LEARN] [one domain insight the wave revealed ≤15w, not the process]`.

## Process

1. **Accept brief + shape** — Scan for intent brief (ACCEPTANCE/STOP
   criteria) and shape output (criteria[]/holdout[]/mustNot[]/shape). If
   missing, clarify before proceeding. If shape recommended Colleague mode
   and task has multiple work items, recommend team composition (bond) —
   persistent dialogue serves understanding better than fire-and-forget
   subagents.

2. **Decompose** — Break into 5-21 atomic work items. Each passes the
   "one sentence without and" test. Every criteria[] entry maps to ≥1
   item. Mark dependencies between items. If Disposable=yes from shape:
   keep items ≤3, expect to discard.

   Zone 3 override: decompose regardless of item count. Each item gets
   retrieval (search/read) before generation. Carry includes "retrieved
   vs assumed" in failure context.

   When decomposition requires codebase understanding (multi-module,
   unfamiliar codebase, 8+ items expected), spawn an Explore agent:
   Task(prompt="[session + criteria + mustNot] Analyze the codebase for
   [scope]. Return: files involved, module boundaries, dependencies
   between components.", subagent_type="Explore")
   Use findings to inform item breakdown. For straightforward tasks,
   decompose inline.

   Announce: `[LOOP] Starting | Shape: {shape} | Items: {N} | Feasible: {axis} — {bound}`

3. **Execute in waves** — A wave = items with no unresolved dependencies.
   Within a wave: reversible before irreversible.

   Spawn per ready item (generator sees criteria + mustNot, NOT holdout):
   `Task(prompt="[session + criteria + mustNot + ACCEPTANCE.constraints]
   [work item]", subagent_type="general-purpose")`

   After wave completes, spawn holdout verification (independent evaluator):
   `Task(prompt="[HOLDOUT-VERIFY] [holdout[] + mustNot[]]
   Evaluate work output. Per holdout item, score:
   PASS(1.0) / WEAK(0.7) / PARTIAL(0.3) / FAIL(0.0).
   Report satisfaction, confidence, basis. Do not fix.",
   subagent_type="general-purpose")`

   Wave report:
   - `[WAVE {N}] satisfaction: {0-100} | confidence: {high/med/low} | basis: {execution/observation/inspection}`
   - Per holdout item: `{item}: {score} {verdict} — {evidence}`
   - Footer: `Done: {n} | Carry: {n} | Stall: {n}`
   - `[LEARN] What this wave revealed: [one insight ≤15w]`
   - Carry = WEAK (evidence quality) or PARTIAL/FAIL (incomplete).
     Context travels WITH the retry prompt (co-located, not referenced).
   - Stall = no progress — diagnose from output, revise remaining items
   - Critical risk (13+ points or irreversible): emit comprehension probe
     per wave — one question (≤10w) targeting what changed and why.
     Standard/Trivial: probe at completion only (step 5).

   Satisfaction gating (advisory by default, blocking for critical risk):

   | Satisfaction | Standard risk | Critical risk |
   | ------------ | ------------- | ------------- |
   | ≥ 85         | → review      | → review      |
   | 60–84        | advisory      | blocking      |
   | < 60         | advisory      | blocking      |

4. **Review** — When satisfaction ≥ threshold, get expert review against
   spec and mustNot constraints. Findings: BLOCKER (must fix) / WARNING /
   SUGGESTION. BLOCKERs create new work items, return to waves.

5. **Verify + present** — Final report:
   - OUTCOME: 1 sentence + `satisfaction: {N} | confidence: {X} | basis: {Y}`
   - DECISIONS: 2-4 bullets, risk-ordered. Each states impact, not just
     action.
   - EVIDENCE: per holdout item, score + command/output that proves it.
   - DETAILS: grouped by concern, available on request.

   After verification, generate one question (≤10w) targeting where
   understanding would break. Gate: Autonomous=skip, Collaborative/Guided=emit.

   User: Adjust → re-enter | Done → complete.

### Circuit Breakers

| Trigger                           | Action                   |
| --------------------------------- | ------------------------ |
| Max iterations (user-configured)  | Pause, announce progress |
| Budget exceeded (user-configured) | Pause, offer continue    |
| mustNot violated                  | Stop immediately         |

### Cancel

"Cancel loop", "stop", "abort" → report completed/remaining. Current
wave completes before cancel.

## Boundaries

Execute against locked criteria; surface scope questions, never resolve
them. Gates flag deviations; user resolves. User owns continuation —
loop never decides to stop or continue on its own.

## Handoff

Loop is a terminal phase — it produces completed, verified work. No
outbound Skill() calls. When finished or cancelled, present results
to the user.

Back-transitions (when discovered mid-execution):

- Wrong intent → surface to user, recommend re-entering intent phase
- Approach failing → surface to user, recommend reshaping
