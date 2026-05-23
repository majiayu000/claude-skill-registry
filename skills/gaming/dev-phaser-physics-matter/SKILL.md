---
name: dev-phaser-physics-matter
description: Matter.js physics: realistic bodies, constraints, and simulation
---

# Phaser Matter Physics

> "Realistic physics simulation for puzzles and complex interactions."

## Before/After: Manual Physics vs Matter.js Constraints

### ❌ Before: Manual Physics Simulation

```typescript
// Manual physics without proper engine
interface Body {
  x: number; y: number;
  vx: number; vy: number;
  mass: number;
  angle: number;
  angularVelocity: number;
}

const bodies: Body[] = [];

function updatePhysics(dt: number) {
  // Apply gravity
  for (const body of bodies) {
    body.vy += 9.8 * dt;
  }

  // Check collisions (O(n²) complexity)
  for (let i = 0; i < bodies.length; i++) {
    for (let j = i + 1; j < bodies.length; j++) {
      if (checkCollision(bodies[i], bodies[j])) {
        resolveCollision(bodies[i], bodies[j]);
      }
    }
  }

  // Update positions
  for (const body of bodies) {
    body.x += body.vx * dt;
    body.y += body.vy * dt;
    body.angle += body.angularVelocity * dt;
  }
}

// Problems:
// - O(n²) collision detection
// - No realistic stacking
// - No constraints/joints
// - Manual collision resolution
// - No rotational physics
```

### ✅ After: Phaser Matter Physics

```typescript
// Matter.js handles complex physics
export class GameScene extends Phaser.Scene {
  create() {
    // Enable Matter physics
    this.physics.world.setBounds(0, 0, 800, 600);

    // Create connected bodies with constraint
    const box1 = this.matter.add.image(300, 200, 'box');
    box1.setRectangle(40, 40);
    box1.setStatic(true);

    const box2 = this.matter.add.image(300, 300, 'box');
    box2.setRectangle(40, 40);

    // Create chain constraint (rope-like) - ONE line!
    this.matter.add.constraint(box1, box2, 100, 0.9, {
      render: { visible: true }
    });

    // Add spring constraint
    const springBox = this.matter.add.image(500, 200, 'box');
    this.matter.add.spring(
      { x: 500, y: 100 },
      springBox,
      100,
      0.001,
      { damping: 0.05 }
    );
  }
}

// Benefits:
// - Efficient SAT collision detection
// - Realistic stacking behavior
// - Built-in constraints (chains, springs, hinges)
// - Rotational physics included
// - Sleep optimization for performance
```

## When to Use This Skill

Use when:

- Building physics puzzle games
- Need realistic collision and physics
- Working with complex body shapes
- Using constraints and joints
- Simulating realistic object interactions

## Quick Start

```typescript
// Enable Matter physics in game config
physics: {
  default: 'matter',
  matter: {
    gravity: { y: 1 },
    debug: false
  }
}

// Create Matter sprite
const box = this.matter.add.image(400, 300, 'box');
box.setRectangle();
```

## Decision Framework

| Need               | Use                  |
| ------------------ | -------------------- |
| Physics puzzles    | Matter physics       |
| Realistic stacking | Matter with friction |
| Ropes/chains       | Constraints          |
| Complex shapes     | Custom body vertices |
| Simple platformer  | Arcade instead       |

## Progressive Guide

