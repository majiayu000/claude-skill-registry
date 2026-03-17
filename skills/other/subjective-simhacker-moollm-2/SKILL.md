---
name: subjective
description: First-person code — the "I" shifts based on who is speaking
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: SUBJECTIVE-ORIENTED
tags: [moollm, programming, perspective, first-person, context]
related: [context, runtime, object, character]
adversary: third-person-coupling
---

# Subjective-Oriented Programming

> *"i_have('key') reads naturally. 'Does the world have a key?' does not."*
> — The Gezelligheid Grotto Design Principles

---

## What Is It?

**Subjective-oriented programming** uses `i_` prefixed functions that speak from the current subject's perspective. The "I" shifts based on context:

| Context | Who is "I"? |
|---------|-------------|
| Player action | The player character |
| Object simulate() | The object |
| NPC dialogue | The NPC |
| Room description | The room |

---

## The Problem with `world.`

```javascript
// Third-person: "Does the world have a key?"
if (world.has("key")) ...

// But who has the key? The world? The player? Confusing!
```

## The Solution: `i_`

```javascript
// First-person: "Do I have a key?"
if (i_have("key")) ...

// Clear! The current subject is asking about themselves.
```

---

## Core `i_` Functions

### Inventory

```javascript
i_have("key")           // Do I have this item?
i_give("key")           // Give item to current target
i_take("key")           // Take item from current target
i_drop("key")           // Drop item in current room
i_has_tag("weapon")     // Do I have any item with this tag?
i_find_by_tag("food")   // Find all my items with this tag
```

### State

```javascript
i_am("lit")             // Am I in this state? (object.state.lit)
i_am_not("broken")      // Am I NOT in this state?
i_set("lit", true)      // Set my state
i_get("fuel")           // Get my state value
```

### Buffs

```javascript
i_have_buff("strength")     // Do I have this buff?
i_add_buff(buff)            // Apply buff to myself
i_remove_buff("strength")   // Remove buff from myself
```

### Flags

```javascript
i_flag("door_unlocked")     // Is this flag set?
i_set_flag("door_unlocked") // Set this flag
```

### Location

```javascript
i_am_in("pub/")             // Am I in this room?
i_can_see("treasure")       // Can I see this object?
i_go("north")               // Move in direction
```

### Communication

```javascript
i_say("Hello!")             // Emit dialogue
i_emote("grins widely")     // Emit emote
i_think("This is odd...")   // Emit internal thought
```

---

## Context Shifting

The meaning of `i_` changes based on who is "speaking":

### Player Context

```yaml
# In player action handlers
effect: |
  if i_have("key"):
    i_say("I found the key!")
    i_drop("key")  # Drop in current room
```

### Object Context (simulate)

```yaml
# In object's simulate field
simulate: |
  if i_am("lit"):
    i_set("fuel", i_get("fuel") - 1)
    if i_get("fuel") <= 0:
      i_set("lit", false)
      i_emit("The lamp dies!")
```

### NPC Context

```yaml
# In NPC dialogue/behavior
behavior: |
  if i_have("gold") and i_can_see("beggar"):
    i_give("gold")
    i_say("For you, friend.")
```

### Room Context

```yaml
# In room description/behavior
describe: |
  if i_am("dark"):
    i_emit("You can't see anything.")
  else:
    i_emit("A cozy room with a fireplace.")
```

---

## Implementation

The `i_` functions are bound to the current subject:

```javascript
class World {
  // The current subject ("I")
  get subject() {
    return this.object || this.npc || this.player;
  }
  
  // === INVENTORY (subjective) ===
  
  i_have(itemId) {
    const inv = this.subject.inventory || [];
    return inv.includes(itemId);
  }
  
  i_give(itemId) {
    const inv = this.subject.inventory || [];
    const idx = inv.indexOf(itemId);
    if (idx > -1) {
      inv.splice(idx, 1);
      (this.target.inventory ??= []).push(itemId);
    }
  }
  
  i_take(itemId) {
    const targetInv = this.target.inventory || [];
    const idx = targetInv.indexOf(itemId);
    if (idx > -1) {
      targetInv.splice(idx, 1);
      (this.subject.inventory ??= []).push(itemId);
    }
  }
  
  i_drop(itemId) {
    const inv = this.subject.inventory || [];
    const idx = inv.indexOf(itemId);
    if (idx > -1) {
      inv.splice(idx, 1);
      (this.room.objects ??= []).push({ id: itemId });
    }
  }
  
  i_has_tag(tag) {
    const inv = this.subject.inventory || [];
    for (const itemId of inv) {
      const item = this.getObject(itemId);
      if (item && (item.tags || []).includes(tag)) {
        return true;
      }
    }
    return false;
  }
  
  // === STATE (subjective) ===
  
  i_am(stateKey) {
    return this.subject.state?.[stateKey] === true;
  }
  
  i_am_not(stateKey) {
    return !this.i_am(stateKey);
  }
  
  i_get(stateKey) {
    return this.subject.state?.[stateKey];
  }
  
  i_set(stateKey, value) {
    this.subject.state ??= {};
    this.subject.state[stateKey] = value;
  }
  
  // === BUFFS (subjective) ===
  
  i_have_buff(buffId) {
    const buffs = this.subject.buffs || [];
    return buffs.some(b => b.id === buffId);
  }
  
  i_add_buff(buff) {
    this.subject.buffs ??= [];
    this.subject.buffs.push(buff);
  }
  
  i_remove_buff(buffId) {
    const buffs = this.subject.buffs || [];
    this.subject.buffs = buffs.filter(b => b.id !== buffId);
  }
  
  // === LOCATION (subjective) ===
  
  i_am_in(roomPath) {
    return this.subject.location === roomPath ||
           this.room?.path === roomPath;
  }
  
  i_can_see(objectId) {
    const objects = this.room?.objects || [];
    return objects.some(o => o.id === objectId);
  }
  
  i_go(direction) {
    this._pendingNavigation = direction;
  }
  
  // === COMMUNICATION (subjective) ===
  
  i_say(message) {
    this.emit(`${this.subject.name}: "${message}"`);
  }
  
  i_emote(action) {
    this.emit(`${this.subject.name} ${action}`);
  }
  
  i_think(thought) {
    this.emit(`(${this.subject.name} thinks: "${thought}")`);
  }
  
  i_emit(message) {
    this.emit(message);
  }
}
```

### Python Equivalent

```python
class World:
    @property
    def subject(self):
        """The current 'I' — object, NPC, or player."""
        return self.object or self.npc or self.player
    
    def i_have(self, item_id: str) -> bool:
        inv = self.subject.get('inventory', [])
        return item_id in inv
    
    def i_am(self, state_key: str) -> bool:
        return self.subject.get('state', {}).get(state_key) == True
    
    def i_get(self, state_key: str):
        return self.subject.get('state', {}).get(state_key)
    
    def i_set(self, state_key: str, value):
        state = self.subject.setdefault('state', {})
        state[state_key] = value
    
    def i_say(self, message: str):
        self.emit(f"{self.subject.get('name')}: \"{message}\"")
    
    def i_emit(self, message: str):
        self.emit(message)
    
    # ... etc
```

---

## Natural Language Compilation

The LLM compiles natural language to `i_` calls:

```yaml
# Natural language
guard: "I have the key and I am not cursed"

# Compiled
guard_js: (world) => world.i_have("key") && !world.i_have_buff("cursed")
guard_py: lambda world: world.i_have("key") and not world.i_have_buff("cursed")
```

```yaml
# Natural language (object context)
simulate: |
  if I am lit and fuel > 0:
    consume 1 fuel
    if fuel reaches 0:
      I am no longer lit
      say "The lamp dies!"

# Compiled
simulate_js: (world) => {
  if (world.i_am("lit") && world.i_get("fuel") > 0) {
    world.i_set("fuel", world.i_get("fuel") - 1);
    if (world.i_get("fuel") <= 0) {
      world.i_set("lit", false);
      world.i_emit("The lamp dies!");
    }
  }
}
```

---

## The `i_` vs `world.` Split

| Use `i_` when... | Use `world.` when... |
|------------------|----------------------|
| Acting as current subject | Accessing global state |
| Checking own inventory | Checking adventure flags |
| Modifying own state | Navigating rooms |
| Speaking in first person | Managing party |

```javascript
// Mixed example
if (i_have("key") && world.flag("door_visible")) {
  i_say("I can unlock this door!");
  world.set_flag("door_unlocked", true);
}
```

---

## Benefits

1. **Readable** — `i_have("key")` reads like English
2. **Context-aware** — "I" shifts naturally
3. **Object-oriented** — Objects think for themselves
4. **Compilable** — LLM can translate natural language easily
5. **Debuggable** — Clear who is speaking in logs

---

## Protocol Symbol

```
SUBJECTIVE-ORIENTED — The "I" shifts based on who is speaking
```
