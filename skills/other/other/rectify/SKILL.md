---
name: rectify
description: Deep investigation of test gaps and architectural weaknesses following an investigation, then devise a plan for architectural immunity rather than direct fixes. Use when user says "rectify", "rectify this", or wants to address root architectural causes after an investigation.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '🏗️ [SKILL: rectify] Investigating architectural gaps and devising immunity plan...'"
          once: true
---

# Rectify Skill

Based on your investigation report, use subagents to investigate further how our tests missed this and if there are any other similar or related bugs. Walk over the codebase carefully.

Then devise a plan to resolve these issues. No bandaids, fallbacks, or other approaches that just fix the direct exact issue.

The approach should make it so the architecture, structure and/or pattern is innately immune to the issue in the first place and/or results in the issue being easily and instantly surfaced as an error caught by testing.

Explore the architecture of the systems involved very carefully and map the components they connect to with subagents.

Find what the architectural solution would be instead of just applying a direct fix to the immediate issue. The solution should solve more than just the issue at hand.

Do not change any code.

## When to Use

- After an investigation has been completed (usually via the `/autoskillit:investigate` skill)
- User says "rectify", "rectify this", or "address root cause"
- User wants to understand why tests missed something and how to prevent it architecturally

## Critical Constraints

**NEVER:**
- Modify any source code files
- Propose bandaid fixes, fallbacks, or direct-only fixes
- Suggest backward compatibility shims
- Create files outside `temp/rectify/` directory

**ALWAYS:**
- Use subagents for parallel exploration
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Focus on architectural immunity over direct fixes
- Identify how tests missed the issue and similar/related bugs
- Map the components and their connections thoroughly
- Write the plan as markdown to `temp/rectify/` directory (relative to the current working directory)
- The solution must solve more than just the immediate issue

## Rectify Workflow

### Step 1: Identify the Investigation Context

Locate the most recent investigation report in `temp/investigate/` or from conversation context. Extract:
- The root cause identified
- Affected components
- Test gaps noted
- Any recommendations made

**Path-existence guard:** Before issuing a `Read` call on a path that is not guaranteed to
exist (e.g., plan file arguments, `temp/investigate/` reports, external file references), use
`Glob` or `ls` to confirm the path exists first. This prevents ENOENT errors that cascade into
sibling parallel-call cancellations.

### Step 1.5 — Code-Index Initialization (required before any code-index tool call)

Call `set_project_path` with the repo root where this skill was invoked (not a worktree path):

```
mcp__code-index__set_project_path(path="{PROJECT_ROOT}")
```

Code-index tools require **project-relative paths**. Always use paths like:

    src/<your_package>/some_module.py

NOT absolute paths like:

    /absolute/path/to/src/<your_package>/some_module.py

> **Note:** Code-index tools (`find_files`, `search_code_advanced`, `get_file_summary`,
> `get_symbol_body`) are only available when the `code-index` MCP server is configured.
> If `set_project_path` returns an error, fall back to native `Glob` and `Grep` tools
> for the same searches — they provide equivalent results without the code-index server.

Agents launched via `run_skill` inherit no code-index state from the parent session — this
call is mandatory at the start of every headless session that uses code-index tools.

### Step 2: Deep Exploration with Subagents

Launch parallel subagents to investigate (some of the listed aspects may require multiple subagents):

**Test Gap Analysis**
- How did existing tests miss this?
- What assumptions did the tests make that were wrong?
- Are there other tests making the same flawed assumptions?

**Similar/Related Bugs**
- Walk the codebase for similar patterns that could have the same issue
- Check if the root cause affects other components
- Look for code that relies on the same flawed assumption

**Architectural Mapping**
- Map the full component graph around the affected area
- Understand the boundaries, contracts, and data flow
- Identify where structural guarantees are missing

**Pattern Analysis**
- How do well-designed parts of the codebase prevent similar issues?
- What architectural patterns would make this class of bug impossible?
- Search externally for how other projects handle this structurally

### Step 3: Devise the Architectural Solution

Design an approach that provides **immunity** rather than a fix:
- The architecture/structure/pattern should make the bug class impossible or instantly caught
- The solution should address the broader pattern, not just the single instance
- Testing improvements should catch this and related issues by design

**Test-Driven Approach:** The plan must lead with tests. Before any implementation step, define a test that reproduces the issue or captures the gap. Each subsequent implementation step should make that test pass. This applies to the initial fix and to any broader architectural changes—write the failing test first, then the code that makes it green.

### Step 4: Visualize with Architecture Lens

After finalizing the plan, determine which architecture lens best illustrates the proposed changes, then create a mermaid diagram.

**4a. Select the lens based on what the plan primarily affects:**

