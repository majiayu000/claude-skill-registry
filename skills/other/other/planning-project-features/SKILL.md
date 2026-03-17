---
name: planning-project-features
description: Create implementation plans for features within a single project. Decomposes work into self-contained sub-plans with iterative multi-agent review. Use when planning new features, refactoring efforts, or any multi-step implementation. Never assumes or fills in gaps - always asks for clarification until requirements are complete.
---

# Planning Project Features

Create thorough, actionable implementation plans for features within a single project. **Never assume or guess** — ask until every gap is filled.

Plans are decomposed into a **master plan** (high-level orchestration) and **sub-plans** (self-contained, independently executable units). Before finalization, plans go through an **iterative multi-agent review loop** that surfaces architectural issues, risks, and implementation problems. This structure ensures that even the least capable executing agent can pick up a sub-plan and succeed without additional context.

## Core Principles

1. **No Assumptions**: If something is unclear, ambiguous, or missing — ask. Do not fill in gaps with reasonable defaults or best guesses.
2. **Relentless Clarification**: Ask as many questions as needed. A plan built on assumptions is worse than no plan.
3. **Atomic Decomposition**: Break work into the smallest self-contained sub-plans possible. Each sub-plan should be executable in isolation.
4. **Embedded Context**: Each sub-plan includes everything an executing agent needs — no reliance on reading other sub-plans or external documents.
5. **Convergent Review**: Plans are reviewed iteratively by specialized sub-agents until no new issues are found.

## Workflow

### Phase 1: Requirement Gathering

Before writing any plan, gather complete information:

1. **Understand the goal**: What problem does this solve? What does success look like?
2. **Identify scope**: What's in scope? What's explicitly out of scope?
3. **Map dependencies**: What existing code/systems does this touch?
4. **Clarify constraints**: Performance requirements? Backward compatibility? Tech stack restrictions?
5. **Define acceptance criteria**: How will we know it's done correctly?

**Ask questions until you can answer all of the above confidently.**

If the user says "just figure it out" or "use your judgment":
1. **First, educate**: Present the options you see, explain trade-offs, and help them make an informed decision
2. **If they persist**: Respect their choice to "vibe-code" and proceed with your best judgment, but document your assumptions clearly in the plan

### Phase 2: Codebase Exploration

Once requirements are clear:

1. **Read existing documentation first**: Check AGENTS.md for documentation pointers, then read relevant docs (domain, architecture, business processes, components). Existing documentation is dramatically cheaper than re-exploring code from scratch.
2. **Explore code only for gaps**: Search for relevant code, patterns, and conventions that documentation doesn't cover.
3. Identify files that will need modification
4. Note any architectural constraints or patterns to follow
5. Flag potential conflicts or risks
6. **Identify required skills**: Determine which skills (both global from `~/.claude/skills/` and local from `.claude/skills/`) an executing agent will need to follow project conventions correctly (e.g., `writing-go-code` for Go changes, `managing-chezmoi` for dotfile edits). Check the project's `AGENTS.md` for documented skill mappings.
7. **Flag documentation gaps**: If critical areas needed for the plan are undocumented, note them. Recommend the appropriate documenting skill:
   - Missing domain knowledge → `documenting-domain`
   - Missing architecture overview → `documenting-architecture`
   - Missing business workflow docs → `documenting-business-processes`
   - Missing component docs → `documenting-components`

   Present gaps to the user — they may want to create docs before planning continues, or accept the gap and proceed.

Share findings with the user and confirm understanding before proceeding.

### Phase 3: Decomposition

This is the most critical phase. Break the feature into sub-plans:

