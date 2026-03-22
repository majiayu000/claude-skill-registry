---
name: context
description: Runtime context passed to compiled closures — the world as seen from inside
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: RUNTIME-CONTEXT
tags: [moollm, runtime, context, closure, state, primitive]
related: [object, adventure, room, buff, simulation]
adversary: global-state
---

# Context

> *"The context IS the world as seen from inside the closure."*
> — Dave Ungar, on lexical scope

---

## What Is It?

The **world** object is passed to every compiled closure. It provides:

1. **Standard keys** — Always present (adventure, player, room, turn)
2. **Extended keys** — Contextual (object, target, npc)
3. **Skill namespaces** — Skills register state under `world.skills.skill_name`
4. **Utility functions** — API for interacting with the world

### Why "world" not "ctx"?

- More evocative — closures see the WORLD
- Self-documenting — `world.player`, `world.room`
- Matches the mental model

---

## Standard Keys

Always present in every world:

```javascript
world.turn           // Current simulation turn
world.timestamp      // ISO timestamp

world.adventure      // Root adventure state
  .name
  .flags             // Global boolean flags
  .world_state       // Global key/value state

world.player         // Current player
  .id
  .name
  .location          // Path to current room
  .inventory         // Array of item ids
  .buffs             // Active buffs

world.room           // Current room
  .id
  .name
  .path
  .exits
  .objects
  .is_dark
  .is_dangerous

world.party          // Party state
  .members
  .leader
```

---

## Extended Keys

Present when relevant:

```javascript
// When running object simulate/methods:
world.object         // The object being simulated
  .id
  .state             // Object's mutable state
  // Methods are bound: world.consume_fuel(1)

// When action targets something:
world.target         // The target
  .id
  .type              // "object", "character", "room"

// When NPC is simulating:
world.npc            // The NPC
  .id
  .goals
  .state
```

---

## Skill State Namespaces

Skills register state under `world.skills.<skill_name>` using **underscores**:

```javascript
// Skill "economy" → world.skills.economy
world.skills.economy.gold        // 100

// Skill "pie-menu" → world.skills.pie_menu (underscore!)
world.skills.pie_menu.last_selection  // "north"

// Skill "time" → world.skills.time
world.skills.time.hour           // 14
world.skills.time.phase          // "afternoon"
```

**Why underscores?** Dashes aren't valid JS/Python identifiers. `foo-bar` skill → `foo_bar` namespace.

This keeps skill state organized and avoids collisions.

---

## Utility Functions

Methods bound to world for interaction:

### Narrative

```javascript
world.emit("The lamp dies!")              // Show message
world.narrate("Darkness falls.", "dramatic")
```

### Events

```javascript
world.trigger_event("GRUE_APPROACHES", { room: world.room.path })
```

### Inventory

```javascript
world.has("brass-key")                    // true/false
world.give("gold-coins")                  // Add to inventory
world.take("used-potion")                 // Remove from inventory
```

### Flags

```javascript
world.flag("dragon_slain")                // Get flag
world.set_flag("treasure_found", true)    // Set flag
```

### State

```javascript
world.get("object.state.fuel")            // Get by path
world.set("object.state.lit", true)       // Set by path
```

### Navigation

```javascript
world.go("../maze/room-a/")               // Move player
world.can_go("north")                     // Check exit
```

### Buffs

```javascript
world.add_buff({ name: "Caffeinated", effect: { energy: +2 }, duration: 5 })
world.remove_buff("caffeinated")
world.has_buff("grue_immunity")
```

### Logging

```javascript
world.log("Debug: fuel = " + world.object.state.fuel)
```

---

## Example: Lamp Simulate

```javascript
simulate_js: (world) => {
  if (world.object.state.lit) {
    world.consume_fuel(1);                  // Call object method
    
    if (world.object.state.fuel <= 0) {
      world.extinguish();                   // Call object method
      world.emit("The lamp sputters and dies!");
      
      if (world.room.is_dark && world.room.is_dangerous) {
        world.trigger_event("GRUE_APPROACHES");
      }
    }
  }
}
```

---

## Example: Guard Expression

```yaml
guard: "player has the key AND room is not dark"
guard_js: (world) => world.has("brass-key") && !world.room.is_dark
```

---

## Example: Score Calculation

```yaml
score_if: "player is tired OR room is dark"
score_if_js: (world) => world.has_buff("tired") || world.room.is_dark
```

