---
name: config
description: Manage bluera-base plugin configuration
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# bluera-base Configuration

Manage plugin settings stored in `.bluera/bluera-base/`.

## Subcommands

| Command | Description |
|---------|-------------|
| `/bluera-base:config` or `/bluera-base:config show` | Interactive feature toggle (view and change settings) |
| `/bluera-base:config init` | Initialize config for this project |
| `/bluera-base:config set <key> <value>` | Set a config value |
| `/bluera-base:config enable <feature>` | Enable a feature |
| `/bluera-base:config disable <feature>` | Disable a feature |
| `/bluera-base:config reset` | Reset to defaults |
| `/bluera-base:config status [--state]` | Show config and state file status |

---

## Algorithm

### Show (default)

Interactive feature toggle with current status display.

**Steps:**

1. Check if `.bluera/bluera-base/` exists
2. Load and merge: defaults ← `config.json` ← `config.local.json`
3. Display brief current status showing which features are enabled
4. Use AskUserQuestion with multiSelect to let user toggle features
5. Apply changes based on selections (handle dependencies)
6. Display summary of changes made

**Phase 1: Display Current Status**

Show a compact summary of current state:

```text
bluera-base configuration

Currently enabled: notifications
Currently disabled: auto-learn, deep-learn, auto-commit, auto-push, dry-check, dry-auto, strict-typing, standards-review
```

**Phase 2: Interactive Toggle**

Use AskUserQuestion with multiSelect. The question text indicates which features are currently ON so users know what to re-select to keep them enabled.

```yaml
question: "Select features to enable (unselected = disabled). Currently ON: notifications"
header: "Features"
multiSelect: true
options:
  - label: "auto-learn"
    description: "Track command patterns, suggest CLAUDE.md edits"
  - label: "deep-learn"
    description: "Semantic session analysis via Claude CLI (~$0.001/session)"
  - label: "auto-commit"
    description: "Prompt to commit on session stop"
  - label: "auto-push"
    description: "Push after commit (requires auto-commit)"
  - label: "notifications"
    description: "Desktop notifications when Claude needs input"
  - label: "dry-check"
    description: "Enable /dry command for duplicate detection"
  - label: "dry-auto"
    description: "Auto-scan for duplicates on stop (requires dry-check)"
  - label: "strict-typing"
    description: "Block any/as (TS), Any/cast (Python)"
  - label: "standards-review"
    description: "Review code against CLAUDE.md before commit"
```

**Phase 3: Apply Changes with Dependency Handling**

Compare user selections to current state and apply changes:

1. **Parse selections** - Get list of selected feature names from response
2. **Handle dependencies** - When enabling dependent features, auto-enable parent:
   - `auto-push` selected → also enable `auto-commit`
   - `dry-auto` selected → also enable `dry-check`
3. **Handle dependency removal** - When disabling parent, also disable dependent:
   - `auto-commit` deselected → also disable `auto-push`
   - `dry-check` deselected → also disable `dry-auto`
4. **Apply changes** - For each feature:
   - If newly selected (was OFF, now ON) → enable it
   - If newly deselected (was ON, now OFF) → disable it

**Phase 4: Display Summary**

```text
Configuration updated:

  ✓ Enabled: auto-learn, strict-typing
  ✗ Disabled: notifications

Unchanged: deep-learn, auto-commit, auto-push, dry-check, dry-auto, standards-review

Config saved to .bluera/bluera-base/config.local.json
```

If no changes were made:

```text
No changes made. Current configuration unchanged.
```

**Feature to Config Path Mapping**

| Feature | Config Path |
|---------|-------------|
| `auto-learn` | `.autoLearn.enabled` |
| `deep-learn` | `.deepLearn.enabled` |
| `auto-commit` | `.autoCommit.enabled` |
| `auto-push` | `.autoCommit.push` |
| `notifications` | `.notifications.enabled` |
| `dry-check` | `.dryCheck.enabled` |
| `dry-auto` | `.dryCheck.onStop` |
| `strict-typing` | `.strictTyping.enabled` |
| `standards-review` | `.standardsReview.enabled` |

### Init

Interactive initialization that explains each feature and lets user configure during setup.

**Steps:**

1. Check if config already exists (offer to reconfigure if so)
2. Create `.bluera/bluera-base/` directory structure
3. Walk through each feature section with AskUserQuestion
4. Build `config.json` from user choices
5. Update `.gitignore` with required patterns
6. Report final configuration

