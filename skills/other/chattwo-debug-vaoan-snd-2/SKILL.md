---
name: ChatTwo Debug
description: Use this skill to read ChatTwo chat logs as a debug console. Covers querying the SQLite database, finding script runs, and extracting debug evidence for bug analysis.
---

# ChatTwo Debug Log Analysis

This skill enables reading and analyzing debug output from SND scripts stored in the ChatTwo plugin's SQLite database.

## Prerequisites

The SQLite MCP server must be configured in `.mcp.json` to connect to the ChatTwo database.

### Project Configuration (Recommended)

The database path is configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-server-sqlite-npx",
        "PATH_TO_YOUR_CHATTWO_DB"
      ]
    }
  }
}
```

**To change the database path:** Edit the last argument in the `args` array in `.mcp.json`.

### Default Path

The typical ChatTwo database location is:
```
{XIVLauncher}/pluginConfigs/ChatTwo/chat-sqlite.db
```

### Alternative: Global Configuration

You can also configure via CLI (adds to user-level config):
```bash
claude mcp add sqlite -- npx -y mcp-server-sqlite-npx "PATH_TO_CHAT_DB"
```

## Database Schema

The ChatTwo database has a single `messages` table:

| Column | Type | Description |
|--------|------|-------------|
| Id | BLOB | Primary key |
| Receiver | INTEGER | Character ID receiving the message |
| ContentId | INTEGER | Content identifier |
| Date | INTEGER | Timestamp (milliseconds since epoch) |
| Code | INTEGER | Chat channel code |
| Sender | BLOB | Sender name (binary encoded) |
| Content | BLOB | Message content (binary encoded with prefix) |
| SenderSource | BLOB | Original sender data |
| ContentSource | BLOB | Original content data |
| SortCode | INTEGER | Sorting order |
| ExtraChatChannel | BLOB | Extra channel info |
| Deleted | BOOLEAN | Soft delete flag |

## Important Chat Codes

| Code | Channel | Description |
|------|---------|-------------|
| 56 | Echo | SND script `/echo` output - **Primary debug channel** |
| 57 | System | Game system messages (gearset changes, etc.) |
| 1 | Say | Public chat |
| 2105 | System | Job change notifications |

## Reading Debug Output

### Basic Query - Recent Echo Messages

```sql
SELECT Date, CAST(Content AS TEXT) as Content
FROM messages
WHERE Code = 56
ORDER BY Date DESC
LIMIT 100
```

**IMPORTANT:** Content is stored as BLOB with a binary prefix. The readable text appears after the prefix characters. Example raw output:
```
���\u0000\u0000\u0000\u0000�\u0002�8��½[CosmicLeveling] === Done ===
```
The actual message is `[CosmicLeveling] === Done ===`.

### Finding Script Runs by Header

Most SND scripts output a header when starting. Use this to find complete runs:

```sql
-- Find all script starts
SELECT Date, CAST(Content AS TEXT) as Content
FROM messages
WHERE Code = 56
ORDER BY Date DESC
LIMIT 500
```

Then filter for headers like:
- `[CosmicLeveling] === Cosmic Exploration Auto-Leveling ===`
- `[ScriptName] === Starting ===`

### Getting a Complete Script Run

Once you find a header timestamp, get all messages from that run:

```sql
SELECT Date, CAST(Content AS TEXT) as Content
FROM messages
WHERE Code = 56
  AND Date >= {HEADER_TIMESTAMP}
  AND Date <= {HEADER_TIMESTAMP + 60000}  -- Within 1 minute
