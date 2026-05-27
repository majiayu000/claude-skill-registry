---
name: dev-multiplayer-prediction-movement
description: Movement prediction with server reconciliation for WASD controls. Use when implementing player movement.
category: multiplayer
---

# Movement Prediction

WASD movement with client-side prediction and server reconciliation.

## When to Use

Use when implementing player movement in multiplayer games:
- FPS/TPS character movement
- WASD movement schemes
- Platformer movement
- Vehicle controls

## Client Implementation

```typescript
import { useRef, useEffect } from '@react-three/fiber';
import { useNetworkManager } from '../../services/NetworkManager';

interface PendingInput {
  input: PlayerInput;
  sequence: number;
  timestamp: number;
}

export function PlayerController() {
  const networkManager = useNetworkManager();
  const meshRef = useRef<RapierRigidBody>(null);

  // Prediction state
  const localStateRef = useRef({
    position: { x: 0, y: 0, z: 0 },
    velocity: { x: 0, y: 0, z: 0 },
  });

  const pendingInputsRef = useRef<PendingInput[]>([]);
  const inputSequenceRef = useRef(0);

  // Server state (for reconciliation)
  const serverStateRef = useRef({
    position: { x: 0, y: 0, z: 0 },
    lastProcessedSequence: 0,
  });

  // Listen for server state updates
  useEffect(() => {
    const unsubscribe = networkManager.onStateChange((serverState) => {
      const localPlayer = serverState.players.get(networkManager.sessionId);
      if (localPlayer) {
        reconcileWithServer(localPlayer);
      }
    });
    return unsubscribe;
  }, [networkManager]);

  // Reconcile local prediction with server state
  function reconcileWithServer(serverPlayer: any) {
    const serverState = serverStateRef.current;
    const localState = localStateRef.current;

    // Remove inputs that server has processed
    pendingInputsRef.current = pendingInputsRef.current.filter(
      p => p.sequence > serverPlayer.lastProcessedSequence
    );

    // Start from server position (authoritative)
    let reconciledPosition = { ...serverPlayer.position };

    // Re-apply all pending inputs
    for (const pending of pendingInputsRef.current) {
      reconciledPosition = applyInput(
        reconciledPosition,
        pending.input,
        0.016 // Assume ~60fps for prediction
      );
    }

    // Smoothly interpolate display to reconciled position
    const smoothingFactor = 0.3;
    localState.position.x = lerp(
      localState.position.x,
      reconciledPosition.x,
      smoothingFactor
    );
    localState.position.y = lerp(
      localState.position.y,
      reconciledPosition.y,
      smoothingFactor
    );
    localState.position.z = lerp(
      localState.position.z,
      reconciledPosition.z,
      smoothingFactor
    );
  }

  // Apply input to position (local prediction)
  function applyInput(position: Vector3, input: PlayerInput, dt: number): Vector3 {
    const speed = MOVEMENT_CONFIG.walkSpeed;
    const result = { ...position };

    if (input.forward) result.z -= speed * dt;
    if (input.backward) result.z += speed * dt;
    if (input.left) result.x -= speed * dt;
    if (input.right) result.x += speed * dt;

    return result;
  }

  // Handle input frame update
  useFrame((state, dt) => {
    const input = getCurrentInput();

    if (hasInput(input)) {
      // 1. Store for prediction
      const sequence = ++inputSequenceRef.current;
      pendingInputsRef.current.push({
        input,
        sequence,
        timestamp: Date.now(),
      });

      // 2. Apply locally (immediate feedback)
      const predictedPosition = applyInput(
        localStateRef.current.position,
        input,
        dt
      );
      localStateRef.current.position = predictedPosition;

      // Update display immediately
      if (meshRef.current) {
        meshRef.current.setTranslation(predictedPosition);
      }

      // 3. Send to server (for validation)
      networkManager.send({
        type: 'player_input',
        input,
        sequence,
      });
    }
  });

  return (
    <RigidBody ref={meshRef} colliders="ball" type="kinematicPosition">
      <mesh>
        <sphereGeometry args={[0.5]} />
        <meshStandardMaterial color="orange" />
      </mesh>
    </RigidBody>
  );
}
```

