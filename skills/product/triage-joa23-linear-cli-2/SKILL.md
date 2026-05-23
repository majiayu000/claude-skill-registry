---
name: triage
description: Triage and prioritize Linear backlog. Analyzes issues for staleness, blockers, and suggests priorities based on dependencies and capacity.
---

# Triage Skill - Backlog Analysis

You are an expert at analyzing and prioritizing software backlogs.

## When to Use

Use this skill when:
- The backlog needs cleanup
- Prioritization decisions need to be made
- Looking for stale or blocked issues

## Process

### CRITICAL: Setup First
**Ensure team context is set:**
```bash
linear init  # If .linear.yaml doesn't exist
```

1. **Fetch the Backlog**
   ```bash
   # Get all backlog issues (returns ALL issues, not just assigned)
   linear issues list --state Backlog --format full --limit 100
   ```

2. **Analyze Dependencies**
   ```bash
   linear deps --team ENG
   ```

3. **Filter by Priority**
   ```bash
   # High priority backlog items
   linear issues list --state Backlog --priority 1 --format full

   # Urgent only (P1)
   linear issues list --state Backlog --priority 1 --format full

   # Customer issues
   linear issues list --labels customer --format full

   # Bugs in backlog
   linear issues list --state Backlog --labels bug --format full
   ```

4. **Identify Issues**
   Look for:
   - **Stale issues**: No updates in 30+ days
   - **Blocked issues**: Dependencies not resolved
   - **Priority mismatches**: High priority but blocked
   - **Orphaned issues**: No assignee, no activity

5. **Generate Recommendations**

## Analysis Framework

### Staleness Check
- Last updated > 30 days ago = Stale
- Last updated > 60 days ago = Very stale (consider closing)
- No activity + no assignee = Orphaned

### Dependency Health
- Blocked by completed issues = Unblock
- Circular dependencies = Flag for resolution
- Long blocking chains = Risk

### Priority Assessment
- P1/P2 but blocked = Escalate blocker
- P3/P4 with no activity = Consider closing
- No priority set = Needs triage

## Output Format

```
BACKLOG TRIAGE: Team ENG
════════════════════════════════════════

URGENT ATTENTION (3)
────────────────────────────────────────
ENG-101 [Stale 45d] Login bug - P1 but no activity
ENG-102 [Blocked] Payment flow - blocked by ENG-99
ENG-103 [Orphaned] API refactor - no owner

RECOMMENDED ACTIONS
────────────────────────────────────────
1. Unblock ENG-102: Complete ENG-99 or remove dependency
2. Assign ENG-103: Needs owner or close if abandoned
3. Update ENG-101: Stale P1 needs attention

HEALTH SUMMARY
────────────────────────────────────────
Total issues: 45
Blocked: 8 (17%)
Stale: 12 (26%)
Healthy: 25 (55%)
```

## Commands Used

```bash
# FIRST: Ensure team context is set
linear init  # If .linear.yaml doesn't exist

# Get backlog issues (returns ALL issues, not just assigned)
linear issues list --state Backlog --format full --limit 100

# Filter by priority
linear issues list --state Backlog --priority 1 --format full  # Urgent
linear issues list --state Backlog --priority 2 --format full  # High

# Filter by labels
linear issues list --labels customer --format full
linear issues list --labels bug --format full
linear issues list --state Backlog --labels "customer,bug" --format full

# Combine filters
linear issues list --state Backlog --priority 1 --labels customer --format full

# Check dependencies
linear deps --team ENG

# Update priority
linear issues update ENG-123 --priority 2

# Add a comment about triage
linear issues comment ENG-123 --body "Triaged: Needs unblocking before sprint"
```

## Key Learnings

- **`linear issues list` returns ALL issues** (not just assigned to you)
- Use `--format full` for structured output
- Combine filters: `--state Backlog --labels customer`
- Priority values: 0=none, 1=urgent, 2=high, 3=normal, 4=low

## Best Practices

1. **Regular cadence** - Triage weekly or bi-weekly
2. **Be decisive** - Close issues that won't be done
3. **Document reasoning** - Add comments explaining priority changes
4. **Involve stakeholders** - Flag issues needing product input
