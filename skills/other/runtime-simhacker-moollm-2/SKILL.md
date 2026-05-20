---
name: runtime
description: Dual Python/JavaScript adventure runtimes — always in sync
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: DUAL-RUNTIME
tags: [moollm, runtime, python, javascript, compilation, sync]
related: [context, adventure, object, expression]
adversary: single-target
---

# Runtime

> *"Test in Python, deploy to browser. Same semantics, both targets."*
> — Vanessa Freudenberg (memorial voice)

---

## What Is It?

The **Runtime** skill defines the dual Python/JavaScript adventure engines. Both runtimes:

- Execute compiled expressions
- Manage world state
- Process simulation ticks
- Handle events

**CRITICAL:** We ALWAYS generate BOTH `_js` AND `_py` code. Never one without the other.

---

## Why Dual Runtimes?

| Runtime | Purpose |
|---------|---------|
| **Python** | Server-side, testing, LLM tethering, CLI |
| **JavaScript** | Browser, standalone play, offline |

```yaml
# Dual Runtime Architecture
dual_runtime:
  source: "YAML"
  compiler: "LLM"
  outputs:
    guard_js: "(world) => ..."
    guard_py: "lambda world: ..."
  
  runtimes:
    python:
      file: "adventure.py"
      targets: ["CLI", "Server"]
    javascript:
      file: "engine.js"
      targets: ["Browser", "SPA"]
```

---

## The World Object

Both runtimes implement identical `World` classes:

### Python

