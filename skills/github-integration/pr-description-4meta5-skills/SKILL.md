---
name: pr-description
description: Generate professional pull request descriptions from git diff with summary, changes, security impact, and testing notes
category: development
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Pull Request Description Generator

Create the most complete and professional Git merge/pull request description, following established best practices.

## Procedure

### Phase 1 - Fetch and Analyze Changes
1. Get all changes in this branch compared to the default branch since it diverged
2. Detect modified files and classify them (e.g., source code, configuration, documentation, tests)
3. Identify major functional areas affected (e.g., ui, auth, api, contracts, security)
4. Detect breaking changes, dependency updates, and any migration requirements
5. Summarize the purpose, major changes, affected components, and any security, dependency, or testing implications

### Phase 2 - Generate Merge Request Description

Generate a detailed and professional description in Markdown format:

```markdown
## Summary
Short high level overview of the purpose.

## Description
Detailed descriptions of all the changes made, their scope, impact and effects.

## Motivation / Context
Why the change is required, including the issue reference if applicable.

## Changes
- [ ] List of major code or feature changes.
- [ ] Highlight of configuration, deployment, or dependency updates.

## Affected Functions
- List `functions` that were added/modified/deleted with brief description

## Security Impact
[icon] Brief summary of security impact
- [ ] List any security-sensitive modifications if any and mitigation strategy if addressed.

## Testing
- [ ] List or summarize test coverage and new test cases.
- [ ] Include steps for manual verification.

## Backward Compatibility
- [icon] Note if any breaking changes exist.
- [icon] Provide migration instructions if needed.
```

### Phase 3 - Refinement
6. Use consistent tense and technical clarity
7. Enforce line length under 100 characters where possible
8. Remove redundant or trivial commit noise (e.g., "fix typo")
9. Cross-reference related issues or tickets automatically (Fixes #1234)

## Constraints
- Analyze only within the given code. Do not invent missing context or external APIs
