---
name: playtest-web
description: Run visual playtesting through the web UI using Chrome automation. Catches layout bugs, state display issues, and UX problems that API testing misses.
allowed-tools: Bash, Read, Glob, Grep
user-invocable: true
proactive: false
---

# Web UI Playtest Agent

Deploy Claude to visually test SENTINEL through the Astro web interface using Chrome automation. Unlike the CLI playtest (which hits the Bridge API directly), this tests the actual rendered UI — catching CSS bugs, layout issues, and state display sync problems.

## Prerequisites

Both the Bridge and Web UI must be running:

```bash
# Terminal 1: Start the Deno bridge with Claude backend
cd sentinel-bridge && deno task start --backend claude

# Terminal 2: Start the Astro web UI
cd sentinel-ui && npm run dev
```

The web UI runs at `http://localhost:4321` and the bridge at `http://localhost:3333`.

## How to Run

When the user invokes `/playtest-web`, follow this protocol:

### Step 1: Get Browser Context

First, establish browser context and create a tab for testing:

```
1. Call tabs_context_mcp to see existing tabs
2. Call tabs_create_mcp to create a new test tab
3. Navigate to http://localhost:4321
4. Take a screenshot to verify the page loaded
```

### Step 2: Verify Services Running

Check that both services are responsive:
- Bridge health: The header should show a green status dot and "ready" state
- UI loaded: The 3-column layout (SELF / NARRATIVE / WORLD) should be visible
- No connection error: Shouldn't see "Bridge Not Connected" message

If the bridge isn't connected, the UI will show an error. Stop and inform the user to start the bridge.

### Step 3: Read the Test Protocol

Read `C:\dev\SENTINEL\.claude\skills\playtest-web\PROTOCOL.md` for the visual testing checklist.

### Step 4: Execute Visual Tests

For each test:

1. **Interact with UI** — Use form_input on command-input, click buttons
2. **Wait for response** — Take screenshots, use read_page to verify DOM updates
3. **Validate display** — Check that panels show correct values
4. **Compare states** — Use JavaScript to read window.__campaignState and compare to displayed values
5. **Document issues** — Screenshot any visual bugs or inconsistencies

### Key UI Elements

| Element ID | Purpose | Validation |
|------------|---------|------------|
| `command-input` | Text input for commands | Can type, clears after submit |
| `command-form` | Form wrapper | Shows loading state during commands |
| `char-name` | Character name display | Matches campaign state |
| `char-background` | Background display | Format: [Background] |
| `energy-fill` | Energy progress bar | Width matches percentage |
| `energy-value` | Energy percentage text | Matches campaign state |
| `credits-value` | Credits display | Format: Xc |
| `location-value` | Current location | Matches campaign state |
| `region-value` | Current region | Matches campaign state |
| `standings-list` | Faction standings | All 11 factions with bars |
| `threads-list` | Active threads | Updates on new threads |
| `loadout-list` | Gear/loadout display | Items with equipped state |
| `enhancement-list` | Enhancements display | From faction |
| `event-log` | SSE event stream | Shows recent events |
| `narrative-log` | Conversation log | User/GM messages |

### UI Interaction Patterns

**Type a command:**
```
1. find: "command input" or ref: command-input
2. form_input: set value to the command text
3. find: "SEND button"
4. computer: left_click on SEND
5. computer: wait 2-3 seconds for response
6. read_page to verify narrative log updated
```

**Use quick command buttons:**
```
1. find: "status button" (or other quick command)
2. computer: left_click
3. The command populates the input
4. Click SEND to execute
```

**Verify state display:**
```javascript
// Use javascript_tool to read internal state
const state = window.__campaignState;
return JSON.stringify({
  name: state.character?.name,
  energy: state.character?.social_energy,
  factions: state.factions?.length
});
```

### Step 5: Generate Visual Bug Report

After running tests, create a report with:

- **Screenshots** — Visual evidence of issues
- **DOM discrepancies** — Where displayed values don't match internal state
- **Layout issues** — Broken layouts, overflow, clipping
- **Interaction bugs** — Buttons that don't work, forms that don't submit
- **State sync issues** — UI not updating after commands

## What This Catches (That CLI Playtest Misses)

| Category | Example Issues |
|----------|----------------|
| **Layout** | Panels overflow, columns collapse wrong, mobile breakpoints broken |
| **Styling** | Wrong colors for standing levels, missing CSS classes, broken animations |
| **State Sync** | UI shows old values after commands, panels don't refresh |
| **Interaction** | Input focus issues, buttons unclickable, keyboard navigation broken |
| **Display Format** | Wrong number formats, truncated text, encoding issues |
| **Responsiveness** | Loading states don't show, errors don't display |

## Bug Severity Levels

- **CRITICAL**: UI completely broken, can't interact with game
- **HIGH**: State display incorrect, misleading information
- **MEDIUM**: Visual glitches, minor layout issues
- **LOW**: Polish issues, slight misalignment

## Example Report

```markdown
# Web UI Playtest Report - 2026-01-24

## Summary
- Visual tests run: 12
- Passed: 10
- Issues found: 2

## High Priority
### WEBUI-001: Energy bar doesn't update after social action
**Screenshot**: [attached]
**Steps**: 1) /start 2) Make social action 3) Check energy bar
**Expected**: Energy bar width decreases
**Actual**: Bar stays at 100% until page refresh
**Internal state**: window.__campaignState.character.social_energy.current = 85

## Medium Priority
### WEBUI-002: Faction standings truncate on narrow viewport
**Screenshot**: [attached]
**Steps**: Resize window to 1000px wide
**Expected**: Faction names abbreviate gracefully
**Actual**: Names overlap progress bars

## Test Details
[Full visual test log with screenshots...]
```

## Tips

- Always take screenshots before and after actions for comparison
- Use javascript_tool to read internal state and compare to displayed values
- Test at different viewport sizes (the UI hides sidebars at <1000px)
- Check both the visual appearance AND the DOM structure with read_page
- Watch the event-log panel — it shows SSE events which help debug sync issues
