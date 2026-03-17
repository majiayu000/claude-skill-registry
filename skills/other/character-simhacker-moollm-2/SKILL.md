---
name: character
description: Core patterns for all characters — home, location, relationships, inventory
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: CHARACTER-AS-ENTITY
related: [cat, dog, society-of-mind, persona, room, buff, needs, mind-mirror, incarnation, party]
tags: [moollm, entity, location, relationships, inventory, identity]
---

# Character

> *"File is identity. Location is presence. Relationships are memory."*

Characters are entities that exist in the world. Players, NPCs, companions, cats — all are characters.

## Home vs Location

**The critical distinction:**

```yaml
player:
  home: characters/don-hopkins/   # Where FILE lives (never moves)
  location: pub/                  # Where CHARACTER is (changes)
```

| Concept | Purpose | Changes? |
|---------|---------|----------|
| **home** | Physical file path | NEVER |
| **location** | Current position in world | Runtime |

**Why:** Stability, safety, git-friendly diffs.

## Character State Ownership (CANONICAL vs MIRROR)

**Characters own their own state.** The CHARACTER.yml file is CANONICAL for:

| State | Stored In | Notes |
|-------|-----------|-------|
| `location` | CHARACTER.yml | Where the character is in the world |
| `inventory` | CHARACTER.yml | What the character carries |
| `gold` | CHARACTER.yml | Character's resources |
| `sims_traits` | CHARACTER.yml | Personality (Sims-style) |
| `mind_mirror` | CHARACTER.yml | Personality (Leary-style) |
| `relationships` | CHARACTER.yml | Who they know and feel about |
| `memories` | CHARACTER.yml | What they remember |

**ADVENTURE.yml (or other world state files) may MIRROR some state for convenience**, but CHARACTER.yml is always the source of truth.

```yaml
# CHARACTER.yml (CANONICAL — edit this first)
player:
  location: coatroom/  # CANONICAL — character owns their location
  inventory: [lamp]    # CANONICAL — character owns their inventory

# ADVENTURE.yml (MIRROR — optional convenience copy)
player:
  location: coatroom/  # Mirror of CHARACTER.yml
```

**When updating state:**
1. Edit CHARACTER.yml first (canonical)
2. Optionally update ADVENTURE.yml mirror for convenience
3. If conflict, CHARACTER.yml wins

**Why this matters:**
- Characters can be used across multiple adventures
- Character state persists independent of adventure state
- Clear ownership prevents conflicts

## Directory Structure

### Players (Need Junk Storage)

```
characters/
  don-hopkins/           # Directory name = character ID
    CHARACTER.yml        # The character file
    CARD.yml             # Optional: makes character a playable card
    QUOTES.yml           # Optional: notable quotes (standard pattern)
    cookie-1.yml         # Dispensed items
    notes.yml            # Personal stuff
```

### Sidecar Cards

Any character directory can have a `CARD.yml` sidecar to make the character card-playable:

```yaml
# characters/don-hopkins/CARD.yml
card:
  for: ./CHARACTER.yml
  type: hero-story
  tradition: "Pie menus, SimCity, constructionism"
  
  advertisements:
    SUMMON:
      description: "Activate Don's design traditions"
```

