---
name: summon
description: Launch AutoMates agents in separate terminal windows with their identities
allowed-tools:
  - Bash
  - Read
---

# /summon - Launch AutoMates Agents

Launch one or more agents in separate terminal windows with their identities, knowledge sections, and startup instructions.

## Usage

```
/summon <agent>              # Launch single agent
/summon <agent1>,<agent2>    # Launch multiple agents
/summon team                 # Launch Planner, Builder, Checker
/summon all                  # Launch all 9 agents
```

## Available Agents

| Agent | Color | Role |
|-------|-------|------|
| planner | Blue | Creates blueprints and roadmaps |
| builder | Orange | Writes code, implements features |
| checker | Green | Reviews code, finds bugs, security |
| brainstorm | Yellow | Generates ideas, explores solutions |
| gal | Teal | Tests UX, skeptical evaluation |
| legal | Deep Slate | Licensing, privacy, compliance |
| gitdude | Violet | Commits, versioning, releases |
| fetcher | Caramel | Gathers documentation, research |
| orca | Charcoal | Designs agent workflows |
| daisy | Pink | Branding, social media, PR, pitches |

## Instructions

When this skill is invoked, execute the summon script:

```bash
AUTOMATES_ROOT="$(pwd)"

# Check if we're in the AutoMates project
if [[ ! -d "${AUTOMATES_ROOT}/AgenTeam" ]]; then
    echo "Error: Not in the AutoMates project (no AgenTeam/ folder found)"
    exit 1
fi

bash "${AUTOMATES_ROOT}/.claude/skills/summon/summon.sh" "$ARGUMENTS"
```

## What Happens

1. A new terminal window/tab opens for each agent
2. Claude Code starts with that agent's identity loaded via `--append-system-prompt`
3. The agent reads their memory, dashboard, and knowledge section
4. Agents share files via `Dashboard/Work_Space/`

## Cross-Platform Support

| Platform | Primary | Fallback |
|----------|---------|----------|
| macOS | iTerm2 | Terminal.app |
| Linux | gnome-terminal | xterm |
| Windows | Windows Terminal | PowerShell |

## Notes

- Each agent runs as a separate Claude Code instance
- Agents have persistent memory in `AgenTeam/<name>/Memory_Logs/`
- Fetcher's memory is in `Library/Fetcher/Memory_Logs/`
- CLAUDE.md is automatically loaded in every session (shared context)
- Coordinate work through shared files in `Dashboard/Work_Space/`

---
*Part of AutoMates.AI — Your AI dev team*
