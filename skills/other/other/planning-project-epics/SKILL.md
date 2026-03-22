---
name: planning-project-epics
description: Decompose large efforts into sequenced features for a single project. Produces a persistent epic plan with rich feature descriptions that feed into planning-project-features separately. Use when the scope is too large for a single feature plan — multiple independently meaningful features with their own design decisions.
---

# Planning Project Epics

Decompose large efforts into sequenced, independently plannable features within a single project. The output is a persistent **epic plan** — a coordination document that lives across sessions, tracking which features are done and what comes next.

Each feature in the epic plan is described richly enough that `planning-project-features` can pick it up cold in a separate session. The epic planner does **not** invoke feature planning — the user decides when to plan each feature.

## Core Principles

1. **No Assumptions**: If something is unclear, ambiguous, or missing — ask. Do not fill in gaps with reasonable defaults or best guesses.
2. **Relentless Clarification**: Ask as many questions as needed. Requirement gathering doesn't end at Phase 1 — when later phases surface new ambiguities, **STOP and present them to the user**.
3. **Feature-Worthiness Judgment**: A feature is a unit of work with its own design decisions worth discussing. If a piece doesn't have meaningful design surface — it's either part of a broader feature or a small amendment the feature planner handles inline.
4. **Dependencies Without Contracts**: Note which features depend on which, but don't define interface shapes or signatures. The feature planner figures those out when it gets there. Cross-feature contracts emerge from feature planning, not epic planning.
5. **Rich Descriptions, Not Task Lists**: Each feature description must give the feature planner enough context to start cold — domain knowledge, relevant specs, existing code pointers, scope boundaries. Not step-by-step instructions.

## Workflow

### Phase 1: Requirement Gathering

Before any exploration, gather the big picture:

1. **Understand the goal**: What is this epic trying to achieve? What does the end state look like?
2. **Identify scope**: What's in scope for this epic? What's explicitly out of scope or deferred?
3. **Map the domain**: What domain concepts, specs, or external systems does this touch?
4. **Clarify constraints**: Timeline pressure? Tech stack restrictions? Backward compatibility requirements?
5. **Define success**: How will we know the epic is complete?

**Ask questions until you can answer all of the above confidently.**

If the user says "just figure it out" or "use your judgment":
1. **First, educate**: Present the options you see, explain trade-offs, and help them make an informed decision
2. **If they persist**: Respect their choice and proceed with your best judgment, but document your assumptions clearly in the epic plan

### Phase 2: Documentation Review

Before exploring code, read what already exists:

1. **Read existing documentation**: Check AGENTS.md for documentation pointers, then read relevant docs (domain, architecture, business processes, components). This builds understanding far cheaper than exploring code.
2. **Flag documentation gaps**: Note areas where documentation is missing or insufficient for the scope of this epic.
3. **Absorb domain language**: Adopt the terminology from existing docs — the epic plan should speak the same language as the project.

### Phase 3: Codebase Exploration

With documentation context in hand, explore what documentation didn't cover:

1. **Map the existing architecture**: Identify the systems, packages, and boundaries the epic touches.
2. **Identify existing infrastructure**: What foundations already exist that features can build on? What's missing?
3. **Find architectural seams**: Look for natural boundaries where features can be separated — different layers, different domains, different packages.
4. **Note conventions and patterns**: Existing patterns that features will need to follow.
5. **Identify required skills**: Determine which skills (global and local) feature planners will need. Check the project's `AGENTS.md` for documented skill mappings.

Share findings with the user and confirm understanding before proceeding.

### Phase 4: Requirement Refinement

After exploring the codebase, revisit Phase 1 findings:

1. **Identify conflicts**: Do any requirements conflict with the actual codebase state, existing architecture, or established patterns?
2. **Surface new questions**: Did exploration reveal ambiguities or decision points that Phase 1 didn't anticipate?
3. **Adjust scope if needed**: Some things may be easier or harder than initially expected. Present findings and let the user decide.

**Present all conflicts and new questions to the user before proceeding.** Do not silently resolve them.

### Phase 5: Feature Decomposition

This is the most critical phase. Break the epic into features:

1. **Apply the feature-worthiness test**: Does this piece have its own design decisions worth discussing? Would a developer spend meaningful time on design and trade-offs, not just implementation? If yes, it's a feature. If not, it gets absorbed into a related feature or noted as a small amendment.

