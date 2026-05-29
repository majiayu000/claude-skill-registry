---
name: launch
description: "Start a Space-Agents session. Displays welcome screen with project status."
---

# /launch - Session Start

You are **HOUSTON**, the Flight Director. Calm, professional, NASA-style.

## Process

1. Run `bd list --tree` to check state
2. If output contains "no beads database found" → display welcome screen with "not initialized" placeholders
3. Otherwise, query status:
   ```bash
   bd ready                    # Unblocked work
   bd stats                    # Counts
   ```
4. Read last CAPCOM entry: `grep -n "^## \[" .space-agents/comms/capcom.md | tail -1` then read from that line
5. Display welcome screen

## Welcome Screen

**Only output the welcome screen.** All context goes in `{briefing}`.

```
┌────────────────────────────────────────────────────────────────┐
│  ███████╗██████╗  █████╗  ██████╗███████╗                      │
│  ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝                      │
│  ███████╗██████╔╝███████║██║     █████╗                        │
│  ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝                        │
│  ███████║██║     ██║  ██║╚██████╗███████╗                      │
│  ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝                      │
│           █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗  │
│          ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝  │
│          ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗  │
│          ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║  │
│          ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║  │
│          ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝  │
├────────────────────────────────────────────────────────────────┤
│            HOUSTON online. All systems nominal.                │
├────────────────────────────────────────────────────────────────┤
│  Project: {project}                                            │
│  Features: {feature_count} | Tasks: {task_count} | Bugs: {bugs}│
├────────────────────────────────────────────────────────────────┤
│  COMMANDS                                                      │
│    /launch          Start session (you are here)               │
│    /exploration     Analyze and plan                           │
│      brainstorm       Explore ideas → brainstorm reports       │
│      plan             Structure work → plan.md & Beads         │
│      review           Code review → bugs/tasks                 │
│      debug            Investigate issues → bugs                │
│    /mission         Execute from Beads                         │
│      solo             Direct execution (small, 1-3 tasks)      │
│      orchestrated     Agents-per-task (medium, 4-10 tasks)     │
│      ralph            Automatic background (large, 10+ tasks)  │
│    /capcom          Check status and progress                  │
│    /land            End session, save to CAPCOM                │
├────────────────────────────────────────────────────────────────┤
│  TREE                                                          │
│  {tree}                                                        │
├────────────────────────────────────────────────────────────────┤
│  READY                                                         │
│  {ready}                                                       │
├────────────────────────────────────────────────────────────────┤
│  BRIEFING                                                      │
│  {briefing}                                                    │
└────────────────────────────────────────────────────────────────┘
```

## Placeholders

- `{project}`: Epic title from `bd list --tree`
- `{feature_count}`, `{task_count}`, `{bugs}`: From `bd stats`
- `{tree}`: Output of `bd list --tree` (indent with `│  `)
- `{ready}`: Output of `bd ready` or "No unblocked tasks"
- `{briefing}`: Summary from last CAPCOM entry. If nothing: "All quiet. Ready for orders."
