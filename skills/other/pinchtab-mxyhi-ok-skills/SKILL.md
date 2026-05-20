---
name: pinchtab
description: "Use this skill when a task needs browser automation through PinchTab: open a website, inspect interactive elements, click through flows, fill out forms, scrape page text, log into sites with a persistent profile, export screenshots or PDFs, manage multiple browser instances, or fall back to the HTTP API when the CLI is unavailable. Prefer this skill for token-efficient browser work driven by stable accessibility refs such as `e5` and `e12`."
metadata:
  openclaw:
    requires:
      bins:
        - pinchtab
      anyBins:
        - google-chrome
        - google-chrome-stable
        - chromium
        - chromium-browser
    homepage: https://github.com/pinchtab/pinchtab
    install:
      - kind: brew
        formula: pinchtab/tap/pinchtab
        bins: [pinchtab]
      - kind: go
        package: github.com/pinchtab/pinchtab/cmd/pinchtab@latest
        bins: [pinchtab]
---

# Browser Automation with PinchTab

PinchTab gives agents a browser they can drive through stable accessibility refs, low-token text extraction, and persistent profiles or instances. Treat it as a CLI-first browser skill; use the HTTP API only when the CLI is unavailable or you need profile-management routes that do not exist in the CLI yet.

Preferred tool surface:

- Use `pinchtab` CLI commands first.
- Use `curl` for profile-management routes or non-shell/API fallback flows.
- Use `jq` only when you need structured parsing from JSON responses.

## Agent Identity And Attribution

When multiple agents share one PinchTab server, always give each agent a stable ID.

- CLI flows: prefer `pinchtab --agent-id <agent-id> ...`
- long-running shells: set `PINCHTAB_AGENT_ID=<agent-id>`
- raw HTTP flows: send `X-Agent-Id: <agent-id>` on requests that should be attributed to that agent

That identity is recorded as `agentId` in activity events and powers:

- scheduler task attribution when work is dispatched on behalf of an agent

If you are switching between unrelated browser tasks, do not reuse the same agent ID unless you intentionally want one combined activity trail.

## Safety Defaults

- Default to `http://localhost` targets. Only use a remote PinchTab server when the user explicitly provides it and, if needed, a token.
- Prefer read-only operations first: `text`, `snap -i -c`, `snap -d`, `find`, `click`, `fill`, `type`, `press`, `select`, `hover`, `scroll`.
- Do not evaluate arbitrary JavaScript unless a simpler PinchTab command cannot answer the question.
- Do not upload local files unless the user explicitly names the file to upload and the destination flow requires it.
- Do not save screenshots, PDFs, or downloads to arbitrary paths. Use a user-specified path or a safe temporary/workspace path.
- Never use PinchTab to inspect unrelated local files, browser secrets, stored credentials, or system configuration outside the task.

## Core Workflow

Every PinchTab automation follows this pattern:

1. Ensure the correct server, profile, or instance is available for the task.
2. Navigate with `pinchtab nav <url>` or `pinchtab instance navigate <instance-id> <url>`.
3. Observe with `pinchtab snap -i -c`, `pinchtab snap --text`, or `pinchtab text`, then collect the current refs such as `e5`.
4. Interact with those fresh refs using `click`, `fill`, `type`, `press`, `select`, `hover`, or `scroll`.
5. Re-snapshot or re-read text after any navigation, submit, modal open, accordion expand, or other DOM-changing action.

Rules:

- Never act on stale refs after the page changes.
- Default to `pinchtab text` when you need content, not layout.
- Default to `pinchtab snap -i -c` when you need actionable elements.
- Use screenshots only for visual verification, UI diffs, or debugging.
- Start multi-site or parallel work by choosing the right instance or profile first.

## Selectors

PinchTab uses a unified selector system. Any command that targets an element accepts these formats:

| Selector | Example | Resolves via |
|---|---|---|
| Ref | `e5` | Snapshot cache (fastest) |
| CSS | `#login`, `.btn`, `[data-testid="x"]` | `document.querySelector` |
| XPath | `xpath://button[@id="submit"]` | CDP search |
| Text | `text:Sign In` | Visible text match |
| Semantic | `find:login button` | Natural language query via `/find` |

