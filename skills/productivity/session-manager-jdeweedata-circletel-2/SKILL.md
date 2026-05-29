---
name: session-manager
description: Manage named Claude Code sessions for CircleTel workflows. Use when starting feature work, resuming previous sessions, organizing multi-day tasks, or switching between different work contexts like admin, dashboard, or payment features.
---

# Session Manager

Skill for managing named Claude Code sessions in CircleTel development.

## When to Use

This skill activates when you:
- Start a new feature or bug fix
- Need to resume previous work
- Switch between different project areas
- Want to organize long-running tasks

**Keywords**: session, resume, rename, continue, context, switch task, pick up, where I left off

## Quick Commands

| Command | Description |
|---------|-------------|
| `/rename <name>` | Name current session |
| `/resume <name>` | Resume a named session |
| `/resume` | Show session picker (P=preview, R=rename) |
| `claude --resume <name>` | Resume from terminal |
| `claude --continue` | Continue most recent session |

## Session Naming Conventions

### By Feature Area
```
dashboard-billing-history
admin-orders-export
payment-netcash-emandate
coverage-mtn-integration
partner-compliance-upload
```

### By Issue/Ticket
```
BUG-1234-infinite-loading
FEAT-567-customer-services
HOTFIX-payment-timeout
```

### By Sprint/Week
```
sprint-23-kyc-flow
week-49-partner-portal
```

## CircleTel Session Templates

| Project Area | Session Name Pattern | Example |
|--------------|---------------------|---------|
| Customer Dashboard | `dashboard-{feature}` | `dashboard-billing-history` |
| Admin Portal | `admin-{feature}` | `admin-orders-export` |
| Payment System | `payment-{provider}-{feature}` | `payment-netcash-emandate` |
| B2B KYC | `b2b-kyc-{stage}` | `b2b-kyc-didit-integration` |
| Coverage API | `coverage-{provider}` | `coverage-mtn-wms` |
| Partner Portal | `partner-{feature}` | `partner-compliance-upload` |

## Workflow Patterns

### Pattern 1: Feature Branch Workflow
```bash
# 1. Create git branch
git checkout -b feature/customer-billing

# 2. Start Claude with named session
claude
# Then type: /rename customer-billing

# 3. Work on feature...

# 4. Next day, resume
claude --resume customer-billing
```

### Pattern 2: Context Switching
```bash
# Working on billing, need to fix urgent bug
# First, save current context
/rename billing-paused

# Start new session for bug
claude
/rename HOTFIX-auth-timeout

# Fix bug, commit, then resume billing
claude --resume billing-paused
```

### Pattern 3: Multi-Day Implementation
```
Day 1: /rename b2b-kyc-sprint
       - Complete database schema
       - Start API routes

Day 2: claude --resume b2b-kyc-sprint
       - Continue API routes
       - Add frontend components

Day 3: claude --resume b2b-kyc-sprint
       - Testing and validation
       - Documentation
```

### Pattern 4: Parallel Feature Development
```bash
# Terminal 1: Main feature
claude --resume dashboard-billing

# Terminal 2: Quick hotfix
claude --resume HOTFIX-auth-fix

# Switch between as needed
```

## Session Picker Shortcuts

When you run `/resume` without a name:

| Key | Action |
|-----|--------|
| `P` | Preview session content |
| `R` | Rename session |
| `Enter` | Select and resume |
| `Esc` | Cancel |
| `j/k` | Navigate up/down |

## Integration with Git Branches

Match session names to git branches for easy tracking:

```bash
# Create branch
git checkout -b feature/customer-dashboard

# Name session same as branch
/rename feature-customer-dashboard

# Later, find session by branch name
claude --resume feature-customer-dashboard
```

## Integration with Context Manager

When resuming long sessions, check context budget:

```bash
# After resuming
claude --resume my-feature

# Run context analysis
powershell -File .claude/skills/context-manager/run-context-analyzer.ps1
```

## Best Practices

1. **Name sessions immediately** - Run `/rename` at start of work
2. **Use descriptive names** - Future you will thank present you
3. **Match git branches** - Same name for branch and session
4. **Document context** - First message should summarize the goal
5. **Clean up old sessions** - Delete completed work sessions
6. **Use prefixes for priority**:
   - `URGENT-` for critical issues
   - `HOTFIX-` for production bugs
   - `FEAT-` for new features
   - `CHORE-` for maintenance

## Troubleshooting

### Can't find session by name
```bash
# List all sessions
/resume
# Use search to filter
```

### Session context seems lost
```bash
# Check context usage
/context

# If near limit, may need new session
# Reference old session in new one:
"I was working on feature X in session 'old-session'. Continuing..."
```

### Multiple sessions with similar names
```bash
# Use more specific names
# Bad: dashboard, dashboard-2
# Good: dashboard-billing-v1, dashboard-usage-charts
```

---

**Version**: 1.0.0
**Last Updated**: 2025-12-10
**For**: Claude Code v2.0.64+
