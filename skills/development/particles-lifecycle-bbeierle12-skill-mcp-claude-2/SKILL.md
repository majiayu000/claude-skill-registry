---
name: particles-lifecycle
description: Particle lifecycle management—emission/spawning, death conditions, object pooling, trails, fade-in/out, and state transitions. Use when particles need birth/death cycles, continuous emission, trail effects, or memory-efficient recycling.
---

# Particle Lifecycle

Manage particle birth, life, death, and rebirth for continuous effects.

## Quick Start

```tsx
interface Particle {
  position: THREE.Vector3;
  velocity: THREE.Vector3;
  life: number;      // Current life (decrements)
  maxLife: number;   // Starting life
  alive: boolean;
}

// Update loop
for (const p of particles) {
  if (!p.alive) continue;
  
  p.life -= delta;
  if (p.life <= 0) {
    p.alive = false;
    continue;
  }
  
  // Age factor (0 at birth, 1 at death)
  const age = 1 - p.life / p.maxLife;
  
  // Update position, apply fade, etc.
}
```

## Emission Patterns

### Continuous Emission

```tsx
class ContinuousEmitter {
  private accumulator = 0;
  
  emit(
    particles: Particle[],
    rate: number,      // Particles per second
    delta: number,
    spawnFn: () => Particle
  ) {
    this.accumulator += rate * delta;
    
    while (this.accumulator >= 1) {
      this.accumulator -= 1;
      
      // Find dead particle to reuse
      const dead = particles.find(p => !p.alive);
      if (dead) {
        Object.assign(dead, spawnFn());
        dead.alive = true;
      }
    }
  }
}

// Usage
const emitter = new ContinuousEmitter();

useFrame((_, delta) => {
  emitter.emit(particles, 100, delta, () => ({
    position: new THREE.Vector3(0, 0, 0),
    velocity: new THREE.Vector3(
      (Math.random() - 0.5) * 2,
      Math.random() * 5,
      (Math.random() - 0.5) * 2
    ),
    life: 2 + Math.random(),
    maxLife: 2 + Math.random(),
    alive: true
  }));
});
```

### Burst Emission

```tsx
function emitBurst(
  particles: Particle[],
  count: number,
  origin: THREE.Vector3,
  speed: number,
  lifeRange: [number, number]
) {
  let emitted = 0;
  
  for (const p of particles) {
    if (emitted >= count) break;
    if (p.alive) continue;
    
    // Random direction on sphere
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    
    const dir = new THREE.Vector3(
      Math.sin(phi) * Math.cos(theta),
      Math.sin(phi) * Math.sin(theta),
      Math.cos(phi)
    );
    
    p.position.copy(origin);
    p.velocity.copy(dir).multiplyScalar(speed * (0.5 + Math.random()));
    p.maxLife = lifeRange[0] + Math.random() * (lifeRange[1] - lifeRange[0]);
    p.life = p.maxLife;
    p.alive = true;
    
    emitted++;
  }
  
  return emitted;
}
```

### Shape Emission

