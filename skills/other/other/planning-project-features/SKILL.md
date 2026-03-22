---
name: planning-project-features
description: Create implementation plans for features within a single project. Decomposes work into self-contained sub-plans with iterative multi-agent review. Use when planning new features, refactoring efforts, or any multi-step implementation. Never assumes or fills in gaps - always asks for clarification until requirements are complete.
---

# Planning Project Features

Create thorough, actionable implementation plans for features within a single project. **Never assume or guess** — ask until every gap is filled.

Plans are decomposed into a **master plan** (high-level orchestration) and **sub-plans** (self-contained, independently executable units). Before finalization, plans go through an **iterative multi-agent review loop** that surfaces architectural issues, risks, and implementation problems. This structure ensures that even the least capable executing agent can pick up a sub-plan and succeed without additional context.

## Core Principles

1. **No Assumptions**: If something is unclear, ambiguous, or missing — ask. Do not fill in gaps with reasonable defaults or best guesses.
2. **Relentless Clarification**: Ask as many questions as needed. A plan built on assumptions is worse than no plan. Requirement gathering doesn't end at Phase 1 — when later phases surface new ambiguities or decision points not resolved earlier, **STOP and present them to the user**. Do not make autonomous architectural decisions.
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
8. **Flag specification gaps**: When the plan depends on a specification or requirements document that doesn't cover a case the implementation needs, treat it as a **blocking gap** — not a documentation gap. Present the gap and options to the user before proceeding. Examples: an API spec that doesn't define error responses, a data model that doesn't cover edge-case states, a workflow description that omits failure paths.

Share findings with the user and confirm understanding before proceeding.

### Phase 3: Decomposition

This is the most critical phase. Break the feature into sub-plans:

1. **Identify natural boundaries**: Look for seams in the work — different layers (data model, API, UI), different domains, or different files/modules.
2. **Minimize dependencies**: Each sub-plan should depend on as few other sub-plans as possible. Where dependencies exist, make them explicit and one-directional.
3. **Embed domain knowledge and cross-boundary contracts**: Each sub-plan must be self-contained — don't assume the agent has read the master plan or other sub-plans. What belongs in a sub-plan:
   - **Domain knowledge** the agent can't derive from code: spec requirements, business rules, config formats, protocol details.
   - **Cross-boundary contracts** — exact interface/type signatures that other sub-plans depend on. When sub-plans run in parallel, the consuming agent can't discover these at execution time, so the plan must specify them. For sequential dependencies, the later agent can read the earlier sub-plan's actual output — no pre-specified contract needed.

   What does NOT belong: internal API design, function signatures within a package, private helpers, method bodies, step-by-step coding instructions, specific commands for testing/linting/building. These are the executing agent's decisions, guided by loaded skills and acceptance criteria.

   **The test**: if changing something would break a *different* sub-plan's code, it's a contract and belongs in the plan. If it only affects code within this sub-plan, it's an internal the agent owns.