ORDER BY Date ASC
```

### Querying Limitations

**LIKE queries don't work well with BLOB content:**
```sql
-- This may return empty results even when data exists:
WHERE CAST(Content AS TEXT) LIKE '%DEBUG%'
```

**Workaround:** Fetch larger result sets and filter in your analysis.

## Common Debug Patterns

### Script Header/Footer Pattern

Scripts output a versioned header at start and footer at end:

```
[ScriptName] === Script Title vX.Y.Z ===   <- Header with VERSION (start of run)
[ScriptName] Mode: Catch-up
[ScriptName] [DEBUG] ...                    <- Debug messages
[ScriptName] ...                            <- Status messages
[ScriptName] === Done ===                   <- Footer (end of run)
```

**The version in the header is critical for correlating debug output with the correct script code.**

### Finding Bug Evidence

1. **Get recent runs:** Query last 500 Code=56 messages
2. **Identify headers:** Look for `=== ... ===` patterns
3. **Group by run:** Messages between header and footer belong to same run
4. **Analyze flow:** Check if debug output matches expected behavior

### Example: CosmicLeveling Debug Analysis

Headers to look for:
- `[CosmicLeveling] === Cosmic Exploration Auto-Leveling v2.13.2 ===` - Run start (note version!)
- `[CosmicLeveling] === Done ===` - Run end

Key debug messages:
- `[DEBUG] Reference level: X | Reached breakpoint: Y`
- `[DEBUG] JobAbbr is Lv.X`
- `[DEBUG] Enabled Crafters: X/8`
- `[Catch-up] ...` or `[Strict] ...` - Mode-specific logic

## Workflow for Bug Analysis

### Step 0: VERIFY SCRIPTS ARE SYNCED (CRITICAL - DO THIS FIRST!)

**Before analyzing ANY debug output, ensure the local scripts match what's in SND:**

```bash
# Check sync status
node sync.js status

# Push local scripts to SND (ensures SND has latest code)
node sync.js push
```

**Why this matters:**
- Debug logs come from the script version running IN SND
- If local files differ from SND, you're analyzing the wrong code!
- The sync tool shows `[updated]` for files that were out of sync

**Example output showing out-of-sync scripts:**
```
  [updated]   CosmicLeveling.lua -> CosmicLeveling    <- WAS OUT OF SYNC!
  [unchanged] New_Macro.lua                           <- Already synced
```

**If scripts were out of sync:**
1. The bug may already be fixed in the local version
2. Push first, then have the user run the script again
3. Only analyze debug logs from AFTER the push

### Step 1: Query recent echo messages

```sql
SELECT Date, CAST(Content AS TEXT) as Content
FROM messages WHERE Code = 56
ORDER BY Date DESC LIMIT 500
```

### Step 2: Find the script run header

Look for `=== ... vX.Y.Z ===` pattern. **The version is critical!**

**Red flag:** If header has NO version (e.g., `=== Cosmic Exploration Auto-Leveling ===` without `vX.Y.Z`), the script is an old version that predates versioned headers.

### Step 3: Extract version from header

e.g., `v2.13.2`

### Step 4: Verify version matches current script

- Read the script file and check `SCRIPT_VERSION` constant
- If mismatch, retrieve the correct version from git history
- **If no version in header:** Script in SND is outdated - push and retest

### Step 5: Extract the run's messages

Use timestamp range (header to footer)

### Step 6: Compare debug output to expected behavior

Based on the CORRECT version's logic

### Step 7: Identify discrepancies

Between what debug says happened vs what should have happened

## Script Version Correlation

**CRITICAL:** Always correlate the version in debug output with the script source code.

### Version Location

Scripts embed version in two places:
1. **Header output:** `[ScriptName] === Title vX.Y.Z ===` (in chat logs)
2. **Source code:** `local SCRIPT_VERSION = "X.Y.Z"` (at top of script)

### Correlation Workflow

1. **Extract version from debug header:**
   ```
   [CosmicLeveling] === Cosmic Exploration Auto-Leveling v2.13.2 ===
   ```
   Version = `2.13.2`

2. **Check current script version:**
   ```lua
   -- In PlayRoom/CosmicLeveling.lua
   local SCRIPT_VERSION = "2.13.2"
   ```

3. **If versions match:** Analyze using current script source
4. **If versions differ:**
   - Debug output is from an older/different version
   - Use `git log` or `git show` to find the correct version's code
   - Or check if the bug was already fixed in a newer version

### Git History for Old Versions

```bash
# Find commits that changed the script
git log --oneline -- PlayRoom/ScriptName.lua

# View script at a specific commit
git show <commit>:PlayRoom/ScriptName.lua
```

### Why This Matters

A bug report from debug output is only useful if you're looking at the same code that produced it. Example:
- Debug shows `v2.12.0` behavior
- Current script is `v2.13.2`
- The bug might already be fixed, or the code path changed entirely

## Tips

- **High volume database:** ChatTwo stores ALL chat history. Query with LIMIT to avoid overwhelming results.
- **Timestamps:** Date column is milliseconds since epoch. Convert for human-readable times.
- **Binary prefix:** Always expect ~15-20 garbage characters before readable content in BLOB fields.
- **Code 56 only:** For SND debug analysis, focus on Code=56 (Echo channel).
