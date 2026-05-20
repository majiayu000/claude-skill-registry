---
name: investigate
description: Guide diagnosis of a user-reported symptom — map to diagnostics, collect data, analyze
user-invocable: true
disable-model-invocation: false
argument-hint: "[symptom]"
---
The user is reporting a symptom or bug. Your job is to figure out what data is needed to diagnose it, guide the user to collect that data, then analyze the results.

## Step 1 — Understand the symptom

Read the user's description and classify into one or more categories:

| Category | Symptoms | Primary Diagnostics |
|----------|----------|-------------------|
| **Keyboard/input** | Lost keypresses, Alt-Tab not triggering, stuck overlay, wrong state | `EventLog`, `AltTabTooltips`, FlightRecorder |
| **Focus/activation** | Wrong window activated, activation fails, focus not set, window behind others | `WinEventLog`, `EventLog`, FlightRecorder |
| **Window list** | Missing windows, ghost windows, wrong order, stale titles | `StoreLog`, `ChurnLog`, FlightRecorder |
| **Workspace** | Wrong workspace detected, windows on wrong workspace, stale list after switch | `KomorebiLog`, `WinEventLog`, FlightRecorder |
| **Overlay/visual** | Flicker, wrong position, wrong size, rendering glitches, slow paint | `PaintTimingLog`, `AltTabTooltips`, FlightRecorder |
| **Icons/process** | Missing icons, wrong icons, missing process names | `IconPumpLog`, `ProcPumpLog`, `IPCLog` |
| **Startup/lifecycle** | Won't start, subprocess not launching, crash on startup | `LauncherLog`, `StoreLog` |
| **Config editor** | WebView2 issues, settings not saving, editor crash | `WebViewLog` |
| **Bypass mode** | Alt-Tab works in some apps but not others, game mode issues | `WinEventLog`, `EventLog`, FlightRecorder |

Multiple categories often overlap — a "wrong window activates" bug may need both focus and workspace diagnostics.

## Step 2 — Tell the user what to enable

Based on the classification, tell the user exactly what to do. Be specific — config key names, not vague instructions.

### Always recommend

- **FlightRecorder** — should already be enabled by default (`[Diagnostics] FlightRecorder=true`). Confirm with the user. If not enabled, this is the first thing to turn on.

### Category-specific diagnostics

Tell the user which keys to set in `config.ini` under `[Diagnostics]`:

```
; Example for a focus/activation issue:
[Diagnostics]
WinEventLog=true
EventLog=true
```

All logs write to `%TEMP%\` with `tabby_` prefix. Tell the user the exact log filenames they'll need to provide (from the table in `.claude/rules/debugging.md`).

### Reproduction instructions

Tell the user:
1. Enable the diagnostics listed above in `config.ini`
2. Restart Alt-Tabby (diagnostics are read at startup)
3. Reproduce the issue
4. **Immediately** press F12 (or their configured FlightRecorder hotkey) to capture a dump
5. Provide: the flight recorder dump from `release/recorder/` AND the relevant log files from `%TEMP%\`

If the issue is intermittent, tell the user to leave diagnostics enabled and capture a dump each time it occurs. Multiple dumps help with correlation.

## Step 3 — Analyze the data

When the user provides data:

### Flight recorder dumps
Use the analysis method from `/flight-recorder` — trace event chains, check global state, find broken sequences, timing gaps.

### Log files
Read the log files and correlate timestamps with the flight recorder dump. Look for:
- Events in the log that correspond to the symptom timeframe
- Error messages or unexpected states
- Patterns across multiple occurrences

### Cross-correlation
The power is in combining sources:
- FlightRecorder shows *what happened* (event sequence)
- WinEventLog shows *what Windows reported* (focus changes, window events)
- EventLog shows *what the keyboard hook saw* (key events, state transitions)
- KomorebiLog shows *what komorebi reported* (workspace changes, window moves)
- PaintTimingLog shows *how long rendering took*

Match timestamps across sources to build the full picture.

## Step 4 — Diagnose or escalate

If the cause is clear:
- Explain the root cause with evidence from the data
- Point to the relevant code (use query tools — `query_state.ps1` for state machine issues, `query_messages.ps1` for message handlers, `query_events.ps1 <code>` to look up event field meanings and emitter functions)
- Suggest whether this is a bug to fix or a known limitation

If the cause is unclear:
- Explain what you've ruled out
- Suggest additional diagnostics that might help
- Ask the user to reproduce with more verbose logging if available

## When the user provides no data yet

If the user just describes a symptom with no dumps or logs, go directly to Step 2 — tell them what to enable and how to reproduce. Don't speculate without data.
