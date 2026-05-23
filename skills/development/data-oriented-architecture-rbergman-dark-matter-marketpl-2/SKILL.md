---
name: data-oriented-architecture
description: "Apply data-oriented architecture patterns when designing systems with polymorphic entities. This skill should be used PROACTIVELY when encountering switch statements or if/else chains that dispatch based on entity type, when designing new entity systems, or when refactoring toward extensibility. Provides registry-based dispatch, capability composition, and infrastructure-first development patterns. Complements solid-architecture with concrete implementation strategies."
---

# Data-Oriented Architecture Patterns

## When To Use This Skill

Activate this skill when:
- Encountering switch statements or if/else chains dispatching on entity/object type
- Designing systems with multiple variants of similar entities
- Refactoring code where adding new types requires changes in multiple locations
- Building plugin systems, handler registries, or factory patterns
- Noticing the "expression problem" (hard to add new types AND new operations)

## Core Principle

**Separate data from behavior, dispatch via registry.**

```
Entity = Pure Data (what it IS) + type discriminator
Definition = Bundled Behavior (what it DOES)
Registry = Type → Definition mapping (HOW to dispatch)
```

## Pattern 1: Registry-Based Polymorphism

### Problem
Switch statements scattered throughout codebase:

```
// Scattered in rendering.ts
switch (entity.type) {
  case 'typeA': renderA(entity); break;
  case 'typeB': renderB(entity); break;
}

// Scattered in update.ts
switch (entity.type) {
  case 'typeA': updateA(entity); break;
  case 'typeB': updateB(entity); break;
}

// Adding new type = edit N files
```

### Solution
Single registry bundling all type-specific behavior:

```
// definitions.ts - ONE location for all type-specific code
const DEFS: Record<EntityType, Definition> = {
  typeA: { render: renderA, update: updateA, ... },
  typeB: { render: renderB, update: updateB, ... },
};

// Consumers dispatch generically
DEFS[entity.type].render(entity, ctx);
DEFS[entity.type].update(entity, dt);

// Adding new type = ONE registry entry, ZERO consumer changes
```

### Implementation Checklist

1. Define base `Definition` interface with all operations
2. Create `DEFS: Record<Type, Definition>` registry
3. Export `getDef(type): Definition` helper
4. Replace all switches with `getDef(entity.type).operation()`
5. Use language features for exhaustiveness (TypeScript `Record`, Rust `match`)

## Pattern 2: Capability Composition

### Problem
Not all entities need all behaviors. Deep inheritance or marker interfaces create coupling.

### Solution
Optional capability configs with type guards:

```
interface Definition<T> {
  // Required for all
  create(): T;
  render(): void;

  // Optional capabilities - entities opt-in
  collision?: CollisionConfig;
  physics?: PhysicsConfig;
  persistence?: PersistenceConfig;
}

// Type guard for safe access
function hasCollision(def): def is Definition & { collision: CollisionConfig } {
  return def.collision !== undefined;
}

// Consumer checks capability
if (hasCollision(def)) {
  collisionSystem.register(entity, def.collision);
}
```

### Benefits
- Entities opt-in to behaviors they need
- No inheritance hierarchies
- Capability presence is runtime-checkable
- Systems ignore entities without relevant capabilities

## Pattern 3: Layered Definition Interfaces

```
BaseDefinition           (create, render, layer)
    ↓ extends
DomainDefinition         (domain-specific: AI, weapons)
    ↓ implemented by
ConcreteDefinitions      (typeA, typeB, typeC)
```

### Implementation

```
// Base - works for any domain
interface EntityDefinition<TState, TType> {
  type: TType;
  create(pos): TState;
  update?(entity, ctx): void;
  render(entity, ctx): void;
  collision?: CollisionConfig;
  physics?: PhysicsConfig;
}

// Domain-specific extension
interface EnemyDefinition extends EntityDefinition<EnemyState, EnemyType> {
  aiStrategy: AIStrategy;
  weapons: WeaponConfig[];
}

// Another domain
interface PickupDefinition extends EntityDefinition<PickupState, PickupType> {
  onCollect(collector): void;
  floatAnimation: AnimationConfig;
}
```

## Pattern 4: Context Objects

### Problem
Functions with many parameters, hard to extend.

### Solution
Bundle related parameters into context objects:

```
// Bad - hard to extend
function update(entity, dt, playerPos, playerVel, gravity, time) { ... }

// Good - extensible
interface UpdateContext {
  dt: number;
  playerPos: Vec2;
  playerVel: Vec2;
  // Easy to add fields without breaking signatures
}

function update(entity, ctx: UpdateContext) { ... }
```

### Context Inheritance

```
interface BaseContext { dt: number; }
interface AIContext extends BaseContext { playerPos: Vec2; threats: Entity[]; }
interface RenderContext { graphics: Graphics; screenPos: Vec2; scale: number; }
```

## Pattern 5: Infrastructure-First Development

### Order of Implementation

1. **Generic infrastructure first** (dispatcher, event bus, registry helpers)
2. **Base interfaces** (EntityDefinition, capability configs)
3. **First domain implementation** (proves the pattern)
4. **Second domain validates pattern** (confirms generality)
5. **Retrofit existing systems** (migrate incrementally)

### Rule

> If writing a switch statement on entity type, infrastructure is missing.

## Anti-Patterns To Avoid

### 1. Scattered Switches
Adding new type requires editing N files.
**Fix**: Consolidate into registry.

### 2. Deep Inheritance
`SpecialEnemy extends FlyingEnemy extends Enemy extends Entity`
**Fix**: Capability composition.

### 3. Optional Fields Instead of Capabilities
```
interface Entity {
  weapon?: Weapon;  // null checks everywhere
}
```
**Fix**: Separate capability with type guard.

### 4. Premature Abstraction
Creating registry for 1 type.
**Fix**: Wait for second type to validate pattern.

### 5. God Objects
Definition with 50 fields for every possible behavior.
**Fix**: Required base + optional capabilities.

## Exhaustiveness Enforcement

Use language features to ensure all types are handled:

```typescript
// TypeScript - Record requires all keys
const DEFS: Record<EntityType, Definition> = {
  // Compiler error if type missing
};

// Helper for switch exhaustiveness
function assertNever(x: never): never {
  throw new Error(`Unexpected: ${x}`);
}
```

## Summary Checklist

When designing entity systems:

- [ ] Entities are pure data with type discriminator field
- [ ] Definitions bundle ALL type-specific behavior
- [ ] Single registry maps type → definition
- [ ] Consumers dispatch via registry lookup (no switches)
- [ ] Capabilities are optional configs with type guards
- [ ] Context objects bundle related parameters
- [ ] Language features enforce exhaustiveness
- [ ] Adding new type = one registry entry, zero system changes
