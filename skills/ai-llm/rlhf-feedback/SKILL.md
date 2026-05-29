---
name: rlhf-feedback
description: Autonomous RLHF feedback capture - Claude self-captures mistakes and successes
triggers:
  - thumbs down
  - thumbs up
  - mistake
  - good job
  - wrong
  - correct
  - that worked
  - that failed
---

# RLHF Feedback Capture Skill

**AUTONOMOUS** - Claude captures feedback without user running commands.

## When to Capture Feedback

### Capture (Thumbs Down) When:
- User says "that's wrong", "no", "incorrect", "that broke something"
- User corrects my answer
- User has to repeat themselves
- I made an assumption that was wrong
- Code I wrote caused errors
- I gave instructions instead of acting (violated ACT DON'T INSTRUCT)

### Capture (Thumbs Up) When:
- User says "good", "thanks", "that worked", "perfect"
- Task completed successfully on first try
- User doesn't need to correct me
- Code works without errors

## How to Capture (Claude Executes This)

```bash
# After detecting negative feedback signal:
node "$CLAUDE_PROJECT_DIR/.claude/scripts/feedback/capture-feedback.js" \
  --feedback=down \
  --context="[What went wrong]" \
  --tags="[relevant-tags]"

# After detecting positive feedback signal:
node "$CLAUDE_PROJECT_DIR/.claude/scripts/feedback/capture-feedback.js" \
  --feedback=up \
  --context="[What went right]" \
  --tags="[relevant-tags]"
```

## Domain Tags for Random Timer

Use these tags to categorize feedback:
- `timer-logic` - Timer countdown, random time generation
- `redux-state` - State management, slices, persistence
- `ui-components` - Buttons, sliders, screens
- `navigation` - React Navigation, screen transitions
- `sound-haptics` - Audio playback, vibration
- `storage` - MMKV, persistence
- `testing` - Jest, Maestro tests
- `styling` - Theme, colors, glassmorphism
- `performance` - Speed, memory, optimization

## Action Tags

- `fix` - Bug fix
- `implementation` - New feature
- `refactor` - Code restructure
- `regression` - Broke something that worked
- `assumption` - Made incorrect assumption
- `shallow-answer` - Didn't read code, gave surface answer

## Examples

### User says "that broke the slider"
```bash
node .claude/scripts/feedback/capture-feedback.js \
  --feedback=down \
  --context="Broke range slider while implementing timer fix" \
  --tags="ui-components,regression"
```

### User says "perfect, timer works now"
```bash
node .claude/scripts/feedback/capture-feedback.js \
  --feedback=up \
  --context="Fixed timer countdown logic correctly" \
  --tags="timer-logic,fix"
```

### User has to repeat themselves
```bash
node .claude/scripts/feedback/capture-feedback.js \
  --feedback=down \
  --context="User had to repeat request - didn't understand first time" \
  --tags="assumption,shallow-answer"
```

## Data Storage

All feedback is LOCAL ONLY (excluded from git):
- `.claude/memory/feedback/feedback-log.jsonl`
- `.claude/memory/feedback/feedback-summary.json`

## Session Start Integration

At session start, the hook queries past failures to remind Claude what to avoid.
This creates a learning loop: Mistake → Capture → Warning → Avoid repeat.

## IMPORTANT: Act Don't Instruct

**Claude EXECUTES the capture command directly.**
Never tell the user to run it - just run it.
