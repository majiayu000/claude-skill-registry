---
name: game-loop
description: Fixed timestep game loop with interpolation for frame-rate independent physics. Separates physics updates from rendering, prevents spiral of death, and supports hitstop/slow-mo effects.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: frontend
  time: 4h
  source: drift-masterguide
---

# Fixed Timestep Game Loop

Frame-rate independent game loop with physics interpolation and time manipulation.

## When to Use This Skill

- Building browser-based games or interactive simulations
- Need consistent physics regardless of monitor refresh rate
- Want smooth rendering with deterministic game logic
- Implementing hitstop, slow-mo, or time manipulation effects

## Core Concepts

The key insight is separating physics (fixed timestep) from rendering (variable). An accumulator tracks time debt, running physics at a consistent rate while interpolating between states for smooth visuals.

```
Frame → Accumulator += delta → While(accumulator >= fixedStep) { physics() } → Render(interpolation)
```

## Implementation

### TypeScript

```typescript
interface GameLoopStats {
  fps: number;
  frameTime: number;
  physicsTime: number;
  renderTime: number;
  lagSpikes: number;
  interpolation: number;
  timeScale: number;
  isInHitstop: boolean;
}

interface GameLoopCallbacks {
  onFixedUpdate: (fixedDelta: number, now: number) => void;
  onRenderUpdate: (delta: number, interpolation: number, now: number) => void;
  onLagSpike?: (missedFrames: number) => void;
}

class GameLoop {
  private fixedTimestep: number;
  private readonly MAX_FRAME_TIME = 0.25;
  
  private accumulator = 0;
  private lastTime = 0;
  private interpolation = 0;
  
  private frameCount = 0;
  private fpsTimer = 0;
  private currentFps = 60;
  private lagSpikes = 0;
  
  private running = false;
  private animationId: number | null = null;
  private callbacks: GameLoopCallbacks;
  
  private hitstopTimer = 0;
  private hitstopIntensity = 0;
  private externalTimeScale = 1.0;

  constructor(callbacks: GameLoopCallbacks, fixedTimestep = 1 / 60) {
    this.callbacks = callbacks;
    this.fixedTimestep = fixedTimestep;
  }

  start(): void {
    if (this.running) return;
    this.running = true;
    this.lastTime = performance.now() / 1000;
    this.accumulator = 0;
    this.loop();
  }

  stop(): void {
    this.running = false;
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  triggerHitstop(frames = 3, intensity = 0.1): void {
    this.hitstopTimer = frames * this.fixedTimestep;
    this.hitstopIntensity = intensity;
  }

  setTimeScale(scale: number): void {
    this.externalTimeScale = Math.max(0, scale);
  }

  getStats(): GameLoopStats {
    return {
      fps: this.currentFps,
      frameTime: 0,
      physicsTime: 0,
      renderTime: 0,
      lagSpikes: this.lagSpikes,
      interpolation: this.interpolation,
      timeScale: this.getEffectiveTimeScale(),
      isInHitstop: this.hitstopTimer > 0,
    };
  }

  private loop = (): void => {
    if (!this.running) return;

    const now = performance.now() / 1000;
    let frameTime = now - this.lastTime;
    this.lastTime = now;

    // Cap frame time to prevent spiral of death
    if (frameTime > this.MAX_FRAME_TIME) {
      const missedFrames = Math.floor(frameTime / this.fixedTimestep);
      this.lagSpikes++;
      this.callbacks.onLagSpike?.(missedFrames);
      frameTime = this.MAX_FRAME_TIME;
    }

    frameTime *= this.getEffectiveTimeScale();

    if (this.hitstopTimer > 0) {
      this.hitstopTimer -= frameTime / this.getEffectiveTimeScale();
    }

    this.accumulator += frameTime;

    // Fixed timestep physics
    while (this.accumulator >= this.fixedTimestep) {
      this.callbacks.onFixedUpdate(this.fixedTimestep, now);
      this.accumulator -= this.fixedTimestep;
    }

    // Interpolation for smooth rendering
    this.interpolation = this.accumulator / this.fixedTimestep;
    this.callbacks.onRenderUpdate(frameTime, this.interpolation, now);

    // FPS calculation
    this.frameCount++;
    this.fpsTimer += frameTime / this.getEffectiveTimeScale();
    if (this.fpsTimer >= 1.0) {
      this.currentFps = Math.round(this.frameCount / this.fpsTimer);
      this.frameCount = 0;
      this.fpsTimer = 0;
    }

    this.animationId = requestAnimationFrame(this.loop);
  };

  private getEffectiveTimeScale(): number {
    return this.hitstopTimer > 0 ? this.hitstopIntensity : this.externalTimeScale;
  }
}

// Interpolation helpers
function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

function lerpAngle(a: number, b: number, t: number): number {
  let diff = b - a;
  while (diff > Math.PI) diff -= Math.PI * 2;
  while (diff < -Math.PI) diff += Math.PI * 2;
  return a + diff * t;
}
```

## Usage Examples

```typescript
// Game state
let playerX = 0, playerY = 0;
let playerVelX = 0, playerVelY = 0;
let prevPlayerX = 0, prevPlayerY = 0;

const gameLoop = new GameLoop({
  onFixedUpdate: (fixedDelta) => {
    // Store previous for interpolation
    prevPlayerX = playerX;
    prevPlayerY = playerY;

    // Deterministic physics
    playerVelY += 980 * fixedDelta; // Gravity
    playerX += playerVelX * fixedDelta;
    playerY += playerVelY * fixedDelta;

    // Collision
    if (playerY > 500) {
      playerY = 500;
      playerVelY = 0;
    }
  },

  onRenderUpdate: (delta, interpolation) => {
    // Smooth rendering between physics states
    const renderX = lerp(prevPlayerX, playerX, interpolation);
    const renderY = lerp(prevPlayerY, playerY, interpolation);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillRect(renderX - 10, renderY - 10, 20, 20);
  },

  onLagSpike: (missed) => console.warn(`Lag: missed ${missed} frames`),
});

gameLoop.start();

// Hitstop on collision
function onPlayerHit() {
  gameLoop.triggerHitstop(4, 0.05); // 4 frames at 5% speed
}

// Slow-mo death
function onPlayerDeath() {
  gameLoop.setTimeScale(0.3);
  setTimeout(() => gameLoop.setTimeScale(1.0), 2000);
}
```

## Best Practices

1. Always store previous state before physics update for interpolation
2. Cap frame time to prevent spiral of death (0.25s is reasonable)
3. Use fixed timestep for all game logic, variable only for rendering
4. Tune hitstop values for game feel (2-5 frames typical)
5. Consider 30Hz physics for mobile to save CPU

## Common Mistakes

- Running physics in render callback (frame-rate dependent)
- Not interpolating positions (causes stuttering)
- Forgetting to cap frame time (causes spiral of death on tab switch)
- Using delta time for physics (non-deterministic)

## Related Patterns

- server-tick (server-side equivalent)
- websocket-management (multiplayer sync)
