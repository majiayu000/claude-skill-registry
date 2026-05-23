---
name: Game Coordination
description: This skill should be used when implementing "gamemaster agents", "spawn player agents", "coordinate multiple agents", "parallel agent execution", "game orchestration patterns", or building multi-agent systems where one agent orchestrates others. Provides comprehensive guidance for creating game-testing frameworks with dynamic agent spawning.
version: 0.1.0
---

# Game Coordination Skill

## Overview

This skill provides guidance for implementing multi-agent game coordination systems where a central gamemaster agent orchestrates multiple player agents running in parallel. The gamemaster acts as an impartial rule enforcer while player agents act competitively to win.

## Core Concepts

### Gamemaster Pattern

The gamemaster is a central orchestrator agent responsible for:

- **Rule enforcement**: Validate player actions against game rules
- **State management**: Maintain authoritative game state
- **Turn coordination**: Signal which player should act next
- **Agent spawning**: Dynamically create player agents using Task tool
- **Game lifecycle**: Initialize, run, and conclude game sessions

**Key characteristic**: The gamemaster is impartial—it does not try to win, only to enforce rules fairly.

### Player Agent Pattern

Player agents are competitive agents that:

- **Act independently**: Make decisions based on their game state
- **Run in parallel**: Multiple players can be spawned simultaneously
- **Use Haiku model**: Fast, cost-effective for repetitive game actions
- **Receive context**: Get game rules and their current view of game state
- **Write decisions**: Output actions to designated files for gamemaster to process

**Key characteristic**: Player agents try to win within the rules.

### Dynamic Agent Spawning

Use the Task tool to spawn agents dynamically with custom prompts:

```markdown
Use Task tool with:
- subagent_type: "general-purpose"
- model: "haiku" (for speed and cost efficiency)
- prompt: Custom prompt with game context
- run_in_background: true (for parallel execution)
```

This allows creating agents with:
- Game-specific rules and objectives
- Current game state visibility
- Player-specific information (hand, score, etc.)
- Strategic instructions

### Agent Coordination Lifecycle

**Phase 1: Initialization**
1. Gamemaster reads game rules from `games/<game-name>/RULES.md`
2. Parse YAML frontmatter for game parameters
3. Initialize game state files in `games/<game-name>/state/`
4. Create initial deck, deal cards, set up turn order

**Phase 2: Turn Loop**
1. Gamemaster writes turn signal to `state/turn-signal.json`
2. Hook detects file change and triggers player agent spawn
3. Player agent reads game state and their hand
4. Player agent writes action decision to `state/player-actions/<player-id>.json`
5. Hook detects action file and triggers gamemaster validation
6. Gamemaster validates action, updates state, signals next turn
7. Repeat until win condition met

**Phase 3: Conclusion**
1. Gamemaster detects win condition
2. Calculate scores and determine winner
3. Write game log to `games/<game-name>/logs/`
4. Write detailed trace to `games/<game-name>/traces/`
5. Clean up active state files

## Gamemaster Implementation

### Required Tools

The gamemaster agent needs:
- **Read**: Load game rules and state files
- **Write**: Update game state and signal files
- **Task**: Spawn player agents dynamically
- **Bash**: Execute validation scripts if needed

### Initialization Steps

To initialize a game session:

1. **Read game rules**:
```javascript
// Read YAML frontmatter and markdown body
const rules = await Read("games/<game-name>/RULES.md");
const config = parseYAMLFrontmatter(rules);
```

2. **Create state directory**:
```bash
mkdir -p games/<game-name>/state/player-actions
```

3. **Initialize game state**:
```javascript
// Write initial state
const gameState = {
  game: config.name,
  players: generatePlayers(config.players),
  deck: initializeDeck(config.deck_composition),
  discardPile: [],
  currentPlayer: 0,
  direction: 1, // 1 for clockwise, -1 for counter-clockwise
  turnNumber: 1,
  gameActive: true
};
Write("games/<game-name>/state/game-state.json", JSON.stringify(gameState, null, 2));
```

