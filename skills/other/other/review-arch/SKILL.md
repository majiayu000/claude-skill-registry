---
name: review-arch
description: Architectural review workflow. Analyzes codebase organization via noun analysis and produces a target blueprint. Advisory only — does not implement changes. Always offers to cut tickets for the planned work; orchestrators receive the proposal and apply their own autonomy judgment to approve / edit / decline.
model: opus
---

# Arch Review — Advisory Architectural Analysis

Analyzes codebase architecture and produces a target blueprint via noun analysis. **Advisory only.** The skill does not implement changes — it surfaces opportunities and offers to cut tickets so the work can be picked up by implementation skills. The offer goes to the operator (human or orchestrator) regardless of caller; orchestrators apply their own autonomy judgment to approve / edit / decline.

## Philosophy

**Review and implementation are different concerns.** A skill that does both makes both worse — implementation pressure compromises the review, and review pressure compromises the implementation. The plugin is moving `/review-*` skills toward advisory-only over time (see the "Advisory aspiration" section of [`references/autonomy.md`](../../references/autonomy.md)); `/review-arch` is the first concrete step in that direction.

**Clarity through organization is the goal.** Every module should have a clear identity — a domain noun it owns. Functions should live where a reader expects to find them. DRY and Prune serve this organizational goal, not the other way around.

**Recommend boldly.** The analysis agent surfaces every opportunity it finds, even uncertain ones — the operator can always reject a recommendation when reviewing the plan. The skill's job is to *see*, not to *act*.

**Single workflow for everyone.** The skill's workflow is identical whether a human operator or an orchestrator (`/refactor-deep`, `/implement-project`, `/lead-project`) is at the receiving end. After the analysis, the skill presents a proposed ticket structure for the recommended work; the operator (human or orchestrator) approves, edits, or declines. Orchestrators apply their own autonomy judgment per [`references/autonomy.md`](../../references/autonomy.md) — declining items they intend to implement inline, approving items they want tracked for later.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│           ARCH REVIEW WORKFLOW (advisory)                       │
├─────────────────────────────────────────────────────────────────┤
│  1. Determine scope                                             │
│  2. Spawn swe-arch-reviewer agent (full analysis)               │
│     → returns dead code list + target blueprint                 │
│  3. Present analysis to operator                                │
│  4. Iterate on plan with operator                               │
│  5. Offer to cut tickets                                        │
│     ├─ Preview ticket set                                       │
│     ├─ Operator approves / edits / declines                     │
│     └─ Create approved tickets in tracker with labels           │
│  6. Completion summary                                          │
│     └─ Tickets created (or "no tickets — analysis only")        │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Scope:** Default is the entire codebase. If the caller specifies a path or module, respect that scope. Pass scope to the analysis agent.

### 2. Analyze Codebase

**Spawn fresh `swe-arch-reviewer` agent:**

The agent performs four sequential analysis steps:

1. Catalogs dead code for removal
2. Builds a domain model via noun analysis
3. Catalogs repetition patterns
4. Produces a target architecture blueprint

**Prompt the agent with:**
```
Perform a full architectural analysis of this codebase.
Scope: [entire codebase | user-specified scope]
Produce a comprehensive target architecture blueprint showing where
everything should live. Cover every module — existing and proposed.
```

The agent returns:
- A noun frequency table (the primary analytical artifact)
- A per-noun namespace evaluation
- A dead code list
- A repetition catalog (DRY candidates, resolved in the blueprint)
- A target architecture blueprint (existing modules + proposed new modules)
- Any linter/formatter issues observed
- Any behavior-altering implications worth flagging

**If the agent reports "No refactoring needed":** Workflow complete. Skip to step 6 (completion summary) with an empty findings list.

### 3. Present Analysis to Operator

After the analysis agent returns, present its findings to the operator (human or orchestrator). The operator needs to see the full picture before deciding what to do.

**Present three things:**

**a) Noun analysis.** Show the noun frequency table and the per-noun namespace evaluations. This is the analytical foundation — the user should understand what nouns the agent identified, how frequently they appear, and why they do or don't deserve their own namespace.

**b) Proposed changes.** Show the blueprint items — modules to change, absorb, dissolve, or rename, plus proposed new modules. For each item, include the agent's rationale. Group by category (dead code removal, renames, moves, absorptions, dissolutions, new modules).

