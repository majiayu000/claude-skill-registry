---
name: surf
description: >
  Unified browser automation for AI agents. Uses surf-cli extension when available
  (full features), falls back to CDP (zero-config). Navigate, read with element refs,
  click, type, screenshot.
allowed-tools: Bash, Read
triggers:
  # CDP/Chrome management
  - open browser
  - start chrome
  - start cdp
  - launch chrome
  - chrome devtools
  - cdp
  - puppeteer
  - headless chrome
  # Browser automation
  - click on
  - fill form
  - take screenshot
  - screenshot
  - navigate to
  - go to url
  - automate browser
  - browser automation
  - read webpage
  - scrape page
  # Testing
  - run ui tests
  - smoke tests with browser
  - browser tests
  - e2e tests
  - end to end tests
  # Troubleshooting
  - check browser
  - browser not working
  - cdp not connecting
metadata:
  short-description: Browser automation (extension preferred, CDP fallback)
  cdp-port: 9222
---

# Surf - Browser Automation for AI Agents

**Two modes of operation:**
1. **With surf-cli extension** (recommended): Full features, works with your existing browser
2. **CDP fallback**: Zero-config, but requires starting a separate Chrome instance

If `/tmp/surf.sock` exists (extension installed), all commands route through surf-cli. Otherwise, commands use CDP.

## First-Time Setup

Run the sanity check to verify setup or get installation instructions:

```bash
./sanity.sh
```

If any checks fail, the script provides step-by-step instructions. The agent should run this script and guide the user through any failed steps until all checks pass.

## Quick Start

### Option A: With Extension (Recommended)

One-time setup (see "Extension Setup" below), then:

```bash
surf tab.list                    # See all browser tabs
surf tab.new "https://example.com"
surf read                        # Page content with element refs (e1, e2...)
surf click e5                    # Click element
surf type "hello" --ref e2       # Type into element
surf snap                        # Screenshot
```

### Option B: CDP Fallback (Zero-config)

```bash
surf cdp start                   # Starts separate Chrome instance
surf go "https://example.com"
surf read
surf click e5
surf cdp stop
```

## Commands

### Navigation & Reading

```bash
surf go "https://example.com"    # Navigate to URL
surf read                        # Read page with element refs
surf read --filter all           # Include all elements (not just interactive)
surf text                        # Get raw text content only
```

### Element Interaction

```bash
surf click e5                    # Click element by ref
surf type "hello"                # Type text
surf type "query" --submit       # Type and press Enter
surf type "text" --ref e3        # Type into specific element
surf key Enter                   # Press key (Enter, Tab, Escape, etc.)
```

### Screenshots & Scrolling

```bash
surf snap                        # Screenshot to /tmp
surf snap --output /tmp/page.png # Specify output path
surf snap --full                 # Full page screenshot
surf scroll down                 # Scroll down
surf scroll up                   # Scroll up
surf scroll top                  # Scroll to top
surf scroll bottom               # Scroll to bottom
surf wait 2                      # Wait 2 seconds
```

## Element References

`surf read` returns an accessibility tree with stable element refs:

```
link "Learn more" [e1] href="https://example.com"
button "Submit" [e2] [cursor=pointer]
textbox "Email" [e3] [cursor=pointer]
heading "Welcome" [e4] [level=1]
```

Use these refs with other commands:
- `surf click e1` - Click the link
- `surf type "hello" --ref e3` - Type into the textbox

## CDP Management

```bash
surf cdp start              # Start Chrome with CDP (port 9222)
surf cdp start 9223         # Use custom port
surf cdp status             # Show status and connection info
surf cdp env                # Output export commands for shell
surf cdp stop               # Stop Chrome
```

For Puppeteer/testing integration:

```bash
eval "$(surf cdp env)"
# Now BROWSERLESS_DISCOVERY_URL and BROWSERLESS_WS are set
```

## Environment Variables

| Variable           | Default                 | Description                   |
| ------------------ | ----------------------- | ----------------------------- |
| `CDP_PORT`         | 9222                    | Chrome DevTools Protocol port |
| `CHROME_USER_DATA` | /tmp/chrome-cdp-profile | Chrome profile directory      |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        surf skill (run.sh)                       │
├─────────────────────────────────────────────────────────────────┤
│                              │                                   │
│            ┌─────────────────┴─────────────────┐                 │
│            │    /tmp/surf.sock exists?         │                 │
│            └─────────────────┬─────────────────┘                 │
│                    YES │              │ NO                       │
│                        ▼              ▼                          │
│  ┌─────────────────────────┐  ┌─────────────────────────┐       │
│  │   surf-cli extension    │  │    CDP Controller       │       │
│  │   (native/cli.cjs)      │  │  (cdp_controller.py)    │       │
│  └───────────┬─────────────┘  └───────────┬─────────────┘       │
│              │                            │                      │
│              ▼                            ▼                      │
│  ┌─────────────────────────┐  ┌─────────────────────────┐       │
│  │ Unix Socket → Native    │  │   CDP WebSocket         │       │
│  │ Host → Extension        │  │   (port 9222)           │       │
│  └───────────┬─────────────┘  └───────────┬─────────────┘       │
│              │                            │                      │
│              └────────────┬───────────────┘                      │
│                           ▼                                      │
│                  ┌─────────────────┐                             │
│                  │     Chrome      │                             │
│                  └─────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

## Example: Automate Google Search

```bash
surf cdp start
surf go "https://google.com"
surf read
# Output shows: textbox "Search" [e1] ...
surf type "claude ai" --ref e1
surf key Enter
surf wait 2
surf read
# Shows search results with element refs
surf click e3  # Click first result
surf snap      # Screenshot
surf cdp stop
```

## Troubleshooting

| Problem                    | Solution                                        |
| -------------------------- | ----------------------------------------------- |
| "Cannot connect to CDP"    | Run `surf cdp start` first                      |
| Chrome not found           | Install Google Chrome or Chromium               |
| Port already in use        | `surf cdp stop` then `surf cdp start`           |
| Element not found          | Run `surf read` first to get current refs       |
| Page not loading           | Check URL is valid, try with `https://`         |
| Empty read output          | Page may still be loading - try `surf wait 2`   |

## Extension Setup (One-time)

**Important:** Google Chrome blocks `--load-extension` for security. Manual setup required:

1. Build extension:
   ```bash
   cd /home/graham/workspace/experiments/surf-cli
   npm install && npm run build
   ```

2. Load in Chrome: `chrome://extensions` → Enable Developer Mode → Load unpacked → select `dist/`

3. Copy the Extension ID shown (e.g., `lgamnnedgnehjplhndkkhojhbifgpcdp`)

4. Install native host:
   ```bash
   surf install <extension-id>
   ```

5. Verify: `surf tab.list` should show your browser tabs

The socket at `/tmp/surf.sock` enables CLI ↔ extension communication.

## Extension vs CDP Comparison

| Feature | Extension | CDP |
|---------|-----------|-----|
| Basic navigation | ✓ | ✓ |
| Element interaction | ✓ | ✓ |
| Screenshots | ✓ | ✓ |
| Multi-tab management | ✓ | Limited |
| Use existing browser | ✓ | ✗ |
| Zero setup | ✗ | ✓ |

**Recommendation:** Set up the extension once for best experience. Use CDP for CI/testing environments where you need a fresh browser.
