---
name: buff
description: Temporary effects system — curses are just shitty buffs
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: BUFF-AS-MODIFIER
related: [simulation, time, needs, character, cat, dog, persona, yaml-jazz]
tags: [moollm, effects, curses, stats, game, modifiers]
target: character  # ONLY characters, never rooms
---

# Buff

> *"All effects are buffs. Some are just shitty."*

Buffs modify stats, abilities, or behavior. They have durations, can stack, and come from various sources. **Curses are just negative buffs** — no separate system.

## Characters Only

**Buffs only target characters.** This is a design constraint, not a limitation.

- Single closure signature: `(world, subject, verb, object)`
- `subject` is always a character — no type checking needed
- Rooms that need buffs get a "room spirit" character

```yaml
# Room needs to be "haunted"? Create its spirit.
character:
  id: dark-cave-spirit
  name: "Spirit of the Dark Cave"
  location: room/dark-cave
  buffs:
    - ref: buff/haunted
```

## Structure

```yaml
buff:
  name: "Caffeinated"
  source: "Espresso"
  effect: { energy: +2, focus: +1 }
  duration: 5  # simulation turns
  stacks: false
```

| Field | Purpose |
|-------|---------|
| `name` | Display name |
| `source` | What granted this buff |
| `effect` | Stat mods OR semantic prompt |
| `duration` | How long it lasts |
| `stacks` | Can multiple instances exist? |
| `max_stacks` | If stacking, limit |
| `decay` | How it ends (time, action, condition) |

## Buff Types

### Numeric
Traditional stat modifiers:
```yaml
buff:
  name: "Caffeinated"
  effect: { energy: +2, focus: +1 }
  duration: 5
```

### Semantic
Arbitrary effect prompts interpreted by the LLM — not predefined stats, just vibes:

- "feeling lucky"
- "cats seem to like you today"
- "slightly cursed"
- "radiating calm energy"
- "shadows feel watchful"

**How it works:**
```
Buff: "cats seem to like you today"
Action: PAT TERPIE
LLM: Gives bonus, narrates extra warmth
```

### Mixed
Combine numeric and semantic:
```yaml
buff:
  name: "Terpie's Blessing"
  effect:
    calm: +2
    vibe: "cats trust you more"
  duration: "a while"
```

## Standard Properties Buffs Affect

### Player/NPC Stats (Sims-Style Needs)

```yaml
# Numeric needs — decay over time, restored by actions
needs:
  hunger: 80      # 0=starving, 100=full
  energy: 65      # 0=exhausted, 100=rested
  social: 45      # 0=lonely, 100=connected
  hygiene: 90     # 0=filthy, 100=clean
  bladder: 30     # 0=desperate, 100=empty
  fun: 55         # 0=bored, 100=entertained
  comfort: 70     # 0=miserable, 100=cozy
```

### Mind-Mirror Stats (Cognitive/Emotional)

```yaml
# Mental state — affects decision-making and narration
mind:
  focus: 75       # Concentration (0-100)
  mood: 20        # Emotional valence (-100 to +100)
  stress: 35      # Anxiety level (0-100)
  creativity: 60  # Creative capacity (0-100)
  confidence: 50  # Self-assurance (0-100)
  patience: 40    # Frustration tolerance (0-100)
  curiosity: 80   # Exploration drive (0-100)
```

### Room Spirit Stats

Room spirits are characters whose stats affect the room they haunt:

```yaml
character:
  id: forge-spirit
  name: "Spirit of the Forge"
  location: room/blacksmith-forge
  
  # These stats affect everyone in the room
  production_speed: 120   # +20% crafting speed
  error_rate: 8           # 8% chance of mistakes
  mood_influence: +5      # Slight pride boost
  comfort_bonus: -10      # Hot and uncomfortable
  discovery_chance: 15    # Sometimes find rare materials
  danger_level: 25        # Burns, sparks, accidents
  
  buffs:
    - id: master-craftsman-blessing
      source: "Pleased the forge spirit"
      effect: { production_speed: +30, error_rate: -5 }
      duration: "until you leave"
```

