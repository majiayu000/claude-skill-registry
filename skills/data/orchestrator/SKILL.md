---
name: orchestrator
description: Plan and coordinate multi-agent bead execution. Use when starting a new epic, assigning tracks to agents, or monitoring parallel work progress.
---

# Orchestrator Skill: Autonomous Multi-Agent Coordination

This skill spawns and monitors parallel worker agents that execute beads autonomously.

**Prerequisite**: Run the `planning` skill first to generate `history/<feature>/execution-plan.md`.

## Architecture (Mode B: Autonomous)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ORCHESTRATOR                                   │
│                              (This Agent)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Read execution-plan.md (from planning skill)                            │
│  2. Initialize Agent Mail                                                   │
│  3. Spawn worker subagents via Task tool                                    │
│  4. Monitor progress via Agent Mail                                         │
│  5. Handle cross-track blockers                                             │
│  6. Announce completion                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │ Task tool spawns parallel workers
           ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  BlueLake        │  │  GreenCastle     │  │  RedStone        │
│  Track 1         │  │  Track 2         │  │  Track 3         │
│  [a → b → c]     │  │  [x → y]         │  │  [m → n → o]     │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│  For each bead:  │  │  For each bead:  │  │  For each bead:  │
│  • Reserve files │  │  • Reserve files │  │  • Reserve files │
│  • Do work       │  │  • Do work       │  │  • Do work       │
│  • Report mail   │  │  • Report mail   │  │  • Report mail   │
│  • Next bead     │  │  • Next bead     │  │  • Next bead     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │     Agent Mail      │
                    │  ─────────────────  │
                    │  Epic Thread:       │
                    │  • Progress reports │
                    │  • Bead completions │
                    │  • Blockers         │
                    │                     │
                    │  Track Threads:     │
                    │  • Bead context     │
                    │  • Learnings        │
                    └─────────────────────┘
```

---

## Phase 1: Read Execution Plan

Use the **Read** tool to load the execution plan:

- **path**: `history/<feature>/execution-plan.md`

Extract:

- `EPIC_ID` - the epic bead id
- `TRACKS` - array of {agent_name, beads[], file_scope}
- `CROSS_DEPS` - any cross-track dependencies

---

## Phase 2: Initialize Agent Mail

### Step 1: Ensure project exists

**Tool**: `mcp__mcp_agent_mail__ensure_project`

| Parameter   | Value                     |
| ----------- | ------------------------- |
| `human_key` | `<absolute-project-path>` |

### Step 2: Register orchestrator identity

**Tool**: `mcp__mcp_agent_mail__register_agent`

| Parameter          | Value                                 |
| ------------------ | ------------------------------------- |
| `project_key`      | `<absolute-project-path>`             |
| `name`             | `<OrchestratorName>` (e.g. `GoldFox`) |
| `program`          | `amp`                                 |
| `model`            | `<model>`                             |
| `task_description` | `Orchestrator for <epic-id>`          |

---

## Phase 3: Spawn Worker Subagents

**Spawn all workers in parallel using the Task tool.**

For each track, invoke:

**Tool**: `Task`

| Parameter     | Value                                         |
| ------------- | --------------------------------------------- |
| `description` | `Worker <AgentName>: Track N - <description>` |
| `prompt`      | See `reference/worker-template.md`            |

### Example Task prompt for Track 1

```
You are agent BlueLake working on Track 1 of epic bd-42.

## Setup
1. Read /path/to/project/AGENTS.md for tool preferences
2. Load the worker skill: skill worker

