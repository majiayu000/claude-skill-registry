---
name: chrome-gif-recorder
description: "Records browser workflows as annotated GIFs for documentation and tutorials. Use when creating visual documentation of browser interactions, recording step-by-step tutorials, or capturing workflows for support tickets. Triggers on phrases like 'record this workflow', 'create a GIF tutorial', 'document this process as GIF', 'show me how to do X as a GIF', or when user needs visual step-by-step documentation. Works with Chrome browser automation via MCP tools (tabs_context_mcp, gif_creator, computer)."
---

# Chrome GIF Recorder

## Overview

Record browser workflows as annotated GIFs with visual indicators for clicks, drags, and actions. Produces professional documentation-ready GIFs with automatic frame capture, action annotations, and quality optimization.

## When to Use This Skill

Use when asked to:
- Create visual documentation of browser workflows ("record this as a GIF tutorial")
- Generate step-by-step tutorials for web applications
- Capture user flows for support tickets or bug reports
- Document repetitive processes for training materials
- Create annotated screen recordings with click indicators

Do NOT use when:
- User needs static screenshots (use screenshot tool instead)
- Recording requires audio narration (this is visual-only)
- User needs long-form video (GIFs are best under 60 seconds)

## Workflow

### 1. Get Tab Context

Always start by getting tab context to identify available tabs:

```
tabs_context_mcp with createIfEmpty: true
```

This ensures you have a valid tabId for all subsequent operations.

### 2. Present Plan to User

Use `update_plan` to show the user what domains you'll visit and what actions you'll take:

```
update_plan with:
  domains: ["example.com", "app.example.com"]
  approach: [
    "Navigate to login page",
    "Fill in credentials",
    "Click submit button",
    "Navigate to dashboard"
  ]
```

Wait for user approval before proceeding.

### 3. Start Recording

Begin GIF recording immediately before workflow execution:

```
gif_creator with:
  action: "start_recording"
  tabId: <tab-id>
```

### 4. Capture First Frame (CRITICAL)

**Immediately after starting recording**, take a screenshot to capture the initial state:

```
computer with:
  action: "screenshot"
  tabId: <tab-id>
```

This ensures the GIF has a proper first frame showing the starting state.

### 5. Execute Workflow Steps

Perform the documented workflow using browser automation tools:

- `navigate` - Navigate to URLs
- `computer` with `left_click` - Click elements
- `form_input` - Fill form fields
- `computer` with `type` - Type text
- `computer` with `scroll` - Scroll pages
- `computer` with `wait` - Pause between actions

**Timing guidance:**
- Add 1-2 second waits between major actions for clarity
- Keep total workflow under 60 seconds for optimal GIF size
- Use natural pacing (not too fast, not too slow)

### 6. Capture Last Frame (CRITICAL)

**Immediately before stopping recording**, take a screenshot to capture the final state:

```
computer with:
  action: "screenshot"
  tabId: <tab-id>
```

This ensures the GIF has a proper last frame showing the end result.

### 7. Stop Recording

Stop the recording after capturing the last frame:

```
gif_creator with:
  action: "stop_recording"
  tabId: <tab-id>
```

### 8. Export with Annotations

Export the GIF with visual enhancements enabled:

```
gif_creator with:
  action: "export"
  tabId: <tab-id>
  download: true
  filename: "workflow-tutorial-<timestamp>.gif"
  options: {
    showClickIndicators: true,
    showDragPaths: true,
    showActionLabels: true,
    showProgressBar: true,
    showWatermark: true,
    quality: 10
  }
```

**Quality settings:**
- `quality: 5` - Fastest encoding, larger file (good for quick previews)
- `quality: 10` - Balanced (recommended default)
- `quality: 20` - Higher quality, slower encoding
- `quality: 30` - Best quality, slowest encoding

### 9. Confirm Download

The GIF will be downloaded to the user's default downloads folder. Confirm the filename and location with the user.

## Best Practices

### Frame Capture Anti-Pattern

**CRITICAL:** Always capture screenshots immediately after `start_recording` and immediately before `stop_recording`.