**Interactive Flow:**

Display each section header, explain the feature, then use AskUserQuestion.

---

#### 1. Auto-Learn (Command Pattern Learning)

```text
## Auto-Learn

Tracks frequently used commands and suggests adding them to CLAUDE.md.

Technical details:
- Observes command patterns during sessions via PreToolUse hook
- Stores patterns in .bluera/bluera-base/state/session-signals.json
- Threshold: number of occurrences before acting (default: 3)
- Modes:
  - "suggest" - shows recommendations at session end, you decide
  - "auto" - writes learnings directly to target file
- Targets:
  - "local" (default) - writes to CLAUDE.local.md (private, gitignored)
  - "shared" - writes to CLAUDE.md (committed, team-shared)
```

Use AskUserQuestion:

- Header: "Auto-Learn"
- Question: "Enable command pattern learning?"
- Options:
  1. **No (default)** - Don't track command patterns
  2. **Yes - suggest mode** - Track and suggest CLAUDE.md updates
  3. **Yes - auto mode** - Track and auto-apply CLAUDE.md updates

---

#### 2. Milhouse (Iterative Development Loop)

```text
## Milhouse

Controls behavior of /milhouse-loop for iterative development tasks.

Technical details:
- defaultMaxIterations: 0 = unlimited, or set limit to prevent runaway loops
- defaultStuckLimit: iterations without progress before asking if stuck (default: 3)
- defaultGates: commands that must pass after each iteration
  - Example: ["bun test", "bun run lint"]
  - Empty = no gates
```

Use AskUserQuestion:

- Header: "Milhouse"
- Question: "Configure milhouse loop settings?"
- Options:
  1. **Use defaults** - Unlimited iterations, stuck limit 3, no gates
  2. **Set max iterations** - Follow up to ask for number
  3. **Configure gates** - Follow up to ask for gate commands

If user selects "Set max iterations", ask:

- Header: "Max Iterations"
- Question: "Maximum iterations before stopping? (0 = unlimited)"
- Options: 5, 10, 20, Unlimited (0)

If user selects "Configure gates", ask for gate commands as comma-separated list.

---

#### 3. Notifications

```text
## Notifications

Desktop notifications when Claude Code needs your input.

Technical details:
- Uses osascript on macOS, notify-send on Linux
- Triggered by Notification hook when Claude prompts for input
- Helps when multitasking in other windows
```

Use AskUserQuestion:

- Header: "Notifications"
- Question: "Enable desktop notifications?"
- Options:
  1. **Yes (default)** - Notify when Claude needs input
  2. **No** - Silent operation

---

#### 4. Auto-Commit

```text
## Auto-Commit

Prompt to commit uncommitted changes when session ends.

Technical details:
- Stop hook blocks exit and prompts you to run /bluera-base:commit
- Uses atomic commit skill for well-formatted commits
- Optional: add push instruction to the prompt
```

Use AskUserQuestion:

- Header: "Auto-Commit"
- Question: "Enable auto-commit on session stop?"
- Options:
  1. **No (default)** - Manual commits only
  2. **Yes - commit only** - Commit but don't push
  3. **Yes - commit and push** - Commit and push to origin

---

#### 5. DRY Check (Duplicate Code Detection)

```text
## DRY Check

Detects copy-paste / duplicate code using jscpd.

Technical details:
- threshold: max allowed duplicate percentage (default: 5%)
- minTokens: minimum tokens to consider duplicate (default: 70)
- minLines: minimum lines to consider duplicate (default: 5)
- onStop: auto-scan when session ends (default: false)
- Manual scan always available via /dry command
```

Use AskUserQuestion:

- Header: "DRY Check"
- Question: "Enable duplicate code detection?"
- Options:
  1. **No (default)** - Disabled
  2. **Yes - manual only** - Use /dry command when needed
  3. **Yes - auto-scan on stop** - Scan for duplicates when session ends

---

#### 6. Strict Typing

