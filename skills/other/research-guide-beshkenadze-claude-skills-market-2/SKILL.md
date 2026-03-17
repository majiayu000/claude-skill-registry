---
name: research-guide
description: Research best practices, guides, and libraries. Use when needing documentation, recommendations, implementation guidance, or library comparisons.
version: 1.0.0
---

# Research Guide

## Overview

Research and document best practices, guides, and library recommendations for any development topic. Leverages `/sc:research` for deep web research and synthesizes findings into detailed reports tailored to the project context.

## Instructions

### Step 1: Analyze Context

Before researching, understand the project context:
- Check `package.json`, `Cargo.toml`, `go.mod`, etc. for existing dependencies
- Review project structure to understand tech stack
- Identify constraints (language, framework, existing patterns)

### Step 2: Formulate Research Query

Build a focused research query based on:
- The specific topic or problem
- Project's tech stack and constraints
- Current year for up-to-date results

### Step 3: Execute Research

Use the `/sc:research` slash command:

```
/sc:research "[topic] best practices [tech-stack] [current-year]" --depth standard
```

For complex topics, use deeper research:
```
/sc:research "[topic]" --depth deep
```

### Step 4: Synthesize Report

Create a detailed report with structure:

```markdown
# Research Report: [Topic]

## Summary
Brief overview of findings (2-3 sentences)

## Recommended Libraries

| Library | Purpose | Stars | Last Update | Notes |
|---------|---------|-------|-------------|-------|
| lib-name | description | ~10k | 2024 | recommendation |

## Best Practices

### Practice 1: [Name]
- What: Description
- Why: Rationale
- How: Implementation guidance

### Practice 2: [Name]
...

## Implementation Guide

Step-by-step guidance for the specific project context.

## References
- [Source 1](url)
- [Source 2](url)

## Compatibility Notes
Project-specific considerations based on existing stack.
```

### Step 5: Save Report

Save to `claudedocs/research_[topic]_[timestamp].md`

## Examples

### Example: Research Authentication

**Input:** "Research best practices for authentication in our TypeScript backend"

**Process:**
1. Check project: TypeScript, Bun, Hono framework
2. Query: `/sc:research "authentication best practices TypeScript Hono 2025" --depth standard`
3. Synthesize findings into report

**Output:** Detailed report covering:
- JWT vs session comparison
- Recommended libraries (jose, arctic, lucia)
- Implementation patterns for Hono
- Security best practices

### Example: Research State Management

**Input:** "What's the best state management for React in 2025?"

**Process:**
1. Check project: React 18, TypeScript
2. Query: `/sc:research "React state management comparison 2025" --depth deep`
3. Compare options in project context

**Output:** Report with:
- Zustand vs Jotai vs Redux Toolkit comparison
- Bundle size analysis
- Recommended choice for project scale
- Migration guide if switching

### Example: Research Testing Strategy

**Input:** "Research testing best practices for our API"

**Process:**
1. Check project: Bun runtime, REST API
2. Query: `/sc:research "API testing best practices Bun TypeScript 2025"`
3. Tailor to existing test setup

**Output:** Report covering:
- Unit vs integration vs e2e strategy
- Recommended test runners (bun:test, vitest)
- Mocking strategies
- CI/CD integration

## Guidelines

- Always check project context before researching
- Include current year in queries for fresh results
- Prioritize libraries actively maintained (updated within 6 months)
- Consider bundle size and dependency count
- Note breaking changes between major versions
- Provide migration paths when recommending changes
- Save all reports to `claudedocs/` directory

## Report Quality Checklist

Before finalizing a report:
- [ ] Summary is concise and actionable
- [ ] Libraries include maintenance status
- [ ] Best practices have clear rationale
- [ ] Implementation guide matches project stack
- [ ] All sources are cited
- [ ] Compatibility with existing deps checked
