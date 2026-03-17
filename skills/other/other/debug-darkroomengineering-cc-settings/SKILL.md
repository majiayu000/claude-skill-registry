---
name: debug
description: |
  Browser debugging with agent-browser CLI. Use when:
  - User mentions "screenshot", "visual bug", "inspect element"
  - User asks "what does it look like", "see the page"
  - Need to debug browser rendering, layout, or visual issues
  - User wants to test UI in browser
  - E2E debugging or visual verification
context: fork
allowed-tools: [Bash]
---

# Browser Debugging with agent-browser

AI-optimized browser automation for visual debugging.

## Commands

```bash
# Navigate to a URL
agent-browser navigate http://localhost:3000

# Take screenshot
agent-browser screenshot

# Get accessibility tree (AI-optimized DOM)
agent-browser snapshot

# Click element by accessibility ref
agent-browser click @e5

# Type text
agent-browser type @e3 "search query"

# Get page info
agent-browser info
```

## Workflow

1. **Navigate** to the target URL
2. **Screenshot** to see current state
3. **Snapshot** to get accessibility tree with element refs
4. **Interact** using element refs (@e1, @e2, etc.)
5. **Screenshot** again to verify changes

## Element References

The accessibility tree gives each element a unique ref:

```
@e1: button "Submit"
@e2: textbox "Email"
@e3: link "Home"
```

Use these refs for reliable element targeting.

## Common Debugging Tasks

### Visual Bug
```bash
agent-browser navigate http://localhost:3000/broken-page
agent-browser screenshot
# Analyze screenshot for visual issues
```

### Interactive Testing
```bash
agent-browser navigate http://localhost:3000/form
agent-browser snapshot
agent-browser type @e2 "test@example.com"
agent-browser click @e5
agent-browser screenshot
```

### Layout Inspection
```bash
agent-browser navigate http://localhost:3000
agent-browser snapshot
# Analyze accessibility tree for structure
```

## Prerequisites

Requires `agent-browser` CLI:
```bash
npm i -g agent-browser@0.8.3
```

## Output

Return findings:
- **Visual state**: What the page looks like
- **Issues found**: Layout problems, missing elements
- **Accessibility tree**: Key element structure
- **Recommendations**: How to fix issues
