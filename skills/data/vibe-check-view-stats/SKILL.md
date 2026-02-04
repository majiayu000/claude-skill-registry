---
name: view-stats
description: Open the Vibe Check stats page in browser. Use when user says "vibe stats", "view my stats", "open stats", or "stats page".
---

# View Vibe Check Stats Online

**Purpose:** Open the user's Vibe Check stats page in their default browser

---

## Configuration Location

The vibe-check configuration is located at: `~/.vibe-check/config.json`

If not found there, check: `/Users/wanderingstan/Developer/vibe-check/config.json`

## How to Open Stats

1. **Read config.json** to get:
   - `api.url` - The server URL
   - `api.username` - The user's username
   - `api.enabled` - Whether remote API is enabled

2. **Check if remote API is enabled**:
   - If `api.enabled` is `false`, inform user that remote stats are not available (they're only saving locally)
   - Suggest they can enable remote sync by editing config.json or reinstalling

3. **Construct the stats URL**:
   - Format: `{api.url}/stats.php?user={username}`
   - Example: `https://vibecheck.wanderingstan.com/stats.php?user=stan`

4. **Open in browser**:
   - macOS: `open "URL"`
   - Linux: `xdg-open "URL"` or `sensible-browser "URL"`
   - Windows: `start "URL"`

---

## Example Implementation

```bash
# Read config
CONFIG_FILE=~/.vibe-check/config.json
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE=/Users/wanderingstan/Developer/vibe-check/config.json
fi

# Extract values using grep/jq or python
URL=$(grep -o '"url":\s*"[^"]*"' "$CONFIG_FILE" | head -1 | cut -d'"' -f4)
USERNAME=$(grep -o '"username":\s*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
ENABLED=$(grep -o '"enabled":\s*true' "$CONFIG_FILE" | head -1)

# Check if enabled
if [ -z "$ENABLED" ]; then
    echo "Remote stats are disabled. You're only saving locally."
    exit 1
fi

# Open stats page
STATS_URL="${URL}/stats.php?user=${USERNAME}"
open "$STATS_URL"  # macOS
# xdg-open "$STATS_URL"  # Linux
```

---

## Alternative: Using Python

```python
import json
import webbrowser
from pathlib import Path

# Find config file
config_path = Path.home() / '.vibe-check' / 'config.json'
if not config_path.exists():
    config_path = Path('/Users/wanderingstan/Developer/vibe-check/config.json')

# Read config
with open(config_path) as f:
    config = json.load(f)

# Check if enabled
if not config['api'].get('enabled', False):
    print("Remote stats are disabled. You're only saving locally.")
    exit(1)

# Get values
url = config['api']['url']
username = config['api']['username']

# Open in browser
stats_url = f"{url}/stats.php?user={username}"
webbrowser.open(stats_url)
print(f"Opening stats page: {stats_url}")
```

---

## Response Format

When triggered, you should:

1. **Locate config.json** - Check standard locations
2. **Read and parse** - Extract api.url, api.username, api.enabled
3. **Validate** - Check if remote API is enabled
4. **Open browser** - Use appropriate command for user's OS
5. **Confirm** - Let user know the URL that was opened

### Example Output

```
Opening your Vibe Check stats page...
📊 https://vibecheck.wanderingstan.com/stats.php?user=stan
```

Or if remote is disabled:

```
⚠️  Remote stats are not enabled in your configuration.

You're currently only saving conversations locally to SQLite.
To enable remote stats, edit ~/.vibe-check/config.json and set:
  "api": { "enabled": true, ... }

Or view your local stats with: claude stats
```

---

## Error Handling

**If config not found:**
- Check both possible locations
- Inform user vibe-check may not be installed
- Provide installation instructions

**If username is empty:**
- This means remote API is disabled
- Show helpful message about enabling it

**If url is empty:**
- Config may be corrupted
- Suggest reinstalling or checking config format

**If browser doesn't open:**
- Print the URL so user can copy/paste it manually
- Suggest checking system permissions
