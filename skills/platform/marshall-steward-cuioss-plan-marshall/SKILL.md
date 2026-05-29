---
name: marshall-steward
description: Project configuration wizard for planning system. Manages executor generation, health checks, build systems, and skill domains.
allowed-tools: Read, Write, Edit, Bash, Glob, Skill, AskUserQuestion
---

# Marshall Steward Skill

## Enforcement Rules

**EXECUTION MODE**: Execute this skill immediately. Do not explain, summarize, or discuss these instructions.

### Script Execution
1. Run scripts EXACTLY as documented - no improvisation
2. Bootstrap scripts use direct Python paths with glob
3. All other scripts use: `python3 .plan/execute-script.py {notation} ...`

### Menu Behavior
1. After ANY operation completes → return to Main Menu
2. Only exit when user selects "Quit"

### Prohibited Actions
- Inventing alternative menu structures or options
- Ending without returning to menu (unless Quit)
- Summarizing what you're about to do instead of doing it

---

## What This Skill Provides

**Wizard Mode**: Sequential setup for new projects (executor generation, marshal.json init, build detection, skill domains)

**Menu Mode**: Interactive maintenance for returning users (regenerate executor, health check, configuration)

---

## Scripts

| Script | Notation | Purpose |
|--------|----------|---------|
| determine-mode | `plan-marshall:marshall-steward:determine-mode` | Determine wizard vs menu mode |
| gitignore-setup | `plan-marshall:marshall-steward:gitignore-setup` | Configure .gitignore for .plan/ |
| cleanup | `plan-marshall:run-config:cleanup` | Clean temp, logs, archived-plans, memory (delegated to run-config) |
| ci_health | `plan-marshall:ci-operations:ci_health` | CI provider detection (delegated to ci-operations) |
| plan-marshall-config | `plan-marshall:plan-marshall-config:plan-marshall-config` | Project-level marshal.json CRUD |
| scan-marketplace-inventory | `plan-marshall:marketplace-inventory:scan-marketplace-inventory` | Script discovery |
| profiles | `pm-dev-java:maven-profile-management:profiles` | Maven profile management |
| permission-doctor | `plan-marshall:permission-doctor:permission-doctor` | Permission analysis |
| permission-fix | `plan-marshall:permission-fix:permission-fix` | Permission fixes |
| generate-executor | `plan-marshall:script-executor:generate-executor` | Executor generation |

---

## Prerequisites

This skill requires `${PLUGIN_ROOT}` to be set by the invoking command (e.g., `/marshall-steward`).
The plugin root is detected via `bootstrap-plugin.py` and cached in `.plan/marshall-state.toon`.

---

## Step 0: Determine Mode

Determine whether to run wizard or menu based on existing files.

**BOOTSTRAP**: Since execute-script.py may not exist yet, use DIRECT Python call with glob:

```bash
python3 ${PLUGIN_ROOT}/plan-marshall/*/skills/marshall-steward/scripts/determine-mode.py mode
```

**Output (TOON)**:
```toon
mode	wizard
reason	executor_missing
```

### Mode Routing

| mode | reason | Action |
|------|--------|--------|
| `wizard` | `executor_missing` | Load: `Read references/wizard-flow.md` → Execute wizard |
| `wizard` | `marshal_missing` | Load: `Read references/wizard-flow.md` → Execute wizard |
| `menu` | `both_exist` | Show Main Menu below |

### Check for `--wizard` Flag

If `--wizard` flag provided, force wizard regardless of determine-mode result:
```
Read references/wizard-flow.md
```
Execute the wizard flow from that file.

---

## Interactive Menu (Returning User)

Display menu when both executor and marshal.json exist.

### Main Menu

```
AskUserQuestion:
  question: "What would you like to do?"
  header: "Main Menu"
  options:
    - label: "1. Maintenance"
      description: "Regenerate executor, clean logs"
    - label: "2. Health Check"
      description: "Verify setup, diagnose issues"
    - label: "3. Configuration"
      description: "Build systems, skill domains"
    - label: "4. Quit"
      description: "Exit plan-marshall"
  multiSelect: false
```

### Menu Routing

| User Selection | Action |
|----------------|--------|
| "1. Maintenance" | Load: `Read references/menu-maintenance.md` → Execute |
| "2. Health Check" | Load: `Read references/menu-healthcheck.md` → Execute |
| "3. Configuration" | Load: `Read references/menu-configuration.md` → Execute |
| "4. Quit" | Output "Good bye!" → STOP |

After any menu option completes, return to Main Menu (except Quit).

---

## Deferred Loading Pattern

This skill uses **progressive disclosure** to minimize context usage:

1. **Core skill loads**: ~150 lines (this file - routing logic only)
2. **On wizard mode**: Load `references/wizard-flow.md` (~250 lines)
3. **On menu selection**: Load only the selected reference (~100-150 lines)

### How to Load a Reference

When routing indicates to load a reference:
```
Read references/{file}.md
```
Then execute the workflow described in that file.

---

## Available References

| Reference | Purpose | Load When |
|-----------|---------|-----------|
| `wizard-flow.md` | First-run wizard steps 1-8 | mode=wizard or --wizard flag |
| `menu-maintenance.md` | Regenerate executor, cleanup | Menu option 1 |
| `menu-healthcheck.md` | Verify setup, diagnose issues | Menu option 2 |
| `menu-configuration.md` | Build systems, skill domains | Menu option 3 |
| `output-format.md` | TOON output standards | Reference for output formatting |
| `error-handling.md` | Error types and recovery | On error conditions |

---

## Error Handling

If an error occurs during execution:
```
Read references/error-handling.md
```
Apply the recovery guidance for the specific error type.