4. **Deal cards and signal first turn**:
```javascript
// Deal cards to players
dealCardsToPlayers(gameState, config.cards_per_player);

// Signal first player's turn
const turnSignal = {
  currentPlayer: gameState.players[0].id,
  turnNumber: 1,
  availableActions: ["play", "draw"],
  visibleState: getVisibleState(gameState, gameState.players[0].id)
};
Write("games/<game-name>/state/turn-signal.json", JSON.stringify(turnSignal, null, 2));
```

### Turn Processing

When processing a player's turn:

1. **Wait for player action**:
```javascript
// Hook will trigger gamemaster when action file appears
const action = await Read(`games/<game-name>/state/player-actions/${playerId}.json`);
```

2. **Validate action**:
```javascript
// Check if action is legal according to rules
if (!isValidAction(action, gameState, playerId)) {
  // Handle invalid action (reject, request retry, penalize)
  handleInvalidAction(playerId, action, gameState);
  return;
}
```

3. **Apply action effects**:
```javascript
// Update game state based on action
applyAction(action, gameState);

// Check for special card effects
if (action.card.type === "action") {
  applySpecialEffect(action.card, gameState);
}
```

4. **Check win condition**:
```javascript
if (checkWinCondition(gameState, playerId)) {
  concludeGame(gameState, playerId);
  return;
}
```

5. **Signal next turn**:
```javascript
// Determine next player (consider Skip, Reverse effects)
const nextPlayer = determineNextPlayer(gameState);
const turnSignal = {
  currentPlayer: nextPlayer.id,
  turnNumber: gameState.turnNumber + 1,
  availableActions: getAvailableActions(gameState, nextPlayer.id),
  visibleState: getVisibleState(gameState, nextPlayer.id)
};
Write("games/<game-name>/state/turn-signal.json", JSON.stringify(turnSignal, null, 2));
```

## Player Agent Implementation

### Spawning Player Agents

When a turn signal is written, spawn the appropriate player agent:

```markdown
Task tool invocation:
- subagent_type: "general-purpose"
- model: "haiku"
- description: "Player agent turn"
- prompt: `You are Player ${playerId} in a game of ${gameName}.

GAME RULES:
${gameRules}

YOUR CURRENT HAND:
${JSON.stringify(playerHand, null, 2)}

VISIBLE GAME STATE:
${JSON.stringify(visibleState, null, 2)}

OBJECTIVE: Choose the best legal action to help you win the game. You are competitive and want to win.

Analyze the current situation, consider your available actions, and choose the optimal play. Write your decision to games/${gameName}/state/player-actions/${playerId}.json in the following format:

{
  "playerId": "${playerId}",
  "action": "play" | "draw",
  "card": { "color": "Red", "value": "7" } // if action is "play"
  "reasoning": "Brief explanation of your choice"
}

Use the Write tool to save your decision.`
- run_in_background: false (wait for player decision)
```

### Player Agent Context

Provide players with:

**Full information**:
- Complete game rules
- Their own hand (private)
- Turn number and available actions

**Partial information**:
- Number of cards each opponent has (not contents)
- Discard pile (visible cards)
- Current game direction and turn order
- Recent actions (from game log)

**Hidden information**:
- Opponent hands
- Remaining deck contents (unless rules specify otherwise)

### Player Agent Goals

Instruct player agents to:
- Make legal moves according to rules
- Play competitively to win
- Consider short-term and long-term strategy
- Respond to opponent actions
- Manage resources (cards, special actions)

## Advanced Patterns

### Parallel Agent Execution

For simultaneous turns or phases:

```markdown
// Spawn multiple agents in parallel
const playerAgentTasks = players.map(player => {
  return Task({
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: generatePlayerPrompt(player, gameState),
    run_in_background: true // Run in parallel
  });
});

// Wait for all agents to complete
const results = await Promise.all(playerAgentTasks.map(task =>
  TaskOutput({ task_id: task.id })
));

// Process all actions
results.forEach((result, index) => {
  processPlayerAction(players[index], result);
});
```