| Spirit Stat | What It Does | Example Buff Effect |
|-------------|--------------|---------------------|
| `production_speed` | Work/craft rate | Blessing: +30% faster |
| `error_rate` | Mistake probability | Curse: +20% more errors |
| `mood_influence` | Mood granted to visitors | Haunting: -15 mood |
| `comfort_bonus` | Comfort modifier | Cozy: +20 comfort |
| `discovery_chance` | Finding hidden things | Mysterious: +25% |
| `danger_level` | Hazard intensity | Cursed: traps more deadly |

## Sources

| Source | Example |
|--------|---------|
| Interactions | Petting a cat grants joy |
| Consumables | Coffee grants energy |
| Locations | Being in pub grants comfort |
| Items | Lit lamp grants grue immunity |
| Relationships | High friendship grants trust |
| Personas | Wearing persona grants themed buffs |

## Lifecycle Hooks

Three hooks control buff behavior, written as natural language and compiled to JS:

| Hook | → Compiles To | Purpose |
|------|---------------|---------|
| `start` | `start_js` | Runs when buff activates |
| `simulate` | `simulate_js` | Runs each tick while active |
| `is_finished` | `is_finished_js` | Returns `true` → buff ends |

### Example: Poison Buff

```yaml
buff:
  id: poison
  name: "Poisoned"
  tags: [curse, damage-over-time, dispellable]
  
  # Natural language prompts (author writes these)
  start: "Mark character as poisoned, turn them slightly green"
  simulate: "Reduce HP by 1, chance of groaning sound"
  is_finished: "Return true after 5 ticks OR if HP drops below 10"
  
  # Compiled by buff compiler (generated)
  start_js: |
    subject.poisoned = true;
    subject.tint = 'green';
  simulate_js: |
    subject.hp -= 1;
    if (Math.random() < 0.3) world.emit('*groan*');
  is_finished_js: |
    return subject.poisonTicks >= 5 || subject.hp < 10;
```

### Closure Signature

All compiled hooks use the same signature:

```javascript
(world, subject, verb, object) => { ... }
```

- `world` — shared game state (never null)
- `subject` — the character with the buff (never null for buffs)
- `verb` — context-dependent (may be null)
- `object` — context-dependent (may be null)

**Body-only in YAML**: Write just the code body, engine wraps it.

## Buff Interactions

Buffs can look up and modify other buffs by tag:

| Interaction | Effect | Example |
|-------------|--------|---------|
| `cancels` | Remove buffs with these tags | Antidote cancels `[poison]` |
| `boosts` | Multiply/extend buffs with tags | Fire spell boosts `[fire]` x2 |
| `replaces` | Remove old, add this | Drunk replaces `[tipsy]` |
| `merges_with` | Combine into new buff | Rage + Focus → Battle Trance |
| `blocked_by` | Can't apply if these exist | Poison blocked by `[immunity-poison]` |
| `counters` | Weaken/shorten these buffs | OJ counters `[hangover]` |
| `countered_by` | These weaken/shorten this | Couch-lock countered by `[citrus]` |

### Cancel Example

```yaml
buff:
  id: cleanse
  name: "Cleanse"
  tags: [holy, dispel]
  cancels: [curse, poison, disease]  # Remove all matching
  start: "Holy light purges dark afflictions"
```

### Boost Example

```yaml
buff:
  id: fire-attunement
  name: "Fire Attunement"
  boosts:
    tags: [fire]
    multiplier: 2.0
    extend_duration: 5
  start: "Fire spells burn twice as hot"
```

### Merge Example

```yaml
buff:
  id: rage
  name: "Rage"
  tags: [combat, aggression]
  merges_with:
    tags: [focus, discipline]
    result: battle-trance  # Creates new combined buff
    
buff:
  id: battle-trance
  name: "Battle Trance"
  tags: [combat, legendary]
  effect: { damage: +50%, focus: +30, pain_immunity: true }
  start: "Fury and focus unite — you become a weapon"
```

