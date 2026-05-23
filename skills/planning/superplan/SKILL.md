---
name: superplan
description: Use when starting significant features, epics, or complex tasks. Creates multi-phase implementation plans with parallelizable phases, poker estimates, TDD-first acceptance criteria, and quality gates. Detects tech stack from CLAUDE.md/AGENTS.md (bypassing internet research if complete) or via codebase scan.
metadata:
  version: "2.1"
  generated-at: "2025-01-21"
compatibility: Internet access used for best practices research (bypassed if CLAUDE.md/AGENTS.md provides complete tech stack). Works with any codebase.
---

# Superplan: Comprehensive Feature Planning

## Overview

Superplan creates detailed, executable implementation plans that enable parallel agent execution. Each plan includes everything needed to implement a feature: requirements, architecture, code changes, tests, and acceptance criteria.

## When to Use Superplan

- Starting a new feature or epic
- Complex tasks requiring multiple phases
- Tasks that could benefit from parallel execution by multiple agents
- When you need comprehensive documentation of implementation decisions
- When the team needs to understand the full scope before committing

## Core Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPERPLAN WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│  1. INTAKE          →  Gather story/requirements from user          │
│  2. DETECT          →  Check CLAUDE.md/AGENTS.md first, then scan   │
│                        (BYPASS codebase scan if docs complete)      │
│  3. INTERVIEW       →  Ask clarifying questions                     │
│  4. RESEARCH        →  Look up best practices for DETECTED STACK    │
│                        (BYPASS if CLAUDE.md/AGENTS.md was complete) │
│  5. EXPLORE         →  Understand existing codebase patterns        │
│                        (ALWAYS runs - never bypassed)               │
│  6. REFACTOR ASSESS →  Evaluate if refactoring should precede work  │
│  7. ARCHITECT       →  Design solution with diagrams                │
│  8. PHASE           →  Break into parallelizable phases + ESTIMATES │
│  9. DETAIL          →  Specify code deltas per phase                │
│ 10. TEST            →  Define failing tests per phase (TDD)         │
│ 11. DOCUMENT        →  Write plan to docs/<feature>-plan.md         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## CRITICAL: Parallel Execution with Sub-Agents

**YOU MUST USE SUB-AGENTS OR PARALLEL TASKS** for every parallelizable operation:

| Operation | How to Execute |
|-----------|---------------|
| Independent file reads | Launch multiple Read tasks in single message |
| Code searches | Use Task tool with multiple Explore agents in parallel |
| Parallel phases (1A, 1B, 1C) | Execute using parallel sub-agents |
| Independent test suites | Run unit/integration/e2e concurrently |

**Example**: "Launch 3 sub-agents in parallel to implement Phases 1A, 1B, and 1C"

