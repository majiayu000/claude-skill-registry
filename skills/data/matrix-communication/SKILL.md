---
name: matrix-communication
description: Matrix chat communication. AUTOMATICALLY TRIGGER when user mentions Matrix rooms (#room:server), asks to send messages to chat, or wants to interact with Matrix. Use for sending messages to Matrix rooms on behalf of users via access token authentication.
---

# Matrix Communication

Send messages to Matrix chat rooms on behalf of users.

## Auto-Trigger

**AUTOMATICALLY USE THIS SKILL** when you encounter:
- **Room references**: `#room:server`, `!roomid:server`
- **Chat requests**: "send to matrix", "post in chat", "notify the team"
- **Matrix URLs**: `https://matrix.*/`, `https://element.*/`
- **Setup requests**: "configure matrix", "set up matrix skill"

## Setup Guide (for Agent)

When user asks to set up Matrix, guide them through these steps:

### Step 1: Check if already configured

```bash
cat ~/.config/matrix/config.json 2>/dev/null && echo "Config exists" || echo "Not configured"
```

### Step 2: If not configured, ask user for:

1. **User ID** - e.g., `@username:matrix.org` or `@username:company.com`
2. **Matrix password** - for E2EE device creation (not stored, used once)
3. **Bot prefix** (optional) - e.g., `🤖` to mark automated messages

### Step 3: Discover homeserver URL

Extract the domain from the user ID and discover the homeserver via `.well-known`:

```bash
# Extract domain from user ID (e.g., @user:example.com -> example.com)
MATRIX_DOMAIN="DOMAIN_FROM_USER_ID"

# Discover homeserver URL
curl -s "https://${MATRIX_DOMAIN}/.well-known/matrix/client" | python3 -c "import sys,json; print(json.load(sys.stdin)['m.homeserver']['base_url'])"
```

**Example:** For `@sebastian.mendel:netresearch.de`:
- Domain: `netresearch.de`
- Discovery URL: `https://netresearch.de/.well-known/matrix/client`
- Returns homeserver: `https://matrix.netresearch.de`

### Step 4: Create config file

```bash
mkdir -p ~/.config/matrix
cat > ~/.config/matrix/config.json << 'EOF'
{
  "homeserver": "DISCOVERED_HOMESERVER_URL",
  "user_id": "USER_PROVIDED_USER_ID",
  "bot_prefix": "🤖"
}
EOF
chmod 600 ~/.config/matrix/config.json
```

### Step 5: Set up E2EE device (recommended)

**Three ways to provide the password:**

**Option A: Environment variable (recommended for agents)**
```bash
MATRIX_PASSWORD="USER_PASSWORD" uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py
```

**Option B: Interactive prompt (recommended for users)**
```bash
uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py
# Script will securely prompt for password
```

**Option C: Command line argument (use with caution)**
```bash
set +H && uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py "USER_PASSWORD"
```

This creates a dedicated "Matrix Skill E2EE" device. The password is used once and not stored.

**Why environment variable?** Avoids shell escaping issues with special characters (`!`, `$`, etc.). The `set +H` workaround for command line is less reliable.

### Step 6: Add access token to config

After E2EE setup, copy the access token to enable non-E2EE scripts:

```bash
# Extract access token from E2EE credentials and add to config
ACCESS_TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.local/share/matrix-skill/store/credentials.json'))['access_token'])")

# Update config with access token
python3 -c "
import json
config_path = '$HOME/.config/matrix/config.json'
with open(config_path) as f:
    config = json.load(f)
config['access_token'] = '$ACCESS_TOKEN'
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print('Access token added to config')
"
```

### Step 7: Verify setup

```bash
uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py --status
uv run skills/matrix-communication/scripts/matrix-rooms.py
```

### Step 8: Verify device (IMPORTANT)

**⚠️ STRONGLY RECOMMENDED:** Verify the new "Matrix Skill E2EE" device to avoid security warnings.

**Why verify?**
- Other users see ⚠️ warnings when unverified devices send messages
- Some rooms may block messages from unverified devices
- Cross-signing establishes trust chain for your account
- Enables automatic room key sharing from other devices

**Agent workflow for real-time emoji display:**

The verification script writes emojis to `/tmp/matrix_verification_emojis.txt` for agent polling. This enables showing emojis to the user BEFORE they need to confirm in Element.

**Step 8a: Clear emoji file and start verification in background**

```bash
rm -f /tmp/matrix_verification_emojis.txt
uv run skills/matrix-communication/scripts/matrix-e2ee-verify.py --timeout 180 > /tmp/verify_log.txt 2>&1 &
```

**Step 8b: Poll for emojis and show to user immediately**

```bash
# Poll until emoji file appears (check every 1-2 seconds)
for i in {1..30}; do
    if [ -f /tmp/matrix_verification_emojis.txt ]; then
        cat /tmp/matrix_verification_emojis.txt
        break
    fi
    sleep 1
done
```

The emojis display like this:
```
╔══════════════════════════════════════════════════════════╗
║           🔐 VERIFICATION EMOJIS - COMPARE NOW! 🔐        ║
╠══════════════════════════════════════════════════════════╣
║       🐱    Cat                                          ║
║       🔑    Key                                          ║
║       🎸    Guitar                                       ║
║       ...   (7 emojis total)                             ║
╚══════════════════════════════════════════════════════════╝
```

**Step 8c: Tell user to confirm in Element**

Once emojis are displayed, instruct the user:
- "Compare these emojis with what Element shows"
- "Click 'They match' in Element to complete verification"

**Step 8d: Wait for verification to complete**

```bash
# Check verification result
grep -q "VERIFICATION SUCCESSFUL" /tmp/verify_log.txt && echo "✅ Verified!"
```

**Device selection:** The script automatically prioritizes:
1. Element Desktop/Mobile clients (interactive)
2. Web clients (riot/chrome/firefox)
3. Named devices
4. Backup devices (lowest priority - can't respond interactively)

Use `--request DEVICE_ID` to target a specific device.

**Notes:**
- User confirms emojis in **Element**, not in the terminal
- After verification, the script automatically fetches room keys
- The emoji file enables real-time display even with buffered command output

### Troubleshooting

**E2EE setup fails with "Invalid username or password":**

If your password contains special characters (`!`, `$`, `\`, etc.), bash may mangle them:

```bash
# WRONG - bash corrupts passwords with special characters
uv run .../matrix-e2ee-setup.py "MyPass!word"

# CORRECT - use environment variable (recommended)
MATRIX_PASSWORD="MyPass!word" uv run .../matrix-e2ee-setup.py

# CORRECT - use interactive prompt
uv run .../matrix-e2ee-setup.py
# Enter password when prompted

# ALTERNATIVE - disable history expansion
set +H && uv run .../matrix-e2ee-setup.py "MyPass!word"
```

**E2EE setup fails with libolm error:**
```bash
# Debian/Ubuntu
sudo apt install libolm-dev

# Fedora
sudo dnf install libolm-devel

# macOS
brew install libolm
```

**Non-E2EE scripts fail with "Config missing required fields: access_token":**

After E2EE setup, the access token is stored separately. Copy it to the main config:
```bash
# Get token and add to config
python3 -c "
import json
creds = json.load(open('$HOME/.local/share/matrix-skill/store/credentials.json'))
config = json.load(open('$HOME/.config/matrix/config.json'))
config['access_token'] = creds['access_token']
json.dump(config, open('$HOME/.config/matrix/config.json', 'w'), indent=2)
print('Done')
"
```

## Config Reference

**File:** `~/.config/matrix/config.json`

| Field | Required | Description |
|-------|----------|-------------|
| `homeserver` | Yes | Matrix server URL |
| `user_id` | Yes | Full Matrix user ID |
| `bot_prefix` | No | Prefix for messages (e.g., `🤖`) |
| `access_token` | No | Auto-created by E2EE setup |

## Scripts

All scripts are in the `scripts/` directory. Run with `uv run`.

### ⚠️ ALWAYS USE E2EE SCRIPTS

**Default to E2EE scripts (`*-e2ee.py`) for all operations.** Most Matrix rooms are encrypted. Only fall back to non-E2EE scripts if E2EE fails or user explicitly requests it.

| Operation | E2EE Script (preferred) | Non-E2EE Fallback |
|-----------|------------------------|-------------------|
| Send message | `matrix-send-e2ee.py` | `matrix-send.py` |
| Read messages | `matrix-read-e2ee.py` | `matrix-read.py` |
| Edit message | `matrix-edit-e2ee.py` | `matrix-edit.py` |
| React | `matrix-react.py` | (same) |
| Redact | `matrix-redact.py` | (same) |

| Script | Purpose |
|--------|---------|
| `matrix-send-e2ee.py` | **Send message (E2EE) - USE THIS** |
| `matrix-read-e2ee.py` | **Read messages (E2EE) - USE THIS** |
| `matrix-edit-e2ee.py` | **Edit message (E2EE) - USE THIS** |
| `matrix-react.py` | React to a message with emoji |
| `matrix-redact.py` | Delete/redact a message |
| `matrix-rooms.py` | List joined rooms |
| `matrix-resolve.py` | Resolve room alias to room ID |
| `matrix-e2ee-setup.py` | One-time E2EE device setup |
| `matrix-e2ee-verify.py` | Device verification (experimental) |
| `matrix-fetch-keys.py` | Request missing keys from other devices |
| `matrix-key-backup.py` | Restore keys from server backup |

## Room Identification

Scripts support multiple ways to identify rooms:

| Format | Example | Description |
|--------|---------|-------------|
| **Room name** | `agent-work` | Easiest - looked up from joined rooms |
| **Room ID** | `!sZBo...Q22E` | Direct - from `matrix-rooms.py` output |
| **Room alias** | `#room:server` | Resolved via Matrix directory |

**Best practice:** Use room names for simplicity. The script will find the matching room from your joined rooms list.

```bash
# These all work - room name is easiest
uv run skills/matrix-communication/scripts/matrix-send.py agent-work "Hello!"
uv run skills/matrix-communication/scripts/matrix-send.py '!sZBoTOreI1z0BgHY' "Hello!"
uv run skills/matrix-communication/scripts/matrix-send.py '#agent-work:server' "Hello!"
```

## Quick Reference

```bash
# Send message by room name (easiest - PREFERRED)
uv run skills/matrix-communication/scripts/matrix-send.py agent-work "Hello from Claude!"

# Send message by room ID (from matrix-rooms.py output)
uv run skills/matrix-communication/scripts/matrix-send.py '!sZBoTOreI1z0BgHY-s2ZC9MV63B1orGFigPXvYMQ22E' "Hello!"

# Send message by room alias
uv run skills/matrix-communication/scripts/matrix-send.py "#myroom:matrix.org" "Hello!"

# Send formatted message (markdown)
uv run skills/matrix-communication/scripts/matrix-send.py ops "**Deployment complete** for project X"

# List joined rooms (shows name, alias, and ID)
uv run skills/matrix-communication/scripts/matrix-rooms.py

# Find room ID by name
uv run skills/matrix-communication/scripts/matrix-rooms.py --lookup agent-work

# Search rooms
uv run skills/matrix-communication/scripts/matrix-rooms.py --search ops

# Read recent messages (unencrypted only)
uv run skills/matrix-communication/scripts/matrix-read.py myroom --limit 10

# Resolve room alias to ID
uv run skills/matrix-communication/scripts/matrix-resolve.py "#myroom:matrix.org"
```

## Message Types

### Regular Messages (m.text)
Default - use for most communication.

### Emote Messages (m.emote)
Like IRC `/me` - displays as action. Use `--emote` flag.
```bash
# Appears as: "* username is deploying to production"
uv run skills/matrix-communication/scripts/matrix-send.py "#ops:matrix.org" "is deploying to production" --emote
```
**When to use:** Status updates, actions, presence indicators.

### Thread Replies
Reply in a thread to keep discussions organized. Use `--thread` with root event ID.
```bash
# Start a thread or reply to existing thread
uv run skills/matrix-communication/scripts/matrix-send.py "#dev:matrix.org" "Update: tests passing" --thread '$rootEventId'
```
**When to use:** Ongoing updates to a topic, multi-step processes, avoiding main room clutter.

### Direct Replies
Reply to a specific message. Use `--reply` with event ID.
```bash
uv run skills/matrix-communication/scripts/matrix-send.py "#team:matrix.org" "Agreed, let's proceed" --reply '$eventId'
```

## Reactions

Add emoji reactions to messages to indicate status without new messages.

```bash
# React with checkmark (task done)
uv run skills/matrix-communication/scripts/matrix-react.py "#ops:matrix.org" '$eventId' "✅"

# Thumbs up (acknowledged)
uv run skills/matrix-communication/scripts/matrix-react.py "#dev:matrix.org" '$eventId' "👍"

# Eyes (looking into it)
uv run skills/matrix-communication/scripts/matrix-react.py "#support:matrix.org" '$eventId' "👀"
```

### Common Reaction Patterns

| Emoji | Meaning | Use Case |
|-------|---------|----------|
| ✅ | Done/Complete | Mark task as finished |
| 👍 | Acknowledged | Confirm receipt |
| 👀 | Looking into it | Started investigating |
| 🚀 | Deployed/Shipped | Indicate release |
| ⏳ | In progress | Working on it |
| ❌ | Failed/Blocked | Indicate problem |

**Workflow example:** Send "Going to reboot server" → later add ✅ reaction when complete.

## Visual Effects (Element Clients)

Include specific emoji to trigger visual effects in Element/SchildiChat:

| Emoji | Effect | Use Case |
|-------|--------|----------|
| 🎉 🎊 | Confetti | Celebrations, milestones |
| 🎆 | Fireworks | Major achievements |
| ❄️ | Snowfall | Seasonal, cool features |

```bash
# Celebrate a release
uv run skills/matrix-communication/scripts/matrix-send.py "#team:matrix.org" "🎉 Version 2.0 released!"
```

**Note:** Effects only show for Element/SchildiChat users. Other clients see the emoji normally.

## Message Formatting

All formatting is automatic - just use markdown syntax.

### Basic Formatting

| Syntax | Result | When to Use |
|--------|--------|-------------|
| `**bold**` | **bold** | Emphasis, headings, status |
| `*italic*` | *italic* | Secondary emphasis |
| `` `code` `` | `code` | Commands, file names, variables |
| `~~strike~~` | ~~strike~~ | Corrections, outdated info |
| `[text](url)` | linked text | Custom link labels |

### Matrix-Specific Features

| Syntax | Result | When to Use |
|--------|--------|-------------|
| `@user:server` | Clickable mention | Notify specific users |
| `#room:server` | Clickable room link | Reference other rooms |
| `> quote` | Blockquote | Quote previous messages |
| `\|\|spoiler\|\|` | Hidden text | Sensitive info, plot spoilers |
| ` ```lang ``` ` | Code block | Multi-line code with syntax highlighting |

### Smart Link Shortening

URLs are automatically shortened to readable links:

| URL | Displayed As |
|-----|--------------|
| `https://jira.*/browse/PROJ-123` | PROJ-123 |
| `https://github.com/owner/repo/issues/42` | owner/repo#42 |
| `https://github.com/owner/repo/pull/42` | owner/repo#42 |
| `https://gitlab.*/group/proj/-/issues/42` | group/proj#42 |

### Lists

```
- Item one
- Item two
- Item three
```

## When to Use Each Feature

**Deployment notifications:**
- Use **bold** for status: `**Deployed**`, `**Failed**`
- Use lists for changes
- Link to Jira issue URL (auto-shortened)

**Code sharing:**
- Use ` ```lang ``` ` for multi-line code
- Use `` `inline` `` for single commands

**Team communication:**
- Use `@user:server` to notify specific people
- Use `#room:server` to reference discussions in other rooms
- Use `> quote` when replying to earlier messages

**Sensitive information:**
- Use `||spoiler||` for credentials, secrets in examples

## E2EE Support

### Which script to use?

| Scenario | Script | Notes |
|----------|--------|-------|
| Unencrypted room | `matrix-send.py` | Fast, no deps |
| E2EE room with "allow unverified" | `matrix-send.py` | Works but not encrypted |
| E2EE room, proper encryption | `matrix-send-e2ee.py` | Requires libolm + setup |

### E2EE Setup (Recommended)

**Use a dedicated device** - this avoids key sync conflicts with Element:

```bash
# One-time setup: create dedicated E2EE device

# Option 1: Environment variable (recommended - handles special chars)
MATRIX_PASSWORD="YOUR_PASSWORD" uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py

# Option 2: Interactive prompt (secure - password not in history)
uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py

# Now send encrypted messages
uv run skills/matrix-communication/scripts/matrix-send-e2ee.py '#room:server' 'Encrypted message'

# Check setup status
uv run skills/matrix-communication/scripts/matrix-e2ee-setup.py --status
```

**Why dedicated device?**
- Clean key state, no conflicts with Element
- Proper cross-signing setup
- Avoids "signature verification failed" errors

**⚠️ Access token fallback (not recommended):**
Using `access_token` from config reuses Element's device, which causes key sync issues and verification problems. Only use if password-based setup isn't possible.

### E2EE Script Usage

```bash
# First run after setup is slow (~5-10s) - syncs keys
uv run skills/matrix-communication/scripts/matrix-send-e2ee.py '#encrypted-room:server' 'Secret message'

# Subsequent runs faster (uses cached keys)
uv run skills/matrix-communication/scripts/matrix-send-e2ee.py '#encrypted-room:server' 'Another message'
```

Storage locations:
- Device credentials: `~/.local/share/matrix-skill/store/credentials.json`
- Encryption keys: `~/.local/share/matrix-skill/store/*.db`

### Device Verification (Recommended)

Device verification marks a device as trusted and enables automatic key sharing from other devices.

```bash
# Auto-find Element device and initiate verification
uv run skills/matrix-communication/scripts/matrix-e2ee-verify.py --timeout 180

# Target specific device
uv run skills/matrix-communication/scripts/matrix-e2ee-verify.py --request DEVICE_ID --timeout 180

# With debug output
uv run skills/matrix-communication/scripts/matrix-e2ee-verify.py --debug --timeout 180
```

**Smart device selection:** The script automatically prioritizes Element clients (Desktop/Android/iOS) over backup devices that can't respond to verification.

**Real-time emoji display:** Emojis are written to `/tmp/matrix_verification_emojis.txt` so agents can poll and display them immediately while the user confirms in Element.

**Why verify?**
- Removes ⚠️ "unverified device" warnings for other users
- Enables automatic room key sharing from other devices
- Required for some security-conscious rooms

### Reading E2EE Messages

```bash
# Read recent encrypted messages
uv run skills/matrix-communication/scripts/matrix-read-e2ee.py '#room:server' --limit 10

# JSON output
uv run skills/matrix-communication/scripts/matrix-read-e2ee.py '#room:server' --json
```

**Note:** Messages sent before your device was created show as `[Unable to decrypt]` - this is normal E2EE behavior (new devices can't read old messages without key sharing).

### Fetching Missing Keys

New devices can't decrypt old messages by default. After verification, use these methods to get missing keys:

#### Method 1: Request from Other Devices (Recommended)

After device verification, other devices can forward keys automatically. This works without any passwords or recovery keys:

```bash
# Fetch keys for a specific room
uv run skills/matrix-communication/scripts/matrix-fetch-keys.py ROOM --sync-time 60

# Example: Fetch keys for IT room with extended wait
uv run skills/matrix-communication/scripts/matrix-fetch-keys.py IT --limit 200 --sync-time 120
```

This script:
1. Reads room history to find undecryptable messages
2. Requests keys from your other verified devices
3. Receives forwarded keys automatically

**Requirements:**
- Device must be verified (run verification first)
- Other verified devices must be online
- Works best with Element running on another device

#### Method 2: Restore from Server Backup

If key forwarding doesn't work (no other devices online), restore from backup using your **recovery key** or **passphrase**:

```bash
# Check backup status
uv run skills/matrix-communication/scripts/matrix-key-backup.py --status

# Restore using recovery key (looks like: EsTj qRGp YB4C ...)
uv run skills/matrix-communication/scripts/matrix-key-backup.py --recovery-key "EsTj qRGp YB4C ..."

# Restore using passphrase
uv run skills/matrix-communication/scripts/matrix-key-backup.py --passphrase "your recovery passphrase"
```

**Find your recovery key in Element:**
Settings → Security & Privacy → Secure Backup → "Show Recovery Key"

| Script | Purpose |
|--------|---------|
| `matrix-fetch-keys.py` | Request keys from other devices (no secrets needed) |
| `matrix-key-backup.py` | Restore keys from server backup (needs recovery key) |

### Limitations

- **Old messages**: Can't decrypt without key backup restoration
- **First sync**: Initial run is slow due to key exchange
- **Device trust**: Auto-trusts devices (TOFU model)
- **Setup required**: First use requires user's Matrix password (one-time only)
- **Verification**: Experimental - cross-signing/room-based verification not fully supported
- **Key backup**: Requires recovery key/passphrase (stored in Element settings)

## Common Patterns

### Deployment notification with Jira link
```bash
uv run skills/matrix-communication/scripts/matrix-send.py "#ops:matrix.org" \
  "**Deployed** to production

https://jira.example.com/browse/PROJ-123

- Version: 1.2.3
- Changes: Auth improvements"
```

### Status update with mentions
```bash
uv run skills/matrix-communication/scripts/matrix-send.py "#dev:matrix.org" \
  "**Done**: API refactoring complete

@lead:matrix.org ready for review

See #code-review:matrix.org for PR discussion"
```

### Share code snippet
```bash
uv run skills/matrix-communication/scripts/matrix-send.py "#dev:matrix.org" \
  "Fix for the auth bug:

\`\`\`python
def validate_token(token):
    return token.startswith('valid_')
\`\`\`"
```

### Quote and respond
```bash
uv run skills/matrix-communication/scripts/matrix-send.py "#team:matrix.org" \
  "> Should we deploy today?

**Yes** - all tests passing. Deploying now."
```

### Check room before sending
```bash
# List rooms to find the right one
uv run skills/matrix-communication/scripts/matrix-rooms.py | grep -i ops

# Then send
uv run skills/matrix-communication/scripts/matrix-send.py "#ops-team:matrix.org" "Message here"
```

### Server maintenance with status updates
```bash
# 1. Announce (save event ID from output)
uv run skills/matrix-communication/scripts/matrix-send.py "#ops:matrix.org" "⏳ Starting server maintenance..."
# Output: Event ID: $abc123

# 2. Update status via reaction
uv run skills/matrix-communication/scripts/matrix-react.py "#ops:matrix.org" '$abc123' "✅"

# 3. Or add thread update
uv run skills/matrix-communication/scripts/matrix-send.py "#ops:matrix.org" "Maintenance complete, all services restored" --thread '$abc123'
```

### Celebrate milestone
```bash
uv run skills/matrix-communication/scripts/matrix-send.py "#team:matrix.org" "🎉 **Milestone reached!**

We hit 1000 users today!

Thanks to everyone who contributed."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `M_FORBIDDEN` | Not in room or no permission | Join room first in Element |
| `M_UNKNOWN_TOKEN` | Invalid/expired token | Get new token from Element |
| `M_NOT_FOUND` | Room doesn't exist | Check room alias spelling |
| `Could not find room` | Name lookup failed | Use `matrix-rooms.py` to list available rooms |
| `Multiple matches found` | Ambiguous room name | Use more specific name or room ID from list |
| `Could not resolve room alias` | Alias doesn't exist | Try room name instead of alias |

## Bash Quoting

**Important:** Bash history expansion treats `!` specially, which can corrupt messages and passwords.

### Best Solution: Disable History Expansion

```bash
# MOST RELIABLE - disable history expansion for the command
set +H && uv run skills/matrix-communication/scripts/matrix-send.py "#room:server" "Done!"
```

### Alternative: Quote Carefully

```bash
# Single quotes - works for simple messages
uv run skills/matrix-communication/scripts/matrix-send.py "#room:server" 'Done!'

# WRONG - double quotes allow history expansion
uv run skills/matrix-communication/scripts/matrix-send.py "#room:server" "Done!"
# Results in: Done\!
```

### For Passwords with Special Characters

Use environment variable (most reliable) or interactive prompt:

```bash
# BEST - environment variable handles all special characters
MATRIX_PASSWORD="MyP@ss!word" uv run .../matrix-e2ee-setup.py

# GOOD - interactive prompt (password not in shell history)
uv run .../matrix-e2ee-setup.py
# Enter password when prompted

# ALTERNATIVE - disable history expansion for command line
set +H && uv run .../matrix-e2ee-setup.py "MyP@ss!word"
```

## Related

- [Matrix Client-Server API](https://spec.matrix.org/latest/client-server-api/)
- `references/api-reference.md` - Matrix API endpoints
