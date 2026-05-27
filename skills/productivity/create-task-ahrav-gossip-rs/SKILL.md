---
name: create-task
description: Use when creating any beads task — auto-researches the codebase, links related tasks, and produces a rich self-contained description from a structured template. Accepts minimal intent and outputs a complete task ready for agent implementation.
---

# Create Task

Creates high-quality, self-contained beads tasks by researching the codebase and
assembling a structured description. Every task produced by this skill should give
an implementing agent 90% of the context it needs inline.

**Core principle:** Invest effort at creation time to save 10x at implementation time.

## Invocation

```
/create-task "Fix off-by-one in window boundary check" --type=bug --priority=1
/create-task --quick "Add capacity hint to Vec in compile_rules" --type=task --priority=3
/create-task --dry-run "Refactor transform chain error handling" --type=task --priority=2
/create-task --from-plan docs/plans/2026-02-23-feature-v3.md --step=3
```

**Input formats:**
- Positional string: `"title text here"`
- Flags: `--title`, `--type`, `--priority`, `--labels`, `--files-hint`, `--parent`
- Pasted paragraph with description

**Flags:**
| Flag | Effect |
|------|--------|
| `--quick` | Skip research (Phase 1). Apply template with available info only. |
| `--dry-run` | Print the full description without creating the beads task. |
| `--from-plan <path> --step=N` | Extract task from a plan file step. |
| `--type=<type>` | Task type: task, bug, feature, epic, question, docs (default: task) |
| `--priority=<N>` | Priority 0-4 (default: 2) |
| `--labels=<a,b>` | Comma-separated labels |
| `--files-hint=<paths>` | Comma-separated file paths to seed research |
| `--parent=<id>` | Parent epic beads ID |

---

## Phase 0 --- Parse Intent

1. Extract from input:
   - **Title** (required): Clear imperative statement of what to do
   - **Brief description**: 1-2 sentence context (if provided)
   - **Type**: default `task`
   - **Priority**: default `2`
   - **Labels, files-hint, parent**: if provided

2. If only a title with no brief description, ask the user:
   > What's the 1-2 sentence context for this task? (What problem does it solve or what need does it address?)

3. If `--from-plan` is specified:
   - Read the plan file at the given path
   - Extract the step indicated by `--step=N`
   - Map plan fields: Problem Statement -> Context, Codebase Context -> Current State,
     step What -> Desired State, step Files -> Files to Modify, step Tests -> Testing Strategy,
     step Acceptance criteria -> Acceptance Criteria
   - Proceed to Phase 3 (skip research — plan already has codebase context)

---

## Phase 1 --- Research (Explore Agent)

**Skip when `--quick` is passed.**

Spawn one `subagent_type=general-purpose` agent with the structured research prompt
below. The agent performs up to ~30 tool calls across 6 steps.

### Research Agent Prompt

```
You are a codebase researcher preparing context for a new task. Your job is to
gather specific, concrete information — NOT to implement anything.

## Task Being Created

**Title**: {TITLE}
**Brief**: {BRIEF_DESCRIPTION}
**Type**: {TYPE}
**Files hint**: {FILES_HINT or "none provided"}

## Research Steps (follow in order)

### Step 1: Find Affected Files
Use Grep and Glob to search for identifiers, types, functions, and concepts
mentioned in the title and brief. Search broadly:
- Exact names and keywords from the title
- Related concepts (synonyms, adjacent functionality)
- File paths mentioned in files-hint

List every file that is likely touched by this task.

### Step 2: Read Relevant Code
Read the specific functions, structs, and modules most relevant to this task.
- Maximum 8 files
- For each, extract the most relevant 5-20 line snippet with file:line header
- Note function signatures, struct definitions, trait impls

### Step 3: Trace Blast Radius
For the primary functions/types affected:
- Grep for callers and call sites
- Note which modules depend on the affected code
- Identify downstream effects of changes

### Step 4: Find Reusable Patterns
Check for existing utilities that could be reused (per duplication prevention rules):
- Search `src/stdx/` for related helpers
- Check sibling modules for similar patterns
- Note any existing abstractions that should be extended rather than duplicated

### Step 5: Search Related Beads Tasks
Run: `bd search "{keywords from title}" --limit 10`
For each result, classify the relationship:
- **blocks**: This new task cannot start until that task completes
- **blocked-by**: That task cannot start until this new task completes
- **relates-to**: Related but independent work
- **possible-duplicate**: May be the same task — FLAG THIS

### Step 6: Assess Scope
Based on your research, classify:
- **files_affected**: count of files that will be modified
- **modules_crossed**: count of distinct modules (top-level src/ directories)
- **touches_hot_path**: true/false — does this touch engine/, scheduler/, or hot loop code?
- **has_unsafe**: true/false — does affected code contain unsafe blocks?

## Output Format

Return a structured markdown document with these sections:

### Affected Files
| File | Relevance | What Changes |
|------|-----------|-------------|

### Code Snippets
For each relevant snippet:
```rust
// {file_path}:{start_line}-{end_line} — {brief description}
{actual code}
```

### Blast Radius
| Caller/Dependent | File | Relationship |
|-----------------|------|-------------|

### Reusable Utilities
| Utility | Location | How to Reuse |
|---------|----------|-------------|
(or "None found")

### Related Tasks
| Task ID | Title | Relationship | Notes |
|---------|-------|-------------|-------|
(or "None found")

### Scope Assessment
- files_affected: {N}
- modules_crossed: {N}
- touches_hot_path: {true/false}
- has_unsafe: {true/false}

IMPORTANT: Be concrete. Every file path must be real. Every code snippet must
be copied from the actual codebase, not invented. Every task ID must come from
`bd search` output.
```

