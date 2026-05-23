---
name: server-tick
description: Server-authoritative tick system for multiplayer games with lag compensation, anti-cheat validation, and deterministic physics. Prevents speed hacks and teleports while keeping gameplay fair for high-latency players.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: api
  time: 8h
  source: drift-masterguide
---

# Server-Authoritative Tick System

Server-side tick system with lag compensation for fair multiplayer gameplay.

## When to Use This Skill

- Building real-time multiplayer games
- Need to prevent cheating (speed hacks, teleports, aimbots)
- Want fair hit detection despite network latency
- Require deterministic physics simulation

## Core Concepts

Client-authoritative multiplayer is trivially exploitable. Server-authoritative feels laggy without lag compensation. The solution:

1. **Fixed tick rate** (60Hz) for deterministic physics
2. **Input validation** with violation tracking and decay
3. **Position history** for lag compensation (200ms window)
4. **Reduced broadcast rate** (20Hz) to save bandwidth

## Implementation

### Python

```python
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, Optional, Tuple, Callable, Awaitable
from enum import Enum
import asyncio
import time
import math


class ViolationType(str, Enum):
    SPEED_HACK = "speed_hack"
    TELEPORT = "teleport"
    INVALID_ACTION = "invalid_action"


@dataclass(frozen=True)
class TickConfig:
    rate_hz: int = 60
    broadcast_divisor: int = 3  # 60/3 = 20Hz broadcast
    max_speed: float = 300.0  # Units per second
    teleport_threshold: float = 100.0
    max_rewind_ms: int = 200
    violation_threshold: int = 10
    decay_per_second: float = 1.0
    
    @property
    def interval_ms(self) -> float:
        return 1000.0 / self.rate_hz
    
    def max_distance_per_tick(self) -> float:
        return self.max_speed / self.rate_hz


@dataclass
class PlayerInput:
    player_id: str
    tick: int
    dx: float = 0.0
    dy: float = 0.0
    timestamp_ms: float = 0.0


@dataclass
class PositionSnapshot:
    x: float
    y: float
    tick: int
    timestamp_ms: float


@dataclass
class PlayerState:
    player_id: str
    x: float = 0.0
    y: float = 0.0
    health: int = 100
    last_valid_position: Tuple[float, float] = (0.0, 0.0)
    violations: float = 0.0
    position_history: deque = field(default_factory=lambda: deque(maxlen=15))
    
    def record_position(self, tick: int, timestamp_ms: float) -> None:
        self.position_history.append(PositionSnapshot(
            x=self.x, y=self.y, tick=tick, timestamp_ms=timestamp_ms
        ))


@dataclass
class GameState:
    game_id: str
    tick: int = 0
    players: Dict[str, PlayerState] = field(default_factory=dict)
    running: bool = False
    start_time_ms: float = 0.0


class InputValidator:
    """Validates player inputs for anti-cheat."""
    
    def __init__(self, config: TickConfig):
        self._config = config
    
    def validate_movement(
        self, player: PlayerState, input: PlayerInput
    ) -> Tuple[bool, Optional[ViolationType]]:
        distance = math.sqrt(input.dx ** 2 + input.dy ** 2)
        max_distance = self._config.max_distance_per_tick()
        
        # 50% tolerance for network jitter
        if distance > max_distance * 1.5:
            return False, ViolationType.SPEED_HACK
        
        # Check for teleport
        new_x = player.x + input.dx
        new_y = player.y + input.dy
        last_x, last_y = player.last_valid_position
        jump_distance = math.sqrt((new_x - last_x) ** 2 + (new_y - last_y) ** 2)
        
        if jump_distance > self._config.teleport_threshold:
            return False, ViolationType.TELEPORT
        
        return True, None
    
    def apply_violation(self, player: PlayerState) -> Tuple[bool, bool]:
        player.violations += 1.0
        should_warn = player.violations >= self._config.violation_threshold * 0.5
        should_kick = player.violations >= self._config.violation_threshold
        return should_warn, should_kick
    
    def decay_violations(self, player: PlayerState, delta_seconds: float) -> None:
        decay = self._config.decay_per_second * delta_seconds
        player.violations = max(0.0, player.violations - decay)


class LagCompensator:
    """Lag compensation for fair hit detection."""
    
    def __init__(self, config: TickConfig):
        self._config = config
    
    def get_position_at_time(
        self, player: PlayerState, target_time_ms: float, current_time_ms: float
    ) -> Tuple[float, float]:
        # Clamp rewind to max window
        rewind_ms = current_time_ms - target_time_ms
        if rewind_ms > self._config.max_rewind_ms:
            target_time_ms = current_time_ms - self._config.max_rewind_ms
        
        if not player.position_history:
            return player.x, player.y
        
        # Find surrounding snapshots
        before: Optional[PositionSnapshot] = None
        after: Optional[PositionSnapshot] = None
        
        for snapshot in player.position_history:
            if snapshot.timestamp_ms <= target_time_ms:
                before = snapshot
            elif after is None:
                after = snapshot
                break
        
        if before is None:
            oldest = player.position_history[0]
            return oldest.x, oldest.y
        
        if after is None:
            return before.x, before.y
        
        # Interpolate between snapshots
        time_range = after.timestamp_ms - before.timestamp_ms
        if time_range <= 0:
            return before.x, before.y
        
        t = max(0.0, min(1.0, (target_time_ms - before.timestamp_ms) / time_range))
        x = before.x + (after.x - before.x) * t
        y = before.y + (after.y - before.y) * t
        
        return x, y
    
    def check_hit(
        self, shooter: PlayerState, target: PlayerState,
        shot_time_ms: float, current_time_ms: float, hit_radius: float = 20.0
    ) -> Tuple[bool, Tuple[float, float]]:
        target_x, target_y = self.get_position_at_time(target, shot_time_ms, current_time_ms)
        distance = math.sqrt((shooter.x - target_x) ** 2 + (shooter.y - target_y) ** 2)
        return distance <= hit_radius, (target_x, target_y)


class TickSystem:
    """Server-authoritative tick system."""
    
    def __init__(self, config: TickConfig = None):
        self._config = config or TickConfig()
        self._games: Dict[str, GameState] = {}
        self._tasks: Dict[str, asyncio.Task] = {}
        self._validator = InputValidator(self._config)
        self._lag_comp = LagCompensator(self._config)
        self._broadcast_callback: Optional[Callable[[str, dict], Awaitable[None]]] = None
        self._kick_callback: Optional[Callable[[str, str, str], Awaitable[None]]] = None
    
    def set_broadcast_callback(self, callback: Callable[[str, dict], Awaitable[None]]) -> None:
        self._broadcast_callback = callback
    
    def set_kick_callback(self, callback: Callable[[str, str, str], Awaitable[None]]) -> None:
        self._kick_callback = callback
    
    def create_game(
        self, game_id: str, player1_id: str, player2_id: str,
        spawn1: Tuple[float, float] = (100, 300),
        spawn2: Tuple[float, float] = (700, 300)
    ) -> GameState:
        game = GameState(game_id=game_id)
        game.players[player1_id] = PlayerState(
            player_id=player1_id, x=spawn1[0], y=spawn1[1], last_valid_position=spawn1
        )
        game.players[player2_id] = PlayerState(
            player_id=player2_id, x=spawn2[0], y=spawn2[1], last_valid_position=spawn2
        )
        self._games[game_id] = game
        return game
    
    async def start_game(self, game_id: str) -> None:
        game = self._games.get(game_id)
        if not game:
            raise ValueError(f"Game {game_id} not found")
        
        game.running = True
        game.start_time_ms = time.time() * 1000
        self._tasks[game_id] = asyncio.create_task(self._tick_loop(game_id))
    
    async def stop_game(self, game_id: str) -> None:
        game = self._games.get(game_id)
        if game:
            game.running = False
        
        task = self._tasks.pop(game_id, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        self._games.pop(game_id, None)
    
    async def process_input(self, game_id: str, input: PlayerInput) -> bool:
        game = self._games.get(game_id)
        if not game or not game.running:
            return False
        
        player = game.players.get(input.player_id)
        if not player:
            return False
        
        valid, violation = self._validator.validate_movement(player, input)
        
        if not valid and violation:
            _, should_kick = self._validator.apply_violation(player)
            if should_kick and self._kick_callback:
                await self._kick_callback(game_id, input.player_id, f"Anti-cheat: {violation.value}")
            return False
        
        player.x += input.dx
        player.y += input.dy
        player.last_valid_position = (player.x, player.y)
        return True
    
    async def _tick_loop(self, game_id: str) -> None:
        game = self._games.get(game_id)
        if not game:
            return
        
        interval = self._config.interval_ms / 1000.0
        last_time = time.time()
        
        while game.running:
            tick_start = time.time()
            delta = tick_start - last_time
            last_time = tick_start
            
            await self._tick(game, delta)
            
            if game.tick % self._config.broadcast_divisor == 0:
                await self._broadcast_state(game)
            
            game.tick += 1
            
            elapsed = time.time() - tick_start
            sleep_time = max(0, interval - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
    
    async def _tick(self, game: GameState, delta: float) -> None:
        current_time_ms = time.time() * 1000
        for player in game.players.values():
            self._validator.decay_violations(player, delta)
            player.record_position(game.tick, current_time_ms)
    
    async def _broadcast_state(self, game: GameState) -> None:
        if not self._broadcast_callback:
            return
        
        state = {
            "type": "game_state",
            "tick": game.tick,
            "players": {
                pid: {"x": p.x, "y": p.y, "health": p.health}
                for pid, p in game.players.items()
            }
        }
        await self._broadcast_callback(game.game_id, state)
```

