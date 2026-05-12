---
description: >-
  Guides structured design brainstorming — explores the codebase, asks clarifying
  questions, proposes multiple approaches with trade-offs, and writes an approved
  design doc to the project. Use before implementation to think through design
  decisions and avoid premature coding. Produces a persistent artifact that feeds
  into plan mode and TDD. For stakeholder-facing or acceptance-criteria-driven
  work, the design doc includes a Given/When/Then Scenarios section consumed by
  /optimus:tdd.
disable-model-invocation: true
---

# Brainstorm

Guide the user through a structured design conversation that produces a written, approved design document before any implementation begins. The output is a persistent file in the project that feeds into Claude Code plan mode and then into `/optimus:tdd` for test-first implementation.

### The Hard Gate

**No implementation until the design is approved.** Do not invoke any implementation skill, write any production code, scaffold any project structure, or take any implementation action until you have written a design doc and the user has approved it. This applies to all tasks — even seemingly simple ones. Unexamined assumptions in "simple" projects cause the most wasted effort.

## Step 1: Pre-flight

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, process within the repo the user is targeting. If ambiguous, ask which repo.

### Verify prerequisites

Check that `.claude/CLAUDE.md` exists. If it doesn't, stop and recommend running `/optimus:init` first — project context and coding guidelines shape design decisions.

Load these documents:

| Document | Role |
|----------|------|
| `.claude/CLAUDE.md` | Project overview, tech stack, architecture |
| `coding-guidelines.md` | Quality standards that constrain the design |

**Monorepo path note:** Read the "Monorepo Scoping Rule" section of `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for doc layout and scoping rules.

### Scan project structure

Explore the project's directory structure, key modules, and existing patterns. This grounds the design conversation in what actually exists — not assumptions.

## Step 2: Gather Intent

### JIRA context detection

Before asking the user for input, check for pre-existing JIRA context:

1. If the user's inline input matches a JIRA key pattern (`[A-Z][A-Z0-9]+-\d+`), check for `docs/jira/<key>.md`. If found, read it and use its Goal and Acceptance Criteria as the brainstorm input. If the file is not found, inform the user ("No task file found for [KEY] — run `/optimus:jira [KEY]` first to fetch it") and proceed with normal intent gathering below.

2. If no inline input (or no JIRA key match), check whether `docs/jira/` exists and contains `.md` files. If so, read each file's YAML frontmatter and select the one with the most recent `date` field. Extract the `issue` field and the Goal section. Present to the user via `AskUserQuestion` — header "JIRA context", question "Found JIRA context: [ISSUE-KEY] — [Goal]. Use this as the basis for design?":
   - **Use it** — "Design around this JIRA task"
   - **Ignore** — "Describe a different task"

   If the file's `date` frontmatter field is older than 7 days, add a note: "(This context is [N] days old — you may want to re-run `/optimus:jira` for fresh data.)"

   If **Use it**: use the file's Goal and Acceptance Criteria as the brainstorm input. Proceed to clarifying questions (skip the intent-gathering prompts below).
   If **Ignore**: proceed with normal intent gathering below.

3. If no `docs/jira/` directory or no files in it, proceed with normal intent gathering below.

### Gather from user

If the user provided a description inline (e.g., `/optimus:brainstorm "add authentication system"`), use it. Otherwise, use `AskUserQuestion` — header "Design scope", question "What do you want to build or change?":
- **New feature** — "Build something new (e.g., 'Add user authentication')"
- **Significant change** — "Rework or extend an existing part of the system"

If the description is longer than ~3 sentences (e.g., a pasted spec, ticket, or acceptance criteria), distill it into a **single-sentence goal** and confirm with `AskUserQuestion` — header "Distilled goal", question "I've distilled your input to: '[single-sentence summary]'. Is this accurate?":
- **Looks good** — "Proceed with this goal"
- **Adjust** — "Let me refine the focus"

### Clarifying questions

Before asking questions, identify your key assumptions about scope, constraints, and expected behavior. Surface them in your reply text before the first `AskUserQuestion` call so the user can correct or confirm them.

Ask up to **3 clarifying questions** to fill critical gaps — one per `AskUserQuestion` call, prefer multiple-choice options. Focus on:
- Constraints the user hasn't mentioned (performance, compatibility, security)
- Scope boundaries (what's in, what's explicitly out)
- Integration points with existing code

Skip questions if the intent is already clear. Three is the maximum, not the target.

## Step 3: Explore and Propose

### Explore relevant code

Based on the user's goal, explore the codebase areas that the design will touch:
- Existing modules, patterns, and conventions relevant to the goal
- Dependencies and integration points
- Related tests (if any) that reveal expected behavior

### Propose approaches

Present **2-3 approaches** to the user:

```
## Approaches