```tsx
// Emit from sphere surface
function emitFromSphere(origin: THREE.Vector3, radius: number): THREE.Vector3 {
  const theta = Math.random() * Math.PI * 2;
  const phi = Math.acos(2 * Math.random() - 1);
  
  return new THREE.Vector3(
    origin.x + radius * Math.sin(phi) * Math.cos(theta),
    origin.y + radius * Math.sin(phi) * Math.sin(theta),
    origin.z + radius * Math.cos(phi)
  );
}

// Emit from box volume
function emitFromBox(min: THREE.Vector3, max: THREE.Vector3): THREE.Vector3 {
  return new THREE.Vector3(
    min.x + Math.random() * (max.x - min.x),
    min.y + Math.random() * (max.y - min.y),
    min.z + Math.random() * (max.z - min.z)
  );
}

// Emit from circle edge
function emitFromCircle(center: THREE.Vector3, radius: number, normal: THREE.Vector3): THREE.Vector3 {
  const angle = Math.random() * Math.PI * 2;
  
  // Create perpendicular vectors
  const up = Math.abs(normal.y) < 0.9 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(1, 0, 0);
  const right = new THREE.Vector3().crossVectors(normal, up).normalize();
  const forward = new THREE.Vector3().crossVectors(right, normal).normalize();
  
  return new THREE.Vector3()
    .addScaledVector(right, Math.cos(angle) * radius)
    .addScaledVector(forward, Math.sin(angle) * radius)
    .add(center);
}

// Emit from cone
function emitFromCone(origin: THREE.Vector3, direction: THREE.Vector3, angle: number, speed: number): THREE.Vector3 {
  const coneAngle = Math.random() * angle;
  const rotation = Math.random() * Math.PI * 2;
  
  const velocity = direction.clone().normalize();
  
  // Rotate around perpendicular axis
  const perpendicular = new THREE.Vector3(1, 0, 0);
  if (Math.abs(direction.x) > 0.9) perpendicular.set(0, 1, 0);
  perpendicular.cross(direction).normalize();
  
  velocity.applyAxisAngle(perpendicular, coneAngle);
  velocity.applyAxisAngle(direction, rotation);
  
  return velocity.multiplyScalar(speed);
}
```

## Object Pooling

Pre-allocate particles to avoid garbage collection:

```tsx
class ParticlePool {
  private particles: Particle[] = [];
  private activeCount = 0;
  
  constructor(maxCount: number) {
    for (let i = 0; i < maxCount; i++) {
      this.particles.push({
        position: new THREE.Vector3(),
        velocity: new THREE.Vector3(),
        life: 0,
        maxLife: 0,
        alive: false
      });
    }
  }
  
  spawn(): Particle | null {
    for (const p of this.particles) {
      if (!p.alive) {
        p.alive = true;
        this.activeCount++;
        return p;
      }
    }
    return null;  // Pool exhausted
  }
  
  kill(particle: Particle) {
    particle.alive = false;
    this.activeCount--;
  }
  
  update(delta: number, updateFn: (p: Particle, age: number) => void) {
    for (const p of this.particles) {
      if (!p.alive) continue;
      
      p.life -= delta;
      
      if (p.life <= 0) {
        this.kill(p);
        continue;
      }
      
      const age = 1 - p.life / p.maxLife;
      updateFn(p, age);
    }
  }
  
  forEach(fn: (p: Particle) => void) {
    for (const p of this.particles) {
      if (p.alive) fn(p);
    }
  }
  
  get active() { return this.activeCount; }
  get capacity() { return this.particles.length; }
}
```

### GPU Pool (Buffer-Based)

```tsx
class GPUParticlePool {
  positions: Float32Array;
  velocities: Float32Array;
  lives: Float32Array;
  maxLives: Float32Array;
  
  private freeIndices: number[] = [];
  
  constructor(public count: number) {
    this.positions = new Float32Array(count * 3);
    this.velocities = new Float32Array(count * 3);
    this.lives = new Float32Array(count);
    this.maxLives = new Float32Array(count);
    
    // All indices start free
    for (let i = count - 1; i >= 0; i--) {
      this.freeIndices.push(i);
    }
  }
  
  spawn(): number {
    const index = this.freeIndices.pop();
    return index ?? -1;
  }
  
  kill(index: number) {
    this.lives[index] = 0;
    this.freeIndices.push(index);
  }
  
  setParticle(index: number, pos: THREE.Vector3, vel: THREE.Vector3, life: number) {
    this.positions[index * 3] = pos.x;
    this.positions[index * 3 + 1] = pos.y;
    this.positions[index * 3 + 2] = pos.z;
    
    this.velocities[index * 3] = vel.x;
    this.velocities[index * 3 + 1] = vel.y;
    this.velocities[index * 3 + 2] = vel.z;
    
    this.lives[index] = life;
    this.maxLives[index] = life;
  }
  
  update(delta: number) {
    for (let i = 0; i < this.count; i++) {
      if (this.lives[i] <= 0) continue;
      
      this.lives[i] -= delta;
      
      if (this.lives[i] <= 0) {
        this.freeIndices.push(i);
        continue;
      }
      
      // Update position
      this.positions[i * 3] += this.velocities[i * 3] * delta;
      this.positions[i * 3 + 1] += this.velocities[i * 3 + 1] * delta;
      this.positions[i * 3 + 2] += this.velocities[i * 3 + 2] * delta;
    }
  }
}
```