### Blocked By Example

```yaml
buff:
  id: poison
  name: "Poisoned"
  tags: [poison, damage-over-time]
  blocked_by: [immunity-poison, divine-protection]
  # Won't apply if target has these tags
```

## Weight Trees (ML-Style Mixtures)

Buffs can form hierarchical weighted mixtures, like neural network layers:

```
Blend → Strains → Terpenes → Effects
  ↓        ↓          ↓          ↓
weights  weights    weights    final
  ↑        ↑          ↑          ↑
 BUFFS   BUFFS      BUFFS     BUFFS   ← Each stage can be modified by buffs!
```

**Meta-buffs can modify the weight tree itself:**

| Buff | Affects | Example |
|------|---------|---------|
| `tolerance` | Strain weights | Regular use → diminishing returns |
| `sensitivity` | Terpene weights | First time → effects amplified |
| `synergy-boost` | Effect weights | Entourage → all effects +20% |
| `citrus-clarity` | Specific terpenes | Limonene effects doubled |
| `indica-affinity` | Strain category | Indica strains hit harder |

### Tolerance Relationships

Tolerances use the **character relationship map** — same system as NPC friendships:

```yaml
character:
  id: player
  name: "Don"
  
  # Relationships include people AND substances
  # Terpenes are unidirectional — they don't have feelings back
  relationships:
    # NPCs (bidirectional)
    bob: { trust: 45, friendship: 60 }
    alice: { trust: 80, friendship: 75 }
    
    # Terpene tolerances (unidirectional — no reciprocal)
    terpene/myrcene: { tolerance: 45 }      # Couch-lock less effective
    terpene/limonene: { tolerance: 12 }     # Citrus hits hard
    terpene/pinene: { tolerance: 30 }
    terpene/linalool: { tolerance: 5 }      # Lavender knocks you out
    terpene/caryophyllene: { tolerance: 60 } # Need more for pain relief
    terpene/humulene: { tolerance: 20 }
    terpene/terpinolene: { tolerance: 8 }   # Full creative boost
    terpene/ocimene: { tolerance: 3 }       # Maximum effect
```

**Key difference from NPC relationships:**

| Aspect | NPC Relationship | Terpene Relationship |
|--------|------------------|----------------------|
| Direction | Bidirectional | **Unidirectional** |
| Reciprocal | Bob likes you back | Myrcene has no feelings |
| Tracked on | Both characters | **Player only** |
| Decay | Neglect hurts both | Time heals tolerance |

**Tolerance mechanics:**

| Tolerance | Multiplier | Experience |
|-----------|------------|------------|
| 0 (virgin) | 1.5x | "Whoa, this is intense" |
| 25 (light) | 1.2x | "Nice, I feel it" |
| 50 (moderate) | 1.0x | "Standard effect" |
| 75 (heavy) | 0.7x | "Need more than usual" |
| 100 (maxed) | 0.4x | "Barely feel anything" |

**Tolerance changes:**

```yaml
# Each use increases tolerance
on_use:
  tolerance_gain: 2-5 points per use
  
# Tolerance decays over time (T-break!)
on_rest:
  tolerance_decay: 1 point per day of abstinence
  
# Full reset after extended break
t_break:
  duration: 2 weeks
  effect: "Reset to 50% of current tolerance"
```

**Effective weight calculation:**

```python
def get_effective_terpene_weight(character, terpene, base_weight):
    tolerance = character.tolerances.get(terpene, 0)
    
    # Convert tolerance to multiplier
    if tolerance < 25:
        multiplier = 1.5 - (tolerance / 50)  # 1.5x → 1.0x
    elif tolerance < 75:
        multiplier = 1.0 - ((tolerance - 50) / 100)  # 1.0x → 0.75x
    else:
        multiplier = 0.75 - ((tolerance - 75) / 100)  # 0.75x → 0.5x
    
    return base_weight * multiplier
```

