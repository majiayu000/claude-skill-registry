---
name: agent-browser
description: Browser automation and testing using Vercel's agent-browser CLI with ref-based element targeting
triggers:
  - browser testing
  - web automation
  - UI testing
  - e2e testing
  - screenshot
  - form filling
  - web scraping
  - page interaction
  - accessibility testing
---

# Agent Browser Testing Skill

Browser automation and end-to-end testing using Vercel's agent-browser CLI. Uses ref-based element targeting for reliable, AI-friendly browser interaction.

## Quick Decision Tree

```
What do you need?
│
├─ Take a screenshot of a page?
│  └─ agent-browser open [url] && agent-browser screenshot
│
├─ Fill out a form?
│  └─ open → snapshot -i → fill @ref → click @submit → snapshot
│
├─ Test a login flow?
│  └─ See references/authentication.md
│
├─ Run an E2E test?
│  └─ See references/testing-patterns.md
│
├─ Scrape page content?
│  └─ agent-browser open [url] && agent-browser snapshot -i
│
└─ Debug element targeting?
   └─ agent-browser snapshot -i --format json
```

## Installation

```bash
# Install agent-browser globally
npm install -g agent-browser

# Install browser dependencies (Chromium)
agent-browser install

# Verify installation
agent-browser --version
```

## Core Concept: Ref-Based Targeting

Agent-browser uses **refs** (like `@e1`, `@e2`, `@e3`) to identify interactive elements on the page. These refs are assigned when you take a snapshot.

```bash
# Take a snapshot with interactive elements labeled
agent-browser snapshot -i

# Output shows refs:
# @e1: [button] "Sign In"
# @e2: [input] Email field
# @e3: [input] Password field
# @e4: [button] "Submit"

# Use refs to interact
agent-browser click @e1
agent-browser fill @e2 "user@example.com"
```

**Important:** Refs are session-specific and invalidate when the page changes. Always re-snapshot after navigation or DOM updates.

## Essential Workflow

```bash
# 1. Open the target URL
agent-browser open https://example.com

# 2. Take a snapshot to see the page and get refs
agent-browser snapshot -i

# 3. Interact with elements using refs
agent-browser click @e1
agent-browser fill @e2 "test value"

# 4. Take another snapshot to verify changes
agent-browser snapshot -i
```

## Common Commands Quick Reference

### Navigation
```bash
agent-browser open <url>              # Navigate to URL
agent-browser back                    # Go back
agent-browser forward                 # Go forward
agent-browser refresh                 # Reload page
```

### Snapshots
```bash
agent-browser snapshot                # Text snapshot
agent-browser snapshot -i             # With interactive refs
agent-browser snapshot --format json  # JSON output
agent-browser screenshot [path]       # Save screenshot
```

### Interaction
```bash
agent-browser click @ref              # Click element
agent-browser fill @ref "value"       # Fill input field
agent-browser select @ref "option"    # Select dropdown option
agent-browser hover @ref              # Hover over element
agent-browser press Enter             # Press keyboard key
```

### Semantic Locators
```bash
agent-browser find role button "Submit"    # Find by ARIA role
agent-browser find text "Welcome"          # Find by visible text
agent-browser find label "Email"           # Find by label
```

### Waiting
```bash
agent-browser wait visible @ref            # Wait for element visible
agent-browser wait hidden @ref             # Wait for element hidden
agent-browser wait network                 # Wait for network idle
agent-browser wait time 2000               # Wait milliseconds
```

### Session Management
```bash
agent-browser session save mystate         # Save browser state
agent-browser session load mystate         # Load saved state
agent-browser session list                 # List saved sessions
agent-browser close                        # Close browser
```

## Security Notes

**Never commit these files:**
- `*.state` - Browser session state files contain cookies
- `agent-browser-profile/` - Profile directories with credentials
- Screenshots that may contain sensitive data

Add to `.gitignore`:
```gitignore
*.state
agent-browser-profile/
.agent-browser/
screenshots/
```

## Integration with Other Skills

### With Parallel Research
```bash
# Research a topic, then verify claims on websites
parallel_research.py chat "Find pricing for Acme Corp"
# Then use agent-browser to verify on their actual pricing page
agent-browser open https://acme.com/pricing
agent-browser snapshot -i
```

### With Screenshot Comparison
```bash
# Take baseline screenshots for visual regression
agent-browser open https://myapp.com
agent-browser screenshot baseline.png

# After changes, compare
agent-browser screenshot current.png
# Use image comparison tool
```

### With Form Data from Sheets
```python
# Load test data from Google Sheets, run form tests
import subprocess
test_data = get_sheet_data("Form Test Cases")
for row in test_data:
    subprocess.run(["agent-browser", "fill", "@email", row["email"]])
    subprocess.run(["agent-browser", "fill", "@password", row["password"]])
    subprocess.run(["agent-browser", "click", "@submit"])
```

## Files in This Skill

- `references/commands.md` - Full command reference
- `references/authentication.md` - Login flow patterns
- `references/testing-patterns.md` - E2E test workflows
- `references/snapshot-workflow.md` - Ref system deep dive
- `scripts/browser_test.py` - Python automation wrapper

## Example: Complete Form Test

```bash
# Open the registration page
agent-browser open https://example.com/register

# Get element refs
agent-browser snapshot -i

# Fill the form (refs from snapshot output)
agent-browser fill @e1 "John Doe"
agent-browser fill @e2 "john@example.com"
agent-browser fill @e3 "SecurePass123!"
agent-browser select @e4 "United States"
agent-browser click @e5  # Terms checkbox
agent-browser click @e6  # Submit button

# Wait for navigation and verify
agent-browser wait network
agent-browser snapshot -i

# Take confirmation screenshot
agent-browser screenshot registration-success.png
```

## Troubleshooting

**Element not found:**
- Re-run `snapshot -i` to get fresh refs
- Use semantic locators: `agent-browser find text "Submit"`
- Check if element is in an iframe

**Page not loading:**
- Increase timeout: `agent-browser open <url> --timeout 30000`
- Wait for network: `agent-browser wait network`

**Session expired:**
- Save state before tests: `agent-browser session save backup`
- Load state to restore: `agent-browser session load backup`