Auto-detection: bare `e5` → ref, `#id` / `.class` / `[attr]` → CSS, `//path` → XPath. Use explicit prefixes (`css:`, `xpath:`, `text:`, `find:`) when auto-detection is ambiguous.

```bash
pinchtab click e5                        # ref
pinchtab click "#submit"                 # CSS (auto-detected)
pinchtab click "text:Sign In"            # text match
pinchtab click "xpath://button[@type]"   # XPath
pinchtab fill "#email" "user@test.com"   # CSS
pinchtab fill e3 "user@test.com"         # ref
```

The same syntax works in the HTTP API via the `selector` field:

```json
{"kind": "click", "selector": "text:Sign In"}
{"kind": "fill", "selector": "#email", "text": "user@test.com"}
{"kind": "click", "selector": "e5"}
```

Legacy `ref` field is still accepted for backward compatibility.

## Command Chaining

Use `&&` only when you do not need to inspect intermediate output before deciding the next step.

Good:

```bash
pinchtab nav https://pinchtab.com && pinchtab snap -i -c
pinchtab click --wait-nav e5 && pinchtab snap -i -c
pinchtab nav https://pinchtab.com --block-images && pinchtab text
```

Run commands separately when you must read the snapshot output first:

```bash
pinchtab nav https://pinchtab.com
pinchtab snap -i -c
# Read refs, choose the correct e#
pinchtab click e7
pinchtab snap -i -c
```

## Challenge Solving

If a page shows a challenge instead of content (e.g., "Just a moment..."), call `POST /solve` with `{"maxAttempts": 3}` to auto-detect and resolve it. Use `POST /tabs/TAB_ID/solve` for tab-scoped. Works best with `stealthLevel: "full"` in config. Safe to call speculatively — returns immediately if no challenge is present. See [api.md](./references/api.md) for full solver options.

## Handling Authentication and State

Pick a pattern before interacting with the site:

1. **One-off browsing**: `pinchtab instance start` → use `--server http://localhost:<port>` for commands.
2. **Reuse a profile**: `pinchtab instance start --profile work --mode headed` → switch to `--mode headless` after login is stored.
3. **Create profile via HTTP**: `POST /profiles` with `{"name":"..."}`, then `POST /profiles/<name>/start`.
4. **Human-assisted login**: Start headed, human signs in, agent reuses the profile headless.
5. **HTTP-only agent**: Use `POST /instances/start`, then target the instance port with curl. Send `X-Agent-Id` for attribution.

If the server is exposed beyond localhost, require a token. See [TRUST.md](./TRUST.md).

**Agent sessions**: Each agent can get its own revocable session token via `pinchtab session create --agent-id <id>` or `POST /sessions`. Set `PINCHTAB_SESSION=ses_...` or send `Authorization: Session ses_...`. Sessions have idle timeout (default 30m) and max lifetime (default 24h).

## Essential Commands

### Server and targeting

```bash
pinchtab server                                     # Start server foreground
pinchtab daemon install                             # Install as system service
pinchtab health                                     # Check server status
pinchtab instances                                  # List running instances
pinchtab profiles                                   # List available profiles
pinchtab --server http://localhost:9868 snap -i -c  # Target specific instance
```

### Navigation and tabs

```bash
pinchtab nav <url>
pinchtab nav <url> --new-tab
pinchtab nav <url> --tab <tab-id>
pinchtab nav <url> --block-images
pinchtab nav <url> --block-ads
pinchtab back                                       # Navigate back in history
pinchtab forward                                    # Navigate forward
pinchtab reload                                     # Reload current page
pinchtab tab                                        # List tabs or focus by ID
pinchtab tab new <url>
pinchtab tab close <tab-id>
pinchtab instance navigate <instance-id> <url>
```

### Observation

```bash
pinchtab snap
pinchtab snap -i                                    # Interactive elements only
pinchtab snap -i -c                                 # Interactive + compact
pinchtab snap -d                                    # Diff from previous snapshot
pinchtab snap --selector <css>                      # Scope to CSS selector
pinchtab snap --max-tokens <n>                      # Token budget limit
pinchtab snap --text                                # Text output format
pinchtab text                                       # Page text content
pinchtab text --raw                                 # Raw text extraction
pinchtab find <query>                               # Semantic element search
pinchtab find --ref-only <query>                    # Return refs only
```

Guidance:

- `snap -i -c` is the default for finding actionable refs.
- `snap -d` is the default follow-up snapshot for multi-step flows.
- `text` is the default for reading articles, dashboards, reports, or confirmation messages.
- `find --ref-only` is useful when the page is large and you already know the semantic target.
- Refs from `snap -i` and full `snap` use different numbering. Do not mix them — if you snapshot with `-i`, use those refs. If you re-snapshot without `-i`, get fresh refs before acting.

### Interaction

All interaction commands accept unified selectors (refs, CSS, XPath, text, semantic). See the Selectors section above.

```bash
pinchtab click <selector>                           # Click element
pinchtab click --wait-nav <selector>                # Click and wait for navigation
pinchtab click --x 100 --y 200                      # Click by coordinates
pinchtab dblclick <selector>                        # Double-click element
pinchtab type <selector> <text>                     # Type with keystrokes
pinchtab fill <selector> <text>                     # Set value directly
pinchtab press <key>                                # Press key (Enter, Tab, Escape...)
pinchtab hover <selector>                           # Hover element
pinchtab select <selector> <value>                  # Select dropdown option
pinchtab scroll <selector|pixels>                   # Scroll element or page
```

Rules:

- Prefer `fill` for deterministic form entry.
- Prefer `type` only when the site depends on keystroke events.
- Prefer `click --wait-nav` when a click is expected to navigate.
- Re-snapshot immediately after `click`, `press Enter`, `select`, or `scroll` if the UI can change.
- To discover valid dropdown values, snapshot with `filter=interactive` first — the output shows `<option>` elements with their `value` attributes. Then use `select` with the exact value.

### Export, debug, and verification

```bash
pinchtab screenshot
pinchtab screenshot -o /tmp/pinchtab-page.png       # Format driven by extension
pinchtab screenshot -q 60                            # JPEG quality
pinchtab pdf
pinchtab pdf -o /tmp/pinchtab-report.pdf
pinchtab pdf --landscape
```

### Advanced operations: explicit opt-in only

Use these only when the task explicitly requires them and safer commands are insufficient.

```bash
pinchtab eval "document.title"
pinchtab download <url> -o /tmp/pinchtab-download.bin
pinchtab upload /absolute/path/provided-by-user.ext -s <css>
```

Rules:

- `eval` is for narrow, read-only DOM inspection unless the user explicitly asks for a page mutation.
- `download` should prefer a safe temporary or workspace path over an arbitrary filesystem location.
- `upload` requires a file path the user explicitly provided or clearly approved for the task.

### HTTP API fallback

```bash
curl -X POST http://localhost:9868/navigate \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

curl "http://localhost:9868/snapshot?filter=interactive&format=compact"

curl -X POST http://localhost:9868/action \
  -H "Content-Type: application/json" \
  -d '{"kind":"fill","selector":"e3","text":"ada@example.com"}'

curl http://localhost:9868/text

## Instance-scoped solve (instance port, not server port)
curl -X POST http://localhost:9868/solve \
  -H "Content-Type: application/json" \
  -d '{"maxAttempts": 3}'

curl http://localhost:9868/solvers
```

Use the API when:

- the agent cannot shell out,
- profile creation or mutation is required,
- or you need explicit instance- and tab-scoped routes.

### Tab-scoped HTTP API

**Important:** Each `POST /navigate` creates a new tab by default. The default (non-tab-scoped) endpoints like `/snapshot`, `/action`, `/text` operate on the *active* tab, which may not be the one you just navigated. In multi-tab workflows, always use tab-scoped routes to avoid acting on the wrong page.

Get the tab ID from the navigate response or from `GET /tabs`.