**IMPORTANT**: Each sub-agent MUST return its conventional commit message upon completion. The main agent MUST output all commit messages to the user. See [Phase Completion: Conventional Commit Message](#phase-completion-conventional-commit-message---required-per-phase).

---

## Poker Planning Estimates

All tasks and phases MUST include Fibonacci estimates: **1, 2, 3, 5, 8, 13, 21**

| Size | Meaning | Example |
|------|---------|---------|
| 1 | Trivial | Config value, typo fix |
| 2 | Small | Single file, simple function |
| 3 | Medium | Multi-file, new component |
| 5 | Large | Feature module, API endpoint |
| 8 | X-Large | Complex feature with dependencies |
| 13 | Epic chunk | Major subsystem change |
| 21 | Too big | **Split into smaller tasks** |

---

## Phase 1: INTAKE - Gather Requirements

### What You're Doing
Collecting the feature requirements from the user through story input.

### Actions

1. **Ask the user to provide their story/requirements** using one of these methods:
   - Copy/paste the story text directly
   - Provide a link to a ticket/story (Jira, Linear, GitHub Issue, etc.)
   - Use an MCP tool to fetch the story if available
   - Describe the feature verbally

2. **Capture the raw input** exactly as provided

3. **Identify the story type**:
   - User Story (`As a <role>, I want <capability>, so that <benefit>`)
   - Technical Task (implementation-focused)
   - Bug Fix (problem/solution)
   - Epic (large feature with sub-stories)

### Output
Document: Source, Type, Raw Requirements, Initial Understanding (1-2 sentences).

---

## Phase 2: DETECT - Technology Stack Analysis

### What You're Doing
Identifying the technology, programming language, and major frameworks to inform best practices research and quality gate setup.

### Detection Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DETECT PHASE FLOW                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. CHECK for CLAUDE.md or AGENTS.md in project root                        │
│     ├─ Found & Complete? → BYPASS codebase scanning for tech stack          │
│     │                   → BYPASS internet research (Phase 4)                │
│     │                   → Proceed directly to INTERVIEW (Phase 3)           │
│     └─ Not Found or Incomplete? → Continue with Detection Actions below     │
│                                                                             │
│  NOTE: This does NOT bypass EXPLORE phase (Phase 5) - always scan codebase  │
│        for patterns and integration points regardless of CLAUDE.md presence │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Check for Project Documentation Files

**FIRST**, check for `CLAUDE.md` or `AGENTS.md` at project root:

```bash
# Check for these files (in priority order):
1. CLAUDE.md   # Claude Code's project documentation
2. AGENTS.md   # Codex's project documentation
```

**If found**, parse for these tech stack elements:

| Element | What to Look For |
|---------|-----------------|
| Languages | "TypeScript", "Python", "Go", etc. in project description |
| Frameworks | Framework mentions: React, Next.js, FastAPI, Django, etc. |
| Build Tools | Package manager, bundler references: npm, pnpm, vite, etc. |
| Quality Tools | Linter/formatter/type checker config mentions |
| Testing Tools | Test framework references: jest, pytest, vitest, etc. |
| Dependencies | Key libraries and their versions |

### Completeness Check

A project documentation file is **COMPLETE** for tech stack if it answers ALL of:

- [ ] Primary language(s) identified
- [ ] Major framework(s) identified (if applicable)
- [ ] Build/package tools identified
- [ ] Quality tools identified (linter, formatter, type checker)
- [ ] Test framework identified

**If ALL boxes can be checked from the file** → Skip to Step 3 (output) and mark RESEARCH phase (Phase 4) as BYPASSED

**If ANY box is missing** → Continue with Step 2 (codebase detection)

### Step 2: Detection Actions (USE PARALLEL SUB-AGENTS)

**Only execute if CLAUDE.md/AGENTS.md is missing or incomplete.**

Launch **parallel Explore agents** to detect:

1. **Languages** - Primary language(s): TypeScript, Python, Go, Rust, Java, etc.
2. **Frameworks** - Major frameworks: React, Next.js, FastAPI, Django, Express, etc.
3. **Build Tools** - Package managers, bundlers: npm, pnpm, yarn, webpack, vite, etc.
4. **Quality Tools** - Existing linters, formatters, type checkers:
   - Linters: eslint, ruff, golint, pylint
   - Formatters: prettier, black, gofmt, rustfmt
   - Type checkers: tsc (TypeScript), mypy (Python), go vet
5. **Testing Tools** - Test frameworks: jest, pytest, go test, vitest, playwright

### Quality Tools Assessment

| Tool Type | If Present | If Missing |
|-----------|------------|------------|
| Linter | Note config path | Add to Phase 0 Bootstrap |
| Formatter | Note config path | Add to Phase 0 Bootstrap |
| Type Checker | Note config path | Add to Phase 0 Bootstrap |
| Test Framework | Note config path | Add to Phase 0 Bootstrap |

### Step 3: Output

Document:
- **Source**: CLAUDE.md/AGENTS.md or codebase scan
- **Languages**, frameworks, build tools, quality tools (present/missing), testing setup
- **Bootstrap requirements**
- **Research bypass status**: If CLAUDE.md/AGENTS.md provided complete info, note "RESEARCH PHASE BYPASSED - tech stack from project documentation"

---

## Phase 3: INTERVIEW - Clarifying Questions

### What You're Doing
Asking targeted questions to fill gaps in requirements before planning.

### Question Categories

Ask questions in these categories (select relevant ones):

1. **Scope & Boundaries** - MVP, out of scope, related features
2. **User Experience** - Primary users, user flow, mockups/designs
3. **Technical Constraints** - Performance, security, compliance, integrations
4. **Data & State** - Data sources, storage, migrations
5. **Testing & Validation** - Success criteria, test scenarios, sign-off
6. **Dependencies** - Blockers, external services, sequencing
7. **Quality Gates** - Existing CI/CD, required checks, coverage thresholds

### How to Interview

Ask 3-5 most relevant questions, then **wait for answers before proceeding**.

See [Interview Guide](references/INTERVIEW-GUIDE.md) for comprehensive question templates and strategies by feature size.

---

## Phase 4: RESEARCH - Best Practices Lookup

### What You're Doing
Researching current best practices as of TODAY'S DATE **for the DETECTED technology stack**.

### BYPASS Condition

**If DETECT phase found complete tech stack info in CLAUDE.md or AGENTS.md**, this phase is BYPASSED.

Skip directly to EXPLORE (Phase 5). The project documentation provides authoritative tech stack information.

**Otherwise**, proceed with research actions below.

### Research Actions (USE PARALLEL WEB SEARCHES)

Launch **parallel web searches** targeting the detected stack:

1. **[Language] [YEAR] best practices** - e.g., "TypeScript 2025 best practices"
2. **[Framework] [YEAR] patterns** - e.g., "React 2025 patterns"
3. **[Framework] security guidelines** - e.g., "Next.js security OWASP"
4. **[Language] testing best practices** - e.g., "Python pytest 2025"

### Research Areas

1. **Industry Standards** - Current best practices, security (OWASP), accessibility (WCAG)
2. **Technology-Specific** - Framework patterns, library versions, known gotchas
3. **Architecture Patterns** - Recommended patterns, anti-patterns, scalability
4. **Quality Tool Configs** - Recommended linter/formatter configs for detected stack

### Output
Document: Sources consulted, key findings by topic, specific recommendations for this feature.

---

## Phase 5: EXPLORE - Codebase Analysis

### What You're Doing
Understanding existing patterns, conventions, and integration points in the codebase.

### Exploration Targets

1. **Existing Patterns** - How similar features are implemented, conventions, testing patterns
2. **Integration Points** - Files/modules to touch, API contracts, shared utilities
3. **Technical Debt** - Areas needing refactoring, known issues affecting this work

### Output
Document: Relevant files table, patterns to follow, integration points, technical debt notes.

---

## Phase 6: REFACTOR/REWRITE ASSESSMENT

### What You're Doing
Evaluating whether the feature/fix would benefit from refactoring or rewriting existing code BEFORE implementation. This phase synthesizes your research on best practices with your exploration of the codebase to make a data-driven refactoring decision.

### CRITICAL: Be Bold

This phase empowers you to **proactively recommend refactoring**. Don't be timid—if the code needs work, say so. Use the Q&A system to discuss major refactoring opportunities with the user.

### Assessment Process (USE PARALLEL WEB SEARCHES)

**Step 1: Research Refactoring for Detected Stack**

Launch parallel web searches for stack-specific refactoring:
- **[Language] refactoring patterns 2025** - e.g., "TypeScript refactoring patterns 2025"
- **[Framework] code smells** - e.g., "React code smells anti-patterns"
- **[Dependency] migration guide** - For major dependencies that may need updating

**Step 2: Apply Code Smell Detection**

Using your exploration results, check for these smells in affected areas:

| Category | Smells to Check |
|----------|-----------------|
| **Bloaters** | Long methods, large classes, primitive obsession, data clumps |
| **OO Abusers** | Switch statements on types, parallel inheritance hierarchies |
| **Change Preventers** | Divergent change, shotgun surgery |
| **Dispensables** | Duplicate code, dead code, speculative generality |
| **Couplers** | Feature envy, inappropriate intimacy, message chains |

**Step 3: Architecture Assessment**

Evaluate:
- Does the current architecture cleanly support this feature?
- Will implementing this feature increase technical debt?
- Are there architectural patterns being violated?
- Is there a cleaner abstraction that would help?

**Step 4: Future Roadmap Interview**

**ASK THE USER** about upcoming features that might tip the scales toward refactoring:

> "Before I finalize the plan, I want to understand your roadmap:
> 1. What other features are planned for this area in the next 6 months?
> 2. How often does this part of the codebase change?
> 3. Are there pain points here that slow down development?
> 4. What's your risk tolerance for refactoring vs. shipping fast?"

This information is CRITICAL for making the right refactoring decision.

### Decision Framework

| Scenario | Recommendation |
|----------|----------------|
| Feature adds code to messy area | **Refactor first** |
| Feature touches well-structured code | **Implement directly** |
| Multiple upcoming features need same area | **Refactor first** |
| Team struggles to understand the code | **Refactor first** |
| One-off change to stable code | **Implement directly** |
| Tight deadline, low complexity | **Implement, document debt** |
| Tight deadline, high complexity | **Discuss trade-offs with user** |

### Refactoring Confidence Levels

Based on your assessment, declare a confidence level:

| Level | Description | Action |
|-------|-------------|--------|
| **LOW** | Code is clean, feature fits naturally | Proceed to ARCHITECT |
| **MEDIUM** | Some smells present, feature workable | Note debt, ask user preference |
| **HIGH** | Significant issues, feature will worsen debt | Recommend refactor phases |
| **CRITICAL** | Major rewrite needed, current approach unsustainable | Propose rewrite with Mikado/Strangler Fig |

### When Confidence is HIGH or CRITICAL

If you determine refactoring should precede the feature work:

1. **Ask permission explicitly**:
   > "Based on my analysis, I recommend refactoring [specific area] BEFORE implementing [feature]. This would involve:
   > - [Refactoring task 1]
   > - [Refactoring task 2]
   >
   > Benefits: [list benefits]
   > Risks of NOT refactoring: [list risks]
   >
   > **Do you want me to add refactoring phases to the plan?**"

2. **If approved**, prepend refactoring phases (Phase 0A, 0B, etc.) before feature phases

3. **Select appropriate methodology**:
   - **Mikado Method**: For complex, interconnected changes where you need to discover dependencies
   - **Strangler Fig**: For replacing entire subsystems incrementally
   - **Branch by Abstraction**: For swapping implementations behind interfaces
   - **Standard Refactoring**: For isolated code smell fixes

### Output

Document:
- Code smells found (with file locations)
- Architecture assessment summary
- Future roadmap impact analysis
- Refactoring confidence level (LOW/MEDIUM/HIGH/CRITICAL)
- Recommended refactoring methodology (if applicable)
- User's decision on refactoring

See [Refactoring Research](references/REFACTORING-RESEARCH.md) for comprehensive methodology details, code smell catalogs, and technology-specific patterns.

---

## Phase 7: ARCHITECT - Solution Design

### What You're Doing
Designing the technical solution with diagrams.

### Architecture Components

1. **High-Level Architecture** - System/component diagram, data flow
2. **API Design** (if applicable) - Endpoints, request/response schemas, error handling
3. **Data Model** (if applicable) - Schema changes, migrations
4. **Component Design** (if applicable) - Component hierarchy, state management, interfaces

### Diagram Format

Use ASCII/text diagrams for portability. See [Plan Template](references/PLAN-TEMPLATE.md) for diagram examples.

---

## Phase 8: PHASE - Parallel Work Breakdown with Estimates

### What You're Doing
Breaking work into phases with **poker estimates** that can be executed in parallel where possible.

### Phase Design Principles

1. **Independence**: Phases executable without waiting for others when possible
2. **Testability**: Each phase independently testable
3. **Clear Boundaries**: Well-defined inputs and outputs
4. **Estimated Size**: Each phase with poker estimate (target: 3-8 points)
5. **Quality Gated**: Each phase includes Definition of Done

### Parallelization Rules (CRITICAL: USE SUB-AGENTS)

- **CAN parallelize**: Independent components, separate API endpoints, unrelated tests
  - **Execute with parallel sub-agents**
- **CANNOT parallelize**: Sequential dependencies, shared state setup, migrations before data access

### Output

Create a phase dependency diagram showing:
- Phase 0 (Bootstrap/Setup) at top - **CONDITIONAL: only if quality tools missing**
- Parallel phases branching out
- Integration phase at bottom

Include dependency table with estimates:

| Phase | Name | Depends On | Parallel With | Estimate | Status |
|-------|------|------------|---------------|----------|--------|

---

## Phase 9: DETAIL - Code Deltas Per Phase

### What You're Doing
Specifying exact code changes for each phase.

### Code Delta Format

For each file, specify:
- **File path** and action: `(CREATE)` or `(MODIFY)`
- **Full file contents** for new files
- **Diff format** for modifications (show context lines with +/- changes)

See [Plan Template](references/PLAN-TEMPLATE.md) for full code delta examples.

---

## Phase 10: TEST - TDD Acceptance Criteria

### What You're Doing
Defining failing tests for each phase BEFORE implementation.

### Testing Pyramid

Follow the pyramid - more unit tests, fewer integration, even fewer E2E:
- **Unit Tests (80%)**: Business logic, utilities - fast, many
- **Integration Tests (15%)**: API contracts, database - medium
- **E2E Tests (5%)**: Critical user journeys only - slow, few

### Test-First Workflow

For each phase:
1. Write tests FIRST (they will fail)
2. Run tests to confirm they fail
3. Implement the code
4. Run tests to confirm they pass
5. All existing tests must still pass

### Durable vs Brittle Tests

Write **durable tests** that test behavior/outcomes, not implementation details:
- Test what the function DOES, not HOW it does it
- Test public API, not internal state
- Tests should survive refactoring without changes

See [Testing Pyramid](references/TESTING-PYRAMID.md) for comprehensive test examples and strategies.

---

## Definition of Done (Quality Gate) - REQUIRED PER PHASE

Every phase MUST include this Definition of Done checklist:

```markdown
### Definition of Done
- [ ] Code passes linter ([detected linter]: eslint/ruff/golint)
- [ ] Code passes formatter check ([detected formatter]: prettier/black/gofmt)
- [ ] Code passes type checker ([detected checker]: tsc/mypy/go vet)
- [ ] All new code has test coverage (target: 80%+)
- [ ] All new tests pass
- [ ] All existing tests still pass
- [ ] No new warnings introduced
- [ ] All tasks completed in this phase are checked off in the plan document
```

**IF QUALITY TOOLS MISSING**: Plan must include **Phase 0: Quality Bootstrap** before any implementation phases.

---

## Phase Completion: Conventional Commit Message - REQUIRED PER PHASE

**CRITICAL: At the end of EVERY phase, you MUST output a conventional commit message.**

### Rules

1. **OUTPUT ONLY** - Print the commit message to the console. **NEVER stage files. NEVER create commits.** The user will handle all git operations.
2. **Conventional Format** - Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
3. **Comprehensive Context** - Include all files changed, what was done, and relevant context
4. **BUBBLE UP FROM SUB-AGENTS** - When phases run in sub-agents or background tasks, the conventional commit message MUST be returned to the main process. The main agent MUST output all commit messages to the user so they can make commits for each phase.

### Commit Message Format

```
<type>(<scope>): <short summary>

<body - detailed description of changes>

Files changed:
- path/to/file1.ts (CREATE/MODIFY/DELETE)
- path/to/file2.ts (CREATE/MODIFY/DELETE)

<footer - breaking changes, issue references, etc.>
```

### Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `docs` | Documentation changes |
| `style` | Formatting, linting (no code change) |
| `chore` | Build, config, dependencies |
| `perf` | Performance improvements |

### Example Output

At the end of a phase, output:

```
PHASE 1A COMPLETE - Conventional Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

feat(auth): implement JWT token validation middleware

Add middleware to validate JWT tokens on protected routes.
Includes token parsing, signature verification, and expiry checks.
Extracts user claims and attaches to request context.

Files changed:
- src/middleware/auth.ts (CREATE)
- src/types/auth.ts (CREATE)
- src/routes/protected.ts (MODIFY)
- tests/middleware/auth.test.ts (CREATE)

Refs: #123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  DO NOT COMMIT - User will handle git operations
```

**IMPORTANT**: Always include the warning that the user will handle git operations. Never assume you will commit or stage files.

### Sub-Agent and Background Task Handling

When phases execute in parallel using sub-agents or background tasks:

1. **Sub-Agent Responsibility**: Each sub-agent MUST include its conventional commit message in its return output
2. **Main Agent Responsibility**: The main agent MUST:
   - Collect all commit messages from completed sub-agents/background tasks
   - Output each commit message to the user immediately upon sub-agent completion
   - Clearly label which phase each commit message belongs to

**Example - Parallel Phase Completion:**

```
PARALLEL PHASES COMPLETE (1A, 1B, 1C)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1A - Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
feat(auth): implement JWT token validation

Files changed:
- src/middleware/auth.ts (CREATE)
- tests/middleware/auth.test.ts (CREATE)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1B - Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
feat(api): add user profile endpoints

Files changed:
- src/routes/profile.ts (CREATE)
- src/types/user.ts (MODIFY)
- tests/routes/profile.test.ts (CREATE)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1C - Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
feat(ui): create settings page component

Files changed:
- src/components/Settings.tsx (CREATE)
- src/styles/settings.css (CREATE)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  DO NOT COMMIT - User will handle git operations for each phase
```

---

## Phase 11: DOCUMENT - Write the Plan

### What You're Doing
Writing the complete plan to `docs/<feature>-plan.md`.

### Plan Execution

Once the plan is complete, ask the user:

> **Would you like me to execute this plan with `/superbuild`, or do you want to review/modify it first?**

If the user wants to execute and has `superbuild` installed, invoke it directly with the plan path.

If `superbuild` is not installed, direct them to install it from: **https://github.com/adamos486/skills**

### Multi-File Strategy

Large plans may exceed file size limits (~25,000 tokens). When this happens:

1. **Split by logical boundaries**:
   - **File 1 (`-plan-1.md`)**: Executive Summary, Requirements, Research, Architecture
   - **File 2 (`-plan-2.md`)**: Phase 0 and Phase 1 (parallelizable phases)
   - **File 3+ (`-plan-N.md`)**: Remaining phases, Testing Strategy, Assumptions, Appendix

2. **Each file must be self-contained**:
   - Include header referencing the plan set
   - Include navigation links to other parts
   - Include Table of Contents for that file

3. **Size thresholds** (~4 tokens per word):
   - Under ~4,000 lines / ~20,000 tokens: Single file
   - Over ~4,000 lines / ~20,000 tokens: Split into multiple files

### Multi-File Header

```markdown
# [Feature Name] Implementation Plan - Part [N] of [Total]

> **Plan Set**: `docs/<feature>-plan-*.md`
> **This File**: Part [N] - [Section Names]
> **Navigation**: [Part 1](feature-plan-1.md) | [Part 2](feature-plan-2.md) | ...
```

### Plan Structure

See [Plan Template](references/PLAN-TEMPLATE.md) for the complete plan file structure including all sections, formats, and examples.

### Chunked Writing

For large plans, write in chunks to prevent context loss:
1. Write Overview + Requirements → Save
2. Write Architecture → Save
3. Write each Phase separately → Save after each
4. Write Assumptions + Appendix → Save

---

## Execution Flow

### Quick Reference

1. **Intake** → Ask for requirements, capture raw input, identify type
2. **Detect** → Check CLAUDE.md/AGENTS.md first; if complete, BYPASS scan + RESEARCH
3. **Interview** → Ask 3-5 clarifying questions, wait for answers
4. **Research** → Web search best practices (BYPASSED if CLAUDE.md/AGENTS.md complete)
5. **Explore** → Analyze codebase patterns and integration points (ALWAYS RUNS)
6. **Refactor Assess** → Evaluate code smells, interview on roadmap, decide if refactoring needed
7. **Architect** → Design solution with diagrams
8. **Phase** → Break into parallelizable phases WITH POKER ESTIMATES
9. **Detail** → Specify code deltas per phase WITH DEFINITION OF DONE
10. **Test** → Define failing tests (TDD) per phase
11. **Document** → Write to `docs/<feature>-plan.md`

**PHASE COMPLETION (after each phase during execution):**
- Check off all completed tasks in the plan document
- Output conventional commit message (NEVER commit, user handles git)

### Status Updates

Use checkpoint summaries after each major phase to show progress. Examples:

```
DETECT COMPLETE (from CLAUDE.md)
- Source: CLAUDE.md ✅
- Language: TypeScript
- Framework: Next.js 14
- Quality Tools: eslint ✅, prettier ✅, tsc ✅, jest ✅
- Bootstrap Required: No
- RESEARCH PHASE: BYPASSED (tech stack from project documentation)
```

```
DETECT COMPLETE (from codebase scan)
- Source: Codebase scan (no CLAUDE.md/AGENTS.md found)
- Language: TypeScript
- Framework: Next.js 14
- Quality Tools: eslint ✅, prettier ✅, tsc ✅, jest ✅
- Bootstrap Required: No
- RESEARCH PHASE: Required
```

```
REFACTOR ASSESSMENT COMPLETE
- Confidence: HIGH
- Code smells found: Long methods (3), duplicate code (2), feature envy (1)
- Future roadmap: 2 related features planned next quarter
- Recommendation: Refactor UserService before feature implementation
- User decision: APPROVED - Adding Phase 0A (refactor) to plan
```

```
PHASES DEFINED (with estimates)
- Total phases: 6 (including refactor phase)
- Total estimate: 31 points
- Refactor phase: 0A (5pts) - must complete first
- Parallelizable: 1A (8pts), 1B (5pts), 1C (3pts) - USE SUB-AGENTS
- Sequential: Phase 0A → Phase 1s → Phase 2 (5pts)
```

```
PHASE 1A COMPLETE
✅ Tasks checked off in plan document
✅ All Definition of Done criteria met

Conventional Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
feat(api): add user authentication endpoints

Implement login, logout, and token refresh endpoints.
Add request validation and error handling.

Files changed:
- src/routes/auth.ts (CREATE)
- src/middleware/validate.ts (MODIFY)
- tests/routes/auth.test.ts (CREATE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  DO NOT COMMIT - User will handle git operations
```

See [Execution Guide](references/EXECUTION-GUIDE.md) for full execution instructions, prompts, and checkpoint templates.

---

## References

For detailed guidance on specific topics:

- [Interview Guide](references/INTERVIEW-GUIDE.md) - Comprehensive question templates by category and feature size
- [Refactoring Research](references/REFACTORING-RESEARCH.md) - Refactoring methodologies (Mikado, Strangler Fig, Branch by Abstraction), code smells catalog, decision frameworks
- [Plan Template](references/PLAN-TEMPLATE.md) - Full plan file structure with all sections and examples
- [Testing Pyramid](references/TESTING-PYRAMID.md) - TDD workflow, test examples, durable vs brittle tests
- [Execution Guide](references/EXECUTION-GUIDE.md) - Step-by-step execution flow and checkpoint templates
