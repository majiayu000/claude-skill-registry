---
name: flight-recorder
description: Analyze flight recorder dumps to diagnose bugs from event traces
user-invocable: true
disable-model-invocation: true
argument-hint: "[dump file or bug description]"
---
Analyze flight recorder dump(s) to diagnose a bug or anomaly. The user may describe the bug, specify files, or both. If invoked with no arguments, load the newest dump and use the USER NOTE in the dump as the bug description.

## File Resolution

1. **No argument**: Use `release/recorder/`, pick the newest `fr_*.txt` by modification time. The USER NOTE inside the dump describes what happened.
2. **Count** (e.g., "last 3", "3 newest"): Load that many newest dumps from `release/recorder/`
3. **"today"** or **"all from today"**: All `fr_*.txt` files from today in `release/recorder/`
4. **Exact filename**: Search `release/recorder/` for a matching file
5. **Full path**: Use as-is

Use `ls -t release/recorder/fr_*.txt` to find files. Confirm resolved file(s) to the user before analyzing.

## Dump Structure

Each dump has four sections:

1. **USER NOTE** — The user's description of what they observed (entered at dump time via InputBox). This is your primary bug description when no argument is provided.
2. **GLOBAL STATE** — Snapshot of GUI state, interceptor flags, overlay visibility, workspace, foreground window at dump time.
3. **WINDOW LIST STATE** — Store revision, dirty flags, queue lengths.
4. **LIVE ITEMS** — Current window list with hwnd, title, process, workspace, current-workspace flag.
5. **EVENT TRACE** — Chronological events (newest first), with `T-SSSSSS.mmm` offsets relative to dump time.

## Analysis Method

### Step 1 — Understand the bug

Read the USER NOTE and any user-provided description. Form a hypothesis about what category of bug this is:
- **Keyboard/input**: Lost keypress, wrong state transition, stuck state
- **Activation**: Wrong window activated, activation failed, focus not set
- **Workspace**: Wrong workspace detected, stale MRU after switch, wrong window list
- **Data**: Ghost windows, missing windows, stale titles/icons
- **Timing**: Race condition, suppression window too short/long, events out of order

### Step 2 — Check global state for immediate red flags

- Is GUI State consistent with what should be happening? (e.g., `ALT_PENDING` with `gINT_AltIsDown=0` is suspicious)
- Is `gINT_BypassMode=1` when it shouldn't be?
- Is `gGUI_PendingPhase` non-empty (stuck async activation)?
- Does the foreground window match what the user expected?

### Step 3 — Trace the event chain

Use `query_state.ps1` to extract the expected state machine branches for comparison with the event trace. Use `query_messages.ps1` to identify WM_ message handlers/senders when Windows messages appear in the trace.

Read the event trace bottom-to-top (chronological order). Look for:

**Complete sequences** — A normal Alt-Tab is:
```
ALT_DN → TAB_DN → TAB_DECIDE → TAB_DECIDE_INNER(isAltTab=1) → STATE→ACTIVE → FREEZE → ALT_UP → QUICK_SWITCH → ACTIVATE_START → ACTIVATE_RESULT(success=1) → MRU_UPDATE → STATE→IDLE
```

**Broken sequences** — Where does the chain deviate? Common patterns:
- `ALT_DN` + `ALT_UP` with no `TAB_DN` = Tab was lost (check BYPASS mode)
- `ACTIVATE_RESULT(success=0)` = Windows rejected activation (check `fg` field)
- `ACTIVATE_GONE` = Window disappeared between selection and activation
- `FOCUS_SUPPRESS` during an Alt-Tab = MRU suppression interfered
- `WS_SWITCH` during an Alt-Tab = workspace changed mid-session
- Large time gap between events = something blocked the main thread

**Timing analysis** — Calculate gaps between related events. Flag any gap > 50ms between keyboard events or > 100ms between state transitions.

**Correlation with live items** — Cross-reference hwnds in events with the LIVE ITEMS list. Are referenced windows still present? On the expected workspace?

### Step 4 — Multi-dump correlation (when multiple files)

When analyzing multiple dumps for the same bug:
- Are the same events present/missing across dumps?
- Is the same window/process always involved?
- Do the bugs correlate with workspace switches or specific workspace names?
- Is there a timing pattern (time of day, interval between dumps)?

## Event Reference

Use `query_events.ps1 <name_or_code>` for structured event lookups — shows field meanings (d1-d4) and emitter functions. Use `query_events.ps1` with no args for the full index. See `docs/USING_RECORDER.md` for analysis patterns and worked examples.

## Reporting

Present findings as:

1. **Bug description**: What the user reported (from NOTE or argument)
2. **Root cause** (or top hypotheses if uncertain): What the event trace shows
3. **Evidence chain**: Quote specific events with timestamps showing the problem
4. **State at dump time**: Any inconsistencies in the global state snapshot
5. **Affected window(s)**: hwnd, title, process — from live items cross-referenced with events

If the cause is clear, suggest where in the code to look (reference the event type to its handler using the architecture knowledge). If uncertain, describe what additional information would help (e.g., "need a dump with DiagEventLog enabled to see the full WinEvent stream").
