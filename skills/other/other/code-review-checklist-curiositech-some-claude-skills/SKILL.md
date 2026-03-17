---
name: code-review-checklist
description: Generates comprehensive, context-aware code review checklists tailored to the specific codebase, programming language, and team standards. Analyzes PR diffs and suggests what reviewers should focus on.
category: Code Quality & Testing
tags:
  - code-review
  - quality
  - checklist
  - pr-review
  - best-practices
allowed-tools: Read, Grep, Glob
---

# Code Review Checklist Generator

Generate thorough, contextual code review checklists that help reviewers focus on what matters most for each specific PR.

## When to Use

- Before starting a code review to know what to look for
- When onboarding new team members to review standards
- To ensure consistent review quality across the team
- When reviewing unfamiliar parts of the codebase

## Approach

1. **Analyze the Diff**: Understand what files changed and the nature of changes
2. **Identify Patterns**: Detect the type of change (feature, bugfix, refactor, etc.)
3. **Language-Specific Checks**: Apply relevant checks for the programming language
4. **Project Context**: Consider existing patterns and conventions in the codebase
5. **Generate Checklist**: Produce prioritized, actionable review items

## Checklist Categories

### Security
- [ ] Input validation present
- [ ] No hardcoded secrets or credentials
- [ ] Proper authentication/authorization checks
- [ ] SQL injection prevention
- [ ] XSS prevention for web code

### Performance
- [ ] No N+1 query patterns
- [ ] Appropriate caching considered
- [ ] No unnecessary loops or iterations
- [ ] Efficient data structures used

### Maintainability
- [ ] Code is readable and self-documenting
- [ ] Functions are appropriately sized
- [ ] No code duplication
- [ ] Consistent naming conventions

### Testing
- [ ] Unit tests cover new functionality
- [ ] Edge cases are tested
- [ ] Tests are meaningful, not just for coverage

## Best Practices

- Prioritize security issues first
- Focus on logic errors over style nitpicks
- Consider the reviewer's time - highlight critical items
- Adapt checklist to project maturity level