**Why:** The gif_creator tool requires explicit screenshots to create GIF frames. Without these critical screenshots:
- First frame may be missing or incorrect
- Last frame may not show final state
- GIF may appear incomplete or broken

**Correct pattern:**
```
1. gif_creator start_recording
2. computer screenshot  ← CRITICAL: First frame
3. [workflow actions]
4. computer screenshot  ← CRITICAL: Last frame
5. gif_creator stop_recording
6. gif_creator export
```

**Incorrect pattern (DO NOT USE):**
```
1. gif_creator start_recording
2. [workflow actions]  ← Missing first frame!
3. gif_creator stop_recording  ← Missing last frame!
4. gif_creator export
```

### Recording Duration

- **Recommended:** 30-60 seconds for most tutorials
- **Maximum:** 90 seconds (longer GIFs become unwieldy)
- **Minimum:** 10 seconds (shorter workflows may need fewer screenshots)

### Filename Conventions

Use descriptive, timestamped filenames:
- `login-workflow-2025-12-20.gif`
- `checkout-process-tutorial.gif`
- `admin-dashboard-navigation.gif`

### Annotation Options

**Enable by default:**
- `showClickIndicators: true` - Orange circles at click locations
- `showActionLabels: true` - Black text labels describing actions
- `showProgressBar: true` - Orange progress bar at bottom

**Optional:**
- `showDragPaths: true` - Red arrows for drag operations (disable if no dragging)
- `showWatermark: true` - Claude logo (disable for client deliverables)

### Quality vs. Speed Trade-offs

| Use Case | Quality Setting | Encoding Speed | File Size |
|----------|----------------|----------------|-----------|
| Quick preview | 5 | Fast | Large |
| Documentation | 10 | Moderate | Medium |
| Polished tutorial | 20 | Slow | Small |
| Final deliverable | 30 | Very slow | Smallest |

## Common Workflows

### Simple Page Navigation

```
1. tabs_context_mcp (get tabId)
2. update_plan (domains + approach)
3. gif_creator start_recording
4. computer screenshot (first frame)
5. navigate to page
6. computer wait (2 seconds)
7. computer screenshot (last frame)
8. gif_creator stop_recording
9. gif_creator export (download: true, quality: 10)
```

### Form Submission Workflow

```
1. tabs_context_mcp
2. update_plan
3. gif_creator start_recording
4. computer screenshot (first frame)
5. navigate to form
6. form_input (fill fields)
7. computer left_click (submit button)
8. computer wait (page load)
9. computer screenshot (last frame)
10. gif_creator stop_recording
11. gif_creator export
```

### Multi-Page Tutorial

```
1. tabs_context_mcp
2. update_plan (multiple domains)
3. gif_creator start_recording
4. computer screenshot (first frame)
5. navigate to page 1
6. computer left_click (action 1)
7. computer wait (1 second)
8. navigate to page 2
9. computer left_click (action 2)
10. computer wait (1 second)
11. computer screenshot (last frame)
12. gif_creator stop_recording
13. gif_creator export
```

## Troubleshooting

### GIF appears empty or has no frames

**Cause:** Missing screenshot calls after start_recording or before stop_recording

**Solution:** Always call `computer screenshot` immediately after starting and before stopping recording

### GIF encoding takes too long

**Cause:** Quality setting too high or recording too long

**Solution:**
- Reduce quality to 5-10 for faster encoding
- Keep workflows under 60 seconds
- Remove unnecessary wait times

### Annotations not visible

**Cause:** Annotation options set to false

**Solution:** Enable options in export call:
```
options: {
  showClickIndicators: true,
  showActionLabels: true,
  showProgressBar: true
}
```

### File size too large

**Cause:** Low quality setting or long recording duration

**Solution:**
- Increase quality setting to 20-30 for better compression
- Reduce recording duration
- Remove unnecessary frames/actions

## Resources

This skill uses only MCP tools and requires no bundled resources. The example directories created during initialization can be deleted:

- `scripts/` - Not needed (no automation scripts required)
- `references/` - Not needed (workflow documented in SKILL.md)
- `assets/` - Not needed (GIFs are generated, not templated)
