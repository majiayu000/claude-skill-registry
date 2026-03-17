---
name: theone-cocos-standards
description: Enforces TheOne Studio Cocos Creator development standards including TypeScript coding patterns, Cocos Creator 3.x architecture (Component system, EventDispatcher), and playable ads optimization guidelines. Triggers when writing, reviewing, or refactoring Cocos TypeScript code, implementing playable ads features, optimizing performance/bundle size, or reviewing code changes.
---

# TheOne Studio Cocos Creator Development Standards

⚠️ **Cocos Creator 3.x (TypeScript 4.1+):** All patterns and examples are compatible with Cocos Creator 3.x playable ads development.

## Skill Purpose

This skill enforces TheOne Studio's comprehensive Cocos Creator development standards with **CODE QUALITY FIRST**:

**Priority 1: Code Quality & Hygiene** (MOST IMPORTANT)
- TypeScript strict mode, ESLint configuration, access modifiers (public/private/protected)
- Throw exceptions (never silent errors)
- console.log for development, remove in production builds
- readonly for immutable fields, const for constants
- No inline comments (use descriptive names)
- Proper error handling and type safety

**Priority 2: Modern TypeScript Patterns**
- Array methods (map/filter/reduce) over loops
- Arrow functions, destructuring, spread operators
- Optional chaining, nullish coalescing
- Type guards, utility types (Partial, Required, Readonly)
- Modern TypeScript features

**Priority 3: Cocos Creator Architecture**
- Component-based Entity-Component (EC) system
- Lifecycle methods: onLoad→start→onEnable→update→onDisable→onDestroy
- EventDispatcher pattern for custom events
- Node event system (EventTouch, keyboard events)
- Resource management and pooling for playables

**Priority 4: Playable Ads Performance**
- DrawCall batching (<10 DrawCalls target)
- Sprite atlas configuration (auto-atlas enabled)
- GPU skinning for skeletal animations
- Zero allocations in update() loop
- Bundle size <5MB (texture compression, code minification)

## When This Skill Triggers

- Writing or refactoring Cocos Creator TypeScript code
- Implementing playable ads features
- Working with component lifecycle and events
- Optimizing performance for playable ads
- Reviewing code changes or pull requests
- Setting up playable project architecture
- Reducing bundle size or DrawCall counts

## Quick Reference Guide

### What Do You Need Help With?

| Priority | Task | Reference |
|----------|------|-----------|
| **🔴 PRIORITY 1: Code Quality (Check FIRST)** | | |
| 1 | TypeScript strict mode, ESLint, access modifiers | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| 1 | Throw exceptions, proper error handling | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| 1 | console.log (development only), remove in production | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| 1 | readonly/const, no inline comments, descriptive names | [Quality & Hygiene](references/language/quality-hygiene.md) ⭐ |
| **🟡 PRIORITY 2: Modern TypeScript Patterns** | | |
| 2 | Array methods, arrow functions, destructuring | [Modern TypeScript](references/language/modern-typescript.md) |
| 2 | Optional chaining, nullish coalescing | [Modern TypeScript](references/language/modern-typescript.md) |
| 2 | Type guards, utility types | [Modern TypeScript](references/language/modern-typescript.md) |
| **🟢 PRIORITY 3: Cocos Architecture** | | |
| 3 | Component system, @property decorator | [Component System](references/framework/component-system.md) |
| 3 | Lifecycle methods (onLoad→start→update→onDestroy) | [Component System](references/framework/component-system.md) |
| 3 | EventDispatcher, Node events, cleanup | [Event Patterns](references/framework/event-patterns.md) |
| 3 | Resource loading, pooling, memory management | [Playable Optimization](references/framework/playable-optimization.md) |
| **🔵 PRIORITY 4: Performance & Review** | | |
| 4 | DrawCall batching, sprite atlas, GPU skinning | [Playable Optimization](references/framework/playable-optimization.md) |
| 4 | Update loop optimization, zero allocations | [Performance](references/language/performance.md) |
| 4 | Bundle size reduction (<5MB target) | [Size Optimization](references/framework/size-optimization.md) |
| 4 | Architecture review (components, lifecycle, events) | [Architecture Review](references/review/architecture-review.md) |
| 4 | TypeScript quality review | [Quality Review](references/review/quality-review.md) |
| 4 | Performance review (DrawCalls, allocations) | [Performance Review](references/review/performance-review.md) |

