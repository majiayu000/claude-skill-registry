---
name: implementation
description: Execute implementation tasks with different approaches (single, dual-agent, plan-based).
---

# Implementation

Executes implementation tasks using different approaches: direct execution, dual-agent comparison, or plan-based execution.

## Requirements

- Active session must exist (session path in working memory)
- If no active session: **STOP and ask user** for session path

## Common Steps (Mandatory)

These steps apply to ALL actions after implementation is complete.

### Working Dir Resolution
- Read Working Dir from session `_overview.md`
- If not set: check project `.samocode` file for `MAIN_REPO`, or use git root, or ask user

### After Code Changes
1. **Lint/typecheck:** Run pyright/ruff (Python). For TypeScript, rely on LSP (vtsls) — do NOT run `npx tsc --noEmit` (it OOMs on large codebases)
2. **Commit code:** In Working Dir, commit with descriptive message
   - Check branch first: warn if on main, should be feature branch

### After Session Changes
1. **Update `_overview.md`:** Add Flow Log entry and Files entry
2. **Commit session:** `cd [SESSION_DIR] && git add . && git commit -m "[action]: [description]"`

### Plan Progress (when working from a plan)
- Read plan file, mark completed items `- [x]`
- Add completion note: `**Phase completed** ([TIMESTAMP_ITERATION])`

## Default Action: dop2

**IMPORTANT:** For implementation phases, use dop2 (dual-agent comparison).

- **dop2** (Dual-Agent): Spawn 2 Task sub-agents to propose solutions, then compare
- **dop** (Direct): Only for trivially simple 1-2 line changes

**DO NOT implement directly with Edit/Write** - spawn sub-agents to propose solutions first.

**Rule of thumb:** If you're considering dop, ask "Could there be a cleaner way?" If yes -> use dop2.

## Actions

### do - Direct Implementation

Execute a task directly with full implementation and documentation.

**Session path:** [SESSION_PATH from working memory]
**Task:** $ARGUMENTS

#### Steps

1. **Investigate and implement:**
   - Review session documents for context
   - Explore codebase as needed
   - Make all necessary code changes

2. **Document work** - Create `[SESSION_PATH]/[TIMESTAMP_FILE]-do-[task-slug].md`:
   ```markdown
   # Task: [brief title]
   Date: [TIMESTAMP_LOG]

   ## What was done
   [Description of changes]

   ## Files Changed
   - [file] - [what changed]

   ## Testing
   [How verified]

   ## Notes
   [Any important observations]
   ```

3. **Complete common steps** (see above)

4. **Report back:** Summary of what was done

---

### do2 - Dual-Agent Comparison

Spawn two agents with different philosophies to solve the same task independently. Compare solutions and present options.

**Session path:** [SESSION_PATH from working memory]
**Task:** $ARGUMENTS

#### Dual Agent Execution

Spawn 2 sub-agents **in parallel** (model: sonnet). Do NOT tell them about each other.

Both agents solve the **entire task independently** with different philosophies.

**Agent 1: Minimal Footprint**

**Session path:** [SESSION_PATH]
**Task:** $ARGUMENTS

**Approach:** Smallest possible change surface.
- Touch few files, prefer localized fixes
- Avoid new abstractions
- Work within existing structures

**Deliverables:**

1. Create `[SESSION_PATH]/[TIMESTAMP_FILE]-solution-minimal.md`:
   ```markdown
   # Solution: Minimal Footprint
   Task: [description]

   ## Approach
   [High-level strategy]

   ## Proposed Changes

   ### File: [path]
   ```[language]
   [code]
   ```
   **Why:** [rationale]

   ## Tradeoffs
   [What we accept]
   ```

2. **DO NOT edit actual code files** - proposals only

3. Report summary

**Agent 2: Clean Foundation**

**Session path:** [SESSION_PATH]
**Task:** $ARGUMENTS

**Approach:** The "right way" with time to do it properly.
- Refactor for cleaner solution
- Introduce helpful abstractions
- Consider future maintainability

**Deliverables:**

1. Create `[SESSION_PATH]/[TIMESTAMP_FILE]-solution-clean.md`:
   ```markdown
   # Solution: Clean Foundation
   Task: [description]

   ## Approach
   [High-level strategy]

   ## Proposed Changes

   ### File: [path]
   ```[language]
   [code]
   ```
   **Why:** [rationale]

   ## Architecture Improvements
   [New patterns, benefits]
   ```

2. **DO NOT edit actual code files** - proposals only

3. Report summary

#### Synthesis (Parent does this)

After both agents complete:

1. Review both solutions
2. Create `[SESSION_PATH]/[TIMESTAMP_FILE]-comparison.md`:
   ```markdown
   # Comparison: [task]

   ## Minimal Footprint
   **Pros:** [list]
   **Cons:** [list]

   ## Clean Foundation
   **Pros:** [list]
   **Cons:** [list]

   ## Recommendation
   [Which approach and why]

   ## Hybrid Possibility
   [Can we combine best of both?]
   ```

3. **Complete common steps** for session files

4. Present to user:
   ```
   Which approach?
   1. Minimal footprint
   2. Clean foundation
   3. Hybrid
   4. Neither (rethink)
   ```

#### After User Confirms

1. **Implement chosen solution**
2. **If part of a plan:** Update plan progress
3. **Complete common steps** (lint, commit code, update session, commit session)

---

### dop - Plan Phase Execution (Direct)

Execute a specific phase from the plan without comparing approaches.

**Only for TRIVIALLY SIMPLE 1-2 line changes.** For anything else, use dop2.

**Session path:** [SESSION_PATH from working memory]
**Phase:** $ARGUMENTS

IMPORTANT: Only work on this specific part. Don't do other parts of the plan.

