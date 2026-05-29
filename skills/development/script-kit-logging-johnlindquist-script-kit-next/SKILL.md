---
name: script-kit-logging
description: Logging and observability patterns for Script Kit GPUI. Use when adding logs, debugging, or understanding the logging system. Covers JSONL format, compact AI log mode, correlation IDs, and error handling.
---

# Script Kit Logging

Structured logging patterns for debugging and observability.

## AI Compact Log Mode (SCRIPT_KIT_AI_LOG=1)

Compact stderr format: `SS.mmm|L|C|message`

- `L`: `i` INFO, `w` WARN, `e` ERROR, `d` DEBUG, `t` TRACE
- `C` categories:
  - `P` position, `A` app, `U` UI, `S` stdin, `H` hotkey
  - `V` visibility, `E` exec, `K` key, `F` focus, `T` theme
  - `C` cache, `R` perf, `W` window_mgr, `X` error
  - `M` mouse_hover, `L` scroll_state, `Q` scroll_perf
  - `D` design, `B` script, `N` config, `Z` resize

Example:
- Standard: `... INFO ... Selected display origin=(0,0)`
- Compact: `13.150|i|P|Selected display origin=(0,0)`

Enable:
```bash
SCRIPT_KIT_AI_LOG=1 ./target/debug/script-kit-gpui 2>&1
```

## Log Modes

| Mode | Command | Use Case |
|------|---------|----------|
| Compact AI logs | `SCRIPT_KIT_AI_LOG=1` | Default for AI agents (saves ~70% tokens) |
| Full debug logs | `RUST_LOG=debug` | Deep debugging |
| Specific module | `RUST_LOG=script_kit::theme=debug` | Target one module |

## JSONL Logging

Logs to: `~/.scriptkit/logs/script-kit-gpui.jsonl`

Line example:
```json
{"timestamp":"...","level":"INFO","target":"script_kit::executor","message":"Script executed","fields":{"script_name":"hello.ts","duration_ms":142,"exit_code":0}}
```

## Tracing Patterns

Use `tracing` + `tracing-subscriber`:
- `#[instrument]` for spans
- Record `duration_ms`; warn if slow (e.g. >100ms)

Correlation IDs:
- Generate UUID per user action/run
- Attach to spans so nested logs inherit it

Required fields when relevant: `correlation_id`, `duration_ms`, `bead_id`, `agent_name`, `files_touched`

## Log Level Guide

- `error`: failure
- `warn`: unexpected but handled
- `info`: key events
- `debug`: development
- `trace`: very verbose

Filter by targets (module paths): `script_kit::ui`, `script_kit::executor`, `script_kit::theme`

## Error Handling

- Application errors: `anyhow::Result`; add `.context()` at boundaries
- Domain/library errors: `thiserror` when callers match variants
- User-facing errors: `NotifyResultExt` → log first (`tracing::error!`) then toast

Best practices:
- Don't `unwrap()`/`expect()`
- Add context at each level ("which file?", "what operation?")
- Use typed fields in logs (avoid interpolated strings)

## Log Queries

```bash
grep '"correlation_id":"abc-123"' ~/.scriptkit/logs/script-kit-gpui.jsonl
grep '"duration_ms":' ~/.scriptkit/logs/script-kit-gpui.jsonl | jq 'select(.fields.duration_ms > 100)'
grep '"level":"ERROR"' ~/.scriptkit/logs/script-kit-gpui.jsonl | tail -50
```