## 🔴 CRITICAL: Code Quality Rules (CHECK FIRST!)

### ⚠️ MANDATORY QUALITY STANDARDS

**ALWAYS enforce these BEFORE writing any code:**

1. **Enable TypeScript strict mode** - "strict": true in tsconfig.json
2. **Use ESLint configuration** - @typescript-eslint rules enabled
3. **Use access modifiers** - public/private/protected on all members
4. **Throw exceptions for errors** - NEVER silent failures or undefined returns
5. **console.log for development only** - Remove all console statements in production builds
6. **Use readonly for immutable fields** - Mark fields that aren't reassigned
7. **Use const for constants** - Constants should be const, not let
8. **No inline comments** - Use descriptive names; code should be self-explanatory
9. **Proper null/undefined handling** - Use optional chaining and nullish coalescing
10. **Type safety** - Avoid `any` type, use proper types and interfaces

**Example: Enforce Quality First**

```typescript
// ✅ EXCELLENT: All quality rules enforced
import { _decorator, Component, Node, EventTouch } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('PlayerController')
export class PlayerController extends Component {
    // 3. Access modifier, 6. readonly for immutable
    @property(Node)
    private readonly targetNode: Node | null = null;

    // 7. const for constants
    private static readonly MAX_HEALTH: number = 100;
    private currentHealth: number = 100;

    // Lifecycle: onLoad → start → onEnable
    protected onLoad(): void {
        // 4. Throw exception for errors
        if (!this.targetNode) {
            throw new Error('PlayerController: targetNode is not assigned');
        }

        // 9. Proper event listener setup
        this.node.on(Node.EventType.TOUCH_START, this.onTouchStart, this);
    }

    protected onDestroy(): void {
        // 9. Always cleanup event listeners
        this.node.off(Node.EventType.TOUCH_START, this.onTouchStart, this);
    }

    private onTouchStart(event: EventTouch): void {
        // 5. console.log only for development (remove in production)
        if (CC_DEBUG) {
            console.log('Touch detected');
        }

        this.takeDamage(10);
    }

    // 8. Descriptive method names (no inline comments needed)
    private takeDamage(amount: number): void {
        this.currentHealth -= amount;

        if (this.currentHealth <= 0) {
            this.handlePlayerDeath();
        }
    }

    private handlePlayerDeath(): void {
        // Death logic
    }
}
```

## ⚠️ Cocos Creator Architecture Rules (AFTER Quality)

### Component System Fundamentals

**Entity-Component (EC) System:**
- Components extend `Component` class
- Use `@ccclass` and `@property` decorators
- Lifecycle: onLoad → start → onEnable → update → lateUpdate → onDisable → onDestroy

**Execution Order:**
1. **onLoad()** - Component initialization, one-time setup
2. **start()** - After all components loaded, can reference other components
3. **onEnable()** - When component/node enabled (can be called multiple times)
4. **update(dt)** - Every frame (use sparingly for playables)
5. **lateUpdate(dt)** - After all update() calls
6. **onDisable()** - When component/node disabled
7. **onDestroy()** - Cleanup, remove listeners, release resources

**Universal Rules:**
- ✅ Initialize in onLoad(), reference other components in start()
- ✅ Register events in onEnable(), unregister in onDisable()
- ✅ Always cleanup listeners in onDestroy()
- ✅ Avoid heavy logic in update() (performance critical for playables)
- ✅ Use readonly for @property fields that shouldn't be reassigned
- ✅ Throw exceptions for missing required references

## Brief Examples

### 🔴 Code Quality First

```typescript
// ✅ EXCELLENT: Quality rules enforced
import { _decorator, Component, Node } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('GameManager')
export class GameManager extends Component {
    @property(Node)
    private readonly playerNode: Node | null = null;

    private static readonly MAX_SCORE: number = 1000;
    private currentScore: number = 0;

    protected onLoad(): void {
        // Throw exception for missing required references
        if (!this.playerNode) {
            throw new Error('GameManager: playerNode is required');
        }

        if (CC_DEBUG) {
            console.log('GameManager initialized'); // Development only
        }
    }

    public addScore(points: number): void {
        if (points <= 0) {
            throw new Error('GameManager.addScore: points must be positive');
        }

        this.currentScore = Math.min(
            this.currentScore + points,
            GameManager.MAX_SCORE
        );
    }
}
```