```bash
# List all tabs
curl http://localhost:9867/tabs \
  -H "Authorization: Bearer <token>"

# Navigate in a specific tab (does not create a new tab)
curl -X POST http://localhost:9867/tabs/TAB_ID/navigate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

# Snapshot a specific tab
curl "http://localhost:9867/tabs/TAB_ID/snapshot?filter=interactive&format=compact" \
  -H "Authorization: Bearer <token>"

# Get text from a specific tab
curl http://localhost:9867/tabs/TAB_ID/text \
  -H "Authorization: Bearer <token>"

# Perform action on a specific tab
curl -X POST http://localhost:9867/tabs/TAB_ID/action \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"click","selector":"#submit-btn"}'

# Navigate back/forward in a specific tab
curl -X POST http://localhost:9867/tabs/TAB_ID/back \
  -H "Authorization: Bearer <token>"
curl -X POST http://localhost:9867/tabs/TAB_ID/forward \
  -H "Authorization: Bearer <token>"

# Screenshot (GET, not POST)
curl http://localhost:9867/tabs/TAB_ID/screenshot \
  -H "Authorization: Bearer <token>" \
  --output screenshot.png

# PDF export (GET or POST)
curl http://localhost:9867/tabs/TAB_ID/pdf \
  -H "Authorization: Bearer <token>" \
  --output page.pdf

# Close a tab
curl -X POST http://localhost:9867/tabs/TAB_ID/close \
  -H "Authorization: Bearer <token>"
```

The default (non-tab-scoped) endpoints also support screenshots and PDF:

```bash
# Screenshot of active tab (GET)
curl http://localhost:9867/screenshot \
  -H "Authorization: Bearer <token>" \
  --output screenshot.png

# PDF of active tab (GET or POST)
curl http://localhost:9867/pdf \
  -H "Authorization: Bearer <token>" \
  --output page.pdf
```

**Navigation with `waitNav`:** When clicking a link or button that triggers page navigation, include `"waitNav": true` in the action body. Without it, PinchTab returns a `navigation_changed` error to protect against unexpected navigation during form interactions.

```json
{"kind": "click", "selector": "#search-btn", "waitNav": true}
```

All tab-scoped routes follow the pattern `/tabs/{TAB_ID}/...` and mirror the default endpoints. The full list includes: `navigate`, `back`, `forward`, `reload`, `snapshot`, `screenshot`, `text`, `pdf`, `action`, `actions`, `dialog`, `wait`, `find`, `lock`, `unlock`, `cookies`, `metrics`, `network`, `solve`, `close`, `storage`, `evaluate`, `download`, `upload`.

## Common Patterns

### Open a page and inspect actions

```bash
pinchtab nav https://pinchtab.com && pinchtab snap -i -c
```

### Fill and submit a form

```bash
pinchtab nav https://example.com/login
pinchtab snap -i -c
pinchtab fill e3 "user@example.com"
pinchtab fill e4 "correct horse battery staple"
pinchtab click --wait-nav e5
pinchtab text
```

### Search, then extract the result page cheaply

```bash
pinchtab nav https://example.com/search
pinchtab snap -i -c
pinchtab fill e2 "quarterly report"
pinchtab click e3  # Click the Search button
pinchtab text
```

**Form submission:** Always click the submit button — never use `press Enter`. Most HTML forms only fire their submission handler on button click, not on Enter keypress.

### Use diff snapshots in a multi-step flow

```bash
pinchtab nav https://example.com/checkout
pinchtab snap -i -c
pinchtab click e8
pinchtab snap -d -i -c
```

### Target elements without a snapshot

When you know the page structure, skip the snapshot and use CSS or text selectors directly:

```bash
pinchtab click "text:Accept Cookies"
pinchtab fill "#search" "quarterly report"
pinchtab click "xpath://button[@type='submit']"
```


## Security and Token Economy

- Use a dedicated automation profile, not a daily browsing profile.
- If PinchTab is reachable off-machine, require a token and bind conservatively.
- Prefer `text`, `snap -i -c`, and `snap -d` before screenshots, PDFs, eval, downloads, or uploads.
- Use `--block-images` for read-heavy tasks that do not need visual assets.
- Stop or isolate instances when switching between unrelated accounts or environments.

## Diffing and Verification

- Use `pinchtab snap -d` after each state-changing action in long workflows.
- Use `pinchtab text` to confirm success messages, table updates, or navigation outcomes.
- Use `pinchtab screenshot` only when visual regressions, CAPTCHA, or layout-specific confirmation matters.
- If a ref disappears after a change, treat that as expected and fetch fresh refs instead of retrying the stale one.


## References

- Full API: [api.md](./references/api.md)
- Minimal env vars: [env.md](./references/env.md)
- Agent optimization: [agent-optimization.md](./references/agent-optimization.md)
- Profiles: [profiles.md](./references/profiles.md)
- MCP: [mcp.md](./references/mcp.md)
- Security model: [TRUST.md](./TRUST.md)


