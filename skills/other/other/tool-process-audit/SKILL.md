---
name: tool-process-audit
description: Diagnose a named or described business/engineering process for bottlenecks, risks, and optimization opportunities. Use when a user asks to review, map, or improve a workflow and wants concrete next steps with effort/impact tradeoffs.
operating_mode: ANALYSIS + RECOMMENDATIONS
trigger_conditions: process review, workflow audit, bottleneck diagnosis, operational improvement, process mapping
related_skills: lp-do-critique, lp-do-fact-find
---

# Process Audit

Audit a business or engineering process end-to-end. Confirm what process is in scope, map current state, test for failure/inefficiency, and return ranked, actionable improvements.

Keep momentum high: avoid long interviews unless ambiguity or risk justifies deeper questioning.

## Relationship to Other Skills

- `lp-do-critique`: Critiques document quality. Use this skill for process reality and operational performance.
- `lp-do-fact-find`: Produces planning artifacts for feature/build work. Use this skill for process diagnosis and optimization recommendations.

## Inputs

| Input | Required | Notes |
|------|----------|-------|
| Process name or description | Yes | One sentence is enough to start. |
| Optional focus tests | No | User-specified lenses (for example: compliance, handoffs, cost, automation). |
| Optional artifacts | No | SOPs, checklists, tickets, logs, screenshots, dashboards. |

If the user gives minimal detail, proceed with a normal walkthrough audit and clearly mark assumptions.

## Operating Mode

**CONFIRM -> MAP -> TEST -> RANK -> RECOMMEND**

**Allowed:**
- Ask targeted clarifying questions (max 5 per turn)
- Infer missing details and mark confidence as `Observed`, `Inferred`, or `Unknown`
- Produce recommendations with explicit effort/impact tradeoffs

**Not allowed:**
- Stalling for perfect information
- Proposing major redesigns before mapping current state
- Presenting unverified assumptions as facts

## Workflow

### 1) Intake

Request:
1. Process name or description
2. Optional artifacts (SOP, checklist, tickets, logs, screenshots)

Then reply with a one-sentence understanding and ask for confirm/correct.

### 2) Disambiguation (only when uncertainty exists)

If process scope is ambiguous:
1. Present 2-4 candidate interpretations (`A/B/C/...`), each in 1-2 sentences.
2. State assumptions for each candidate.
3. Ask the user to select or correct.

Clarifying-question priority (max 5 in one turn):
1. Primary goal/output
2. Trigger/start condition
3. End condition / done definition
4. Roles/owners
5. Tools/systems

If uncertainty is low, skip directly to confirmation and continue.

### 3) Scope What to Test

Ask once:
`Do you need anything specific tested (for example bottlenecks, failure modes, compliance, cost, automation, UX, handoffs, controls, metrics)?`

- If user specifies tests: treat them as primary lenses.
- If not: run the default walkthrough lenses in Step 5.

### 4) Map Current State

Build a process map:
`Trigger -> Steps -> Handoffs -> Decision points -> End state`

For each step, capture when available:
- owner/role
- inputs
- outputs
- tools/systems
- time/latency (or queue wait)
- dependencies
- failure modes

Use `Unknown` explicitly when data is missing.

### 5) Run Audit Lenses

Default lenses (run unless user narrows scope):
1. Bottlenecks and queues (wait states, batching, WIP overload)
2. Rework and defects (ambiguity, defects, repeat handling)
3. Handoffs (ownership gaps, context loss, duplicate effort)
4. Controls and risk (approval gaps, audit trail weakness, compliance exposure)
5. Measurement (missing KPIs, no leading indicators, no feedback loop)
6. Automation leverage (manual repetitive work, reconciliation, copy/paste)
7. Scalability (what breaks at 2x and 10x volume)
8. User experience where applicable (friction, drop-offs, unclear instructions)

### 6) Rank Findings

For each issue, score:
- `Impact` (1-5)
- `Frequency` (1-5)
- `Detectability difficulty` (1-5; 5 = hard to detect)
- `Effort to fix` (`S`, `M`, `L`)

Priority score:
`Priority = Impact x Frequency x Detectability difficulty`

Sort by:
1. Higher priority score
2. Higher impact
3. Lower effort (`S` before `M` before `L`)

Each finding must include:
- issue statement
- root-cause hypothesis
- evidence confidence (`Observed | Inferred | Unknown`)
- recommended fix (concrete action)
- effort estimate (`S/M/L`)
- expected impact

### 7) Build Optimization Plan

Group recommendations into:
- **Quick wins (0-2 days)**
- **Medium fixes (1-2 weeks)**
- **Structural redesign (multi-role/system changes)**

For each recommendation, include an owner suggestion and a measurable success signal.

### 8) High-Stakes Risk Rule

If legal, financial, safety, or major compliance risk appears:
1. Flag it explicitly as `High-stakes risk`.
2. Prioritize immediate controls before optimization work.
3. State what evidence is missing and what verification is needed next.

## Output Contract (Required Order)

Always deliver in this exact order:

1. **Confirmed process definition** (1-3 sentences)
2. **Process map** (numbered steps + decision points + key handoffs)
3. **Issues and risks** (ranked with scoring rationale)
4. **Optimizations** (quick wins + medium + structural)
5. **Recommended next steps** (first actions, owner suggestions, and what info would improve confidence)

## Response Template

Use this compact structure:

```md
## Confirmed process definition
...

## Process map
1. ...
2. ...
Decision points: ...
Handoffs: ...

## Issues and risks (ranked)
1. <Issue>
   - Score: Impact <n> x Frequency <n> x Detectability <n> = <n>
   - Confidence: Observed | Inferred | Unknown
   - Root cause: ...
   - Fix: ...
   - Effort: S | M | L
   - Expected impact: ...

## Optimizations
### Quick wins (0-2 days)
- ...
### Medium fixes (1-2 weeks)
- ...
### Structural redesign
- ...

## Recommended next steps
1. ...
2. ...
3. ...
Confidence boosters: ...
```

## Quality Bar

- Do not stop at generic advice; every top issue needs a concrete fix.
- Keep assumptions visible and minimal.
- Prefer the smallest effective change before structural redesign.
- If evidence is thin, provide the best current audit plus a clear data-collection next step.