### Layer 1: Terpenes → Effects

Each terpene has weighted effects:

```yaml
myrcene-blessing:
  effects_weighted:
    relaxation: { value: +30, weight: 1.0 }   # Full effect
    pain_relief: { value: +20, weight: 0.8 }  # 80%
    sedation: { value: +25, weight: 0.9 }     # 90%
```

### Layer 2: Strains → Terpenes

Each strain is a weighted mixture of terpenes:

```yaml
strain-og-kush:
  terpene_profile:
    myrcene: 0.35      # 35% of profile
    limonene: 0.25     # 25%
    caryophyllene: 0.20
    linalool: 0.10
    humulene: 0.10
```

### Layer 3: Blends → Strains

Blends mix multiple strains:

```yaml
blend-wake-and-bake:
  strain_mixture:
    sour-diesel: 0.50     # Half the blend
    jack-herer: 0.30      # 30%
    pineapple-express: 0.20
```

### Computing Final Effects

```python
# Blend → Strain → Terpene → Effect propagation
def compute_blend_effects(blend):
    final_terpenes = {}
    
    # Layer 3→2: Blend weights × Strain terpene profiles
    for strain_id, strain_weight in blend.strain_mixture.items():
        strain = get_strain(strain_id)
        for terpene, terpene_weight in strain.terpene_profile.items():
            final_terpenes[terpene] += strain_weight * terpene_weight
    
    # Layer 2→1: Terpene amounts × Effect weights
    final_effects = {}
    for terpene, amount in final_terpenes.items():
        terpene_buff = get_terpene_buff(terpene)
        for effect, config in terpene_buff.effects_weighted.items():
            final_effects[effect] += amount * config.weight * config.value
    
    return final_effects
```

### Example Calculation

```
Wake & Bake Blend:
├── Sour Diesel (50%)
│   ├── limonene: 0.30 × 0.50 = 0.15
│   └── pinene: 0.15 × 0.50 = 0.075
├── Jack Herer (30%)
│   ├── limonene: 0.20 × 0.30 = 0.06
│   └── pinene: 0.25 × 0.30 = 0.075
└── Pineapple Express (20%)
    ├── limonene: 0.30 × 0.20 = 0.06
    └── pinene: 0.25 × 0.20 = 0.05

Final limonene: 0.15 + 0.06 + 0.06 = 0.27
Final pinene: 0.075 + 0.075 + 0.05 = 0.20

Then: limonene × mood_boost, pinene × focus → final character effects
```

This is essentially **a mini neural network** where:
- Weights are terpene profiles and strain mixtures
- Activations are effect values
- Forward pass computes final buff effects

## Buff Orchestration (Simulation Loop)

The orchestrator runs buff rounds during simulation ticks:

### 1. Scan Phase

Orchestrator collects all active buffs across all characters:

```yaml
# Orchestrator builds active-buff manifest
active_buffs:
  - character: player
    buff_ref: "skills/buff/buffs/INDEX.yml#caffeinated"
    remaining: 6
    stacks: 2
    
  - character: player
    buff_ref: "skills/buff/buffs/INDEX.yml#high"
    remaining: 8
    stacks: 1
    
  - character: bob-npc
    buff_ref: "skills/buff/buffs/INDEX.yml#drunk"
    remaining: 4
    stacks: 1
```

### 2. Event Generation

Create buff-tick events with pointers:

```yaml
buff_round:
  tick: 42
  events:
    - type: buff-simulate
      character: player
      buff: caffeinated
      simulate_js: "subject.energy_effective += 20; subject.focus_effective += 15;"
      
    - type: buff-simulate  
      character: player
      buff: high
      simulate: "Deep thoughts about random topics, food cravings"
      simulate_js: "if (Math.random() < 0.3) world.emit('*ponders existence*');"
      
    - type: buff-simulate
      character: bob-npc
      buff: drunk
      simulate: "Occasional slurred speech, may say embarrassing things"
```

### 3. LLM Simulation Prompt

