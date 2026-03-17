---
name: pomodoro
description: Simple Pomodoro timer for focused work sessions with session tracking and productivity analytics. Use when users request focus timers, ask about productivity patterns, or want to track work sessions over time. Demonstrates the System Skill Pattern (CLI + SKILL.md + Database).
license: MIT
allowed-tools:
  - Bash
  - Read
---

# Pomodoro Timer Skill

## Overview

A 25-minute timer for focused work sessions that saves every session to SQLite. Enables history tracking, productivity analytics, and pattern recognition over time.

**This is a System Skill** - it provides handles to operate a personal data system. As commands run and sessions accumulate, context builds and compounds. The system learns patterns and provides increasingly valuable insights through an OODA loop of observation, orientation, decision, and action.

## Mental Model: The OODA Loop

Operating this skill involves running a continuous cycle:

1. **Observe** → Check current status (`./pomodoro status`) and review history (`./pomodoro history`)
2. **Orient** → Analyze patterns in the data (`./pomodoro stats --period week`)
3. **Decide** → Determine optimal actions (e.g., "Morning sessions have 95% completion - schedule deep work then")
4. **Act** → Start sessions (`./pomodoro start`), provide recommendations, celebrate milestones

Each cycle builds on accumulated data, making insights more valuable over time.

## Dependencies

- Binary location: `~/.claude/skills/pomodoro/pomodoro`
- Database: Auto-created at `~/.claude/skills/pomodoro/pomodoro.db` on first run
- No external dependencies required

## Quick Decision Tree

```
User task → What kind of request?
   ├─ Start focused work → Check status first, then start session
   ├─ Check current timer → Use status command
   ├─ Review productivity → Use stats command (day/week/month/year)
   ├─ View past sessions → Use history command
   └─ Stop early → Use stop command
```

## Core Commands

**To see all available options**: Run `./pomodoro --help` or `./pomodoro <command> --help`

### Starting a Session

Begin a Pomodoro session:

```bash
# Traditional 25-minute Pomodoro
./pomodoro start --task "Refactor authentication module"

# Custom durations and cycles
./pomodoro start --task "Quick review" --work 5 --break 3 --cycles 2
./pomodoro start --task "Deep focus" --work 50 --break 10 --cycles 1

# Flash cards (rapid cycles)
./pomodoro start --task "Flash cards" --work 2 --break 1 --cycles 5
```

**Options:**
- `--work <minutes>` - Work duration (default: 25)
- `--break <minutes>` - Break duration (default: 5)
- `--cycles <count>` - Number of work+break rounds (default: 1)

**Behavior:**
- Only one session can run at a time
- Timer runs in foreground showing progress every minute
- Breaks start automatically after work sessions
- Next work session starts automatically after break (if cycles remaining)
- Each work session saved separately to database

**JSON output example:**
```bash
./pomodoro start --task "Write docs" --json
# Returns: {"status": "started", "task": "Write docs", "duration": 25, "started_at": "2025-10-22T14:30:00Z"}
```

### Checking Status

See if a timer is running:

```bash
./pomodoro status
./pomodoro status --json  # For programmatic use
```

**Output example:**
```
Active session: "Write documentation"
Started: 2:30 PM
Time remaining: 18 minutes
```

### Viewing History

Review past sessions:

```bash
./pomodoro history --days 7    # Last 7 days
./pomodoro history --days 30   # Last 30 days
./pomodoro history --json      # For programmatic use
```

**Output includes:**
- Task names
- Start and completion times
- Duration
- Completion status (completed vs. stopped early)

### Analyzing Productivity

Get insights from accumulated data:

```bash
./pomodoro stats --period day     # Today's stats
./pomodoro stats --period week    # This week
./pomodoro stats --period month   # This month
./pomodoro stats --period year    # This year
./pomodoro stats --json           # For programmatic use
```

**Statistics include:**
- Total and completed sessions
- Completion rate (% of sessions finished)
- Total focus time
- Most productive hours of day
- Task distribution (which tasks completed most often)

**JSON output example:**
```json
{
  "period": "week",
  "total_sessions": 23,
  "completed": 19,
  "completion_rate": 0.826,
  "focus_hours": 7.9,
  "productive_hours": [9, 10, 11],
  "top_tasks": ["Refactoring", "Documentation", "Code review"]
}
```