**c) No-change items.** Show the modules the agent evaluated and explicitly decided to leave alone, with their domain justifications. This is important context — the operator may disagree and want to add items, or may spot a module the agent missed entirely.

### 4. Iterate on Plan with Operator

The operator has the full analysis. Give them the opportunity to shape the plan before any tickets are cut.

**The operator may want to:**
- Remove items they disagree with
- Add items the agent missed
- Modify proposed changes (e.g., "move that function to module X instead of Y")
- Ask questions about specific recommendations ("why did you flag this as dead code?")
- Adjust the scope based on what they see
- Reprioritize items

**Continue iterating until the operator is satisfied with the plan.** Don't rush this — architectural decisions are consequential and benefit from deliberation.

When invoked by an orchestrator, the orchestrator applies its own judgment to the iteration step: it may remove items it intends to implement inline as part of its workflow, add items it wants tracked that the agent missed in its narrow analysis, or reprioritize based on the larger project context. See [`references/autonomy.md`](../../references/autonomy.md) for the orchestrator's discretion in this kind of plan-shaping decision.

### 5. Offer to Cut Tickets

Once the plan is finalized, offer to convert the planned work into tickets. **This is the only place the skill writes to anything outside the working tree.**

**Generate a draft ticket per blueprint item.** Group related items into a single ticket if doing so makes the work cohesive (e.g., "dissolve helpers.go: distribute its 6 functions" is one ticket, not six). Each ticket includes:

- **Title** — short, action-oriented (e.g., "Dissolve helpers.go; distribute functions to domain owners").
- **Description** — the rationale from the blueprint plus the specific moves/renames involved.
- **Recommended implementation skill** — name the skill that should pick this up, with scope hint. Examples:
  - "Implementation: `/refactor` with scope `src/utils/`" (for mechanical changes within an existing module)
  - "Implementation: `/scope` first to plan dependencies, then `/implement`" (for new module creation)
  - "Implementation: `/implement-batch` with this ticket plus the related `request.go` absorption ticket" (for cross-cutting changes)
- **Acceptance criteria** — what "done" looks like for this ticket (tests still pass, specific symbols moved, specific files removed).

**Preview the full ticket set to the operator.** Show all tickets at once so the operator can see the whole plan. The operator can:

- Approve as-is
- Edit titles, descriptions, or acceptance criteria
- Remove tickets they don't want cut (decline)
- Add labels (default to no labels; offer common candidates: `refactor`, `tech-debt`, `arch`)

When invoked by an orchestrator, the orchestrator applies its own autonomy judgment to the approve/edit/decline decision — typically declining items it intends to implement inline as part of its workflow and approving items it wants tracked for follow-up. Either response is valid; the skill doesn't presume one outcome.

**On approval, create tickets in the tracker.** Detect the tracker using the same pattern as `/scope`:
- GitHub → `gh` CLI
- Gitea → `mcp__gitea__*` MCP tools
- GitLab → `glab` CLI

Capture each ticket's URL or number for the completion summary.

**If the operator declines to cut tickets:** That's a valid outcome. Note in the completion summary that the analysis was advisory-only — the orchestrator (or operator) may still act on the analysis without tickets.

### 6. Completion Summary

```
## Arch Review Complete

### Scope
[Entire codebase | caller-specified scope]

### Analysis statistics
- Modules evaluated: N
- Blueprint items proposed: N
- Dead code items identified: N
- Items removed during iteration: N
- Items finalized for ticket creation: N

### Tickets created
- #123: Dissolve helpers.go; distribute functions — recommends /refactor scoped to pkg/helpers
- #124: Absorb validate() into request.go — recommends /refactor scoped to pkg/request and pkg/server
- ...

(or: "No tickets created — analysis was advisory-only per operator request.")

### Recommended next steps
[Brief paragraph naming the natural follow-up. Examples:
 - "Tickets are labeled `arch`; consider `/implement-batch` to work through them as a cohesive unit."
 - "Single ticket — run `/implement` when ready."
 - "No tickets cut — analysis stands as a planning artifact; revisit when you have time to act on it."
 - When invoked by an orchestrator: "Tickets are now in the tracker for deferred follow-up; orchestrator declined N items to handle inline."]
```

## Agent Coordination

