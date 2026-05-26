---
name: aget-wake-up
description: Initialize AGET session with status briefing
allowed-tools:
  - Bash
  - Read
  - Glob
---

# aget-wake-up

Initialize an AGET agent session. This skill runs the wake-up protocol to display agent identity, version, fleet status, and session context.

## Instructions

When this skill is invoked:

1. Run the wake-up script:
   ```bash
   python3 scripts/wake_up.py
   ```

2. If the script succeeds, summarize the key information:
   - Agent name and version
   - Fleet status (if supervisor)
   - Active projects (if any in `planning/`)
   - Skills and Learnings counts

3. If the script fails or is not found, fall back to manual wake-up:
   - Read `.aget/version.json` for version info
   - Read `AGENTS.md` header for agent identity
   - Run `git status` for current state
   - Count Skills: `ls .claude/skills/ 2>/dev/null | wc -l`
   - Count Learnings: `ls .aget/evolution/L*.md 2>/dev/null | wc -l`

## Output Format

Present a concise briefing:
```
[Agent Name] v[version] ready
- Fleet: [N] agents (if supervisor)
- Location: [current directory]
- Git: [branch] ([clean/dirty])
- Skills: [N] | Learnings: [N]
- Active: [project name] (if any)
```

## Error Handling

- If `scripts/wake_up.py` returns exit code 1: Report validation warnings
- If `scripts/wake_up.py` returns exit code 2: Report configuration error
- If script missing: Use fallback method silently

## Related

- L532: Skills vs Learnings Distinction
- CAP-SESSION-001: Wake-Up Protocol