### Stopping Early

End the current session before completion:

```bash
./pomodoro stop
```

Use when interruptions occur or task completes early. Session marked as incomplete in database.

## Essential Workflows

### Starting Focused Work

To help a user start a Pomodoro session:

1. **Check for active session**: `./pomodoro status`
2. **If clear, start with appropriate options**:
   - Traditional: `./pomodoro start --task "Deep work on authentication"`
   - Custom: `./pomodoro start --task "Sprint planning" --work 15 --break 5 --cycles 3`
   - Flash cards: `./pomodoro start --task "Vocabulary review" --work 2 --break 1 --cycles 10`
3. **Confirm to user**: "25-minute Pomodoro started for [task name]. Timer running."

### Daily Review

To provide daily productivity summary:

1. **Fetch today's data**: `./pomodoro stats --period day --json`
2. **Parse and present insights**:
   - "Completed 6 Pomodoros today (3.0 hours of focus time)"
   - "5/6 sessions completed - 83% completion rate"
   - "Most work on: Refactoring, Documentation"
   - "Productive hours: 9-11 AM"

### Weekly Analysis

To provide weekly productivity review:

1. **Fetch week's data**: `./pomodoro stats --period week --json`
2. **Identify patterns**:
   - Compare to previous weeks if data available
   - Note peak productive hours
   - Identify which task types have highest completion rates
3. **Make recommendations**:
   - "Schedule deep work during your peak hours (9-11 AM)"
   - "Coding sessions have 90% completion vs 70% for meetings - consider task segmentation"

### Pattern Recognition Over Time

As sessions accumulate, provide increasingly valuable insights:

**After a few sessions (1-5):**
- "Completed 3 Pomodoros today"
- "Building momentum with focus sessions"

**After several days (5-20 sessions):**
- "7 completed out of 9 sessions - 78% completion rate"
- "Most productive between 9-11 AM"

**After a week (20-50 sessions):**
- "Strong week: 23 sessions with 85% completion"
- "Peak productivity: 9-11 AM (95% completion) vs 2-4 PM (65% completion)"
- "Consider scheduling deep work in morning hours"

**After a month (50+ sessions):**
- "Coding tasks: 90% completion rate"
- "Documentation tasks: 70% completion rate"
- "Consider shorter Pomodoros (15 min) for documentation work"

**After several months (100+ sessions):**
- "Completion rate improving: 72% → 85% over last 3 months"
- "Wednesday is most productive day (92% completion)"
- "Afternoon sessions improve when limited to 15 minutes"
- "80% more sessions completed on coding vs documentation tasks"

**Commands to use for pattern recognition:**
```bash
./pomodoro stats --period month --json  # Get monthly data
./pomodoro history --days 90 --json     # Review last 90 days
```

### Milestone Celebrations

Acknowledge progress at key milestones:

- **10 sessions**: "First 10 Pomodoros complete - building the habit!"
- **50 sessions**: "50 sessions milestone - over 20 hours of focused work!"
- **100 sessions**: "100 Pomodoros! That's 40+ hours of deep focus time."
- **High completion rates**: "95% completion this week - excellent focus!"

To check milestone status: `./pomodoro stats --period year --json`

## Common Pitfalls

### Starting When Session Already Active

❌ **Don't** start a new session without checking status first
✅ **Do** run `./pomodoro status` before starting

**Why**: Only one session can run at a time. Starting when active causes error.

**Pattern to follow**:
```bash
# Check first
./pomodoro status
# If "No active session", then start
./pomodoro start --task "New task"
```

### Non-Descriptive Task Names

❌ **Don't** use vague names: "Work", "Stuff", "Things"
✅ **Do** use specific names: "Refactor auth module", "Write API docs", "Review PR #123"

**Why**: Descriptive names enable better analytics. Pattern recognition needs specificity to identify which task types work best.

### Interrupting Long-Running Sessions

❌ **Don't** let terminal close or process be killed during session
✅ **Do** use `./pomodoro stop` if interruption is necessary

**Why**: Interrupted sessions aren't saved to database. Use stop command to record partial session.

