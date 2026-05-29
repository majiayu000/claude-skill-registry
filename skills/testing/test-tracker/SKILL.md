---
name: test-tracker
description: Test and run the vibereps exercise tracker. Use when user wants to launch, restart, or test the exercise UI. Handles killing existing instances and launching fresh.
allowed-tools: Bash, Read
---

# Test Exercise Tracker

## Quick Commands

**Launch in quick mode** (while Claude works):
```bash
pkill -f "exercise_tracker.py" 2>/dev/null
./exercise_tracker.py user_prompt_submit '{}'
```

**Launch in normal mode** (after task complete):
```bash
pkill -f "exercise_tracker.py" 2>/dev/null
./exercise_tracker.py task_complete '{}'
```

**Kill tracker**:
```bash
pkill -f "exercise_tracker.py"
```

## With specific exercises

Set `VIBEREPS_EXERCISES` to limit which exercises appear:
```bash
VIBEREPS_EXERCISES=squats,jumping_jacks ./exercise_tracker.py user_prompt_submit '{}'
```

## Disable temporarily

Add to hook command:
```bash
VIBEREPS_DISABLED=1 ./exercise_tracker.py ...
```

## Check if running

```bash
lsof -i :8765
```

## Clear Chrome window cache

If window size is wrong:
```bash
rm -rf /tmp/vibereps-chrome
```
