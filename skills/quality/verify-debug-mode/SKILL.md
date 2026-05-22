---
name: verify-debug-mode
description: Confirm a requested feature change via AERA Debug mode (Debug view, console, logs). Use when validation must happen through Debug UI or when you need to add debug-only probes/commands to make a change observable.
---

# Verify via Debug Mode

## Intent

- Confirm the change works using Debug mode surfaces.
- Add debug-only probes/commands when existing Debug tools cannot observe the change.
- Always run Debug-mode verification after implementing any feature change or addition.

## Workflow

1) Define the acceptance signal
- State the exact value, log line, or UI output that proves the change works.
- Prefer a single requestId or timestamp you can filter in logs.

2) Enable Debug mode
- Set localStorage keys (`thelab.debugMode=1`, `thelab.activeView=DEBUG`) and reload.
- Open the Debug Console view (Debug & Diagnostics).

3) Use existing Debug tools first
- Debug Console (`src/components/debug/DebugTerminal.tsx`)
  - `help`, `health`, `doctor`, `list ...`, `inspect ...`, `run indicator ...`, `logs ...`, `chart snapshot ...`
- Debug Logs (`src/components/debug/DebugLogViewer.tsx`)
  - Filter by level, module, requestId
- Backend debug routes (`server/src/routes/debugRoutes.js`)

4) Capture evidence
- Record the command and output (or log entries) that prove the change works.
- Note the requestId/module used for filtering.

## Add probes when Debug mode is missing the signal

1) Add a backend debug command
- Update `server/src/services/debugCommands/commandCatalog.js`
- Implement a handler in `server/src/services/debugCommands/handlers/`
- Return short `lines` for console output and optional `data` for detail.

2) Add a debug API endpoint
- Add a route in `server/src/routes/debugRoutes.js`
- Add a client method in `src/services/api/client.ts`

3) Add a Debug UI hook
- Add a small panel/button in `src/views/DebugView.tsx`
- Keep it read-only and only available in Debug view.

4) Prefer log probes when possible
- Use `apiClient.debugClientLog(...)` with `requestId` and context fields.
- Keep logs concise and actionable.

## Verification

- Always run a Debug-mode probe after implementing a feature change or addition (no extra prompt).
- Re-run the debug probe and confirm the acceptance signal.
- Log the evidence in `ACTION_LOG.md` / `ACTION_LOG.jsonl`.

## Automation pledge

- When the user asks for a feature change or addition, run the Debug-mode probe immediately after the implementation finishes.
- If the Debug-mode signal does not exist, add the minimum probe (command/log/UI) needed and then run it.
