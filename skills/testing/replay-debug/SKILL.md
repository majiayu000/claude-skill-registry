---
name: Replay Debug
description: This skill should be used when the user asks to "debug", "create test script", "analyze replay report", "why isn't my game", "test if", "verify that", "check if", "reproduce bug", "frame-by-frame", or mentions "ncrs", "replay test", "replay debugging", "snap", "assertion", or debugging game behavior via replay scripts.
version: 1.0.0
---

# Replay-Based Debugging for Nethercore ZX

Debug ZX games using scriptable replay tests. Generate NCRS (Nethercore Replay Script) files that reproduce bugs, capture state snapshots, and verify assertions frame-by-frame.

## Overview

The replay debugging system enables AI-assisted debugging by:
1. **Generating test scripts** from bug descriptions
2. **Running tests** headlessly with state capture
3. **Analyzing reports** to identify root causes
4. **Suggesting fixes** with code references

This transforms debugging from "describe what you see" to "write what should happen, get precise feedback."

## Core Workflow

### When User Reports a Bug

1. Ask clarifying questions if needed:
   - What inputs trigger the issue?
   - What is the expected vs actual behavior?
   - When in gameplay does it occur?

2. Generate a minimal `.ncrs` script:
   - Start with `snap: true` on frame 0 to capture initial state
   - Add inputs that reproduce the scenario
   - Add snaps around the problematic action
   - Use assertions for expected behavior

3. Instruct user to run:
   ```bash
   nether replay run test.ncrs --report report.json
   ```

4. When user shares the report, analyze for root cause.

### Generating Test Scripts

Keep scripts minimal (under 100 frames when possible):

```toml
# Basic test structure
console = "zx"
seed = 0
players = 1

frames = [
  { f = 0, p1 = "idle", snap = true },                    # Initial state
  { f = 1, p1 = "a", snap = true, assert = "$velocity_y < 0" },  # Action + verify
  { f = 10, p1 = "idle", snap = true },                   # After effect
]
```

**Key principles:**
- Capture frame 0 for baseline state
- Add snaps before and after the problematic action
- Use assertions for pass/fail verification
- Include only frames relevant to the bug

### Analyzing Reports

Reports contain snapshots showing pre/post state per frame:

```json
{
  "snapshots": [
    {
      "frame": 1,
      "input": "a",
      "pre": { "$velocity_y": 0, "$on_ground": true },
      "post": { "$velocity_y": -8.0, "$on_ground": false },
      "delta": { "$velocity_y": -8.0, "$on_ground": "true -> false" }
    }
  ],
  "assertions": [
    { "frame": 1, "condition": "$velocity_y < 0", "passed": true, "actual": -8.0 }
  ]
}
```

**Focus on:**
- `delta` - What changed each frame (the key insight)
- Failed assertions - Expected vs actual values
- Unexpected values in pre/post snapshots

**Common diagnosis patterns:**
- Velocity stayed 0 after jump input -> Jump not applying force
- Position unchanged with movement input -> Collision blocking or input not read
- Variable changed unexpectedly -> State corruption or wrong calculation
- Assertion passed but behavior wrong -> Assertion too lenient

## NCRS Quick Reference

### Format

```toml
console = "zx"           # Required: Console type
seed = 0                 # Required: Random seed for determinism
players = 1              # Required: Player count (1-4)

frames = [
  { f = 0, p1 = "idle" },
  { f = 1, p1 = "a", snap = true },
  { f = 2, p1 = "a", assert = "$velocity_y < 0" },
]
```

### Frame Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `f` | Frame number | `f = 60` |
| `p1`-`p4` | Player inputs | `p1 = "right+a"` |
| `snap` | Capture pre/post state | `snap = true` |
| `assert` | Pass/fail condition | `assert = "$health > 0"` |
| `action` | Debug action to invoke | `action = "Load Level"` |
| `action_params` | Action parameters | `action_params = { level = 2 }` |

### Input Values

**Button names:** `idle`, `up`, `down`, `left`, `right`, `a`, `b`, `x`, `y`, `l`, `r`, `l2`, `r2`, `start`, `select`

**Combinations:** Use `+` to combine: `"right+a"`, `"up+right+b"`

### Assertion Operators

Supported: `==`, `!=`, `<`, `>`, `<=`, `>=`

```toml
assert = "$velocity_y < 0"        # Negative velocity (jumping up)
assert = "$on_ground == true"     # Boolean check
assert = "$health >= 50"          # Range check
```

## Debug Variables

Games register debug variables with `$` prefix. Scan code for `debug_register_*` calls to find available variables:

