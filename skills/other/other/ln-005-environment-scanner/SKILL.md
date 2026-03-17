---
name: ln-005-environment-scanner
description: "Probes CLI agents (Codex, Gemini) and writes docs/environment_state.json — agent availability config for Phase 0"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Environment Scanner (Standalone Utility)

**Type:** Standalone Utility
**Category:** 0XX Shared

Probes CLI agents (Codex, Gemini) and writes `docs/environment_state.json`. Skills read this file to check `disabled` flags before live-probing agents.

---

## When to Use This Skill

- First-time project setup (no `docs/environment_state.json` yet)
- After installing/removing CLI agents (Codex, Gemini)
- After `ln-004-agent-config-sync` (sync may change agent availability)
- When a skill reports unexpected agent unavailability

---

## Output File

`docs/environment_state.json` — validated against `references/environment_state_schema.json`.

```json
{
  "$schema": "environment_state_v1",
  "scanned_at": "2026-03-08T14:30:00Z",
  "agents": {
    "codex": { "available": true, "version": "0.1.2503" },
    "gemini": { "available": false, "detail": "Command not found in PATH" }
  }
}
```

### User Override

Users can add `"disabled": true` to any agent entry to opt out without losing detection state:

```json
"codex": { "available": true, "disabled": true, "version": "0.1.2503" }
```

Scanner preserves `disabled` field on rescan — it overwrites `available`, `detail`, `version` but never touches `disabled`.

**How skills use this:** Before running `--health-check`, skills read this file. If `disabled: true` → agent is skipped immediately (no probe). If `disabled: false` or absent → live health-check runs.

---

## Workflow

```
Probe Agents → Write JSON → Summary
```

### Phase 1: Probe CLI Agents

Single call to `agent_runner.py --health-check` probes all registered agents:

```bash
python shared/agents/agent_runner.py --health-check
```

**Path resolution:** `shared/agents/agent_runner.py` is relative to skills repo root. Locate via this SKILL.md directory → parent.

**Parse output** (JSON with per-agent status):

| Agent | Registry Key | State Fields |
|-------|-------------|--------------|
| Codex | `codex` (checks `codex --version`) | `available`, `version` (first line of version output) |
| Gemini | `gemini` (checks `gemini --version`) | `available`, `version` (first line of version output) |

**If `agent_runner.py` not found or errors:** Set both agents to `available: false`, `detail: "agent_runner.py not available"`.

### Phase 1.5: Hook Health Check

**MANDATORY READ:** Load `shared/references/hook_health_check.md`

Validate hooks configuration: JSON syntax, script existence, dependency availability. Append results to `docs/environment_state.json` under `hooks` key:

```json
"hooks": {
  "status": "ok",
  "events": 3,
  "scripts_found": "3/3",
  "dependencies": { "python3": "3.12.0" }
}
```

If hooks.json not found: `"hooks": { "status": "not_configured" }`.

### Phase 2: Write JSON

1. **Read existing state** (if `docs/environment_state.json` exists):
   - Preserve `disabled` fields from existing entries
   - Preserve any user-added custom fields
2. **Build new state:**
   - `$schema`: `"environment_state_v1"`
   - `scanned_at`: current ISO 8601 timestamp
   - `agents`: merge probe results (new `available`/`detail`/`version`) with preserved `disabled` flags
3. **Ensure `docs/` directory exists** (create if missing)
4. **Write** `docs/environment_state.json` with 2-space indentation
5. **Validate** written file against `references/environment_state_schema.json` structure (key presence check)

### Phase 3: Summary Report

Display results as a table:

```
Environment Scan Complete:
| Agent  | Status      | Detail                    |
|--------|-------------|---------------------------|
| Codex  | available   | 0.1.2503                  |
| Gemini | unavailable | Command not found in PATH |

State written to: docs/environment_state.json
```

If any agent has `disabled: true`, show status as `disabled` (not available/unavailable).

---

## Critical Rules

1. **Probe all agents.** This skill always probes ALL agents, regardless of existing state. It is the full rescan.
2. **Preserve `disabled`.** Never overwrite user's `disabled: true` flags. Detection state updates, user preference stays.
3. **No side effects.** This skill only writes `docs/environment_state.json`. No other files modified.
4. **Fail gracefully.** Each probe is independent. One failure = one `available: false` entry, scan continues.
5. **No TTL.** State file has no expiration. It is refreshed only by running this skill.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Skip probes for "known" agents | Always probe all agents — this is a full scan |
| Delete `disabled` flags on rescan | Merge: overwrite detection fields, preserve `disabled` |
| Retry failed probes | One attempt per agent. Failure = `available: false` |
| Probe MCP tools or platform | Only probe CLI agents (Codex, Gemini). MCP tools configured elsewhere |
| Add TTL or cache expiry logic | State is manual-refresh only |

---

## Definition of Done

- [ ] Both agents probed (Codex, Gemini)
- [ ] Hook health check completed (hooks.json, scripts, dependencies)
- [ ] `docs/environment_state.json` written with valid structure (agents + hooks)
- [ ] Existing `disabled` flags preserved across rescan
- [ ] Summary table displayed to user

---
**Version:** 2.0.0
**Last Updated:** 2026-03-08
