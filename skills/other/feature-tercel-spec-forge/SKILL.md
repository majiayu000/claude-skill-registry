---
name: feature
description: >
  Generates lightweight, implementation-ready feature specifications. A feature spec is the bridge
  between spec-forge's formal documentation chain (PRD/SRS/Tech Design/Test Plan) and code-forge's
  implementation planning. It distills what a module or component must do into a concise,
  language-agnostic document that code-forge:plan can consume directly. Supports two modes:
  standalone creation through a brief Q&A interview, or automatic extraction from an existing
  tech-design document. Output lives in docs/features/ and is shared across all language-specific
  implementations.
instructions: >
  Follow the workflow below exactly. This skill produces a single concise document per feature,
  not a heavyweight specification. Keep it focused on what a developer needs to know to plan
  implementation: module purpose, core responsibilities, key interfaces, data flow, and constraints.
  Do NOT duplicate the depth of a full tech-design — if the user needs that level of detail,
  direct them to /spec-forge:tech-design instead.
---

# Feature — Lightweight Feature Specification

Generate a concise, implementation-ready feature specification that serves as the input contract for code-forge:plan.

## Core Principles

1. **Concise over comprehensive**: 1-3 pages, not 20. Enough for a developer to plan implementation, not enough for a full architecture review.
2. **Language-agnostic**: Describe behavior, interfaces, and constraints — not Pydantic models or TypeBox schemas.
3. **Implementation-ready**: Every section should help code-forge:plan generate concrete tasks.
4. **Single module focus**: One feature spec per module or cohesive component. If scope spans multiple modules, suggest running `/spec-forge:decompose` first.
5. **Two sources of truth**: Can be created from scratch via Q&A, or extracted from an existing tech-design.

## Output Location

```
docs/features/{feature-name}.md
```

where `{feature-name}` is a lowercase, kebab-case slug (e.g., `core-executor`, `schema-system`, `acl-system`).

**CRITICAL — No Sequential Numbering**: Do NOT prefix filenames with sequence numbers like `F001-`, `F002-`, `001-`, etc. The filename is ONLY the kebab-case slug. Ordering and relationships between features are managed in the overview file, not encoded in filenames.

If the `docs/features/` directory does not exist, create it.

### Overview File

When generating feature specs for a multi-feature project (i.e., more than one feature spec exists or will exist in `docs/features/`), maintain an overview file:

```
docs/features/overview.md
```

**Overview file rules:**
- Create or update this file whenever a new feature spec is generated
- If the overview file already exists, read it and append/update the new feature entry
- If a project manifest exists (`docs/project-*.md`), use its execution order and dependency information
- Do NOT create the overview for a single standalone feature — only when 2+ features exist

**Overview template:**

```markdown
# Feature Overview

> Auto-generated index of feature specs for this project.
> Updated: {date}

## Features

| Feature | Description | Dependencies | Status |
|---------|-------------|--------------|--------|
| [{feature-name}](./{feature-name}.md) | {one-line description} | {none or list} | draft |
| ... | ... | ... | ... |

## Execution Order

{Ordered list showing recommended implementation sequence, derived from dependencies.
If sourced from a project manifest, reference it.}

1. **{feature-name}** — {reason it goes first, e.g., "no dependencies"}
2. **{feature-name}** — {reason, e.g., "depends on feature-1"}
3. ...
```

## Workflow

### Step 1: Detect Mode

Parse the feature name from arguments. Then determine the mode:

**Chain mode detection**: If the invocation prompt contains "Chain mode" or "Auto-confirm extraction", this is being called as part of the spec-forge chain. In chain mode:
- Skip all `AskUserQuestion` calls — auto-select the recommended option at each step
- If existing feature spec exists → auto-select "Regenerate from scratch"
- If upstream tech-design is found → auto-select "Extract from tech-design"
- In Step 2a.2 → skip confirmation, proceed directly to generation
- **CRITICAL**: Filename MUST be `{feature-name}.md` — plain kebab-case slug, NO numeric prefixes (`01-`, `F001-`, etc.). This rule applies in ALL modes but is especially important in chain mode where multiple features are generated sequentially.
- After generating, ALWAYS create or update `docs/features/overview.md` (the overview tracks execution order, not filenames)

1. **Check for existing feature spec**: If `docs/features/{feature-name}.md` already exists:
   - Display: "Feature spec already exists at docs/features/{feature-name}.md"
   - Use `AskUserQuestion` (skip in chain mode — auto-select "Regenerate from scratch"):
     - "Update existing spec" — read current file as context, proceed to Q&A with existing content pre-loaded
     - "Regenerate from scratch" — proceed as if no file exists
     - "Cancel"

2. **Check for upstream tech-design**: Scan for `docs/{feature-name}/tech-design.md` or `docs/*/tech-design.md` that covers this feature.
   - **Found** → **Extract mode** (Step 2a)
   - **Not found** → **Standalone mode** (Step 2b)

3. If upstream tech-design is found, ask the user (skip in chain mode — auto-select "Extract from tech-design"):
   - "Extract from tech-design (Recommended)" — faster, ensures consistency with formal specs
   - "Create from scratch" — ignore existing tech-design, do fresh Q&A
   - "Cancel"

### Step 2a: Extract Mode (from Tech Design)

Read the upstream `docs/{feature-name}/tech-design.md` (or the matched tech-design file).

#### 2a.1 Scan and Extract

Extract these elements from the tech-design:
- Module purpose and scope
- Key components and their responsibilities
- Core interfaces (public API surface, not internal details)
- Data flow (input → processing → output)
- Dependencies on other modules
- Constraints and invariants
- Error handling strategy (summary, not full taxonomy)

