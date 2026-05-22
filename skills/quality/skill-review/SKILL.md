---
name: skill-review
description: Reviews and validates agent skills against best practices. Triggers on "review this skill", "check my skill", "validate skill", "is this skill well-written", or when creating/editing skills.
---

# Skill Review

## Overview

Validates agent skills against the Agent Skills standard and compiled best practices. Reviews structure, frontmatter, description quality, progressive disclosure, and common anti-patterns.

## When to Use

- User asks to review or validate a skill
- User is creating a new skill and wants feedback
- User asks "is this skill well-written?"
- User mentions skill quality, best practices, or improvement

## Review Process

### Phase 1: Load References

Before reviewing, read:
- `references/best-practices.md` — Comprehensive guidelines
- `references/checklist.md` — Quick validation checklist

### Phase 2: Identify Target

Determine what to review:
- **Single skill**: Review `skills/<name>/SKILL.md` and its structure
- **All skills**: Audit entire `skills/` directory
- **New skill draft**: Review provided content before creation

### Phase 3: Structural Audit

Check the skill directory structure:

```
skill-name/
├── SKILL.md              # Required
├── references/           # Optional - loaded docs
├── scripts/              # Optional - executable code
└── assets/               # Optional - output files (not loaded)
```

**Verify:**
- [ ] SKILL.md exists
- [ ] Directory name matches `name` in frontmatter
- [ ] References are one level deep (no nested chains)
- [ ] Scripts use forward slashes (no Windows paths)
- [ ] No extraneous files (README.md, CHANGELOG.md, etc.)
- [ ] Script paths in SKILL.md body (`scripts/foo.py`) exist in directory
- [ ] If scripts use external binaries, dependencies are documented

### Phase 4: Frontmatter Validation

Check YAML frontmatter:

```yaml
---
name: skill-name          # Required: lowercase, hyphens, ≤64 chars
description: >-           # Required: ≤1024 chars, third-person
  What it does. When to use it.
---
```

**Validate:**
- [ ] `name`: Lowercase with hyphens only (`[a-z0-9-]`)
- [ ] `name`: ≤64 characters
- [ ] `name`: No "anthropic" or "claude" in name
- [ ] `description`: Non-empty, ≤1024 characters
- [ ] `description`: Third-person voice (not "I can" or "You can")
- [ ] `description`: Includes what it does AND when to trigger
- [ ] `description`: Contains specific trigger phrases

### Phase 5: Description Quality

The description is **the** triggering mechanism. Evaluate:

**Good descriptions include:**
- Specific actions: "Extract text and tables from PDF files"
- Trigger phrases: "Use when analyzing Excel files, spreadsheets, or .xlsx"
- Synonyms users might say: "tabular data, CSV, workbooks"

**Bad descriptions:**
- Vague: "Helps with documents"
- Generic: "Processes data"
- Missing triggers: "Analyzes spreadsheets" (no "when to use")

### Phase 6: Body Analysis

Review SKILL.md body content:

**Length:**
- [ ] Under 500 lines (check with `wc -l`)
- [ ] If longer, split into reference files

**Progressive Disclosure:**
- [ ] Quick start or overview near top
- [ ] Details moved to references/
- [ ] Long reference files (>100 lines) have TOC

**Token Efficiency:**
- [ ] No obvious explanations (Claude already knows)
- [ ] Examples over lengthy prose
- [ ] Each line justifies its token cost

**Degrees of Freedom:**
- [ ] High freedom for context-dependent tasks
- [ ] Low freedom for fragile/error-prone tasks
- [ ] Defaults provided when multiple options exist

### Phase 7: Anti-Pattern Check

Scan for common issues:

| Anti-Pattern | Look For |
|-------------|----------|
| Windows paths | `scripts\file.py` instead of `scripts/file.py` |
| Nested references | A.md → B.md → C.md chains |
| Time-sensitive info | "If before August 2025..." |
| Magic numbers | Unexplained values |
| Too many options | "You can use X, or Y, or Z..." without default |
| Inconsistent terms | Mixing "endpoint"/"URL"/"route" |
| User-facing docs | README, CHANGELOG, installation guides |
| First/second person descriptions | "I can help" or "You can use" |

### Phase 8: Report Findings

Present findings using this format:

```
## Skill Review: [skill-name]

### Summary
[1-2 sentence overall assessment]

### Structure
[✓/✗] Directory organization
[✓/✗] File presence
[✓/✗] Reference depth

### Frontmatter
[✓/✗] name validation
[✓/✗] description validation

### Description Quality
**Score**: [Strong / Adequate / Needs Work]
**Issues**: [List specific problems]
**Suggested rewrite** (if needed):
```yaml
description: >-
  [Improved description]
```

### Body Analysis
**Line count**: [X] lines
**Token efficiency**: [Good / Could trim]
**Progressive disclosure**: [✓/✗]

### Anti-Patterns Found
- [Issue 1] — Location: `file:line`
- [Issue 2] — Location: `file:line`

### Recommendations
1. [Actionable fix]
2. [Actionable fix]
```

## Quick Review Mode

For rapid validation, run through the checklist in `references/checklist.md` and report only failures.

## Resources

### references/best-practices.md
Comprehensive guide covering architecture, design principles, writing effective descriptions, bundled resources, workflow patterns, and advanced patterns from production skills.

### references/checklist.md
Quick-reference validation checklist for fast reviews.