### TypeScript

```typescript
enum ViolationType {
  SPEED_HACK = 'speed_hack',
  TELEPORT = 'teleport',
  INVALID_ACTION = 'invalid_action',
}

interface TickConfig {
  rateHz: number;
  broadcastDivisor: number;
  maxSpeed: number;
  teleportThreshold: number;
  maxRewindMs: number;
  violationThreshold: number;
  decayPerSecond: number;
}

const DEFAULT_CONFIG: TickConfig = {
  rateHz: 60,
  broadcastDivisor: 3,
  maxSpeed: 300,
  teleportThreshold: 100,
  maxRewindMs: 200,
  violationThreshold: 10,
  decayPerSecond: 1.0,
};

interface PositionSnapshot {
  x: number;
  y: number;
  tick: number;
  timestampMs: number;
}

interface PlayerState {
  playerId: string;
  x: number;
  y: number;
  health: number;
  lastValidPosition: [number, number];
  violations: number;
  positionHistory: PositionSnapshot[];
}

class TickSystem {
  private config: TickConfig;
  private games = new Map<string, GameState>();
  private intervals = new Map<string, NodeJS.Timeout>();
  
  constructor(config: Partial<TickConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }
  
  createGame(gameId: string, player1Id: string, player2Id: string): GameState {
    const game: GameState = {
      gameId,
      tick: 0,
      players: new Map([
        [player1Id, this.createPlayer(player1Id, 100, 300)],
        [player2Id, this.createPlayer(player2Id, 700, 300)],
      ]),
      running: false,
    };
    this.games.set(gameId, game);
    return game;
  }
  
  private createPlayer(id: string, x: number, y: number): PlayerState {
    return {
      playerId: id,
      x, y,
      health: 100,
      lastValidPosition: [x, y],
      violations: 0,
      positionHistory: [],
    };
  }
  
  processInput(gameId: string, input: PlayerInput): boolean {
    const game = this.games.get(gameId);
    if (!game?.running) return false;
    
    const player = game.players.get(input.playerId);
    if (!player) return false;
    
    const distance = Math.sqrt(input.dx ** 2 + input.dy ** 2);
    const maxDistance = this.config.maxSpeed / this.config.rateHz;
    
    if (distance > maxDistance * 1.5) {
      player.violations += 1;
      return false;
    }
    
    player.x += input.dx;
    player.y += input.dy;
    player.lastValidPosition = [player.x, player.y];
    return true;
  }
  
  getPositionAtTime(player: PlayerState, targetTimeMs: number, currentTimeMs: number): [number, number] {
    const rewindMs = Math.min(currentTimeMs - targetTimeMs, this.config.maxRewindMs);
    const clampedTargetTime = currentTimeMs - rewindMs;
    
    if (player.positionHistory.length === 0) {
      return [player.x, player.y];
    }
    
    let before: PositionSnapshot | null = null;
    let after: PositionSnapshot | null = null;
    
    for (const snapshot of player.positionHistory) {
      if (snapshot.timestampMs <= clampedTargetTime) {
        before = snapshot;
      } else if (!after) {
        after = snapshot;
        break;
      }
    }
    
    if (!before) return [player.positionHistory[0].x, player.positionHistory[0].y];
    if (!after) return [before.x, before.y];
    
    const t = Math.max(0, Math.min(1, 
      (clampedTargetTime - before.timestampMs) / (after.timestampMs - before.timestampMs)
    ));
    
    return [
      before.x + (after.x - before.x) * t,
      before.y + (after.y - before.y) * t,
    ];
  }
}
```