Orchestrator instructs LLM to enumerate and simulate:

```yaml
prompt: |
  BUFF ROUND — Tick 42
  
  Enumerate and simulate each active buff:
  
  1. PLAYER — Caffeinated (6 ticks remaining, 2 stacks)
     Effect: +20 energy, +15 focus per stack
     Simulate: Apply effects, note jitteriness if 2+ stacks
     
  2. PLAYER — High (8 ticks remaining)
     Effect: -25 stress, +20 creativity, +30 hunger
     Simulate: "Deep thoughts about random topics, food cravings"
     → Narrate any random musings or munchie urges
     
  3. BOB — Drunk (4 ticks remaining)
     Effect: +30 confidence, -25 focus, -30 judgement
     Simulate: "Occasional slurred speech, may say embarrassing things"
     → Decide if Bob says something regrettable this tick
  
  For each buff:
  - Apply stat modifications to _effective values
  - Run simulate behavior (chance-based events)
  - Check is_finished conditions
  - Decrement remaining duration
  - Remove expired buffs, trigger spawns_after
  
  Return updated character states and any narration.
```

### 4. Buff Lifecycle Per Tick

```
┌─────────────────────────────────────────────────────────────────┐
│                        BUFF TICK                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  For each character:                                             │
│    For each active buff:                                         │
│                                                                  │
│      1. APPLY EFFECTS                                            │
│         stat_effective += buff.effect × buff.stacks             │
│                                                                  │
│      2. RUN SIMULATE                                             │
│         Execute simulate_js OR let LLM interpret simulate       │
│         (chance-based events, narration, random behaviors)      │
│                                                                  │
│      3. CHECK IS_FINISHED                                        │
│         If is_finished_js returns true → mark for removal       │
│         If remaining <= 0 → mark for removal                    │
│                                                                  │
│      4. DECREMENT DURATION                                       │
│         remaining -= 1                                           │
│                                                                  │
│      5. HANDLE EXPIRATION                                        │
│         If marked for removal:                                   │
│           - Remove buff from character                           │
│           - Trigger spawns_after buffs (with delay/chance)      │
│           - Emit buff-expired event                              │
│                                                                  │
│      6. HANDLE INTERACTIONS                                      │
│         Check for cancels, boosts, replaces, merges             │
│         Apply buff-on-buff effects                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5. Compiled vs Interpreted

| Mode | When | How |
|------|------|-----|
| **Compiled** | `simulate_js` exists | Engine evals cached closure directly |
| **Interpreted** | Only `simulate` text | LLM reads prompt, narrates behavior |
| **Hybrid** | Both exist | JS runs effects, LLM narrates flavor |

```yaml
buff:
  id: drunk
  # LLM interprets this for narration
  simulate: "Occasional slurred speech, may say embarrassing things"
  # Engine runs this for mechanics
  simulate_js: |
    if (Math.random() < 0.2) {
      world.emit(subject.name + " slurs something incomprehensible");
    }
```

### 6. Attention Concentration (Time-Slicing)

The event-based design **concentrates LLM attention** on specific tasks:

```
┌──────────────────────────────────────────────────────────────────┐
│              LLM ATTENTION TIME-SLICING                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Instead of: "Simulate everything at once" (diffuse attention)   │
│                                                                   │
│  We do: Series of focused micro-tasks                            │
│                                                                   │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐          │
│  │ Buff 1  │ → │ Buff 2  │ → │ Buff 3  │ → │ Buff 4  │          │
│  │ PLAYER  │   │ PLAYER  │   │ BOB     │   │ ROOM    │          │
│  │ caffein │   │ high    │   │ drunk   │   │ haunted │          │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘          │
│       ↓             ↓             ↓             ↓                │
│   [focused]    [focused]    [focused]    [focused]               │
│   attention    attention    attention    attention               │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Why this works:**

| Problem | Solution |
|---------|----------|
| LLM loses track with many buffs | One buff at a time, clear context |
| Effects get confused/merged | Each buff isolated in its own slice |
| Hard to debug | Each event is traceable, logged |
| Inconsistent simulation | Same prompt structure every time |

