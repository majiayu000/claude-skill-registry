---
name: Real-time Multiplayer
description: Enabling simultaneous gameplay across networks using WebSocket or WebRTC, including state synchronization, lag compensation, client-side prediction, and server authority for fair gameplay.
---

# Real-time Multiplayer

> **Current Level:** Advanced  
> **Domain:** Gaming / Networking

---

## Overview

Real-time multiplayer enables simultaneous gameplay across networks. This guide covers networking, state synchronization, and lag compensation for building responsive multiplayer games that handle network latency and maintain game state consistency.

## Real-time Networking

### WebSocket vs WebRTC

| Feature | WebSocket | WebRTC |
|---------|-----------|--------|
| **Latency** | 50-100ms | 10-30ms |
| **Topology** | Client-Server | Peer-to-Peer |
| **Reliability** | TCP (reliable) | UDP (unreliable) |
| **Use Case** | Turn-based, MOBA | FPS, Racing |

## Client-side Prediction

```typescript
// Client-side prediction for smooth gameplay
export class ClientPrediction {
  private pendingInputs: Input[] = [];
  private lastProcessedInput = 0;

  processInput(input: Input): void {
    // Apply input immediately (prediction)
    this.applyInput(input);

    // Store for server reconciliation
    this.pendingInputs.push(input);

    // Send to server
    this.sendToServer(input);
  }

  private applyInput(input: Input): void {
    // Update local state based on input
    switch (input.type) {
      case 'move':
        this.player.position.x += input.dx;
        this.player.position.y += input.dy;
        break;
      
      case 'jump':
        this.player.velocity.y = input.force;
        break;
    }
  }

  private sendToServer(input: Input): void {
    socket.emit('player-input', {
      inputId: input.id,
      type: input.type,
      data: input.data,
      timestamp: Date.now()
    });
  }
}

interface Input {
  id: number;
  type: string;
  data: any;
  dx?: number;
  dy?: number;
  force?: number;
}
```

## Server Reconciliation

```typescript
// Server reconciliation to correct client predictions
export class ServerReconciliation {
  reconcile(serverState: GameState): void {
    // Find last processed input
    const lastProcessedInput = serverState.lastProcessedInput;

    // Remove processed inputs
    this.pendingInputs = this.pendingInputs.filter(
      input => input.id > lastProcessedInput
    );

    // Set state to server's authoritative state
    this.player.position = serverState.position;
    this.player.velocity = serverState.velocity;

    // Re-apply pending inputs
    for (const input of this.pendingInputs) {
      this.applyInput(input);
    }
  }
}

interface GameState {
  lastProcessedInput: number;
  position: { x: number; y: number };
  velocity: { x: number; y: number };
}
```

## Lag Compensation

```typescript
// Lag compensation for hit detection
export class LagCompensation {
  private stateHistory: Map<number, GameState> = new Map();
  private maxHistorySize = 60; // 1 second at 60 FPS

  saveState(timestamp: number, state: GameState): void {
    this.stateHistory.set(timestamp, state);

    // Limit history size
    if (this.stateHistory.size > this.maxHistorySize) {
      const oldest = Math.min(...this.stateHistory.keys());
      this.stateHistory.delete(oldest);
    }
  }

  rewindToTimestamp(timestamp: number): GameState | null {
    // Find closest state
    let closestTime = 0;
    let minDiff = Infinity;

    for (const time of this.stateHistory.keys()) {
      const diff = Math.abs(time - timestamp);
      if (diff < minDiff) {
        minDiff = diff;
        closestTime = time;
      }
    }

    return this.stateHistory.get(closestTime) || null;
  }

  checkHit(
    shooterTimestamp: number,
    targetPosition: { x: number; y: number },
    shotPosition: { x: number; y: number }
  ): boolean {
    // Rewind to shooter's timestamp
    const historicalState = this.rewindToTimestamp(shooterTimestamp);

    if (!historicalState) return false;

    // Check if shot hit target at that time
    const distance = Math.sqrt(
      Math.pow(historicalState.position.x - shotPosition.x, 2) +
      Math.pow(historicalState.position.y - shotPosition.y, 2)
    );

    return distance < 10; // Hit radius
  }
}
```

## State Synchronization

```typescript
// State synchronization strategies
export class StateSynchronization {
  // Full state sync (simple but bandwidth-heavy)
  syncFullState(state: GameState): void {
    socket.emit('state-update', state);
  }

  // Delta compression (only send changes)
  syncDeltaState(previousState: GameState, currentState: GameState): void {
    const delta = this.calculateDelta(previousState, currentState);
    
    if (Object.keys(delta).length > 0) {
      socket.emit('state-delta', delta);
    }
  }

  private calculateDelta(prev: GameState, current: GameState): Partial<GameState> {
    const delta: Partial<GameState> = {};

    if (prev.position.x !== current.position.x || prev.position.y !== current.position.y) {
      delta.position = current.position;
    }

    if (prev.velocity.x !== current.velocity.x || prev.velocity.y !== current.velocity.y) {
      delta.velocity = current.velocity;
    }

    return delta;
  }

  // Interpolation for smooth movement
  interpolate(from: GameState, to: GameState, alpha: number): GameState {
    return {
      position: {
        x: from.position.x + (to.position.x - from.position.x) * alpha,
        y: from.position.y + (to.position.y - from.position.y) * alpha
      },
      velocity: {
        x: from.velocity.x + (to.velocity.x - from.velocity.x) * alpha,
        y: from.velocity.y + (to.velocity.y - from.velocity.y) * alpha
      },
      lastProcessedInput: to.lastProcessedInput
    };
  }
}
```

