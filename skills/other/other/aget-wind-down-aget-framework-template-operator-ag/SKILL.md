---
name: aget-wind-down
description: End AGET session with state capture and sanity checks
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# aget-wind-down

End an AGET agent session properly. This skill runs the wind-down protocol to capture session state, run sanity checks, and prepare handoff notes.

## Instructions

When this skill is invoked:

1. Run the wind-down script:
   ```bash
   python3 scripts/wind_down.py
   ```

2. The script will:
   - Run sanity checks (housekeeping protocol)
   - Capture session duration and activity
   - Scan for pending work in `planning/`
   - Generate session summary
   - Suggest commit message if changes exist

3. If user provides notes, pass them to the script:
   ```bash
   python3 scripts/wind_down.py --notes "User provided notes here"
   ```

4. If re-entrancy guard blocks (exit code 4), inform user:
   - Wind-down was run recently (5-minute cooldown)
   - Use `--force` to bypass if needed

## Output Format

Present the wind-down summary:
```
Wind Down Complete
- Session: [duration]
- Sanity: [healthy/warnings/errors]
- Pending: [N] items in planning/
- Changes: [staged/unstaged counts]
- Suggested commit: "[message]"
```

## Error Handling

- Exit code 0: Clean close, sanity healthy
- Exit code 1: Close with warnings (report them)
- Exit code 2: Close with errors (require acknowledgment)
- Exit code 3: Configuration error
- Exit code 4: Re-entrancy guard active

## Options

- `--skip-sanity`: Skip sanity check (not recommended)
- `--force`: Bypass re-entrancy guard (L468)
- `--json`: Machine-readable output

## Related

- L468: Re-entrancy Protection
- L532: Skills vs Learnings Distinction
- CAP-SESSION-003: Wind Down Protocol
