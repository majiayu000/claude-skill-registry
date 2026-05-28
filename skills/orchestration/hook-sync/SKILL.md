---
name: Hook Sync
description: This skill should be used when implementing "hook-based coordination", "file change detection", "event-driven agent triggering", "PostToolUse hooks", "hybrid hooks", or building systems where file changes automatically trigger agent responses. Provides comprehensive guidance for hook-based synchronization in multi-agent systems.
version: 0.1.0
---

# Hook Sync Skill

## Overview

This skill provides guidance for implementing hook-based synchronization systems where file changes automatically trigger agent responses. Hooks enable event-driven coordination between agents without polling or manual intervention.

## Core Concepts

### Hook-Based Coordination

Hooks are event handlers that execute in response to Claude Code events:

**Key events for file coordination**:
- **PostToolUse(Write)**: After any file write operation
- **PreToolUse**: Before tool execution (for validation)
- **UserPromptSubmit**: After user sends a message

**Benefits**:
- Automatic response to state changes
- No polling or busy-waiting required
- Declarative coordination logic
- Centralized event handling

### Hybrid Hook Pattern

Combine script-based filtering with AI-based decision making:

**Script component**: Fast filtering and validation
- Check file paths match patterns
- Validate file format
- Extract relevant data
- Determine if action needed

**Prompt component**: Intelligent response
- Analyze file contents
- Decide which agent to spawn
- Generate agent context
- Handle complex scenarios

## Hook Configuration

### Basic Structure

Hooks are configured in `hooks/hooks.json`:

```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [
      {
        "type": "prompt",
        "prompt": "Check if file change requires agent response"
      }
    ]
  }]
}
```

### File Pattern Matching

Detect specific file writes:

```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "prompt",
      "prompt": "File written: {{tool_use.parameters.file_path}}\n\nIf this is a turn-signal file (games/*/state/turn-signal.json), read the file to determine which player agent to spawn.\n\nIf this is a player-action file (games/*/state/player-actions/*.json), trigger the gamemaster agent to validate and process the action.\n\nOtherwise, take no action."
    }]
  }]
}
```

### Hybrid Hook Pattern

Use script for fast filtering, prompt for decisions:

```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [
      {
        "type": "command",
        "command": "bash $CLAUDE_PLUGIN_ROOT/hooks/scripts/check-game-file.sh {{tool_use.parameters.file_path}}",
        "timeout": 5
      },
      {
        "type": "prompt",
        "prompt": "The previous command checked if this file change requires action. If it exited with code 0, the file is a game state file that needs processing. Read the file and spawn the appropriate agent."
      }
    ]
  }]
}
```

## Agent Triggering Patterns

### Turn-Based Triggering

When turn signal is written, spawn player agent:

**Hook configuration**:
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "prompt",
      "prompt": "A file was written: {{tool_use.parameters.file_path}}\n\nCheck if this matches the pattern: games/*/state/turn-signal.json\n\nIf yes:\n1. Read the turn-signal.json file\n2. Extract the currentPlayer and turnNumber\n3. Read the game rules from games/*/RULES.md\n4. Read the player's hand from game state\n5. Spawn a player agent using Task tool with:\n   - model: haiku\n   - prompt including rules, hand, and visible state\n   - Instructions to write decision to player-actions/<player-id>.json\n\nIf no: Take no action."
    }]
  }]
}
```

**Agent spawn on trigger**:
```javascript
// Hook detects turn-signal.json write
const turnSignal = JSON.parse(await Read("games/uno/state/turn-signal.json"));

// Spawn player agent
await Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: `Player ${turnSignal.currentPlayer} turn`,
  prompt: generatePlayerPrompt(turnSignal),
  run_in_background: false
});
```

### Action Processing Triggering

When player writes action, trigger gamemaster:

**Hook configuration**:
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "prompt",
      "prompt": "File written: {{tool_use.parameters.file_path}}\n\nCheck if this matches: games/*/state/player-actions/*.json\n\nIf yes:\n1. Read the action file\n2. Extract gameId, playerId, action details\n3. If you ARE the gamemaster agent:\n   - Validate the action against game rules\n   - Update game state if valid\n   - Write next turn signal\n4. If you are NOT the gamemaster:\n   - Use Task tool to spawn/resume gamemaster agent\n   - Provide action file path for processing\n\nIf no: Take no action."
    }]
  }]
}
```

## Hook Templates

### Game State Monitor Hook

Monitor all game state file changes:

```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "prompt",
      "prompt": "File change detected: {{tool_use.parameters.file_path}}\n\n## Game Coordination Hook\n\nCheck the file path:\n\n**Turn Signal** (games/*/state/turn-signal.json):\n- Read file to get currentPlayer\n- Load game rules and player hand\n- Spawn player agent for that player's turn\n\n**Player Action** (games/*/state/player-actions/<player-id>.json):\n- Read action file\n- Trigger gamemaster to validate and process\n- Update game state if valid\n\n**Game State** (games/*/state/game-state.json):\n- Log state change for debugging\n- Check if game has ended\n- If ended, generate final report\n\n**Other files**: No action needed\n\nProcess accordingly."
    }]
  }]
}
```

### Validation Hook