## Fade Patterns

### Linear Fade

```tsx
// age: 0 (birth) to 1 (death)
const alpha = 1 - age;
```

### Fade In/Out

```tsx
function fadeInOut(age: number, fadeInDuration = 0.1, fadeOutStart = 0.7): number {
  if (age < fadeInDuration) {
    return age / fadeInDuration;  // Fade in
  } else if (age > fadeOutStart) {
    return 1 - (age - fadeOutStart) / (1 - fadeOutStart);  // Fade out
  }
  return 1;  // Full opacity
}
```

### Eased Fade

```tsx
// Smooth fade out (ease-in)
const alpha = Math.pow(1 - age, 2);

// Quick fade then slow (ease-out)
const alpha = 1 - Math.pow(age, 2);

// S-curve (smoothstep)
const alpha = 1 - (age * age * (3 - 2 * age));
```

### Blink/Flash

```tsx
function blink(age: number, frequency: number): number {
  return (Math.sin(age * frequency * Math.PI * 2) + 1) * 0.5;
}
```

## Size Over Life

```tsx
// Grow then shrink
function sizeOverLife(age: number, maxSize: number): number {
  // Peak at 20% of life
  const peak = 0.2;
  if (age < peak) {
    return (age / peak) * maxSize;
  } else {
    return (1 - (age - peak) / (1 - peak)) * maxSize;
  }
}

// Pop in, slow shrink
function popShrink(age: number, maxSize: number): number {
  const popDuration = 0.05;
  if (age < popDuration) {
    return maxSize;  // Instant full size
  }
  return maxSize * (1 - (age - popDuration) / (1 - popDuration));
}
```

## Color Over Life

```tsx
// Gradient from start to end color
function colorOverLife(age: number, startColor: THREE.Color, endColor: THREE.Color): THREE.Color {
  return startColor.clone().lerp(endColor, age);
}

// Multi-stop gradient
function colorGradient(age: number, stops: Array<{ pos: number; color: THREE.Color }>): THREE.Color {
  // Find surrounding stops
  let lower = stops[0];
  let upper = stops[stops.length - 1];
  
  for (let i = 0; i < stops.length - 1; i++) {
    if (age >= stops[i].pos && age <= stops[i + 1].pos) {
      lower = stops[i];
      upper = stops[i + 1];
      break;
    }
  }
  
  const t = (age - lower.pos) / (upper.pos - lower.pos);
  return lower.color.clone().lerp(upper.color, t);
}

// Usage
const fireGradient = [
  { pos: 0, color: new THREE.Color('#ffffff') },
  { pos: 0.2, color: new THREE.Color('#ffff00') },
  { pos: 0.5, color: new THREE.Color('#ff6600') },
  { pos: 1, color: new THREE.Color('#330000') }
];
```

## Trails

### Position History Trail

```tsx
class TrailParticle {
  positions: THREE.Vector3[] = [];
  maxLength: number;
  
  constructor(maxLength: number) {
    this.maxLength = maxLength;
  }
  
  update(newPosition: THREE.Vector3) {
    this.positions.unshift(newPosition.clone());
    
    if (this.positions.length > this.maxLength) {
      this.positions.pop();
    }
  }
  
  getTrailGeometry(): THREE.BufferGeometry {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(this.positions.length * 3);
    const alphas = new Float32Array(this.positions.length);
    
    for (let i = 0; i < this.positions.length; i++) {
      positions[i * 3] = this.positions[i].x;
      positions[i * 3 + 1] = this.positions[i].y;
      positions[i * 3 + 2] = this.positions[i].z;
      
      alphas[i] = 1 - i / this.positions.length;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('alpha', new THREE.BufferAttribute(alphas, 1));
    
    return geometry;
  }
}
```