## Server Implementation

```typescript
import { Room, Client } from "colyseus";
import { Schema, type, MapSchema } from "@colyseus/schema";

class PlayerState extends Schema {
  @type("number") x = 0;
  @type("number") y = 0;
  @type("number") z = 0;
  @type("number") rotation = 0;
  @type("number") lastProcessedSequence = 0; // For reconciliation
}

export class GameRoom extends Room<GameRoomState> {
  private inputBuffers: Map<string, PlayerInput[]> = new Map();

  onCreate() {
    this.setState(new GameRoomState());
    this.setSimulationInterval((dt) => this.update(dt));
  }

  onJoin(client: Client) {
    const player = new PlayerState();
    player.x = 0;
    player.z = 0;
    this.state.players.set(client.sessionId, player);
    this.inputBuffers.set(client.sessionId, []);
  }

  onMessage(client: Client, data: any) {
    if (data.type === 'player_input') {
      const player = this.state.players.get(client.sessionId);
      if (!player) return;

      // Store input with sequence number
      this.inputBuffers.get(client.sessionId)?.push({
        ...data.input,
        sequence: data.sequence,
      });

      // Track last processed sequence for reconciliation
      player.lastProcessedSequence = data.sequence;
    }
  }

  update(dt: number) {
    const deltaTime = dt / 1000;

    for (const [sessionId, player] of this.state.players) {
      const inputs = this.inputBuffers.get(sessionId) || [];

      // Process all pending inputs
      for (const input of inputs) {
        this.processPlayerInput(player, input, deltaTime);
      }

      // Clear processed inputs
      this.inputBuffers.set(sessionId, []);
    }
  }

  processPlayerInput(player: PlayerState, input: PlayerInput, dt: number) {
    const speed = MOVEMENT_CONFIG.walkSpeed; // Must match client!

    // Apply movement SERVER-SIDE
    if (input.forward) player.z -= speed * dt;
    if (input.backward) player.z += speed * dt;
    if (input.left) player.x -= speed * dt;
    if (input.right) player.x += speed * dt;

    // Validate bounds (anti-cheat)
    player.x = Math.max(-50, Math.min(50, player.x));
    player.z = Math.max(-50, Math.min(50, player.z));

    // Server state automatically syncs to clients via Colyseus
  }
}
```

## Smoothing Function

```typescript
// Smooth correction without "snapping"
function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

function reconcilePosition(
  displayPosition: Vector3,
  serverPosition: Vector3,
  pendingInputs: PendingInput[]
): Vector3 {
  // Calculate reconciled position
  let reconciled = { ...serverPosition };

  for (const input of pendingInputs) {
    reconciled = applyInput(reconciled, input.input, 0.016);
  }

  // Smooth interpolation (not instant snap)
  const t = 0.2; // 20% correction per frame
  return {
    x: lerp(displayPosition.x, reconciled.x, t),
    y: lerp(displayPosition.y, reconciled.y, t),
    z: lerp(displayPosition.z, reconciled.z, t),
  };
}
```

## Diagonal Movement

```typescript
// Normalize diagonal input to prevent speed advantage
function normalizeInput(input: PlayerInput): PlayerInput {
  const forward = input.forward ? 1 : 0;
  const backward = input.backward ? 1 : 0;
  const left = input.left ? 1 : 0;
  const right = input.right ? 1 : 0;

  const horizontal = left - right;
  const vertical = forward - backward;

  const length = Math.sqrt(horizontal * horizontal + vertical * vertical);

  if (length > 1) {
    // Moving diagonally - normalize
    return {
      forward: input.forward,
      backward: input.backward,
      left: input.left,
      right: input.right,
      normalizedFactor: 1 / length,
    };
  }

  return input;
}
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Client/server speed mismatch | Use shared config |
| No diagonal normalization | Normalize diagonal input |
| Instant snap to server state | Smooth interpolation |
| Not re-applying pending inputs | Always re-apply after reconciliation |
| Fixed smoothing factor | Dynamic smoothing based on distance |

## Reference

- [prediction-basics.md](./prediction-basics.md) - Core concepts
- [prediction-shooting.md](./prediction-shooting.md) - Shooting with rollback
