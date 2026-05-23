---
name: teammate
description: Spawn or manage voice teammates. Each teammate is a separate Claude personality in its own tmux pane.
---

# Manage Voice Teammates

## Usage

`/claude-talk:teammate [personality]` — spawn a specific personality, or omit for interactive selection.

## Steps

### 1. Spawn Teammate

Spawn a teammate by personality name (use Bash):
```bash
source ~/.claude-talk/venvs/wlk/bin/activate
claude-talk teammate spawn "$PERSONALITY"
```

Where `$PERSONALITY` is the argument passed to this skill (e.g., `claude`, `vex`, `hank`). If no argument, list available personalities first:
```bash
source ~/.claude-talk/venvs/wlk/bin/activate
claude-talk personality list
```
Then ask the user which personality to spawn and run `claude-talk teammate spawn <chosen>`.

### 2. Confirm

Report back: which personality was spawned, which tmux pane they're in, and that voice routing is now active for them.

Also mention: teammates can message each other using `claude-talk message send <personality> "text"` or broadcast to all with `claude-talk message broadcast "text"`. Messages arrive as `Teammate <name> said: ...` in the recipient's session.
