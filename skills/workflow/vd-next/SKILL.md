---
name: vd-next
description: Advance a VibeDev workflow from chat. Use when the user types `$vd-next` / says “vd next” and wants the agent to fetch the next compiled step prompt from the VibeDev MCP HTTP server (`vibedev-mcp serve`) and handle breakpoint/new-thread/diagnose states.
---

# `vd-next` (VibeDev Next Step Driver)

## Goal

Make “type `$vd-next` repeatedly” a reliable workflow:
- fetch the next step prompt from the VibeDev server
- respect `NEW_THREAD` / `AWAIT_HUMAN` / `DIAGNOSE`
- print the exact prompt to run next (with the server’s completion marker)

## How to run (scripted)

Run the bundled script:

- `python skills/vd-next/scripts/vd_next.py`

Common options:
- `--job-id <JOB_...>` (if omitted, picks the first `EXECUTING` job)
- `--server http://127.0.0.1:8765`
- `--json` (print raw JSON response)

## Expected loop

1. User calls `$vd-next`
2. Fetch next action from `/api/jobs/{job_id}/next-prompt-auto`
3. Output:
   - If `action=NEXT_STEP` or `RETRY`: print the prompt to execute
   - If `action=NEW_THREAD`: instruct user to start a new thread and print the seed prompt
   - If `action=AWAIT_HUMAN` or `DIAGNOSE`: stop and tell user what to do
4. After the step is done, the agent (or user) submits evidence via VibeDev tools / UI
5. Repeat

Notes:
- Breakpoints are implemented as a normal step that produces a Memory Pack and sets a `NEW_THREAD` flag for the following step.
- Memory Packs should be saved as context blocks tagged `carry_forward` (and optionally `carry_to_step:<step_id>`).