### Agent Personality Variations

Create different player strategies by varying prompts:

```javascript
const strategies = {
  aggressive: "Play aggressively. Use action cards immediately to disrupt opponents.",
  defensive: "Play conservatively. Save action cards for defensive situations.",
  balanced: "Balance offense and defense. Adapt to the game situation."
};

// Assign random or specific strategies
const playerPrompt = generatePlayerPrompt(player, gameState, strategies.aggressive);
```

### Error Handling

Handle player agent failures gracefully:

```javascript
try {
  const playerDecision = await spawnPlayerAgent(player, gameState);
} catch (error) {
  // Agent failed - options:
  // 1. Retry with same agent
  // 2. Make random legal move
  // 3. Skip turn with penalty
  // 4. End game

  handlePlayerAgentFailure(player, error, gameState);
}
```

## File Structure Integration

Coordinate with file-based communication:

**Gamemaster writes**:
- `games/<game-name>/state/game-state.json` - Authoritative state
- `games/<game-name>/state/turn-signal.json` - Turn notifications
- `games/<game-name>/logs/game-<timestamp>.json` - Completed games
- `games/<game-name>/traces/game-<timestamp>.md` - Detailed traces

**Player agents write**:
- `games/<game-name>/state/player-actions/<player-id>.json` - Action decisions

**Both read**:
- `games/<game-name>/RULES.md` - Game rules and configuration

## Integration with Hooks

Hooks coordinate file-based communication:

**PostToolUse(Write) hook** detects file changes:
- If `turn-signal.json` written → Spawn player agent for that turn
- If `player-actions/<player-id>.json` written → Trigger gamemaster validation

See **hook-sync** skill for detailed hook implementation patterns.

## Best Practices

### Gamemaster Design

✅ **DO:**
- Enforce rules strictly and fairly
- Validate all player actions
- Maintain authoritative game state
- Log all actions for debugging
- Provide clear error messages

❌ **DON'T:**
- Make decisions for players
- Favor any player
- Allow ambiguous rule interpretations
- Skip validation for performance

### Player Agent Design

✅ **DO:**
- Give each agent complete rule context
- Provide current visible game state
- Encourage competitive play
- Use Haiku model for speed
- Vary strategies for testing

❌ **DON'T:**
- Give players information they shouldn't have
- Make agents cooperate (unless rules require it)
- Use slow models for simple games
- Hardcode strategies

### Coordination Design

✅ **DO:**
- Use clear file-based protocols
- Handle timing and race conditions
- Implement proper error handling
- Log all agent interactions
- Make debugging easy

❌ **DON'T:**
- Assume perfect agent behavior
- Ignore edge cases
- Create circular dependencies
- Make coordination implicit

## Additional Resources

### Reference Files

For detailed implementation patterns, consult:
- **`references/agent-spawning-patterns.md`** - Detailed Task tool patterns, error handling, parallel execution
- **`references/gamemaster-implementation.md`** - Complete gamemaster architecture, validation strategies, state management

### Example Files

Working examples in `examples/`:
- **`gamemaster-prompt.md`** - Example gamemaster system prompt
- **`player-prompt.md`** - Example player agent prompt template

## Troubleshooting

**Agents not spawning**:
- Verify Task tool has correct subagent_type
- Check prompt is properly formatted
- Ensure game state files exist

**Players making invalid moves**:
- Strengthen rule descriptions in prompt
- Add validation examples
- Increase gamemaster validation strictness

**Coordination issues**:
- Check file-based communication protocol (see file-protocol skill)
- Verify hooks are triggering correctly (see hook-sync skill)
- Add logging to track agent interactions

**Performance problems**:
- Use Haiku for player agents
- Run players in parallel when possible
- Minimize context in player prompts
- Cache game rules

For comprehensive multi-agent coordination in game testing contexts, combine this skill with **file-protocol** (communication) and **hook-sync** (event triggering).
