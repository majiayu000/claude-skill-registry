---
name: things-setup
description: Connect Things 3 to Dex for bi-directional task sync
manifest:
  id: things
  auth: none
  category: task_sync
  platform: macos
  mcp_server: things3-mcp
---

# Things 3 Setup

Connect Things 3 to Dex for bi-directional task sync. No account needed. Everything stays on your Mac. Works offline.

## What This Enables

Once connected, Dex can:
- **Task Sync:** Create tasks in Things 3 when you add them in Dex, and vice versa
- **Daily Plan:** Pull in tasks you created in Things and merge them into your plan
- **Completion Sync:** Complete a task in either place — it syncs to the other
- **Priority Mapping:** P0/P1 tasks go to your Today list, P2/P3 to Anytime
- **Pillar Mapping:** Dex pillars map to Things Areas for organized task views

## Privacy

- Everything is local. Things 3 uses AppleScript — no cloud API, no tokens, no accounts
- Tasks sync between two apps on YOUR Mac. Nothing leaves your machine
- No credentials to store. No tokens to expire. No OAuth flows
- Works completely offline

## When to Run

- User types `/things-setup`
- User asks about connecting Things 3
- User wants task sync with a Mac-native app
- During `/integrate-mcp` if Things is mentioned
- During onboarding if user mentions Things 3

---

## Setup Flow

### Step 1: Platform Check

Things 3 is macOS only. Verify:

1. Check if running on macOS (`process.platform === 'darwin'` or `uname` check)
2. **If not macOS:**
   ```
   Things 3 is a macOS-only app. It won't work on this platform.

   For cross-platform task sync, consider:
   - /todoist-setup (works everywhere)
   - /trello-setup (web-based)
   ```
   Stop here.

### Step 2: Check if Already Connected

1. Read `System/integrations/config.yaml`
2. If `things.enabled: true`, skip to **Step 7** (Reconfigure)
3. If not configured, continue

### Step 3: Check if Things 3 is Installed

Run a quick AppleScript test:

```bash
osascript -e 'tell application "System Events" to (name of processes) contains "Things3"'
```

Or check if the app exists:

```bash
ls /Applications/Things3.app 2>/dev/null || ls "$HOME/Applications/Things3.app" 2>/dev/null
```

**If Things 3 is not found:**

```
I can't find Things 3 on your Mac.

Things 3 is available from the Mac App Store:
https://apps.apple.com/app/things-3/id904280696

Once installed, run /things-setup again.
```

Stop here.

**If found:**

```
Things 3 detected. This is the simplest integration to set up — no accounts or API keys needed.

Everything stays on your Mac and works offline. Ready?
```

Wait for confirmation.

### Step 4: Add the things3-mcp Server

Check the user's MCP configuration. If `things3-mcp` is not listed:

1. Explain:

```
I need to add the Things 3 connector to your Dex configuration.

This uses a lightweight AppleScript bridge — no accounts, no API keys.
It talks directly to Things 3 on your Mac.
```

2. Add to the user's `.mcp.json`:

```json
{
  "things3-mcp": {
    "command": "npx",
    "args": ["-y", "things3-mcp"],
    "env": {}
  }
}
```

3. Tell the user the MCP server needs to restart for changes to take effect.

### Step 5: Test the Connection

Run a quick test to verify AppleScript access:

1. List Things Areas:
   ```bash
   osascript -e 'tell application "Things3" to get name of areas'
   ```

2. List Things Projects:
   ```bash
   osascript -e 'tell application "Things3" to get name of projects'
   ```

**If macOS prompts for AppleScript permission:**

```
macOS is asking for permission to control Things 3. Click "OK" to allow.

This is a one-time prompt. Things 3 uses AppleScript for local communication —
no network access is involved.
```

**Show results:**

```
Connection test passed.

Your Things 3 setup:
- Areas: [list of areas]
- Projects: [list of projects]
```

If the test fails, jump to Troubleshooting.

### Step 6: Configure Mapping

Map Dex pillars to Things Areas:

```
Now let's map your Dex pillars to Things Areas.

Your Dex pillars:
1. Deal Support
2. Thought Leadership
3. Product Feedback

Your Things Areas:
[list from Step 5]

I'll suggest a mapping — adjust if needed:

| Dex Pillar | Things Area |
|------------|-------------|
| Deal Support | [best match or "Deal Support"] |
| Thought Leadership | [best match or "Thought Leadership"] |
| Product Feedback | [best match or "Product Feedback"] |

Does this mapping look right? I can create any missing Areas in Things.
```

If areas don't exist, offer to create them:

```bash
osascript -e 'tell application "Things3" to make new area with properties {name:"Deal Support"}'
```

Then ask about sync behavior:

```
One more question: How should task sync work?

1. **Auto-sync** — Tasks sync automatically between Dex and Things
2. **Ask each time** — I'll confirm before syncing each task

Most people prefer auto-sync. Which do you want?
```

### Step 7: Save Configuration

Write to `System/integrations/config.yaml` — update the things section:

```yaml
things:
  enabled: true
  configured_at: YYYY-MM-DD
  mcp_server: things3-mcp
  auth_type: none
  task_sync: true
  sync_mode: auto
  area_mapping:
    deal_support: Deal Support
    thought_leadership: Thought Leadership
    product_feedback: Product Feedback
  features:
    task_sync: true
    external_task_merge: true
```

If the file already exists, only update the `things:` section. Preserve other integration configs.

### Step 8: Capability Cascade

Now that Things is connected, highlight what changes:

```
Things 3 is connected.

Here's what changes now:

- **/daily-plan** syncs tasks from Things into your morning plan
- **Task creation** in Dex mirrors to Things (P0/P1 → Today, P2/P3 → Anytime)
- **Task completion** syncs both ways — finish in either app
- **Pillars → Areas** keep your Things organized by Dex structure

No accounts. No tokens. No expiration. Works offline.

Tip: Tasks you create directly in Things will appear in your next /daily-plan.
```

---

## Troubleshooting

### Things 3 Not Installed

Things 3 must be installed from the Mac App Store. It's a paid app (~$49.99).
Once installed, run `/things-setup` again.

### AppleScript Permission Denied

macOS may block AppleScript access. To fix:

1. Open **System Settings** > **Privacy & Security** > **Automation**
2. Find your terminal app (Terminal, iTerm2, etc.)
3. Enable the toggle for **Things3**
4. Retry the setup

### "Things3 got an error" Messages

Things 3 must be running for AppleScript to work. Open Things 3, then retry.

### Areas Not Showing

If no Areas appear during setup:

1. Open Things 3
2. Go to Settings > General
3. Make sure Areas are enabled
4. Create at least one Area, then retry

### Sync Conflicts

If a task is edited in both Dex and Things between syncs:

- Dex is the source of truth for task status
- Things is the source of truth for task title edits
- Notes merge (Dex context is appended, not overwritten)

---

## Reconfiguration

If the user runs `/things-setup` when already configured:

1. Show current config from `System/integrations/config.yaml`
2. Offer options:
   - Update pillar-to-area mapping
   - Change sync mode (auto vs. ask)
   - Re-test the connection
   - Disconnect Things

### Disconnect Flow

If user wants to disconnect:

1. Update `System/integrations/config.yaml`:
   ```yaml
   things:
     enabled: false
   ```
2. Confirm: "Things 3 is disconnected. Tasks will no longer sync. Run `/things-setup` anytime to reconnect."
