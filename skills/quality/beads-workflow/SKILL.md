---
name: beads-workflow
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when converting markdown plans into br beads with dependencies for implementation or swarm execution."
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Start | THE EXACT PROMPT | Polishing | br Commands | bd → br Migration | Quality Checklist | Troubleshooting | References -->

# Beads Workflow — From Plan to Actionable Tasks

> **Core Principle:** "Check your beads N times, implement once" — where N is as many as you can stomach.
>
> Beads are so detailed and polished that you can mechanically unleash a big swarm of agents to implement them, and it will come out just about perfectly.

## Quick Start

```bash
# 1. Initialize beads in project
br init

# 2. Convert plan to beads (see THE EXACT PROMPT below)

# 3. Polish iteratively
# Run polish prompt 6-9 times until steady-state

# 4. Validate
br dep cycles        # Must be empty
bv --robot-insights  # Check graph health

# 5. Begin implementation
bv --robot-next      # Get first bead
```

---

## THE EXACT PROMPT — Plan to Beads Conversion

```
OK so now read ALL of [YOUR_PLAN_FILE].md; please take ALL of that and elaborate on it and use it to create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.). The beads should be so detailed that we never need to consult back to the original markdown plan document. Remember to ONLY use the `br` tool to create and modify the beads and add the dependencies. Use ultrathink.
```

### Shorter Version

```
OK so please take ALL of that and elaborate on it more and then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.)  Use only the `br` tool to create and modify the beads and add the dependencies. Use ultrathink.
```

### What This Creates

- Tasks and subtasks with clear scope
- Dependency links (what blocks what)
- Detailed descriptions with background, reasoning, considerations
- Self-contained (never need to consult original plan)

---

## Polishing Beads

### THE EXACT PROMPT — Polish (Standard)

```
Reread AGENTS dot md so it's still fresh in your mind. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things!

DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY!

Also, make sure that as part of these beads, we include comprehensive unit tests and e2e test scripts with great, detailed logging so we can be sure that everything is working perfectly after implementation. Remember to ONLY use the `br` tool to create and modify the beads and to add the dependencies to beads. Use ultrathink.
```

### Polishing Protocol

1. Run polish prompt
2. Review changes
3. Repeat until steady-state (typically 6-9 rounds)
4. If it flatlines, start a fresh CC session
5. Optionally have Codex/GPT 5.5 do a final round

---

## Fresh Session Technique

If polishing flatlines, start a new Claude Code session:

### THE EXACT PROMPT — Re-establish Context

```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project.  Use ultrathink.
```

### THE EXACT PROMPT — Then Review Beads

```
We recently transformed a markdown plan file into a bunch of new beads. I want you to very carefully review and analyze these using `br` and `bv`.
```

Then follow up with the standard polish prompt.

---

## br Commands

### Issue Lifecycle

```bash
br init                              # Initialize workspace
br create "Title" -t feature -p 1    # Create bead
br update <id> --status in_progress
br close <id> --reason "Done"
br reopen <id>                       # If needed
```

### Dependencies

```bash
br dep add br-child br-parent        # child depends on parent
br dep remove br-child br-parent
br dep list <id>
br dep tree <id>
br dep cycles                        # MUST be empty!
```

### Querying

```bash
br list                              # All beads
br ready                             # Actionable (not blocked)
br blocked                           # Blocked beads
br search "authentication"
br list --json                       # Machine-readable
```

### Sync to Git

```bash
br sync --flush-only                 # Export DB → JSONL
git add .beads/ && git commit -m "Update beads"
```

---

## bd → br Migration (Docs)

Use this when you see legacy `bd` references in AGENTS.md or docs.

**Behavioral difference (only one):**
- **`br sync` never runs git commands**. After `br sync --flush-only`, you must `git add .beads/` and `git commit` (and `git push`) yourself.

**Transform checklist (order matters):**
1. `bd` commands → `br` commands
2. `bd sync` → `br sync --flush-only` + `git add .beads/` + `git commit`
3. Do NOT assume issue IDs must change `bd-*` → `br-*` — the prefix is configurable (often remains `bd-*`).
4. Remove daemon/auto-commit references

**Verify:**
```bash
grep -c '`bd ' file.md        # must be 0
grep -c 'bd sync' file.md     # must be 0
grep -c 'br sync --flush-only' file.md  # must be > 0
```

---

## BV Robot Mode

**CRITICAL:** Never run bare `bv` — it launches interactive TUI.

```bash
bv --robot-triage                    # Full triage
bv --robot-next                      # Single top pick
bv --robot-plan                      # Parallel execution tracks
bv --robot-insights | jq '.Cycles'   # Check for cycles
bv --robot-insights | jq '.bottlenecks'
```

---

## Quality Checklist

Before implementation, verify each bead:

- [ ] **Self-contained** — Understandable without external context
- [ ] **Clear scope** — One coherent piece of work
- [ ] **Dependencies explicit** — Links to blocking/blocked beads
- [ ] **Testable** — Clear success criteria
- [ ] **Includes tests** — Unit and e2e tests in scope
- [ ] **Preserves features** — Nothing from plan was lost
- [ ] **Not oversimplified** — Complexity preserved where needed
- [ ] **No cycles** — `br dep cycles` returns empty

---

## Integration with Agent Mail

Use bead ID as the coordination thread:

```python
# Reserve files for bead
file_reservation_paths(..., reason="br-123")

# Announce work in thread
send_message(..., thread_id="br-123", subject="[br-123] Starting...")

# Close bead when done
br close br-123 --reason "Completed"
release_file_reservations(...)
```

---

## When Beads Are Ready

Your beads are ready for implementation when:

1. **Steady-state reached** — Multiple polish rounds yield minimal changes
2. **Cross-model reviewed** — At least one alternative model reviewed
3. **No cycles** — `br dep cycles` returns empty
4. **Tests included** — Each feature has associated test beads
5. **Dependencies clean** — Graph makes logical sense

---

## References

| Topic | Reference |
|-------|-----------|
| All prompts | [PROMPTS.md](references/PROMPTS.md) |
| Bead structure | [BEAD-ANATOMY.md](references/BEAD-ANATOMY.md) |
| Troubleshooting | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
| br command reference | See br --help or beads_rust README |
| BV integration | See bv-graph-triage skill |

---

## Troubleshooting

### Worktree Error Fix

If you get `failed to create worktree: 'main' is already checked out`:

```bash
git branch beads-sync main
git push -u origin beads-sync
br config set sync-branch beads-sync
```

Always use a dedicated sync branch that you never check out directly.

### Quick Health Check

```bash
br config list        # All settings
br dep cycles         # Must be empty
which br              # Verify br is installed
```

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for full diagnostics.

---

## Validation

```bash
# Check for cycles (must be empty)
br dep cycles

# Check graph health
bv --robot-insights | jq '.Cycles'

# Verify all beads have descriptions
br list --json | jq '.issues[]? | select(.description == "")'
```
