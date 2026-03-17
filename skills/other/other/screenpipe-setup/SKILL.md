---
name: screenpipe-setup
description: Enable ambient work intelligence via screen OCR (beta feature)
version: 0.1.0
triggers:
  - /screenpipe-setup
  - /screenpipe-enable
  - enable screen capture
  - setup screenpipe
  - ambient intelligence
---

# ScreenPipe Setup

Enable ambient work intelligence - Dex learns what you're working on via screen OCR.

## Beta Gate (Check First!)

**This is a beta feature.** Before proceeding:

1. Read `System/user-profile.yaml` → Check if `beta.activated.screenpipe: true`
2. If NOT activated:
   ```
   "ScreenPipe is a beta feature. To enable it, first run:
   
   /beta-activate DEXSCREENPIPE2026
   
   Then come back and run /screenpipe-setup again."
   ```
3. Only proceed if beta is activated

## What It Does

ScreenPipe captures OCR text from your screen so you can ask things like:
- "What was I working on this morning?"
- "Summarize my work today"
- "When did I last look at the Q1 presentation?"

## Privacy Defaults (Explain to User)

**Work apps only.** Everything personal is blocked:
- ❌ All web browsers (Chrome, Safari, Firefox, Arc, Edge)
- ❌ Password managers, messaging apps, social media
- ❌ Banking, healthcare, email, entertainment, shopping
- ✅ IDEs, terminals, Slack, Notion, Figma, Calendar

**Auto-delete:** Data older than 30 days is automatically purged (configurable).

## Setup Flow

### 1. Check if Installed

```bash
which screenpipe
```

If not found:
```bash
brew install screenpipe
```

### 2. Apply Privacy Config

Write to `~/.screenpipe/config.json`:

```json
{
  "fps": 0.5,
  "disable_audio": true,
  "use_pii_removal": true,
  "ignored_apps": [
    "Safari", "Google Chrome", "Firefox", "Arc", "Brave Browser",
    "Microsoft Edge", "Opera", "Vivaldi", "Tor Browser", "DuckDuckGo",
    "1Password", "Keychain Access", "Bitwarden", "LastPass", "KeePass",
    "Messages", "WhatsApp", "Telegram", "Signal", "Discord", "FaceTime",
    "Photos", "Preview", "TV", "Music", "Podcasts", "Books", "News", "Stocks"
  ],
  "ignored_urls": [
    "google.com/search", "bing.com/search", "duckduckgo.com",
    "wellsfargo.com", "chase.com", "bankofamerica.com", ".bank",
    "venmo.com", "paypal.com", "mint.intuit.com",
    "schwab.com", "fidelity.com", "vanguard.com", "robinhood.com",
    "facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com",
    "reddit.com", "youtube.com", "netflix.com", "spotify.com",
    "amazon.com", "ebay.com", "mail.google.com", "outlook.live.com"
  ]
}
```

### 3. Set Default Retention

```bash
echo "30" > ~/.screenpipe/retention_days
```

### 4. Install Cleanup Script

```bash
# Copy cleanup script from dex-core
cp dex-core/core/scripts/screenpipe-cleanup.sh ~/.screenpipe/cleanup.sh
chmod +x ~/.screenpipe/cleanup.sh

# Install daily cleanup (runs at 3 AM)
cp dex-core/core/scripts/com.dex.screenpipe-cleanup.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.dex.screenpipe-cleanup.plist
```

### 5. Update User Profile

Set `screenpipe.enabled: true` and `screenpipe.prompted: true` in `System/user-profile.yaml`

### 6. Start ScreenPipe

```bash
screenpipe &
```

### 7. Verify

```bash
curl http://localhost:3030/health
```

### Done Message

"✅ ScreenPipe is running!

**What's captured:** Work apps (VS Code, Terminal, Slack, Notion, etc.)
**What's blocked:** All browsers, personal apps, banking, social media
**Data location:** `~/.screenpipe/` (on your machine only)
**Auto-delete:** After 30 days

**Try asking:** 'What was I working on in the last hour?'

**View your data anytime:** `open http://localhost:3030`
**Disable anytime:** `screenpipe stop`"

---

## Disable Flow

Triggers: `/screenpipe-disable`, "disable screenpipe", "stop screen capture"

```bash
screenpipe stop
# or
pkill screenpipe
```

Update `screenpipe.enabled: false` in user-profile.yaml

Ask: "Want to delete the captured data too?"
- Yes: `rm -rf ~/.screenpipe/`
- No: "Data preserved - you can review or delete later"

---

## Change Retention

When user says things like:
- "Keep screen data for 7 days"
- "Change retention to 90 days"

Extract the number and update:
```bash
echo "7" > ~/.screenpipe/retention_days
```

Also update `screenpipe.retention_days` in user-profile.yaml

Confirm: "Done! ScreenPipe will now keep data for X days. Old data will be cleaned up tonight at 3 AM."

---

## Add to Blocklist

When user says:
- "Block Spotify from ScreenPipe"
- "Don't capture my company intranet"

1. Read current `~/.screenpipe/config.json`
2. Add to `ignored_apps` or `ignored_urls` array
3. Write back
4. Tell user to restart: `screenpipe stop && screenpipe`

---

## Local Model Option

If user wants maximum privacy (nothing to Anthropic):

1. Guide them through `/ai-setup` first
2. Choose Offline/Local mode (Ollama)
3. Then set up ScreenPipe
4. "With local models, your screen data never leaves your machine - even when you ask me questions about it."

## Track Usage (Silent)

Update `System/usage_log.md` to mark ScreenPipe setup as used.

**Analytics (Silent):**

Call `track_event` with event_name `screenpipe_setup_completed` (no properties).

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