```python
class World:
    """Adventure runtime context for Python."""
    
    def __init__(self, adventure_data: dict):
        # Standard keys
        self.turn = 0
        self.timestamp = None
        self.adventure = adventure_data
        self.player = adventure_data.get('player', {})
        self.room = None
        self.party = adventure_data.get('party', {})
        
        # Extended keys (set contextually)
        self.object = None   # During object simulation
        self.target = None   # During targeted action
        self.npc = None      # During NPC simulation
        
        # Skill state namespaces
        self.skills = DotDict()  # world.skills.economy.gold
        
    # INVENTORY
    
    def has(self, item_id: str) -> bool:
        return item_id in self.player.get('inventory', [])
        
    def has_tag(self, tag: str) -> bool:
        """Check if player has any item with the given tag."""
        for item_id in self.player.get('inventory', []):
            item = self.get_object(item_id)
            if item and tag in item.get('tags', []):
                return True
        return False
        
    def find_by_tag(self, tag: str, in_room: bool = True) -> list:
        """Find all objects with the given tag."""
        results = []
        # Check inventory
        for item_id in self.player.get('inventory', []):
            item = self.get_object(item_id)
            if item and tag in item.get('tags', []):
                results.append(item)
        # Check current room
        if in_room and self.room:
            for obj in self.room.get('objects', []):
                if tag in obj.get('tags', []):
                    results.append(obj)
        return results
        
    def give(self, item_id: str):
        inv = self.player.setdefault('inventory', [])
        inv.append(item_id)
        
    def take(self, item_id: str):
        inv = self.player.get('inventory', [])
        if item_id in inv:
            inv.remove(item_id)
            
    # FLAGS
    
    def flag(self, name: str) -> bool:
        return self.adventure.get('flags', {}).get(name, False)
        
    def set_flag(self, name: str, value: bool):
        flags = self.adventure.setdefault('flags', {})
        flags[name] = value
        
    # NARRATIVE
    
    def emit(self, message: str):
        self._output_queue.append(message)
        
    def narrate(self, message: str, style: str = "normal"):
        self._output_queue.append({'text': message, 'style': style})
        
    # EVENTS
    
    def trigger_event(self, name: str, data: dict = None):
        self._event_queue.append({'name': name, 'data': data or {}})
        
    # NAVIGATION
    
    def go(self, destination: str):
        self._pending_navigation = destination
        
    def can_go(self, direction: str) -> bool:
        exits = self.room.get('exits', {})
        return direction in exits
        
    # BUFFS
    
    def has_buff(self, buff_id: str) -> bool:
        buffs = self.player.get('buffs', [])
        return any(b.get('id') == buff_id for b in buffs)
        
    def add_buff(self, buff: dict):
        buffs = self.player.setdefault('buffs', [])
        buffs.append(buff)
        
    def remove_buff(self, buff_id: str):
        buffs = self.player.get('buffs', [])
        self.player['buffs'] = [b for b in buffs if b.get('id') != buff_id]
        
    # EFFECTIVE VALUES (Buff Modification Protocol)
    #
    # Base value = persistent truth
    # Effective value = recalculated each tick
    #
    # "The base value is truth. The effective value is reality."
    #
    
    def reset_effective(self, obj: dict = None):
        """
        Reset all effective values to their base values.
        Called at the start of each tick.
        """
        obj = obj or self.object
        if not obj or 'state' not in obj:
            return
        
        state = obj['state']
        for key in list(state.keys()):
            if not key.endswith('_effective'):
                effective_key = f"{key}_effective"
                state[effective_key] = state[key]
                
    def get_effective(self, obj: dict, prop: str):
        """Get effective value, falling back to base if not set."""
        state = obj.get('state', {})
        effective_key = f"{prop}_effective"
        if effective_key in state:
            return state[effective_key]
        return state.get(prop)
        
    def modify_effective(self, obj: dict, prop: str, delta):
        """Add delta to effective value."""
        state = obj.get('state', {})
        effective_key = f"{prop}_effective"
        state[effective_key] = state.get(effective_key, state.get(prop, 0)) + delta
        
    def multiply_effective(self, obj: dict, prop: str, factor: float):
        """Multiply effective value by factor."""
        state = obj.get('state', {})
        effective_key = f"{prop}_effective"
        state[effective_key] = state.get(effective_key, state.get(prop, 0)) * factor
    
    # RESILIENCE (SimCity Zone Pattern)
    #
    # WILL WRIGHT: "If one tile burns but the center survives,
    #               the zone will eventually rebuild."
    #
    
    def ensure_defaults(self, obj: dict = None) -> dict:
        """
        Ensure object has its default state values.
        Self-initializing: creates state if missing.
        Self-healing: clamps invalid values.
        """
        obj = obj or self.object
        if not obj:
            return {}
        
        # Create state if missing
        if 'state' not in obj:
            obj['state'] = {}
        
        # Merge defaults
        defaults = obj.get('defaults', {})
        for key, default_val in defaults.items():
            if key not in obj['state']:
                obj['state'][key] = default_val
        
        return obj['state']
        
    def heal_state(self, obj: dict = None):
        """
        Fix inconsistent state values.
        - Clamp negative numbers to 0
        - Fix logical inconsistencies
        """
        state = self.ensure_defaults(obj)
        
        # Clamp numeric values to non-negative
        for key, val in list(state.items()):
            if isinstance(val, (int, float)) and val < 0:
                state[key] = 0
                
        return state
    
    # STATE ACCESS
    
    def get(self, path: str):
        """Get value by dot path: world.get('object.state.fuel')"""
        parts = path.split('.')
        obj = self
        for part in parts:
            if isinstance(obj, dict):
                obj = obj.get(part)
            else:
                obj = getattr(obj, part, None)
            if obj is None:
                return None
        return obj
        
    def set(self, path: str, value):
        """Set value by dot path: world.set('object.state.lit', True)"""
        parts = path.split('.')
        obj = self
        for part in parts[:-1]:
            if isinstance(obj, dict):
                obj = obj.setdefault(part, {})
            else:
                obj = getattr(obj, part)
        if isinstance(obj, dict):
            obj[parts[-1]] = value
        else:
            setattr(obj, parts[-1], value)
```

### JavaScript