#### Steps

1. **Find the plan:**
   - Check session `_overview.md` -> Plans section for plan file
   - Read the plan file from session folder
   - Locate the specific phase/section to implement

2. **Implement:**
   - Make all necessary code changes for this phase only
   - Follow codebase best practices

3. **Document work** - Create `[SESSION_PATH]/[TIMESTAMP_FILE]-dop-[phase-slug].md`:
   ```markdown
   # Phase: [phase name]
   Date: [TIMESTAMP_LOG]
   Plan: [plan filename]

   ## Completed Items
   - [x] [Item from plan]
   - [x] [Item from plan]

   ## Changes Made
   - [file] - [what changed]

   ## Testing
   [How verified]

   ## Notes
   [Any issues or observations]
   ```

4. **Complete common steps** (lint, commit code, update plan, update session, commit session)

5. **Report back:** Summary of completed items

---

### dop2 - Dual-Agent Plan Phase with Auto-Selection

**DEFAULT IMPLEMENTATION STRATEGY** - Use Task tool to spawn 2 sub-agents.

Execute a plan phase using dual-agent comparison, with automatic solution selection weighted toward clean approach.

**CRITICAL:** You MUST use the Task tool to spawn sub-agents. DO NOT implement directly.

**Session path:** [SESSION_PATH from working memory]
**Task:** $ARGUMENTS

IMPORTANT: Only work on this specific task. Don't do other parts of the plan.

#### Phase Scope Assessment

**Before spawning agents, assess phase complexity:**

1. **Review the phase items** - Count distinct deliverables/changes
2. **If phase has 5+ items or touches 5+ files:**
   - Consider splitting into sub-phases (e.g., "Phase 3a", "Phase 3b")
   - Each sub-phase should be a coherent unit (1-3 related items)
   - Run dop2 for each sub-phase sequentially
3. **If phase has 2-4 independent sub-items:**
   - Can run 2 dop2 calls in parallel for independent items
   - Only parallelize if items don't share files/dependencies

#### Dual Agent Execution

Spawn 2 sub-agents **in parallel** (model: sonnet) with the context below. Do NOT tell them about each other.

**CRITICAL:** Both agents solve the **entire task independently**. This is NOT task splitting - each agent produces a FULL solution with their own philosophy.

**Agent 1: Minimal Footprint**

**Session path:** [SESSION_PATH]
**Task:** $ARGUMENTS

**Your approach:** Solve with the smallest possible change surface.

**Guidelines:**
- Touch as few files as possible
- Prefer simple, localized fixes
- Avoid new abstractions or patterns
- Work within existing structures

**Deliverables:**

1. Create `[SESSION_PATH]/[TIMESTAMP_FILE]-solution-minimal.md`:
   ```markdown
   # Solution: Minimal Footprint
   Date: [TIMESTAMP_LOG]
   Task: [description]

   ## Approach
   [High-level strategy]

   ## Proposed Changes

   ### File: [path]
   ```[language]
   [code]
   ```
   **Why:** [rationale]

   ## Tradeoffs
   [What we accept with this approach]

   ## Risks
   [Potential issues]
   ```

2. Update `_overview.md`: Flow Log and Files entries

3. **DO NOT edit actual code files** - suggestions only

4. Report back with summary

**Agent 2: Clean Foundation**

**Session path:** [SESSION_PATH]
**Task:** $ARGUMENTS

**Your approach:** Solve the "right way" assuming time to do it properly.

**Guidelines:**
- Refactor if it leads to cleaner solution
- Introduce abstractions where they reduce future complexity
- Consider how this code will evolve
- Prioritize maintainability over minimal diff

**Deliverables:**

1. Create `[SESSION_PATH]/[TIMESTAMP_FILE]-solution-clean.md`:
   ```markdown
   # Solution: Clean Foundation
   Date: [TIMESTAMP_LOG]
   Task: [description]

   ## Approach
   [High-level strategy]

   ## Proposed Changes

   ### File: [path]
   ```[language]
   [code]
   ```
   **Why:** [rationale]

   ## Architecture Improvements
   [New patterns, refactorings]

   ## Benefits
   [Long-term advantages]
   ```

2. Update `_overview.md`: Flow Log and Files entries

3. **DO NOT edit actual code files** - suggestions only

4. Report back with summary

#### Synthesis & Auto-Selection

After both agents complete:

1. Create `[SESSION_PATH]/[TIMESTAMP_FILE]-comparison-[task-slug].md`:
   ```markdown
   # Comparison: [task]

   ## Key Differences
   [What's fundamentally different]

   ## Solution 1: Minimal
   **Pros:** [list]
   **Cons:** [list]
   **Risk:** [Low/Medium/High]

   ## Solution 2: Clean
   **Pros:** [list]
   **Cons:** [list]
   **Risk:** [Low/Medium/High]

   ## Recommendation
   [Which approach and why]

   ## Hybrid Possibility
   [Can we combine best of both?]
   ```

2. **Auto-Selection Logic:**
   - **Default: Choose Clean Foundation** unless minimal has compelling justification
   - Choose Minimal only if:
     - Clean introduces significant complexity with unclear benefit
     - Minimal solves urgent issue with acceptable tradeoffs
     - Clean approach has high risk/uncertainty

3. **Complete common steps** for session files

4. Present comparison and ask:
   ```
   Which approach?
   1. Minimal footprint
   2. Clean foundation
   3. Hybrid
   4. Neither (rethink)
   ```

#### After User Confirms

1. **Implement chosen solution**
2. **Update plan progress** (mark items `- [x]`, add completion note)
3. **Complete common steps** (lint, commit code, update session, commit session)

IMPORTANT! If unsure about something, ask first.
