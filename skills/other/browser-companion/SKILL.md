---
name: browser-companion
description: >-
  Zero-dependency live-preview server providing an agent↔browser bidirectional
  companion. Watches a content directory, wraps HTML fragments in a frame
  template, broadcasts live-reload over WebSocket, and captures browser-side
  click events to a JSONL file. Use when an agent needs to show HTML to the
  user in a browser and react to clicks — mockups, design exploration, gallery
  browsing, multi-select choices, prototype iteration. Triggered by
  "live preview", "browser companion", "preview server", "browser mockup",
  "show in browser", "arkhe-preview", or any skill that wants to write HTML
  fragments and have the user see them reload in real time.
disable-model-invocation: true
argument-hint: "[start|stop|status] [options]"
---

# Browser Companion

A zero-dependency Node.js HTTP + WebSocket server that turns a directory of HTML fragments into a live-reloading preview, with browser→agent click event capture.

The skill ships a public CLI `arkhe-preview` placed in `plugins/devtools/bin/`. **Any plugin's skill can invoke it as a bare bash command** — no need to know the devtools install path.

## Quick Start

```bash
# Start a server scoped to the current project
arkhe-preview start --project-dir "$(pwd)"

# Output (one JSON line on stdout):
#   {"type":"server-started","port":54123,"url":"http://localhost:54123",
#    "screen_dir":".../<id>/content","state_dir":".../<id>/state",
#    "session_dir":".../<id>","pid":12345}

# Tell the user to open the URL. Then write HTML to screen_dir:
echo '<h2>Hello</h2><button data-event="ok">OK</button>' > "$SCREEN/content.html"

# Browser auto-reloads. User clicks. Read events:
tail -f "$STATE/events.jsonl"

# When done:
arkhe-preview stop "$SESSION_DIR"
```

## When to Use This

- **Design / mockup loops** — write HTML to `screen_dir`, browser shows it
- **Multi-select / variant selection** — give the user clickable options, read events.jsonl to learn what they picked
- **Iteration on generated UI** — overwrite fragment → instant reload
- **Cross-plugin** — any plugin's skill can call `arkhe-preview` directly; it lives in devtools but its CLI is on PATH whenever devtools is enabled

## Core Commands

```bash
arkhe-preview start [options]      # Print {url, screen_dir, state_dir, session_dir, pid} JSON
arkhe-preview stop <session-dir>   # Graceful SIGTERM, falls back to SIGKILL
arkhe-preview status <session-dir> # {running, pid, url} JSON (always exits 0)
arkhe-preview --help               # Full option reference (USAGE.txt)
```

Common start options:
- `--project-dir <path>` — store under `<path>/.claude/preview/<id>/` (default: `/tmp/arkhe-preview-<id>/`)
- `--frame-template <path>` — override default HTML frame
- `--helper <path>` — override default browser-side helper JS
- `--port <N>` — pin a specific port
- `--owner-pid 0` — disable the watchdog (use idle timeout only)

## Custom Frame & Helper

Default frame is neutral — a small header, OS-aware light/dark theming, no domain UI. Default helper captures clicks on `[data-event]` and ships them as JSONL events.

For richer UIs (indicator bars, gallery sidebars, multi-select chrome), supply a custom frame template and helper:

```bash
arkhe-preview start --project-dir "$PWD" \
  --frame-template ./my-frame.html \
  --helper ./my-helper.js
```

Frame template must contain `<!-- FRAGMENT -->` (canonical) or `<!-- CONTENT -->` (legacy alias) where the agent's HTML will be inserted.

Reference example flavors live in `${CLAUDE_PLUGIN_ROOT}/skills/browser-companion/examples/`:
- [`brainstorm/README.md`](examples/brainstorm/README.md) — multi-select indicator bar with `[data-choice]` capture
- [`gallery/README.md`](examples/gallery/README.md) — variant browser sidebar with `[data-variant]` capture

These are static reference docs, NOT runtime presets. Copy what fits.

## Session Layout

```
<project>/.claude/preview/<session-id>/
├── content/                 # Agent writes HTML fragments here
├── state/
│   ├── server-info          # JSON: url, port, host, pid
│   ├── events.jsonl         # Append-only browser events (one JSON object/line)
│   └── server.pid           # Server PID
└── logs/
    └── server.log
```

## Event Schema

Every WebSocket message from a browser client is persisted to `events.jsonl` as one JSON line. Server adds `timestamp` (ISO 8601) and `clientId` if not already present. No filtering — consumers parse what they care about.

```json
{"timestamp":"2026-05-21T12:34:56.789Z","clientId":"a1b2c3d4","type":"click","action":"ok","payload":{"foo":"bar"},"text":"OK","id":null}
```

## See Also

- [WORKFLOW.md](WORKFLOW.md) — full protocol, CLI contract, WebSocket details, lifecycle, attribution
- [EXAMPLES.md](EXAMPLES.md) — end-to-end walkthroughs
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — port collisions, watchdog issues, PATH not refreshed, etc.
