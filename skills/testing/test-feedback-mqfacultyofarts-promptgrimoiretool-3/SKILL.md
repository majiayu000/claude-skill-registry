---
name: test-feedback
description: File structured GitHub issues for testing feedback on prototype releases. Use when testing a new prototype build and need to report bugs, usability issues, or feature requests. Guides through creating well-structured issue reports.
---

# Test Feedback Skill

Help testers create well-structured GitHub issues for prototype feedback.

## When to Use

- After testing a prototype release
- When encountering a bug or unexpected behavior
- When suggesting improvements or new features
- When reporting usability issues

## Issue Types

### Bug Report

```markdown
## Bug Report

**Prototype Version:** [version/commit/date of build tested]

**Environment:**
- Browser: [e.g., Chrome 120, Safari 17]
- OS: [e.g., macOS 14.2, Windows 11]
- Screen size: [e.g., 1920x1080, mobile]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Continue...]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happened]

**Screenshots/Recording:**
[Attach if applicable]

**Severity:**
- [ ] Critical - blocks core functionality
- [ ] Major - significant feature broken
- [ ] Minor - cosmetic or edge case
```

### Feature Request

```markdown
## Feature Request

**Related to:** [Brief context, e.g., "Case annotation workflow"]

**Problem Statement:**
[What problem does this solve? What's frustrating about current behavior?]

**Proposed Solution:**
[How should it work?]

**Alternatives Considered:**
[Other approaches, if any]

**Priority:**
- [ ] Must-have for MVP
- [ ] Nice-to-have
- [ ] Future consideration
```

### Usability Issue

```markdown
## Usability Issue

**Prototype Version:** [version/date]

**Task Attempted:**
[What were you trying to accomplish?]

**Difficulty Encountered:**
[What made it hard?]

**Suggested Improvement:**
[How could this be easier?]

**User Context:**
[Relevant experience level, e.g., "First time using the tool"]
```

## Process

1. **Identify the issue type** - Bug, feature request, or usability issue
2. **Gather context** - Version, environment, steps to reproduce
3. **Draft the issue** using the appropriate template above
4. **Add labels** - Use domain/phase labels (e.g., `domain:case-brief`, `phase:mvp`). Set issue type (Bug/Feature/Task) via GraphQL — see `manage-issues` skill
5. **Submit via gh CLI**

## Creating Issues

Use the GitHub CLI to create issues, then set the issue type via GraphQL (see `manage-issues` skill for full patterns):

```bash
# Bug report
gh issue create --title "Bug: [Brief description]" \
  --label "domain:case-brief,phase:mvp" \
  --body "$(cat <<'EOF'
[Issue body from template]
EOF
)"
# Then set type=Bug via GraphQL (see manage-issues skill)

# Feature request
gh issue create --title "Feature: [Brief description]" \
  --label "domain:case-brief" \
  --body "$(cat <<'EOF'
[Issue body from template]
EOF
)"
# Then set type=Feature via GraphQL (see manage-issues skill)
```

## Labels

See `manage-issues` skill for current label conventions. Key points:
- **No `bug` or `enhancement` labels** — use GitHub Issue Types (Bug/Feature/Task) instead
- Use domain labels: `domain:workspace-platform`, `domain:case-brief`, `domain:roleplay`, etc.
- Use phase labels: `phase:mvp`, `phase:post-mvp`

## Good Issue Titles

- Bug: "PDF highlights disappear after page navigation"
- Feature: "Add keyboard shortcuts for highlight tagging"
- UX: "Brief section order doesn't match reading workflow"

## Tips for Effective Feedback

1. **One issue per report** - Don't bundle multiple problems
2. **Be specific** - "Button doesn't work" → "Save button shows spinner but never completes"
3. **Include context** - What were you doing when this happened?
4. **Attach evidence** - Screenshots, screen recordings, console errors
5. **Suggest solutions** - If you have ideas, share them
