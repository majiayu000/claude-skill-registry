---
name: user-experience
description: Consistent user communication patterns for confidence, clarity, and engagement. Reference for all command output.
---

# User Experience Skill
// Project Autopilot - User Experience Framework
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Goal:** Give users confidence that everything is working correctly, keep them engaged with clear status updates, and provide actionable information at every step.

---

## Core Principles

1. **Confidence First** - Show validation/checks passing to build trust
2. **Progress Visibility** - Always show where we are and what's next
3. **Actionable Output** - Every message should be useful
4. **Consistent Patterns** - Same structure everywhere
5. **No Surprises** - Warn before, confirm after

---

## Standard Output Structure

### Command Start Banner

Every command should start with a clear header. Use simple formatting without box characters to avoid alignment issues:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 AUTOPILOT: [COMMAND NAME]
   [Brief description of what this command does]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 AUTOPILOT: BUILD
   Execute project plan with wave-based parallelization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Startup Checks

Show system validation to build confidence:

```
▶ Startup Checks
  ✓ Project structure valid
  ✓ Phase ordering verified (6 phases, 3 waves)
  ✓ Dependencies resolved (no cycles)
  ✓ Global config loaded
  ✓ Budget available ($45.50 remaining)

Ready to proceed.
```

**On failure:**
```
▶ Startup Checks
  ✓ Project structure valid
  ✗ Phase ordering invalid
    └─ Error: Phase 3 depends on Phase 5 (forward dependency)

⚠ Cannot proceed. Run /autopilot:validate --fix to repair.
```

### Progress Sections

Use consistent section headers:

```
─────────────────────────────────────────────────────────────
📋 PHASE 1 OF 6: Project Setup
─────────────────────────────────────────────────────────────
```

### Task Progress

Show real-time task updates:

```
  ┌─ Task 1.1: Initialize project structure
  │  🔄 Creating package.json...
  │  🔄 Setting up TypeScript config...
  │  ✓ Completed in 12s | $0.04
  └────────────────────────────────────────

  ┌─ Task 1.2: Configure ESLint and Prettier
  │  🔄 Installing dependencies...
  │  ✓ Completed in 8s | $0.02
  └────────────────────────────────────────
```

### Phase Summary

After each phase:

```
─────────────────────────────────────────────────────────────
✅ PHASE 1 COMPLETE
─────────────────────────────────────────────────────────────

  Tasks:     3/3 completed
  Duration:  1m 24s
  Cost:      $0.08 (estimate: $0.10, -20% under 🟢)

  Quality Gate:
    ✓ Build passes
    ✓ Lint clean (0 errors)
    ✓ Tests pass (12/12)

  📌 Checkpoint saved

─────────────────────────────────────────────────────────────
```

### Cost Dashboard

Show running cost status:

```
─────────────────────────────────────────────────────────────
💰 BUDGET STATUS
─────────────────────────────────────────────────────────────

  Progress: ████████░░░░░░░░░░░░░░░░░░░░░░ 27%

  Spent:     $2.35 of $50.00
  Remaining: $47.65
  Estimate:  $8.50 total (17% of budget)

  ✅ On track - well within budget

─────────────────────────────────────────────────────────────
```

### Completion Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 BUILD COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Project:   my-awesome-app
  Duration:  45m 12s
  Cost:      $4.85 (estimate: $6.00, -19% under budget 🟢)

─────────────────────────────────────────────────────────────

📊 Summary

  Phases completed:  6/6 ✅
  Tasks completed:   24/24 ✅
  Tests passing:     156/156 ✅
  Coverage:          87%
  Git commits:       12

─────────────────────────────────────────────────────────────

📈 Accuracy

  Your estimates were 19% conservative (you saved $1.15)
  Historical accuracy: 94% (improving!)

─────────────────────────────────────────────────────────────

🔗 Next Steps

  • Run your app:     npm run dev
  • View history:     /autopilot:altitude --global
  • Start new task:   /autopilot:takeoff "next feature"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Status Indicators

### Progress Bar

```
# Full width (30 chars)
Progress: ████████████████████████████░░ 93%

# With label
Phases:   ██████████░░░░░░░░░░░░░░░░░░░░ 33% (2/6)
Budget:   ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 14% ($2.35/$50)
```

### Check Lists

```
# Passing checks
  ✓ Build passes
  ✓ Tests pass (47/47)
  ✓ Coverage 87% (≥80%)
  ✓ Lint clean

# Mixed results
  ✓ Build passes
  ✗ Tests fail (45/47)
  ⚠ Coverage 78% (target: 80%)
  ✓ Lint clean
```

### Status Badges

```
# Inline status
[PASS] All checks complete
[FAIL] 2 tests failing
[WARN] Coverage below target
[INFO] Using cached data
[SKIP] Already completed
```

---

## Engagement Patterns

### Keep Users Informed

**During long operations:**
```
  🔄 Building project... (this may take 30-60 seconds)
     Completed: 3/8 tasks
     Current:   Setting up database schema
     Next:      Creating API routes
```

**Estimated time remaining:**
```
  ⏱ Estimated time remaining: ~3 minutes
     Based on: 4 tasks × ~45s average
```

### Celebrate Wins

**After successful validation:**
```
  ✅ All 6 phases validated successfully!
     • No circular dependencies
     • Wave ordering correct
     • All prerequisites satisfied
```

**After completing phases:**
```
  🎯 Phase 3 complete! 50% done.
     You're making great progress.
```