### Level 1: Basic Matter Bodies

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Create image as Matter body
    const box = this.matter.add.image(400, 100, "box");
    box.setRectangle(); // Default: use texture size
    box.setBounce(0.5);
    box.setFriction(0.1);

    // Circle body
    const ball = this.matter.add.image(400, 200, "ball");
    ball.setCircle();
    ball.setBounce(0.8);

    // Static ground
    const ground = this.matter.add.image(400, 550, "ground");
    ground.setStatic(true);
    ground.setRectangle(800, 50);
  }
}
```

### Level 2: Custom Body Shapes

```typescript
create() {
  // Triangle body
  const triangle = this.matter.add.image(400, 100, 'triangle');
  triangle.setPolygon(0, 0, [
    { x: 0, y: -30 },
    { x: 30, y: 30 },
    { x: -30, y: 30 }
  ]);

  // Custom shape from vertices
  const rock = this.matter.add.image(400, 200, 'rock');
  rock.setPolygon(0, 0, [
    { x: -25, y: -20 },
    { x: 20, y: -25 },
    { x: 30, y: 10 },
    { x: 10, y: 30 },
    { x: -20, y: 25 }
  ]);

  // Compound body (multiple shapes)
  const compound = this.matter.add.image(400, 300, 'crate');
  compound.setRectangle(40, 40);
  compound.setBounce(0.2);
  compound.setFriction(0.5);
}
```

### Level 3: Constraints and Joints

```typescript
create() {
  const box1 = this.matter.add.image(300, 200, 'box');
  box1.setRectangle(40, 40);
  box1.setStatic(true);

  const box2 = this.matter.add.image(300, 300, 'box');
  box2.setRectangle(40, 40);

  // Create chain constraint (rope-like)
  this.matter.add.constraint(box1, box2, 100, 0.9, {
    render: { visible: true }
  });

  // Create hinge constraint
  const door = this.matter.add.image(400, 300, 'door');
  door.setRectangle(10, 100);
  this.matter.add.constraint(door, { x: 400, y: 250 }, 50, 1, {
    pointA: { x: 0, y: -50 },
    pointB: { x: 0, y: 0 }
  });

  // Spring constraint
  const springBox = this.matter.add.image(500, 200, 'box');
  springBox.setRectangle(40, 40);

  this.matter.add.spring(
    { x: 500, y: 100 },
    springBox,
    100,
    0.001,
    { damping: 0.05 }
  );
}
```

### Level 4: Physics Events and Collision

```typescript
create() {
  // Collision event
  this.matter.world.on('collisionstart', (event: any) => {
    event.pairs.forEach((pair: any) => {
      const bodyA = pair.bodyA;
      const bodyB = pair.bodyB;

      if (bodyA.label === 'player' && bodyB.label === 'coin') {
        this.collectCoin(bodyB.gameObject);
      }
    });
  });

  // Create labeled bodies
  const player = this.matter.add.image(400, 300, 'player');
  player.setRectangle();
  (player.body as MatterJS.Body).label = 'player';

  const coin = this.matter.add.image(400, 400, 'coin');
  coin.setCircle();
  (coin.body as MatterJS.Body).label = 'coin';
}
```

### Level 5: Advanced Matter Physics

```typescript
export class PhysicsScene extends Phaser.Scene {
  private bridgeParts: Phaser.Physics.Matter.Image[] = [];

  create() {
    this.createBridge();
    this.createRope();
    this.createPhysicsStack();
  }

  createBridge() {
    const startX = 200;
    const startY = 200;
    const plankCount = 8;
    const plankWidth = 60;
    const gap = 5;

    let previousPlank: Phaser.Physics.Matter.Image | null = null;

    for (let i = 0; i < plankCount; i++) {
      const x = startX + i * (plankWidth + gap);
      const y = startY;

      const plank = this.matter.add.image(x, y, "plank");
      plank.setRectangle(plankWidth, 20);
      plank.setBounce(0);
      plank.setFriction(0.8);

      this.bridgeParts.push(plank);

      if (i === 0 || i === plankCount - 1) {
        plank.setStatic(true);
      }

      if (previousPlank) {
        this.matter.add.constraint(
          previousPlank,
          plank,
          plankWidth + gap,
          0.9,
          {
            pointA: { x: plankWidth / 2, y: 0 },
            pointB: { x: -plankWidth / 2, y: 0 },
          },
        );
      }

      previousPlank = plank;
    }
  }

