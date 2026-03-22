---
name: trace
description: Spawn agent to trace code flow via query tools — answer only, no context cost
user-invocable: true
disable-model-invocation: false
context: fork
agent: Explore
argument-hint: "<question about code flow>"
---
Trace the following code flow through the Alt-Tabby codebase:
"$ARGUMENTS"

## Available Query Tools

Run via `powershell -File tools/<name>`. These are the primary research tools — always prefer them over reading files directly.

### CALL CHAIN (primary tool for tracing)
```
query_callchain.ps1 <funcName> [-Depth N] [-Reverse]
```
Forward: shows what `<funcName>` calls, to N levels deep (default 2).
Reverse: shows what calls `<funcName>`, to N levels up.
Example: `powershell -File tools/query_callchain.ps1 GUI_Repaint -Depth 3`

### FUNCTION BODY
```
query_function.ps1 <funcName>
```
Extracts full function body with line numbers. Use when you need to understand WHAT a function does, not just what it calls.
Example: `powershell -File tools/query_function.ps1 GUI_TransitionTo`

### GLOBAL OWNERSHIP
```
query_global_ownership.ps1 <globalName>
```
Shows who declares, writes (with mutation count), and reads a global.
Example: `powershell -File tools/query_global_ownership.ps1 gGUI_State`

### GLOBAL MUTATIONS (detailed)
```
query_mutations.ps1 <globalName> [-Brief]
```
Shows every function that mutates a global, with guards (Critical sections, if-conditions) and literal values assigned. More detailed than ownership.
Example: `powershell -File tools/query_mutations.ps1 gGUI_State`

### IMPACT / BLAST RADIUS
```
query_impact.ps1 <funcName> [-Deep]
```
Shows callers, globals written, downstream readers of those globals.
`-Deep` adds transitive callers (callers of callers).
Example: `powershell -File tools/query_impact.ps1 GUI_Repaint -Deep`

### FILE INTERFACE
```
query_interface.ps1 <filename>
```
Public functions + globals for a file (like `help(module)`). Accepts filename with or without `.ahk` extension.
Example: `powershell -File tools/query_interface.ps1 gui_paint`

### INCLUDE CHAIN
```
query_includes.ps1 [filename]
```
No args: full include tree from entry points.
With filename: who includes this file, what it includes, transitive entry points.
Example: `powershell -File tools/query_includes.ps1 gui_state.ahk`

### FUNCTION VISIBILITY
```
query_function_visibility.ps1 <funcName>
```
Where defined, public/private, all callers across all files.
Example: `powershell -File tools/query_function_visibility.ps1 _GUI_FreezeDisplayList`

### CONFIG
```
query_config.ps1 [keyword | -Section <name> | -Usage <propertyName>]
```
No args: section/group index. Keyword: fuzzy search. `-Usage`: which files read `cfg.X`.
Example: `powershell -File tools/query_config.ps1 -Usage ThemeMode`

### IPC MESSAGES
```
query_ipc.ps1 [message]
```
No args: list all `IPC_MSG_*` constants. With message: who sends/handles it.
Example: `powershell -File tools/query_ipc.ps1 snapshot`

### STATE MACHINE
```
query_state.ps1 [state] [event]
```
No args: index of all states/events. With args: specific dispatch branch.
Hardcoded to `GUI_OnInterceptorEvent` in `gui_state.ahk`.
Example: `powershell -File tools/query_state.ps1 ACTIVE TAB_STEP`

### TIMERS
```
query_timers.ps1 [keyword]
```
No args: full SetTimer inventory. With keyword: fuzzy filter.
Example: `powershell -File tools/query_timers.ps1 heartbeat`

### WINDOWS MESSAGES
```
query_messages.ps1 [query]
```
No args: list all `WM_` handlers. With query: hex, `WM_` name, or handler function.
Example: `powershell -File tools/query_messages.ps1 WM_CTLCOLORSTATIC`

## Research Instructions

1. **ALWAYS prefer query tools over reading files directly** — they return semantic answers and cost far less context
2. **Start with `query_callchain.ps1`** as the primary tracing tool
3. Use `query_function.ps1` ONLY when call chain output doesn't explain what a step does
4. Use `query_global_ownership.ps1` or `query_mutations.ps1` when the question involves data flow through globals
5. Use `query_impact.ps1` when the question is about what a change would affect
6. Use `query_interface.ps1` to understand a module's API surface before diving into specifics

## Response Format

Return ONLY a synthesized answer in this exact format:

## Summary
One sentence: what the flow does end-to-end.

## Path
1. FunctionName (file.ahk:line) — what this step does
2. FunctionName (file.ahk:line) — what this step does
...

## Key State
- globalName (owner: file) — role in this flow
- globalName (owner: file) — role in this flow

Maximum 30 lines total. No raw tool output. No reasoning about your research process.