### 🟡 Modern TypeScript Patterns

```typescript
// ✅ GOOD: Array methods instead of loops
const activeEnemies = allEnemies.filter(e => e.isActive);
const enemyPositions = activeEnemies.map(e => e.node.position);

// ✅ GOOD: Optional chaining and nullish coalescing
const playerName = player?.name ?? 'Unknown';

// ✅ GOOD: Destructuring
const { x, y } = this.node.position;

// ✅ GOOD: Arrow functions
this.enemies.forEach(enemy => enemy.takeDamage(10));

// ✅ GOOD: Type guards
function isPlayer(node: Node): node is PlayerNode {
    return node.getComponent(PlayerController) !== null;
}
```

### 🟢 Cocos Creator Component Pattern

```typescript
import { _decorator, Component, Node, EventTouch, Vec3 } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('TouchHandler')
export class TouchHandler extends Component {
    @property(Node)
    private readonly targetNode: Node | null = null;

    private readonly tempVec3: Vec3 = new Vec3(); // Reusable vector

    // 1. onLoad: Initialize component
    protected onLoad(): void {
        if (!this.targetNode) {
            throw new Error('TouchHandler: targetNode is required');
        }
    }

    // 2. start: Reference other components (if needed)
    protected start(): void {
        // Can safely access other components here
    }

    // 3. onEnable: Register event listeners
    protected onEnable(): void {
        this.node.on(Node.EventType.TOUCH_START, this.onTouchStart, this);
        this.node.on(Node.EventType.TOUCH_MOVE, this.onTouchMove, this);
    }

    // 4. onDisable: Unregister event listeners
    protected onDisable(): void {
        this.node.off(Node.EventType.TOUCH_START, this.onTouchStart, this);
        this.node.off(Node.EventType.TOUCH_MOVE, this.onTouchMove, this);
    }

    // 5. onDestroy: Final cleanup
    protected onDestroy(): void {
        // Release any additional resources
    }

    private onTouchStart(event: EventTouch): void {
        // Handle touch
    }

    private onTouchMove(event: EventTouch): void {
        // Reuse vector to avoid allocations
        this.targetNode!.getPosition(this.tempVec3);
        this.tempVec3.y += 10;
        this.targetNode!.setPosition(this.tempVec3);
    }
}
```

### 🟢 Event Dispatcher Pattern

```typescript
import { _decorator, Component, EventTarget } from 'cc';
const { ccclass } = _decorator;

// Custom event types
export enum GameEvent {
    SCORE_CHANGED = 'score_changed',
    LEVEL_COMPLETE = 'level_complete',
    PLAYER_DIED = 'player_died',
}

export interface ScoreChangedEvent {
    oldScore: number;
    newScore: number;
}

@ccclass('EventManager')
export class EventManager extends Component {
    private static instance: EventManager | null = null;
    private readonly eventTarget: EventTarget = new EventTarget();

    protected onLoad(): void {
        if (EventManager.instance) {
            throw new Error('EventManager: instance already exists');
        }
        EventManager.instance = this;
    }

    public static emit(event: GameEvent, data?: any): void {
        if (!EventManager.instance) {
            throw new Error('EventManager: instance not initialized');
        }
        EventManager.instance.eventTarget.emit(event, data);
    }

    public static on(event: GameEvent, callback: Function, target?: any): void {
        if (!EventManager.instance) {
            throw new Error('EventManager: instance not initialized');
        }
        EventManager.instance.eventTarget.on(event, callback, target);
    }

    public static off(event: GameEvent, callback: Function, target?: any): void {
        if (!EventManager.instance) {
            throw new Error('EventManager: instance not initialized');
        }
        EventManager.instance.eventTarget.off(event, callback, target);
    }
}

// Usage in component
@ccclass('ScoreDisplay')
export class ScoreDisplay extends Component {
    protected onEnable(): void {
        EventManager.on(GameEvent.SCORE_CHANGED, this.onScoreChanged, this);
    }

    protected onDisable(): void {
        EventManager.off(GameEvent.SCORE_CHANGED, this.onScoreChanged, this);
    }

    private onScoreChanged(data: ScoreChangedEvent): void {
        console.log(`Score: ${data.oldScore} → ${data.newScore}`);
    }
}
```