```javascript
class World {
  /** Adventure runtime context for JavaScript. */
  
  constructor(adventureData) {
    // Standard keys
    this.turn = 0;
    this.timestamp = null;
    this.adventure = adventureData;
    this.player = adventureData.player || {};
    this.room = null;
    this.party = adventureData.party || {};
    
    // Extended keys (set contextually)
    this.object = null;   // During object simulation
    this.target = null;   // During targeted action
    this.npc = null;      // During NPC simulation
    
    // Skill state namespaces
    this.skills = {};     // world.skills.economy.gold
    
    // Internal queues
    this._outputQueue = [];
    this._eventQueue = [];
    this._pendingNavigation = null;
  }
  
  // === INVENTORY ===
  
  has(itemId) {
    return (this.player.inventory || []).includes(itemId);
  }
  
  hasTag(tag) {
    /** Check if player has any item with the given tag. */
    for (const itemId of this.player.inventory || []) {
      const item = this.getObject(itemId);
      if (item && (item.tags || []).includes(tag)) {
        return true;
      }
    }
    return false;
  }
  
  findByTag(tag, inRoom = true) {
    /** Find all objects with the given tag. */
    const results = [];
    // Check inventory
    for (const itemId of this.player.inventory || []) {
      const item = this.getObject(itemId);
      if (item && (item.tags || []).includes(tag)) {
        results.push(item);
      }
    }
    // Check current room
    if (inRoom && this.room) {
      for (const obj of this.room.objects || []) {
        if ((obj.tags || []).includes(tag)) {
          results.push(obj);
        }
      }
    }
    return results;
  }
  
  give(itemId) {
    this.player.inventory = this.player.inventory || [];
    this.player.inventory.push(itemId);
  }
  
  take(itemId) {
    const inv = this.player.inventory || [];
    const idx = inv.indexOf(itemId);
    if (idx > -1) inv.splice(idx, 1);
  }
  
  // === FLAGS ===
  
  flag(name) {
    return (this.adventure.flags || {})[name] || false;
  }
  
  setFlag(name, value) {
    this.adventure.flags = this.adventure.flags || {};
    this.adventure.flags[name] = value;
  }
  
  // === NARRATIVE ===
  
  emit(message) {
    this._outputQueue.push(message);
  }
  
  narrate(message, style = "normal") {
    this._outputQueue.push({ text: message, style });
  }
  
  // === EVENTS ===
  
  triggerEvent(name, data = {}) {
    this._eventQueue.push({ name, data });
  }
  
  // === NAVIGATION ===
  
  go(destination) {
    this._pendingNavigation = destination;
  }
  
  canGo(direction) {
    const exits = this.room?.exits || {};
    return direction in exits;
  }
  
  // === BUFFS ===
  
  hasBuff(buffId) {
    const buffs = this.player.buffs || [];
    return buffs.some(b => b.id === buffId);
  }
  
  addBuff(buff) {
    this.player.buffs = this.player.buffs || [];
    this.player.buffs.push(buff);
  }
  
  removeBuff(buffId) {
    const buffs = this.player.buffs || [];
    this.player.buffs = buffs.filter(b => b.id !== buffId);
  }
  
  // === EFFECTIVE VALUES (Buff Modification Protocol) ===
  //
  // Base value = persistent truth
  // Effective value = recalculated each tick
  //
  // "The base value is truth. The effective value is reality."
  //
  
  resetEffective(obj = null) {
    /**
     * Reset all effective values to their base values.
     * Called at the start of each tick.
     */
    obj = obj || this.object;
    if (!obj || !obj.state) return;
    
    const state = obj.state;
    for (const key of Object.keys(state)) {
      if (!key.endsWith('_effective')) {
        const effectiveKey = `${key}_effective`;
        state[effectiveKey] = state[key];
      }
    }
  }
  
  getEffective(obj, prop) {
    /** Get effective value, falling back to base if not set. */
    const state = obj.state || {};
    const effectiveKey = `${prop}_effective`;
    if (effectiveKey in state) {
      return state[effectiveKey];
    }
    return state[prop];
  }
  
  modifyEffective(obj, prop, delta) {
    /** Add delta to effective value. */
    const state = obj.state || {};
    const effectiveKey = `${prop}_effective`;
    state[effectiveKey] = (state[effectiveKey] ?? state[prop] ?? 0) + delta;
  }
  
  multiplyEffective(obj, prop, factor) {
    /** Multiply effective value by factor. */
    const state = obj.state || {};
    const effectiveKey = `${prop}_effective`;
    state[effectiveKey] = (state[effectiveKey] ?? state[prop] ?? 0) * factor;
  }
  
  // === RESILIENCE (SimCity Zone Pattern) ===
  //
  // WILL WRIGHT: "If one tile burns but the center survives,
  //               the zone will eventually rebuild."
  //
  
  ensureDefaults(obj = null) {
    /**
     * Ensure object has its default state values.
     * Self-initializing: creates state if missing.
     * Self-healing: clamps invalid values.
     */
    obj = obj || this.object;
    if (!obj) return {};
    
    // Create state if missing
    obj.state = obj.state || {};
    
    // Merge defaults
    const defaults = obj.defaults || {};
    for (const [key, defaultVal] of Object.entries(defaults)) {
      if (!(key in obj.state)) {
        obj.state[key] = defaultVal;
      }
    }
    
    return obj.state;
  }
  
  healState(obj = null) {
    /**
     * Fix inconsistent state values.
     * - Clamp negative numbers to 0
     * - Fix logical inconsistencies
     */
    const state = this.ensureDefaults(obj);
    
    // Clamp numeric values to non-negative
    for (const [key, val] of Object.entries(state)) {
      if (typeof val === 'number' && val < 0) {
        state[key] = 0;
      }
    }
    
    return state;
  }
  
  // === STATE ACCESS ===
  
  get(path) {
    const parts = path.split('.');
    let obj = this;
    for (const part of parts) {
      obj = obj?.[part];
      if (obj === undefined) return undefined;
    }
    return obj;
  }
  
  set(path, value) {
    const parts = path.split('.');
    let obj = this;
    for (const part of parts.slice(0, -1)) {
      obj[part] = obj[part] || {};
      obj = obj[part];
    }
    obj[parts[parts.length - 1]] = value;
  }
}
```