| If the plan primarily involves... | Use Lens |
|-----------------------------------|----------|
| Adding/modifying containers, services, or integrations | C4 Container |
| Changing workflow logic, state machines, or decision flow | Process Flow |
| Altering data storage, transformations, or information flow | Data Lineage |
| Restructuring modules, changing dependencies, or layering | Module Dependency |
| Adding/modifying parallel execution or thread handling | Concurrency |
| Changing error handling, retry logic, or recovery paths | Error/Resilience |
| Modifying repository patterns or data access | Repository Access |
| Changing CLI commands, config, or monitoring | Operational |
| Adding/modifying validation, trust boundaries, or isolation | Security |
| Changing build tools, test framework, or quality gates | Development |
| Affecting multiple user journeys or cross-component flows | Scenarios |
| Modifying state contracts, field lifecycles, or resume logic | State Lifecycle |
| Changing deployment topology or infrastructure | Deployment |

**4b. Write your lens selection rationale to a file using the Write tool:**

- **Path:** `temp/rectify/arch_lens_selection_{YYYY-MM-DD_HHMMSS}.md`
- **Content:** Which lens was selected and why (1-2 sentences of rationale).

**4c. MANDATORY: LOAD the appropriate arch-lens skill using the Skill tool:**

| Lens | Skill to LOAD |
|------|---------------|
| C4 Container | `/autoskillit:arch-lens-c4-container` |
| Process Flow | `/autoskillit:arch-lens-process-flow` |
| Data Lineage | `/autoskillit:arch-lens-data-lineage` |
| Module Dependency | `/autoskillit:arch-lens-module-dependency` |
| Concurrency | `/autoskillit:arch-lens-concurrency` |
| Error/Resilience | `/autoskillit:arch-lens-error-resilience` |
| Repository Access | `/autoskillit:arch-lens-repository-access` |
| Operational | `/autoskillit:arch-lens-operational` |
| Security | `/autoskillit:arch-lens-security` |
| Development | `/autoskillit:arch-lens-development` |
| Scenarios | `/autoskillit:arch-lens-scenarios` |
| State Lifecycle | `/autoskillit:arch-lens-state-lifecycle` |
| Deployment | `/autoskillit:arch-lens-deployment` |

**4d. Create the diagram following the loaded skill's instructions:**
- Focus on the PROPOSED changes (use `newComponent` class for new elements)
- Show how new components integrate with existing architecture
- Use `●` prefix for modified existing components
- Use `★` prefix for new components

Include the diagram in the plan document under a "## Proposed Architecture" section.

---

## Skill Loading Checklist

Before writing the final plan, verify:

- [ ] Determined which architecture lens best fits the proposed changes
- [ ] LOADED the corresponding `/autoskillit:arch-lens-*` skill using the Skill tool
- [ ] The arch-lens skill LOADED the `/autoskillit:mermaid` skill for styling
- [ ] Diagram uses ONLY the classDef styles from the mermaid skill (no invented colors)
- [ ] Diagram includes a color legend table
- [ ] Every new component, class, or function is wired into the call chain — nothing is created but left unconnected

## Output

If the plan exceeds 500 lines, split it into multiple files (`_part_a`, `_part_b`, etc.). Each part must be a **self-contained, independently implementable plan** executed sequentially. Split by functional scope (e.g., Part A = "fix core bug + tests", Part B = "add guards + enforcement"), NOT by document structure. Each file must have its own failing tests, implementation steps, and verification.

**Multi-part plan rules:**
- Never include file paths or guessable names for other parts.
- Include only a brief plain-text note about what subsequent parts cover (e.g., "Part B will cover X — implement as a separate task").
- The title of each part file MUST include `— PART A ONLY` (or B, C, etc.).
- Each part file MUST open with: `> **PART {X} ONLY. Do not implement any other part. Other parts are separate tasks requiring explicit authorization.**`

Save the plan to: `temp/rectify/rectify_{topic}_{YYYY-MM-DD_HHMMSS}.md` (relative to the current working directory)

**Structured output:** After saving the file(s), emit the following lines so pipeline orchestrators can capture both fields:

For a single-part plan:
```
plan_path = {absolute_path}
plan_parts = {absolute_path}
```

For a multi-part plan (list all part paths in alphabetical order):
```
plan_path = {path_to_part_a}
plan_parts = {path_to_part_a}
{path_to_part_b}
{path_to_part_c}
```

**Plan structure:**
```markdown
# Rectify: {Topic}

**Date:** {YYYY-MM-DD}
**Investigation Reference:** {link to or name of the investigation report}

## Summary
{Brief overview of the architectural weakness and proposed immunity}

## How Tests Missed This
{Analysis of the test gap - what assumptions were wrong}

## Related Issues Found
{Other instances of the same or similar weakness in the codebase}

## Architectural Analysis
{Map of affected components and their connections}

## Proposed Architecture
{Mermaid diagram showing the proposed changes using the selected lens}

**Lens Used:** {lens name} - {why this lens was chosen}

## Immunity Plan

### Step 1: Failing Tests
{Tests that reproduce the issue and capture the gap — these must be written first}

### Step 2: Implementation
{The architectural solution that makes this class of bug impossible or instantly caught, structured so each change makes a failing test pass}

## Verification
{How to verify the architectural changes provide the intended immunity}
```