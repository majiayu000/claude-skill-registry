---
name: workflow-create-plan
description: This skill should be used when generating a detailed implementation plan from an existing PRD and codebase research. It synthesizes requirements with codebase context into actionable, bite-sized TDD tasks suitable for junior developers.
---

# Create Implementation Plan Workflow

## Overview

Generate a detailed implementation plan from an existing Product Requirements Document (PRD) and codebase research document. The plan synthesizes the "what" from the PRD with the "how" from research, creating actionable tasks, phases, and dependencies for development.

**Type:** FLEXIBLE - Adapt task granularity to the complexity of the feature.

**Output:** `plan.md` (detailed) and `Architecture-Decisions.md` (concise decision log), both with YAML frontmatter.

## When to Use

Use this workflow when:
- A PRD exists and you need to plan implementation
- Research has been conducted and you need actionable tasks
- Breaking down a feature into developer-ready work items
- Creating a step-by-step guide for junior developers

**Announce at start:** "I'm using the create-plan workflow to generate an implementation plan with decision log."

## Core Principles

- Assume the implementer has **zero context** for the codebase
- Document everything: which files to touch, exact code, how to test
- **Bite-sized tasks** (2-5 minutes each)
- **TDD approach**: Write failing test -> Run -> Implement -> Verify -> Commit
- DRY, YAGNI, frequent commits
- **Decision logging**: Extract key architectural choices into scannable ADR format

## Initial Setup

When this workflow is invoked (e.g., with `path/to/prd-file.md path/to/research-file.md [optional: feature-name]`), respond with:

```
I'm ready to create an implementation plan. I'll read the provided PRD and research files, then synthesize them into actionable steps. If you have a specific feature name, provide it; otherwise, I'll infer from the PRD.
```

Parse arguments:
- `prd_file`: Absolute path to the PRD Markdown file.
- `research_file`: Absolute path to the research Markdown file.
- `feature_name` (optional): Slug for output filename (e.g., "user-auth"); default to sanitized PRD title.

Validate paths exist using List tool. If invalid, prompt: "Please provide valid absolute paths to the PRD and research files."

If no arguments are parsed, try to look for `./research.md` file and `./prd.md` file.

## Steps to Follow

### Step 1: Read Input Files Fully

- Use Read tool (no offset/limit) to read PRD and research files in parallel.
- Extract key elements:
  - From PRD: Goals, User Stories, Functional Requirements, Non-Goals, Success Metrics, Open Questions.
  - From Research: Summary, Detailed Findings, Code References (file paths/lines), Architecture Insights, Historical Context.
- **CRITICAL**: Do this in main context before any sub-tasks to ensure full understanding.

### Step 1.5: Detect Project Language and Load Skills

Scan the repository root for language-specific configuration files:

| File Present | Language | Skills to Load |
|--------------|----------|----------------|
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python | `python-dev-guidelines`, `python-testing-guidelines` |
| `package.json` | TypeScript/JavaScript | (future: ts-dev-guidelines) |
| `go.mod` | Go | (future: go-dev-guidelines) |
| `Cargo.toml` | Rust | (future: rust-dev-guidelines) |

Use the `skill` tool to load all detected skills before proceeding. These skills contain critical implementation patterns that MUST be reflected in the plan.

> **CRITICAL for Python projects**: After loading `python-testing-guidelines`, ensure ALL test tasks follow these requirements:
> - All tests MUST use dummy classes that inherit from real classes (NO `unittest.mock`, `Mock`, `MagicMock`, `AsyncMock`, or `patch()`)
> - Tests mirror source structure: `src/module/file.py` → `tests/module/test_file.py`
> - All fixtures and dummy classes MUST be centralized in `tests/fixtures.py`
> - Error-as-value pattern for new code: functions return `(result, error)` tuples

### Step 2: Analyze and Decompose

