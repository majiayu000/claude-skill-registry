---
name: git-workflow
description: Git commit, PR, and branching standards with ZERO TOLERANCE for AI attribution. Use when (1) Creating commits, (2) Writing commit messages, (3) Creating pull requests, (4) Writing PR descriptions, (5) Branching or merging code. ABSOLUTE RULE - NEVER include "Claude", "Anthropic", "AI-generated", emojis with "Generated with", or any AI tool attribution in commits, PRs, issues, or documentation.
---

# Git & PR Workflow Standards

## Core Principles

* **Small PRs:** ≤300 LOC changed ideally
* **Commit often:** Early, meaningful commits with clear messages
* **Linear history:** Prefer rebase over merge commits
* **Professional:** No AI attribution, no tool branding, clean descriptions

## 🚨 ABSOLUTE ZERO-TOLERANCE RULE: NO AI ATTRIBUTION 🚨

**NEVER, UNDER ANY CIRCUMSTANCES, include ANY of the following in:**
* Git commit messages
* Pull request descriptions
* Issue comments
* GitHub discussions
* Code comments
* Documentation
* ANY public-facing repository content

### ❌ STRICTLY FORBIDDEN TEXT - NEVER USE

* "Claude"
* "Anthropic"
* "claude.com"
* "Claude Code"
* "Claude Desktop"
* "Generated with Claude"
* "Co-Authored-By: Claude"
* "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
* "Co-Authored-By: Claude <noreply@anthropic.com>"
* Any emoji followed by "Generated with" or "Powered by"
* Any reference to AI assistants, AI code generation, or automated tools
* Any branding, attribution, or links to third-party AI services

### ✅ CORRECT FORMAT - ALWAYS USE

* Clean, professional commit messages
* Clear description of what changed
* Explanation of why the change was made
* No attribution, no branding, no tool references

## Examples

### ❌ FORBIDDEN COMMIT

```
Add multi-dimension vector support

- Support for 384, 768, 1024, and 1536 dimensions
- Update validation logic for new dimensions
- Add comprehensive test coverage

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### ✅ CORRECT COMMIT

```
Add multi-dimension vector support

- Support for 384, 768, 1024, and 1536 dimensions
- Update validation logic for new dimensions
- Add comprehensive test coverage
```

### ❌ FORBIDDEN PR DESCRIPTION

```markdown
## Summary
Implemented new authentication flow with JWT tokens.

## Test Plan
All tests passing.

---
🤖 Powered by Claude
```

### ✅ CORRECT PR DESCRIPTION

```markdown
## Summary
Implemented new authentication flow with JWT tokens.

## Test Plan
All tests passing.
```

## Enforcement

* **ZERO TOLERANCE** rule with **NO EXCEPTIONS**
* Every commit must be verified before pushing
* Every PR must be reviewed for attribution before creating
* If attribution is found, it must be removed immediately via force push or amendment
* This rule applies to ALL repositories, ALL projects, ALL commits
* Violations compromise the professional appearance of our work

## Why This Matters

* Maintains professional repository appearance
* Avoids unwanted third-party attribution
* Ensures our work is presented as our own
* Prevents confusion about authorship and ownership
* Compliance with company branding guidelines

## PR Requirements

Every PR must include:

* **Problem/Context:** What issue are we solving and why?
* **Solution summary:** How does this change address the problem?
* **Test plan:** Commands + results proving functionality
* **Risk/rollback:** Potential issues and how to revert if needed
* **Story link + Type + Estimate:** Link to issue/story with type (feature/bug/chore) and points

## Reference Files

See `references/ai-attribution-enforcement.md` for comprehensive forbidden text list and enforcement details.

See `references/pr-templates.md` for complete PR templates for feature, bug, and chore PRs.

See `references/branch-conventions.md` for branch naming patterns and examples.
