---
name: review-workflow-design
description: Design spec-based review workflows with visual proof and issue classification. Use when setting up review processes, validating against specifications, or implementing screenshot-based visual validation.
allowed-tools: Read, Grep
---

# Review Workflow Design Skill

Design review workflows that validate implementation against specifications with visual proof.

## When to Use

- Setting up review processes for features
- Creating proof-of-value workflows
- Designing spec-based validation
- Implementing auto-resolution loops

## Core Concept

Review answers: **"Is what we built what we asked for?"**

This is different from testing which answers: "Does it work?"

## Design Workflow

### Step 1: Define Spec Location Pattern

Establish where specifications live:

```text
specs/
├── feature-{name}.md
├── bug-{name}.md
└── chore-{name}.md
```

Or:

```text
specs/issue-{number}-{type}.md
```

### Step 2: Design Screenshot Capture Points

Identify critical paths that need visual proof:

1. **Initial State**: Before any interaction
2. **Key Actions**: After significant user actions
3. **Final State**: End result of the feature

Example:

```text
1. Take screenshot of dashboard (initial state)
2. Click "Export" button
3. Take screenshot of export modal
4. Complete export
5. Take screenshot of success message
```

### Step 3: Define Severity Classification

Configure issue severity levels:

| Severity | Criteria | Action |
| --- | --- | --- |
| **blocker** | Prevents release, harms UX | Auto-resolve |
| **tech_debt** | Quality issue, works | Document |
| **skippable** | Polish, preference | Ignore |

### Step 4: Set Up Resolution Workflow

Design the auto-resolution loop:

```text
Review
  ├── Issues found?
  │     ├── Blockers? → /patch → /implement → Re-review
  │     └── No blockers → Success
  └── No issues → Success

Maximum 3 retry attempts
```

### Step 5: Configure Proof Storage

Options for screenshot storage:

- **Local**: `agents/{adw_id}/review_img/`
- **Cloud**: R2, S3, or similar (public URLs)
- **Git**: Committed with review artifacts

## Review Command Structure

```markdown
# Review Implementation Against Spec

## Variables
spec_file: $1

## Instructions

1. **Read Specification**
   - Understand requirements
   - Note success criteria

2. **Analyze Changes**
   - git diff origin/main
   - Compare against spec

3. **Capture Screenshots**
   - 1-5 screenshots of critical functionality
   - Number: 01_name.png, 02_name.png

4. **Classify Issues**
   - blocker: Must fix before release
   - tech_debt: Document for later
   - skippable: Can ignore

## Output Format

{
  "success": boolean,
  "review_summary": "string",
  "review_issues": [...]
}
```

## Issue Structure

```json
{
  "issue_description": "What's wrong",
  "issue_resolution": "How to fix it",
  "issue_severity": "blocker| tech_debt |skippable"
}
```

## Resolution Loop Pattern

```text
for attempt in range(1, MAX_ATTEMPTS + 1):
    review_result = run_review()

    if review_result.success:
        break  # No blockers

    blockers = filter(issues, severity="blocker")

    for blocker in blockers:
        create_patch(blocker)
        implement_patch()

    # Loop continues with re-review
```

## Integration with SDLC

```text
/plan    → What are we building?
/build   → Make it real
/test    → Does it work?
/review  → Is it what we asked for? ← THIS SKILL
/patch   → Fix blockers
/document → How does it work?
```

## Best Practices

1. **Screenshots are proof**: They show stakeholders what was delivered
2. **Specs are truth**: Review against spec, not assumptions
3. **Severity matters**: Only blockers need immediate resolution
4. **Retry limits**: Prevent infinite loops (3 attempts typical)
5. **Document tech debt**: Don't lose the information

## Memory References

- @review-vs-test.md - The distinction this skill implements
- @issue-severity-classification.md - How to classify issues
- @one-agent-one-purpose.md - Review as a focused purpose

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
