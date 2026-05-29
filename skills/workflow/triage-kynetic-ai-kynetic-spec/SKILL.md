---
name: triage
description: Triage inbox items systematically. Analyzes items against spec/tasks, categorizes them, and processes using spec-first approach with plan mode for larger features.
---

# Triage

Systematically process items: inbox, observations, or automation eligibility.

## Focus Modes

Use `/triage <mode>` to focus on a specific area:

| Mode | Purpose | Documentation |
|------|---------|---------------|
| `inbox` | Process inbox items → specs/tasks | [docs/inbox.md](docs/inbox.md) |
| `observations` | Process pending observations | [docs/observations.md](docs/observations.md) |
| `automation` | Assess task automation eligibility | [docs/automation.md](docs/automation.md) |

Without a mode, follow the full triage session pattern below.

## Full Session Pattern

1. **Get context**
   ```bash
   kspec session start --full
   kspec inbox list
   kspec meta observations --pending-resolution
   kspec tasks assess automation
   ```

2. **Present overview to user**
   - Inbox items by category
   - Pending observations by type
   - Unassessed tasks needing triage

3. **Ask which focus area**
   - Inbox items
   - Observations
   - Automation eligibility

4. **Process that focus area**
   - Use the relevant sub-document for guidance

5. **Repeat or stop** when user indicates

## Quick Start by Mode

### `/triage inbox`

Process inbox items using spec-first approach. See [docs/inbox.md](docs/inbox.md).

```bash
kspec inbox list
# For each item: delete, promote, or create spec first
kspec inbox delete @ref --force
kspec inbox promote @ref --title "..." --spec-ref @spec
```

### `/triage observations`

Process pending observations. See [docs/observations.md](docs/observations.md).

```bash
kspec meta observations --pending-resolution
# For each: resolve, promote to task, or leave
kspec meta resolve @ref "Resolution notes"
kspec meta resolve @ref1 @ref2 "Batch resolution"
kspec meta observations promote @ref --title "..."
```

### `/triage automation`

Assess task automation eligibility. See [docs/automation.md](docs/automation.md).

```bash
kspec tasks assess automation
# Review criteria, fix issues, or mark status
kspec task set @ref --automation eligible
kspec task set @ref --automation needs_review --reason "..."
```

## Key Principles

- **Ask one question at a time** - Don't batch decisions
- **Spec before task** - Fill spec gaps before creating tasks
- **AC is required** - Specs without acceptance criteria are incomplete
- **Use CLI, not YAML** - All changes through kspec commands
- **Delete freely** - Outdated items should go

## Progress Tracking

Use TodoWrite to track progress during triage:
- Create todos for items being processed
- Mark completed as you go (don't batch)

At session end, provide summary:
- Items processed (deleted, promoted, spec'd)
- Tasks created/updated
- Observations resolved
- Remaining items