## Usage Examples

### Game Setup

```python
tick_system = TickSystem()

# Create game with two players
game = tick_system.create_game("match-123", "player-1", "player-2")

# Set up callbacks
tick_system.set_broadcast_callback(broadcast_to_players)
tick_system.set_kick_callback(kick_player)

# Start the game loop
await tick_system.start_game("match-123")
```

### Processing Player Input

```python
# When receiving input from client
input = PlayerInput(
    player_id="player-1",
    tick=game.tick,
    dx=5.0,
    dy=2.0,
    timestamp_ms=client_timestamp
)

valid = await tick_system.process_input("match-123", input)
if not valid:
    # Input was rejected (possible cheat attempt)
    pass
```

### Lag-Compensated Hit Detection

```python
# When player fires a shot
shooter = game.players["player-1"]
target = game.players["player-2"]

hit, target_pos = tick_system._lag_comp.check_hit(
    shooter=shooter,
    target=target,
    shot_time_ms=client_shot_timestamp,
    current_time_ms=time.time() * 1000,
    hit_radius=20.0
)

if hit:
    target.health -= 25
```

## Best Practices

1. Tune tick rate for your game - 30-60Hz is typical for action games
2. Set broadcast rate lower than tick rate to save bandwidth
3. Keep lag compensation window reasonable (100-200ms)
4. Use violation decay to forgive occasional network hiccups
5. Log all kicks with full context for review
6. Test with simulated high latency

## Common Mistakes

- Running physics at variable rate (causes non-determinism)
- No tolerance for network jitter (false positives)
- Lag compensation window too large (feels unfair to targets)
- Not decaying violations (kicks legitimate players)
- Broadcasting every tick (wastes bandwidth)
- Trusting client timestamps without bounds checking

## Related Patterns

- websocket-management - Connection handling for game clients
- atomic-matchmaking - Creating matches before game starts
- graceful-shutdown - Draining games on server shutdown
