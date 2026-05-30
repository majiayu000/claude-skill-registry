---
name: scope-project
description: Adversarial project planning workflow. Explores the problem space, drafts tickets in batches, then runs sequential adversarial loops — a mandatory UX loop ("should we build this?"), zero or more discretionary specialist loops (security, performance) for projects with architectural implications in those domains, and a mandatory implementer loop ("could we build this?") — to find gaps before implementation. Creates well-specified, batch-tagged tickets upstream only after every applicable loop signs off.
model: opus
---

# Scope Project - Adversarial Project Planning

Thoroughly plans an entire project through exploration, iterative ticket drafting, and adversarial review. A planner drafts tickets; an implementer challenges them. Only when the implementer is satisfied that every ticket could be implemented without unanswered questions do the tickets go upstream.

**This skill does NOT write code.** It explores, questions, plans, and creates tickets.

## Philosophy

**Planning is cheaper than rework.** A gap discovered during planning costs minutes to fix. The same gap discovered during implementation costs hours — and may cascade into other tickets. A UX gap discovered after release costs more still. A security gap discovered after release can be catastrophic. Invest heavily in planning quality.

**Adversarial loops catch classes of gap that self-review misses.** The mandatory UX loop asks "should we build this?" — surfacing user-experience traps, mental-model misfits, dead ends, and missing recovery paths. The mandatory implementer loop asks "could we build this?" — surfacing vague requirements, unclear dependencies, and missing tickets. Different lenses catch different gaps; the planner has blind spots in both.

**Discretionary specialist loops handle architectural quality concerns.** Security and performance often have architectural implications best addressed at planning time, not bolted on after implementation. When a project has load-bearing concerns in those domains, a specialist loop runs between the UX and implementer loops. These loops are *discretionary* — invoked only when context warrants — to avoid checklist behavior on projects where the domain isn't load-bearing.

**The architectural filter governs specialist loop invocation.** Invoke a specialist loop only when the concern would require an architectural change to fix later, not a localized code edit. This filter is what prevents discretionary loops from becoming mandatory checklists. Most a11y work is implementation-time and fails the filter; most security and performance concerns in load-bearing domains pass it.

**Locked elements are constraints, not negotiations.** Each adversarial loop produces "locked" elements — UX-locked, security-locked, performance-locked — that downstream loops cannot negotiate away on grounds of effort. The implementer cannot rewrite an approved auth model because it complicates the build. The escape hatch — implementer-surfaced infeasibility loops back to whichever loop locked the element — preserves this discipline while handling the rare case where intent and physical feasibility conflict.

**Convergence is the goal, not perfection.** Each loop iterates until its reviewer is satisfied, not until every conceivable edge case is documented. Use judgment about when tickets are "good enough" — detailed enough to implement without guessing, sound enough on every applicable quality dimension, but not so verbose they become novels.

**Batch structure is a planning decision.** Tickets go upstream already tagged with their batch assignment. The batch structure should reflect real implementation dependencies, not arbitrary grouping.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                  SCOPE PROJECT WORKFLOW                       │
├──────────────────────────────────────────────────────────────┤
│  1. Project discovery (dialogue with user)                   │
│  2. Codebase exploration                                     │
│  3. Draft project plan + identify applicable specialist      │
│     loops (present to user for approval)                     │
│  4. Create .tickets/ staging directory                       │
│  5. Draft tickets (subagent per ticket)                      │
│  6. UX adversarial review loop (mandatory):                  │
│     ├─ UX reviewer reviews all tickets                       │
│     ├─ Planner addresses feedback                            │
│     ├─ Repeat until UX reviewer signs off                    │
│     └─ Escalate to human if stalemated                       │
│  7. Specialist adversarial review loops (discretionary):     │
│     ├─ Security loop (if applicable, runs first)             │
│     ├─ Performance loop (if applicable, runs second)         │
│     ├─ Each: agent reviews, planner addresses, repeat        │
│     ├─ Andon cord: escalate to user if findings exceed       │
│     │  what planning can resolve                             │
│     └─ Skip entirely if no specialist loops apply            │
│  8. Implementation adversarial review loop (mandatory):      │
│     ├─ Implementer reviews all tickets                       │
│     ├─ Planner addresses feedback                            │
│     ├─ Escape hatch: infeasibility against any locked        │
│     │  element → relevant loop (step 6 or step 7)            │
│     ├─ Repeat until implementer signs off                    │
│     └─ Escalate to human if stalemated                       │
│  9. Present final tickets to user                            │
│ 10. Cut tickets upstream (subagent per ticket)               │
│ 11. Clean up .tickets/ directory                             │
└──────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Project Discovery

**Understand what the user wants to build.** This is a dialogue — ask probing questions to get a precise picture of the project.

**Questions to explore:**
- What is the project's goal? What problem does it solve?
- What's the scope? What's explicitly out of scope?
- Are there existing systems this interacts with?
- What are the constraints? (Timeline, technology, compatibility)
- Are there natural phases or batches? What depends on what?
- What does "done" look like for the whole project?