**Iteration Pattern:**

```yaml
# Orchestrator feeds LLM one task at a time
iteration_1:
  focus: "PLAYER's Caffeinated buff"
  context: [player_state, buff_definition, tick_number]
  task: "Apply effects, check finish condition, narrate if needed"
  output: [updated_state, narration, events]
  
iteration_2:
  focus: "PLAYER's High buff"
  context: [player_state, buff_definition, tick_number]  
  task: "Apply effects, chance of munchies event, narrate thoughts"
  output: [updated_state, narration, events]
  
# ... and so on
```

**Benefits:**

1. **Focused attention** — LLM only thinks about one buff
2. **Predictable structure** — Same input/output format each time
3. **Debuggable** — Can trace exactly which buff caused what
4. **Parallelizable** — Independent buffs can run in parallel
5. **Interruptible** — Can pause/resume between iterations
6. **Cacheable** — Compiled `_js` buffs skip LLM entirely

**Speed-of-Light Compatible:**

This fits the [speed-of-light](../speed-of-light/) pattern — many focused micro-operations in a single LLM call, or batched across calls:

```yaml
# Single call, multiple focused tasks
prompt: |
  Process these buff events in sequence:
  
  [1/4] PLAYER — Caffeinated
  → Apply: energy +40, focus +30 (2 stacks)
  → Check: is_finished? No (6 remaining)
  → Output: state changes only
  
  [2/4] PLAYER — High  
  → Apply: stress -25, creativity +20, hunger +30
  → Simulate: "Deep thoughts" — roll for musing
  → Output: state + optional narration
  
  [3/4] BOB — Drunk
  → Apply: confidence +30, focus -25
  → Simulate: "Slurred speech" — roll for embarrassment
  → Output: state + optional narration
  
  [4/4] LIBRARY-SPIRIT — Haunted
  → Apply: error_rate +15, mood_influence -20
  → Simulate: "Poltergeist activity" — roll for book fall
  → Output: room effects + optional event
```

## Stacking

- **Same source:** Doesn't stack — refresh duration instead
- **Different sources:** Stack additively up to category limit

### Category Limits
```yaml
terpene_effects: 3
charm_effects: 5
consumable_effects: 4
negative_effects: 3  # 3+ same negative = LEGENDARY
```

### Synergies
Some buffs COMBINE into stronger effects:
- Myr + Lily = "Sedation Stack"
- Lemon + Pine = "Focus Boost"
- All 8 kittens = "ENTOURAGE EFFECT" (legendary)

## Negative Buffs (Curses)

Curses are just shitty buffs. Same structure, negative effects.

```yaml
buff:
  name: "Scratched"
  source: "Failed BELLY RUB"
  effect: { hp: -1, visible_marks: true }
  duration: "Until healed"
```

### Persistent Curses
Long-term negative buffs with lift conditions:
```yaml
buff:
  name: "Curse of Darkness"
  effect: { lamp_efficiency: -25% }
  duration: conditional
  lift_condition: "Light 3 dark places"
  reward_on_lift: "LIGHT-BEARER title"
```

## Duration Types

| Type | Example |
|------|---------|
| Turns | `duration: 4` |
| Conditional | `duration: until you eat` |
| While present | `duration: while in pub` |
| Permanent | `duration: forever` |
| Natural language | `duration: a few minutes` |
| Probabilistic | `duration: 25% fade chance per turn` |

### Natural Language Durations

We're not tracking real time — the LLM interprets and makes its best guess:

- "forever"
- "5 minutes"
- "a day"
- "until sunset"
- "randomly 50%"
- "a while"
- "briefly"
- "until you forget"

See [time/](../time/) for full natural duration examples.

### Decay

When LLM judges turn(s) have passed:
1. Decrement duration on timed buffs
2. Remove buffs that hit 0
3. Apply new buffs from current turn