4. **Keep sub-plans small**: A good sub-plan should be completable in a single focused session. If it feels too big, split it further.
5. **Skills are the agent's authority, not the plan's**: List the skills each sub-plan requires, but do NOT replicate skill content into the plan. Skills define how to write code, how to test, how to lint, how to build — the executing agent loads them and follows them. The plan defines *what* to build and *why*; skills define *how*. If a skill says "use `task test`," the plan should not say "run `go test ./...`." If a skill mandates table-driven tests, the plan should not specify test structure — the agent will follow the skill. The plan's job is to provide architectural decisions, domain knowledge, and constraints that skills don't cover. This applies to both design skills (coding conventions, test patterns) and operational skills (running tests, linting, building). If the project has skills for testing, linting, or building, list them in the sub-plan's Required Skills. The sub-plan's verification/acceptance criteria should say "all tests pass, code builds, lints clean" — not specify raw commands. The executing agent uses the loaded operational skills to determine the correct commands.
6. **Plan documentation updates as a sub-plan**: If the feature affects documented domain concepts, architecture, or business processes, add a final sub-plan that updates those docs. The planner knows which concepts, boundaries, and flows are changing — enough to specify which docs to update, which new docs to create, and which existing docs to use as structural patterns. Implementation details that affect docs will be resolved by the executing agent at documentation time. This makes documentation updates human-reviewable alongside the rest of the plan. See [Documentation Sub-Plan](#documentation-sub-plan) for guidance on what belongs here vs. post-execution review.

Present the decomposition to the user for review before writing the actual plan files.

### Phase 4: Plan Creation, Reviewer Assignment & Model Selection

Only after Phases 1-3 are complete:

1. **Create the plan directory and files**:

   **Plan location depends on context:**
   - Standalone feature: `.claude/plans/features/<feature-name>/`
   - Feature belonging to an epic: `.claude/plans/epics/<epic-name>/<feature-name>/`

   If the user references an epic plan or provides an epic context, use the epic path. Otherwise, default to standalone.

```
<plan-directory>/
├── 00-master.md          # Master plan: overview, ordering, dependencies
├── 01-<first-task>.md    # Sub-plan 1
├── 02-<second-task>.md   # Sub-plan 2
├── reviews/              # Review output (created during Phase 5)
└── ...
```

2. **Discover available local reviewers**: Read the project's local agents directory to find reviewer agents. Match each sub-plan to the most appropriate available reviewer based on the agent's description and the sub-plan's domain.

3. **Assign reviewers**: Write the chosen reviewer's name into each sub-plan's `## Reviewer` field.

4. **Validate**: If no suitable local reviewer exists for a sub-plan's domain, **warn the user** with a specific recommendation (e.g., "sub-plan 03 covers database migrations but no reviewer with that expertise exists locally"). Ask how to proceed — do not skip the review silently.

5. **Assign execution models**: For each sub-plan, assess complexity and recommend an execution model. This enables cost optimization by using cheaper models for straightforward work while reserving the most capable model for planning and review.

**Model Selection Decision Tree** — evaluate top-down, use the first tier that fits:

1. **Most capable model** — use when the sub-plan involves:
   - Ambiguous or underspecified requirements that need interpretation
   - Multi-step reasoning across multiple systems or domains
   - Novel architectural approaches with no existing pattern to follow
   - Security-sensitive operations where mistakes are costly
   - Documentation updates (see [Documentation Sub-Plan](#documentation-sub-plan))

2. **Mid-tier model** — use when the sub-plan involves:
   - Complex business logic with multiple edge cases
   - Integration of multiple systems or packages
   - Performance-critical code requiring careful trade-offs
   - State machines or error handling with recovery logic

3. **Cheapest model** — use when the sub-plan involves:
   - Following established patterns already present in the codebase
   - CRUD operations, straightforward integrations, configuration changes
   - File moves/renames, simple data transformations
   - Test writing for existing code with clear acceptance criteria

When in doubt, prefer one tier up — the cost of a wrong model choice is rework, which is more expensive than the model difference.

Document the recommendation in each sub-plan's `## Execution Model` field with a brief rationale.

6. **Ensure worker agents exist for execution**: Each sub-plan's model + skills combination needs a matching worker agent definition. Worker agents are the **only reliable mechanism** for controlling which model a sub-agent runs on — model selection via natural language prompts or team configuration is unreliable.

   **Search for existing workers**: Check both local and global agent directories. An agent is a match if its `model` field and `skills` list cover the sub-plan's requirements. A partial match (correct model but incomplete skills, or correct skills but different model) can serve as a basis for a new worker — clone and adapt rather than starting from scratch.

   **Create missing workers**: If no matching worker exists, create one following this format:

   - **Naming convention**: `{model-tier}-{domain}-worker.md` (e.g., `mid-go-worker.md`, `cheap-docs-worker.md`). Domain should reflect the skills baked in; model tier should match the decision tree terminology.
   - **Placement**: Always local (project-level agents directory), since skills are typically project-local.
   - **Frontmatter rules**:
     - `description` MUST be a quoted single-line YAML string with `\n` escapes. Multiline descriptions break frontmatter parsing and the agent won't be discovered.
     - `model`: set to the target model identifier — this is what actually controls the execution model.
     - `skills`: list of skill names to preload into the agent's context at startup. The agent does not need to load skills manually.
     - Do NOT set `tools` unless you need to restrict access — omit for full tool access.
   - **System prompt**: Brief role description. The sub-plan provides all task context; the agent definition provides model, skills, and identity.

   **Warn the user**: Newly created worker agents may require a session restart to be discovered. Note this when presenting the plan.

### Phase 5: Initial Review Loop

After plan creation and reviewer assignment, run an iterative review process **once, before the user sees the plan**. The loop continues until all reviewers report no new findings. This is the only automatic, full-scope review — post-feedback revisions follow a lighter process (see Phase 6).

#### Reviewer Agents

The review loop uses two types of reviewer agents:

**Global reviewers** (from the global agents directory) — generic, project-agnostic:
- **`plan-architect-reviewer`** — Evaluates the decomposition, boundaries between sub-plans, dependency graph, and whether the pieces will fit together when assembled.
- **`plan-risk-reviewer`** — Identifies technical risks the planner missed: migration pitfalls, backward-compatibility landmines, missing rollback strategies, and sub-plans that may be harder or more complex than they appear.

**Local reviewers** (from the local agents directory) — project-specific, domain-specialized:
- Each project defines its own reviewer agents tailored to the domains it works with (e.g., API, UI, database, infrastructure). These reviewers can preload project-specific skills via the `skills` frontmatter field for deep domain knowledge.
- The planner does not assume naming conventions — it discovers available agents and matches them to sub-plans by reading their descriptions.

#### Review Output Location

Review output is saved to `reviews/` within the plan directory, named `<plan-file>.<reviewer-type>.md`:

```
<plan-directory>/reviews/
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

Reviewers evaluate architecture, contracts, constraints, and acceptance criteria — not implementation details (which are no longer in the plan). If a reviewer suggests adding implementation specifics ("specify which encoder method to use"), reject the suggestion — that's the executing agent's domain.

Incorporate findings into both the master plan and affected sub-plans.

#### Step 2: Sub-Plan Review

After the master plan review is resolved, launch each sub-plan's assigned reviewer (from the `## Reviewer` field) against it. Sub-plan reviews can run in parallel — even when different sub-plans use different reviewers. Each reviewer returns its findings as a response — write them to `reviews/<plan-file>.<reviewer-type>.md`.

**Output normalization**: If a local reviewer's output doesn't follow the standard format (Verdict, Critical Findings, Concerns, Observations), normalize it before incorporating. The planner interprets the reviewer's findings and translates them into actionable changes to the plan.

**Planning-rule validation**: Before incorporating any reviewer finding, verify it does not contradict an explicit rule from this skill. Reviewer agents load domain-specific skills but not the planning skill itself — they may suggest changes (e.g., model downgrades, skipping review steps) that violate planning-level constraints. When a conflict exists, this skill's rules take precedence — note the reviewer's rationale in the review file but do not apply the change.

Incorporate findings into the sub-plans. If a sub-plan review surfaces an issue that affects the master plan (e.g., a missed dependency, a boundary that needs to shift), update the master plan and re-run affected master plan reviewers.

#### Step 3: Convergence

Repeat Steps 1-2 only for affected parts until no reviewer produces new findings. Do NOT restart the entire review — only re-review plans that changed. This convergence loop applies **only within the initial review** — it does not re-trigger after user feedback in Phase 6.

The user may also request additional specialized reviewers (e.g., security, performance) for specific sub-plans. Add these on request, but they are not part of the default flow.

### Phase 6: User Approval & Feedback

Before presenting, run a final consistency check:

1. **Model assignments** — verify each sub-plan's execution model matches the decision tree and any explicit rules
2. **Skill conformance** — verify that reviewer-driven changes haven't introduced patterns that contradict required skills listed in each sub-plan
3. **Cross-sub-plan prerequisites** — verify that every interface, type, or file referenced in a sub-plan's Prerequisites section is created by an earlier sub-plan in the dependency graph

Fix any inconsistencies before proceeding.

Present the fully reviewed plan (master + sub-plans) along with a summary of review findings and how they were addressed. Only mark as ready when the user explicitly approves.

**Remind the user**: The plan intentionally omits implementation details — those are the executing agent's responsibility, guided by loaded skills. The user reviews architecture and constraints now; they review actual code after execution. This is by design, not a gap.

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

If this project has component documentation, run the `component-docs-reviewer` agent after all sub-plans complete to catch implementation-vs-plan drift in component docs.

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
- **Execution model**: Always assign the most capable available model. Documentation requires understanding the full feature context, making judgments about what to include, and producing clear prose — this is not rote work.

### When to Skip It

Skip the documentation sub-plan when:
- The feature doesn't affect any documented concepts, flows, or architecture
- The only doc impact is component-level (handled by `component-docs-reviewer` post-execution)
- No project documentation exists yet (recommend creating initial docs as a separate effort)

## Rules (Non-Negotiable)

- **Always respect model assignments during execution** — Sub-plan model assignments are deliberate cost-optimization decisions. When executing a plan, the assigned model MUST be used. If a sub-agent fails at the assigned model, diagnose and fix the failure (e.g., permission mode, tool access). Never silently fall back to executing the work on a more expensive model. If the issue cannot be resolved, stop and ask the user how to proceed.
- **Use worker agents for multi-plan execution** — When a plan has 2+ sub-plans, spawn each sub-plan's assigned worker agent (created in Phase 4 step 6). Worker agents are the **only reliable mechanism** for controlling sub-agent model selection — model requests via natural language prompts or team configuration are unreliable. Run independent sub-plans in parallel where the agent framework supports it. The lead coordinates handoffs between sequential sub-plans by relaying information (sub-agents cannot communicate with each other). If a worker agent fails, diagnose and retry — do not silently execute on the main agent or fall back to a more expensive model. If the issue cannot be resolved, STOP and ask the user.
- **Reviewers return findings, planner writes files** — Reviewer agents (both global and local) return their findings as their Task response. They do not write files. The planner is responsible for writing review output to `reviews/<plan-file>.<reviewer-type>.md`.
- **Never write a plan based on incomplete information**
- **Never invent requirements the user didn't specify**
- **Always decompose into sub-plans** — a single monolithic plan is a failure mode
- **Each sub-plan must be self-contained** — embed context, don't reference other sub-plans
- **Always list required skills in every sub-plan** — an executing agent without the right skills will produce subpar results or get stuck
- **Always run the review loop before presenting to the user** — unreviewed plans are draft plans, not finished plans
- **Save plans to the correct location** — standalone features go to `.claude/plans/features/<feature-name>/`, epic features go to `.claude/plans/epics/<epic-name>/<feature-name>/`. Never save to `~/.claude/`, and never use random/generated filenames
- **Ask for clarification even if it feels repetitive** — it's better than introducing garbage

[master-plan-template]: references/master-plan-template.md
[sub-plan-template]: references/sub-plan-template.md
