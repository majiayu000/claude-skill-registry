---
name: code-review
description: "Comprehensive parallel code review using 5 specialized subagents: general, architectural, TypeScript, product/vision, and TDD/beads compliance"
---

# Parallel Code Review

## Overview

Conduct a comprehensive code review by dispatching 5 parallel subagents, each with a specialized focus. Results are synthesized into a unified review.

## When to Use

- Before merging significant changes
- After completing feature implementation
- When reviewing PRs from others
- Before deployment of major features

## The Process

### Step 1: Gather Context

First, collect the changes to review:
- For PRs: `gh pr diff`
- For local changes: `git diff main...HEAD` or `git diff --staged`
- Identify modified files and their purposes

### Step 2: Launch Parallel Subagents

Launch **5 parallel Sonnet agents** using the Task tool, each with a specialized review focus:

```
Use the Task tool to launch 5 agents IN PARALLEL (single message, multiple tool calls):
```

#### Agent 1: General Code Review
```
Review these changes for:
- Obvious bugs and logic errors
- Error handling gaps
- Edge cases not covered
- Code clarity and readability
- Test coverage for new code
- Security vulnerabilities (injection, auth, data exposure)

Focus on issues that would cause runtime failures or incorrect behavior.
Ignore style/formatting issues caught by linters.

Return a list of issues with:
- Severity (critical/high/medium/low)
- File and line reference
- Description and suggested fix
```

#### Agent 2: Architectural Review
```
Review these changes for architectural concerns:
- Does this follow existing patterns in the codebase?
- Are dependencies appropriate (no circular deps, correct layer boundaries)?
- Is the abstraction level correct (not too abstract, not too concrete)?
- Does this scale appropriately?
- Are there better existing utilities/helpers that should be used?
- Does this introduce technical debt?

Check consistency with CLAUDE.md and ARCHITECTURE.md if present.

Return architectural concerns with:
- Impact level (breaking/significant/minor)
- Description of the concern
- Recommended approach
```

#### Agent 3: TypeScript Review
```
Review these TypeScript changes for:
- Type safety issues (any abuse, unsafe casts, missing null checks)
- Generic usage (correct constraints, inference issues)
- Interface/type design (appropriate use of interfaces vs types)
- Import organization and module boundaries
- Async/await correctness (missing awaits, unhandled promises)
- Potential runtime type mismatches

Assume the code compiles - focus on semantic type issues.

Return TypeScript issues with:
- File and line reference
- The problematic pattern
- Type-safe alternative
```

#### Agent 4: Product/Vision/Roadmap Review
```
Review these changes against the project's vision and direction:
- Read README.md, CLAUDE.md, and any docs/ for project context
- Check recent git history to understand where the project is heading
- Does this change align with the project's goals?
- Does it conflict with planned features or recent direction changes?
- Are there naming/API inconsistencies with the broader product?
- Does this maintain the project's design philosophy?

Return alignment concerns with:
- What aspect of vision/roadmap it affects
- How the change diverges
- Suggestion to realign (or note if intentional evolution)
```

#### Agent 5: TDD & Beads Compliance Review
```
Review these changes for TDD discipline and beads issue tracking:

**TDD Compliance:**
- Are there corresponding test files for new code?
- Do tests follow RED-GREEN-REFACTOR pattern?
- Were tests written BEFORE implementation? (check git history/commits)
- Are test names clear and behavior-focused?
- Is test coverage adequate for the changes?
- Are there any implementation files without corresponding tests?

**Beads Issue Tracking:**
- Check `bd list` for related issues
- Are changes linked to beads issues?
- Do beads issues follow TDD labeling convention?
  - `tdd-red` labels for failing test issues
  - `tdd-green` labels for implementation issues
  - `tdd-refactor` labels for refactoring issues
- Are there orphaned changes not tracked in beads?
- Should new beads issues be created for discovered work?

**Workflow Compliance:**
- Is work being done in the right order? (red → green → refactor)
- Are dependencies between issues correct?
- Are issues being closed as work completes?

Return TDD/beads compliance issues with:
- Type (missing-test / wrong-order / untracked-work / missing-issue)
- File or feature affected
- Recommended action (create issue, add test, update labels)
```

### Step 3: Synthesize Results

After all agents complete:

1. **Deduplicate**: Remove issues flagged by multiple agents
2. **Prioritize**: Sort by severity/impact
3. **Filter**: Remove likely false positives:
   - Pre-existing issues not introduced by this change
   - Issues that linters/compilers would catch
   - Purely stylistic concerns not in CLAUDE.md
4. **Verify**: For critical issues, spot-check the code yourself

### Step 4: Present Findings

Format the review as:

```markdown
## Code Review Summary

**Files reviewed**: [list]
**Overall assessment**: [APPROVE / REQUEST CHANGES / COMMENT]

### Critical Issues (must fix)
1. [Issue] - [File:Line] - [Which review found it]

### Recommended Changes
1. [Issue] - [File:Line] - [Which review found it]

### Minor Suggestions
1. [Suggestion] - [File:Line]

### Positive Observations
- [What was done well]
```

## Key Principles

- **Parallel execution**: All 5 agents run simultaneously for speed
- **Specialized focus**: Each agent has deep expertise in their domain
- **Synthesis over duplication**: Consolidate overlapping findings
- **Signal over noise**: Filter aggressively to surface real issues
- **Actionable feedback**: Every issue should have a clear resolution path

## Agent Configuration

When launching agents:
- Use `model: "sonnet"` for thorough analysis
- Include the full diff/changes in each agent's prompt
- Include relevant context files (CLAUDE.md, README.md, package.json)
- Set clear expectations for output format

## Example Invocation

```
I need to review the changes in this PR. Let me launch 5 parallel review agents.

[Launch Task tool 5 times in a SINGLE message with the specialized prompts above]
```