### A: [Name]
[Brief description — 2-3 sentences]
- **Pros:** [key advantages]
- **Cons:** [key disadvantages]
- **Effort:** [Low / Medium / High]
- **Alignment:** [how well it fits existing patterns]

### B: [Name]
...

### C: [Name] (optional — only if genuinely distinct)
...

**Recommendation:** [Approach letter] — [one-sentence rationale]
```

Use `AskUserQuestion` — header "Approach", question "Which approach should I design in detail?":
- One option per approach, with the recommendation marked

If the user wants to combine aspects of multiple approaches or suggests a different direction, incorporate their feedback and present a revised approach before proceeding.

## Step 4: Design

Based on the chosen approach, develop a detailed design. Cover each section as applicable — omit sections that don't apply to the task:

- **Goal** — single paragraph: what and why
- **Approach** — how it works, key decisions and their rationale
- **Components** — what gets created or modified, each component's responsibility
- **Interfaces** — how components interact (APIs, data flow, contracts, function signatures)
- **Edge cases and risks** — what could go wrong, mitigations
- **Scenarios** — *conditional.* 3–7 Given/When/Then scenarios that `/optimus:tdd` consumes as the behavior list. See `$CLAUDE_PLUGIN_ROOT/skills/brainstorm/references/scenario-style.md` for inclusion signals and phrasing — read it before writing scenarios.
- **Out of scope** — explicit boundaries to prevent scope creep

Present the design in conversation. Use `AskUserQuestion` — header "Design review", question "Does this design look right?":
- **Approve** — "Write it to a design doc"
- **Adjust** — "I have feedback before writing"

If the user has feedback, refine the design and present it again. Iterate until approved.

## Step 5: Write Design Doc

Read `$CLAUDE_PLUGIN_ROOT/skills/brainstorm/references/design-doc-format.md` for the template.

### Write the file

- **Path:** `docs/design/YYYY-MM-DD-<topic-slug>.md` — derive the slug from the goal (lowercase, replace non-alphanumeric characters with hyphens, collapse consecutive hyphens, strip leading/trailing hyphens, max 5 words). The slug must match `[a-z0-9]+(-[a-z0-9]+)*` — reject any slug that does not match this pattern
- Create the `docs/design/` directory if it doesn't exist
- Fill the template with the approved design content
- Set **Status** to `Approved`

### Self-review

After writing, read the file back and check for:
- TODOs, placeholders, or "TBD" markers
- Internal contradictions (e.g., a component listed in Components but missing from Interfaces)
- Requirements ambiguous enough to cause someone to build the wrong thing
- YAGNI violations — features or complexity the user didn't ask for
- If a Scenarios section was included: re-check it against `$CLAUDE_PLUGIN_ROOT/skills/brainstorm/references/scenario-style.md` (Discipline and Anti-patterns)

Fix any issues found. If a fix would change a design decision, ask the user first.

## Step 6: Report

Present the result:

```
## Design Complete

