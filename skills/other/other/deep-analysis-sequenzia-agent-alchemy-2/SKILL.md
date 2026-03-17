---
name: deep-analysis
description: >-
  Deep codebase exploration and synthesis using parallel task agents with dynamic planning.
  Use when asked for "deep analysis", "analyze codebase", "explore and analyze",
  "investigate codebase", or "deep understanding".
user-invocable: true
license: MIT
compatibility: ">=1.2.0"
metadata:
  category: "analysis"
---

# Deep Analysis

Perform a deep, parallelized codebase analysis. Dynamically plan focus areas from reconnaissance, spawn parallel exploration task agents, then synthesize findings into a unified report.

## Phase 1: Reconnaissance & Planning

Determine the analysis context from `$ARGUMENTS`. If no arguments provided, default to "general codebase understanding".

Perform rapid codebase reconnaissance using `glob`, `grep`, and `read`:

1. **Directory structure** -- `glob` top-level directories and key subdirectories to understand layout
2. **Language/framework detection** -- `read` config files (`package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, etc.)
3. **File distribution** -- `glob` by extension (`**/*.ts`, `**/*.py`, etc.) to gauge area sizes
4. **Key documentation** -- `read` `README.md`, `AGENTS.md`, `CLAUDE.md`, `OPENCODE.md` if they exist
5. **Feature-focused** (if `$ARGUMENTS` targets a feature): `grep` for feature-related terms to identify hotspot directories
6. **General** (if no specific feature): identify the 3-5 largest or most significant directories

From reconnaissance results, generate **2-4 dynamic focus areas**. Each focus area must include:

- **Label**: Short descriptive name (e.g., "API Layer", "Authentication System", "Data Models")
- **Directories**: Which directories to explore
- **Starting files**: 2-5 key files to read first
- **Search patterns**: Grep patterns for deeper discovery
- **Complexity estimate**: Low / Medium / High

**Fallback**: If reconnaissance produces insufficient data (e.g., empty repo, unreadable files), use static focus area templates based on common project structures.

Compose a **team plan document** with:
- Analysis context (from `$ARGUMENTS` or default)
- Reconnaissance summary (languages, frameworks, structure)
- Focus areas with assignments
- Agent composition table (N explorers + 1 synthesizer)

## Phase 2: Plan Approval

Present the team plan to the user in a readable format showing:
- The analysis context
- Each focus area with its label, directories, starting files, and complexity
- The planned agent composition

Use the `question` tool to ask for approval:

> **Approve** -- Proceed with this plan
> **Modify** -- Adjust focus areas (describe changes)
> **Regenerate** -- Start over with different approach

- If **Modify**: ask what to change, apply modifications, re-present the plan. Allow up to 3 modification cycles.
- If **Regenerate**: ask for feedback on what went wrong, return to Phase 1 reconnaissance with adjusted strategy. Allow up to 2 regeneration cycles.
- If **Approve**: proceed to Phase 3.

## Phase 3: Parallel Exploration

Spawn one `task` agent per focus area, all in parallel. Each task agent receives:

- Its assigned focus area details (label, directories, starting files, search patterns)
- The analysis context
- Instructions to explore thoroughly using `read`, `glob`, and `grep`
- A structured output format to follow:
  - **Area Summary**: What this area does
  - **Key Components**: Important files, modules, classes, functions
  - **Patterns Found**: Design patterns, conventions, architectural decisions
  - **Dependencies**: Internal and external dependencies
  - **Notable Findings**: Anything surprising, problematic, or particularly well-designed

Set the `description` parameter for each task to `"Explore: [focus area label]"`.

Example task dispatch (adapt based on actual focus areas):

```
task({ description: "Explore: API Layer", prompt: "..." })
task({ description: "Explore: Data Models", prompt: "..." })
task({ description: "Explore: Authentication", prompt: "..." })
```

Launch all tasks simultaneously -- do NOT wait for one to finish before starting the next.

Wait for all parallel tasks to complete and collect their results.

**Error handling**: If a task agent fails or returns empty results, note the gap. Do not retry -- the synthesizer will work with partial results.

## Phase 4: Synthesis & Presentation

Spawn a single synthesis `task` agent with:

- All exploration results from Phase 3
- The original analysis context
- Access to `bash` for deeper investigation (git history, dependency graphs, line counts)
- Instructions to produce a unified analysis with:

  **1. Executive Summary** (3-5 sentences)

  **2. Architecture Overview**
  - High-level structure and component relationships
  - Key design patterns and conventions
  - Technology stack summary

  **3. Detailed Findings** (organized by focus area)
  - Merged insights from all explorers
  - Cross-cutting concerns identified across areas

  **4. Patterns & Conventions**
  - Coding style and conventions
  - Error handling approach
  - Testing strategy

  **5. Gaps & Recommendations**
  - Areas needing attention
  - Potential improvements
  - Technical debt observations

  **6. Key Metrics** (if discoverable via bash)
  - Lines of code by language
  - Test coverage indicators
  - Dependency counts

Set the synthesizer task `description` to `"Synthesize: Deep Analysis Results"`.

**Error handling**: If the synthesizer fails, present the raw exploration results from Phase 3 directly, organized by focus area.

Once synthesis completes, present the full analysis to the user.

## Tool Guidance

**Lead agent** (this skill): `read`, `glob`, `grep`, `bash`, `task`, `question`

**Explorer task agents**: `read`, `glob`, `grep` only -- read-only exploration, no writes, no bash

**Synthesizer task agent**: `read`, `glob`, `grep`, `bash` -- can run git commands, count lines, check dependencies

Note: The `question` tool is only available in this lead agent. Task agents cannot ask the user questions -- all necessary context must be provided in their task prompts.

## Guidelines

1. Keep focus areas distinct -- minimize overlap between explorer assignments
2. Provide each explorer with enough context to work independently
3. Include the full analysis context in every task prompt so agents understand the goal
4. The synthesizer should identify cross-cutting patterns that individual explorers may miss
5. Prefer concrete findings over vague observations
6. If invoked by another skill, return the structured synthesis for downstream use

**CRITICAL: Complete ALL 4 phases before finishing.**