**Push back on vagueness.** If the user says "add authentication," ask: what kind? OAuth? JWT? Session-based? What providers? What permissions model? The goal is precision.

**Output:** Clear, shared understanding of the project and its boundaries.

### 2. Codebase Exploration

**Explore the codebase to understand context.** Use exploration agents and tools to map out:

- Current architecture and conventions
- Code areas that will be affected
- Existing patterns to follow or extend
- Integration points and constraints
- Third-party dependencies involved

**For third-party dependencies:**
- Use WebFetch to read API documentation
- Clone relevant repositories to `/tmp` for examination if needed
- Understand integration points and constraints

**Output:** Comprehensive understanding of the codebase as it relates to the project.

### 3. Draft Project Plan

Synthesize the discovery and exploration into a structured project plan.

**The plan should include:**

**Project summary:**
- Goal and scope (1-2 paragraphs)
- Key technical decisions and rationale

**Batch structure:**
- How many batches, and what's the ordering rationale
- Dependencies between batches
- What each batch delivers (a coherent increment)

**Ticket inventory:**
- List of tickets per batch (title + one-line summary)
- Dependencies between tickets (within and across batches)
- Estimated scope per ticket (qualitative: small / medium / large)

**Risk areas:**
- Tickets that seem underspecified
- Cross-cutting concerns that span multiple tickets
- Integration risks between batches

**Applicable specialist loops:**

Apply the architectural filter (see step 7) to the plan and identify which specialist loops will run. For each candidate loop, state:

- Whether it applies (yes / no), and the architectural rationale
- If yes, which specific aspects of the plan it will scrutinize

This is the planner's recommendation; the user gets a veto in the next step. Locking the decision here, before drafting begins, prevents mid-flow renegotiation and gives the user full visibility into what reviews the project will receive.

**Present the plan to the user for approval.** This is the primary human checkpoint — the user should agree with the project structure, batch grouping, ticket inventory, and applicable specialist loops before detailed ticket drafting begins.

**Wait for user approval before proceeding.** The user may adjust batches, add/remove tickets, reorder, override the planner's specialist-loop selection (add a loop the planner skipped, or skip a loop the planner included), or ask questions. Iterate until approved.

### 4. Create Staging Directory

Create a `.tickets/` directory in the repository root, organized by batch:

```
.tickets/
├── batch-1/
│   ├── 01-<slug>.md
│   ├── 02-<slug>.md
│   └── 03-<slug>.md
└── batch-2/
    ├── 01-<slug>.md
    └── 02-<slug>.md
```

The numbering reflects execution order within each batch. The slug is derived from the ticket title.

**Add `.tickets/` to `.gitignore`** to prevent accidental commits of staging artifacts.

### 5. Draft Tickets

**Spawn one subagent per ticket** to draft ticket content. Each subagent receives:
- The approved project plan (from step 3)
- The codebase exploration findings relevant to that ticket
- The ticket's position in the batch structure (what comes before it, what depends on it)

**Each subagent writes a markdown file** in the `.tickets/` directory following this format:

```markdown
---
title: <ticket title>
batch: <batch name>
order: <execution order within batch>
depends_on: []
labels: [batch-N, <other labels>]
---

## Problem Statement
[What problem does this ticket solve? Why is it needed?]

## Proposed Solution
[High-level approach — what to build, not how to build it line-by-line]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

## Technical Notes
[Implementation considerations, affected components, relevant code paths]
- Affected files: [list key files]
- Key functions: [list functions to modify/create]
- Patterns to follow: [existing patterns in the codebase]
- Security considerations: [if applicable — new attack surface, input handling, auth/authz changes, trust boundary impacts]

## Implementation Notes
[Guidance for the implementer — current function signatures, module
boundaries, integration points. The kind of context that saves the
implementer from having to rediscover what the planner already found.]

## Dependencies
- Depends on: [list ticket slugs this depends on]
- Blocks: [list ticket slugs that depend on this]

## Out of Scope
[What explicitly will NOT be done in this ticket]
```

