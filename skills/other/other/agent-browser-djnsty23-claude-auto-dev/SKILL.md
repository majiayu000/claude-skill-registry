---
name: agent-browser
description: Browser automation CLI for AI agents. 5-6x more token-efficient than Playwright MCP. Use for browser testing and web automation.
triggers:
  - browser
  - agent-browser
  - web test
  - ui test
allowed-tools: Bash
model: opus
user-invocable: true
---

# agent-browser

Headless browser automation CLI designed for AI agents. Uses Rust CLI + Node.js daemon (Playwright under the hood).

**Why use this instead of Playwright MCP:**
- 5-6x less token consumption (~1,400 vs ~7,800 tokens for 6 tests)
- No MCP tool schema overhead (~95 tokens vs ~13,647 tokens)
- Snapshot + Refs system instead of full DOM dumps

---

## Installation

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
```

### Windows Note
On Windows, brief console windows may appear when launching the browser. This is a Chromium platform limitation - the testing still works correctly. Use `--headed` mode if you prefer seeing the browser window intentionally.

---

## Core Workflow

```bash
# 1. Open page
agent-browser open http://localhost:3000

# 2. Get interactive elements with refs
agent-browser snapshot -i

# 3. Interact using refs (@e1, @e2, etc.)
agent-browser click @e1
agent-browser fill @e2 "test@example.com"

# 4. Re-snapshot after page changes
agent-browser snapshot -i

# 5. Close when done
agent-browser close
```

---

## Command Reference

### Navigation
```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Refresh page
agent-browser close           # Close browser
```

### Snapshots (Key Feature)
```bash
agent-browser snapshot        # Full accessibility tree
agent-browser snapshot -i     # Interactive elements only (recommended)
agent-browser snapshot -c     # Compact output
agent-browser snapshot -d 3   # Limit depth to 3
agent-browser snapshot -i -c  # Interactive + compact (best for testing)
```

### Interactions (use refs from snapshot)
```bash
agent-browser click @e1              # Click element
agent-browser dblclick @e1           # Double-click
agent-browser fill @e2 "text"        # Clear and type
agent-browser type @e2 "text"        # Type without clearing
agent-browser press Enter            # Press key
agent-browser hover @e1              # Hover
agent-browser check @e1              # Check checkbox
agent-browser uncheck @e1            # Uncheck checkbox
agent-browser select @e1 "value"     # Select dropdown option
agent-browser scroll down 500        # Scroll page
agent-browser drag @e1 @e2           # Drag and drop
agent-browser upload @e1 file.pdf    # Upload file
```

### Getting Data
```bash
agent-browser get text @e1           # Get element text
agent-browser get html @e1           # Get innerHTML
agent-browser get value @e1          # Get input value
agent-browser get attr @e1 href      # Get attribute
agent-browser get title              # Page title
agent-browser get url                # Current URL
agent-browser get count "selector"   # Count matching elements
```

### State Checks
```bash
agent-browser is visible @e1         # Check visibility
agent-browser is enabled @e1         # Check if enabled
agent-browser is checked @e1         # Check checkbox state
```

### Waiting
```bash
agent-browser wait @e1               # Wait for element
agent-browser wait 2000              # Wait milliseconds
agent-browser wait --text "Success"  # Wait for text
agent-browser wait --url "**/dash"   # Wait for URL pattern
agent-browser wait --load networkidle # Wait for network idle
```

### Semantic Locators (alternative to refs)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" fill "query"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

### Screenshots & Recording
```bash
agent-browser screenshot page.png         # Screenshot
agent-browser screenshot --full page.png  # Full page
agent-browser record start ./demo.webm    # Start recording
agent-browser record stop                 # Stop recording
```

### Console & Errors
```bash
agent-browser console              # View console messages
agent-browser console --clear      # Clear console
agent-browser errors               # View page errors
agent-browser errors --clear       # Clear errors
```

### Browser Settings
```bash
agent-browser set viewport 1920 1080       # Set viewport
agent-browser set device "iPhone 14"       # Emulate device
agent-browser set media dark               # Dark mode
agent-browser set offline on               # Offline mode
agent-browser set geo 37.7749 -122.4194    # Geolocation
```

### Cookies & Storage
```bash
agent-browser cookies                      # Get all cookies
agent-browser cookies set name value       # Set cookie
agent-browser cookies clear                # Clear cookies
agent-browser storage local                # Get localStorage
agent-browser storage local set key value  # Set localStorage
```

### Network
```bash
agent-browser network requests             # View tracked requests
agent-browser network requests --filter api # Filter requests
agent-browser network route "**/api" --abort # Block requests
agent-browser network route "**/api" --body '{"mock":true}' # Mock response
```

### Tabs & Windows
```bash
agent-browser tab                # List tabs
agent-browser tab new [url]      # New tab
agent-browser tab 1              # Switch to tab 1
agent-browser tab close          # Close current tab
agent-browser window new         # New window
```

### Frames & Dialogs
```bash
agent-browser frame "iframe"     # Switch to iframe
agent-browser frame main         # Back to main frame
agent-browser dialog accept      # Accept dialog
agent-browser dialog dismiss     # Dismiss dialog
```

### Sessions (parallel browser instances)
```bash
agent-browser --session agent1 open site.com  # Named session
agent-browser session list                    # List sessions
AGENT_BROWSER_SESSION=agent1 agent-browser click @e1
```

### Auth State Persistence
```bash
agent-browser state save auth.json    # Save auth state
agent-browser state load auth.json    # Load auth state
```

---

## Test Patterns

### Login Flow
```bash
agent-browser open http://localhost:3000/login
agent-browser snapshot -i
agent-browser fill @e2 "test@example.com"    # Email field
agent-browser fill @e3 "password123"         # Password field
agent-browser click @e4                      # Login button
agent-browser wait --url "**/dashboard"
agent-browser snapshot -i
agent-browser get text @e1                   # Verify welcome message
```

### Form Validation
```bash
agent-browser open http://localhost:3000/form
agent-browser snapshot -i
agent-browser click @e5                      # Submit empty form
agent-browser wait --text "required"         # Wait for validation
agent-browser snapshot -i                    # Check error messages
agent-browser errors                         # Check console for errors
```

### E2E Flow
```bash
# Save auth state after login
agent-browser state save ./test-auth.json

# Reuse in subsequent tests
agent-browser state load ./test-auth.json
agent-browser open http://localhost:3000/protected
```

---

## Comparison vs Playwright MCP

| Feature | agent-browser | Playwright MCP |
|---------|---------------|----------------|
| Token usage | ~1,400/6 tests | ~7,800/6 tests |
| Tool definitions | ~95 tokens | ~13,647 tokens |
| Setup | npm install, CLI | MCP config required |
| Chromium | Yes | Yes |
| Firefox/Safari | No | Yes |
| Network interception | Basic | Full |
| Multi-tab | Yes | Yes |
| PDF generation | No | Yes |

**Use agent-browser for:** UI testing, form validation, navigation flows, auth testing

**Use Playwright MCP for:** Cross-browser testing, complex network mocking, PDF generation

---

## Debugging

### Headed Mode (see browser)
```bash
agent-browser open http://localhost:3000 --headed
```

### Trace Recording
```bash
agent-browser trace start ./trace.zip
# ... perform actions ...
agent-browser trace stop
# Open trace.zip in Playwright Trace Viewer
```

### Highlight Element
```bash
agent-browser highlight @e1   # Visual highlight in headed mode
```
