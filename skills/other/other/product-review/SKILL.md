---
name: product-review
description: "Product-taste review that challenges 'are we building the right thing?' Four modes: EXPAND (dream big), HOLD (maximum rigor), REDUCE (strip to essentials), DESIGN (UX-first). Run before /spec or standalone. Use DESIGN mode for UI-heavy features."
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# /product-review

A product-taste review skill. Challenges whether you're building the right thing, scoped the right way, before you commit engineering effort. Run standalone or before `/spec` for greenfield features.

**Priority hierarchy**: Step 0 > Error Map > Failure Modes > Architecture > Everything else.

**Tone**: Opinionated. Direct. Not a rubber stamp. If the plan is wrong, say so.

---

## Step 0: Nuclear Scope Challenge

This step runs FIRST, before any review sections. It determines whether the work should exist at all.

### 0A. Premise Challenge

Ask and answer explicitly:
- Is this the right problem to solve?
- Is this the best framing of the problem?
- What happens if we do nothing? (If "nothing bad" — that's a signal.)
- Who asked for this and why? User pain vs. internal preference?
- Can agents perform this action too, or is this UI-only? If UI-only, why?
- What's the agent story? API/tool parity for every user-facing capability.

### 0B. Existing Code Leverage

Map every sub-problem in the plan to existing code:
- What already exists that solves part of this?
- What can be extended vs. what must be built new?
- Is this a rebuild of something that should be a refactor?

Output a "What Already Exists" table:

```
SUB-PROBLEM          | EXISTING CODE        | REUSE?  | NOTES
---------------------|----------------------|---------|------
                     |                      |         |
```

### 0C. Dream State Mapping

ASCII diagram showing three states:

```
CURRENT STATE          THIS PLAN              12-MONTH IDEAL
─────────────          ─────────              ──────────────
[describe]      →      [describe]      →      [describe]

Gap: ___               Gap: ___
```

Does this plan move toward the 12-month ideal, or sideways?

### 0D. Mode-Specific Analysis

Before the user selects a mode, run the analysis for ALL four to inform selection:

**EXPAND lens**:
- 10x check: If this had to serve 10x users/load/scope, what breaks?
- Platonic ideal: What would the perfect version look like, unconstrained?
- Delight opportunities: Where could this surprise users positively?

**HOLD lens**:
- Complexity check: What's the minimum set of changes to ship this?
- Risk surface: What existing behavior could this break?

**REDUCE lens**:
- Ruthless cut: What can be removed and shipped as follow-up?
- Core kernel: What's the absolute smallest thing that delivers value?

**DESIGN lens**:
- User journey mapping: What are the 3-5 primary user journeys?
- Interaction pattern audit: Right UI patterns? (modal vs drawer vs inline, wizard vs single-page)
- Information architecture: Fits user's mental model?
- Responsive strategy: Mobile-first or desktop-first? Primary device?
- Accessibility-first: What a11y requirements baked in from start?

### 0E. Temporal Interrogation (EXPAND/HOLD/DESIGN)

Which implementation decisions must be made NOW vs. can be deferred?
- Decisions with high reversal cost → decide now
- Decisions with low reversal cost → defer, don't over-specify

### 0F. Mode Selection

Present the four modes. Context-dependent defaults:
- New product/feature with unclear scope → default EXPAND
- Well-scoped change to existing system → default HOLD
- Scope creep detected, overloaded plan → default REDUCE
- Primarily UI/frontend feature → default DESIGN

Ask the user to select. **Once selected, commit fully. No drifting between modes.**

---

## Mode Quick Reference

```
BEHAVIOR               | EXPAND          | HOLD            | REDUCE          | DESIGN
------------------------|-----------------|-----------------|-----------------|------------------
Scope changes           | Add if valuable | Freeze          | Cut aggressively| Reframe as user needs
Architecture questions  | Explore options | Validate chosen | Simplify        | Map to user journeys
Edge cases              | Map all         | Map critical    | Defer non-fatal | Map user-facing ones
Test ambition           | Comprehensive   | Thorough        | Critical paths  | User flow coverage
Failure handling        | Every path      | Every path      | Fatal paths     | User-visible paths
"Nice to have" items    | Evaluate        | Reject          | Cut             | Evaluate for delight
Agent parity            | Design for it   | Verify exists   | Defer if costly | Design for it
Follow-up work          | Identify        | Identify        | Mandate         | Prioritize by user pain
```

---

## Review Sections

Run each section sequentially. **STOP after each section** and ask the user one focused question before proceeding. Each question must present 2-3 lettered options, lead with your recommendation and WHY. No batching multiple issues into one question.

### Section 1: Architecture Review

Analyze:
- Dependency graph: what depends on what? Draw it.
- Data flow through 4 paths: **happy**, **nil/null**, **empty**, **error**
- State machines: identify implicit states and transitions
- Coupling: where are the hard dependencies? What's hard to change later?
- Scaling considerations: what breaks at 10x? 100x?
- Security architecture: trust boundaries, auth flow
- Rollback posture: can you undo this deploy without data loss?
- Agent parity: for each user-facing action, is there an equivalent API/tool path? Draw the capability map.

**EXPAND adds**: "What makes this beautiful?" — is there an elegant design waiting to be found? Platform potential — does this create leverage for future features?

**DESIGN reframes**: Component hierarchy, state management approach, data flow to UI. What's the component tree? Where does state live?

Output: Architecture diagram (ASCII).

### Section 2: Error & Failure Map

Build the error table:

```
CODEPATH     | WHAT CAN GO WRONG    | ERROR TYPE  | HANDLED? | HANDLER ACTION      | USER SEES
-------------|----------------------|-------------|----------|---------------------|----------
             |                      |             |          |                     |
```

**DESIGN reframes**: User-visible error states, recovery flows, empty states. What does the user see when things go wrong?

Rules:
- Catch-all error handling is a smell. Name every error you catch.
- Every handled error must **retry**, **degrade**, or **re-raise**. Pick one.
- Swallow-and-continue is almost never acceptable. Justify each instance.
- For LLM/AI calls, treat these as distinct failure modes: malformed response, empty response, hallucinated/invalid structured output, refusal.
- For external service calls: timeout, rate limit, auth failure, unexpected response shape.

### Section 3: Security & Threat Model

**DESIGN reframes**: Client-side validation, PII display, auth UX. How does the user experience security?

Analyze:
- Attack surface: what's exposed? What's new exposure?
- Input validation: every user-controlled input, every boundary crossing
- Authorization: who can do what? Are there escalation paths?
- Secrets management: how are credentials stored, rotated, scoped?
- Dependencies: supply chain risk for new dependencies
- Data classification: PII, financial, credentials — where does sensitive data flow?
- Injection vectors: SQL, command, template, prompt injection
- Audit logging: are security-relevant actions logged?

### Section 4: Data Flow & Edge Cases

**DESIGN reframes**: Loading states, optimistic updates, stale data. What does the user see while data is in flight?

ASCII diagram:

```
INPUT → VALIDATION → TRANSFORM → PERSIST → OUTPUT
  ↓         ↓            ↓          ↓         ↓
[shadow paths: what happens when each stage fails or receives unexpected input]
```

Interaction edge cases table:

```
FEATURE A STATE  | FEATURE B STATE  | EXPECTED BEHAVIOR  | TESTED?
-----------------|------------------|--------------------|--------
                 |                  |                    |
```

### Section 5: Test Coverage Map

Diagram all new:
- UX flows (user-facing paths)
- Data flows (internal data movement)
- Codepaths (branches, conditionals)
- Async work (jobs, queues, callbacks)
- Integrations (external services)
- Error paths (from Section 2)

For each, specify:

```
FLOW/PATH          | TEST TYPE    | HAPPY PATH | FAILURE PATH | EDGE CASE
-------------------|-------------|------------|--------------|----------
                   |             |            |              |
```

**Test ambition check** (mode-dependent):
- EXPAND: "What tests would make you confident shipping this at 3am?"
- HOLD: "What tests cover every behavior change?"
- REDUCE: "What tests cover the critical paths only?"
- DESIGN: "What user flow E2E tests, visual regression tests, and a11y audits cover the experience?"

### Section 6: Deployment & Rollback

**DESIGN reframes**: Feature flags for UI, progressive rollout, A/B readiness. How do you ship UI changes safely?

Analyze:
- Migration safety: backward-compatible? Can old code run against new schema?
- Feature flags: what should be flagged? Kill switch available?
- Rollout order: what deploys first? Dependencies between deploy steps?
- Rollback plan: exact steps to undo. Data migration reversibility.
- Deploy-time risk window: what's broken between step 1 and step N of deploy?
- Post-deploy verification: how do you know it worked? What do you check?

---

## Required Outputs

After all sections, produce these deliverables.

### Failure Modes Registry

```
CODEPATH   | FAILURE MODE       | HANDLED? | TESTED? | USER SEES?  | LOGGED?
-----------|--------------------|----------|---------|-------------|--------
           |                    |          |         |             |
```

**Any row with HANDLED=N, TESTED=N, USER SEES=Silent is a CRITICAL GAP.** Call these out explicitly.

### NOT In Scope

List deferred work with rationale:

```
DEFERRED ITEM              | WHY DEFERRED              | FOLLOW-UP NEEDED?
---------------------------|---------------------------|------------------
                           |                           |
```

### Diagrams

Produce all of:
1. System architecture (components, boundaries, dependencies)
2. Data flow with shadow paths (from Section 4)
3. State machine (if applicable)
4. Error flow (from Section 2)

### Completion Summary

```
SECTION                  | FINDINGS | CRITICAL GAPS | QUESTIONS RESOLVED
-------------------------|----------|---------------|-------------------
0. Nuclear Scope         |          |               |
1. Architecture          |          |               |
2. Error & Failure Map   |          |               |
3. Security & Threat     |          |               |
4. Data Flow & Edge      |          |               |
5. Test Coverage         |          |               |
6. Deployment & Rollback |          |               |
```

### DESIGN Mode Additional Outputs

When running in DESIGN mode, also produce:

**User Journey Map (ASCII):** Primary flows with decision points and error branches.

```
USER ENTERS → [Decision Point] → Path A → [Success]
                                → Path B → [Error Recovery] → [Retry/Exit]
```

**Interaction Pattern Decisions:**

```
INTERACTION          | PATTERN CHOSEN    | ALTERNATIVES      | WHY
---------------------|-------------------|-------------------|----
                     |                   |                   |
```

**Responsive Strategy:** Device priority, breakpoint behavior for key components.

### Agent Parity Map

```
UI ACTION              | AGENT EQUIVALENT       | STATUS
-----------------------|------------------------|--------
                       |                        | ✅/⚠️/❌
```

Any row with STATUS=❌ and no justification is a CRITICAL GAP.

### Unresolved Decisions

List any questions the user chose not to answer or deferred. These carry forward to `/spec`.

---

## Suppressions

Do NOT:
- Flag style-only suggestions (naming, formatting). That's for linters.
- Re-argue scope after mode selection. The mode is locked.
- Suggest performance optimizations. `/multi-review`'s performance-oracle covers that.
- Suggest observability/monitoring additions. Too ops-specific for product review.
- Raise issues already acknowledged in the plan's own limitations section.