1. **Identify natural boundaries**: Look for seams in the work — different layers (data model, API, UI), different domains, or different files/modules.
2. **Minimize dependencies**: Each sub-plan should depend on as few other sub-plans as possible. Where dependencies exist, make them explicit and one-directional.
3. **Embed all necessary context**: Each sub-plan must include the interfaces, data shapes, conventions, and file contents an executing agent needs. Don't assume the agent has read the master plan or any other sub-plan.
4. **Define clear inputs and outputs**: If sub-plan B depends on sub-plan A, sub-plan B must specify exactly what it expects to exist (e.g., "a `UserService` interface in `internal/service/user.go` with methods `Create(ctx, user) error` and `GetByID(ctx, id) (User, error)`").
5. **Keep sub-plans small**: A good sub-plan should be completable in a single focused session. If it feels too big, split it further.
6. **Plan documentation updates as a sub-plan**: If the feature affects documented domain concepts, architecture, or business processes, add a final sub-plan that updates those docs. This sub-plan is planned upfront — the planner already knows what's changing and can specify exactly which docs to update, which new docs to create, and which existing docs to use as structural patterns. This makes documentation updates human-reviewable alongside the rest of the plan. See [Documentation Sub-Plan](#documentation-sub-plan) for guidance on what belongs here vs. post-execution review.

Present the decomposition to the user for review before writing the actual plan files.

### Phase 4: Plan Creation, Reviewer Assignment & Model Selection

Only after Phases 1-3 are complete:

1. **Create the plan directory and files**:

```
.claude/plans/<feature-name>/
├── 00-master.md          # Master plan: overview, ordering, dependencies
├── 01-<first-task>.md    # Sub-plan 1
├── 02-<second-task>.md   # Sub-plan 2
├── reviews/              # Review output (created during Phase 5)
└── ...
```

2. **Discover available local reviewers**: Read the project's `.claude/agents/` directory to find reviewer agents. Match each sub-plan to the most appropriate available reviewer based on the agent's description and the sub-plan's domain.

3. **Assign reviewers**: Write the chosen reviewer's name into each sub-plan's `## Reviewer` field.

4. **Validate**: If no suitable local reviewer exists for a sub-plan's domain, **warn the user** with a specific recommendation (e.g., "sub-plan 03 covers database migrations but no reviewer with that expertise exists in `.claude/agents/`"). Ask how to proceed — do not skip the review silently.

5. **Assign execution models**: For each sub-plan, assess complexity and recommend an execution model. This enables cost optimization by using cheaper models for straightforward work while reserving Opus for planning and review.

**Model Selection Decision Tree**:

| Use Haiku When | Use Sonnet When | Keep Opus For |
|----------------|-----------------|---------------|
| Following established patterns | Novel implementation approaches | Planning & decomposition |
| CRUD operations | Complex business logic | Architecture review |
| Straightforward integrations | Multiple edge cases to consider | Risk assessment |
| Test writing for existing code | Integration of multiple systems | Synthesis & coordination |
| Configuration changes | Performance-critical code | Multi-step reasoning |
| Documentation updates | Security-sensitive operations | Ambiguous requirements |
| File moves/renames | State machine implementations | |
| Simple data transformations | Error handling with recovery logic | |

**Assessment criteria**:
- **Haiku-appropriate**: Task follows clear patterns, has well-defined inputs/outputs, requires minimal decision-making
- **Sonnet-appropriate**: Task requires some architectural thinking, handles moderate complexity, balances multiple concerns
- **Opus-appropriate**: Rare for execution; only when sub-plan has residual ambiguity or requires creative problem-solving

Document the recommendation in each sub-plan's `## Execution Model` field with a brief rationale.

### Phase 5: Initial Review Loop

After plan creation and reviewer assignment, run an iterative review process **once, before the user sees the plan**. The loop continues until all reviewers report no new findings. This is the only automatic, full-scope review — post-feedback revisions follow a lighter process (see Phase 6).

#### Reviewer Agents

The review loop uses two types of reviewer agents:

**Global reviewers** (from `~/.claude/agents/`) — generic, project-agnostic:
- **`plan-architect-reviewer`** — Evaluates the decomposition, boundaries between sub-plans, dependency graph, and whether the pieces will fit together when assembled.
- **`plan-risk-reviewer`** — Identifies technical risks the planner missed: migration pitfalls, backward-compatibility landmines, missing rollback strategies, and sub-plans that may be harder or more complex than they appear.

