---
name: linear-sop
description: Linear ticket management best practices. Use when creating issues, updating status, or attaching evidence. Provides evidence templates for dev/staging/done phases.
---

# Linear SOP Skill

## Purpose

Guide consistent Linear ticket management. Provides evidence templates for the mandatory dev/staging/UAT evidence policy.

## When This Skill Applies

- Creating new Linear issues
- Updating ticket status
- Attaching evidence to tickets
- Parsing acceptance criteria
- Working with UUIDs and issue IDs

## Linear Operations (Manual Process)

Since Gemini CLI doesn't have native Linear integration, use the Linear web UI or CLI for these operations:

### Reading Issues

```bash
# Via Linear Web UI
# Navigate to: https://linear.app/team/{PROJECT_TEAM_NAME}/issue/{TICKET_PREFIX}-XXX

# Or use Linear CLI if installed
linear issue view {TICKET_PREFIX}-XXX
```

### Creating Issues

```bash
# Via Linear Web UI: Click "New Issue" or press C
# Or use Linear CLI:
linear issue create --title "feat(scope): description" --team {PROJECT_TEAM_NAME}
```

### Updating Issues

```bash
# Via Linear Web UI: Open issue and update status
# Or use Linear CLI:
linear issue update {TICKET_PREFIX}-XXX --state "Done"
```

### Adding Comments

```bash
# Via Linear Web UI: Open issue and add comment
# Or use Linear CLI:
linear issue comment {TICKET_PREFIX}-XXX "**Dev Evidence**\n\n..."
```

## Evidence Policy (MUST)

Every issue requires evidence at each phase:

| Phase       | Required? | Content                 |
| ----------- | --------- | ----------------------- |
| **Dev**     | MUST      | Implementation proof    |
| **Staging** | MUST      | UAT validation (or N/A) |
| **Done**    | MUST      | Final verification      |

## Evidence Templates

### Dev Evidence Template

```markdown
**Dev Evidence**

**PR**: https://github.com/{ORG_NAME}/{REPO_NAME}/pull/XXX
**Commit**: [short-hash]
**Branch**: {TICKET_PREFIX}-XXX-description

**Implementation:**

- [x] Feature implemented
- [x] Tests passing
- [x] Lint passing

**Verification:**

\`\`\`bash
yarn ci:validate

# Output: All checks passed

\`\`\`
```

### Staging/UAT Evidence Template

```markdown
**Staging Evidence**

**Environment**: Pop OS dev server
**URL**: http://pop-os:3000

**Validation Steps:**

1. Deployed to staging: [timestamp]
2. Smoke test passed: [yes/no]
3. Feature verified: [description]

**UAT Status:** [Passed/Pending/N/A]

If N/A, reason: [e.g., "Dev tooling only - no user-facing changes"]
```

### Done Evidence Template

```markdown
**Done Evidence**

**PR Merged**: https://github.com/{ORG_NAME}/{REPO_NAME}/pull/XXX
**Merge Commit**: [hash]

**Final Checklist:**

- [x] All acceptance criteria met
- [x] Documentation updated (if applicable)
- [x] No regressions detected
```

## Acceptance Criteria Parsing

When reading issue descriptions, extract ACs:

```markdown
## Acceptance Criteria

- [ ] User can perform action X
- [ ] System responds with Y
- [ ] Error handling for Z
```

Convert to testable checklist:

```typescript
const acceptanceCriteria = [
  { criterion: "User can perform action X", verified: false },
  { criterion: "System responds with Y", verified: false },
  { criterion: "Error handling for Z", verified: false },
];
```

## Status Workflow

```text
Backlog -> Ready -> In Progress -> Testing -> Ready for Review -> Done
```

### Status Update Guidelines

| From             | To               | When                     |
| ---------------- | ---------------- | ------------------------ |
| Backlog          | Ready            | Sprint planning          |
| Ready            | In Progress      | Work starts              |
| In Progress      | Testing          | PR created               |
| Testing          | Ready for Review | Tests pass, UAT complete |
| Ready for Review | Done             | POPM approval            |

## UUID Handling

Linear uses UUIDs internally. When working with APIs:

```typescript
// Issue identifiers (human-readable)
const issueId = "{TICKET_PREFIX}-459";

// UUIDs (API operations)
const uuid = "ef6a5fa0-2b46-417f-8266-dea2d187b10a";

// Get UUID from identifier via Linear web UI or API
// The issue URL contains the UUID
```

## Common Operations

### Link PR to Issue

PRs are automatically linked when:

- Branch name contains `{TICKET_PREFIX}-XXX`
- PR title contains `[{TICKET_PREFIX}-XXX]`

### Create Sub-Issue

Use Linear web UI: Click "Add sub-issue" on parent issue

### Query by Label

Use Linear web UI filters:
1. Open team view
2. Click "Filter"
3. Select label (e.g., "sprint-1")

## Reference

- **Agent Workflow SOP**: `docs/sop/AGENT_WORKFLOW_SOP.md`
- **Linear Documentation**: https://linear.app/docs
- **CONTRIBUTING.md**: Workflow documentation
