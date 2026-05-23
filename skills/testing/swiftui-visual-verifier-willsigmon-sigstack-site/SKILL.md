---
name: SwiftUI Visual Verifier
description: Launch Leavn app in iOS simulator, navigate features using MCP browser tools, take screenshots, verify UI rendering and feature functionality
allowed-tools: Bash, mcp__plugin_testing-suite_playwright-server__*
---

# SwiftUI Visual Verifier

## Instructions

Visually verify Leavn app features:

1. **Build and launch**:
   ```bash
   make sim-run DEVICE="LeavnTest"
   ```

2. **Use browser MCP tools** to interact:
   - `browser_snapshot` - Get accessibility tree
   - `browser_click` - Tap buttons/tabs
   - `browser_take_screenshot` - Capture UI
   - `browser_type` - Enter text in search
   - `browser_wait_for` - Wait for animations

3. **Test critical features**:
   - Home tab: Feelings picker circle, daily verse card
   - Bible: Chapter rendering, search (type "love")
   - Community: Prayer wall, tabs
   - ShareVerse: Tap share, verify popover

4. **Visual checks**:
   - No truncated text
   - Proper spacing/alignment
   - Correct colors/gradients
   - Smooth animations
   - Responsive layouts

5. **Create test report**:
   - Feature: PASS/FAIL
   - Screenshots showing working features
   - List any visual bugs found

Use this skill when: Need visual verification, test features work, check UI rendering, verify user flows