**Local reviewers** (from `.claude/agents/`) — project-specific, domain-specialized:
- Each project defines its own reviewer agents tailored to the domains it works with (e.g., API, UI, database, infrastructure). These reviewers can preload project-specific skills via the `skills` frontmatter field for deep domain knowledge.
- The planner does not assume naming conventions — it discovers available agents and matches them to sub-plans by reading their descriptions.

#### Review Output Location

Review output is saved to `reviews/` within the plan directory, named `<plan-file>.<reviewer-type>.md`:

```
.claude/plans/<feature-name>/reviews/
├── 00-master.architect.md      # Architecture review of master plan
├── 00-master.risk.md           # Risk review of master plan
├── 01-data-model.installer.md  # Installer review of sub-plan 01
├── 02-api-layer.ci.md          # CI review of sub-plan 02
└── ...
```

**Important**: Reviewer agents return their findings as their Task response — they do not write files. The planner is responsible for writing each reviewer's output to the appropriate `reviews/` file.

This directory is ephemeral — already covered by the `.claude/plans/` ignore rule — but persists locally across sessions for reference.

#### Step 1: Master Plan Review

Launch `plan-architect-reviewer` and `plan-risk-reviewer` against the master plan (in parallel — they are independent). Pass the plan directory path so they can read all plan files and cross-reference against the codebase. Each reviewer returns its findings as a response — write them to `reviews/00-master.architect.md` and `reviews/00-master.risk.md` respectively.

Incorporate findings into both the master plan and affected sub-plans.

#### Step 2: Sub-Plan Review

After the master plan review is resolved, launch each sub-plan's assigned reviewer (from the `## Reviewer` field) against it. Sub-plan reviews can run in parallel — even when different sub-plans use different reviewers. Each reviewer returns its findings as a response — write them to `reviews/<plan-file>.<reviewer-type>.md`.

**Output normalization**: If a local reviewer's output doesn't follow the standard format (Verdict, Critical Findings, Concerns, Observations), normalize it before incorporating. The planner interprets the reviewer's findings and translates them into actionable changes to the plan.

Incorporate findings into the sub-plans. If a sub-plan review surfaces an issue that affects the master plan (e.g., a missed dependency, a boundary that needs to shift), update the master plan and re-run affected master plan reviewers.

#### Step 3: Convergence

Repeat Steps 1-2 only for affected parts until no reviewer produces new findings. Do NOT restart the entire review — only re-review plans that changed. This convergence loop applies **only within the initial review** — it does not re-trigger after user feedback in Phase 6.

The user may also request additional specialized reviewers (e.g., security, performance) for specific sub-plans. Add these on request, but they are not part of the default flow.

### Phase 6: User Approval & Feedback

Present the fully reviewed plan (master + sub-plans) along with a summary of review findings and how they were addressed. Only mark as ready when the user explicitly approves.

#### Handling User Feedback

When the user requests changes, incorporate them and then **classify each change** to determine whether re-review is needed:

| Change Type | Examples | Re-review Action |
|---|---|---|
| Cosmetic / wording | Clarify a step description, rename a sub-plan, fix typos | **None** |
| Scoped implementation detail | Add an edge case to one sub-plan, change a file path, adjust a step | **None** — planner judgment is sufficient |
| Scope adjustment within a sub-plan | Add/remove acceptance criteria, change approach for one sub-plan | Re-review **only that sub-plan** with its assigned reviewer |
| Structural change | New sub-plan added, dependency graph changed, boundaries shifted, sub-plans merged/split | Re-review affected sub-plans + `plan-architect-reviewer` on master plan |

**Default behavior**: After incorporating feedback, state what changed and recommend whether re-review is warranted. **Do not automatically re-run reviewers.** Let the user decide whether to spend the tokens. Example:

> "I've updated sub-plans 02 and 03 based on your feedback. The changes are scoped to implementation details — I don't think a re-review is needed, but I can run one if you'd like."

The user can always explicitly request a re-review regardless of change classification.

### Post-Execution: Component Documentation Review

Domain, architecture, and process documentation updates are handled by the documentation sub-plan (Phase 3, step 6) — planned upfront and human-reviewed.