Prevent invalid state changes:

```json
{
  "PreToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "prompt",
      "prompt": "About to write file: {{tool_use.parameters.file_path}}\n\nIf this is a game state file (games/*/state/*.json):\n1. Validate JSON syntax in tool_use.parameters.content\n2. Check file structure matches expected schema\n3. If invalid: BLOCK the write and explain why\n4. If valid: ALLOW the write\n\nOtherwise: ALLOW the write."
    }]
  }]
}
```

## Script Integration

### File Pattern Checker

Create `hooks/scripts/check-game-file.sh`:

```bash
#!/usr/bin/env bash
# Check if file is a game coordination file

file_path=$1

# Check for turn signal
if [[ "$file_path" =~ games/.*/state/turn-signal\.json ]]; then
    echo "turn-signal"
    exit 0
fi

# Check for player action
if [[ "$file_path" =~ games/.*/state/player-actions/.*\.json ]]; then
    echo "player-action"
    exit 0
fi

# Check for game state
if [[ "$file_path" =~ games/.*/state/game-state\.json ]]; then
    echo "game-state"
    exit 0
fi

# Not a game file
exit 1
```

### File Validator

Create `hooks/scripts/validate-game-file.sh`:

```bash
#!/usr/bin/env bash
# Validate game file JSON structure

file_path=$1

# Check file exists
if [ ! -f "$file_path" ]; then
    echo "ERROR: File not found"
    exit 1
fi

# Validate JSON syntax
if ! jq empty "$file_path" 2>/dev/null; then
    echo "ERROR: Invalid JSON"
    exit 1
fi

# Check required fields based on file type
file_type=$(jq -r '.fileType // "unknown"' "$file_path")

case "$file_type" in
    "turn-signal")
        jq -e '.currentPlayer and .turnNumber' "$file_path" > /dev/null
        ;;
    "player-action")
        jq -e '.playerId and .action and .turnNumber' "$file_path" > /dev/null
        ;;
    "game-state")
        jq -e '.players and .turnNumber and .gameActive' "$file_path" > /dev/null
        ;;
    *)
        echo "ERROR: Unknown file type: $file_type"
        exit 1
        ;;
esac

if [ $? -ne 0 ]; then
    echo "ERROR: Missing required fields for $file_type"
    exit 1
fi

echo "Valid $file_type file"
exit 0
```

## Best Practices

### Hook Design

✅ **DO:**
- Use prompt-based hooks for complex logic
- Filter with scripts before expensive AI operations
- Include file paths in prompts for context
- Handle multiple file patterns in one hook
- Provide clear decision criteria

❌ **DON'T:**
- Create separate hooks for every file pattern
- Use only command hooks for complex decisions
- Trigger on every file write without filtering
- Spawn agents without checking context
- Ignore error handling

### Performance

✅ **DO:**
- Filter early with regex patterns
- Use fast scripts for simple checks
- Cache game rules and static data
- Batch multiple actions when possible
- Set reasonable timeouts

❌ **DON'T:**
- Parse large files in every hook
- Spawn agents unnecessarily
- Reload static data repeatedly
- Create infinite trigger loops
- Ignore timeout configurations

### Debugging

✅ **DO:**
- Log hook executions
- Include file paths in messages
- Test hooks with sample files
- Validate JSON before processing
- Use clear error messages

❌ **DON'T:**
- Silently fail
- Omit context from logs
- Skip validation
- Create complex hook chains
- Ignore hook errors

## Integration Patterns

### Complete Turn Cycle

1. **Gamemaster writes turn signal** → PostToolUse hook triggers
2. **Hook spawns player agent** → Player analyzes state
3. **Player writes action** → PostToolUse hook triggers
4. **Hook notifies gamemaster** → Gamemaster validates
5. **Gamemaster updates state** → Next turn begins

### Error Recovery

If player agent fails:
- Hook detects timeout or error
- Spawns fallback handler
- Logs error for analysis
- Continues game with default action

If gamemaster fails:
- Hook detects missing state update
- Attempts recovery or game halt
- Notifies user of issue

## Testing Hooks

### Manual Testing

```bash
# Test turn signal trigger
echo '{"fileType":"turn-signal","currentPlayer":"player-1","turnNumber":1}' > games/uno/state/turn-signal.json

# Verify hook triggers
# Check if player agent spawns

# Test player action trigger
echo '{"fileType":"player-action","playerId":"player-1","action":"play","card":{"color":"Red","value":"7"}}' > games/uno/state/player-actions/player-1.json

# Verify hook triggers
# Check if gamemaster processes action
```

### Hook Debugging

Run Claude Code with debug mode:
```bash
claude --debug
```

Check hook execution logs for:
- Hook trigger events
- File path matching
- Script output
- AI responses
- Error messages

## Additional Resources

### Example Files

Working examples in `examples/`:
- **`hooks-config.json`** - Complete hooks.json configuration
- **`check-game-file.sh`** - File pattern matcher script
- **`validate-game-file.sh`** - File validator script

## Integration

This skill works with:
- **game-coordination**: Agents triggered by these hooks
- **file-protocol**: Files monitored by these hooks

For complete multi-agent coordination, use all three skills together.
