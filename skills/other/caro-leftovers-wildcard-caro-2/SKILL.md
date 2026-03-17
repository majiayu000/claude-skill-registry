---
name: caro-leftovers
description: "Document leftover tasks as GitHub issues with full correlation to branch, PR, and original work plan. Use when ending a session with incomplete work that another agent should pick up."
version: "1.0.0"
allowed-tools: "Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion"
license: "AGPL-3.0"
---

# Caro Leftovers Reporter

Create GitHub issues to document incomplete work, maintaining full traceability to the originating branch, PR, work plan, and user instructions. This enables asynchronous work continuation by other agents.

## When to Use

- Ending a session with incomplete tasks
- Work was blocked by external dependencies
- Scope expanded beyond current session
- Technical debt identified but not addressed
- Future enhancements discovered during implementation

## Workflow

### Phase 1: Context Collection

Gather all correlation data automatically:

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Get recent commits on this branch
git log --oneline -10

# Find associated PR (if any)
gh pr list --head "$BRANCH" --json number,title,url,body,milestone --jq '.[0]'

# Get repository info
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

Also check for existing context:
- Plan files in `thoughts/shared/plans/`
- Handoffs in `thoughts/shared/handoffs/`
- Todo lists from current session

### Phase 2: Leftover Identification

Ask the user what remains incomplete:

```
What work remains incomplete from this session?

Categories:
1. **Critical blockers** - Must fix before merge
2. **Technical debt** - Should address soon
3. **Future enhancements** - Out of current scope
```

For each item, collect:
- Brief description (becomes issue title)
- What was attempted/learned
- Suggested next steps
- Priority/severity

### Phase 3: Issue Generation

For each leftover item, **preview and confirm** before creating:

```
Preview Issue #1:
─────────────────
Title: [Leftover]: {description}
Labels: leftover, from-agent, {category}
Milestone: {auto-detected or ask}

Body:
{rendered issue body}
─────────────────

Create this issue? (yes/no)
```

**Milestone Logic:**
- If PR is linked to a milestone → suggest that milestone
- If branch name contains version (e.g., `v1.1.0-feature`) → suggest matching milestone
- Otherwise → ask user with available milestones as options

### Phase 4: Summary Report

After all issues created:

```
Leftover Issues Created
═══════════════════════

✓ #123 - [Leftover]: Add retry logic for API calls
  Labels: leftover, from-agent, technical-debt
  Milestone: v1.1.0

✓ #124 - [Leftover]: Document new config options
  Labels: leftover, from-agent, docs
  Milestone: v1.2.0

Correlation Context:
  Branch: feature/api-improvements
  PR: #99 - API Client Refactoring
  Plan: thoughts/shared/plans/api-refactor.md

Next Steps:
  1. Review issues for accuracy
  2. Assign to team member or leave for agent pickup
  3. Continue with /create_handoff if ending session
```

## GitHub Commands Reference

```bash
# Create leftover issue
gh issue create \
  --title "[Leftover]: ${title}" \
  --body-file /tmp/issue-body.md \
  --label "leftover,from-agent,${category}" \
  --milestone "${milestone}"

# List available milestones
gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.title) (\(.open_issues) open)"'

# Add comment to PR linking the issue
gh pr comment ${pr_number} --body "Created leftover issue: #${issue_number}"

# View issue after creation
gh issue view ${issue_number} --web
```

## Issue Template

Use the template in `templates/leftover-issue.md` for consistent formatting.

Key sections:
- **Context**: Branch, PR, plan references
- **Original Request**: What user asked for
- **What Was Planned**: Intended implementation
- **What Was Completed**: Actual progress made
- **What Remains**: The incomplete work
- **Suggested Next Steps**: Actionable guidance

## Integration Points

### With `/create_handoff`

After creating leftover issues, suggest:
```
Issues created. Run /create_handoff to create a full session handoff?
```

The handoff can reference the created issues in its "Next Steps" section.

### With `/caro.sync roadmap`

Leftovers assigned to milestones will appear in roadmap sync:
```
v1.1.0: 21 open issues (+2 from leftovers)
```

### With Plan Mode

Can extract incomplete items from plan files:
- Look for unchecked items: `- [ ]`
- Look for "TODO" or "Future" sections
- Look for items marked "out of scope"

## Best Practices

1. **Be specific**: Issue titles should be actionable
2. **Include context**: What was tried, what was learned
3. **Suggest next steps**: Give future agents a starting point
4. **Use appropriate labels**: Critical vs technical-debt vs enhancement
5. **Link to code**: Reference specific files/lines when relevant

## Example Session

```
User: /caro.leftovers

Claude: Collecting session context...

Branch: feature/safety-validation
PR: #145 - Add command safety validation
Milestone: v1.1.0

What work remains incomplete?

User: The pattern matching for destructive commands is done,
      but I didn't add tests for the edge cases with pipes.
      Also, the config file support was out of scope.

Claude: I'll create 2 leftover issues:

Issue 1: Test edge cases for pipe command validation
  Category: Technical debt (tests)
  Milestone: v1.1.0 (from PR)

[Preview shown]

Create this issue? yes

Issue 2: Add config file support for custom safety patterns
  Category: Future enhancement
  Milestone: v1.2.0 (suggested - not blocking v1.1.0)

[Preview shown]

Create this issue? yes

Created:
  ✓ #201 - [Leftover]: Test edge cases for pipe command validation
  ✓ #202 - [Leftover]: Add config file support for custom safety patterns

Run /create_handoff to document full session context?
```
