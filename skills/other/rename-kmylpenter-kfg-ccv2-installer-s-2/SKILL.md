---
name: rename
description: Zmiana nazwy bieżącej konwersacji Claude Code. Triggers: rename, zmień nazwę, nowy tytuł
---

# Rename Conversation Skill

⚡ **ULTRA-FAST** skill - executes in seconds using pure Bash (no file reading to context).

Renames current Claude Code conversation by injecting new user message at the beginning.

## Parameters

- `new_name`: New conversation name (e.g., "updateQuoteCostsandFields")

## Implementation (FAST - Use Bash Only)

**CRITICAL: Do NOT use Read tool. Do NOT parse JSON in Python. Use ONLY Bash commands below.**

### Single Bash Script (Copy-Paste Ready)

```bash
NEW_NAME="[user provided name]"

# Find conversation file (exclude agent-*.jsonl)
CONV_FILE=$(ls -t ~/.claude/projects/*/*.jsonl 2>/dev/null | grep -v 'agent-' | head -1)

# Backup
cp "$CONV_FILE" "$CONV_FILE.backup"

# Generate UUID
NEW_UUID=$(python -c "import uuid; print(str(uuid.uuid4()))" 2>/dev/null || echo "$(date +%s)-0000-0000-0000-000000000000")

# Extract data from line 2
LINE2=$(sed -n '2p' "$CONV_FILE")
CWD=$(echo "$LINE2" | grep -o '"cwd":"[^"]*"' | sed 's/"cwd":"//; s/"$//')
SESSION=$(echo "$LINE2" | grep -o '"sessionId":"[^"]*"' | sed 's/"sessionId":"//; s/"$//')
VERSION=$(echo "$LINE2" | grep -o '"version":"[^"]*"' | sed 's/"version":"//; s/"$//')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

# Double-escape backslashes for JSON
CWD_ESCAPED=$(echo "$CWD" | sed 's/\\/\\\\/g')

# Create new message JSON
NEW_MSG="{\"parentUuid\":null,\"isSidechain\":false,\"userType\":\"external\",\"cwd\":\"$CWD_ESCAPED\",\"sessionId\":\"$SESSION\",\"version\":\"$VERSION\",\"gitBranch\":\"\",\"type\":\"user\",\"message\":{\"role\":\"user\",\"content\":\"$NEW_NAME\"},\"uuid\":\"$NEW_UUID\",\"timestamp\":\"$TIMESTAMP\",\"thinkingMetadata\":{\"level\":\"high\",\"disabled\":false,\"triggers\":[]},\"todos\":[]}"

# Update parentUuid in original line 2
LINE2_UPDATED=$(echo "$LINE2" | sed 's/"parentUuid":null/"parentUuid":"'$NEW_UUID'"/')

# Reconstruct file
{
  sed -n '1p' "$CONV_FILE"
  echo "$NEW_MSG"
  echo "$LINE2_UPDATED"
  tail -n +3 "$CONV_FILE"
} > "$CONV_FILE.tmp" && mv "$CONV_FILE.tmp" "$CONV_FILE"

echo "✅ Renamed to: $NEW_NAME"
echo "Backup: ${CONV_FILE}.backup"
```

## Usage Pattern

**User:** "Rename conversation to X"

**Assistant response:**
1. Execute Bash script above (replace NEW_NAME with X)
2. Single message: "✅ Zmieniono nazwę na: X"
3. Total time: ~2-3 seconds

## DO NOT

- ❌ Use Read tool on conversation file (wastes context)
- ❌ Parse JSON in Python (slow)
- ❌ Use multiple Bash calls (slow)
- ❌ Read entire file into memory

## DO

- ✅ Use single Bash script
- ✅ Process with sed/grep/awk only
- ✅ Keep response under 50 tokens
- ✅ Complete in <5 seconds
