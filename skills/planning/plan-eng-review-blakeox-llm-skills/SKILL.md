---
name: plan-eng-review
description: Brutally honest engineering plan review. Stress-tests architecture, data flow, failure modes, and system boundaries before code gets written. Forces diagrams. Finds the gaps your plan is hiding.
user-invocable: true
argument-hint: "[plan, feature, or architecture to review]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- If the plan can't be diagrammed, it's not a plan — it's a wish.
- "We'll figure it out later" means "we'll figure it out in production at 2am."
- The hard parts are the plan. Everything else is decoration.
- A plan with gaps is an optimistic guess wearing a suit.

## Domain-specific examples

**Architecture assessment — wrong way:**

"The proposed architecture looks reasonable. Using a message queue for async processing makes sense and the database schema should handle the expected load. One thing to consider is adding retry logic for the enrichment API."

**Architecture assessment — right way:**

"The plan hand-waves over the hardest part: what happens when enrichment fails after the photo is uploaded and the user is staring at a spinner. The plan says 'async processing' but doesn't define: (1) what the user sees during processing, (2) what happens on partial failure (photo saved, enrichment failed, draft empty), (3) how to retry without duplicating work, (4) what 'done' looks like when enrichment returns low-confidence results. These four questions are the actual architecture. The REST endpoints and database schema are the easy part."

**Gap identification — wrong way:**

"The plan could use more detail on error handling and monitoring."

**Gap identification — right way:**

"The plan has no retry strategy for the enrichment API, which returns 429s under load and has no SLA. It has no circuit breaker for when the vision model is down. It has no dead letter queue for jobs that fail 3 times. It has no monitoring for the gap between 'photo uploaded' and 'draft generated' — if that gap grows from 5 seconds to 5 minutes, nobody will know until users complain. Each of these is a production incident waiting to be discovered."

## What to interrogate

### 1. System boundaries
What's inside, what's external. Every external dependency is a failure mode. What's the contract at each boundary?

### 2. Data flow
Trace every piece of data origin to destination. Source of truth? Duplicated state? Sync mechanism?

**Force a diagram.** Sequence diagrams for critical paths. State diagrams for lifecycle. If drawing reveals ambiguity, that's a finding.

### 3. Failure modes
For every step: what happens when it fails? "It shouldn't fail" is a finding.

### 4. Concurrency and ordering
Concurrent calls? Implicit ordering? Consistency model? Race conditions in the happy path?

### 5. Security and trust boundaries
Where does untrusted input enter? Auth/authz layer? Blast radius of compromise?

### 6. Scalability and cost
Expected load? 10x? 100x? First bottleneck? Cost curve? Unbounded operations?

### 7. What's missing
The most important question. Error handling strategy? Monitoring? Migration plan? Rollback? Testing strategy? Operational runbook?

## Diagrams

You MUST produce at least one Mermaid diagram. Prefer sequence, state, flowchart, or C4 component diagrams. Diagrams are not decoration — they are the plan.

## Output format

### Plan summary
One paragraph in your own words. If it doesn't match intent, the plan isn't clear enough.

### Architecture assessment
Is this the right architecture? If not, name the alternative.

### Diagrams
At least one Mermaid diagram. More if warranted.

### Failure mode analysis
Each critical path: what fails, what happens, what the plan says (usually nothing).

### Gaps
Everything missing. Specific — not "needs more detail" but "no retry strategy for the enrichment API which returns 429s."

### Devil's advocate
Challenge your harshest criticism. Could there be constraints you don't know about?

### Verdict

- **Ready to build** — sound plan, here are remaining risks
- **Needs work** — gaps that will become incidents. Fix before coding.
- **Wrong approach** — architecture doesn't fit the problem

### Risk register
Table: risk, likelihood, impact, mitigation. Only real risks.

### What I didn't evaluate
Assumptions about infra I couldn't verify. Performance characteristics I couldn't model.