**Subagent coordination:**
- Subagents run in parallel where possible (independent tickets)
- Sequential for tickets with dependencies (later ticket needs to reference earlier ticket's content)
- Each subagent writes its file and reports completion

### 6. UX Adversarial Review Loop

This loop runs **before** the implementer review. UX issues become hard constraints on the implementation discussion — they are not items the implementer can negotiate away on grounds of effort.

The technical loop catches "could I build this?" reliably, but never asks "should this be built this way?". That is what this loop catches: features that work but trap users, surfaces that imply a mental model the user does not share, dead ends with no recovery, expert tools that lock out novices.

#### 6a. Spawn UX Reviewer

**Spawn a fresh `ux-reviewer` agent** to review the entire ticket set.

The reviewer reads all tickets together (not ticket-by-ticket — coherence across tickets is part of what it evaluates) and walks a fixed seven-concern spine:

1. **Coherence** — consistent mental model across tickets?
2. **Completeness** — implicit user needs unaddressed? Dead ends?
3. **Mental-model fit** — surface matches how users will think?
4. **Implicit knowledge** — what must users already know?
5. **Failure paths** — recovery legible when things go wrong?
6. **Power/novice tension** — both served, or one privileged?
7. **Orientation** — does the user know where they are and what's next?

The agent auto-detects target type (CLI / MCP server / webapp / library / mixed) from project signals and adapts the *evidence it inspects* by type, but walks all seven concerns regardless. If the target type is ambiguous, it asks you to clarify.

**Prompt the reviewer with:**

```
You are reviewing a draft ticket set as a UX advocate before implementation
begins. Your role is adversarial: find user-experience problems while they
are still cheap to fix.

Review *all tickets together* — coherence across tickets is part of your
evaluation. Walk the seven-concern spine systematically:

1. Coherence — consistent mental model across tickets?
2. Completeness — implicit user needs unaddressed? Dead ends?
3. Mental-model fit — surface matches how users will think?
4. Implicit knowledge — what must users already know?
5. Failure paths — recovery legible when things go wrong?
6. Power/novice tension — both served, or one privileged?
7. Orientation — does the user know where they are and what's next?

Auto-detect target type (CLI / MCP / webapp / library / mixed) from
project signals. If ambiguous, ask the orchestrator. Adapt the *evidence
you look at* by target type, but walk all seven concerns regardless.

Categorize findings: blocker / concern / suggestion. Issue verdict:
APPROVED or NEEDS REVISION.

Do not critique technical implementation choices — that is the
implementer's lens, not yours.
```

#### 6b. Planner Addresses UX Feedback

The orchestrator (you, the planner) reviews each finding and responds:

- **Blockers:** Must be addressed. Revise the affected ticket(s) so the UX issue is resolved.
- **Concerns:** Address them, or document explicitly why the concern is acceptable in this context. Don't silently dismiss.
- **Suggestions:** Use judgment. Accept those that improve the design; decline those that over-specify.

**Asking the human is normal.** If the UX reviewer surfaces a question about user populations, intended audience, or design intent that you genuinely cannot answer, ask the user. UX questions surfaced here cost minutes; the same questions surfaced after release cost rework or shipped traps.

**Update the `.tickets/` files** with revisions. UX-locked elements — concept names, error semantics, command/tool names, workflow shapes the reviewer approved — become hard constraints. The downstream reviews (specialist loops in step 7, implementer in step 8) must not negotiate them away on grounds of effort. If the implementer later surfaces an infeasibility that breaks one of these, that is the escape hatch back to step 6, not a license to revise UX unilaterally.

#### 6c. Re-Review

**Spawn a fresh `ux-reviewer`** (clean context) to review the revised tickets. The fresh instance prevents anchoring on prior findings.

**Repeat steps 6a-6c until:**

- The reviewer returns `APPROVED` — the design is UX-cogent across the seven concerns
- **Or** the process has stalemated — same blockers cycling without resolution

**On stalemate:** Escalate to the human. UX stalemate usually means a design intent the user has not made explicit — exactly what this loop is designed to surface. Present the unresolved findings and ask for direction.

**There is no hard iteration cap.** Convergence is the goal. Most projects converge in 1-2 rounds at this loop because the spine is fixed and the planner has more visibility into the design than into implementation feasibility.

### 7. Specialist Adversarial Review Loops

This step runs zero or more discretionary specialist adversarial loops between the UX loop (mandatory) and the implementer loop (mandatory). Specialist loops catch architectural quality concerns — security, performance — that the design-intent and feasibility loops miss but that are catastrophic to bolt on after implementation.

**If no specialist loops apply (per the architectural filter and step 3 selection), skip this step entirely.** Most projects do not need specialist loops. The discipline is in *not* invoking them when they aren't load-bearing.

#### The Architectural Filter (Load-Bearing Meta-Rule)

Before any specialist loop is invoked, apply this filter:

> **Would this concern require an architectural change to fix later, or is it a localized code edit?**

If the concern is *architectural* — design-shaping, expensive to rework after implementation — invoke the specialist loop. If the concern is *localized* — a code-level fix the implementer review or downstream code review will catch — do not invoke the loop.

The architectural filter is what prevents this step from becoming a mandatory checklist. It is the *first thing* you consider before any trigger heuristic. A project that mentions "auth" does not automatically need the security loop — apply the filter: does this auth choice have architectural implications (trust model, session storage strategy, multi-tenancy isolation), or is it a known pattern with off-the-shelf controls (well-trodden bcrypt + JWT in a single-tenant app)?

#### Trigger Heuristics

Triggers operationalize the architectural filter. They are *necessary but not sufficient* signals — a project missing the trigger is unlikely to need the loop, but a project hitting the trigger still needs the architectural filter applied before invoking.

| Loop          | Triggers                                                                                            |
|---------------|-----------------------------------------------------------------------------------------------------|
| Security      | Auth, registration, sessions, crypto, PII, payments, file uploads, multi-tenancy, trust boundaries  |
| Performance   | Hot paths, large-scale data, real-time / latency-sensitive, batch processing at scale               |

#### Loop Order

When multiple specialist loops apply, run them sequentially in this order:

1. **Security loop** — runs first. Security findings are rarely negotiable; security-locked elements should already be in scope before performance is evaluated.
2. **Performance loop** — runs second. Performance often trades off against security (caching introduces auth-context concerns; precomputation introduces stale-data risks). With security-locked elements already in place, performance review proceeds with those constraints visible.

#### Per-Loop Structure

Each specialist loop mirrors the UX loop:

1. **Spawn the specialist agent** to review the entire ticket set
2. **Planner addresses findings** — revise tickets, ask the user, accept/decline suggestions
3. **Spawn a fresh agent instance** for re-review (prevents anchoring)
4. **Repeat until APPROVED** or until stalemated (escalate to user)

Findings approved by the loop become **specialist-locked** elements (security-locked, performance-locked) — hard constraints on the implementer review in step 8. The implementer cannot negotiate them away on grounds of effort.

#### Andon Cord

The planner has authority to escalate to the user at any point during a specialist loop, not just on stalemate. Pull the cord when:

- The loop produces findings that exceed what planning can resolve (e.g., the security reviewer surfaces a fundamental design question only the user can answer)
- The loop seems to be off-rails (e.g., the agent is producing findings outside its lens)
- A finding warrants human judgment before the loop continues

This is broader than the stalemate escalation — proactive, planner-initiated, available at any round.

#### 7a. Security Loop (if applicable)

**Spawn `sec-blue-teamer` agent** to review the entire ticket set.

**Spec-time prompt adaptation.** The agent normally audits implemented code. For this invocation, frame the task as spec-time design review:

```
You are reviewing a draft ticket set as a spec-time security advocate.
This is NOT a code audit. There is no implementation yet — only tickets
describing the proposed design.

Evaluate the design's security posture:

1. Threat model — what trust boundaries does the proposed design imply?
   What attackers should the design defend against, and does it?
2. Control surface — what defensive controls are implied by the tickets?
   Are required controls represented as tickets, or assumed?
3. Architectural choices — does the proposed design lock in poor security
   posture (e.g., shared session store across tenants, secrets in
   user-visible URLs, trust assumptions that won't hold at scale)?
4. Missing tickets — what controls or design decisions does the project
   need that no ticket covers (rate limiting, audit logging, key rotation,
   credential recovery, lockout policies)?

Findings should be design-shaping, not code-level. Do not flag code
quality, library choice, or implementation details — those belong to
the implementer review and downstream code review.

Categorize findings: blocker / concern / suggestion.
Issue verdict: APPROVED or NEEDS REVISION.
```

**Planner addresses findings** following the same pattern as the UX loop:

- **Blockers:** Must be addressed. Revise tickets.
- **Concerns:** Address them or document explicitly why they are acceptable.
- **Suggestions:** Use judgment.

Security-approved elements become **security-locked**. The implementer cannot rewrite the auth model, threat boundaries, or required controls on grounds of build complexity.

#### 7b. Performance Loop (if applicable)

**Spawn `swe-perf-reviewer` agent** to review the entire ticket set.

**Spec-time prompt adaptation:**

```
You are reviewing a draft ticket set as a spec-time performance advocate.
This is NOT a code-level performance audit. There is no implementation
yet — only tickets describing the proposed design.

Evaluate the design's performance posture:

1. Architectural choices — do the proposed approaches have viable
   performance paths at the project's expected scale? (E.g., does the
   data flow imply N+1 queries by construction? Does the proposed
   batching strategy support the throughput requirement?)
2. Scaling characteristics — where does the design imply contention,
   serialization, or fan-out that limits scalability?
3. Missing tickets — what performance-related work does the project
   need that no ticket covers (benchmarking, indexing, caching strategy,
   load testing, profiling instrumentation)?
4. Trade-offs — does the design make performance trade-offs the user
   should be explicit about (consistency vs. latency, freshness vs.
   throughput)?

Findings should be design-shaping, not code-level. Do not flag
algorithmic complexity of individual functions, micro-optimizations,
or implementation choices — those belong to the implementer review
and downstream code review.

Categorize findings: blocker / concern / suggestion.
Issue verdict: APPROVED or NEEDS REVISION.
```

**Planner addresses findings** as in the security loop.

Performance-approved elements become **performance-locked**.

#### Why A11y Is Not in the Initial Loop Pool

A11y is excluded from the discretionary loop pool. Most accessibility work — color contrast, alt text, form labels, ARIA attributes — is implementation-time. The architectural filter would rarely admit it; these are localized code edits, not architectural rework.

Genuinely architectural a11y concerns exist (custom controls vs. native HTML, keyboard-first interaction patterns, focus-management strategy for SPAs), but they are rare. If a project surfaces a real architectural a11y concern, the planner can still spawn `qa-web-a11y-reviewer` ad-hoc with similar spec-time prompt adaptation. Codifying a11y as a standing discretionary loop is YAGNI.

### 8. Implementation Adversarial Review Loop

This is where the planner-implementer dialectic catches technical gaps. A planner and an implementer iterate on the tickets until the implementer is satisfied.

**Locked elements from steps 6 and 7 are constraints, not items the implementer can negotiate away.** UX-locked, security-locked, and performance-locked elements stand. The implementer reviews implementability against those constraints; it does not get a second pass at design intent or quality posture.

**Escape hatch back to the relevant prior loop:** If the implementer surfaces a finding that cannot be addressed without changing a locked element (e.g., "the proposed UX requires synchronous network calls that aren't possible here," or "the security-locked threat model can't be enforced without shared state the architecture doesn't support"), return to the loop that locked the element with the new constraint as input. The relevant reviewer iterates with the constraint in scope, the loop converges, and you resume step 8. This prevents implementer-wins-by-default — design and quality requirements stand unless physically infeasible. Document the constraint that triggered the loop-back so the receiving reviewer has it.

#### 8a. Spawn Implementer

**Spawn a fresh implementer agent** to review all tickets. Select the appropriate agent type:

- If the project is primarily in one language with a dedicated SME (Go, Zig, Docker, Makefile, GraphQL, Ansible): spawn that SME
- If mixed-language or no dedicated SME: spawn a general-purpose agent

**The implementer's mandate:** Review every ticket as if you were assigned to implement it tomorrow. Identify anything that would leave you guessing, blocked, or making assumptions.

**Prompt the implementer with:**
```
You are reviewing a set of project tickets as a prospective implementer.
Your job is adversarial: find every gap, ambiguity, missing dependency,
and unanswered question. Be thorough and specific.

For each ticket, evaluate:
1. Could I implement this without guessing? Are requirements precise?
2. Are acceptance criteria testable and unambiguous?
3. Are dependencies explicit? Do I know what must exist before I start?
4. Are there missing tickets? Work that's assumed but not assigned?
5. Do any tickets overlap or conflict?
6. Is the batch assignment correct? Any forward dependencies within a batch?
7. Are implementation notes accurate? Do code references check out?
8. Is anything out of scope that shouldn't be?

Also evaluate the project holistically:
- Are there gaps between tickets? Work that falls through the cracks?
- Is the batch ordering sound?
- Are cross-cutting concerns addressed?

Produce a structured review with:
- Per-ticket findings (categorized: blocker / question / suggestion)
- Cross-ticket findings
- Missing ticket proposals (if any)
- Verdict: APPROVED or NEEDS REVISION
```

#### 8b. Planner Addresses Feedback

The orchestrator (you, the planner) reviews the implementer's findings and addresses each one:

- **Blockers:** Must be resolved. Revise the affected ticket(s).
- **Questions:** Answer them — either by revising the ticket to include the answer, or by asking the human for clarification.
- **Suggestions:** Use judgment — accept valuable suggestions, decline ones that over-specify.
- **Missing tickets:** Draft new tickets if the gap is real. Decline if the work is genuinely out of scope.
- **Batch reassignments:** Adjust batch structure if the implementer's reasoning is sound.

**Asking the human is normal and productive.** If the implementer surfaces a question that the planner genuinely can't answer (design decision, business requirement, user preference), ask the human. This is the workflow working as intended — surfacing questions during planning rather than during implementation.

**Update the `.tickets/` files** with revisions. If new tickets are added or batch structure changes, update the directory structure accordingly.

#### 8c. Re-Review

**Spawn a fresh implementer agent** (clean context) to review the revised tickets. The fresh instance prevents anchoring on previous findings.

**Repeat steps 8a-8c until:**
- The implementer returns `APPROVED` — all tickets are implementable without guessing
- **Or** the process has stalemated — the same issues keep cycling without resolution
- **Or** the implementer surfaces an infeasibility against any locked element — return to the loop that locked it (step 6 for UX-locked, step 7 for security-locked or performance-locked) with the new constraint, then resume step 8 once that loop reconverges

**On stalemate:** Escalate to the human. Present the unresolved issues and ask for direction. The planner and implementer may have a legitimate disagreement that requires human judgment.

**There is no hard iteration cap.** The goal is convergence. Most projects should converge in 2-3 rounds. If it takes more, something fundamental may be underspecified — which is exactly what this workflow is designed to surface.

### 9. Present Final Tickets to User

After the implementer approves, present the complete ticket set to the user:

**Summary view:**
```
## Project Plan: <name>

### Batch 1: <name>
1. <title> — <one-line summary>
2. <title> — <one-line summary>
3. <title> — <one-line summary>

### Batch 2: <name>
1. <title> — <one-line summary>
2. <title> — <one-line summary>

### Review Summary
- Total tickets: N
- Adversarial review rounds: N
- Human clarifications requested: N
- Missing tickets identified during review: N
```

**Offer to show full ticket details** for any ticket the user wants to inspect.

**Wait for user approval.** The user may request final adjustments before tickets go upstream.

### 10. Cut Tickets Upstream

**Detect issue tracker** per [`references/trackers.md`](../../references/trackers.md).

**Create batch labels/tags first:**
- For each batch, create a label (e.g., `batch-1`, `batch-2`) if it doesn't already exist
- Use a consistent color scheme or prefix for batch labels

**Spawn one subagent per ticket** to create issues upstream. Each subagent:
- Creates the issue with title and body (from the `.tickets/` file)
- Applies labels: batch tag + any additional labels from the ticket frontmatter
- Reports back with the issue URL and number

**Subagent coordination:**
- Create tickets within a batch sequentially (so earlier tickets can be referenced by later ones in "depends on" links)
- Batches can be processed in parallel if the tracker supports it

**After all tickets are created, present the results:**
```
## Tickets Created

### Batch 1: <name> (label: batch-1)
- #12: <title> — <url>
- #13: <title> — <url>
- #14: <title> — <url>

### Batch 2: <name> (label: batch-2)
- #15: <title> — <url>
- #16: <title> — <url>

All N tickets created successfully.
```

### 11. Clean Up

- Remove the `.tickets/` directory
- Remove the `.tickets/` entry from `.gitignore` (if this workflow added it)
- Confirm cleanup is complete

## Ticket Quality Criteria

The implementer evaluates tickets against these criteria:

| Criterion                                | What it means                                                                                          |
|------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Implementable without guessing**       | Requirements are precise enough that two different developers would build substantially the same thing  |
| **Testable acceptance criteria**         | Each criterion can be verified with a concrete action ("run X, expect Y"), not a subjective judgment ("it should be fast") |
| **Explicit dependencies**               | Every ticket states what must exist before work begins — no implicit "presumably ticket A runs first"  |
| **No batch-internal forward dependencies** | Ticket B in batch 1 must not depend on ticket C in batch 1 if C comes after B in execution order     |
| **No gaps**                              | Every piece of necessary work is assigned to a ticket — nothing falls through the cracks               |
| **No overlaps**                          | No two tickets modify the same code in conflicting ways                                                |
| **Accurate code references**            | File paths, function names, and module references in technical/implementation notes are correct         |
| **Appropriate scope**                    | Each ticket is a coherent unit of work — not so large it's unmanageable, not so small it's trivial     |

## Agent Coordination

**Sequential phases:**
- Steps 1-3 are interactive with the user (sequential)
- Step 5 uses parallel subagents for ticket drafting
- Step 6 is sequential (planner → UX reviewer → planner → ...)
- Step 7 is sequential per applicable loop (planner → specialist → planner → ...); loops run in order (security before performance)
- Step 8 is sequential (planner → implementer → planner → ...)
- Step 10 uses parallel subagents for ticket creation

**Context management:**
- The orchestrator maintains the project plan and tracks revision history for every loop that runs
- Ticket drafting subagents receive focused context (just their ticket's scope)
- Review agents receive all tickets but no review history
- Fresh agent instances per review round in every loop (prevents anchoring)
- Specialist agents (sec-blue-teamer, swe-perf-reviewer) receive spec-time prompt adaptation per the per-loop invocation prompts in step 7

**State:**
- `.tickets/` directory is the source of truth for ticket content
- The orchestrator tracks: per-loop review round counts, unresolved issues, human clarifications requested, locked elements per loop (UX-locked, security-locked, performance-locked) so downstream reviews honor them, the set of applicable specialist loops chosen at step 3, and any escape-hatch loop-backs from step 8 to step 6 or step 7

## Abort Conditions

**Escalate to human:**
- Any loop's iteration has stalemated (UX, security, performance, or implementer — same blockers cycling)
- Andon cord pulled: planner judges that a specialist loop's findings exceed what planning can resolve, or the loop is off-rails
- Fundamental ambiguity that only the user can resolve
- Issue tracker unavailable or tickets can't be created

**Abort entire workflow:**
- User interrupts
- Critical system error

**Do NOT abort for:**
- Any reviewer finding many issues in round 1 (that's the workflow working)
- Multiple rounds of revision in any loop (convergence takes time)
- An escape-hatch loop-back from step 8 to step 6 or step 7 (normal and productive — surfaces a real conflict between locked-element intent and implementation feasibility)
- Skipping step 7 entirely because no specialist loops apply (the architectural filter working as intended)
- Human clarification needed (normal and productive)

## Integration with Other Skills

**Relationship to `/scope`:**
- `/scope` explores and creates a single ticket interactively
- `/scope-project` plans an entire project with adversarial review
- `/scope-project` uses a lighter-weight ticket drafting process (subagents with project context) rather than invoking full `/scope` per ticket
- For individual tickets that prove deeply underspecified during adversarial review, the orchestrator may invoke `/scope` as targeted escalation

**Relationship to `/implement-project`:**
- `/scope-project` creates tickets; `/implement-project` implements them
- Tickets go upstream already tagged with batch labels that `/implement-project` consumes
- Typical flow: `/scope-project` → `/implement-project`

## Example Session

```
User: /scope-project

What project are you planning?
> I want to add MCP server support to our CLI tool. It should expose
  the tool's core functionality as MCP tools, handle JSON-RPC, and
  support stdio transport.

Let me explore the codebase to understand the current architecture...

[Codebase exploration: CLI structure, command handlers,
 existing transport code, third-party MCP libraries]

A few questions:
- Which commands should be exposed as MCP tools? All of them, or a subset?
- Should the MCP server be a subcommand (`tool mcp-server`) or a separate binary?
- Any authentication requirements for the MCP transport?
> All commands. Subcommand. No auth needed for stdio.

## Project Plan

### Batch 1: Core MCP Infrastructure
1. Add MCP server subcommand — entry point, stdio transport, JSON-RPC handler
2. Define MCP tool schema — map CLI commands to MCP tool definitions
3. Implement tool dispatch — route MCP tool calls to existing command handlers

### Batch 2: Tool Implementations
4. Expose read commands — list, get, search as MCP tools
5. Expose write commands — create, update, delete as MCP tools
6. Add MCP resource support — expose data as MCP resources

### Batch 3: Polish
7. Error handling — map CLI errors to JSON-RPC error codes
8. Integration tests — end-to-end MCP protocol tests
9. Documentation — MCP server usage docs, tool catalog

Cross-batch dependencies: batch 2 depends on batch 1, batch 3 depends on both.

Applicable specialist loops:
- Security: NO. Stdio transport with no auth in a single-user dev tool;
  the MCP exposure is a trust-boundary concern but not architectural —
  controls are localized to the dispatch layer in ticket #4.
- Performance: NO. Tool calls are 1:1 with existing CLI commands, no
  fan-out, no scale concerns surface from the project description.

Approve this plan?
> Looks good. Proceed.

Creating .tickets/ directory...
Drafting tickets (9 subagents)...
All tickets drafted.

[UX Review — Round 1]
Spawning ux-reviewer...
Target type detected: CLI (with MCP server subcommand surface)

UX reviewer findings:
- BLOCKER (mental-model fit): Tickets #1-3 use "MCP tool" interchangeably
  with "CLI command". An MCP-tool-calling agent and a CLI-typing user
  have different expectations about idempotency, side effects, and
  return shape. The ticket set does not clarify which model governs.
- CONCERN (failure paths): Ticket #7 specifies error code mapping but
  no ticket covers what an MCP client sees when the underlying CLI
  command requires interactive input (confirmation prompts).
- CONCERN (orientation): No ticket addresses how an MCP client knows
  whether a long-running operation is still in progress.
- Verdict: NEEDS REVISION

Addressing UX findings...
- Tickets #1-3: Added explicit note that MCP exposure must be
  side-effect-aware; interactive commands require non-interactive
  alternatives.
- New ticket added to batch 3: "Long-running operation status reporting"
- User, the UX reviewer asks: for the interactive-input issue — should
  MCP clients see an error directing them to a non-interactive flag, or
  should the MCP layer auto-decline interactive commands?
> Auto-decline. MCP-exposed commands must be non-interactive.

[UX Review — Round 2]
Spawning fresh ux-reviewer...
- Verdict: APPROVED

[Specialist Loops — Skipped]
No specialist loops applicable per step 3 selection. Proceeding to
implementer review.

[Implementation Review — Round 1]
Spawning implementer (swe-sme-golang)...

Implementer findings:
- BLOCKER: Ticket #1 doesn't specify which MCP SDK to use or how
  JSON-RPC parsing works. I'd be guessing at the transport layer.
- BLOCKER: Ticket #2 says "map CLI commands to MCP tool definitions"
  but doesn't specify the schema format. MCP has specific schema
  requirements (JSON Schema for inputs).
- QUESTION: Ticket #6 mentions MCP resources — is this MCP spec
  resources, or something custom? The acceptance criteria are vague.
- SUGGESTION: Tickets #4 and #5 could be one ticket — the dispatch
  mechanism is the same, just different commands.
- MISSING TICKET: No ticket for MCP protocol version negotiation
  (initialize/initialized handshake).
- Verdict: NEEDS REVISION

Addressing findings...
- Ticket #1: Added MCP SDK specification, JSON-RPC transport details
- Ticket #2: Added JSON Schema mapping requirements
- Ticket #6: Clarifying with user...

User, the implementer asks: for ticket #6 (MCP resources), are these
MCP spec resources (URI-addressable data)? What data should be exposed?
> Yes, MCP spec resources. Expose the tool's config file and the
  data index as resources.

- Ticket #6: Updated with specific resources and URI scheme
- Tickets #4/#5: Keeping separate — read vs write have different
  error handling characteristics
- New ticket: Added #10 "MCP protocol handshake" to batch 1

[Implementation Review — Round 2]
Spawning fresh implementer...

Implementer findings:
- SUGGESTION: Ticket #10 (handshake) should come before #2 in
  execution order — can't define tools before the protocol is set up.
- SUGGESTION: Ticket #8 implementation notes should reference the
  specific MCP SDK test utilities.
- Verdict: APPROVED (with minor suggestions)

Addressing suggestions...
- Reordered batch 1: #1, #10, #2, #3
- Updated ticket #8 implementation notes

## Final Tickets

### Batch 1: Core MCP Infrastructure (label: batch-1)
1. Add MCP server subcommand
2. MCP protocol handshake
3. Define MCP tool schema
4. Implement tool dispatch

### Batch 2: Tool Implementations (label: batch-2)
5. Expose read commands as MCP tools
6. Expose write commands as MCP tools
7. Add MCP resource support

### Batch 3: Polish (label: batch-3)
8. Error handling and JSON-RPC error codes
9. Integration tests
10. Documentation
11. Long-running operation status reporting

UX review rounds: 2
Specialist loops: none applicable
Implementation review rounds: 2
Human clarifications: 2

Approve for upstream creation?
> Yes

Creating batch labels...
Creating tickets (11 subagents)...

## Tickets Created

### Batch 1: Core MCP Infrastructure (label: batch-1)
- #31: Add MCP server subcommand — github.com/.../issues/31
- #32: MCP protocol handshake — github.com/.../issues/32
- #33: Define MCP tool schema — github.com/.../issues/33
- #34: Implement tool dispatch — github.com/.../issues/34

### Batch 2: Tool Implementations (label: batch-2)
- #35: Expose read commands — github.com/.../issues/35
- #36: Expose write commands — github.com/.../issues/36
- #37: Add MCP resource support — github.com/.../issues/37

### Batch 3: Polish (label: batch-3)
- #38: Error handling — github.com/.../issues/38
- #39: Integration tests — github.com/.../issues/39
- #40: Documentation — github.com/.../issues/40
- #41: Long-running operation status reporting — github.com/.../issues/41

All 11 tickets created successfully.
Cleaned up .tickets/ directory.

Ready for implementation with: /implement-project all tickets tagged batch-1, batch-2, batch-3
```

## Example: Specialist Loop in Action

Abbreviated example showing the security loop on a project where the architectural filter admits it.

```
User: /scope-project

I want to add user registration and authentication. Email/password with
email verification, password reset, and session management.

[Discovery, codebase exploration...]

## Project Plan

### Batch 1: Auth foundations
1. Schema and password hashing (bcrypt, peppered)
2. Registration endpoint with email verification token
3. Login endpoint with session creation
4. Logout and session invalidation

### Batch 2: Account recovery
5. Password reset request (token issuance, email delivery)
6. Password reset confirmation (token validation, password change)

### Batch 3: Session hardening
7. Session expiration and rotation policy
8. Rate limiting on auth endpoints

Applicable specialist loops:
- Security: YES. Auth model, session storage, token generation, and
  trust boundaries are architectural choices. The architectural filter
  passes — getting these wrong would require rework, not localized
  fixes.
- Performance: NO. Auth flows are not performance-critical at expected
  scale; rate limiting is in scope but does not require an architectural
  performance review.

Approve this plan?
> Yes.

[Drafting tickets, UX loop converges in 1 round...]

[Security Loop — Round 1]
Spawning sec-blue-teamer (spec-time mode)...

Security findings:
- BLOCKER: No threat model documented. The tickets imply protection
  against credential stuffing and account takeover but never state it.
  Concrete threats and the controls that address each are missing.
- BLOCKER: Session storage strategy unspecified. Server-side sessions?
  Stateless JWTs? The choice has architectural consequences for logout
  semantics, session revocation, and horizontal scaling — and ticket #4
  (logout) presumes one model without saying which.
- CONCERN: Email verification token generation unspecified — random
  source, length, expiry. Weak tokens are a known attack class.
- CONCERN: No ticket for credential storage at rest beyond bcrypt
  hashing. Pepper storage location, key rotation strategy missing.
- MISSING TICKET: No audit logging ticket. Auth events without an audit
  trail are an architectural gap, not a code-level oversight.
- MISSING TICKET: No account lockout policy after repeated failed
  logins.
- Verdict: NEEDS REVISION

Addressing security findings...
- Added explicit threat model section to ticket #1: credential stuffing,
  account takeover, password spraying, session hijacking, enumeration.
- Locked session strategy to server-side sessions with rotation on
  privilege change. Updated ticket #4 with revocation semantics.
- Updated ticket #2: token generation must use a CSPRNG, 32 bytes,
  base64url, 24h expiry.
- Added ticket #9 (batch 3): "Pepper storage and rotation policy" —
  pepper in KMS, rotation runbook.
- Added ticket #10 (batch 1): "Authentication audit log" — log every
  auth event with structured fields, retention 90 days.
- Added ticket #11 (batch 3): "Account lockout policy" — exponential
  backoff after 5 failed attempts, lockout reset on successful login or
  password reset.

[Security Loop — Round 2]
Spawning fresh sec-blue-teamer...
- SUGGESTION: Audit log ticket should specify which events are
  user-correlated vs. system-only.
- Verdict: APPROVED

Security-locked elements:
- Threat model in ticket #1
- Server-side session strategy with rotation in ticket #4
- Token generation parameters in ticket #2
- Audit logging requirements in ticket #10
- Lockout policy in ticket #11

[Implementation Loop — Round 1, Round 2: APPROVED]
[Implementer respected security-locked elements; no escape-hatch
loop-back required.]

## Tickets Created (11 tickets, 3 batches)
UX review rounds: 1
Security loop rounds: 2
Implementation review rounds: 2

The security loop caught the threat-model gap, the session-storage
ambiguity, and three missing tickets before any code was written.
Each of those would have been an architectural rework if discovered
post-implementation.
```