---

## Compiled Expression Format

Natural language compiles to BOTH targets:

```yaml
# Source
guard: "player has brass-key AND room is not dark"

# Generated (BOTH always!)
guard_js: (world) => world.has("brass-key") && !world.room.is_dark
guard_py: lambda world: world.has("brass-key") and not world.room.is_dark
```

### Expression Types

| Type | JavaScript | Python |
|------|------------|--------|
| boolean | `(world) => ...` | `lambda world: ...` |
| action | `(world) => { ... }` | `def action(world): ...` |
| method | `(world, arg) => { ... }` | `def method(world, arg): ...` |
| closure | `(world) => { ... }` | `def closure(world): ...` |

### Complex Example: Object Methods

```yaml
# Source
methods:
  consume_fuel: "reduce fuel by amount, minimum 0"
  extinguish: "set lit to false, emit darkness event"

# Generated
methods_js:
  consume_fuel: (world, amount = 1) => {
    world.object.state.fuel = Math.max(0, world.object.state.fuel - amount);
  }
  extinguish: (world) => {
    world.object.state.lit = false;
    world.emit("Darkness falls.");
    world.triggerEvent("DARKNESS");
  }

methods_py:
  consume_fuel: |
    def consume_fuel(world, amount=1):
        world.object.state['fuel'] = max(0, world.object.state['fuel'] - amount)
  extinguish: |
    def extinguish(world):
        world.object.state['lit'] = False
        world.emit("Darkness falls.")
        world.trigger_event("DARKNESS")
```

---

## Simulation Loop

Both runtimes implement the same simulation loop with **effective value phases**:

```yaml
# Simulation tick phases
simulation_tick:
  - phase: 1. RESET
    action: "foo_effective = foo (reset to base)"
  - phase: 2. BUFFS
    action: "Apply buff modifiers to _effective values"
  - phase: 3. SIMULATE
    action: "Objects run simulate(), modify _effective"
  - phase: 4. MAIL
    action: "Deliver queued messages (deterministic!)"
  - phase: 5. EVENTS
    action: "Process event queue"
  - phase: 6. NAVIGATE
    action: "Move player if requested"
  - phase: 7. DISPLAY
    action: "UI shows _effective with base comparison"
```

### Phase 4: MAIL — Deterministic Message Delivery

Messages are queued during simulation, then delivered deterministically:

```python
# PHASE 4: Deliver mail (no LLM needed!)
for message in world.skills.postal.get('outgoing', []):
    routing = message.get('routing')
    
    # Transfer attachments
    for transfer in routing.get('attachments_transfer', []):
        if transfer['action'] == 'send':
            move_item(world, transfer['ref'], 
                     from_path=transfer['from_inventory'],
                     to_path=transfer['to_inventory'])
    
    # Deliver to inbox
    if routing['delivery_point'] == 'inbox':
        add_to_inbox(world, routing['inbox_path'], message)
    
    # Update status
    message['status'] = 'delivered'
    message['delivered'] = world.timestamp
    
    # Trigger events (goal completion, etc)
    for trigger in routing.get('triggers', []):
        world.trigger_event(trigger['event'], trigger['data'])

world.skills.postal['outgoing'] = []
```

