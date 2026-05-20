---
name: track-implementation-progress
description: "Track implementation progress against plan. Use to monitor component delivery and identify blockers."
category: review
mcp_fallback: none
user-invocable: false
---

# Track Implementation Progress

Monitor completion of planned components and identify blockers.

## When to Use

- Regular progress tracking during implementation
- Identifying which components are complete
- Finding blockers preventing progress
- Reporting status to team
- Planning next sprints/phases
- Estimating project completion
- Deciding resource allocation

## Quick Reference

```bash
# List all GitHub issues
gh issue list --state all --limit 100

# Get issue status
gh issue view <issue-number>

# Check issue milestones
gh issue list --milestone <milestone-name>

# Filter by label
gh issue list --label "implementation"

# Get issue project status
gh api repos/OWNER/REPO/issues/<number> --jq '.state, .closed_at'
```

## Progress Tracking Workflow

1. **Collect data**: Get all issue statuses from GitHub
2. **Categorize issues**: By phase (plan, test, implementation, package, cleanup)
3. **Calculate metrics**: Completion rate by phase and component
4. **Identify blockers**: Issues in progress but not moving
5. **Analyze dependencies**: What's blocking other work
6. **Create report**: Summary of progress
7. **Identify next steps**: What should be worked on next

## Progress Metrics

**Completion Rate**:

- Total issues planned
- Total issues closed
- Percentage complete
- Velocity (issues/week or issues/sprint)

**By Phase**:

- Plan phase completion
- Test phase completion
- Implementation completion
- Package completion
- Cleanup completion

**By Component**:

- Foundation component progress
- Shared library progress
- Tooling progress
- First paper progress
- CI/CD progress

**Blockers**:

- Issues stuck in progress (not updated in N days)
- Issues blocked by dependencies
- Issues with no assigned owner
- Issues waiting for input

## Status Indicators

**Healthy Progress**:

- Issues closing regularly
- Velocity consistent
- Few blockers
- Dependencies clear
- Team engaged

**Warning Signs**:

- Issues stuck for weeks
- No recent updates
- Accumulating blockers
- Unclear dependencies
- Low engagement

## Output Format

Report progress with:

1. **Overall Status** - Percentage complete, velocity
2. **By Phase** - Completion status for each phase
3. **By Component** - Progress on each major area
4. **Completed This Period** - Recently closed issues
5. **In Progress** - Currently being worked on
6. **Blockers** - What's preventing progress
7. **Next Steps** - Recommended priorities

## Progress Report Template

```markdown
# Implementation Progress Report - [Date]

## Overall Status
- Completion: X% (Y of Z issues closed)
- Velocity: X issues/week
- Health: [Green/Yellow/Red]

## By Phase
- Plan: 100% (20/20)
- Test: 75% (15/20)
- Implementation: 50% (10/20)
- Package: 25% (5/20)
- Cleanup: 0% (0/20)

## Recent Activity
- Closed: issue #123, #124
- In Progress: issue #125, #126
- Blocked: issue #127 (waiting for #120)

## Blockers
1. Issue #127 - Blocked by #120 (PR in review)
2. Issue #128 - Unclear requirements

## Next Actions
1. Complete issue #120 review
2. Clarify requirements for #128
3. Start issue #129 (ready to go)
```

## Metrics to Track

**Velocity**:

- Issues closed per week
- Trend over time (improving/declining)
- Compare to planned velocity

**Burndown**:

- Total remaining issues
- Expected completion date
- Risk of missing deadlines

**Quality**:

- Number of reopened issues
- Time to close (average)
- Bugs found post-close

**Dependencies**:

- Blocked issues
- Critical path items
- Dependency chains

## Blocker Resolution

**Identify**:

- What's blocking progress
- When it got stuck
- Who can unblock it

**Escalate**:

- Inform team of blocker
- Request help if needed
- Update issue status

**Track**:

- Monitor blocker status
- Update resolution attempts
- Note resolution when complete

## Error Handling

| Problem | Solution |
|---------|----------|
| Can't access issues | Check gh auth status |
| Issues not updated | Filter for last updated date |
| Missing data | Check issue descriptions and labels |
| Unclear status | Ask issue owner for update |
| Too many issues | Filter by label or milestone |

## Tracking Best Practices

- Update issues regularly with progress comments
- Use consistent labels for status tracking
- Link issues to milestones for grouping
- Set issue assignees to clarify ownership
- Close issues when complete, reopen if needed
- Document blockers in issue comments
- Create sub-issues for complex tasks
- Use GitHub projects for visual board view

## References

- See CLAUDE.md for issue and project organization
- See plan-validate-structure for plan health
- See agent-coverage-check for agent completion
