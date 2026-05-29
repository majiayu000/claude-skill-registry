---
name: inventory
description: "You carry pointers. When you set them down, they become real."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - list_dir
  - delete_file
related: [character, object, room, container, prototype, postal, logistic-container]
tags: [moollm, inventory, carrying, boxing, reference, fungible]
credits:
  - "Will Wright — The Sims (routing slots, object advertisements)"
  - "Wube Software — Factorio (logistic inventory, fungible stacks)"
  - "David Ungar & Randall Smith — Self language (prototype references)"
---

# INVENTORY

> **"Carry pointers or values. Set them down, they become real."**

The universal protocol for carrying, storing, and transferring objects.
Applies to ANY container: characters, bags, rooms, artifacts, vehicles.

---

## Files in This Skill

- `SKILL.md` — Full protocol documentation (this file)
- `README.md` — Human landing page
- `CARD.yml` — Interface definition
- `INVENTORY.yml.tmpl` — Standalone inventory template

---

## Core Philosophy

**Inventory holds two kinds of things: POINTERS and VALUES.**

Your character's home directory is their "bag." Items in it are:

| Type | Weight | What You Have |
|------|--------|---------------|
| **Pointer** | 0 | Reference to where something lives |
| **Value** | varies | Text, number, array, object, subtree |
| **Object** | item.weight | Deep copy of the actual thing |
| **Fungible** | per-item | Stack with count, no individual tracking |

**Pointers are lightweight:** You don't carry the brass lantern. You carry a *path* to where it lives.

**Values are direct:** You can also carry raw text, numbers, arrays, entire subtrees — any YAML/JSON value.

When you drop either kind, it gets **boxed** into a YAML file with its own existence.

---

## Universal Application

Inventory applies to ANY container, not just characters:

| Container | Has Inventory? | Example |
|-----------|---------------|---------|
| **Character** | ✓ | Palm's backpack |
| **Bag** | ✓ | Bag of holding |
| **Room** | ✓ (implicit) | Objects in the pub |
| **Chest** | ✓ | Treasure chest contents |
| **Vehicle** | ✓ | Cargo hold |
| **Artifact** | ✓ | Ring with stored spell |

**Embedding inventory:**

```yaml
# In CHARACTER.yml (most common)
inventory:
  refs:
    - pub/bar/brass-lantern.yml
  fungibles:
    - { proto: economy/gold.yml, count: 500 }

# Or standalone INVENTORY.yml for any container
# bag-of-holding/INVENTORY.yml
inventory:
  refs:
    - kitchen/cookie-jar.yml#cookie
    - street/acme-catalog.yml
  objects:
    - { id: magic-sword, name: "Vorpal Blade", weight: 3 }
```

---

## Reference Types

References can point into ANY file type. A reference is just a string that locates something.

### Pointer Syntax

| Syntax | Points To | Example |
|--------|-----------|---------|
| `path/to/file.yml` | Whole YAML file | `pub/cookie-jar.yml` |
| `file.yml#id` | Section by id | `pub/cookie-jar.yml#cookie` |
| `file.yml#parent.child` | Nested path | `seating.yml#bar.stool-1` |
| `file.md#heading` | Markdown heading | `characters/README.md#doctor-no` |
| `file.json#/json/path` | JSON pointer | `config.json#/settings/defaults` |
| `file.ext?search=pat` | Search pattern | `npcs.yml?name=Henk` |
| `file.cpp:42` | Line number | `engine.cpp:142` |
| `file.py:10-25` | Line range | `adventure.py:100-150` |

**The pointer is the reference.** It can point to:
- A prototype in a YAML file
- A section embedded in a larger file
- A heading in a markdown document
- A JSON field
- Even a line in source code

### Unified Addressing

This pointer syntax is shared across ALL systems:

| System | Uses Pointers For |
|--------|-------------------|
| **Inventory** | What you carry (`refs:`) |
| **Location** | Where you are (`location:`) |
| **Postal** | Where to deliver mail (`to:`) |
| **Structural Editing** | Where to PEEK/POKE |

Same syntax, everywhere. Mail a letter to a function. Stand on a JSON key. POKE a value into a YAML path. It's all the same address space.

**Not all addresses make sense — but they're all valid.** You can stand on `package.json#/devDependencies/vitest`. Weird? Sure. Works? Yes.

### Reference Structure

Simple reference (just a string):
```yaml
inventory:
  refs:
    - pub/bar/brass-lantern.yml
    - street/acme-catalog.yml#portable-hole
```

Rich reference (with metadata):
```yaml
inventory:
  refs:
    - ref: pub/bar/brass-lantern.yml
      acquired: "2026-01-23T10:00:00Z"
      condition: "good"
      note: "Found in the cellar"
```