---

## Phase 2 --- Link Related Tasks

Process the Related Tasks output from the research agent:

1. **Possible duplicates**: Present to the user with details. Ask before proceeding.
   > Found a possible duplicate: {task_id} "{title}". Should I:
   > (a) Skip creating this task (it's already covered)
   > (b) Create anyway (different scope)
   > (c) Show me more details

   **Never silently create a duplicate.**

2. **Blocking relationships**: After the task is created (Phase 4), run:
   ```bash
   bd dep add <new-id> <blocker-id>
   ```

3. **Relates-to**: Include in the Related Work section of the description.

---

## Phase 3 --- Compose Description

Assemble the full task description from the template below, filling sections
with explore agent output (Phase 1) or available information (if `--quick`).

### Complexity Scaling

| Complexity | Criteria | Sections | Expected Length |
|------------|----------|----------|-----------------|
| Trivial | 1 function, clear fix | Mandatory only | 30-60 lines |
| Standard | 1-3 files, 1 module | All mandatory | 80-150 lines |
| Complex | 3+ files, multi-module | All mandatory + conditionals | 200-400 lines |

Determine complexity from the scope assessment (Phase 1) or from the brief
description (if `--quick`).

### Mandatory Sections (ALL Tasks)

```markdown
## Context
{Why this task exists. What problem or need it addresses. What symptom prompted it.}

## Current State
{What exists today with code snippets and file:line references.}

```rust
// src/engine/core.rs:142-158 — current boundary check
{actual code from research}
```

## Desired State
{What should exist after. Specific behavior, interface, or structure.}

## Implementation Guidance

### Files to Modify
| File | Change | Rationale |
|------|--------|-----------|

### Patterns to Follow
{Existing patterns to mirror, with file:line refs. "None" if nothing specific.}

### Utilities to Reuse
{From src/stdx/ or siblings. "None found" if nothing applies.}

### Blast Radius
{Callers, downstream effects, call sites needing updates.}

## Code References
{3-5 inline snippets of the most relevant current code, each 5-20 lines.
Each snippet has a file:line header.}

## Related Work
| Task ID | Title | Relationship |
|---------|-------|-------------|
{Or "None found" — section must always be present.}

## Acceptance Criteria
- [ ] {Specific verifiable condition}
- [ ] All existing tests pass: `cargo test`
- [ ] Code compiles clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`

## Pointers
{Where to look for the remaining ~10%: docs, related commits, design docs, files to read.}
```

### Conditional Sections

Include these based on scope assessment:

| Section | Include When | Content |
|---------|-------------|---------|
| **Design Notes** | modules_crossed >= 2 or multiple valid approaches | Trade-offs, alternatives considered, rationale for chosen approach |
| **Risk Analysis** | priority <= 1 or has_unsafe | What could go wrong, mitigation strategies, rollback plan |
| **Performance Considerations** | touches engine/, stdx/, scheduler/ | Hot path impact, allocation concerns, benchmark expectations |
| **Testing Strategy** | files_affected > 1 | What tests to add/modify, test types (unit, property, integration), coverage goals |

Place conditional sections between "Code References" and "Related Work".

### Handling Missing Information

If the research agent didn't find enough for a section, include the section
with a `[NEEDS ENRICHMENT]` marker:

```markdown
### Blast Radius
[NEEDS ENRICHMENT] — Could not trace all callers. The implementing agent should
grep for usages of `FunctionName` before making changes.
```

---

## Phase 4 --- Create Task

1. Write the composed description to a temp file:
   ```bash
   TMPFILE=$(mktemp /tmp/task-desc-XXXXXX.md)
   ```
   Write the description content to the temp file.

2. Create the beads task:
   ```bash
   bd create --title="{TITLE}" --type={TYPE} --priority={PRIORITY} --body-file="$TMPFILE"
   ```

   Add `--labels={LABELS}` if provided.
   Add `--parent={PARENT}` if provided.

3. Register dependencies (from Phase 2):
   ```bash
   bd dep add <new-id> <blocker-id>
   ```

4. Clean up temp file:
   ```bash
   rm "$TMPFILE"
   ```

5. Show the created task:
   ```bash
   bd show <new-id>
   ```

6. Present summary to user:
   ```
   Created task: {id}
   Title: {title}
   Type: {type} | Priority: P{priority}
   Sections: {count} mandatory + {count} conditional
   Related tasks linked: {count}
   Dependencies added: {count}
   ```

### Dry Run Mode

If `--dry-run` is passed, skip step 2-4. Instead, print the full description
to the user with a header:

```
--- DRY RUN: Task Description Preview ---
Title: {title}
Type: {type} | Priority: P{priority}

{full description}

--- End Preview (no task created) ---
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| Creating a task with no description | Agent wastes time rediscovering context | Always use this skill or follow the template |
| Writing "see review for details" | External reference will rot; agent can't work it | Inline all context in the description |
| Code references without file:line | Agent can't find the code | Always include file path and line numbers |
| Acceptance criteria like "it works" | Not verifiable | Specific conditions: "function returns X when given Y" |
| Skipping Related Work search | Creates duplicates, misses dependencies | Always run `bd search` |
| Research agent reading 20+ files | Diminishing returns, bloats context | Cap at 8 files, focus on most relevant |
| Silently creating a duplicate | Wastes implementation effort | Always present possible duplicates to user |

## Related Skills

- `/plan-forge` — creates implementation plans; use `--create-tasks` to auto-generate tasks from plan steps
- `/execute-review-findings` — converts review findings to tasks (uses compatible template)
- `/review-dispatch` — produces findings that may become tasks
