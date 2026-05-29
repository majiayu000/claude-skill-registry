---
name: setup-vibereps
description: First-time setup for vibereps exercise tracker. Use when user wants to install, configure, or set up vibereps for the first time. Guides through exercise selection, hook configuration, and preferences.
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash
---

# Setup Vibereps

Guide users through vibereps configuration with a friendly setup wizard.

## Setup Flow

### Step 1: Ask Exercise Mode (Standing vs Seated)

Use AskUserQuestion to ask about exercise preference:

```
Question: "What type of exercises would you like?"
Header: "Mode"
MultiSelect: false
Options:
- "Standing & Seated (Recommended)": "Full variety - squats, jumping jacks, plus desk-friendly neck stretches"
- "Standing only": "Active exercises - squats, jumping jacks, push-ups, calf raises"
- "Seated only": "Desk-friendly - shoulder shrugs, neck stretches"
```

### Step 2: Ask Which Exercises

Based on their mode choice, show relevant exercises:

**Standing exercises:**
- squats: "Lower body strength, counters hip flexor tightness"
- jumping_jacks: "Cardio, gets blood flowing quickly"
- calf_raises: "Subtle, can do while standing at desk"
- standing_crunches: "Core workout, elbow to opposite knee"
- side_stretches: "Flexibility, relieves back tension"
- pushups: "Upper body, requires floor space"
- high_knees: "Cardio, raises heart rate"
- torso_twists: "Core mobility, loosens spine"
- arm_circles: "Shoulder mobility, easy warmup"

**Seated exercises:**
- shoulder_shrugs: "Releases neck and shoulder tension"
- neck_tilts: "Stretches sides of neck"
- neck_rotations: "Improves neck mobility"

Use AskUserQuestion with MultiSelect: true to let them pick specific exercises from the filtered list.

### Step 3: Ask About Custom Exercises

```
Question: "Would you like to add your own custom exercises?"
Header: "Custom"
MultiSelect: false
Options:
- "No, use selected exercises": "Start with the exercises you chose"
- "Yes, show me how": "Learn how to create custom exercise detection"
```

If they choose "Yes", tell them:
- Run `/add-exercise` in Claude Code to create a new exercise with guided setup
- Or manually create JSON configs in the `exercises/` directory

### Step 4: Find Install Location

```bash
if [[ -f "$HOME/.vibereps/exercise_tracker.py" ]]; then
    echo "$HOME/.vibereps"
else
    echo "$(pwd)"
fi
```

### Step 5: Configure Hooks

Read existing `~/.claude/settings.json` and update the PostToolUse hook with selected exercises:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "VIBEREPS_EXERCISES={exercises} {vibereps_dir}/exercise_tracker.py post_tool_use '{}'"
      }]
    }],
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "{vibereps_dir}/notify_complete.py '{}'"
      }]
    }]
  }
}
```

Replace:
- `{vibereps_dir}` with the detected path (use full path, not ~)
- `{exercises}` with comma-separated exercise list (e.g., `squats,jumping_jacks,shoulder_shrugs`)

Use Edit tool to update the settings file, preserving other settings.

### Step 6: Summary

Show a summary:
```
Setup complete!

Selected exercises: squats, jumping_jacks, shoulder_shrugs, neck_rotations

How it works:
1. Claude edits a file → Exercise tracker launches
2. Do a quick exercise while Claude works
3. Get notified when Claude is ready!

Useful commands:
- /test-tracker     - Test the exercise tracker
- /add-exercise     - Create a custom exercise
- /tune-detection   - Adjust detection if reps aren't counting

To change exercises later, run /setup-vibereps again.
```

## Important Notes

- Always use absolute paths in hooks (not ~, use full $HOME path)
- The Notification hook should have an empty matcher "" to catch all notifications
- Preserve existing hooks and settings when updating settings.json
