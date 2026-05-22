---
name: proxelar
description: "Intercept, inspect, and modify HTTP/HTTPS traffic via a Rust MITM proxy with Lua scripting hooks. Supports API debugging, LLM call capture for evals, endpoint mocking, CORS/auth header injection, latency simulation, and telemetry blocking. Triggers on 'proxy', 'intercept traffic', 'inspect requests', 'mock API', 'capture API calls', 'MITM', 'network debug', 'HTTP inspection'."
---

# Proxelar

Rust-based MITM proxy for intercepting and transforming HTTP/HTTPS traffic via Lua scripting. Provides TUI, terminal, and web GUI interfaces. Installed via `brew install proxelar`.

## Category

Infrastructure Operations

## Modes

| Mode | Command | When to use |
|------|---------|-------------|
| Forward proxy | `proxelar` | Intercept outbound traffic from any app configured to use `127.0.0.1:8080` |
| Reverse proxy | `proxelar -m reverse --target http://localhost:3000` | Inspect traffic to a local dev server without configuring the client |
| Web GUI | `proxelar -i gui` | Agent-visible network inspector at `http://localhost:8081` — screenshot for visual feedback |
| Scripted | `proxelar --script path/to/hook.lua` | Automated request/response transformation via Lua hooks |

Combine modes: `proxelar -m reverse --target http://localhost:3000 -i gui --script scripts/log_to_jsonl.lua`

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `-i, --interface` | `terminal`, `tui`, `gui` | `tui` |
| `-m, --mode` | `forward`, `reverse` | `forward` |
| `-p, --port` | Listening port | `8080` |
| `-b, --addr` | Bind address | `127.0.0.1` |
| `-t, --target` | Upstream target (required for reverse mode) | -- |
| `--gui-port` | Web GUI port | `8081` |
| `--ca-dir` | CA certificate directory | `~/.proxelar` |
| `-s, --script` | Lua script for request/response hooks | -- |

## Lua Scripting

Define `on_request` and/or `on_response` hooks:

```lua
function on_request(request)
    -- request.method, request.url, request.headers, request.body
    -- Return request to forward (modified or not)
    -- Return response table to short-circuit: { status = 403, headers = {}, body = "Blocked" }
    -- Return nil to pass through unchanged
end

function on_response(request, response)
    -- response.status, response.headers, response.body
    -- Return response (modified or not), or nil to pass through
end
```

## Bundled Lua Scripts

Run any script with `proxelar --script ~/.claude/skills/proxelar/scripts/<name>.lua`

| Script | Purpose |
|--------|---------|
| `log_to_jsonl.lua` | Log request/response pairs as JSONL to `~/.proxelar/traffic.jsonl` |
| `capture_for_eval.lua` | Capture LLM API calls (Anthropic/OpenAI/Gemini) as structured JSONL for eval pipelines |
| `mock_api.lua` | Template for mocking API endpoints — edit the `mocks` table |
| `inject_cors.lua` | Add permissive CORS headers to all responses |
| `latency_inject.lua` | Add configurable artificial latency to matching URLs |
| `block_telemetry.lua` | Block analytics and telemetry domains |

## Agent Integration

### Agent-Browser Bridge

Route agent-browser traffic through Proxelar for combined page + network visibility:

```bash
# Terminal 1: start proxelar in reverse mode
proxelar -m reverse --target http://localhost:3000 -i gui --script ~/.claude/skills/proxelar/scripts/log_to_jsonl.lua &

# Terminal 2: navigate through proxelar, then snapshot
agent-browser --proxy "http://127.0.0.1:8080" open http://127.0.0.1:8080 && agent-browser snapshot
```

### Agent Visual Feedback via Web GUI

Start Proxelar with `-i gui`, then screenshot `http://localhost:8081` via Claude-in-Chrome or agent-browser to give the agent network-layer visibility into what the application is doing.

### Frametime + Network Correlation

Inject `scripts/frametime_bench.js` into a running page via `mcp__claude-in-chrome__javascript_tool` or agent-browser `eval`. Read console output with pattern `p50` to get percentile data. Run alongside `latency_inject.lua` to correlate network latency with rendering jank.

## CA Certificate

First run auto-generates `~/.proxelar/proxelar-ca.pem`. Trust it once:

```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/.proxelar/proxelar-ca.pem
```

Or visit `http://proxel.ar` through the proxy for guided install.

## Gotchas

- Check port 8080 is free before starting: `lsof -i :8080`
- Reverse mode requires `--target` — CLI errors immediately if omitted
- Lua scripts are loaded once at startup; edit requires restart
- Web GUI binds to `127.0.0.1:8081` by default; use `--addr 0.0.0.0` for remote access
- WebSocket traffic passes through but Lua hooks only fire on HTTP request/response, not individual WS frames
- TUI and Web GUI support interactive request inspection, editing, and dropping — not just passive viewing
