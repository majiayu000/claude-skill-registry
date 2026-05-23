---
name: review-claude-md-adherence
description: Verify code changes comply with CLAUDE.md instructions and project standards.
context: fork
---

Use the claude-md-adherence-reviewer agent to audit code for CLAUDE.md compliance: $ARGUMENTS

If no arguments provided, analyze the git diff between the current branch and main/master branch.
