---
description: Pick the terminal background color Ralph uses to distinguish its terminal from Claude Code.
---

# Terminal Color

The user wants to change Ralph's terminal background tint - the color applied during `npx agentic-loop run` to visually distinguish Ralph's terminal from Claude Code.

> **Note:** This only works in macOS Terminal.app. On other terminals (iTerm2, VS Code, Linux), Ralph skips tinting automatically.

## Step 1: Show Current Color

Read `.ralph/config.json` and check for `terminalTint`. Show the current setting:
- If set: "Current tint: `{value}`"
- If not set: "Current tint: `#1a1a2e` (default dark navy)"

## Step 2: Ask Color Preference

Use AskUserQuestion:

**Question:** "What color should Ralph's terminal background be?"
**Header:** "Tint color"
**Options:**
- **Dark Navy (default)** - "`#1a1a2e` - cool and distinct, easy on the eyes"
- **Dark Teal** - "`#1a2e2e` - subtle blue-green undertone"
- **Dark Red** - "`#2e1a1a` - warm undertone, clearly different"
- **Off** - "Disable terminal tinting entirely"

If the user selects "Other", ask them to provide a hex color (e.g., `#2e2e1a`).

## Step 3: Validate (if custom hex)

If the user provided a custom hex:
- Must match `#` followed by exactly 6 hex characters (`/^#[0-9a-fA-F]{6}$/`)
- If invalid, say "That doesn't look like a valid hex color (e.g., `#1a1a2e`). Try again." and re-ask.

## Step 4: Save to Config

Read `.ralph/config.json`, set the `terminalTint` field, and write it back.

- **If a color was chosen:** Set `"terminalTint": "#xxxxxx"`
- **If "Off" was chosen:** Set `"terminalTint": "off"`

Use jq to update:
```bash
jq --arg color "THE_HEX_VALUE" '.terminalTint = $color' .ralph/config.json > .ralph/config.json.tmp && mv .ralph/config.json.tmp .ralph/config.json
```

## Step 5: Preview (macOS Terminal.app only)

If running in Terminal.app, apply the color immediately so the user can see it:

```bash
# Apply preview (will be restored when Claude session ends)
osascript -e 'tell application "Terminal" to set background color of front window to {R, G, B}' 2>/dev/null
```

Where R, G, B are the hex values converted to 16-bit (multiply each 8-bit value by 257).

If "Off" was chosen, skip the preview.

## Step 6: Confirm

Say:

"Done! Ralph will use `#xxxxxx` as the terminal tint.

Next time you run `npx agentic-loop run`, the terminal background will change to this color. It restores to your original background when the loop ends.

Run `/color` again anytime to change it."

If "Off" was chosen, say:

"Done! Terminal tinting is now disabled. Ralph will run without changing your terminal background."