## Input Handling

```typescript
// Input buffering and processing
export class InputHandler {
  private inputBuffer: Input[] = [];
  private inputSequence = 0;

  captureInput(type: string, data: any): void {
    const input: Input = {
      id: ++this.inputSequence,
      type,
      data,
      timestamp: Date.now()
    };

    this.inputBuffer.push(input);
  }

  processInputs(deltaTime: number): void {
    while (this.inputBuffer.length > 0) {
      const input = this.inputBuffer.shift()!;
      this.processInput(input, deltaTime);
    }
  }

  private processInput(input: Input, deltaTime: number): void {
    switch (input.type) {
      case 'move':
        const speed = 5;
        this.player.position.x += input.data.direction.x * speed * deltaTime;
        this.player.position.y += input.data.direction.y * speed * deltaTime;
        break;

      case 'shoot':
        this.createProjectile(input.data.angle);
        break;
    }
  }

  private createProjectile(angle: number): void {
    // Create projectile
  }
}
```

## Physics Synchronization

```typescript
// Deterministic physics for multiplayer
export class PhysicsSync {
  private fixedTimeStep = 1 / 60; // 60 FPS
  private accumulator = 0;

  update(deltaTime: number): void {
    this.accumulator += deltaTime;

    // Fixed timestep updates
    while (this.accumulator >= this.fixedTimeStep) {
      this.fixedUpdate(this.fixedTimeStep);
      this.accumulator -= this.fixedTimeStep;
    }
  }

  private fixedUpdate(dt: number): void {
    // Update physics deterministically
    for (const entity of this.entities) {
      // Apply velocity
      entity.position.x += entity.velocity.x * dt;
      entity.position.y += entity.velocity.y * dt;

      // Apply gravity
      entity.velocity.y += 9.8 * dt;

      // Collision detection
      this.checkCollisions(entity);
    }
  }

  private checkCollisions(entity: Entity): void {
    // Collision detection logic
  }
}

interface Entity {
  position: { x: number; y: number };
  velocity: { x: number; y: number };
}
```

## Cheating Prevention

```typescript
// Server-side validation
export class AntiCheatService {
  validatePlayerAction(
    playerId: string,
    action: PlayerAction,
    gameState: GameState
  ): boolean {
    switch (action.type) {
      case 'move':
        return this.validateMovement(playerId, action, gameState);
      
      case 'shoot':
        return this.validateShot(playerId, action, gameState);
      
      default:
        return false;
    }
  }

  private validateMovement(
    playerId: string,
    action: PlayerAction,
    gameState: GameState
  ): boolean {
    const player = gameState.players.get(playerId);
    if (!player) return false;

    // Check if movement is within max speed
    const maxSpeed = 10;
    const distance = Math.sqrt(
      Math.pow(action.data.x - player.position.x, 2) +
      Math.pow(action.data.y - player.position.y, 2)
    );

    const timeDelta = (Date.now() - player.lastUpdate) / 1000;
    const speed = distance / timeDelta;

    if (speed > maxSpeed) {
      this.flagCheater(playerId, 'speed_hack');
      return false;
    }

    return true;
  }

  private validateShot(
    playerId: string,
    action: PlayerAction,
    gameState: GameState
  ): boolean {
    const player = gameState.players.get(playerId);
    if (!player) return false;

    // Check fire rate
    const minFireInterval = 100; // ms
    const timeSinceLastShot = Date.now() - player.lastShotTime;

    if (timeSinceLastShot < minFireInterval) {
      this.flagCheater(playerId, 'rapid_fire');
      return false;
    }

    return true;
  }

  private flagCheater(playerId: string, reason: string): void {
    console.log(`Cheating detected: ${playerId} - ${reason}`);
    // Log to database, potentially ban player
  }
}

interface PlayerAction {
  type: string;
  data: any;
}
```

## Room/Lobby System

