---
name: review-race-conditions
description: Audit for race conditions in timers, hotkeys, callbacks, and shared state
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Systematically audit the codebase for race conditions. Use maximum parallelism — spawn explore agents for independent areas.

## AHK v2 Concurrency Model

AHK v2 is single-threaded but **not atomic** — timers, hotkeys, and callbacks CAN interrupt each other mid-execution. `Critical "On"` prevents interruption for the current thread. This is the only synchronization primitive available. See `.claude/rules/ahk-patterns.md` (Race Conditions section) and `.claude/rules/keyboard-hooks.md` for established patterns.

## What to Look For

### 1. Unguarded shared state mutations

Globals modified inside timer callbacks, hotkey handlers, or event callbacks without `Critical "On"`:
- Incrementing counters: `gRev += 1`
- Check-then-act: `if (!map.Has(k)) { map[k] := v }`
- Map/Array iteration while another callback could modify the collection
- State transitions (read-modify-write on `gGUI_State` or similar)

### 2. Critical section gaps

`Critical "On"` present but:
- `Critical "Off"` missing on an early `return` or `continue` path
- Critical released mid-operation (e.g., before rendering — this was tried and reverted, see `keyboard-hooks.md` "Do NOT Release Critical Before Rendering")
- Critical scope too narrow (protects the write but not the read that informed it)

### 3. Timer + hotkey interaction

A `SetTimer` callback modifying state that a hotkey handler also reads/writes. Both can fire in the same thread context. Use `query_timers.ps1` to inventory all timers and their callbacks, then cross-reference with hotkey handlers.

### 4. IPC message handling during state transitions

Named pipe reads processed via timer while the state machine is mid-transition. Check that IPC handlers either defer during transitions or are properly guarded.

### 5. Producer callbacks during GUI operations

Producers (WinEventHook, Komorebi subscription) firing callbacks that modify `gGUI_LiveItems`, window store data, or MRU order while the GUI is painting or the state machine is processing input.

## Known Safe Patterns (Do NOT Flag)

These have been deliberately designed and tested — flagging them wastes time:

- `Critical "On"` held through the entire `GUI_OnInterceptorEvent` handler including rendering (~16ms). This is intentional — releasing early causes corruption.
- `SendMode("Event")` instead of `SendInput` — prevents hook uninstall during sends.
- Async activation with `gGUI_EventBuffer` — events buffered while `gGUI_Pending.phase != ""`.
- Lost Tab synthesis (`ALT_DN` + `ALT_UP` without `TAB`).
- Flight recorder `FR_Record()` — pre-allocated ring buffer, writes are inherently safe.
- `_GUI_LogError()` — always-on by design.

## Explore Strategy

Split by concurrency boundary, not just file location:

- **Hotkey handlers** — `gui_input.ahk`, `gui_interceptor.ahk`: all `INT_*` functions
- **Timer callbacks** — use `query_timers.ps1` to find all `SetTimer` targets, then read each callback
- **Windows message handlers** — use `query_messages.ps1` to map WM_ handlers and senders (interrupt sources)
- **WinEvent callbacks** — `winevent_hook.ahk`: `_WEH_*` callback functions
- **Komorebi callbacks** — `komorebi_sub.ahk`, `komorebi_lite.ahk`: subscription event handlers
- **IPC handlers** — `ipc_pipe.ahk`, pump files: pipe read/write paths
- **State machine** — use `query_state.ps1` to extract specific branches from `GUI_OnInterceptorEvent` without loading the full function
- **Call graph** — use `query_function_visibility.ps1` to map which interrupt sources can reach vulnerable code (e.g., "is this function called from both timer callbacks and hotkey handlers?")
- **Mutation detail** — use `query_mutations.ps1 <globalName>` to see per-function mutation sites with assignment operators and assigned values — reveals unguarded writes without reading full files

## Validation

After explore agents report back, **validate every finding yourself**. Race conditions are easy to hypothesize and hard to confirm. Many "races" identified by exploration are actually guarded by Critical sections or by AHK's threading model (only one pseudo-thread runs at a time; interruption only happens at specific yield points).

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with actual code quoted. Vague line references are not sufficient.
2. **Trace the interrupt path**: Which specific callback could interrupt this code? Is it a timer, hotkey, or WinEvent? At what point in the vulnerable code would the interruption occur?
3. **Counter-argument**: "What would make this race impossible?" — Is there a Critical section in a caller? Does AHK's threading model prevent this specific interleaving? Is the state only accessed from one callback type?
4. **Observed vs inferred**: State whether you saw unguarded concurrent access directly, or inferred it from code structure. Inferred races need stronger evidence.
5. **Reproducibility**: Can this race actually manifest in normal usage, or only under extreme timing? A theoretical race in a once-per-session init path is lower priority than one in a per-keystroke hot path.

## Plan Format

Group by severity (data corruption > logic error > cosmetic):

| File | Lines | Race Description | Interrupt Source | Severity | Fix |
|------|-------|-----------------|-----------------|----------|-----|
| `file.ahk` | 42–58 | `gFoo` read-then-write without Critical | Timer `_HeartbeatTick` | Data corruption | Wrap in `Critical "On"` / `Critical "Off"` |

For each fix, note:
- Whether it introduces new Critical section duration that could affect input latency
- Whether the fix is localized or requires coordinating changes across files

Ignore any existing plans — create a fresh one.
