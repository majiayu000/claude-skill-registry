---
name: pr-description-template
description: PR description templates with format specifications and examples. Use when generating PR descriptions. Provides the complete PR structure and writing guidance.
argument-hint: "[template-type: feature | bugfix | refactor | format | help]"
allowed-tools: Read, Glob
---

# PR Description Template Skill

This skill provides everything needed to write high-quality PR descriptions: templates, format specifications, and examples.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/pr-description-template` | Show available templates and help |
| `/pr-description-template feature` | Example PR for new feature implementations |
| `/pr-description-template bugfix` | Example PR for bug fixes |
| `/pr-description-template refactor` | Example PR for refactoring/architectural changes |
| `/pr-description-template format` | Show complete PR description format |

---

## Available Templates

| Template | Use For | Characteristics |
|----------|---------|-----------------|
| **feature** | New functionality, APIs, components | Emphasizes scope, design decisions, future work |
| **bugfix** | Bug fixes, regressions, hotfixes | Emphasizes root cause, testing, before/after |
| **refactor** | Architectural changes, code restructuring | Emphasizes compatibility, migration, incremental changes |

### Template Selection Guide

**Choose `feature` when:**
- Adding new functionality (greenfield development)
- Implementing new APIs, services, or components
- Adding new user-facing features
- Introducing new capabilities to the codebase

**Choose `bugfix` when:**
- Fixing a bug of any size
- Addressing regressions
- Hotfixes for production issues
- Correcting unexpected behavior

**Choose `refactor` when:**
- Making architectural changes
- Restructuring code without changing behavior
- Reorganizing modules or file structure
- Implementing breaking changes with migration
- Improving code quality without adding features

---

## PR Description Format

**Every PR description MUST follow this structure.** This is the canonical format for all pull requests.

### Required Sections

```markdown
## Summary

<High-level summary of changes and context for why the changes were made.
Should answer: What does this PR do? Why is it needed?
Keep to 2-4 sentences. Focus on business value and user impact.>

## What's Included

<Compact list organized by category to help reviewer understand scope at a glance>

**Source Code:**
- `path/to/file.py` - Brief description of change

**Tests:**
- `tests/test_file.py` - What's being tested

**Documentation:**
- `docs/file.md` - What was documented (or note if missing)

**Configuration:**
- `pyproject.toml` - Dependencies added/changed

## Key Design Decisions

<Design decisions to document for reviewer context.
Focus on "why this approach" not implementation details.
Number each decision for easy reference in review comments.>

1. **Decision Title**: Rationale for why this approach was chosen over alternatives

2. **Convention Deviation** (if any): Any intentional deviations from development-conventions with justification

## Critical Areas for Review

<Prioritized areas deserving careful review.
Help reviewer focus their attention on what matters most.
Include line numbers when specific ranges need attention.>

1. **`path/to/critical/file.py:L10-L50`** - Description of why this needs careful review (e.g., complex logic, security implications, breaking change)

2. **`path/to/another/file.py`** - Why this is important to review
```

### Optional Sections

Include these when applicable:

```markdown
## Future Phases

<Only include if this PR is a partial implementation of a larger plan>

The following phases from the [implementation plan](<plan-path>) are planned for future PRs:
- **Phase N**: Brief description of what's coming
- **Phase M**: Brief description of what's coming

## Breaking Changes

<Only include if there are breaking changes>

- **Change**: Description of what breaks
- **Migration**: How to update dependent code
- **Deprecation Timeline**: When old behavior will be removed (if applicable)

## Testing Notes

<Only include if testing requires special setup or has important caveats>

- How to test locally
- Required environment setup
- Known edge cases
```

---

## Writing Guidelines

### Summary Section

**DO:**
- Start with what the PR accomplishes (the "what")
- Explain why it's needed (the "why")
- Mention user-facing impact if applicable
- Keep it concise (2-4 sentences)

**DON'T:**
- List files changed (that's for "What's Included")
- Include implementation details
- Use vague language like "various improvements"
- Make it longer than a short paragraph

**Good Example:**
> Adds batch processing support for the data pipeline, enabling processing of up to 10,000 records in a single operation. This addresses the performance bottleneck reported in issue #123 where large datasets caused timeouts.

**Bad Example:**
> This PR updates processor.py and adds tests. Made some improvements to the code.

### What's Included Section

**DO:**
- Group by file type (Source, Tests, Documentation, Configuration)
- Use relative paths from repository root
- Keep descriptions to one line per file
- Highlight new files vs modified files if helpful

**DON'T:**
- Include every file if there are many (summarize: "15 test files for new validators")
- Add excessive detail (save that for design decisions)
- Forget to mention documentation updates (or note "Documentation: None" if appropriate)

### Key Design Decisions Section

**DO:**
- Number decisions for easy reference in reviews
- Explain the "why" not the "what"
- Mention alternatives considered when relevant
- Flag any convention deviations with justification

**DON'T:**
- Repeat implementation details
- Include decisions that are obvious
- Skip this section (even simple PRs have at least one decision worth noting)

### Critical Areas for Review Section

**DO:**
- Prioritize areas by importance
- Include line numbers for specific ranges
- Explain WHY each area needs attention
- Mention security, complexity, or breaking change concerns

**DON'T:**
- List every file (only truly critical areas)
- Be vague ("please review carefully")
- Skip this section (helps reviewers use their time effectively)

---

## Title Guidelines

PR titles should be concise and descriptive:

**Format:** `<type>: <brief description>`

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code restructuring
- `docs:` - Documentation only
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

**Good Examples:**
- `feat: Add batch processing for data pipeline`
- `fix: Resolve timeout on large dataset uploads`
- `refactor: Extract validation logic into separate module`

**Bad Examples:**
- `Update files` (too vague)
- `Fix bug` (what bug?)
- `WIP` (not ready for review)

---

## Action Instructions

Based on the argument provided, perform one of these actions:

### `/pr-description-template` (no args) or `/pr-description-template help`
Show this overview with available templates and commands.

### `/pr-description-template feature`
Read and display: `.claude/skills/pr-description-template/example-feature.md`

### `/pr-description-template bugfix`
Read and display: `.claude/skills/pr-description-template/example-bugfix.md`

### `/pr-description-template refactor`
Read and display: `.claude/skills/pr-description-template/example-refactor.md`

### `/pr-description-template format`
Display the "PR Description Format" section from this skill.

---

## Template File Locations

All example templates are in this skill directory:

- `example-feature.md` - Complete example for new feature PRs
- `example-bugfix.md` - Complete example for bug fix PRs
- `example-refactor.md` - Complete example for refactoring PRs