- Ultrathink: Map PRD requirements to research findings (e.g., "User login flow" -> relevant auth components from research).
- Identify gaps: If PRD questions remain open or research lacks details, ask 1-3 targeted clarifying questions (e.g., "What priority for [requirement]? Options: a) High, b) Medium, c) Low").
- Create internal todo list with todowrite for plan components (e.g., tasks, dependencies). Break into phases: Planning, Implementation, Testing, Deployment.
- Consider: Existing patterns from research, security best practices, integration points.

### Step 3: Refine with Sub-Agents (If Needed)

Spawn parallel Task agents only for gaps (e.g., feasibility checks):
- Use `codebase-analyzer` for deep dives on unresolved PRD requirements (prompt: "Analyze how to implement [specific req] using existing codebase patterns from [research summary]. Return code examples and file paths.").
- Use `codebase-locator` to find additional files if research is outdated (prompt: "Locate files related to [PRD component] not covered in [research file].").

Limit to 2-3 agents; wait for all to complete before proceeding.
Incorporate results into decomposition (update todo).

### Step 4: Synthesize the Plan

Compile: Connect PRD goals to research-backed tasks. Prioritize based on dependencies and risks.

Generate metadata:
- date: Current ISO datetime.
- planner: "opencode".
- git_commit: Current hash (via Bash: `git rev-parse HEAD`).
- branch: Current branch (via Bash: `git branch --show-current`).
- repository: Repo name (infer from git remote or env).
- feature: feature_name or inferred.
- tags: [plan, feature-name, relevant-tags-from-prd/research].
- status: complete.
- last_updated: YYYY-MM-DD.
- last_updated_by: "opencode".

Structure the document with YAML frontmatter + content (saved as `plan.md` via Edit tool, but only after user confirmation).

### Step 5: Extract and Format Architecture Decisions

From the synthesized plan content, extract 6-8 key architectural decisions and format them as ADR (Architecture Decision Records). This happens automatically without user prompting.

**Decision Extraction Guidelines:**

Extract decisions from these plan sections:
- Architecture approach
- Tech stack selections
- Data modeling choices
- Integration patterns
- Testing strategies
- Design patterns used

**Decision Format (per decision):**

```markdown
### [DECISION #]: [Decision Title]

**Status:** Accepted

**Context:**
[2-3 sentences explaining the problem space or constraints]

**Decision:**
[1-2 sentences clearly stating the chosen approach]

**Justification:**
[4-5 bullet points with positive framing:]
- [Benefit 1: positive impact, measurable advantage]
- [Benefit 2: what we gain from this approach]
- [Benefit 3: efficiency, maintainability, or performance win]
- [Benefit 4: alignment with existing patterns or best practices]
- [Benefit 5: specific advantage over alternatives]

**Alternatives Considered:**
- [Alternative A]: [Brief description + why not chosen]
- [Alternative B]: [Brief description + why not chosen]

**Rationale:**
[1-2 sentences synthesizing the justification into a clear choice statement]
```

**Generate Architecture-Decisions.md:**

```markdown
---
date: [ISO datetime]
planner: opencode
git_commit: [hash]
branch: [name]
repository: [name]
feature: "[feature_name]"
status: accepted
---

# Architecture Decisions: [Feature Name]

> **Generated from:** plan.md
> **Review time:** 5-10 minutes

## Decision Summary

This document captures 6-8 key architectural decisions for the [feature name]. Each decision follows the ADR (Architecture Decision Record) format with positive justification for the chosen approach.

---

[Insert 6-8 decisions using format above]

---

## Implementation Tracking

These decisions are reflected in the detailed implementation tasks in plan.md:

- Decision 1 → Tasks [X-Y] [description]
- Decision 2 → Tasks [A-B] [description]
...

## Related Documents

- PRD: [prd_file path]
- Research: [research_file path]
- Implementation Plan: plan.md
- Git Commit: [hash]
```

### Step 6: Generate Plan Document

