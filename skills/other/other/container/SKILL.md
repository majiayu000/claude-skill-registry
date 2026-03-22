---
name: container
description: "Intermediate scope for inheritance — like OpenLaszlo's <node>"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [room, object, adventure, prototype, logistic-container]
tags: [moollm, scope, inheritance, hierarchy, composition]
---

# Container

> **Intermediate scopes that provide inheritance without being navigable rooms.**

Containers are directories that define shared properties for their children,
without themselves being places you can "go to."

## The OpenLaszlo Inspiration

In OpenLaszlo (Don Hopkins' earlier work!), `<node>` was a fundamental building block:

```xml
<!-- OpenLaszlo: <node> provides inheritance without visual layout -->
<node name="mazeDefaults">
  <attribute name="isDark" value="true"/>
  <attribute name="hasDanger" value="true"/>
</node>

<view extends="mazeDefaults">
  <!-- Inherits isDark, hasDanger -->
</view>
```

MOOLLM's `CONTAINER.yml` does the same for adventure directories:

```yaml
# maze/CONTAINER.yml
container:
  name: "The Twisty Maze"
  
  inherits:
    is_dark: true
    is_dangerous: true
    grue_rules:
      can_appear: true
```

All rooms inside `maze/` automatically inherit these properties!

---

## Container vs Room vs Meta

| Type | File | Navigable? | Inherits to children? |
|------|------|------------|----------------------|
| Room | `ROOM.yml` | ✅ Yes | ❌ No |
| Container | `CONTAINER.yml` | ❌ No | ✅ Yes |
| Meta | `.meta.yml` | ❌ No | ❌ No (just metadata) |

**Use Container when:**
- You want to define shared properties
- Children should inherit automatically
- The directory itself is not a place

**Use Room when:**
- The directory is a navigable location
- It has exits and can be entered

**Use .meta.yml when:**
- Just declaring "this is a system directory"
- No inheritance needed

---

## Inheritance Rules

### Cascade Down

Properties in `inherits:` flow to ALL descendants:

```
maze/
├── CONTAINER.yml       # inherits: { is_dark: true }
├── room-a/
│   └── ROOM.yml        # Inherits is_dark: true
├── room-b/
│   └── ROOM.yml        # Inherits is_dark: true
└── deep/
    └── CONTAINER.yml   # Can add MORE inherits
        └── room-c/
            └── ROOM.yml # Inherits from BOTH containers!
```

### Override by Redefining

Children can override inherited values:

```yaml
# maze/room-f/ROOM.yml
room:
  name: "The Treasure Chamber"
  is_dark: false  # Override! This room has magical light
```

### Merge, Don't Replace

For objects and arrays, inheritance MERGES:

```yaml
# maze/CONTAINER.yml
container:
  inherits:
    rules:
      - "Grues patrol in darkness"
      
# maze/room-g/ROOM.yml  
room:
  rules:
    - "This room has a pit trap"  # ADDS to inherited rules
```

Result: room-g has BOTH rules.

---

## Defaults vs Inherits

| Field | Purpose |
|-------|---------|
| `inherits` | Properties that children GET automatically |
| `defaults` | Values to use IF a child doesn't define them |

```yaml
container:
  # Every child room IS dark (forced)
  inherits:
    is_dark: true
    
  # If a room doesn't define atmosphere, use this
  defaults:
    room:
      atmosphere: "damp and musty"
```

---

## Use Cases

### Maze with Grue Rules

```yaml
# maze/CONTAINER.yml
container:
  name: "The Twisty Maze"
  description: "Passages all alike... or are they?"
  
  inherits:
    is_dark: true
    is_dangerous: true
    grue_rules:
      can_appear: true
      safe_with_light: true
      
  rules:
    - "No teleportation"
    - "Breadcrumbs disappear after 3 turns"
    - "Echoes alert nearby rooms"
    
  ambient:
    sound: "dripping water"
    smell: "wet stone"
    temperature: cold
```

### Animal Character Category

```yaml
# characters/animals/CONTAINER.yml
container:
  name: "Animal Characters"
  description: "Non-human beings with souls"
  
  inherits:
    type: animal
    has_instincts: true
    
  defaults:
    character:
      can_speak_human: false
      pet_able: true
      diet: omnivore
```

### Kitchen Appliances

```yaml
# kitchen/appliances/CONTAINER.yml
container:
  name: "Kitchen Appliances"
  
  inherits:
    type: appliance
    requires_power: true
    
  defaults:
    object:
      breakable: true
      fixable_with: "wrench"
```

---

## Resolution Order

When looking up a property:

1. **Self** — Check the object/room itself
2. **Parent Container** — Check `CONTAINER.yml` in parent dir
3. **Grandparent Container** — Keep going up
4. **Adventure Defaults** — `ADVENTURE.yml` defaults
5. **Prototype** — The skill template

```
maze/deep/room-c/ROOM.yml
    ↓ inherits from
maze/deep/CONTAINER.yml
    ↓ inherits from  
maze/CONTAINER.yml
    ↓ inherits from
ADVENTURE.yml (if it has defaults)
    ↓ inherits from
skills/room/ROOM.yml.tmpl
```

---

## Linter Behavior

The linter recognizes `CONTAINER.yml`:

```bash
📂 Phase 1: Discovery
   Found: 36 rooms, 54 objects, 6 characters
   Found: 2 containers  # NEW!
```

Containers suppress the "missing type declaration" warning:

```yaml
# Before: maze/ triggers warning
⚠️ Directory has room children but no ROOM.yml

# After: maze/CONTAINER.yml exists
✅ maze/ is a container (not a room)
```

---

## Related Patterns

- **Prototype Inheritance** (Self/JavaScript) — Objects inherit from prototypes
- **Lexical Scope** (Lisp/JavaScript) — Inner scopes access outer variables
- **Cascading** (CSS) — Styles flow from parent to child
- **XML Namespaces** — Context flows through the tree

---

## Credits

- **OpenLaszlo** — The `<node>` element as non-visual scope
- **Self** — Prototype inheritance without classes
- **CSS** — The cascade as inheritance mechanism
- **Don Hopkins** — For remembering OpenLaszlo! 🎉
