---
name: ui-testing
description: |
  Browser automation skill for UI testing via Chrome MCP tools. Use when:
  (1) QA Agent needs to verify UI visually or test interactions,
  (2) UI/UX Designer needs to check responsive design or component states,
  (3) Frontend Dev needs quick visual verification during development,
  (4) Test Writer needs to document user flows with screenshots/GIFs,
  (5) Any agent needs to test web interfaces, record demos, or debug UI issues.
  Capabilities: screenshots, interaction testing, accessibility checks, GIF recording,
  responsive testing, console/network debugging.
---

# UI Testing Skill

Browser automation for UI verification using Chrome MCP tools.

## Quick Reference

| Task | Tool | Key Parameters |
|------|------|----------------|
| Screenshot | `computer` | `action: "screenshot"` |
| Click | `computer` | `action: "left_click", coordinate: [x,y]` or `ref: "ref_1"` |
| Type | `computer` | `action: "type", text: "..."` |
| Find element | `find` | `query: "search button"` |
| Read page | `read_page` | `filter: "interactive"` or `"all"` |
| Navigate | `navigate` | `url: "https://..."` |
| Resize | `resize_window` | `width: 1920, height: 1080` |
| Record GIF | `gif_creator` | `action: "start_recording"` |
| Console | `read_console_messages` | `pattern: "error"` |
| Network | `read_network_requests` | `urlPattern: "/api/"` |

All tools prefixed with `mcp__claude-in-chrome__`.

## Workflow: Visual Testing

### 1. Setup Test Session

```
1. tabs_context_mcp (createIfEmpty: true)
2. tabs_create_mcp  → get new tabId
3. navigate (url: target_url, tabId: {tab})
4. computer (action: "wait", duration: 2, tabId: {tab})
5. computer (action: "screenshot", tabId: {tab})
```

### 2. Responsive Testing

Test at standard breakpoints:

| Device | Width | Height |
|--------|-------|--------|
| Mobile | 375 | 667 |
| Tablet | 768 | 1024 |
| Desktop | 1440 | 900 |
| Wide | 1920 | 1080 |

```
1. resize_window (width: 375, height: 667, tabId: {tab})
2. computer (action: "wait", duration: 1, tabId: {tab})
3. computer (action: "screenshot", tabId: {tab})
4. Repeat for other breakpoints
```

### 3. Component State Testing

Test hover, active, focus states:

```
# Hover state
1. find (query: "submit button", tabId: {tab})
2. computer (action: "hover", ref: "ref_X", tabId: {tab})
3. computer (action: "screenshot", tabId: {tab})

# Focus state (tab to element)
4. computer (action: "key", text: "Tab", tabId: {tab})
5. computer (action: "screenshot", tabId: {tab})

# Click state
6. computer (action: "left_click", ref: "ref_X", tabId: {tab})
7. computer (action: "screenshot", tabId: {tab})
```

## Workflow: Interaction Testing

### Form Testing

```
1. find (query: "email input", tabId: {tab})
2. computer (action: "left_click", ref: "ref_X", tabId: {tab})
3. computer (action: "type", text: "test@example.com", tabId: {tab})
4. computer (action: "key", text: "Tab", tabId: {tab})  # Move to next field
5. computer (action: "type", text: "password123", tabId: {tab})
6. computer (action: "screenshot", tabId: {tab})  # Capture filled form
7. find (query: "submit button", tabId: {tab})
8. computer (action: "left_click", ref: "ref_Y", tabId: {tab})
9. computer (action: "wait", duration: 2, tabId: {tab})
10. computer (action: "screenshot", tabId: {tab})  # Capture result
```

### Navigation Testing

```
1. find (query: "navigation menu", tabId: {tab})
2. computer (action: "left_click", ref: "ref_X", tabId: {tab})
3. computer (action: "wait", duration: 1, tabId: {tab})
4. computer (action: "screenshot", tabId: {tab})
5. Check URL changed: read_page to verify content
```

### Error State Testing

```
# Test validation errors
1. find (query: "email input", tabId: {tab})
2. computer (action: "left_click", ref: "ref_X", tabId: {tab})
3. computer (action: "type", text: "invalid-email", tabId: {tab})
4. computer (action: "key", text: "Tab", tabId: {tab})
5. computer (action: "screenshot", tabId: {tab})  # Capture error state
6. read_page (tabId: {tab})  # Verify error message in DOM
```

## Workflow: Accessibility Testing

### Read Accessibility Tree