```markdown
---
date: [ISO datetime]
planner: opencode
git_commit: [hash]
branch: [name]
repository: [name]
feature: "[feature_name]"
tags: [plan, ...]
status: complete
last_updated: [YYYY-MM-DD]
last_updated_by: opencode
prd_source: [prd_file path]
research_source: [research_file path]
language: [detected language]
loaded_skills: [list of loaded skill names]
---

# Implementation Plan: [Feature Name]

> **For execution:** Use the `workflow-implement-plan` skill to execute this plan task-by-task with batch checkpoints.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---

**Date**: [ISO datetime]
**Planner**: opencode
**Git Commit**: [hash]
**Branch**: [name]
**PRD Source**: [prd_file]
**Research Source**: [research_file]

## Overview
[Brief synthesis: Problem from PRD + key research insights.]

## Goals (from PRD)
[List measurable objectives from PRD.]

## Task Breakdown

### Task 1: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

### Task 2: [Next Component]
[Same structure: Files, Step 1-5]

...

## Language-Specific Guidelines

[If Python project, include:]
> **Python Testing Requirements** (from `python-testing-guidelines`):
> - NO `unittest.mock` - use dummy classes inheriting from real classes
> - All dummies and fixtures in `tests/fixtures.py`
> - Test classes named: `TestMethodName` or `TestClassNameMethodName`
> - Error-as-Value pattern: functions return `(result, error)` tuples

## Dependencies & Risks
- Dependencies: [e.g., "Requires Auth module from research Component 1"]
- Risks: [From research insights + PRD non-goals]

## Code References (from Research)
- `path/to/file.py:123` - [Brief desc + relevance to plan]
- [List 5-10 key ones]

## Success Metrics (from PRD)
[Restate + verification steps]

## Open Questions
[Any gaps; suggest follow-ups.]
```

### Step 7: Save and Present

- Confirm with user: "Here's the proposed plan summary: [concise 3-5 bullet overview]. Shall I generate the full plan.md and Architecture-Decisions.md?"
- If yes, use Write tool to write both files:
  - `plan.md`: Detailed implementation plan
  - `Architecture-Decisions.md`: Concise decision log (6-8 ADR-style decisions)
- Output: Present summary with key tasks, decisions, and code refs. Ask: "Any follow-ups or adjustments?"

## Handle Follow-Ups

- Update plan.md: Add `## Follow-up [timestamp]` section, update frontmatter (last_updated, last_updated_by, last_updated_note).
- Update Architecture-Decisions.md: If decisions change, add `## Decision Updates [timestamp]` section with new or modified decisions.
- Re-run steps 3-5 for new info; spawn sub-agents as needed.

## Task Granularity

**Each step is ONE action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

**Task requirements:**
- Exact file paths always (`src/auth/login.ts:45-67`)
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant code from research

## Important Notes

- Parallelism: Read files and sub-agents in parallel for efficiency.
- Read-Only: No code changes; focus on planning.
- Conventions: Mimic codebase style from research. Follow security (no secrets).
- Junior-Dev Focus: Tasks explicit, with file refs for navigation. Assume zero codebase context.
- Edge Cases: If no feature_name, infer from PRD title (e.g., slugify "User Login" -> "user-login").
- Tools: Use todowrite for internal tracking; Bash for git metadata.
- TDD: Every task follows Write Test -> Fail -> Implement -> Pass -> Commit cycle.
- **Decision Log**: Always generated alongside plan.md. Automatic, non-optional part of plan creation.
- **Positive Framing**: Decision justifications use positive language (what we gain, not what we avoid).
- **Abstraction Level**: Architecture-Decisions.md is higher-level than plan.md - captures cross-cutting choices, not implementation details.

## Integration with Other Workflows

After plan is complete, offer:

**"Plan complete and saved to `plan.md` and `Architecture-Decisions.md`. Ready to implement?"**

- Use **workflow-implement-plan** skill to execute with batch checkpoints
- Or implement manually following the step-by-step tasks
- Review Architecture-Decisions.md for 5-10 minutes to understand key architectural choices before implementation