### GPU Trail (Shader-Based)

```glsl
// Vertex shader with trail
attribute float aTrailIndex;  // 0 = head, 1 = tail
attribute vec3 aPrevPosition;
attribute vec3 aNextPosition;

uniform float uTrailLength;

varying float vTrailAlpha;

void main() {
  // Interpolate between positions based on trail index
  vec3 pos = mix(aNextPosition, aPrevPosition, aTrailIndex);
  
  // Alpha fades along trail
  vTrailAlpha = 1.0 - aTrailIndex;
  
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  gl_PointSize = mix(10.0, 2.0, aTrailIndex);  // Size decreases along trail
}
```

### Line Trail

```tsx
function TrailLine({ points, color = '#ffffff' }) {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    const positions = new Float32Array(points.length * 3);
    
    points.forEach((p, i) => {
      positions[i * 3] = p.x;
      positions[i * 3 + 1] = p.y;
      positions[i * 3 + 2] = p.z;
    });
    
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    return geo;
  }, [points]);
  
  return (
    <line geometry={geometry}>
      <lineBasicMaterial color={color} transparent opacity={0.5} />
    </line>
  );
}
```

## State Machines

```tsx
enum ParticleState {
  Spawning,
  Active,
  Dying,
  Dead
}

interface StatefulParticle extends Particle {
  state: ParticleState;
  stateTime: number;
}

function updateParticleState(p: StatefulParticle, delta: number) {
  p.stateTime += delta;
  
  switch (p.state) {
    case ParticleState.Spawning:
      // Fade in over 0.2 seconds
      if (p.stateTime >= 0.2) {
        p.state = ParticleState.Active;
        p.stateTime = 0;
      }
      break;
      
    case ParticleState.Active:
      p.life -= delta;
      if (p.life <= 0.5) {  // Start dying when 0.5s left
        p.state = ParticleState.Dying;
        p.stateTime = 0;
      }
      break;
      
    case ParticleState.Dying:
      p.life -= delta;
      if (p.life <= 0) {
        p.state = ParticleState.Dead;
        p.alive = false;
      }
      break;
  }
}

function getParticleAlpha(p: StatefulParticle): number {
  switch (p.state) {
    case ParticleState.Spawning:
      return p.stateTime / 0.2;
    case ParticleState.Active:
      return 1;
    case ParticleState.Dying:
      return p.life / 0.5;
    default:
      return 0;
  }
}
```

## Sub-Emitters

Spawn particles from dying particles:

```tsx
function updateWithSubEmitter(
  particles: Particle[],
  subEmitCount: number,
  subEmitFn: (parent: Particle) => Particle
) {
  const toEmit: Particle[] = [];
  
  for (const p of particles) {
    if (!p.alive) continue;
    
    p.life -= delta;
    
    if (p.life <= 0) {
      p.alive = false;
      
      // Spawn sub-particles
      for (let i = 0; i < subEmitCount; i++) {
        toEmit.push(subEmitFn(p));
      }
    }
  }
  
  // Add sub-particles to pool
  for (const sub of toEmit) {
    const dead = particles.find(p => !p.alive);
    if (dead) {
      Object.assign(dead, sub);
    }
  }
}
```

## File Structure

```
particles-lifecycle/
├── SKILL.md
├── references/
│   ├── emission-patterns.md   # All emission shapes
│   └── easing-curves.md       # Fade/size curves
└── scripts/
    ├── emitters/
    │   ├── continuous.ts      # Continuous emission
    │   ├── burst.ts           # Burst emission
    │   └── shapes.ts          # Shape emitters
    ├── pool.ts                # Object pooling
    ├── trails.ts              # Trail implementations
    └── lifecycle.ts           # Fade, size, color curves
```

## Reference

- `references/emission-patterns.md` — All emission shape functions
- `references/easing-curves.md` — Fade and size curve options