### 🔵 Playable Performance Optimization

```typescript
import { _decorator, Component, Node, Sprite, SpriteAtlas } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('OptimizedSpriteManager')
export class OptimizedSpriteManager extends Component {
    // Use sprite atlas for DrawCall batching
    @property(SpriteAtlas)
    private readonly characterAtlas: SpriteAtlas | null = null;

    // Preallocate arrays to avoid allocations in update()
    private readonly tempNodes: Node[] = [];
    private frameCount: number = 0;

    protected onLoad(): void {
        if (!this.characterAtlas) {
            throw new Error('OptimizedSpriteManager: characterAtlas is required');
        }

        // Prewarm sprite frames from atlas
        this.prewarmSpriteFrames();
    }

    private prewarmSpriteFrames(): void {
        // Load all sprites from atlas (batched in single DrawCall)
        const spriteFrame = this.characterAtlas!.getSpriteFrame('character_idle');
        if (!spriteFrame) {
            throw new Error('Sprite frame not found in atlas');
        }
    }

    // Optimize update: avoid allocations, use object pooling
    protected update(dt: number): void {
        // Run expensive operations every N frames instead of every frame
        this.frameCount++;
        if (this.frameCount % 10 === 0) {
            this.updateExpensiveOperation();
        }
    }

    private updateExpensiveOperation(): void {
        // Reuse array instead of creating new one
        this.tempNodes.length = 0;

        // Batch operations to reduce DrawCalls
    }
}
```

## Code Review Checklist

### Quick Validation (before committing)

**🔴 Code Quality (CHECK FIRST):**
- [ ] TypeScript strict mode enabled in tsconfig.json
- [ ] ESLint rules passing (no errors)
- [ ] All access modifiers correct (public/private/protected)
- [ ] Exceptions thrown for errors (no silent failures)
- [ ] console.log removed or wrapped in CC_DEBUG
- [ ] readonly used for non-reassigned fields
- [ ] const used for constants
- [ ] No inline comments (self-explanatory code)
- [ ] Proper null/undefined handling
- [ ] No `any` types (use proper types)

**🟡 Modern TypeScript Patterns:**
- [ ] Array methods used instead of manual loops
- [ ] Arrow functions for callbacks
- [ ] Optional chaining (?.) for safe property access
- [ ] Nullish coalescing (??) for default values
- [ ] Destructuring for cleaner code
- [ ] Type guards for type narrowing

**🟢 Cocos Creator Architecture:**
- [ ] Component lifecycle methods in correct order
- [ ] onLoad() for initialization, start() for references
- [ ] Event listeners registered in onEnable()
- [ ] Event listeners unregistered in onDisable()
- [ ] Resources released in onDestroy()
- [ ] @property decorator used correctly
- [ ] Required references validated (throw if null)

**🔵 Playable Performance:**
- [ ] No allocations in update() loop
- [ ] Sprite atlas used for DrawCall batching
- [ ] GPU skinning enabled for skeletal animations
- [ ] Expensive operations throttled (not every frame)
- [ ] Object pooling for frequently created objects
- [ ] Texture compression enabled
- [ ] Bundle size <5MB target
- [ ] DrawCall count <10 target

## Common Mistakes to Avoid

### ❌ DON'T:
1. **Ignore TypeScript strict mode** → Enable "strict": true
2. **Silent error handling** → Throw exceptions for errors
3. **Leave console.log in production** → Remove or wrap in CC_DEBUG
4. **Skip access modifiers** → Use public/private/protected
5. **Use `any` type** → Define proper types and interfaces
6. **Add inline comments** → Use descriptive names instead
7. **Skip event cleanup** → Always unregister in onDisable/onDestroy
8. **Allocate in update()** → Preallocate and reuse objects
9. **Forget sprite atlas** → Use atlas for DrawCall batching
10. **Heavy logic in update()** → Throttle expensive operations
11. **Skip null checks** → Validate required references in onLoad
12. **Mutable @property fields** → Use readonly when appropriate
13. **Manual loops over arrays** → Use map/filter/reduce
14. **Ignore bundle size** → Monitor and optimize (<5MB target)

