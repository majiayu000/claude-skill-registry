---
name: gh-issue-triage
description: Label taxonomy and triage workflow for GitHub issues. Defines type labels (bug/feature/enhancement/docs/chore), priority levels (critical/high/medium/low), status labels, and triage decision workflow. Use when categorizing and prioritizing issues.
---

# Issue Triage

Rules and workflows for categorizing, labeling, and prioritizing GitHub issues.

## Quick Reference

| Label Type | Purpose | Mutually Exclusive? |
|------------|---------|---------------------|
| Type | What kind of issue | Yes |
| Priority | How urgent | Yes |
| Status | Current state | Yes |
| Area | Which component | No |

## Label Taxonomy

### Type Labels (mutually exclusive)

| Label | Description | Color |
|-------|-------------|-------|
| `bug` | Something is broken | `#d73a4a` (red) |
| `feature` | New functionality | `#a2eeef` (cyan) |
| `enhancement` | Improvement to existing feature | `#84b6eb` (blue) |
| `docs` | Documentation only | `#0075ca` (dark blue) |
| `chore` | Maintenance, deps, infra | `#fef2c0` (yellow) |

### Priority Labels (mutually exclusive)

| Label | Description | Response |
|-------|-------------|----------|
| `priority: critical` | Drop everything, fix now | Immediate |
| `priority: high` | Next up after current work | This sprint |
| `priority: medium` | Normal backlog | Scheduled |
| `priority: low` | Nice to have, someday | Backlog |

### Status Labels (mutually exclusive)

| Label | Description |
|-------|-------------|
| `needs-triage` | New, not yet categorized |
| `needs-info` | Waiting for reporter clarification |
| `accepted` | Triaged and in backlog |
| `in-progress` | Someone is working on it |
| `blocked` | Can't proceed, waiting on something |

### Area Labels (project-specific, not exclusive)

Define based on your project structure:
- `area: api`
- `area: cli`
- `area: docs`
- `area: ui`
- `area: auth`

## Triage Workflow

### Step 1: New Issues

Every new issue gets `needs-triage` label automatically (via GitHub Actions or manually).

### Step 2: Initial Review

```
Is this a duplicate?
  YES → Close with "Duplicate of #N", link original
  NO  → Continue

Is this spam/invalid?
  YES → Close without label
  NO  → Continue

Is the issue clear enough to act on?
  YES → Continue to Step 3
  NO  → Add `needs-info`, comment asking for clarification
```

### Step 3: Categorization

```
Apply type label:
  - Broken functionality → `bug`
  - New capability → `feature`
  - Improve existing → `enhancement`
  - Documentation → `docs`
  - Maintenance → `chore`

Apply area label(s):
  - Based on affected component
  - Can have multiple areas
```

### Step 4: Prioritization

```
Apply priority:
  - Production down / security issue → `priority: critical`
  - Major impact, many users → `priority: high`
  - Normal request → `priority: medium`
  - Nice to have → `priority: low`
```

### Step 5: Finalize

```
1. Remove `needs-triage`
2. Add `accepted`
3. Assign to milestone (if applicable)
4. Suggest assignee (if known)
```

## Priority Guidelines

### Critical
- Production is down
- Security vulnerability
- Data loss occurring
- Blocks all users

### High
- Major feature broken
- Significant user impact
- Blocks important workflow
- Time-sensitive deadline

### Medium
- Normal bug reports
- Feature requests
- Improvements
- Most issues land here

### Low
- Minor cosmetic issues
- Edge case bugs
- Nice-to-have features
- "Someday" items

## Common Patterns

### Insufficient Information

```
Issue: "It doesn't work"
Action:
1. Add `needs-info`
2. Comment: "Can you provide steps to reproduce and your environment?"
3. Wait for response
```

### Duplicate Detection

```
Issue: Similar to existing #123
Action:
1. Close issue
2. Comment: "Duplicate of #123"
3. Add any new context to #123
```

### Critical Security Issue

```
Issue: Security vulnerability
Action:
1. Add `priority: critical`, `bug`
2. Assign immediately
3. Consider private discussion
```

### Feature Without Acceptance Criteria

```
Issue: "Add dark mode"
Action:
1. Add `feature`, `needs-info`
2. Comment: "Great idea! Can you describe acceptance criteria?"
```

## Reference Files

See `references/` for:
- `label-taxonomy.md` - Complete label reference with colors

## Integration with Other Components

### Typical Triage Workflow
1. Issue created using **gh-issue-templates** (gets `needs-triage` label)
2. Use **gh-issue-triage** (this skill) to determine type and priority
3. Apply labels using **gh-wrangler** agent
4. Track state changes using **gh-issue-lifecycle**

### Label Setup
Use `references/label-taxonomy.md` to:
- Create labels with correct colors: `gh label create "bug" --color "d73a4a"`
- Maintain consistent taxonomy across repositories
- Setup new repositories with standard labels

### Priority Assignment
Consult "Priority Guidelines" section in this skill:
- **Critical**: Production down, security, data loss
- **High**: Major features broken, significant impact
- **Medium**: Normal bugs and features (most issues)
- **Low**: Nice-to-have, cosmetic, edge cases

## Related

- Skill: `gh-issue-templates` - Creating well-formatted issues
- Skill: `gh-issue-lifecycle` - State transitions and linking
- Agent: `gh-wrangler` - Interactive triage workflow