---

## Example: Skill State

```yaml
# Skill "economy" needs to check gold
guard: "player has at least 10 gold"
guard_js: (world) => world.skills.economy.gold >= 10

# Skill "pie-menu" checks last selection
score_if: "last pie menu selection was north"
score_if_js: (world) => world.skills.pie_menu.last_selection === "north"
```

---

## Design Principles

### Structured, Not Arbitrary

world is NOT just a bag of key/values. It has defined structure:
- Standard keys are always present
- Extended keys appear in context
- Skills namespace their state (with underscores!)
- Functions are bound methods

### Skill Namespaces (Underscores!)

Skills don't pollute root world. They register under `world.skills.skill_name`:

```javascript
// Skill "economy" → world.skills.economy
world.skills.economy.gold
world.skills.economy.currency

// Skill "pie-menu" → world.skills.pie_menu (underscore!)
world.skills.pie_menu.last_selection
world.skills.pie_menu.hover_direction

// Skill "foo-bar" → world.skills.foo_bar
world.skills.foo_bar.some_state
```

**Rule:** `skill-name` with dashes → `skill_name` with underscores in namespace.

### Methods Are Bound

Object methods appear as functions on world:

```javascript
// Object defines:
methods:
  consume_fuel: "reduce fuel by amount"

// At runtime, method is bound:
world.consume_fuel(1)  // Works!
```

---

## Related Skills

- [object](../object/) — Provides ctx.object
- [room](../room/) — Provides ctx.room
- [adventure](../adventure/) — Provides ctx.adventure
- [buff](../buff/) — Used by ctx.add_buff/has_buff

---

## Dual Runtime: Python + JavaScript

**CRITICAL:** We always generate BOTH `_js` AND `_py` versions of compiled expressions.

```yaml
# Natural language
guard: "player has the key AND room is not dark"

# BOTH generated:
guard_js: (world) => world.has("brass-key") && !world.room.is_dark
guard_py: lambda world: world.has("brass-key") and not world.room.is_dark
```

### Why Dual Runtimes?

| Runtime | Purpose |
|---------|---------|
| **Python** | Server-side simulation, testing, LLM tethering |
| **JavaScript** | Browser runtime, standalone play |

### Keeping Them In Sync

1. **Same semantics** — Both should produce identical results
2. **Same world structure** — `world.player`, `world.room`, etc.
3. **Same utility functions** — `world.has()`, `world.emit()`, etc.
4. **Generated together** — LLM produces both in one pass

### The Compilation Event

```yaml
- event: COMPILE_EXPRESSION
  field: guard
  source: "player has the key"
  targets:
    - field: guard_js
      language: javascript
    - field: guard_py
      language: python
  expected_type: boolean
```

### Python Runtime Class

```python
class World:
    """Python runtime context — mirrors JavaScript World class."""
    
    def __init__(self, adventure_data):
        self.turn = 0
        self.adventure = adventure_data
        self.player = adventure_data['player']
        self.room = None  # Set on navigation
        self.party = adventure_data['party']
        self.object = None  # Set during object simulation
        self.skills = {}  # Skill state namespaces
        
    def has(self, item_id: str) -> bool:
        return item_id in self.player.get('inventory', [])
        
    def flag(self, name: str) -> bool:
        return self.adventure.get('flags', {}).get(name, False)
        
    def emit(self, message: str):
        print(message)  # Or queue for output
        
    def trigger_event(self, name: str, data=None):
        # Event system handles this
        pass
```

### JavaScript Runtime Class

```javascript
class World {
  /** JavaScript runtime context — mirrors Python World class. */
  
  constructor(adventureData) {
    this.turn = 0;
    this.adventure = adventureData;
    this.player = adventureData.player;
    this.room = null;  // Set on navigation
    this.party = adventureData.party;
    this.object = null;  // Set during object simulation
    this.skills = {};  // Skill state namespaces
  }
  
  has(itemId) {
    return (this.player.inventory || []).includes(itemId);
  }
  
  flag(name) {
    return (this.adventure.flags || {})[name] || false;
  }
  
  emit(message) {
    console.log(message);  // Or queue for UI
  }
  
  triggerEvent(name, data) {
    // Event system handles this
  }
}
```

---

## Protocol Symbol

```
RUNTIME-CONTEXT — The world passed to closures (Python + JavaScript)
```