```text
## Strict Typing

Block unsafe type patterns in TypeScript and Python.

Technical details:
- TypeScript: blocks `any` type, `as` casts (except `as const`), @ts-ignore without explanation
- Python: blocks `Any` type, `# type: ignore` without error code, `cast()`
- Enforced by post-edit-check.sh hook on every file edit
- Escape hatch: `// ok:` or `# ok:` comment on specific lines
```

Use AskUserQuestion:

- Header: "Strict Typing"
- Question: "Enable strict typing enforcement?"
- Options:
  1. **No (default)** - Allow any/as casts
  2. **Yes** - Block any, as casts, type: ignore

---

**After all questions:**

1. Build config object from user responses
2. Write to `.bluera/bluera-base/config.json`
3. Update `.gitignore`:

   ```gitignore
   .bluera/
   !.bluera/
   !.bluera/bluera-base/
   !.bluera/bluera-base/config.json
   ```

4. Display final configuration summary:

```text
Configuration saved to .bluera/bluera-base/config.json

Enabled features:
  ✓ notifications
  ✓ strict-typing

Disabled features:
  ✗ auto-learn
  ✗ auto-commit
  ✗ dry-check

Run /bluera-base:config show to see full settings.
Run /bluera-base:config enable|disable <feature> to change later.
```

### Set

Arguments: `<key> <value> [--shared]`

1. Parse key as JSON path (e.g., `.autoLearn.mode`)
2. Validate value type matches schema
3. Write to `config.local.json` (or `config.json` with `--shared`)
4. Display updated value

### Enable / Disable

Toggle features by name. If the feature name is not recognized, list available features.

| Feature | Config Path | Description |
|---------|-------------|-------------|
| `auto-learn` | `.autoLearn.enabled` | Track command patterns, suggest CLAUDE.md edits |
| `auto-commit` | `.autoCommit.enabled` | Auto-commit uncommitted changes on session stop |
| `auto-push` | `.autoCommit.push` | Add push instruction to auto-commit prompt (requires `auto-commit` enabled) |
| `notifications` | `.notifications.enabled` | Desktop notifications on permission prompts |
| `dry-check` | `.dryCheck.enabled` | Enable DRY duplicate code detection |
| `dry-auto` | `.dryCheck.onStop` | Auto-scan for duplicates on session stop (requires `dry-check` enabled) |
| `strict-typing` | `.strictTyping.enabled` | Block `any`/`as` (TS), `Any`/`cast` (Python) |
| `standards-review` | `.standardsReview.enabled` | Review code against CLAUDE.md before commit |
| `deep-learn` | `.deepLearn.enabled` | Semantic session analysis using Claude CLI |

**If unrecognized feature name:**

```text
Unknown feature: "autoLearn"

Available features:
  auto-learn       Track patterns, suggest CLAUDE.md edits
  auto-commit      Prompt to commit on stop
  auto-push        Add push instruction to prompt
  notifications    Desktop notifications on prompts
  dry-check        Detect duplicate code
  dry-auto         Auto-scan for duplicates on stop
  strict-typing    Block any/as (TS), Any/cast (Python)
  standards-review Review code against CLAUDE.md on commit
  deep-learn       Semantic session analysis via Claude CLI
```

### Reset

Options:

- No args: Remove `config.local.json` only (keep shared config)
- `--all`: Remove both config files

### Status

Show state file status for debugging and visibility.

1. Check if `.bluera/bluera-base/` exists
2. List state directory contents with sizes
3. If milhouse-loop.md exists, show iteration status
4. Report environment variables if set (BLUERA_STATE_DIR, BLUERA_CONFIG)

**Output format:**

```text
Config: .bluera/bluera-base/
├── config.json (exists, 250 bytes)
└── config.local.json (not found)

State: .bluera/bluera-base/state/
├── milhouse-loop.md (active, iteration 3/10)
└── session-signals.json (12 entries)