## Your Track
Beads to complete IN ORDER: bd-43, bd-44, bd-45
File scope: packages/sdk/**

## Protocol for EACH bead:

### Start Bead
1. mcp__mcp_agent_mail__register_agent with name="BlueLake", task_description="<bead-id>"
2. mcp__mcp_agent_mail__summarize_thread with thread_id="track:BlueLake:bd-42"
3. mcp__mcp_agent_mail__file_reservation_paths with paths=["packages/sdk/**"], reason="<bead-id>"
4. Run: bd update <bead-id> --status in_progress

### Work on Bead
- Use preferred tools from AGENTS.md (gkg for exploration, morph for edits)
- Check inbox periodically with mcp__mcp_agent_mail__fetch_inbox

### Complete Bead
1. Run: bd close <bead-id> --reason "Summary of work"
2. mcp__mcp_agent_mail__send_message:
   - to: ["GoldFox"]
   - thread_id: "bd-42"
   - subject: "[<bead-id>] COMPLETE"
   - body_md: "Done: <summary>. Next: <next-bead-id>"
3. mcp__mcp_agent_mail__send_message (context for next bead):
   - to: ["BlueLake"]
   - thread_id: "track:BlueLake:bd-42"
   - subject: "<bead-id> Complete - Context for next"
   - body_md: "## Learnings\n- ...\n## Gotchas\n- ..."
4. mcp__mcp_agent_mail__release_file_reservations

### Continue to Next Bead
- Loop back to "Start Bead" with next bead in track
- Read your track thread for context from previous bead

## When Track Complete
mcp__mcp_agent_mail__send_message:
- to: ["GoldFox"]
- thread_id: "bd-42"
- subject: "[Track 1] COMPLETE"
- body_md: "All beads done. Summary: ..."

Return a summary of all work completed.
```

---

## Phase 4: Monitor Progress

While workers execute, monitor via Agent Mail.

### Check Epic Thread for Updates

**Tool**: `mcp__mcp_agent_mail__search_messages`

| Parameter     | Value       |
| ------------- | ----------- |
| `project_key` | `<path>`    |
| `query`       | `<epic-id>` |
| `limit`       | `20`        |

### Check for Blockers

**Tool**: `mcp__mcp_agent_mail__fetch_inbox`

| Parameter        | Value                |
| ---------------- | -------------------- |
| `project_key`    | `<path>`             |
| `agent_name`     | `<OrchestratorName>` |
| `urgent_only`    | `true`               |
| `include_bodies` | `true`               |

### Check Bead Status

```bash
bv --robot-triage --graph-root <epic-id> 2>/dev/null | jq '.quick_ref'
```

---

## Phase 5: Handle Cross-Track Issues

### If Worker Reports Blocker

**Tool**: `mcp__mcp_agent_mail__reply_message`

| Parameter     | Value                |
| ------------- | -------------------- |
| `project_key` | `<path>`             |
| `message_id`  | `<blocker-msg-id>`   |
| `sender_name` | `<OrchestratorName>` |
| `body_md`     | `Resolution: ...`    |

### If File Conflict

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter     | Value                                      |
| ------------- | ------------------------------------------ |
| `project_key` | `<path>`                                   |
| `sender_name` | `<OrchestratorName>`                       |
| `to`          | `["<HolderAgent>"]`                        |
| `thread_id`   | `<epic-id>`                                |
| `subject`     | `File conflict resolution`                 |
| `body_md`     | `<Worker> needs <files>. Can you release?` |

---

## Phase 6: Epic Completion

When all workers report track complete:

### Verify All Done

```bash
bv --robot-triage --graph-root <epic-id> 2>/dev/null | jq '.quick_ref.open_count'
# Should be 0
```

### Send Completion Summary

**Tool**: `mcp__mcp_agent_mail__send_message`

| Parameter     | Value                                     |
| ------------- | ----------------------------------------- |
| `project_key` | `<path>`                                  |
| `sender_name` | `<OrchestratorName>`                      |
| `to`          | `["BlueLake", "GreenCastle", "RedStone"]` |
| `thread_id`   | `<epic-id>`                               |
| `subject`     | `[<epic-id>] EPIC COMPLETE`               |
| `body_md`     | See template below                        |

```markdown
## Epic Complete: <title>

### Track Summaries

- Track 1 (BlueLake): <summary>
- Track 2 (GreenCastle): <summary>
- Track 3 (RedStone): <summary>

### Deliverables

- <what was built>

### Learnings

- <key insights>
```

### Close Epic

```bash
bd close <epic-id> --reason "All tracks complete"
```

---

## Quick Reference

| Phase      | Tool / Command                                                               |
| ---------- | ---------------------------------------------------------------------------- |
| Read Plan  | `Read` tool → `history/<feature>/execution-plan.md`                          |
| Initialize | `mcp__mcp_agent_mail__ensure_project`, `mcp__mcp_agent_mail__register_agent` |
| Spawn      | `Task` tool for each track (parallel)                                        |
| Monitor    | `mcp__mcp_agent_mail__fetch_inbox`, `mcp__mcp_agent_mail__search_messages`   |
| Resolve    | `mcp__mcp_agent_mail__reply_message` for blockers                            |
| Complete   | Verify all done, send summary, `bd close`                                    |

---

## Additional Resources

- **Worker Prompt Template**: See `reference/worker-template.md` for the full template with variable substitution