#### 2a.2 Confirm with User

Present a brief summary of what was extracted. Use `AskUserQuestion` (0-1 questions) — **skip in chain mode, proceed directly to generation**:
- "Anything to add or change?" with options:
  - "Looks good, generate" — proceed
  - "Add notes" — user provides additional context
  - "Cancel"

#### 2a.3 Generate

Write the feature spec to `docs/features/{feature-name}.md` using the template below. Skip to Step 4.

### Step 2b: Standalone Mode (Q&A)

No upstream tech-design found. Gather requirements through a brief interview.

#### 2b.1 Read Context

1. Glob the project tree (top 3 levels) for structure awareness
2. Read README.md if it exists
3. Scan `docs/` for related documents (PRD, SRS, other feature specs)
4. Scan existing code if the module partially exists

Summarize context internally — do not present to user.

#### 2b.2 Interview (2-3 rounds)

Use `AskUserQuestion` to understand the feature. Adapt based on answers.

**Round 1 — Purpose and Scope:**
- What does this module/component do? (one paragraph)
- What are its core responsibilities? (3-5 bullet points)
- What is explicitly out of scope?

**Round 2 — Interfaces and Data:**
- What does it receive as input? From whom?
- What does it produce as output? For whom?
- What external systems or modules does it depend on?
- Are there key data structures or models involved?

**Round 3 — Constraints (if needed):**
- Performance requirements? (throughput, latency)
- Security or access control requirements?
- Concurrency or ordering guarantees?
- Any hard constraints from the protocol or spec layer?

Stop when you have enough to write a clear feature spec. Do NOT over-interview — 2 rounds is often sufficient.

### Step 3: Generate Feature Spec

Write the document to `docs/features/{feature-name}.md` using the template below.

**Reminder**: The filename MUST be `{feature-name}.md` — a plain kebab-case slug with NO numeric prefixes (no `F001-`, `001-`, etc.).

### Step 3b: Update Overview (if applicable)

After writing the feature spec, check if 2+ feature specs now exist in `docs/features/` (excluding `overview.md`):
- **If yes**: Create or update `docs/features/overview.md` using the overview template from the Output Location section
- **If no** (this is the only feature spec): Skip overview generation

### Step 4: Quality Check

Verify the generated feature spec against these criteria:

- [ ] **Purpose is clear**: A developer can understand what this module does in 30 seconds
- [ ] **Scope is bounded**: What's included AND what's excluded is explicit
- [ ] **Interfaces are defined**: Inputs, outputs, and dependencies are listed
- [ ] **Language-agnostic**: No language-specific types, libraries, or patterns
- [ ] **Actionable**: code-forge:plan could generate implementation tasks from this
- [ ] **Concise**: Under 3 pages / ~150 lines
- [ ] **No numbered prefix**: Filename is a plain kebab-case slug, NOT prefixed with F00X or similar

Fix any issues before presenting.

### Step 5: Summary

Display:

```
Feature spec generated: {feature-name}
  Location: docs/features/{feature-name}.md
  Source: {extracted from tech-design | standalone Q&A}
  Length: {line count} lines
  Overview: {updated | not needed (single feature)}

Next steps:
  /code-forge:plan @docs/features/{feature-name}.md   → Generate implementation plan
  /spec-forge:tech-design {feature-name}               → Generate full technical design (if needed)
```

## Feature Spec Template

```markdown
# {Feature Name}

> Feature spec for code-forge implementation planning.
> Source: {standalone | extracted from docs/{name}/tech-design.md}
> Created: {date}

## Purpose

{One paragraph describing what this module does and why it exists.}

## Scope

**Included:**
- {responsibility 1}
- {responsibility 2}
- ...

**Excluded:**
- {explicitly out of scope item 1}
- ...

## Core Responsibilities

1. **{Responsibility name}** — {brief description of what it does}
2. **{Responsibility name}** — {brief description}
3. ...

## Interfaces

### Inputs
- **{input name}** ({source}) — {description}
- ...

### Outputs
- **{output name}** ({destination}) — {description}
- ...

### Dependencies
- **{module/system name}** — {what it provides and why it's needed}
- ...

## Data Flow

{Describe the main processing pipeline or data flow. Use a mermaid diagram if the flow has 3+ steps:}

```mermaid
graph LR
    A[Input] --> B[Process Step 1]
    B --> C[Process Step 2]
    C --> D[Output]
```

## Key Behaviors

{Describe the important behavioral rules, algorithms, or processing logic. Focus on WHAT happens, not HOW to implement it.}

### {Behavior 1}
{Description}

### {Behavior 2}
{Description}

## Constraints

- **{constraint type}**: {description}
- ...

## Error Handling

{Summary of error categories and expected behavior. Not a full error taxonomy — just enough to guide implementation.}

## Notes

{Any additional context, open questions, or references to related documents.}
```

## Relationship to Other spec-forge Documents

| Document | Relationship |
|----------|-------------|
| **PRD** | Feature spec may reference PRD requirements but does not duplicate them |
| **SRS** | Feature spec is less formal — no requirement IDs, no CRUD matrix |
| **Tech Design** | Feature spec is a condensed derivative; tech-design is the authoritative source |
| **Test Plan** | Feature spec does not cover testing strategy |
| **Decompose** | If a project is decomposed, each sub-feature can have its own feature spec |

## When to Use This vs Tech Design

| Scenario | Use |
|----------|-----|
| Quick module planning, daily development | `/spec-forge:feature` |
| Formal architecture review, team alignment | `/spec-forge:tech-design` |
| Full project specification chain | `/spec-forge <name>` (includes tech-design) |
| Already have tech-design, need implementation input | `/spec-forge:feature` (extract mode) |