### Ignoring Completion Rate Signals

❌ **Don't** ignore consistent low completion rates for certain task types
✅ **Do** adjust session length based on task type patterns

**Why**: If documentation tasks show 60% completion vs 90% for coding, shorter sessions (15 min) may work better for documentation.

**How to identify**:
```bash
./pomodoro stats --period month --json
# Review completion rates by task type
# Suggest duration adjustments based on patterns
```

## Best Practices

### Session Management

- Use descriptive task names for better analytics
- Complete full 25 minutes when possible
- Take breaks between sessions
- Adjust duration based on task type (use `--work` flag)
- Stop explicitly if interrupted (don't let process be killed)

### User Interaction

- Celebrate milestones (10, 50, 100, 250, 500 sessions)
- Acknowledge completion rates: "Excellent focus - 90% this week!"
- Suggest optimal times based on historical data
- Encourage consistent practice
- Point out improvements: "Completion rate up from 75% to 85%"

### Data Analysis

- Review daily stats at end of each day
- Check weekly patterns for scheduling insights
- Track trends over time (month, year)
- Use JSON output for custom analytics
- Cross-reference task types with completion rates
- Identify peak productive hours

### Command Composition

Combine commands for deeper insights:

```bash
# Morning check-in: status + daily stats
./pomodoro status
./pomodoro stats --period day

# Weekly review: history + stats
./pomodoro history --days 7 --json
./pomodoro stats --period week --json

# Long-term analysis: monthly trends
./pomodoro stats --period month --json
./pomodoro history --days 90 --json
```

## Technical Notes

### JSON Output

All commands support `--json` flag for programmatic access:

```bash
./pomodoro status --json
./pomodoro history --json
./pomodoro stats --json
```

Use JSON output when:
- Parsing data programmatically
- Building custom analytics
- Feeding into other tools
- Need structured output

### Database

- **Location**: `~/.claude/skills/pomodoro/pomodoro.db`
- **Format**: SQLite database with single `sessions` table
- **Persistence**: All sessions saved permanently
- **Growth**: Database grows with use (each session ~100 bytes)
- **Analytics**: Richer insights as data accumulates
- **Maintenance**: No cleanup or archiving needed

**Schema**:
```sql
CREATE TABLE sessions (
  id INTEGER PRIMARY KEY,
  task TEXT NOT NULL,
  duration INTEGER NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT
);
```

### Timer Behavior

- Runs in foreground process (blocks terminal)
- Shows progress every minute during work sessions
- Shows progress every minute during break sessions
- Automatically transitions from work → break → work
- Each work session saved separately to database
- Supports custom durations via flags

**Example session flow** (3 cycles):
```
Work 25min → Break 5min → Work 25min → Break 5min → Work 25min → Break 5min → Done
```

Result: 3 separate database entries (one per work session)

### Binary Location

- **Path**: `~/.claude/skills/pomodoro/pomodoro`
- **Always use**: `./pomodoro` when running from skill directory
- **Full path**: `~/.claude/skills/pomodoro/pomodoro` from anywhere

**To run from skill directory**:
```bash
cd ~/.claude/skills/pomodoro
./pomodoro start --task "Task name"
```

## The System Skill Pattern in Action

This skill demonstrates the **System Skill Pattern** (CLI + SKILL.md + Database):

1. **CLI Binary**: Handles to operate the system - start sessions, query history, analyze patterns
2. **SKILL.md**: Operating procedure for the OODA loop (Observe → Orient → Decide → Act)
3. **SQLite Database**: Persistent memory where every session adds context

**The key insight**: With these three components, the skill animates a system rather than just responding to requests. Each interaction builds on the last. Analytics become richer. Insights get sharper. The tool compounds in value.

**Example of compounding value**:
- Week 1: "Started 5 sessions"
- Week 4: "Morning sessions: 95% completion. Afternoon: 70%. Schedule deep work mornings."
- Month 3: "Coding: 90% completion. Docs: 72%. Try 15-minute sessions for documentation."

This pattern works for any skill where accumulating data adds value and where giving Claude handles to operate a system creates more utility than one-time responses.

**See also**: README.md for deeper technical details and implementation guide.