```typescript
// Room management with Colyseus
import { Room, Client } from 'colyseus';

export class GameRoom extends Room {
  maxClients = 4;

  onCreate(options: any): void {
    console.log('Room created:', this.roomId);

    this.setState({
      players: new Map(),
      gameStarted: false
    });

    this.setSimulationInterval((deltaTime) => this.update(deltaTime));
  }

  onJoin(client: Client, options: any): void {
    console.log('Player joined:', client.sessionId);

    this.state.players.set(client.sessionId, {
      id: client.sessionId,
      position: { x: 0, y: 0 },
      velocity: { x: 0, y: 0 }
    });

    // Start game when room is full
    if (this.clients.length === this.maxClients) {
      this.startGame();
    }
  }

  onLeave(client: Client): void {
    console.log('Player left:', client.sessionId);
    this.state.players.delete(client.sessionId);
  }

  onMessage(client: Client, message: any): void {
    if (message.type === 'input') {
      this.handleInput(client.sessionId, message.data);
    }
  }

  private startGame(): void {
    this.state.gameStarted = true;
    this.broadcast('game-started');
  }

  private update(deltaTime: number): void {
    // Update game state
    for (const [id, player] of this.state.players) {
      player.position.x += player.velocity.x * deltaTime;
      player.position.y += player.velocity.y * deltaTime;
    }
  }

  private handleInput(playerId: string, input: any): void {
    const player = this.state.players.get(playerId);
    if (player) {
      player.velocity = input.velocity;
    }
  }
}
```

---

## Quick Start

### Client-Side Prediction

```typescript
// Client predicts movement
function predictMovement(playerId: string, input: Input) {
  const player = getPlayer(playerId)
  player.position.x += input.deltaX
  player.position.y += input.deltaY
  
  // Send to server
  socket.emit('player-move', { playerId, input })
}

// Server corrects if needed
socket.on('server-update', (update) => {
  const player = getPlayer(update.playerId)
  
  // Reconcile if different
  if (player.position.x !== update.position.x) {
    player.position = update.position  // Server is authoritative
  }
})
```

### Lag Compensation

```typescript
// Server rewinds time for hit detection
function checkHit(shooterId: string, targetId: string, shotTime: number) {
  const lag = getPlayerLatency(shooterId)
  const rewindTime = shotTime - lag
  
  // Check hit at rewind time
  const targetPos = getPlayerPositionAtTime(targetId, rewindTime)
  return isHit(shotPosition, targetPos)
}
```

---

## Production Checklist

- [ ] **Networking**: Choose WebSocket or WebRTC
- [ ] **Client Prediction**: Implement client-side prediction
- [ ] **Server Authority**: Server is authoritative
- [ ] **Reconciliation**: Correct client predictions
- [ ] **Lag Compensation**: Compensate for network latency
- [ ] **State Synchronization**: Efficient state sync
- [ ] **Anti-cheat**: Validate all actions server-side
- [ ] **Bandwidth**: Optimize network usage
- [ ] **Testing**: Test with various latencies
- [ ] **Documentation**: Document networking architecture
- [ ] **Monitoring**: Monitor network performance
- [ ] **Error Handling**: Handle network errors

---

## Anti-patterns

### ❌ Don't: Trust Client

```typescript
// ❌ Bad - Trust client position
function movePlayer(playerId: string, newPosition: Position) {
  players[playerId].position = newPosition  // Client can cheat!
}
```

```typescript
// ✅ Good - Server calculates
function movePlayer(playerId: string, input: Input) {
  const player = players[playerId]
  // Server calculates movement
  player.position.x += input.deltaX * player.speed
  player.position.y += input.deltaY * player.speed
}
```

### ❌ Don't: No Lag Compensation

```typescript
// ❌ Bad - No lag compensation
function checkHit(shooterPos: Position, targetPos: Position) {
  return distance(shooterPos, targetPos) < HIT_RADIUS
  // Unfair for high latency players!
}
```

```typescript
// ✅ Good - Lag compensation
function checkHit(shooterId: string, targetId: string, shotTime: number) {
  const lag = getPlayerLatency(shooterId)
  const rewindTime = shotTime - lag
  const targetPos = getPlayerPositionAtTime(targetId, rewindTime)
  return distance(shotPosition, targetPos) < HIT_RADIUS
}
```

---

## Integration Points

- **Matchmaking** (`38-gaming-features/matchmaking/`) - Player matching
- **WebSocket Patterns** (`34-real-time-features/websocket-patterns/`) - WebSocket implementation
- **Game Analytics** (`38-gaming-features/game-analytics/`) - Game metrics

---

## Further Reading

- [Real-time Multiplayer Networking](https://www.gabrielgambetta.com/client-server-game-architecture.html)
- [Client-Side Prediction](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking)

## Best Practices

1. **Client Prediction** - Predict locally for responsiveness
2. **Server Authority** - Server is authoritative
3. **Reconciliation** - Correct client predictions
4. **Lag Compensation** - Rewind for hit detection
5. **Fixed Timestep** - Use fixed timestep for physics
6. **Delta Compression** - Send only changes
7. **Interpolation** - Smooth remote player movement
8. **Anti-cheat** - Validate all actions server-side
9. **Bandwidth** - Optimize network usage
10. **Testing** - Test with various latencies

## Resources

- [Colyseus](https://colyseus.io/)
- [Fast-Paced Multiplayer](https://www.gabrielgambetta.com/client-server-game-architecture.html)
- [Source Multiplayer Networking](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking)
- [Networked Physics](https://gafferongames.com/post/networked_physics_2004/)
