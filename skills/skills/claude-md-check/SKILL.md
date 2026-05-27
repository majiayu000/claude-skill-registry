---
name: claude-md-check
description: Validate CLAUDE.md structure and completeness
user-invocable: true
---

# CLAUDE.md Validator

Validate the project's CLAUDE.md file for completeness and best practices.

---

## Validation Checklist

### Required Sections (Must Have)
- [ ] **Project Overview** - Brief description
- [ ] **Tech Stack** - Languages, frameworks, tools
- [ ] **Commands** - dev, test, build commands

### Recommended Sections (Should Have)
- [ ] **Conventions** - Coding standards
- [ ] **Key Files** - Important files
- [ ] **Architecture** - Directory structure

### Quality Checks
- [ ] **No secrets** - No API keys in file
- [ ] **Correct commands** - Listed commands work
- [ ] **Up to date** - Matches actual dependencies

---

## Output Format

```markdown
## CLAUDE.md Validation Report

### Status: PASS / NEEDS IMPROVEMENT / MISSING

### Required Sections
| Section | Status | Notes |
|---------|--------|-------|
| Project Overview | | |
| Tech Stack | | |
| Commands | | |

### Issues Found
1. [Issue and how to fix]

### Suggestions
1. [Improvement]
```

---

## Auto-Fix

If issues found, offer to:
- Add missing sections with placeholders
- Update tech stack from package.json
- Verify and correct commands
