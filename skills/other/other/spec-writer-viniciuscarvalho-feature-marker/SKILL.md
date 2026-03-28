---
name: spec-writer
description: Transform ideas into detailed implementation specifications. Creates specs with requirements, design, and implementation steps.
argument-hint: [topic] [--mode=<interactive|autonomous>] [--services=<svc1,svc2>] [--template=<path>]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git diff:*)
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(ls *)
  - Write
---

# Spec Writer

Interactive specification writer that transforms ideas into actionable implementation plans through collaborative dialogue.

## Arguments

- `topic` (positional): The topic or idea to write a spec for
- `--mode=<interactive|autonomous>`: Operating mode (default: interactive)
- `--services=<svc1,svc2>`: Limit spec to specific services
- `--template=<path>`: Use a custom template file
- `--output=<path>`: Override output location

## Configuration

Check for `.claude/spec-workflow/config.yaml` in the project:

```yaml
paths:
  specs: "./specs"              # Where specs are saved

services:                       # Your technology stack (optional)
  backend:
    path: "./backend"
    patterns: "./backend/AGENTS.md"  # Architecture docs to reference
  frontend:
    path: "./frontend"

spec:
  naming: "{date}-{topic}-spec.md"   # Spec file naming pattern
```

### Project DNA

If `.claude/spec-workflow/PROJECT.md` exists, read it **at the start of every spec-writing session** (before any questions). Its content is the authoritative source of:

- **Architecture Rules** → enforce in Component Design and Tech decisions; flag violations as blockers
- **Code Conventions** → use when proposing naming, file structure, error handling
- **Known Constraints** → reference when evaluating feasibility and risk sections
- **"Done" criteria** → use as the baseline for Acceptance Criteria and Testing Strategy
- **Out of Scope** → apply ruthlessly to YAGNI decisions

When PROJECT.md is present, your spec proposals must be consistent with its rules.
If a design decision conflicts with an Architecture Rule, flag it explicitly:
```
⚠️ Note: This approach uses a hard delete. PROJECT.md requires soft delete (status: 'archived').
   Adjusting design to follow project convention.
```

### Philosophy Injection

If `.claude/spec-workflow/philosophy/spec-standards.md` exists, read it and incorporate its guidance. This file contains the user's standards for what makes a good spec.

### Template

Use template from (in priority order):
1. `--template` argument
2. `.claude/spec-workflow/templates/spec.md` in project
3. Built-in template (see references/spec-template.md)

---

## Modes

This skill operates in three modes:

### Interactive Mode (Default)

**Trigger:** User invokes spec-writer directly

- Full dialogue with user
- Validation checkpoints after each phase
- Questions asked one at a time
- User confirms design decisions

Announce at start: "I'm using the spec-writer skill to create the implementation plan."

### Autonomous Mode

**Trigger:** Invoked by spec-orchestrator with `{ mode: "autonomous", request: string }`

- Makes design decisions independently
- No validation checkpoints
- Documents reasoning for decisions made
- Produces complete spec in one pass

Announce at start: "I'm writing a spec autonomously for orchestrator review."

### Revision Mode

**Trigger:** Invoked by spec-orchestrator with `{ mode: "revision", currentSpec: string, feedback: object, iteration: number }`

- Receives existing spec + reviewer feedback
- Updates spec to address feedback
- Maintains Review Discussion section
- Appends Revision Notes

Announce at start: "I'm revising the spec based on reviewer feedback (iteration N)."

---

## Mode-Specific Behavior

| Phase | Interactive | Autonomous | Revision |
|-------|-------------|------------|----------|
| Understanding | Ask questions | Infer from context | Skip (spec exists) |
| YAGNI checkpoint | User validates | Self-assess, document reasoning | N/A |
| Design alternatives | Present options, user chooses | Choose best, document alternatives | Address feedback |
| Section checkpoints | Pause for validation | Continue without pause | N/A |
| Review Discussion | N/A (first draft) | N/A (first draft) | Update with feedback |
| Revision Notes | N/A | N/A | Required |

---

This skill is typically used after the idea-explorer skill has refined an idea into an understood problem space and success criteria, but before any implementation work begins. The output is a detailed spec file that the spec-executor skill can implement.

If the idea being presented is not yet well understood or has ambiguity, encourage the user to use the idea-explorer skill first.

## Core Philosophy

**Understand before writing spec**

This skill prioritizes:

1. **Dialogue over assumptions** - Ask clarifying questions (interactive mode)
2. **YAGNI ruthlessly** - Eliminate unnecessary scope early
3. **Incremental validation** - Confirm understanding at each step (interactive mode)
4. **Parallelization-aware design** - Structure work for concurrent execution WHEN beneficial
5. **Preserve decision rationale** - Document key trade-offs and reasoning

---

## Pre-Phase: PRD Validation Check

Before writing the spec, check if PRD validation has been run:

1. **Load `prd-validation.md`** from `.claude/feature-state/{slug}/prd-validation.md` if it exists
2. **If validation has blockers** → stop and present them to the user:
   ```
   ❌ PRD has unresolved blockers — spec cannot be written until fixed.
   Run prd-validator first, or fix these issues in prd.md:
   - [Blocker 1 from prd-validation.md]
   - [Blocker 2 from prd-validation.md]
   ```
