---
name: pre-work-research
description: Use before starting implementation - research repository documentation, codebase patterns, and external resources to inform the approach
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
model: opus
---

# Pre-Work Research

## Overview

Research before coding. Understand the landscape before changing it.

**Core principle:** Measure twice, cut once.

**Announce at start:** "I'm researching the codebase and documentation before implementing."

## When to Research

Research is appropriate when:

| Situation | Research Needed |
|-----------|-----------------|
| Unfamiliar area of codebase | Yes |
| New library or API | Yes |
| Complex integration | Yes |
| Performance-sensitive code | Yes |
| Security-sensitive code | Yes |
| Simple, isolated change | Minimal |

## The Research Protocol

### Step 1: Understand Requirements

Before researching implementation:

- Read the full issue description
- Review all acceptance criteria
- Note any constraints mentioned
- Identify unknowns

### Step 2: Research Repository Documentation

```bash
# Project overview
cat README.md

# Architecture/design docs
ls -la docs/
find . -name "*.md" -path "./docs/*"

# Contributing guidelines
cat CONTRIBUTING.md

# API documentation
cat docs/api*.md
cat docs/architecture*.md
```

**Look for:**
- Architecture decisions
- Design patterns used
- Coding conventions
- Testing requirements
- Deployment considerations

### Step 3: Research Existing Codebase

#### Find Similar Implementations

```bash
# Find similar features
grep -r "similar keyword" src/

# Find related tests
grep -r "similar keyword" **/*.test.*

# Find imports of relevant modules
grep -r "import.*ModuleName" src/
```

#### Understand Patterns

```bash
# How are similar things done?
# Look at 2-3 examples of similar functionality

# Example: If adding an API endpoint
grep -r "router\." src/routes/
cat src/routes/[existing-endpoint].ts

# Example: If adding a service
ls -la src/services/
cat src/services/[existing-service].ts
```

#### Check for Utilities

```bash
# What utilities exist?
ls -la src/utils/
cat src/utils/[relevant-util].ts

# Are there shared helpers?
grep -r "export function" src/utils/
```

### Step 4: Research External Resources

When using external APIs or libraries:

#### Official Documentation

```bash
# Read the docs for dependencies
pnpm info [package-name]
# Then visit documentation URL
```

```
Search: "[library-name] documentation"
Search: "[library-name] getting started"
Search: "[library-name] [specific feature]"
```

#### API References

For external APIs:

- Authentication requirements
- Rate limits
- Error handling
- Response formats
- Versioning

#### Community Resources

- GitHub issues for common problems
- Stack Overflow for patterns
- Blog posts for best practices

### Step 5: Document Findings

Create a research summary:

```markdown
## Pre-Work Research: Issue #[NUMBER]

### Requirements Understanding
- [Key requirement 1]
- [Key requirement 2]

### Codebase Patterns
- Pattern for [X]: See `src/example/pattern.ts`
- Utilities available: `src/utils/helper.ts`
- Test pattern: See `src/example/example.test.ts`

### External Dependencies
- [Library]: [Key findings]
- [API]: [Authentication method, rate limits]

### Approach
Based on research, the approach is:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Risks/Considerations
- [Risk 1]
- [Consideration 1]
```

### Step 6: Update Issue (If Significant)

If research reveals important context:

```bash
gh issue comment [ISSUE_NUMBER] --body "## Pre-Implementation Research

### Approach
[Summary of planned approach]

### Considerations
- [Important finding 1]
- [Important finding 2]

### Questions (if any)
- [Question needing clarification]
"
```

## Research Depth by Task Size

| Task Size | Research Depth |
|-----------|---------------|
| Trivial (typo, config) | None needed |
| Small (single file) | Quick pattern check |
| Medium (feature) | Full protocol |
| Large (system) | Extended research |

### Quick Pattern Check (5 min)

```bash
# Just verify pattern
grep -r "pattern" src/ | head -5
cat src/similar/example.ts | head -50
```

### Full Protocol (15-30 min)

Complete Steps 1-6 above.

### Extended Research (1+ hour)

- Read all relevant documentation
- Trace through existing implementations
- Create proof-of-concept if needed
- Document architectural considerations

## What to Look For

### In Documentation

| Look For | Why |
|----------|-----|
| Architecture diagrams | Understand system structure |
| Coding standards | Match existing style |
| Decision records | Understand why things are done a way |
| API contracts | Maintain compatibility |

### In Codebase

| Look For | Why |
|----------|-----|
| Similar features | Follow established patterns |
| Test patterns | Write consistent tests |
| Error handling | Handle errors consistently |
| Logging patterns | Log appropriately |

### In External Resources

| Look For | Why |
|----------|-----|
| Official examples | Use recommended patterns |
| Common pitfalls | Avoid known issues |
| Performance tips | Optimize appropriately |
| Security guidance | Implement securely |

## Research Outputs

After research, you should know:

- [ ] How similar features are implemented
- [ ] What patterns to follow
- [ ] What utilities are available
- [ ] What the testing approach should be
- [ ] Any risks or special considerations

## Checklist

Before starting implementation:

- [ ] Issue requirements understood
- [ ] Repository docs checked
- [ ] Similar code patterns found
- [ ] Relevant utilities identified
- [ ] External resources researched (if applicable)
- [ ] Approach documented
- [ ] Issue updated (if significant findings)

## Integration

This skill is called by:
- `issue-driven-development` - Step 5

This skill informs:
- `tdd-full-coverage` - How to write tests
- `strict-typing` - Type patterns to use
- `inline-documentation` - Documentation patterns
