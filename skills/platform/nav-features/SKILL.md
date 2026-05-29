---
name: nav-features
description: Show and toggle Navigator features. Auto-invoke when user says "show features", "enable/disable feature", "my navigator settings", or "configure navigator".
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Navigator Features Skill

Display and toggle Navigator features with an interactive table. Helps users understand what's enabled and customize their setup.

## When to Invoke

Invoke this skill when the user:
- Says "show my features", "navigator features", "what features are enabled"
- Says "enable [feature]", "disable [feature]", "turn on/off [feature]"
- Says "configure navigator", "my navigator settings"
- Asks "what can navigator do?", "what features are available?"

**DO NOT invoke** if:
- User is asking about project features (not Navigator)
- User is in middle of implementation
- Just starting session (use nav-start instead)

## Execution Steps

### Step 1: Read Current Configuration

```bash
python3 "$SKILL_BASE_DIR/functions/feature_manager.py" show
```

This displays the feature table:
```
v5.6.0 Features:

┌─────────────────┬────────┬─────────────────────────────────────────────────┐
│ Feature         │ Status │ Description                                     │
├─────────────────┼────────┼─────────────────────────────────────────────────┤
│ task_mode       │ ✅     │ Auto-detects task complexity, defers to skills  │
│ tom_features    │ ✅     │ Verification checkpoints, user profile, diag... │
│ loop_mode       │ ⏸ Off  │ Autonomous loop execution (enable when needed)  │
│ simplification  │ ✅     │ Post-implementation code cleanup with Opus      │
│ auto_update     │ ✅     │ Auto-updates on session start                   │
└─────────────────┴────────┴─────────────────────────────────────────────────┘

All v5.6.0 features configured.
```

### Step 2: Handle Toggle Request (If Applicable)

If user requested to enable/disable a feature:

```bash
# Enable a feature
python3 "$SKILL_BASE_DIR/functions/feature_manager.py" enable task_mode

# Disable a feature
python3 "$SKILL_BASE_DIR/functions/feature_manager.py" disable loop_mode
```

**Supported features**:
- `task_mode` - Unified workflow orchestration
- `tom_features` - Theory of Mind (verification checkpoints, profile, diagnostics)
- `loop_mode` - Autonomous loop execution
- `simplification` - Code cleanup before commit
- `auto_update` - Auto-update on session start

**After toggle, show updated table**.

### Step 3: Explain Feature (If Asked)

If user asks about a specific feature, provide details:

**task_mode**:
```
Task Mode (v5.6.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Auto-detects task complexity and routes appropriately:
- Simple tasks → Direct execution
- Skill matches → Defers to skill workflow
- Substantial → Task Mode phases (RESEARCH→COMPLETE)

Config: task_mode.enabled, complexity_threshold (0.5)
```

**tom_features**:
```
Theory of Mind (v5.0.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Human-AI collaboration improvements:
- Verification checkpoints for high-stakes skills
- User profile (nav-profile) - remembers preferences
- Quality detection (nav-diagnose) - catches drift

Config: tom_features.verification_checkpoints, profile_enabled
```

**loop_mode**:
```
Loop Mode (v5.1.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Run until done" capability:
- Structured completion signals (NAVIGATOR_STATUS)
- Dual-condition exit (heuristics + EXIT_SIGNAL)
- Stagnation detection prevents infinite loops

Trigger: "run until done", "loop mode"
Config: loop_mode.enabled, max_iterations (5)
```

**simplification**:
```
Code Simplification (v5.4.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Automatic code clarity improvements:
- Runs post-implementation, before commit
- Clarity over brevity, functionality preserved
- Uses Opus model for best results

Trigger: "simplify this code"
Config: simplification.enabled, trigger, scope
```

**auto_update**:
```
Auto-Update (v5.5.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Automatic plugin updates on session start:
- Checks for newer version
- Updates silently if available
- Never blocks session start

Config: auto_update.enabled, check_interval_hours (1)
```

## Predefined Functions

### functions/feature_manager.py

**Purpose**: Display and toggle Navigator features

**Usage**:
```bash
# Show all features
python3 feature_manager.py show

# Show for first session (includes welcome message)
python3 feature_manager.py show --first-session

# Enable a feature
python3 feature_manager.py enable task_mode

# Disable a feature
python3 feature_manager.py disable loop_mode

# Get feature details
python3 feature_manager.py info task_mode
```

**Output**: Formatted feature table or status message

## Error Handling

**Config not found**:
```
❌ .nav-config.json not found

Run "Initialize Navigator in this project" first.
```

**Unknown feature**:
```
❌ Unknown feature: xyz

Available features:
  task_mode, tom_features, loop_mode, simplification, auto_update
```

## Success Criteria

- [ ] Feature table displayed correctly
- [ ] Toggle updates config file
- [ ] Updated table shown after toggle
- [ ] Feature details available on request

## Notes

This skill is triggered on first session (via nav-start) to help users understand available features and optionally disable unused ones to save tokens.
