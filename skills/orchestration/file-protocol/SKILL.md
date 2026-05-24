---
name: File Protocol
description: This skill should be used when implementing "file-based communication", "agent communication via files", "JSON state management", "file locking", "race condition handling", "atomic writes", or building systems where multiple agents coordinate through shared files. Provides comprehensive guidance for file-based inter-agent communication protocols.
version: 0.1.0
---

# File Protocol Skill

## Overview

This skill provides guidance for implementing file-based communication protocols that enable multiple agents to coordinate through structured file reads and writes. This approach is particularly valuable for multi-agent systems where agents need to share state, signal events, and coordinate actions without direct API communication.

## Core Concepts

### File-Based Communication

File-based communication uses the filesystem as a message-passing and state-sharing medium:

**Advantages**:
- Simple and transparent (can inspect files manually)
- Language/process agnostic
- Built-in persistence (files survive process crashes)
- Easy debugging and logging
- No network configuration required

**Challenges**:
- Race conditions (simultaneous reads/writes)
- File locking coordination
- Atomicity concerns
- Performance (disk I/O overhead)

**Best for**: Multi-agent coordination, game state management, asynchronous workflows

### Communication Patterns

**Signal Files**: Trigger-based coordination
- File presence or modification signals an event
- Example: `turn-signal.json` triggers player agent spawn

**State Files**: Shared state management
- Central authority writes, multiple readers consume
- Example: `game-state.json` maintains authoritative state

**Action Files**: Request/response communication
- Agents write action requests, coordinator processes and responds
- Example: Player writes `player-actions/player-1.json`, gamemaster reads and validates

**Log Files**: Append-only history
- Immutable record of events for debugging and analysis
- Example: `game-log.json` records all moves

## File Structure Design

### Directory Organization

Organize files by purpose and access pattern:

```
games/<game-name>/
├── RULES.md                    # Static configuration (read-only)
├── state/                      # Active game state (read-write)
│   ├── game-state.json        # Authoritative state (GM writes, all read)
│   ├── turn-signal.json       # Turn notifications (GM writes, hooks read)
│   ├── player-actions/        # Player decisions (players write, GM reads)
│   │   ├── player-1.json
│   │   └── player-2.json
│   └── .locks/                # Lock files for coordination
│       └── game-state.lock
├── logs/                       # Completed games (append-only)
│   └── game-2024-01-27.json
└── traces/                     # Detailed debugging (append-only)
    └── game-2024-01-27.md
```

### File Naming Conventions

Use consistent, descriptive names:

**State files**: Describe the content
- `game-state.json` (not `state.json`)
- `turn-signal.json` (not `signal.json`)
- `player-1-hand.json` (not `p1.json`)

**Action files**: Include actor identifier
- `player-actions/player-1.json`
- `player-actions/player-2.json`

**Lock files**: Match the protected resource
- `.locks/game-state.lock`
- `.locks/turn-signal.lock`

**Log files**: Include timestamp
- `logs/game-2024-01-27-14-30-00.json`
- `traces/game-2024-01-27-14-30-00.md`

## JSON Schema Design

### Principles

**Include metadata**: Every file should have context
```json
{
  "fileType": "game-state",
  "version": "1.0",
  "timestamp": "2024-01-27T14:30:00Z",
  "gameId": "uno-game-42",
  "data": { ... }
}
```

**Use explicit types**: Avoid ambiguous values
```json
// Good
{"action": "play", "card": {"color": "Red", "value": "7"}}

// Bad
{"action": "p", "c": "R7"}
```

**Include validation**: Add fields for integrity checking
```json
{
  "turnNumber": 42,
  "previousTurnHash": "abc123...",
  "playerId": "player-1",
  "action": { ... }
}
```

### State File Schema

Authoritative game state maintained by gamemaster:

```json
{
  "fileType": "game-state",
  "version": "1.0",
  "timestamp": "2024-01-27T14:30:00Z",
  "game": "UNO",
  "gameId": "uno-game-42",
  "turnNumber": 12,
  "gameActive": true,
  "players": [
    {
      "id": "player-1",
      "cardCount": 5,
      "score": 0,
      "isActive": true
    }
  ],
  "currentPlayer": "player-1",
  "direction": 1,
  "deck": {
    "remaining": 42,
    "shuffled": true
  },
  "discardPile": [
    {"color": "Red", "value": "7"}
  ]
}
```

### Turn Signal Schema

Signals which player should act:

```json
{
  "fileType": "turn-signal",
  "version": "1.0",
  "timestamp": "2024-01-27T14:30:05Z",
  "gameId": "uno-game-42",
  "turnNumber": 12,
  "currentPlayer": "player-1",
  "availableActions": ["play", "draw"],
  "visibleState": {
    "discardTop": {"color": "Red", "value": "7"},
    "opponentCardCounts": {
      "player-2": 3,
      "player-3": 6,
      "player-4": 4
    }
  }
}
```

### Action File Schema

Player decision output:

```json
{
  "fileType": "player-action",
  "version": "1.0",
  "timestamp": "2024-01-27T14:30:10Z",
  "gameId": "uno-game-42",
  "playerId": "player-1",
  "turnNumber": 12,
  "action": "play",
  "card": {
    "color": "Blue",
    "value": "7"
  },
  "reasoning": "Changing to Blue to keep Red 7 as option",
  "confidence": 0.85
}
```

See **`references/schema-reference.md`** for complete schema specifications and validation rules.

## Atomic Operations

### Read-Modify-Write Pattern

When updating state based on previous value:

1. **Acquire lock**
```bash
while ! mkdir .locks/game-state.lock 2>/dev/null; do
  sleep 0.1
done
```