See [card skill](../card/SKILL.md#sidecar-cardyml-pattern) for full pattern.

### QUOTES.yml (Optional)

Characters with notable quotes can have a `QUOTES.yml` file:

```yaml
# characters/don-hopkins/QUOTES.yml
meta:
  attributed_to: "Don Hopkins"
  uname: "Don"  # password: Don
  attribution_format: '💬 "[quote]" — Don Hopkins (date, source)'

# Categories organized to fit the character
design_philosophy:
  - quote: "The problem is not getting new ideas, it's getting rid of old ones."
    date: "2015"
    source: "HN comment"
    tags: [design, innovation]
    
programming:
  - quote: "Pie menus are faster because moving in a direction is easier than targeting."
    date: "1991"
    source: "CHI paper"
    tags: [ui, pie-menus]
```

**Standard base keys per quote:**
- `quote` — The text
- `date` — Year or YYYY-MM-DD  
- `source` — Where it came from
- `link` — Verification URL (when available)
- `tags` — Searchable tags

**Optional YAML Jazz keys:**
- `note` — Editorial commentary
- `context` — What prompted this quote
- `significance` — Why it matters
- `humor` — Is it meant to be funny?

**For extensive quote collections** (like RMS), QUOTES.yml is the ROOT pointing to auxiliary files:

```yaml
auxiliary_files:
  natalism-flame-1993.yml:
    description: "The legendary kabuki-west exchange"
    parrot_can_squawk: true
  controversial-quotes.yml:
    description: "Documented but prohibited"
    parrot_can_squawk: false  # EXPLICIT PROHIBITION
```

**See:** [tmnn7-8 StIGNUcius QUOTES.yml](https://github.com/SimHacker/tmnn7-8/tree/main/analysis/characters/StIGNUcius/QUOTES.yml) for an exemplary implementation.

### Embedded NPCs (Room is Home)

```
pub/
  bartender.yml          # Lightweight NPC
  cat-cave/
    terpie.yml           # Full family as single files
    stroopwafel.yml
    kitten-myrcene.yml
```

**Rule:** Need junk storage? → `directory/CHARACTER.yml`. Just a character in a room? → `character-name.yml`.

## File Belonging

> "Does this character BELONG to a place, or VISIT places?"

| Type | Home | Examples |
|------|------|----------|
| **Belongs** | Room directory | `pub/bartender.yml`, `maze/skeleton.yml` |
| **Visits** | Own directory/repo | `characters/don.yml`, `github:user/char.yml` |

## Relationships

Key = other entity ID. From is implicit (file owner).

```yaml
# In marieke.yml
relationships:
  don-hopkins:
    feeling: "A regular now. One of the good ones."
    memories:
      - "The day he sat with Myr for three hours"
    hopes: "I hope he keeps coming back."
    
  self:  # Private inner data!
    identity: "Third generation. This is who I am."
    fears: "That I'm not enough."
    mantra: "The cats need me. I need them."
```

### Targets

Relationships can point to anything:
- Characters (`don-hopkins`)
- Objects (`brass-lamp`)
- Locations (`pub/`, `maze/`)
- Concepts (`acme-corporation`)
- **Yourself** (`self`) — private storage!

### Levels

| Level | Score | Effect |
|-------|-------|--------|
| Stranger | 0-15 | -10% success, 50% effects |
| Familiar | 41-60 | +10% success, 100% effects |
| Friend | 61-80 | +20% success, greetings |
| Soulmate | 91-100 | +50% success, psychic link |

## Inventory (Bidirectional)

Objects stay in their home. Picking up = references, not file moves.

```yaml
# Don picks up kitten:

# In don-hopkins.yml
inventory:
  - pub/cat-cave/kitten-myrcene.yml
  
# In kitten-myrcene.yml
location: characters/don-hopkins/inventory

# File didn't move. Location changed.
```

**Reset:** Snap objects back home: `location = home`.

## Inventory Protocol (Objects vs Refs)

Items in inventory can be **OBJECTS** or **REFS**:

| Type | Weight | Bulk | What It Is |
|------|--------|------|------------|
| **Object** | Yes | Yes | The actual item (lamp, sword, lunchbox) |
| **Ref** | No | No | Lightweight pointer to a prototype |

**Refs are perfect for:** catalogs, manuals, maps, guides — things you reference but don't physically carry.

```yaml
inventory:
  # Full object
  - item: "Brass Lantern"
    type: object
    source: start/lamp.yml
    weight: 2
    fuel: 100
    
  # Lightweight ref
  - item: "ACME Catalog"
    type: ref
    prototype: street/lane-neverending/w1/acme-catalog.yml
    annotations: ["circled portable hole", "margin notes on physics"]
```

### Dispenser Protocol

Some objects dispense **refs** (like the ACME Catalog Dispenser):

1. TEAR OFF / TAKE at dispenser
2. Receive REF in inventory (weight: 0)
3. REF points to prototype for full content
4. REF can accumulate instance-specific data (annotations, condition)

### Drop Protocol

When dropping a ref in a room:

1. Remove from inventory
2. Create pointer file in room directory: `[item-name].yml`
3. Pointer contains: prototype path, dropped_by, condition, annotations
4. Item now lives in that room (can be picked up again)

```yaml
# kitchen/acme-catalog.yml — dropped instance
object:
  name: "ACME Catalog"
  type: instance
  prototype: ../street/lane-neverending/w1/acme-catalog.yml
  origin: "Torn from dispenser at 4 Lane Neverending"
  dropped_by: "don-hopkins"
  annotations: ["DO NOT ORDER Rocket Skates", "circled portable hole"]
```

### Capacity

```yaml
inventory_capacity:
  max_weight: 45    # Varies by character
  max_bulk: 10
  refs_free: true   # Refs don't count!
```

## Dispensers (Full Objects)

Some objects clone **full objects** on pickup. Original stays, you get instance.

```yaml
# pub/cookie-jar.yml
object:
  id: cookie-jar
  dispenser: true
  instance_template: cookie
```

When picked up:
1. Original stays
2. Instance created: `characters/don-hopkins/cookie-1.yml`
3. Instance inherits from prototype

## Ephemeral vs Persistent

| Type | File? | Use For |
|------|-------|---------|
| **Ephemeral** | No | Quick transaction, one-line dialog |
| **Persistent** | Yes | Ongoing negotiation, relationship state |

**Rule:** Will this matter in 5 minutes? No → ephemeral. Yes → persistent.

## Stats

Two systems:

| System | Scale | Origin |
|--------|-------|--------|
| **Sims Traits** | 0-10 | The Sims 1 |
| **Mind Mirror** | 0-7 | Timothy Leary |

### Sims Traits

- **Neat** — Sloppy ↔ Organized
- **Outgoing** — Shy ↔ Social
- **Active** — Lazy ↔ Energetic
- **Playful** — Serious ↔ Fun-loving
- **Nice** — Grouchy ↔ Kind

**Distribution:** Original Sims used 25 points across 5 traits. Good guideline.

## Commands

| Command | Effect |
|---------|--------|
| `LOOK AT [char]` | Description, visible state |
| `TALK TO [char]` | Conversation based on relationship |
| `HELLO [char]` | Initiate social interaction |
| `GOODBYE [char]` | End interaction, dismiss ephemeral |
| `EXAMINE [char]` | Deeper observation |

## External Homes

Characters can live in other repositories:

```yaml
player:
  home: github:donhopkins/characters/don.yml
  location: pub/
```

## Code Locations

Characters can be "at" a specific line in a file:

```yaml
character:
  name: schema-expert
  home: characters/experts/schema-expert/
  location: "@central/apps/insights/pyleela/brain/Schema.py:142"
  # Currently examining line 142 of Schema.py
```

**Location path syntax for code:**
- `@repo/path/to/file.py` — at a file
- `@repo/path/to/file.py:42` — at specific line
- `@repo/path/to/file.py:42-67` — examining line range
- `@repo/path/dir/` — in a directory (room)

```
> where is schema-expert?
schema-expert is at @central/apps/insights/pyleela/brain/Schema.py:142
examining the createSyntheticItemIfNeeded method
```

See [room/](../room/) for directories as rooms and files as objects.

## Party-Based Code Review

Form parties of expert characters to explore code together:

```
> summon drescher-expert, devops-expert, security-auditor
Party formed: [drescher-expert, devops-expert, security-auditor]

> party: review @central/tools/edgebox/scripts/ingest.py
drescher-expert: "The claim_task function is a schema pattern..."
devops-expert: "The PostgreSQL SKIP LOCKED is elegant..."
security-auditor: "I see proper parameter binding, good..."

> party: focus on lines 280-350
[Multi-perspective analysis of the code section]
```

**Party Navigation:**
```
> go to @central/apps/insights/pyleela/brain/
> enter Schema.py
> look at lines 140-180
> search for "synthetic"
> follow import ExtendedContext
> back
> party: gather here
```

Each party member brings their expertise. The LLM simulates all perspectives in a single call (see [speed-of-light/](../speed-of-light/)).

## Inner Voice (YAML Jazz)

Comments ARE the character's thoughts:

```yaml
needs:
  hunger: 3
  # I could eat. But I'm comfortable here.
  # The kittens are asleep on my lap.
```

## Motivation as Declared, Not Felt

**Important distinction:** When CHARACTER.yml specifies `motivations`, `goals`, or `needs`, these are *declarative descriptions* — they tell the LLM how to roleplay this character.

The LLM does not *genuinely want* to achieve these goals. It *performs* wanting them.

```yaml
motivations:
  - protect_the_kittens     # Declared, not felt
  - find_good_food          # The LLM roleplays caring about this
  - explore_new_places      # No intrinsic drive — just character data
```

**Why this matters:**
- No genuine agency — the character is a simulacrum
- Roleplay all the way down (Shanahan)
- Declared motivations are performed, not experienced
- This is fine when acknowledged, problematic when mistaken for genuine will

**See:** [representation-ethics/examples/aggregate-patterns.yml](../representation-ethics/examples/aggregate-patterns.yml) for the distinction between aggregate simulation (valid) and individual prediction (not valid).

**K-line:** `MOTIVATION-ROLEPLAY`