**Design doc:** `<file-path>`
**Goal:** <single-sentence goal>
**Approach:** <chosen approach name>
**Components:** <count> (<count> new, <count> modified)
```

## Step 7: Next Step

Handle non-implementation tasks first:
- **Refactoring task** → tell the user: "Recommend running `/optimus:refactor` to restructure the code. **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch."
- **Test-only task** → tell the user: "Recommend running `/optimus:unit-test` to write tests for existing code. **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch."

For implementation tasks, assess complexity from the Components table in the design doc. If the Components table lists zero code components or the Goal names a written artifact (research note, audit report, investigation write-up), the deliverable is **prose** — use the Medium-to-large branch below but follow the "Prose deliverable" note on the execution prompt.

### Small (1–2 components, <5 behaviors implied)

Tell the user: "This is small enough to implement directly — run `/optimus:tdd` to build it test-first. It will auto-detect the design doc at `<file-path>`. **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch."

### Medium-to-large (3+ components or complex interfaces)

Generate a plan-mode prompt inline, pre-filled from the design doc. Present it as a single copyable block:

````
```
## Goal
[Goal from the design doc]

## Context
[Synthesize from the design doc's Context and Approach sections.
Include key decisions, constraints, and the chosen approach rationale.]

## Starting Hints
- Design doc: <file-path>
- [Key files/modules identified during codebase exploration in Step 3]

## What to Figure Out
1. Which existing files and modules need to be modified or extended?
2. What's the right implementation sequence given the component dependencies?
3. Are there existing patterns in the codebase to follow or reuse?
4. What are the risks or edge cases not covered in the design?

## Plan Deliverable
The plan should include:
- Proposed approach with rationale
- Files to create or modify, with what changes
- Implementation sequence and dependencies
- Test strategy mapped to each component

## Scope
- Focus on: [components from the design doc]
- Out of scope: [from the design doc's Out of Scope section]

## How this conversation should run
Treat this conversation as a review loop — validate the plan against the actual codebase and iterate with me. When I say I'm done iterating, acknowledge but do not write yet — plan mode is read-only. I will then toggle plan mode off and send a short follow-up message (e.g. "go"). On that follow-up, append a "Refined plan" section to `<design-doc-path>` to capture the refined plan, and stop. I will start a fresh conversation to run `/optimus:tdd`.
```
````

When emitting both the plan-mode prompt above and the execution prompt below, substitute `<design-doc-path>` with the actual path from Step 5 so each pasted block is self-contained.

Tell the user:

> 1. Start a fresh Claude Code conversation in **plan mode** (CLI: press `Shift+Tab` until the mode indicator shows plan mode; other clients: use the equivalent toggle). Paste the prompt above.
> 2. Iterate with Claude. **Do not approve the plan** — approval executes immediately and skips `/optimus:tdd`'s Red-Green-Refactor discipline. When you're satisfied, tell Claude you're done iterating; Claude will acknowledge. Then toggle plan mode off using the same control **and send a short follow-up message (e.g. "go")** — Claude will append a "Refined plan" section to `<design-doc-path>` in response.
> 3. Start a **second fresh conversation** and paste the execution prompt below.

Then emit the **execution prompt** as a second copyable block, pre-filled from the design doc:

````
```
## Goal
Run `/optimus:tdd` to implement the refined plan in `<design-doc-path>` test-first.

## Starting Hints
- Design doc (with "Refined plan" section): <design-doc-path>
- Components from the design: [list component names from the Components table]

## Scope
- Focus on: [components from the design doc]
- Out of scope: [from the design doc's Out of Scope section]
```
````

**Prose deliverable:** if the design produces a written artifact rather than code, replace the execution prompt above with one that instructs Claude directly — e.g. `Execute the refined plan in <design-doc-path> to produce <deliverable-path>.` — and note that `/optimus:tdd` does **not** apply. After `<deliverable-path>` is produced, recommend `/optimus:commit` to commit the artifact.

See `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` for the full handoff convention and why plan mode is used review-only.