```
1. read_page (tabId: {tab}, filter: "all")
   → Returns full a11y tree with roles, names, states

2. read_page (tabId: {tab}, filter: "interactive")
   → Returns only interactive elements (buttons, links, inputs)
```

### Accessibility Checklist

| Check | How to Verify |
|-------|---------------|
| All buttons have labels | `read_page` → check button names not empty |
| Images have alt text | `read_page` → check img elements have names |
| Form inputs have labels | `read_page` → verify input descriptions |
| Focus visible | Tab through elements, screenshot each |
| Color contrast | Visual inspection of screenshots |
| Keyboard navigable | Use `key: "Tab"` to traverse |

### Keyboard Navigation Test

```
1. computer (action: "key", text: "Tab", tabId: {tab})
2. computer (action: "screenshot", tabId: {tab})  # Focus indicator visible?
3. Repeat Tab, screenshot each focused element
4. computer (action: "key", text: "Return", tabId: {tab})  # Activate element
5. computer (action: "screenshot", tabId: {tab})
```

## Workflow: GIF Recording

### Record User Flow

```
# Start recording
1. gif_creator (action: "start_recording", tabId: {tab})
2. computer (action: "screenshot", tabId: {tab})  # First frame

# Perform actions (each screenshot captures a frame)
3. computer (action: "left_click", coordinate: [x,y], tabId: {tab})
4. computer (action: "screenshot", tabId: {tab})
5. computer (action: "type", text: "...", tabId: {tab})
6. computer (action: "screenshot", tabId: {tab})
... continue flow ...

# Stop and export
7. computer (action: "screenshot", tabId: {tab})  # Last frame
8. gif_creator (action: "stop_recording", tabId: {tab})
9. gif_creator (action: "export", download: true, filename: "user-flow.gif", tabId: {tab})
```

### GIF Options

```
gif_creator (
  action: "export",
  download: true,
  filename: "demo.gif",
  options: {
    showClickIndicators: true,   # Orange circles at clicks
    showActionLabels: true,      # Labels for actions
    showProgressBar: true,       # Progress bar at bottom
    quality: 10                  # 1-30, lower = better quality
  },
  tabId: {tab}
)
```

## Workflow: Debugging

### Console Errors

```
1. read_console_messages (tabId: {tab}, onlyErrors: true)
   → Shows only errors and exceptions

2. read_console_messages (tabId: {tab}, pattern: "TypeError|ReferenceError")
   → Filter specific error types

3. read_console_messages (tabId: {tab}, pattern: "MyApp", clear: true)
   → App-specific logs, clear after reading
```

### Network Requests

```
1. read_network_requests (tabId: {tab}, urlPattern: "/api/")
   → Filter API calls only

2. read_network_requests (tabId: {tab}, limit: 50)
   → Last 50 requests

3. read_network_requests (tabId: {tab}, clear: true)
   → Clear after reading to track new requests
```

### JavaScript Execution

```
javascript_tool (
  action: "javascript_exec",
  text: "document.querySelector('.error-message')?.textContent",
  tabId: {tab}
)
```

## Test Report Format

After testing, report findings:

```markdown
## UI Test Report

**Page:** {url}
**Date:** {date}
**Tester:** {agent}

### Visual Verification
- [ ] Layout matches design spec
- [ ] Responsive at mobile (375px)
- [ ] Responsive at tablet (768px)
- [ ] Responsive at desktop (1440px)

### Interaction Testing
- [ ] Forms submit correctly
- [ ] Navigation works
- [ ] Error states display properly
- [ ] Loading states visible

### Accessibility
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Labels on all inputs
- [ ] Alt text on images

### Issues Found
| Severity | Issue | Screenshot |
|----------|-------|------------|
| High | {issue} | {screenshot_id} |

### Recommendations
- {recommendation 1}
- {recommendation 2}
```

## Tips

1. **Always get tab context first** - `tabs_context_mcp` before any operation
2. **Wait after navigation** - Pages need time to load
3. **Use `find` for elements** - More reliable than coordinates
4. **Screenshot after each action** - Captures state for verification
5. **Clear console/network** - Before testing to isolate new issues
6. **Name GIFs descriptively** - `login-flow.gif` not `recording.gif`

## Common Issues

| Problem | Solution |
|---------|----------|
| Element not found | Wait longer, check selector |
| Click missed | Use `ref` from `find` instead of coordinates |
| Page not loaded | Increase wait duration |
| GIF too large | Use fewer frames, lower quality |
| Tab invalid | Call `tabs_context_mcp` for fresh IDs |
