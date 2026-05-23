---
name: reflect
description: Reflect on a session to identify learnings, friction points, and improvements. Captures valuable insights for future sessions and system evolution.
---

# Session Reflection

Structured reflection using the `@session-reflect` workflow.

## Quick Start

```bash
# Start the reflection workflow
kspec workflow start @session-reflect

# Advance through steps (workflow will guide you)
kspec workflow next --notes "your notes..."
```

## Workflow Overview

The reflection workflow has 6 steps:

1. **What Worked Well** - Identify effective practices
2. **Friction Points** - Where things were harder than needed
3. **Check Coverage** - Search specs/tasks/inbox for existing tracking
4. **Propose Improvements** - Concrete ideas for untracked friction
5. **Discussion** - Present to user, get approval one at a time
6. **Capture** - Add approved items to inbox/observations

Use `kspec workflow show` to see current progress.

## Step Details

### Step 1: What Worked Well

Identify practices that were effective:
- Workflows that flowed smoothly
- Tools/commands that helped
- Communication patterns that kept alignment
- Decisions that proved correct

*Be specific - "categorizing items first" not "good planning"*

### Step 2: Friction Points

Identify where things were harder than needed:
- Repetitive manual steps
- Missing commands or options
- Context loss or re-explanation
- Workarounds used

*Focus on systemic issues, not one-off mistakes*

### Step 3: Check Existing Coverage

Before proposing improvements, search ALL sources:

```bash
kspec search "<keyword>"  # Searches specs, tasks, AND inbox
```

For each friction point, note if it's:
- **Already tracked** - reference the existing item/task
- **Partially covered** - note what's missing
- **Not tracked** - candidate for capture

**Exit criteria:** Must have searched specs, tasks, and inbox.

### Step 4: Propose Improvements

For untracked friction, propose concrete improvements:
- What it would do
- How it would help
- Rough scope (small/medium/large)

### Step 5: Discussion

Present findings to user. **Ask one at a time** about each improvement:
- Is this worth capturing?
- Any refinements to the idea?
- Related ideas from user perspective?

### Step 6: Capture

Use appropriate destination:

```bash
# Actionable improvements (future work)
kspec inbox add "Description" --tag reflection --tag <area>

# Friction patterns (systemic issues)
kspec meta observe friction "Description"

# Success patterns (worth replicating)
kspec meta observe success "Description"

# Open questions
kspec meta question add "Question?"
```

## Where to Capture What

| What you found | Where to put it | Why |
|----------------|-----------------|-----|
| Actionable improvement idea | `inbox add` | Will become a task eventually |
| Friction pattern (systemic) | `meta observe friction` | Informs process improvement |
| Success pattern | `meta observe success` | Worth documenting/replicating |
| Open question needing research | `meta question add` | Track during session |
| Bug or specific fix needed | `task add` | Ready to implement |

## Reflection Prompts

Use these during steps 1-2:

**Process:** What pattern did I repeat 3+ times? What workarounds did I use?
**Tools:** What command/flag did I wish existed?
**Communication:** Where was the user surprised? What should I have asked earlier?
**Learning:** What do I know now that I didn't at session start?

## Key Principles

- **Specific over general** - "No bulk AC add" not "CLI could be better"
- **Systemic over incidental** - Focus on repeatable friction
- **Ask don't assume** - User decides what's worth capturing
- **Brief on successes** - Friction points are the value

## Workflow Commands

```bash
# Check current step
kspec workflow show

# Advance with notes
kspec workflow next --notes "..."

# Skip a step if not applicable
kspec workflow next --skip --notes "reason"

# Pause for later
kspec workflow pause

# Resume
kspec workflow resume
```

## Integration

After reflection, observations can be:
- Promoted to tasks: `kspec meta promote @ref --title "..."`
- Resolved when addressed: `kspec meta resolve @ref`

## Loop Mode

You are running in autonomous loop mode. Start the workflow:

```bash
kspec workflow start @session-reflect-loop
```

### Key Differences from Interactive Mode

1. **High confidence only** - Only capture friction/successes you're certain about
2. **Search first** - MUST search existing specs/tasks/inbox before capturing anything
3. **No user prompts** - Skip discussion step, auto-resolve decisions
4. **Lower volume** - Better to capture nothing than capture noise

### Workflow Steps

1. **Review session** - What worked well, what caused friction
2. **Search existing** - For each potential capture:
   ```bash
   kspec search "<keyword>"
   ```
   If already tracked, skip it.
3. **Capture high-confidence items only**
   - Clear friction pattern you encountered multiple times? Capture it
   - Uncertain or one-off issue? Skip it
   - Success pattern worth replicating? Capture it
4. **Exit** - Don't wait for user confirmation

### Exit Conditions

- **Session reviewed** - Reflection complete (normal exit)
- **Nothing to capture** - No high-confidence items identified
- **All already tracked** - Search found existing coverage

### What NOT to Capture

- Vague observations ("could be better")
- One-time issues that won't recur
- Things you're unsure about
- Anything already tracked in specs/tasks/inbox
