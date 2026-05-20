---
name: design-guards
description: Investigate a bug pattern audit report and design architectural guards (tests, contracts, structural changes) that provide immunity to each identified pattern. Use when user says "design guards", "design defenses", or wants architectural solutions for bug patterns.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: design-guards] Designing architectural guards for bug patterns...'"
          once: true
---

# Design Guards Skill

Take a bug pattern audit report and design architectural guards that make each pattern structurally impossible or instantly caught. This is a multi-pattern analysis driven by a pattern report rather than a single bug investigation.

## When to Use

- After `/audit-bugs` produces a bug pattern report
- User says "design guards", "design defenses", or "guard against these patterns"
- User wants architectural immunity for a set of identified bug patterns

## Arguments

Path to a bug pattern audit report (typically under `temp/audit-bugs/`). If not specified, use the most recent `temp/audit-bugs/bug_pattern_audit_*.md`.

## Critical Constraints

**NEVER:**
- Modify any source code files
- Propose bandaid fixes or direct-only patches
- Create files outside `temp/design-guards/` directory

**ALWAYS:**
- Use subagents for parallel codebase exploration
- Focus on structural immunity over one-off fixes
- Each guard must be concrete and testable
- All output goes under `temp/design-guards/` (create if needed)
- Final report: `temp/design-guards/defense_guards_{YYYY-MM-DD_HHMMSS}.md`
- Subagents must NOT create their own files - they return findings in their response text only
- Do not change any code

## Workflow

### Step 1: Parse the Bug Pattern Report

Read the input report and extract each pattern:
- Pattern name and description
- Affected components and sessions
- The root architectural gap identified

### Step 2: Investigate Each Pattern in Parallel

For each pattern (or group of related patterns), launch subagents to explore:

**Current State**
- Find all current instances of the pattern in the codebase (not just the ones that already caused bugs)
- Map which components are vulnerable to this pattern today

**Existing Guards**
- What tests, contracts, or validation already exists for this area?
- Why did existing guards miss these bugs?

**Architectural Solutions**
- How do well-designed parts of the codebase prevent similar issues?
- What structural pattern would make this class of bug impossible?
- What's the minimum change that provides maximum coverage?

### Step 3: Design Guards for Each Pattern

For each pattern, produce:

1. **Detection scan** - A concrete grep/search command or pattern that finds latent instances today
2. **Contract test** - A test that fails if the pattern re-emerges (description of what it asserts, not code)
3. **Structural guard** - An architectural change that makes the pattern impossible by construction (if applicable)
4. **Standard recommendation** - Whether this should become an enforced standard in `/audit-defense-standards`

Prioritize guards by:
- **Coverage**: How many bug instances would this single guard have prevented?
- **Automation**: Can it be enforced in CI/pre-commit, or does it require manual audit?
- **Cost**: How invasive is the change?

### Step 4: Write Report

Ensure `temp/design-guards/` exists (`mkdir -p`).

Save to: `temp/design-guards/defense_guards_{YYYY-MM-DD_HHMMSS}.md`

```markdown
# Defense Guards: {Report Title}

**Date:** {today}
**Source Report:** {path to bug audit report}
**Patterns Addressed:** {count}

## Summary
{Which patterns get guards, expected coverage, recommended standards}

## Guard N: {Pattern Name}

**Addresses Pattern:** {name} ({X} of {Y} historical bugs)

### Current Exposure
{How many latent instances exist in the codebase today}

### Detection Scan
{Runnable grep/search commands}

### Contract Test
{What the test asserts, where it belongs}

### Structural Guard
{Architectural change that prevents by construction}

### Standard Recommendation
{YES/NO - should this become an audit-defense-standards entry?}
{If YES: one-sentence rule statement}

---

## Standards to Add
{List of guards recommended as permanent standards for audit-defense-standards, with rule statements}
```

### Step 5: Terminal Summary

Output: guard count, coverage stats, how many standards recommended, and report location.