Env (from CLAUDE_ENV_FILE):
├── BLUERA_STATE_DIR: /path/to/state
└── BLUERA_CONFIG: /path/to/config.json
```

---

## Configuration Schema

```json
{
  "version": 1,
  "autoLearn": {
    "enabled": false,     // opt-in: track commands for learning suggestions
    "mode": "suggest",    // suggest | auto
    "threshold": 3,       // occurrences before suggesting
    "target": "local"     // local | shared
  },
  "milhouse": {
    "defaultMaxIterations": 0,   // 0 = unlimited
    "defaultStuckLimit": 3,      // 0 = disabled
    "defaultGates": []           // e.g., ["bun test", "bun run lint"]
  },
  "notifications": {
    "enabled": true
  },
  "autoCommit": {
    "enabled": false,    // opt-in: auto-commit on session stop
    "onStop": true,      // trigger on Stop hook
    "push": false,       // also push after commit
    "remote": "origin"   // remote to push to
  },
  "dryCheck": {
    "enabled": false,    // opt-in: enable DRY duplicate detection
    "onStop": false,     // auto-scan on session stop
    "threshold": 5,      // max allowed duplicate %
    "minTokens": 70,     // min tokens to consider duplicate
    "minLines": 5        // min lines to consider duplicate
  },
  "strictTyping": {
    "enabled": false     // opt-in: block 'any', 'as' casts, type: ignore
  },
  "standardsReview": {
    "enabled": false,    // opt-in: review code against CLAUDE.md on commit
    "mode": "warn"       // warn (report only) | block (prevent commit)
  },
  "deepLearn": {
    "enabled": false,    // opt-in: semantic session analysis
    "model": "haiku",    // haiku | sonnet
    "maxBudget": 0.02    // max USD per analysis
  }
}
```

---

## Directory Structure

```text
.bluera/bluera-base/
├── config.json              # Team-shareable (committed)
├── config.local.json        # Personal overrides (gitignored)
└── state/                   # Runtime state (gitignored)
    ├── milhouse-loop.md     # Active loop state
    ├── session-signals.json # Learning observation data
    ├── pending-learnings.jsonl # Deep learning pending queue
    ├── dry-report.md        # Last DRY scan report
    └── jscpd-report.json    # Raw jscpd output
```

---

## Examples

```bash
# Interactive toggle - view current settings and toggle features on/off
/bluera-base:config

# Same as above (show is the default)
/bluera-base:config show

# Initialize config for a new project (guided setup)
/bluera-base:config init

# CLI toggle - enable/disable specific features (for scripting)
/bluera-base:config enable auto-learn

# Set learning mode to auto-apply
/bluera-base:config set .autoLearn.mode auto

# Set default gates for milhouse
/bluera-base:config set .milhouse.defaultGates '["bun test", "bun run lint"]' --shared

# Disable notifications
/bluera-base:config disable notifications

# Reset local overrides
/bluera-base:config reset

# Reset everything
/bluera-base:config reset --all

# Show state file status (useful for debugging milhouse loops)
/bluera-base:config status --state

# Enable auto-commit on session stop
/bluera-base:config enable auto-commit

# Enable auto-push after commit
/bluera-base:config enable auto-push

# Set custom remote for auto-push
/bluera-base:config set .autoCommit.remote upstream --shared

# Enable DRY duplicate checking
/bluera-base:config enable dry-check

# Enable auto-scan on session stop
/bluera-base:config enable dry-auto

# Set custom DRY thresholds
/bluera-base:config set .dryCheck.minTokens 50 --shared

# Enable strict typing enforcement (blocks any, as casts, type: ignore)
/bluera-base:config enable strict-typing

# Enable standards review on commit (validates against CLAUDE.md)
/bluera-base:config enable standards-review

# Set standards review to block mode (prevents commits with violations)
/bluera-base:config set .standardsReview.mode block --shared

# Enable deep learning (semantic session analysis)
/bluera-base:config enable deep-learn

# Set deep learning model (haiku is faster/cheaper, sonnet is smarter)
/bluera-base:config set .deepLearn.model sonnet

# Set max budget per analysis
/bluera-base:config set .deepLearn.maxBudget 0.05
```

---

## Gitignore Patterns

The `/bluera-base:config init` command adds these patterns to `.gitignore`:

```gitignore
# Bluera plugins - shared config committed, local/state ignored
.bluera/
!.bluera/
!.bluera/bluera-base/
!.bluera/bluera-knowledge/
.bluera/bluera-base/*
.bluera/bluera-knowledge/*
!.bluera/bluera-base/config.json
!.bluera/bluera-base/TODO.txt
!.bluera/bluera-knowledge/stores.config.json
```

This ensures:

- `.bluera/` data is ignored by default
- `config.json` is committed (team-shareable)
- `config.local.json` and `state/` are gitignored

---

## Implementation Notes

Use the config library for all operations:

```bash
source "${CLAUDE_PLUGIN_ROOT}/hooks/lib/config.sh"
source "${CLAUDE_PLUGIN_ROOT}/hooks/lib/gitignore.sh"

# Load effective config
config=$(bluera_load_config)

# Get specific value
enabled=$(bluera_get_config ".autoLearn.enabled")

# Check boolean
if bluera_config_enabled ".autoLearn.enabled"; then
  # do learning...
fi

# Set value
bluera_set_config ".autoLearn.mode" "auto"

# Ensure gitignore patterns
gitignore_ensure_patterns
```