2. **Read current state**
```javascript
const state = JSON.parse(await Read("games/uno/state/game-state.json"));
```

3. **Modify state**
```javascript
state.turnNumber += 1;
state.currentPlayer = "player-2";
```

4. **Write atomically**
```javascript
// Write to temp file first
await Write("games/uno/state/game-state.json.tmp", JSON.stringify(state, null, 2));

// Atomic rename
await Bash("mv games/uno/state/game-state.json.tmp games/uno/state/game-state.json");
```

5. **Release lock**
```bash
rmdir .locks/game-state.lock
```

### Write-Only Pattern

When writing new file (no read needed):

1. **Generate unique filename**
```javascript
const filename = `player-actions/player-${playerId}-${Date.now()}.json`;
```

2. **Write directly** (no lock needed for new files)
```javascript
await Write(`games/uno/state/${filename}`, JSON.stringify(action, null, 2));
```

## Race Condition Handling

### Common Scenarios

**Scenario 1: Simultaneous state updates**
- **Problem**: Two agents try to update game-state.json
- **Solution**: Use lock files, only one agent writes at a time

**Scenario 2: Reading stale data**
- **Problem**: Agent reads state before latest update completes
- **Solution**: Include version numbers or timestamps, retry on conflict

**Scenario 3: Lost updates**
- **Problem**: Second write overwrites first write
- **Solution**: Atomic write pattern with lock acquisition

See **`references/race-conditions.md`** for detailed scenarios and solutions.

## File Locking Strategies

### Directory-Based Locks

Most reliable cross-platform approach:

```bash
# Acquire lock (mkdir is atomic)
while ! mkdir .locks/resource.lock 2>/dev/null; do
  sleep 0.1

  # Timeout after 10 seconds
  if [ $SECONDS -gt 10 ]; then
    echo "Lock timeout"
    exit 1
  fi
done

# Critical section
# ... perform locked operations ...

# Release lock
rmdir .locks/resource.lock
```

### PID-Based Locks

Track lock owner for debugging:

```bash
# Acquire with PID
mkdir .locks/resource.lock
echo $$ > .locks/resource.lock/owner

# Critical section
# ...

# Release
rm .locks/resource.lock/owner
rmdir .locks/resource.lock
```

### Stale Lock Detection

Handle crashes that leave locks:

```bash
# Check lock age
if [ -d .locks/resource.lock ]; then
  lock_age=$(($(date +%s) - $(stat -f%m .locks/resource.lock)))
  if [ $lock_age -gt 30 ]; then
    echo "Removing stale lock"
    rmdir .locks/resource.lock
  fi
fi
```

See **`references/locking-patterns.md`** for complete implementations.

## Hook Integration

File-based communication integrates with hooks for event-driven coordination:

**PostToolUse(Write) hook** detects file changes:
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "prompt",
      "prompt": "A file was written: {{tool_use.parameters.file_path}}. If this is a turn-signal or player-action file in games/*/state/, trigger appropriate agent response."
    }]
  }]
}
```

See **hook-sync** skill for detailed hook implementation.

## Best Practices

### File Design

✅ **DO:**
- Use descriptive, consistent naming
- Include metadata in every file
- Use JSON for structured data
- Version your schemas
- Add timestamps for debugging

❌ **DON'T:**
- Use cryptic abbreviations
- Mix different data types in one file
- Rely on file modification times only
- Change schemas without versioning
- Omit error context

### Concurrency

✅ **DO:**
- Use locks for read-modify-write
- Implement timeout for lock acquisition
- Clean up stale locks
- Write to temp files then rename
- Handle lock contention gracefully

❌ **DON'T:**
- Skip locks for "fast" operations
- Hold locks longer than necessary
- Ignore lock acquisition failures
- Write directly to final file
- Assume operations are instant

### Error Handling

✅ **DO:**
- Validate JSON schema on read
- Check file existence before reading
- Handle parse errors gracefully
- Log all file operations
- Provide clear error messages

❌ **DON'T:**
- Assume files always exist
- Skip validation
- Silently fail
- Leave incomplete files
- Ignore I/O errors

## Debugging

### File Inspection

Monitor file changes in real-time:

```bash
# Watch directory for changes
watch -n 0.5 'ls -lt games/uno/state/'

# Tail logs as they're written
tail -f games/uno/logs/game-latest.json

# View file with timestamps
stat -f "%Sm %N" -t "%Y-%m-%d %H:%M:%S" games/uno/state/*.json
```

### Validation Tools

Validate JSON files:

```bash
# Check JSON syntax
jq empty games/uno/state/game-state.json

# Validate against schema
ajv validate -s schema.json -d games/uno/state/game-state.json

# Pretty-print for inspection
jq . games/uno/state/game-state.json
```

### Common Issues

**File not found**: Check paths, ensure directory exists
**Parse error**: Validate JSON syntax, check for partial writes
**Stale data**: Verify atomic write pattern, check timestamps
**Lock contention**: Review lock acquisition logic, add logging
**Race condition**: Add locks, use atomic operations

## Additional Resources

### Reference Files

For detailed implementation guidance:
- **`references/schema-reference.md`** - Complete JSON schemas and validation
- **`references/race-conditions.md`** - Detailed race condition scenarios and solutions
- **`references/locking-patterns.md`** - Advanced locking implementations

### Example Files

Working examples in `examples/`:
- **`file-operations.sh`** - Shell scripts for atomic operations
- **`state-schemas.json`** - JSON schema definitions
- **`validation-example.js`** - File validation implementation

## Integration

This skill works together with:
- **game-coordination**: Agents that read/write these files
- **hook-sync**: Hooks that detect file changes and trigger agents

For complete multi-agent file-based coordination, use all three skills together.
