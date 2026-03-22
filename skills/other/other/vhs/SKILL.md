---
name: vhs
description: Terminal recording and animated GIF generation using VHS for TUI application demos and QA evidence
category: DevOps Operations
---

# Skill: vhs

## What I do

I provide VHS terminal recording expertise: first-run bypass patterns, database seeding, and reproducible demo environments for TUI/CLI applications.

## When to use me

- Creating visual demos for features or bug fixes
- Automating TUI behaviour verification via BDD tests
- Producing QA evidence (bug proof, fix proof, demos)
- Troubleshooting timing-related UI issues

## Core principles

1. **Deterministic** — Temporary databases and isolated configs for reproducible results
2. **Visual Pacing** — Use `Sleep` so viewers can follow the logic
3. **Consistent Presentation** — Standard terminal dimensions (1200x600) and theme

## Patterns & examples

### First-Run Bypass Pattern (CRITICAL)

TUI apps with onboarding wizards need a pre-configured environment.

**Setup script** (`demos/setup-{workflow}-demo.sh`):
```bash
#!/bin/bash
set -e
FAKE_HOME="$(pwd)/demos/temp_demo_env"
rm -rf "$FAKE_HOME"
mkdir -p "$FAKE_HOME/.your-app"

# Create config (bypasses first-run)
cat <<EOF > "$FAKE_HOME/.your-app/config.yaml"
initialised: true
EOF

# Seed database
sqlite3 "$FAKE_HOME/.your-app/data.db" <<'SQLEOF'
CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO items (name) VALUES ('Demo Item');
SQLEOF
```

**Tape file pattern**:
```vhs
# ✅ Correct: Hidden setup + HOME override
Output demos/vhs/generated/{workflow}/{name}.gif
Set Shell "bash"
Set FontSize 14
Set Width 1200
Set Height 600
Set Theme "Catppuccin Mocha"

Hide
Type "./demos/setup-{workflow}-demo.sh"
Enter
Sleep 1s
Type "clear"
Enter
Sleep 300ms
Show

Type "export HOME=$(pwd)/demos/temp_demo_env && ./your-app [flags]"
Enter
Sleep 3s
# ... workflow steps ...
Ctrl+C
Sleep 500ms
```

**Wrong pattern**:
```vhs
# ❌ Wrong: No config — triggers first-run wizard
Type "./your-app"
Enter
```

### VHS Tape Syntax Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `Output` | Set output file | `Output demos/feature.gif` |
| `Set` | Configure terminal | `Set FontSize 14` |
| `Type` | Simulate typing | `Type "ls -la"` |
| `Enter` | Press Enter key | `Enter` |
| `Key` | Press any key | `Key Tab`, `Key Escape` |
| `Sleep` | Pause execution | `Sleep 500ms`, `Sleep 2s` |
| `Hide`/`Show` | Hide setup commands | Wrap setup in Hide block |
| `Source` | Include another tape | `Source config.tape` |

### Directory Structure

```
demos/
├── setup-*.sh              # Setup scripts per workflow
├── temp_demo_env/          # Fake HOME (gitignored)
└── vhs/
    ├── features/{workflow}/
    │   ├── config.tape     # Shared settings
    │   ├── happy-path.tape
    │   └── sad-path.tape
    └── generated/{workflow}/*.gif
```

## Timing Guidelines

| Action | Delay |
|--------|-------|
| After app launch | `Sleep 3s` |
| Between key presses | `Sleep 500ms` |
| After significant actions | `Sleep 2s` |
| After clearing screen | `Sleep 300ms` |

## Common Issues and Fixes

| Issue | Cause | Solution |
|-------|-------|----------|
| **Onboarding wizard appears** | No config in fake HOME | Create complete config file in setup script |
| **Database not found** | Wrong DB path | Use explicit `--db` flag or ensure path matches |
| **No data displayed** | Empty database | Seed database in setup script |
| **Tape hangs** | Missing Enter | Add `Enter` after every `Type` command |
| **Form won't submit** | Wrong button focus | Navigate to confirm: `Key Left` then `Enter` |
| **UI not rendering** | Insufficient delay | Increase `Sleep` after launch and transitions |
| **Dropdown fails** | Fragile navigation | Use `/` to search instead of counting `Down` |

## Anti-patterns to avoid

- ❌ **No setup script** — Running app directly triggers first-run wizard
- ❌ **Hardcoded paths** — Use `$(pwd)` for portable paths
- ❌ **Visible setup** — Always wrap setup commands in `Hide`/`Show`
- ❌ **Missing HOME override** — App uses real config instead of demo config
- ❌ **Arbitrary sleeps** — Use consistent timing guidelines for predictability
- ❌ **No database seeding** — Empty state confuses demo viewers

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/VHS.md`

## Related skills

- `bubble-tea-expert` — Understanding the underlying TUI framework
- `bdd-workflow` — Using VHS for automated acceptance testing
- `ui-design` — Evaluating the visual clarity of recorded interactions
- `british-english` — Ensuring all demo text follows spelling standards
