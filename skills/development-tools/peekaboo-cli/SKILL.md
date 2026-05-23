---
name: peekaboo-cli
description: "Peekaboo CLI for macOS screenshot capture and screen analysis. Use when capturing screenshots, analyzing application windows, or listing running applications."
durability: encoded-preference
---

# Peekaboo CLI

macOS CLI for screenshot capture and screen analysis. Installed via `brew install steipete/tap/peekaboo`.

## Image Capture

```
peekaboo image --mode window --window-id 29 --capture-focus background --path /tmp/app.png
peekaboo image --mode screen --path /tmp/screenshot.png
peekaboo image --mode frontmost --path /tmp/front.png
```

Key options:
- `--mode`: auto | screen | window | frontmost | menu
- `--app`: Target application name (for window mode)
- `--window-id`: Target specific window by ID (from `peekaboo list windows`)
- `--window-title`: Target specific window by title
- `--capture-focus`: auto | foreground | background
- `--path`: Output file path
- `--retina`: High-resolution capture
- `--format`: png (default) | jpg

### Window Selection Rule

**CRITICAL**: Apps like Chrome have many helper windows (toolbars, popups) that are tiny (e.g. 3440x24). Using `--app "Google Chrome"` alone often captures a helper window instead of the actual browser window, resulting in a blank/white image.

**Always use this two-step approach for window captures:**

1. List windows to find the correct one:
   ```
   peekaboo list windows --app "Google Chrome"
   ```
2. Use `--window-id` to capture the right window:
   ```
   peekaboo image --mode window --window-id <ID> --capture-focus background --path /tmp/chrome.png
   ```

Look for the window with a meaningful title and reasonable size (e.g. 1440x875), not Untitled windows with tiny sizes.

### Browser Capture Focus Rule

**CRITICAL**: Always use `--capture-focus background` for browser captures (Chrome, Safari, Firefox, Arc, etc.). The `auto` and `foreground` modes bring the browser to foreground, which causes the page to scroll back to the top. This loses the user's scroll position.

For non-browser applications, `auto` (default) is usually fine.

## See (UI Accessibility Snapshot)

Returns UI element tree with text content. Useful when you need to read text, not view images.

```
peekaboo see --app Safari
peekaboo see --mode screen
peekaboo see --app "Google Chrome" --json
```

Note: `see` cannot show images or visual content — only text and UI element structure.

## List

```
peekaboo list                              # List all apps (default)
peekaboo list apps                         # List running applications
peekaboo list windows --app "Safari"       # List windows for an app
peekaboo list screens                      # List displays
peekaboo list permissions                  # Check permissions
peekaboo list menubar                      # List menu bar items
```

## Common Scenarios

### Capture specific app window
```
peekaboo list windows --app "Google Chrome"     # Find window ID with meaningful title
peekaboo image --mode window --window-id 29 --capture-focus background --path /tmp/chrome.png
```
Then use the Read tool to analyze the image.

### Read text from an app (no screenshot needed)
```
peekaboo see --app "Google Chrome"
```
Returns accessibility tree with visible text — sufficient when you only need text, not images.

### Full screen capture
```
peekaboo image --mode screen --path /tmp/screen.png
```

### Specific window by title
```
peekaboo image --mode window --app "Google Chrome" --window-title "Gmail" --capture-focus background --path /tmp/gmail.png
```

## Privacy Rules

**CRITICAL**: NEVER use `--analyze` or `--provider` flags. These send data to external LLMs.

Always use the Read tool for image analysis. Claude can analyze images directly without external services.

## Permission Requirements

Peekaboo requires TWO separate macOS permissions:
1. **Accessibility** (System Settings > Privacy & Security): Window listing and focus management
2. **Screen Recording** (System Settings > Privacy & Security): Actual pixel capture

Both must be granted. Accessibility alone is NOT sufficient. Terminal may need restart after granting.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Blank/white/tiny image | Captured a helper window instead of the real one | Use `peekaboo list windows --app` to find the correct window ID, then `--window-id` |
| "No capturable windows" | Window on different Space | Ask user to switch Space or move window |
| Blank/black image | Screen Recording permission missing | Guide to System Settings > Privacy & Security > Screen Recording |
| "Not trusted" | Accessibility permission missing | Guide to System Settings > Privacy & Security > Accessibility |
| "Application not found" | Wrong app name | Run `peekaboo list apps` to find exact name |
| File save failed | Directory doesn't exist | Use /tmp/ as fallback |