---

## Location as Pointer (Code as Space)

**The pointer syntax is bidirectional.** Not just "what you carry" — also "where you ARE."

Any object's `location:` field uses the same pointer syntax. This means characters, artifacts, and entities can exist *inside* any file type:

```yaml
# Character standing on a TypeScript function
name: Alice
location: src/lib/utils.ts#fetchData
note: "Reviewing this function with the team"

# Artifact placed at a specific line range
name: Bug Marker
location: src/auth/login.ts:45-67
note: "The authentication bug lives here"

# Entity inside a JSON config
name: Config Watcher
location: package.json#/dependencies/svelte
note: "Monitoring version changes"
```

### Code Review as Adventure

A hacking party can literally stand inside source code:

```yaml
# The review party
participants:
  - { name: Alice, location: "src/api/handler.ts#processRequest" }
  - { name: Bob, location: "src/api/handler.ts#validateInput" }
  - { name: Carol, location: "src/api/handler.ts:89-95" }  # The problematic lines

session:
  topic: "Why does validation fail on unicode input?"
  room: "src/api/handler.ts"
  context: "Standing around the processRequest function"
```

### What This Enables

| Use Case | Location Pointer |
|----------|------------------|
| **Code review** | Stand on functions, discuss them |
| **Bug hunting** | Place markers at suspicious lines |
| **Pair programming** | Multiple characters at same location |
| **Architecture tours** | Walk through a codebase as rooms |
| **Documentation** | Annotate code with character observations |

**The codebase becomes a dungeon.** Files are rooms. Functions are objects. Line ranges are specific spots. Characters can go there, look around, leave notes, argue about what they see.

---

## Pickup Modes

Two fundamentally different ways to pick something up:

### TAKE REF — Lightweight Pointer

```
> TAKE REF TO brass-lantern
You now have a reference to the brass lantern. (weight: 0)
```

**What happens:**
1. Create pointer in your inventory
2. Object stays where it is
3. Object's `location` field updates: `location: "characters/don/inventory"`
4. You have zero weight added

**Use when:**
- Just need access to it
- Don't want to carry weight
- Shared resource (dispenser, catalog)
- Can't physically move it (too heavy)

### TAKE OBJECT — Deep Copy

```
> TAKE OBJECT cookie
You pick up the cookie. (weight: 0.1)
```

**What happens:**
1. Copy entire object into your inventory
2. Your file gets bigger (embedded object)
3. Weight added to your load
4. Original MAY stay or be deleted (your choice)

**Use when:**
- Small object, negligible weight
- Want to OWN it completely
- Need to modify it freely
- Don't want inheritance chain

### Picking Up Boxed Items

**GOLDEN RULE: Once boxed, always boxed.**

If something already has a file (is "boxed"), picking it up preserves everything:

```yaml
# kitchen/acme-catalog-001.yml already exists with:
#   inherits: street/acme-catalog.yml
#   annotations: ["circled portable hole"]
#   dropped_by: palm

# Don picks it up AS OBJECT:
# File moves to: characters/don/acme-catalog-001.yml
# All annotations preserved!

# Don picks it up AS REF:
# inventory: [ref: "kitchen/acme-catalog-001.yml"]
# File stays in kitchen, Don just has pointer.
```

---

## Drop Modes

Three fundamentally different ways to put something down:

### DROP AS BOX — Create New File

```
> DROP brass-lantern AS BOX
Created: kitchen/brass-lantern-001.yml
```

**What happens:**
1. Create new YAML file at destination
2. New file `inherits:` from your ref's target
3. Adds boxed metadata (who, when, where)
4. You can KEEP your original ref (sharing) or consume it
5. Boxed item now has its own existence and local state

**Boxing creates an instance:**
```yaml
# kitchen/brass-lantern-001.yml
object:
  inherits: "pub/bar/brass-lantern.yml"
  
  # Instance metadata
  instantiated_at: "2026-01-23T14:00:00Z"
  instantiated_by: "don"
  instantiated_from: "inventory"
  
  # Local state (can now diverge from prototype)
  condition: "slightly worn"
  inscribed: "Property of Don"
```

### DROP AS BEAM — Move Actual File

```
> DROP brass-lantern AS BEAM
File moved to: garden/brass-lantern.yml
```