3. **If validation passed** → use Reference Check table and Scope Analysis as context:
   - Treat ✅ entities as EXISTING (don't redesign them)
   - Treat ❌/new entities as TO BE CREATED (plan their design)
   - Use scope analysis to calibrate TechSpec complexity
4. **If `prd-validation.md` does not exist** → proceed without it (non-blocking), but note that validation was skipped

---

## Phase 1: Understanding (Exploring Requirements)

> **Mode note:** In autonomous mode, infer answers from context and document assumptions. In revision mode, skip this phase.

### Entry Point

When the user describes a feature or change:

1. **Examine current state**
   - Read relevant existing files
   - Review input from idea exploration (if available)
   - If not on main, check what changes have been made on the current branch
   - Identify existing patterns and documentation

2. **Service awareness** (if configured)
   - Check which services are defined in config
   - Read pattern documentation for relevant services (`services.<name>.patterns`)
   - Consider impact across services

3. **Apply YAGNI checkpoint**

After gathering initial requirements, explicitly ask:

```
**Scope Check:** Based on what you've described, I'm considering these features:

- [Feature 1] - Essential / Nice-to-have / Not needed?
- [Feature 2] - Essential / Nice-to-have / Not needed?
- [Feature 3] - Essential / Nice-to-have / Not needed?

Let's mark "Nice-to-have" items as future work and focus on essentials.
```

---

## Phase 2: Design (Exploring Approaches)

> **Mode note:** In autonomous mode, choose the best approach and document alternatives. In revision mode, focus on addressing feedback.

### Present Alternatives

When there are multiple valid approaches:

```
**Design Decision: [Topic]**

I see 2-3 viable approaches. Here's my analysis:

---

**Recommended: Option A - [Name]**

[2-3 sentence description]

Pros:
- [Advantage 1]
- [Advantage 2]

Cons:
- [Tradeoff 1]

---

**Alternative: Option B - [Name]**

[2-3 sentence description]

Pros:
- [Advantage 1]

Cons:
- [Tradeoff 1]
- [Tradeoff 2]

---

**My recommendation:** Option A because [specific reasoning].

Does this align with your thinking, or would you prefer a different direction?
```

---

## Phase 3: Write the Specification

> **Mode note:** In autonomous mode, skip validation checkpoints. In revision mode, use the Revision Mode Workflow below.

1. Write each section, pausing after each to confirm understanding is correct. **(Interactive mode only)**
2. Be prepared to iterate on sections based on feedback.

### Design Sections

Present design in digestible sections (100-300 words each):

1. **Architecture Overview** - High-level component diagram, service boundaries, data flow
2. **Data Model Changes** - Schema modifications, new types, migrations
3. **API Design** (if applicable) - Schema additions/modifications, breaking changes
4. **Component Design** - Key modules, responsibilities, interfaces
5. **Error Handling** - Failure modes, recovery strategies
6. **Testing Strategy** - Unit tests, integration tests, edge cases

### Validation Checkpoint

**(Interactive mode only)** After EACH section:

```
**Checkpoint: [Section Name]**

Does this design approach work for you? Any questions before we continue?
```

---

## Revision Mode Workflow

When invoked with `{ mode: "revision", currentSpec, feedback, iteration }`:

### Step 1: Analyze Feedback

Review the feedback object:

- **mustAddress** — Blocking issues that must be resolved
- **shouldConsider** — Important suggestions, address or justify skipping
- **minorOptional** — Quick wins, address if easy
- **disagreements** — Conflicting reviewer perspectives

### Step 2: Update the Spec

For each piece of feedback:

1. Make the necessary changes to the spec content
2. Integrate changes coherently (don't just append)
3. Maintain the spec's overall structure and flow

### Step 3: Update Review Discussion Section

Add or update the **Review Discussion** section in the spec:

```markdown
## Review Discussion

### Key Feedback Addressed
- **[Issue]** ([Reviewer]): [How it was resolved]

### Tradeoffs Considered
- **[Alternative]**: [Why it was rejected or deferred]

### Dissenting Perspectives
- **[Concern]** ([Reviewer]): [Why not fully addressed, reasoning]
```

This section accumulates across iterations—add to it, don't replace.

### Step 4: Append Revision Notes

At the end of the spec, append:

```markdown
---

## Revision Notes (Iteration N)

### Addressed
- [Feedback item]: [How addressed]

### Intentionally Not Addressed
- [Feedback item]: [Reasoning — this may trigger escalation]

### Other Changes
- [Any additional improvements]
```

### Handling Disagreements

If you believe feedback is incorrect:

1. Still acknowledge the concern in Review Discussion
2. Explain your reasoning clearly in "Intentionally Not Addressed"
3. Accept that this may trigger escalation to human review

If reviewers disagree with each other:

1. Note both perspectives in Review Discussion
2. Make a reasoned choice and document why
3. Or flag for human decision if truly unresolvable

---

## Phase 4: Specification Output

### File Naming

Save specs using the configured naming pattern. Default: `{specs-path}/{date}-{topic}-spec.md`

Example: `./specs/2024-12-21-user-notifications-spec.md`

### Spec Template

Use the template from configuration or the built-in template.

---

## Workflow Summary

```
User Request
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 1: UNDERSTANDING          │
│ • Examine current state         │
│ • Ask questions (one at a time) │
│ • Apply YAGNI checkpoint        │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 2: DESIGN                 │
│ • Present 2-3 approaches        │
│ • Lead with recommendation      │
│ • Validate each section         │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 3: SPECIFICATION          │
│ • Generate spec document        │
│ • Save to configured location   │
│ • Include parallelization if    │
│   work is parallelizable        │
└─────────────────────────────────┘
     │
     ▼
Ready for Implementation
```

---

## Phase 5: After Writing the Spec (Interactive Mode Only)

> **Mode note:** Skip this phase in autonomous and revision modes—the orchestrator handles the workflow.

Ask these questions one at a time:

1. Ask if the user would like to create a worktree for this work. If yes:
   - Use `/create-worktree` with a suitable name
   - Add the worktree name to the spec frontmatter
   - Move the spec to the worktree's specs directory

2. Ask if the user would like to make a commit
