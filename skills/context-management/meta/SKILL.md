---
name: meta
description: Manage session context - focus, threads, questions, and observations. Use when tracking what you're working on, managing parallel work streams, or capturing friction points.
---

# Meta - Session Context Management

Manage session continuity through focus, threads, questions, and observations. These tools help maintain context across sessions and capture learnings.

## When to Use

- Starting work on a specific area (set focus)
- Tracking multiple parallel work streams (threads)
- Noting questions that need answers (questions)
- Capturing friction, successes, or ideas (observations)

## Focus Management

Focus tracks what you're currently working on. It appears in `session start` output.

### Setting Focus

When starting work on a specific area:

```bash
# Set focus to current work area
kspec meta focus "implementing JSON output for all commands"

# Focus now appears in session start
kspec session start
```

### Checking Focus

```bash
# View current focus
kspec meta focus
```

### Clearing Focus

When switching to different work or ending a session:

```bash
kspec meta focus --clear
```

## Thread Management

Threads track parallel work streams. Use when you're working on multiple things and need to context-switch.

### When to Use Threads

- Debugging while implementing a feature
- Waiting on external input for one task, working on another
- Exploring multiple approaches simultaneously

### Adding a Thread

```bash
# Add a new thread
kspec meta thread --add "investigating test failures"
kspec meta thread --add "refactoring output module"
```

### Listing Threads

```bash
kspec meta thread --list
```

### Removing a Thread

When done with a thread:

```bash
# Remove by index (0-based)
kspec meta thread --remove 0
```

## Question Tracking

Track open questions that need answers during the session.

### When to Use Questions

- Process questions: "Should we validate on read or write?"
- Scope questions: "Does this include the edge case?"
- Technical questions: "Is this the right approach?"

### Adding Questions

```bash
kspec meta question --add "Should validation happen at parse time or command execution?"
```

### Listing Questions

```bash
kspec meta question --list
```

### Removing Questions

When answered or no longer relevant:

```bash
kspec meta question --remove 0
```

## Observations Workflow

Observations capture systemic patterns - friction, successes, questions, and ideas. Unlike inbox items (future work), observations inform process improvement.

### Types of Observations

| Type | Purpose | Example |
|------|---------|---------|
| friction | Something harder than it should be | "Bulk updates require too many commands" |
| success | Pattern worth replicating | "Decision tree in triage skill worked well" |
| question | Systemic question | "When should agents use inbox vs tasks?" |
| idea | Improvement opportunity | "Could auto-generate AC from test names" |

### Creating Observations

```bash
# Friction point
kspec meta observe friction "No way to bulk-add acceptance criteria"

# Success pattern
kspec meta observe success "Using --dry-run before derive prevented duplicate tasks"

# Question about process
kspec meta observe question "When should agents enter plan mode vs just implement?"

# Idea for improvement
kspec meta observe idea "CLI could suggest next steps after task completion"
```

### Listing Observations

```bash
# All observations
kspec meta observations

# Only unresolved
kspec meta observations --pending-resolution

# With full details
kspec meta observations -v
```

### Promoting to Task

When an observation reveals actionable work:

```bash
kspec meta observations promote @ref --title "Add bulk AC command" --priority 2
```

### Resolving Observations

When addressed or no longer relevant:

```bash
# Single observation
kspec meta resolve @ref "Resolution notes"

# Batch resolve multiple observations
kspec meta resolve @ref1 @ref2 @ref3 "All addressed in PR #123"
```

## Where to Capture What

| What you have | Where to put it | Why |
|---------------|-----------------|-----|
| Vague idea for future | `inbox add` | Low-friction capture, triage later |
| Clear actionable work | `task add` | Ready to implement |
| Something was hard | `meta observe friction` | Informs process improvement |
| Something worked well | `meta observe success` | Worth replicating |
| Open question about work | `meta question --add` | Track during session |
| Systemic process question | `meta observe question` | Broader than current session |

**Rule of thumb:**
- **Inbox** = future work (becomes tasks eventually)
- **Questions** = session context (answer during work)
- **Observations** = systemic patterns (inform improvements)

## Session Patterns

### Starting a Focused Session

```bash
# 1. Get context
kspec session start

# 2. Set focus
kspec meta focus "working on documentation improvements"

# 3. Note any open questions from previous session
kspec meta question --add "Should skills duplicate AGENTS.md content?"
```

### Managing Context Switches

```bash
# 1. Add thread for new work
kspec meta thread --add "investigating test failure"

# 2. Do the investigation
# ...

# 3. Remove thread when done
kspec meta thread --remove 0
```

### Capturing Friction in the Moment

When you notice something is harder than it should be:

```bash
# Don't lose the thought - capture immediately
kspec meta observe friction "Had to run 5 commands to update one spec field"

# Continue with your work
# Review during /reflect
```

### End of Session

```bash
# Clear focus
kspec meta focus --clear

# Review and resolve any temporary questions
kspec meta question --list

# Observations persist for later triage
```

## Integration with Other Skills

- **`/triage`** - Processes observations alongside inbox items
- **`/reflect`** - Reviews what worked and what didn't, creates observations
- **`/kspec`** - Core task and spec workflows
- **`session start`** - Shows current focus, threads, questions