**What happens:**
1. Actual file relocates to destination
2. No inheritance created
3. All properties preserved (it's the same file)
4. You NO LONGER have it
5. Origin is now empty (file moved)

**Use when:**
- Giving something away permanently
- Moving heavy objects
- Avoiding inheritance chains
- The thing should BE here now

### DROP INTO — Insert in Container List

```
> DROP cookie INTO treasure-chest
Cookie added to treasure-chest.yml contents list.
```

**What happens:**
1. Target file has a list (contents, items, inventory)
2. Your item inserted into that list
3. No new file created
4. Packed storage in existing file

**Container file structure:**
```yaml
# treasure-chest.yml
object:
  name: "Treasure Chest"
  contents:
    - { id: gold-coins, proto: economy/gold.yml, count: 100 }
    - { id: ruby, name: "Ruby", weight: 0.5 }
    - ref: magic-scroll.yml   # ← your item inserted here
```

---

## Boxing Protocol

**Boxing (like Java boxing) — instantiating a pointer into a real file with identity.**

When you have a lightweight pointer and DROP AS BOX, the reference gets **boxed** — instantiated into a YAML file that inherits from the pointer's target. Like Java's `int` → `Integer`, but here it's `pointer` → `YAML file with identity`.

### The Journey of an Object

```yaml
# THE JOURNEY OF A CATALOG:

# 1. ORIGIN: street/acme-catalog.yml (prototype, dispenser)

# 2. DON TAKES REF at street:
don.inventory: [ref → street/acme-catalog.yml]
# (No file created yet, just pointer)

# 3. DON DROPS AS BOX in kitchen:
# Creates: kitchen/acme-catalog-001.yml
#   inherits: street/acme-catalog.yml
#   boxed_by: don, annotations: ["circled hole"]
# Don's ref is consumed.

# 4. PALM TAKES AS OBJECT from kitchen:
# File moves: palm.inventory/acme-catalog-001.yml
# All annotations preserved!
# Kitchen is now empty.

# 5. PALM DROPS AS BEAM in study:
# File moves: study/acme-catalog-001.yml
# Still has Don's annotations!
# Palm no longer has it.

# 6. BUMBLEWICK TAKES AS REF from study:
bumblewick.inventory: [ref → study/acme-catalog-001.yml]
# File stays in study.

# 7. BUMBLEWICK DROPS AS BOX in garden:
# Creates: garden/acme-catalog-002.yml
#   inherits: study/acme-catalog-001.yml
#   boxed_by: bumblewick, annotations: ["added doodles"]
# Now there are TWO catalogs:
#   - study/acme-catalog-001.yml (Don's original box)
#   - garden/acme-catalog-002.yml (Bumblewick's copy)

# Full provenance chain preserved at every step!
```

### Boxing Golden Rules

1. **Once boxed, always boxed** — Instances travel intact
2. **Instances accumulate history** — Each handler can add provenance
3. **Inheritance chains** — Instances can inherit from instances
4. **Local state divergence** — Instances can override their prototype

---

## Transport Modes

For heavy objects you can't carry:

### BEAM / TRANSPORTER

Use a reference as a targeting system:

```
> TAKE REF TO grand-piano
You have a reference to the grand piano. (weight: 0)

> GO concert-hall
You arrive at the concert hall.

> BEAM grand-piano HERE
*shimmer* Piano materialized!
concert-hall/grand-piano.yml created.
```

**How it works:**
1. Take lightweight REF to heavy object
2. Travel to destination (carrying only the pointer)
3. BEAM command uses ref as target
4. Object teleported/moved to your location
5. Ref consumed, you have actual object here

### FORKLIFT Mode

Mechanical assistance for moving heavy objects:

```
> SUMMON FORKLIFT
Forklift arrives.

> LOAD bronze-statue ONTO forklift
Statue loaded.

> GO garden
You move to garden, forklift follows.

> UNLOAD bronze-statue AS BEAM
Statue placed in garden/bronze-statue.yml
```

---

## Fungibles

Fungible items are **identical and interchangeable**. No individual tracking — just a count.

**Counts can be fractional!** 3.5 gold coins, 0.25 moolah, 2.7 kg of flour — why not?

### Fungible Stack Structure

```yaml
inventory:
  fungibles:
    - { proto: economy/gold.yml, count: 500 }
    - { proto: economy/moolah.yml, count: 3.50 }      # Fractional!
    - { proto: food/cookie.yml, count: 12 }
    - { proto: food/flour.yml, count: 2.7, unit: kg } # Continuous
    - { proto: materials/iron-ore.yml, count: 45, quality: high }
```

### Operations

| Operation | Command | Effect |
|-----------|---------|--------|
| Add | Pick up 100 gold | `gold.count += 100` |
| Remove | Pay 50 gold | `gold.count -= 50` |
| Split | Split pile | Create two stacks from one |
| Merge | Combine piles | Add counts together |

### FUNGIFY — Convert to Stack

```
> FUNGIFY gold-pile
3 unique gold coins → 1 fungible stack (count: 3)
WARNING: Individual properties lost!
```

**What you lose:**
- Individual conditions (fair, good, mint)
- Unique properties (rare, cursed)
- Provenance (who owned it before)
- Sentimental value

**Partial FUNGIFY:**
```
> FUNGIFY gold-pile KEEPING rare
2 coins fungified, 1 rare coin kept unique.
```

### UNFUNGIFY — Create Individuals

```
> UNFUNGIFY gold COUNT 5
5 gold coins created as individual items.
Each can now have unique properties.
```

---

## Dispensers

A dispenser lets you TAKE copies without depleting the original.

| Type | What You Get | Example |
|------|--------------|---------|
| **Ref Dispenser** | Lightweight pointer | Catalog rack, brochure stand |
| **Instance Dispenser** | New object file | Cookie jar, vending machine |
| **Fungible Dispenser** | Add to stack | Gold pile, ore vein |

**Dispenser config:**
```yaml
object:
  name: "Cookie Jar"
  type: dispenser
  
  dispenser_config:
    mode: instance       # ref | instance | fungible
    template: cookie     # What to dispense
    stock: 12            # null = infinite
    respawn: daily       # How stock replenishes
    
  templates:
    cookie:
      name: "Cookie"
      prototype: food/cookie.yml
      weight: 0.1
```

---

## Stamp Pads

Refs as instance factories — like Factorio blueprints.

```yaml
stamp_pad:
  prototype: furniture/chair.yml
  mode: counted           # counted | unlimited | charged
  uses_remaining: 10
  
  instance_defaults:
    condition: new
    placed_by: "{player.name}"
```

**Stamping:**
```
> SELECT chair-stamp
Chair Stamp selected. [10 remaining]

> STAMP AT corner
*plop* Chair appears in corner.
corner/stamped-chair-001.yml created.
[9 remaining]
```

---

## Structural Editing

The pointer syntax is a **universal structural editing protocol** for YAML and JSON. Same addressing, same operations, syntax-independent.

### The Insight

If you can TAKE a subtree, you can PEEK at it.
If you can DROP a subtree, you can POKE it.
If you can move subtrees between files, you can edit structure.

**Pointers are addresses. Addresses enable operations.**

### Operations

| Operation | Command | Effect |
|-----------|---------|--------|
| **PEEK** | `PEEK path#key.subkey` | Read value at path |
| **POKE** | `POKE path#key.subkey = value` | Write value at path |
| **SNIP** | `SNIP path#subtree` | Extract subtree (leaves hole) |
| **PULL** | `PULL path#subtree` | Extract into inventory or new file |
| **SPLICE** | `SPLICE value INTO path#list` | Insert into list/array |
| **APPEND** | `APPEND value TO path#list` | Add to end of list |
| **SET** | `SET path#key = value` | Create or overwrite key |
| **DELETE** | `DELETE path#key` | Remove key entirely |
| **CLEAR** | `CLEAR path#key` | Set to null/empty |
| **DUPLICATE** | `DUPLICATE path#subtree TO path2#newkey` | Copy subtree |
| **MOVE** | `MOVE path#subtree TO path2#newkey` | Relocate subtree |

### Examples

```yaml
# PEEK — read a value
> PEEK config.yml#settings.timeout
30

# POKE — write a value  
> POKE config.yml#settings.timeout = 60
Done.

# SNIP — extract and remove
> SNIP characters.yml#npcs.henk
Henk extracted to inventory. (hole left in npcs)

# PULL — extract to file
> PULL characters.yml#npcs.henk TO henk.yml
Created henk.yml with Henk's data.

# SPLICE — insert into list
> SPLICE {name: "Cookie", weight: 0.1} INTO chest.yml#contents
Inserted at position 0.

# APPEND — add to end
> APPEND "new item" TO inventory.yml#refs
Added to refs list.

# SET — create or overwrite
> SET room.yml#visited = true
Set visited to true.

# DELETE — remove key
> DELETE character.yml#temp_data
Removed temp_data.

# DUPLICATE — copy subtree
> DUPLICATE template.yml#npc_base TO characters.yml#npcs.bob
Bob created from npc_base template.

# MOVE — relocate subtree
> MOVE old.yml#settings TO new.yml#config
Settings moved from old.yml to new.yml#config.
```

### Syntax Independence

These operations work identically on YAML and JSON:

| Source | Target | Works? |
|--------|--------|--------|
| YAML | YAML | ✓ |
| JSON | JSON | ✓ |
| YAML | JSON | ✓ (auto-convert) |
| JSON | YAML | ✓ (auto-convert) |

**The pointer addresses structure, not syntax.** The underlying tree is the same whether serialized as YAML or JSON.

### Nested Paths

```yaml
# Deep addressing
> PEEK game.yml#characters.party.members[0].inventory.weapons[2]
"Vorpal Sword"

# Wildcards for bulk operations
> DELETE config.yml#users.*.temp_tokens
Deleted temp_tokens from all users.

# Conditional addressing
> PEEK npcs.yml#[?(@.faction=="rebels")]
[all NPCs where faction is "rebels"]
```

### Atomic Operations

For complex edits, use transactions:

```yaml
# BEGIN/COMMIT for atomic multi-step edits
> BEGIN EDIT game.yml
> SET #player.health = 100
> APPEND "heal-potion" TO #player.inventory
> DELETE #player.status.poisoned
> COMMIT
Atomic edit applied.

# ROLLBACK on failure
> BEGIN EDIT game.yml
> SET #player.gold = -500  # Invalid!
> ROLLBACK
Edit cancelled.
```

### Integration with Inventory

Structural editing IS inventory manipulation:

| Inventory Action | Structural Equivalent |
|-----------------|----------------------|
| TAKE REF | PEEK (get address) |
| TAKE OBJECT | SNIP (extract copy) |
| DROP AS BOX | PULL to new file |
| DROP INTO | SPLICE/APPEND |
| BEAM | MOVE |

**Same protocol, different metaphors.** Characters "pick up" and "drop" things. Editors "snip" and "splice" structure. Both are moving subtrees via pointers.

---

## Commands

| Command | Action |
|---------|--------|
| `TAKE [item]` | Pick up (default: smart mode) |
| `TAKE REF TO [item]` | Pick up as pointer |
| `TAKE OBJECT [item]` | Pick up as deep copy |
| `DROP [item]` | Put down (default: smart mode) |
| `DROP [item] AS BOX` | Create new file with inheritance |
| `DROP [item] AS BEAM` | Move actual file |
| `DROP [item] INTO [container]` | Insert into list |
| `BEAM [item] TO [dest]` | Teleport without carrying |
| `INVENTORY` | List carried items |
| `CAPACITY` | Show limits and usage |
| `FUNGIFY [pile]` | Convert to fungible stack |
| `UNFUNGIFY [stack]` | Convert to individual items |

---

## Smart Defaults

When you don't specify mode, the system chooses:

**TAKE defaults:**
| Situation | Default Mode |
|-----------|--------------|
| From dispenser | REF (repeatable) |
| Boxed item | OBJECT (preserve annotations) |
| Heavy item | REF (can't carry) |
| Small unique item | OBJECT (don't leave behind) |

**DROP defaults:**
| Situation | Default Mode |
|-----------|--------------|
| Have reference | BOX (create instance) |
| Have object, giving away | BEAM (transfer) |
| Have object, sharing | BOX (keep original) |
| In your own space | BEAM (organizing) |

---

## Weight and Capacity

```yaml
capacity:
  max_weight: 45        # Total carrying capacity
  max_bulk: 10          # Volume limit
  refs_free: true       # References don't count!
  
  current:
    weight: 12          # Sum of objects
    bulk: 3
    refs: 15            # Unlimited pointers
```

**Why refs are free:** A reference is just a string — a path to something. It costs nothing to carry a path. The weight only comes when you carry the actual thing.

---

## Dovetails With

- **[../character/](../character/)** — Characters have inventories
- **[../object/](../object/)** — Objects can be items or containers
- **[../room/](../room/)** — Rooms implicitly contain objects
- **[../container/](../container/)** — Container abstraction
- **[../prototype/](../prototype/)** — References point to prototypes
- **[../postal/](../postal/)** — Mail delivery uses inventory transfer
- **[../logistic-container/](../logistic-container/)** — Factorio-style logistics
- **[../buff/](../buff/)** — Temporary effects on items
- **[../economy/](../economy/)** — Currency as fungible inventory

---

## Protocol Symbols

| Symbol | Meaning |
|--------|---------|
| `INVENTORY` | Invoke this skill |
| `TAKE-REF` | Lightweight pointer pickup |
| `TAKE-OBJECT` | Deep copy pickup |
| `DROP-BOX` | Create inheriting file |
| `DROP-BEAM` | Move actual file |
| `FUNGIFY` | Convert to stack |
| `BOXING` | Pointer → instance (like Java boxing) |
| `TRANSPORTER` | Move without carrying |

---

*"Pointers and values — carry them light, drop them real."*