  createRope() {
    const links = 10;
    const linkLength = 20;
    const startX = 600;
    const startY = 100;

    let prevLink: Phaser.Physics.Matter.Image | null = null;

    for (let i = 0; i < links; i++) {
      const link = this.matter.add.circle(startX, startY + i * linkLength, 5);
      link.setBounce(0);
      link.setFriction(0.5);

      if (i === 0) {
        link.setStatic(true);
      }

      if (prevLink) {
        this.matter.add.constraint(prevLink, link, linkLength, 0.9);
      }

      prevLink = link;
    }
  }

  createPhysicsStack() {
    const stackSize = 5;
    const boxSize = 40;
    const startX = 500;
    const startY = 500;

    for (let row = 0; row < stackSize; row++) {
      for (let col = 0; col < stackSize - row; col++) {
        const x = startX + col * boxSize + row * (boxSize / 2);
        const y = startY - row * boxSize;

        const box = this.matter.add.image(x, y, "box");
        box.setRectangle(boxSize, boxSize);
        box.setBounce(0.1);
        box.setFriction(0.5);
        box.setDensity(0.001);
      }
    }
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Use Matter for simple platformers - Arcade is better
- Set high density on all objects - causes instability
- Ignore sleep settings - kills performance
- Create complex constraints without tuning
- Mix body coordinates systems arbitrarily
- Forget to set static on anchored objects

✅ **DO:**

- Use Matter for puzzles, stacking, complex interactions
- Adjust density based on object type
- Enable sleep for inactive bodies
- Test constraint values iteratively
- Keep coordinates consistent
- Set static bodies for anchors/ground

## Code Patterns

### Body Configuration

```typescript
const box = this.matter.add.image(400, 300, "box");

// Shape
box.setRectangle(width, height);
box.setCircle(radius);
box.setPolygon(x, y, vertices);
box.setTrapezoid(width, height, slope);

// Physics properties
box.setBounce(0.5); // Restitution
box.setFriction(0.1); // Surface friction
box.setFrictionStatic(0.5); // Static friction
box.setDensity(0.001); // Mass = density * area
box.setAngle(Math.PI / 4); // Rotation in radians

// State
box.setStatic(true); // Immovable
box.setSensor(true); // Detect but don't collide
```

### Constraint Types

```typescript
// Chain constraint (rigid-ish connection)
this.matter.add.constraint(bodyA, bodyB, length, stiffness);

// Spring constraint
this.matter.add.spring(bodyA, bodyB, length, stiffness, config);

// World constraint (anchor to point)
this.matter.add.constraint(body, { x, y }, length, stiffness);

// Hinge (rotational joint)
this.matter.add.constraint(bodyA, bodyB, length, stiffness, {
  pointA: { x: offsetX, y: offsetY },
  pointB: { x: offsetX, y: offsetY },
});
```

## Matter vs Arcade Comparison

| Feature     | Arcade                | Matter                     |
| ----------- | --------------------- | -------------------------- |
| Performance | Faster                | Slower                     |
| Complexity  | Simple                | Complex                    |
| Collision   | AABB/OBB              | SAT/Polygon                |
| Constraints | Basic                 | Advanced                   |
| Best For    | Platformers, top-down | Puzzles, realistic physics |
| Body Types  | Dynamic/Static        | Dynamic/Static/Sensor      |

## Checklist

- [ ] Matter physics enabled in config
- [ ] Bodies properly shaped
- [ ] Static bodies marked as static
- [ ] Constraints tuned properly
- [ ] Collision labels set for events
- [ ] Density/bounce/friction configured
- [ ] Sleep enabled for performance

## Reference

- [Matter.js Docs](https://brm.io/matter-js-docs/) — Underlying physics engine
- [Phaser Matter Docs](https://photonstorm.github.io/phaser3-docs/Phaser.Physics.Matter.MatterPhysics.html) — Phaser integration
