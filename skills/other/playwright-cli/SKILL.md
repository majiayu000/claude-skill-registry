---
name: playwright-cli
description: >-
  Browser automation via Playwright CLI for navigating pages, interacting with
  elements, capturing screenshots, and testing web applications through shell
  commands. Use when user mentions "playwright", "browser automation",
  "take a screenshot", "browser testing", "headless browser", "web testing",
  "fill out a form", "e2e test", or needs to automate browser workflows
  from the command line. This is a pre-installed CLI tool — do NOT install
  anything via npx or npm. Invoke this skill first, then use playwright-cli
  bash commands.
allowed-tools: Bash(playwright-cli:*)
---

# Playwright CLI

Automate browsers through shell commands via the Bash tool.

## Core Workflow

Every interaction follows this pattern:

1. **Open** a page: `playwright-cli open <url>`
2. **Snapshot** to discover elements: `playwright-cli snapshot`
3. **Interact** using refs from the snapshot: `playwright-cli click <ref>`
4. **Verify** the result: `playwright-cli screenshot` or `playwright-cli snapshot`

Always run `snapshot` before interacting — element refs come exclusively from
snapshot output and become stale after navigation.

## Command Reference

### Navigation

| Command | Description |
|---------|-------------|
| `open <url>` | Open URL in new page |
| `goto <url>` | Navigate current page |
| `go-back` / `go-forward` | Browser back/forward |
| `reload` | Reload current page |
| `close` | Close the browser |

### Interaction

| Command | Description |
|---------|-------------|
| `click <ref>` | Click an element |
| `dblclick <ref>` | Double-click an element |
| `fill <ref> <text>` | Clear field, then type text |
| `type <text>` | Type into focused element (appends) |
| `check <ref>` / `uncheck <ref>` | Toggle checkbox |
| `select <ref> <values>` | Select dropdown option(s) |
| `hover <ref>` | Hover over element |
| `drag <start> <end>` | Drag between elements |
| `upload <ref> <paths>` | Upload file(s) to file input |
| `eval "<js>"` | Evaluate JavaScript on page |
| `eval "<js>" <ref>` | Evaluate JavaScript on element |
| `dialog-accept [text]` | Accept dialog (optional prompt text) |
| `dialog-dismiss` | Dismiss dialog |
| `resize <w> <h>` | Resize browser window |

### Output

| Command | Description |
|---------|-------------|
| `screenshot [ref] [--filename=f]` | Capture PNG screenshot (page or element) |
| `snapshot [--filename=f]` | Accessibility tree — structured, token-efficient |
| `pdf [--filename=f]` | Generate PDF of the page |

> **Important:** `--filename` resolves relative to the working directory, NOT `outputDir`.
> When using `--filename`, always prepend the project's `outputDir` value
> (check `.playwright/cli.config.json`; defaults to `.playwright-cli`).
> Example: `playwright-cli screenshot --filename=<outputDir>/my-screenshot.png`

### Tabs

| Command | Description |
|---------|-------------|
| `tab list` | List open tabs |
| `tab create [url]` | Open new tab |
| `tab select <index>` | Switch to tab |
| `tab close [index]` | Close tab |

### Keyboard

```bash
playwright-cli press Enter          # Enter, Tab, Escape, ArrowDown, etc.
playwright-cli keydown Shift         # Hold key down
playwright-cli keyup Shift           # Release key
```

### Mouse

```bash
playwright-cli mousemove 150 300     # Move to coordinates
playwright-cli mousedown [button]    # Press button (left/right)
playwright-cli mouseup [button]      # Release button
playwright-cli mousewheel 0 100      # Scroll (deltaX deltaY)
```

## Sessions

- **Default session** — all commands share one session automatically
- **Named sessions** — `playwright-cli -s=<name> open <url>` for parallel browsers
- **List sessions** — `playwright-cli list`
- **Close one** — `playwright-cli -s=<name> close`
- **Close all** — `playwright-cli close-all`
- **Force kill** — `playwright-cli kill-all`
- **Persistent profile** — `playwright-cli open <url> --persistent`
- **Custom profile** — `playwright-cli open <url> --profile=/path/to/dir`
- **Delete data** — `playwright-cli delete-data` or `playwright-cli -s=<name> delete-data`
- **Environment variable** — `PLAYWRIGHT_CLI_SESSION=my-project`

## Configuration

```bash
playwright-cli open <url> --browser=chromium    # chromium (default), firefox, webkit, chrome, msedge
playwright-cli open <url> --headed              # Visible browser window
playwright-cli open <url> --config=config.json  # Custom config file
playwright-cli open <url> --extension           # Connect via browser extension
```

Create `.playwright/cli.config.json` in the project for persistent settings:

```json
{ "browser": { "browserName": "chromium", "launchOptions": { "headless": true } }, "outputDir": ".playwright-cli", "timeouts": { "action": 5000, "navigation": 60000 } }
```

Other options: `network.allowedOrigins`, `network.blockedOrigins`, `saveVideo`.
Environment variables use `PLAYWRIGHT_MCP_` prefix (e.g., `PLAYWRIGHT_MCP_BROWSER=firefox`).

## Common Pitfalls

- **Interacting without snapshot** — refs are unknown until `snapshot` runs
- **Stale refs after navigation** — re-run `snapshot` after `goto`, link clicks, or form submissions
- **fill vs type** — `fill` clears the field first; `type` appends to current content
- **Stuck sessions** — run `playwright-cli kill-all` to force-close all browsers

## Resources

- [EXAMPLES.md](EXAMPLES.md) — Multi-step workflow examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Error diagnosis and fixes
- [references/request-mocking.md](references/request-mocking.md) — Intercept, mock, and block network requests
- [references/running-code.md](references/running-code.md) — Execute arbitrary Playwright code via `run-code`
- [references/session-management.md](references/session-management.md) — Named sessions, isolation, concurrent browsers
- [references/storage-state.md](references/storage-state.md) — Cookies, localStorage, sessionStorage management
- [references/test-generation.md](references/test-generation.md) — Generate Playwright test code from CLI actions
- [references/tracing.md](references/tracing.md) — Capture execution traces for debugging
- [references/video-recording.md](references/video-recording.md) — Record browser sessions as WebM video