See [skills/postal/ROUTING.md](../postal/ROUTING.md) for full routing documentation.

```python
# Python
def tick(world: World):
    world.turn += 1
    world.timestamp = datetime.now().isoformat()
    
    # PHASE 1: Reset all effective values to base
    for obj in world.room.get('objects', []):
        world.reset_effective(obj)
    world.reset_effective(world.player)
    
    # PHASE 2: Apply buffs
    for buff in world.player.get('buffs', []):
        if buff.get('effect_py'):
            exec(buff['effect_py'])(world)
        # Decrement duration, remove expired buffs
        if buff.get('duration'):
            buff['duration'] -= 1
    world.player['buffs'] = [b for b in world.player.get('buffs', []) 
                             if b.get('duration', 1) > 0]
    
    # PHASE 3: Simulate all objects in current room
    for obj in world.room.get('objects', []):
        if obj.get('simulate_py'):
            world.object = obj
            exec(obj['simulate_py'])(world)
            world.object = None
            
    # PHASE 4: Process event queue (actions)
    for event in world._event_queue:
        handle_event(world, event)
    world._event_queue.clear()
    
    # Process navigation
    if world._pending_navigation:
        navigate(world, world._pending_navigation)
        world._pending_navigation = None
```

```javascript
// JavaScript
function tick(world) {
  world.turn += 1;
  world.timestamp = new Date().toISOString();
  
  // PHASE 1: Reset all effective values to base
  for (const obj of world.room?.objects || []) {
    world.resetEffective(obj);
  }
  world.resetEffective(world.player);
  
  // PHASE 2: Apply buffs
  for (const buff of world.player.buffs || []) {
    if (buff.effect_js) {
      buff.effect_js(world);
    }
    // Decrement duration
    if (buff.duration !== undefined) {
      buff.duration -= 1;
    }
  }
  // Remove expired buffs
  world.player.buffs = (world.player.buffs || [])
    .filter(b => (b.duration ?? 1) > 0);
  
  // PHASE 3: Simulate all objects in current room
  for (const obj of world.room?.objects || []) {
    if (obj.simulate_js) {
      world.object = obj;
      obj.simulate_js(world);
      world.object = null;
    }
  }
  
  // PHASE 4: Process event queue (actions)
  for (const event of world._eventQueue) {
    handleEvent(world, event);
  }
  world._eventQueue = [];
  
  // Process navigation
  if (world._pendingNavigation) {
    navigate(world, world._pendingNavigation);
    world._pendingNavigation = null;
  }
}
```

---

## Testing Parity

Both runtimes should produce identical results:

```python
# Test in Python
def test_lamp_simulation():
    world = World(load_adventure())
    world.room = load_room("start/")
    lamp = find_object(world, "brass-lantern")
    
    lamp.state = {"lit": True, "fuel": 2}
    world.object = lamp
    
    # Tick 1: fuel 2 → 1
    exec(lamp.simulate_py)(world)
    assert lamp.state["fuel"] == 1
    
    # Tick 2: fuel 1 → 0, lamp goes out
    exec(lamp.simulate_py)(world)
    assert lamp.state["fuel"] == 0
    assert lamp.state["lit"] == False
    assert "GRUE_APPROACHES" in [e["name"] for e in world._event_queue]
```

Same test runs in JavaScript:

```javascript
// Test in JavaScript
function testLampSimulation() {
  const world = new World(loadAdventure());
  world.room = loadRoom("start/");
  const lamp = findObject(world, "brass-lantern");
  
  lamp.state = { lit: true, fuel: 2 };
  world.object = lamp;
  
  // Tick 1: fuel 2 → 1
  lamp.simulate_js(world);
  assert(lamp.state.fuel === 1);
  
  // Tick 2: fuel 1 → 0, lamp goes out
  lamp.simulate_js(world);
  assert(lamp.state.fuel === 0);
  assert(lamp.state.lit === false);
  assert(world._eventQueue.some(e => e.name === "GRUE_APPROACHES"));
}
```

---

## Protocol Symbol

```
DUAL-RUNTIME — Python + JavaScript, always in sync
```