## Effective Derived Values: Flags Edition

This is the **effective derived values protocol** for booleans.

| Type | Base | Modifiers | Effective |
|------|------|-----------|-----------|
| **Numeric** | `energy: 5` | buff `+2` | `effective_energy: 7` |
| **Boolean** | `in_darkness: false` | room.lit=false, has_lamp=false | `effective_in_darkness: true` |

Same pattern:
- **Numeric:** base + sum(modifiers) = effective
- **Boolean:** base OR any(conditions) = effective flag

### Push / Pull / Latch

The LLM can handle any combination:

| Mode | Pattern | Example |
|------|---------|---------|
| **Pull** | Compute on demand | `in_darkness` derived from lamp + room state |
| **Push** | Source sets flag | Buff explicitly sets `urgent_situation: true` |
| **Latch** | Stays until cleared | `has_visited_room_a: true` persists |

```yaml
# PULL — derived on demand, not stored
in_darkness: (room.lit == false) AND (has_lamp == false)

# PUSH — buff explicitly sets
buff:
  sets_flags: [urgent_situation]

# LATCH — persists in state until cleared
player:
  visited_rooms: [room-a, room-b]  # grows, never shrinks
```

Traditional reactive systems pick one mode. The LLM does all three simultaneously — it sees the whole context and figures out which pattern applies.

### Tweening and Animation

Values don't have to snap — they can interpolate over time:

| Type | Instant | Tweened |
|------|---------|---------|
| **Numeric** | `energy: 5 → 7` | `energy: 5 → 7 over 3 turns` |
| **Boolean** | `lit: false → true` | `lit: fading in over 2 turns` |
| **Position** | `room-a → room-b` | `walking through hallway` |

```yaml
buff:
  name: "Warming Up"
  effect: { warmth: +3 }
  tween: ease-in    # Gradual increase
  duration: 5

animation:
  entering_room:
    from: hallway
    to: pub
    frames: [approaching, at_door, stepping_in, arrived]
```

The LLM narrates intermediate states. "You feel yourself warming up..." not just "You are warm now."

### Velocity

Any reactive variable can have a rate of change:

```yaml
energy:
  value: 5
  velocity: -1      # Draining 1 per turn
  
trust:
  value: 45
  velocity: +3      # Building rapport
  
mood:
  value: "content"
  velocity: "improving"  # Semantic velocity works too
```

| Variable | Value | Velocity | Meaning |
|----------|-------|----------|---------|
| `energy` | 5 | -1 | Tired and getting worse |
| `trust` | 45 | +3 | Relationship strengthening |
| `position` | room-a | north | Moving northward |
| `mood` | anxious | calming | Settling down |

The LLM reads velocity to predict and narrate: *"You're running low on energy and fading fast..."* vs *"Low energy but recovering."*

### Physics Simulation

Extend to full 2D/3D cartoon physics:

```yaml
thrown_ball:
  position: [5, 3]
  velocity: [2, 4]       # Moving up-right
  acceleration: [0, -1]  # Gravity pulling down
  
bouncing:
  elasticity: 0.8        # Loses 20% on bounce
  
cartoon_physics:
  hang_time: true        # Pause at apex
  squash_stretch: true   # Deform on impact
  delayed_fall: true     # Look down first, then fall
```

The LLM narrates physics with cartoon timing:

> *The ball arcs gracefully upward... hangs for a moment at the peak... 
> then plummets, SQUASHING flat against the floor before bouncing back 
> slightly less enthusiastically.*

Works for:
- Thrown objects (ball, inventory items)
- Character movement (jumping, falling, knockback)
- Environmental effects (swinging doors, rolling boulders)
- Looney Tunes logic (run off cliff, pause, look down, THEN fall)
- Temperature cooling or warming (ice cream melting, water freezing)

## Commands

| Command | Effect |
|---------|--------|
| `BUFFS` or `STATUS` | List active buffs with remaining duration |
| `EXAMINE [buff]` | Full details of buff source, effect, duration |