```rust
// In game init()
debug_register_f32(b"player_x", 8, &PLAYER_X);    // -> $player_x
debug_register_f32(b"velocity_y", 10, &VEL_Y);    // -> $velocity_y
debug_register_bool(b"on_ground", 9, &ON_GROUND); // -> $on_ground
```

**Common variables:**
- `$player_x`, `$player_y` - Position
- `$velocity_x`, `$velocity_y` - Movement
- `$on_ground` - Grounded state
- `$health`, `$score` - Game state

## Debug Actions

Games can register callable debug actions with parameters. Use these in scripts to skip setup and focus on the bug.

### Why Use Actions?

**Instead of:**
- Recording 5 minutes of menu navigation
- Playing through tutorial levels
- Manually positioning enemies

**Use:**
- `action = "Load Level"` to skip to specific levels
- `action = "Set Player Position"` to place player
- `action = "Spawn Enemy"` to create test scenarios

### Discovering Actions

```bash
grep -r "debug_action_begin" src/
```

Example registration in game code:
```rust
debug_action_begin(b"Load Level".as_ptr(), 10, b"debug_load_level".as_ptr(), 16);
debug_action_param_i32(b"level".as_ptr(), 5, 1);  // param "level", default 1
debug_action_end();
```

### Using Actions in Scripts

```toml
# Skip to level 2 for testing
[[frames]]
f = 0
action = "Load Level"
action_params = { level = 2 }

# Now test from level 2
[[frames]]
f = 1
p1 = "idle"
snap = true
```

### Common Actions

| Action | Parameters | Use Case |
|--------|------------|----------|
| Load Level | `{ level = N }` | Skip to specific level |
| Set Position | `{ x, y }` | Place player for collision tests |
| Set Health | `{ health = N }` | Test low-health scenarios |
| Spawn Enemy | `{ type, x, y }` | Create specific test scenarios |
| Skip Menu | (none) | Bypass title/menu screens |
| God Mode | `{ enabled = bool }` | Isolate mechanics from damage |

### Benefits

- **Faster execution** - Skip irrelevant gameplay
- **Focused tests** - Test exactly what matters
- **Less brittle** - Immune to menu/UI changes
- **Reusable** - Same action works across scripts

## CLI Commands

```bash
# Run script and generate report
nether replay run test.ncrs --report report.json

# Run headlessly (no window, for CI)
nether replay run test.ncrs --headless --report report.json

# Stop on first failed assertion
nether replay run test.ncrs --fail-fast

# Validate script syntax without running
nether replay validate test.ncrs
```

## Example Debugging Session

**User:** "My player doesn't jump when I press A"

**Response:**

1. Generate test script:
```toml
# jump_test.ncrs - Test jump mechanics
console = "zx"
seed = 0
players = 1

frames = [
  { f = 0, p1 = "idle", snap = true },                           # Initial state
  { f = 1, p1 = "a", snap = true, assert = "$velocity_y < 0" },  # Jump frame
  { f = 2, p1 = "a", snap = true },                              # Holding jump
  { f = 10, p1 = "idle", snap = true },                          # After jump
]
```

2. Run: `nether replay run jump_test.ncrs --report report.json`

3. Share the report for analysis.

**Report shows `$velocity_y` stayed 0 after pressing A:**

The report shows `$velocity_y` remained 0 after pressing A at frame 1. This indicates the jump is not applying velocity.

Common causes:
- Using `input.a_pressed()` instead of `input.a_just_pressed()`
- Jump velocity applied to wrong variable
- Ground check preventing jump

Read the jump handling code to identify the specific issue.

## File Organization

Store test scripts in a dedicated directory:

```
game-project/
└── tests/
    └── replay/
        ├── jump_test.ncrs
        ├── collision_test.ncrs
        └── movement_test.ncrs
```

## Additional Resources

### Reference Files

For detailed NCRS format specification:
- **`references/ncrs-format.md`** - Complete format reference with all options

### Example Files

Working examples in `examples/`:
- **`jump-test.ncrs`** - Jump mechanics debugging
- **`collision-test.ncrs`** - Collision detection debugging
- **`movement-test.ncrs`** - Movement debugging
- **`action-setup.ncrs`** - Using debug actions for test setup

### Related Skills

- **`debugging-guide`** - F4 panel, sync testing, debug registration
- **`testing-fundamentals`** (zx-test) - Sync tests, replay regression

## Commands

Use these slash commands for common operations:
- `/replay-test [description]` - Generate test script from bug description
- `/replay-analyze [path]` - Analyze a report.json file
- `/replay-template [type]` - Generate template (jump, collision, movement, etc.)