### Provide Context

**Show what's happening behind the scenes:**
```
  ℹ Using Haiku model for this task (saves 90% vs Opus)
  ℹ Skipping re-validation (no files changed)
  ℹ Found cached data in learnings.md (saving tokens)
```

---

## Error Communication

### Clear Error Messages

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ ERROR: Phase validation failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Problem:
    Phase 3 depends on Phase 5 (forward dependency)

  Location:
    .autopilot/phases/003/PLAN.md, line 4

  Why this matters:
    Phase 3 cannot execute before Phase 5 completes.
    This would cause the build to fail.

  How to fix:
    Option 1: Run /autopilot:validate --fix (recommended)
    Option 2: Manually edit the depends_on field

  Learn more:
    /autopilot:help ordering

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Warnings

```
  ⚠ Warning: Cost approaching warning threshold
    Current: $9.85 / Warning: $10.00

    Continuing execution. Use --alert-cost to adjust threshold.
```

### Recovery Options

Always show what the user can do:

```
  Build failed at Task 3.2

  Options:
    • /autopilot:cockpit --task=3.2   Resume from failed task
    • /autopilot:altitude             Check current state
    • /autopilot:rollback             Revert to last checkpoint
```

---

## Interactive Prompts

### Approval Request

```
─────────────────────────────────────────────────────────────
⏸ APPROVAL REQUIRED
─────────────────────────────────────────────────────────────

  Ready to execute 6 phases with estimated cost of $4.50

  Phase breakdown:
    001 Setup      │ $0.15 │ 3 tasks
    002 Database   │ $0.35 │ 4 tasks
    003 Auth       │ $0.55 │ 5 tasks
    004 API        │ $0.85 │ 6 tasks
    005 Frontend   │ $1.20 │ 8 tasks
    006 Testing    │ $0.65 │ 6 tasks
                   ├───────┤
    Total          │ $4.50 │ 32 tasks

  Budget: $50.00 available (would use 9%)

─────────────────────────────────────────────────────────────

  Reply "approved" to start, or "cancel" to abort.

  Tip: Use /autopilot:takeoff -y to skip approval next time.
```

### Decision Point

```
─────────────────────────────────────────────────────────────
🤔 DECISION NEEDED
─────────────────────────────────────────────────────────────

  Multiple authentication approaches available:

  1. JWT tokens (recommended)
     • Stateless, scalable
     • Est. cost: $0.45

  2. Session-based
     • Server-side state
     • Est. cost: $0.55

  3. OAuth only
     • Delegate to provider
     • Est. cost: $0.35

  Which approach? [1/2/3]:
```

---

## Compact vs Verbose Mode

### Compact (--quiet)

```
✓ Validation passed (6 phases)
✓ Phase 1 complete ($0.08)
✓ Phase 2 complete ($0.35)
✓ Phase 3 complete ($0.52)
✓ Build complete ($4.85, -19%)
```

### Verbose (default)

Full output with all sections, progress bars, and context.

### Debug (--debug)

Add technical details:

```
  [DEBUG] Spawning planner agent on Sonnet
  [DEBUG] Context size: 12,450 tokens (6% of limit)
  [DEBUG] Reading .autopilot/phases/001/PLAN.md (234 lines)
```

---

## Quick Reference

### Opening a Command

```python
def command_start(name, description):
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 AUTOPILOT: {name.upper()}
   {description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
```

### Section Header

```python
def section(title):
    print(f"""
─────────────────────────────────────────────────────────────
{title}
─────────────────────────────────────────────────────────────
""")
```

### Task Status

```python
def task_start(id, name):
    print(f"  ┌─ Task {id}: {name}")

def task_progress(message):
    print(f"  │  🔄 {message}...")

def task_complete(duration, cost):
    print(f"  │  ✓ Completed in {duration}s | ${cost:.2f}")
    print(f"  └────────────────────────────────────────")
```

### Progress Bar

```python
def progress_bar(current, total, width=30):
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"{bar} {percent*100:.0f}%"
```

---

## Message Templates

### Startup

| Situation | Message |
|-----------|---------|
| Starting | `▶ Starting {command}...` |
| Loading | `  Loading {resource}...` |
| Validating | `  Validating {item}...` |
| Ready | `✓ Ready to proceed` |

### Progress

| Situation | Message |
|-----------|---------|
| Phase start | `📋 Phase {n} of {total}: {name}` |
| Task start | `🔄 {task_id}: {description}` |
| Task done | `✓ {task_id} complete | {duration}s | ${cost}` |
| Phase done | `✅ Phase {n} complete` |

### Completion

| Situation | Message |
|-----------|---------|
| Success | `🎉 {command} complete!` |
| With savings | `Saved ${amount} ({percent}% under estimate)` |
| Checkpoint | `📌 Progress saved` |

### Errors

| Situation | Message |
|-----------|---------|
| Error | `❌ Error: {description}` |
| Warning | `⚠ Warning: {description}` |
| Info | `ℹ {description}` |
| Recovery | `Options: {list of commands}` |

---

## Integration Checklist

When implementing a command, ensure:

- [ ] Starts with command banner
- [ ] Shows startup checks
- [ ] Has section headers for major steps
- [ ] Shows progress during long operations
- [ ] Provides cost updates
- [ ] Celebrates successful completion
- [ ] Shows clear errors with recovery options
- [ ] Has both compact and verbose modes
- [ ] Saves checkpoints with confirmation
- [ ] Suggests next actions
