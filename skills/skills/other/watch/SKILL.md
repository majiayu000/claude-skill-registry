---
name: watch
description: Monitored development with dev3000 (d3k). Use when debugging web apps, needing full-stack visibility, reading error context, or capturing browser + server logs. Triggers on "watch", "d3k", "dev3000", "monitor app", "capture logs", "what went wrong", "error context".
---

# Monitored Development

CAPTURE THEN DIAGNOSE. Never guess at the cause — capture the full timeline first, then read it. d3k unifies server, browser, and network events into one log that makes root causes visible.

## Rules

- Never diagnose without context — always `d3k errors --context` before forming a hypothesis
- Let d3k own the dev server — don't run your server separately, d3k wraps it
- Read the timeline, don't grep for errors — surrounding events reveal the chain of causation
- Classify errors before fixing — the source tag determines where to investigate
- Always use long-form flags (`--context`, `--type`) to avoid collision with d3k's `-c` (command) flag

## Startup

Always compose the full stack when starting a monitored dev session.

1. Check prerequisites: `which d3k || npm install -g dev3000`, `which portless || npm install -g portless`
2. Read `package.json` scripts to find the dev command and determine the runner
3. Start with CDP browser monitoring:

```bash
portless <name> d3k -c "<runner> <dev-cmd>" --no-tui --no-skills --no-agent
```

| Slot | Source |
|------|--------|
| `<name>` | Project or app directory name |
| `<runner>` | Package manager: `bun`, `npx`, `pnpm exec` |
| `<dev-cmd>` | From package.json scripts.dev, e.g. `next dev --webpack` |

d3k launches CDP-monitored Chrome automatically. Portless gives stable URL (`<name>.localhost:1355`).
Only use `--servers-only` when explicitly asked to skip browser launch.

**Examples:**
```bash
portless myapp d3k -c "bun run dev" --no-tui --no-skills --no-agent
portless playground d3k -c "bun next dev --webpack" --no-tui --no-skills --no-agent
portless docs d3k -c "npx vitepress dev" --no-tui --no-skills --no-agent
```

## Flow: Debug Cycle

The core loop — capture everything, classify, fix, verify.

```
startup (see above)
→ reproduce the issue (d3k captures everything)
→ d3k errors --context (errors with surrounding interaction context)
→ classify by source tag
→ fix based on classification
→ reproduce again → d3k errors shows clean
```

## Flow: Error Classification

The source tag in `d3k errors --context` output tells you where to look:

| Tag | Means | Investigate |
|-----|-------|-------------|
| `[SERVER]` | Backend crash/exception | Server code, dependencies, env vars |
| `[CONSOLE ERROR]` | Frontend JS error | Component code, state, props |
| `[NETWORK]` 4xx | Client request issue | URL, auth headers, request payload |
| `[NETWORK]` 5xx | Server handling issue | API route handler, DB queries, external services |
| `[RUNTIME.ERROR]` | Unhandled rejection/exception | Async code, missing error boundaries |

Read the events *before* the error — they reveal the chain:
```
[INTERACTION] Click on button#submit
[NETWORK] POST /api/users → 500 (12ms)
[CONSOLE ERROR] TypeError: Cannot read property 'id' of undefined
```

Fix the API route, not the frontend.

## Flow: Inspect

When the user says "check what happened", "what went wrong", or "look at the page":

1. Read timeline: `d3k errors --context`
2. Snapshot the page: `d3k agent-browser --cdp $(d3k cdp-port) snapshot -i`
3. Screenshot if needed: `d3k agent-browser --cdp $(d3k cdp-port) screenshot /tmp/page.png`
4. Classify and diagnose from combined timeline + page state

The CDP connection means every browser interaction appears in d3k's timeline alongside server/network effects — full cause-and-effect visibility.

## Flow: Monitored Development

Start d3k from the beginning, not after something breaks.

```
startup → develop normally
→ d3k logs --type browser (check for warnings periodically)
→ d3k errors before commit (catch anything captured during dev)
→ fix any issues → clean commit
```

Filter logs by source:
- `d3k logs --type browser` — browser events only
- `d3k logs --type server` — server output only
- `d3k logs --type network` — network requests only

## Flow: AI-Assisted Diagnosis

When the timeline is complex, let d3k synthesize:

```bash
d3k fix              # Diagnose from all captured context
d3k fix -f build     # Focus on build errors specifically
d3k fix -t 5         # Analyze last 5 minutes only
```

## Composition

- **With browser:** `d3k agent-browser --cdp $(d3k cdp-port)` bridges automation with monitoring — interactions appear in the timeline
- **With portless:** Always compose via Startup. Portless gives stable URLs, d3k gives timeline capture.
- **With hope:loop:** `d3k errors --context` output as debugging evidence when waves encounter failures
- **With hope:verify:** d3k screenshot captures as visual regression evidence in pre-PR checks

## Anti-Patterns

- **Diagnosing without capturing** — guessing at causes without reading the timeline
- **Running dev server separately from d3k** — d3k needs to own the process to capture everything
- **Using `--servers-only` by default** — disables CDP browser monitoring, the most valuable layer
- **Using short flags with d3k subcommands** — `-c` collides with `--command`; always use `--context`, `--type`
- **Fixing the symptom** — a frontend crash from a failed API call means fixing the backend, not adding null checks
