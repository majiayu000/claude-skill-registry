---
name: stop-game
description: Emergency halt of active game session. Use when user wants to stop a running game, halt playtest, cancel game simulation, or clean up game state.
argument-hint: [game-name]
allowed-tools: Read, Write, Bash, Glob
disable-model-invocation: true
---

# Stop Game - Emergency Halt

Emergency halt an active game session and clean up state files.

## Arguments

- `$0` (optional): Game name to stop. If omitted, finds the active game.

## Implementation Steps

### 1. Find Active Game

```javascript
let gameName = "$0";

if (!gameName) {
  // Find active game by checking for active game-state files
  const stateFiles = await Glob("games/*/state/game-state.json");

  for (const stateFile of stateFiles) {
    const state = JSON.parse(await Read(stateFile));
    if (state.gameActive) {
      gameName = stateFile.split('/')[1];
      break;
    }
  }

  if (!gameName) {
    console.log("No active games found");
    return;
  }
}
```

### 2. Read Current State

```javascript
const statePath = `games/${gameName}/state/game-state.json`;
const gameState = JSON.parse(await Read(statePath));

if (!gameState.gameActive) {
  console.log(`Game ${gameName} is not active`);
  return;
}
```

### 3. Mark Game as Stopped

```javascript
gameState.gameActive = false;
gameState.gameStatus = "stopped";
gameState.stoppedAt = new Date().toISOString();
gameState.stoppedReason = "Manual stop by user";

await Write(statePath, JSON.stringify(gameState, null, 2));
```

### 4. Write Partial Log

Save incomplete game log for analysis:

```javascript
const logTimestamp = new Date().toISOString().replace(/[:.]/g, '-');
const partialLog = {
  fileType: "game-log",
  status: "stopped",
  game: gameName,
  gameId: gameState.gameId,
  stoppedAt: gameState.stoppedAt,
  completedTurns: gameState.turnNumber,
  finalState: gameState
};

await Write(
  `games/${gameName}/logs/game-stopped-${logTimestamp}.json`,
  JSON.stringify(partialLog, null, 2)
);
```

### 5. Clean Up State Files

```bash
rm -f games/${gameName}/state/turn-signal.json
rm -f games/${gameName}/state/player-actions/*.json
rm -rf games/${gameName}/state/.locks/*
```

### 6. Report to User

Display:
- Game name and ID
- Turn number when stopped
- Final player states
- Location of partial log