**Sequential execution:**
- The analysis agent runs once per invocation. Fresh instance per invocation.
- No SME agents are spawned by this skill (no implementation).
- No QA agents are spawned by this skill (no changes to verify).

**State to maintain (as orchestrator):**
- Scope
- Analysis output from `swe-arch-reviewer`
- The iterating plan as the operator shapes it
- Ticket URLs/numbers created (if any)

## Abort Conditions

**Abort the workflow:**
- Analysis agent fails or returns malformed output — retry once; if it fails again, surface the error.
- Operator interrupts during iteration.
- Tracker is unavailable when the operator has approved ticket creation — surface the error; preserve the approved ticket set in the completion summary so the operator can create them manually.

**Do NOT abort for:**
- Empty findings — that's a valid outcome. Report "no architectural improvements identified" and exit cleanly.
- Operator declining to cut tickets — analysis stands as a planning artifact.

## Integration with Other Skills

**`/review-arch` vs `/refactor`:** `/refactor` is tactical cleanup within existing architecture. `/review-arch` is strategic — it questions the architecture and proposes restructuring. Use `/refactor` for routine cleanup; use `/review-arch` when the module structure itself needs rethinking. After `/review-arch`'s tickets are cut, `/refactor` and `/implement` carry them out.

**`/review-arch` vs `/scope`:** `/scope` creates individual tickets through exploratory dialogue when you already know what you want. `/review-arch` *discovers* what tickets are needed by analyzing the codebase as a whole and cuts a coherent batch from one blueprint.

## Example Session

```
> /review-arch

Scope: entire codebase

Spawning swe-arch-reviewer agent...

Analysis complete. Here's what I found:

## Noun Frequency
| Noun     | Count | Has Namespace? | Modules Where It Appears |
|----------|-------|----------------|--------------------------|
| request  | 14    | No             | Server, App, Middleware  |
...

## Proposed Changes
1. Dead code removal (4 instances across 3 files)
2. Rename parser.go → request.go (domain noun)
3. request.go absorbs validate() from server.go
4. Dissolve helpers.go; distribute its 6 functions
5. Create response.go (response construction is scattered)

## No-Change Items
- config.go — clear identity, well-scoped
- middleware.go — cohesive, correctly placed

What would you like to change about this plan?

> I agree with 1-4, but let's hold off on creating response.go.

Updated plan: 4 items.

Offer: create tickets for the 4 finalized items?
> Yes, please.

Drafting tickets...

### Ticket preview
1. Remove dead code (4 instances)
   - Implementation: /refactor scoped to {server.go, helpers.go, parser.go}
   - AC: lines listed in description are gone; tests pass

2. Rename parser.go → request.go (domain noun)
   - Implementation: /refactor scoped to parser.go
   - AC: file is renamed; all references updated; tests pass

3. request.go absorbs validate() from server.go
   - Implementation: /refactor scoped to {server.go, request.go}
   - AC: validate() lives in request.go; server.go imports nothing from request beyond what it already uses; tests pass

4. Dissolve helpers.go; distribute 6 functions
   - Implementation: /scope first (cross-module moves benefit from planning); then /implement-batch
   - AC: helpers.go is deleted; each named function has a new home documented in the ticket

Labels to apply (defaults to none)?
> arch, tech-debt

Creating tickets in Gitea...
- #201: Remove dead code (4 instances) — created
- #202: Rename parser.go → request.go — created
- #203: request.go absorbs validate() from server.go — created
- #204: Dissolve helpers.go — created

## Arch Review Complete

### Scope: entire codebase

### Analysis statistics
- Modules evaluated: 8
- Blueprint items proposed: 5
- Items removed during iteration: 1 (create response.go, deferred)
- Items finalized for ticket creation: 4

### Tickets created
- #201, #202, #203 — recommend /refactor scoped per ticket
- #204 — recommends /scope then /implement-batch

### Recommended next steps
Tickets are labeled `arch, tech-debt`. Consider `/implement-batch` to
work through #201-#203 as a cohesive unit (they touch overlapping
files); #204 deserves its own scoping pass first.
```

When invoked by an orchestrator, the same flow runs — the orchestrator receives the analysis and the ticket-structure proposal, applies its own autonomy judgment, and approves / edits / declines. There is no separate "autonomous mode" — the orchestrator is just another receiver of the same offer.