**Component docs** are the exception: they describe implementation details (interfaces, internal behavior, code patterns) that may deviate from the plan during execution. For projects that have component documentation, run the `component-docs-reviewer` agent after all sub-plans complete to catch implementation-vs-plan drift in component docs.

## Plan Structures

Templates for plan files are in this skill's `references/` directory. Read them when creating plans:

- **[Master plan template][master-plan-template]** — Orchestration document structure (no implementation details)
- **[Sub-plan template][sub-plan-template]** — Self-contained execution unit structure

## Documentation Sub-Plan

When a feature affects documented domain concepts, architecture, or business processes, the planner adds a **documentation sub-plan** as the final sub-plan in the execution order. This makes doc updates part of the plan — visible, reviewable, and deliberate.

### What Goes in the Documentation Sub-Plan

| Doc Level | Planned Upfront? | Rationale |
|---|---|---|
| Domain docs | Yes | The planner knows what domain concepts are changing |
| Architecture docs | Yes | The planner knows what structural changes are happening |
| Process docs | Yes | The planner knows what flows are being added/modified |
| Component docs | **No** — post-execution | Component docs describe implementation details that may drift from the plan |

### How to Write It

The documentation sub-plan follows the standard sub-plan template but its implementation steps are doc edits, not code changes. Be specific:

- **Which existing docs to update** — file paths, which sections, what to change
- **Which new docs to create** — file paths, which existing doc to use as a structural pattern, what the new doc should cover
- **Structural pattern matching** — if existing docs follow a pattern (e.g., process steps link to sub-process docs), new additions must follow it. Specify the pattern explicitly.
- **Required skills**: List the documenting skills the executing agent needs (e.g., `documenting-business-processes` for new process docs, `documenting-domain` for new domain entries)

### When to Skip It

Skip the documentation sub-plan when:
- The feature doesn't affect any documented concepts, flows, or architecture
- The only doc impact is component-level (handled by `component-docs-reviewer` post-execution)
- No project documentation exists yet (recommend creating initial docs as a separate effort)

## Rules (Non-Negotiable)

- **Always respect model assignments during execution** — Sub-plan model assignments (Haiku, Sonnet, Opus) are deliberate cost-optimization decisions. When executing a plan, the assigned model MUST be used. If a sub-agent fails at the assigned model, diagnose and fix the failure (e.g., permission mode, tool access). Never silently fall back to executing the work on a more expensive model. If the issue cannot be resolved, stop and ask the user how to proceed.
- **Use Agent Teams for multi-plan execution — ALWAYS** — When a plan has 2+ sub-plans, ALWAYS use Agent Teams (TeamCreate) to spawn teammates for execution. This is not optional. Agent Team teammates have their own independent context windows (preserving the lead's context budget) and have full tool access including file writes. Task sub-agents (spawned via the Task tool) cannot write files regardless of permission mode and consume the main context window. Never use Task sub-agents for plan execution. If Agent Teams are unavailable or fail, STOP and ask the user — do not silently execute sub-plans on the main agent.
- **Reviewers return findings, planner writes files** — Reviewer agents (both global and local) return their findings as their Task response. They do not write files. The planner is responsible for writing review output to `reviews/<plan-file>.<reviewer-type>.md`.
- **Never write a plan based on incomplete information**
- **Never invent requirements the user didn't specify**
- **Always decompose into sub-plans** — a single monolithic plan is a failure mode
- **Each sub-plan must be self-contained** — embed context, don't reference other sub-plans
- **Always list required skills in every sub-plan** — an executing agent without the right skills will produce subpar results or get stuck
- **Always run the review loop before presenting to the user** — unreviewed plans are draft plans, not finished plans
- **Save plans to `.claude/plans/<feature-name>/`** in the local repository — not to `~/.claude/`, and never with random/generated filenames
- **Ask for clarification even if it feels repetitive** — it's better than introducing garbage

[master-plan-template]: references/master-plan-template.md
[sub-plan-template]: references/sub-plan-template.md