### ✅ DO:
1. **Enable TypeScript strict mode** ("strict": true)
2. **Throw exceptions for errors** (never silent failures)
3. **Use console.log for development only** (remove in production)
4. **Use access modifiers** (public/private/protected)
5. **Define proper types** (avoid `any`)
6. **Use descriptive names** (no inline comments)
7. **Always cleanup events** (onDisable/onDestroy)
8. **Preallocate objects** (reuse in update())
9. **Use sprite atlas** (DrawCall batching)
10. **Throttle expensive operations** (not every frame)
11. **Validate required references** (throw in onLoad if null)
12. **Use readonly for @property** (when appropriate)
13. **Use array methods** (map/filter/reduce)
14. **Monitor bundle size** (<5MB target for playables)

## Review Severity Levels

### 🔴 Critical (Must Fix)
- **TypeScript strict mode disabled** - Must enable "strict": true
- **Silent error handling** - Must throw exceptions for errors
- **console.log in production code** - Remove or wrap in CC_DEBUG
- **Missing access modifiers** - All members must have modifiers
- **Using `any` type without justification** - Define proper types
- **Inline comments instead of descriptive names** - Rename and remove comments
- **Event listeners not cleaned up** - Memory leak, must unregister
- **Missing required reference validation** - Must throw in onLoad if null
- **Allocations in update() loop** - Performance critical, must preallocate
- **No sprite atlas for multiple sprites** - DrawCall explosion, must use atlas
- **Bundle size >5MB** - Exceeds playable limit, must optimize

### 🟡 Important (Should Fix)
- **Missing readonly on @property fields** - Should be readonly when not reassigned
- **Missing const for constants** - Should use const instead of let
- **Manual loops instead of array methods** - Should use map/filter/reduce
- **Missing optional chaining** - Should use ?. for safe access
- **Missing nullish coalescing** - Should use ?? for default values
- **Heavy logic in update()** - Should throttle expensive operations
- **No object pooling for frequent allocations** - Should implement pooling
- **Texture compression not enabled** - Should enable for smaller bundle
- **DrawCall count >10** - Should optimize batching

### 🟢 Nice to Have (Suggestion)
- Could use arrow function for callback
- Could destructure for cleaner code
- Could use type guard for type safety
- Could improve naming for clarity
- Could add interface for better typing
- Could optimize algorithm for better performance

## Detailed References

### TypeScript Language Standards
- [Quality & Hygiene](references/language/quality-hygiene.md) - Strict mode, ESLint, access modifiers, error handling
- [Modern TypeScript](references/language/modern-typescript.md) - Array methods, optional chaining, type guards, utility types
- [Performance](references/language/performance.md) - Update loop optimization, zero allocations, caching

### Cocos Creator Framework
- [Component System](references/framework/component-system.md) - EC system, lifecycle methods, @property decorator
- [Event Patterns](references/framework/event-patterns.md) - EventDispatcher, Node events, subscription cleanup
- [Playable Optimization](references/framework/playable-optimization.md) - DrawCall batching, sprite atlas, GPU skinning, resource pooling
- [Size Optimization](references/framework/size-optimization.md) - Bundle size reduction, texture compression, build optimization

### Code Review
- [Architecture Review](references/review/architecture-review.md) - Component violations, lifecycle errors, event leaks
- [Quality Review](references/review/quality-review.md) - TypeScript quality issues, access modifiers, error handling
- [Performance Review](references/review/performance-review.md) - Playable-specific performance problems, DrawCalls, allocations

## Summary

This skill provides comprehensive Cocos Creator development standards for TheOne Studio's playable ads team:
- **TypeScript Excellence**: Strict mode, modern patterns, type safety
- **Cocos Architecture**: Component lifecycle, event patterns, resource management
- **Playable Performance**: DrawCall batching, GPU skinning, <5MB bundles
- **Code Quality**: Enforced quality, hygiene, and performance rules

Use the Quick Reference Guide above to navigate to the specific pattern you need.
