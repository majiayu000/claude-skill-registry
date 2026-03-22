---
name: session-retention-debug
description: Diagnose and validate server session retention/reconnect behavior for TermLink. Use when checking session idle aging, retention TTL impact, active connection counts, and cleanup behavior via /api/sessions.
---

# Session Retention Debug

Use this skill to validate the server-side session retention requirement and observe lifecycle behavior.

Run commands from repository root:
`E:\coding\TermLink`

## Quick Start

1. Snapshot current sessions:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/session-retention-debug/scripts/inspect-sessions.ps1 -BaseUrl http://127.0.0.1:3000 -User admin -Pass admin
```

2. Monitor changes continuously:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/session-retention-debug/scripts/watch-sessions.ps1 -BaseUrl http://127.0.0.1:3000 -User admin -Pass admin -IntervalSec 10
```

## What It Verifies

1. `activeConnections` changes correctly when clients connect/disconnect.
2. Idle sessions are retained rather than immediately removed.
3. Session aging (`lastActiveAt`) can be observed over time for TTL validation.
4. Capacity pressure behavior can be observed by tracking total sessions.

## Rules

- Always target a specific environment via `-BaseUrl`.
- Use authenticated calls when `AUTH_ENABLED=true`.
- Do not infer retention from UI only; verify with `/api/sessions` snapshots.