2. **Find natural boundaries**: Look for:
   - Different infrastructure concerns (storage, networking, caching)
   - Different domain areas (user management, billing, content)
   - Different architectural layers that are independently meaningful
   - Pieces with distinct design trade-offs (driver selection, abstraction strategy, protocol design)

3. **Sequence by dependency**: Identify which features must come before others. Keep the dependency graph simple — deep chains of dependencies suggest the decomposition might be wrong.

4. **Identify parallel opportunities**: Features with no dependencies between them can be planned and executed independently — note this for the user's scheduling.

5. **Watch for cross-cutting concerns**: Some concerns span multiple features (error handling strategy, logging conventions, testing approach). Call these out in the epic plan so they don't get decided inconsistently across features.

Present the decomposition to the user for review before writing the epic plan.

### Phase 6: Epic Plan Creation

Only after Phases 1-5 are complete:

1. **Create the epic plan file**: Save to `.claude/plans/epics/<epic-name>.md` using the [epic plan template][epic-plan-template].

2. **Write rich feature descriptions**: Each feature section must contain enough context for a feature planner starting cold:
   - What the feature accomplishes and why it's a distinct unit
   - Domain knowledge, spec references, relevant existing code
   - Dependencies on other features (existence only — not contract shapes)
   - Scope boundaries — what's in this feature vs. adjacent ones
   - Required skills for the feature planner and executing agents

3. **Set initial status**: All features start as `not-started`.

### Phase 7: Review Loop

After plan creation, run a review using the global reviewers before presenting to the user.

**Launch in parallel:**
- **`plan-architect-reviewer`** — Evaluates feature boundaries, dependency graph, whether the decomposition will hold together when features are planned and built separately.
- **`plan-risk-reviewer`** — Identifies risks: features that may be harder than they appear, dependency chains that could cause rework, missing considerations.

Pass the epic plan file path so reviewers can read it and cross-reference against the codebase.

**Important**: Reviewer agents return their findings as their Task response — they do not write files. The epic planner writes review output to `.claude/plans/epics/reviews/<epic-name>.<reviewer-type>.md`.

Incorporate findings into the epic plan. If changes are significant enough to alter feature boundaries or dependencies, re-run only the affected reviewer(s). Do not restart the full review for minor adjustments.

### Phase 8: User Approval & Feedback

Present the reviewed epic plan with a summary of review findings and how they were addressed.

**Remind the user**: The epic plan intentionally stays at the feature level — no interface contracts, no implementation details. Those emerge during feature planning. The user reviews decomposition and sequencing now; they review design details when planning each feature.

#### Handling User Feedback

When the user requests changes, incorporate them and classify:

| Change Type | Examples | Re-review Action |
|---|---|---|
| Cosmetic / wording | Clarify a description, fix typos | **None** |
| Scope adjustment within a feature | Expand/narrow what a feature covers | **None** — planner judgment is sufficient |
| Feature boundary change | Merge features, split a feature, move scope between features | Re-review with **architect reviewer** |
| Structural change | New feature added, dependency graph changed significantly | Re-review with **both reviewers** |

**Default behavior**: After incorporating feedback, state what changed and recommend whether re-review is warranted. **Do not automatically re-run reviewers.** Let the user decide.

## Epic Plan as a Living Document

The epic plan persists across sessions. When the user returns:

- They can ask the agent to read the epic plan and identify the next feature to plan
- After a feature is planned or executed, the user (or agent, when asked) updates the feature's status
- If feature planning reveals that the epic decomposition needs adjustment (e.g., a feature should be split further, or two features should merge), update the epic plan accordingly

The user is the workflow engine — the epic plan is their coordination artifact.

## Rules (Non-Negotiable)

- **Never define cross-feature contracts** — no interface signatures, no type shapes, no API contracts. Those are the feature planner's responsibility.
- **Never write an epic plan based on incomplete information**
- **Never invent requirements the user didn't specify**
- **Every feature must pass the feature-worthiness test** — if it doesn't have design decisions worth discussing, it's not a feature
- **Always run the review loop before presenting to the user** — unreviewed epic plans are drafts
- **Save epic plans to `.claude/plans/epics/`** in the local repository — not to `~/.claude/`
- **Ask for clarification even if it feels repetitive** — it's better than a decomposition built on assumptions
- **Rich feature descriptions are mandatory** — a feature planner starting cold must be able to understand what to plan without reading the whole epic or other features

[epic-plan-template]: references/epic-plan-template.md
