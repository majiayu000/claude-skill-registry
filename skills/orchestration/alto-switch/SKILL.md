---
name: alto-switch
description: Use when switching ALTO orchestrator modes (dev/build/setup). Guides mode transitions and session management via the alto command.
---

# Mode Switching

The `alto` command handles mode switching and session management automatically.

## Commands

| Command | What it does |
|---------|--------------|
| `alto` | Resume current mode (sends "hi" if no message provided) |
| `alto dev` | Switch to dev mode and start Claude |
| `alto build` | Switch to build mode and start Claude |
| `alto setup` | Switch to setup mode and start Claude |

## Modes

| Mode | Purpose |
|------|---------|
| setup | Feature definition, configuration |
| build | Autonomous execution |
| dev | ALTO development |

## If User Is Already In Claude

They must exit first:
```
/exit
```

Then from terminal:
```
alto <mode>
```

The switch happens automatically - no need to manually edit files or restart.
