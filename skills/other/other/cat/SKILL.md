---
name: cat
description: Feline interactions, buffs, and relationship building
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: CAT
origin: "Tamagotchi, Harvest Moon, Stardew Valley, real cats"
related: [dog, character, buff, mind-mirror, room]
tags: [moollm, pet, companion, interaction, buff, feline]
---

# CAT — The Feline Interaction Skill

> *"Cats are the original NPCs. They have their own agenda."*

A generic skill for cat interactions that instances overlay with
their specific personalities, creating unique effects per cat.

Philosophy: Cats are not just decoration. They're gameplay.

invokes:
  - mind-mirror          # Personality determines effects
  - play-learn-lift      # Learn what each cat likes
  - procedural-rhetoric  # Cats teach through interaction

## INTERACTIONS — Universal Cat Actions

All interactions use Sims traits for success calculation. Each cat overlays
their personality to modify outcomes.

### TOUCH INTERACTIONS

#### PAT

```yaml
PAT:
  command: "PAT [cat]"
  duration: brief
  risk: low
  
  success_calculation: |
    success_chance = (cat.nice + cat.outgoing) / 20
    # Nice 8 + Outgoing 6 = 70% success
    
  outcomes:
    success:
      buff: "+1 Cheerful (5 min)"
      message: "*purrs briefly*"
    neutral:
      message: "*tolerates it*"
    failure:
      debuff: "-1 to next interaction with this cat"
      message: "*ear flicks irritably*"
```

#### SCRITCH

```yaml
SCRITCH:
  command: "SCRITCH [cat]"
  aliases: ["CHIN SCRATCH", "EAR SCRATCH"]
  requires_knowledge: true
  
  knowledge_sources:
    - "Previous interactions with this cat"
    - "Observing other NPCs interact"
    - "ASK MARIEKE ABOUT [cat]'s favorite spots"
    
  success_calculation: |
    base = (cat.nice + cat.playful) / 20
    if knows_preference: base += 0.3
    
  outcomes:
    success:
      buff: "+2 Cheerful, +1 Playful, cat remembers you"
      message: "*tilts head into the scritch* *motor purr activates*"
    wrong_spot:
      message: "*flinches* *gives you a look*"
      learning: "Now you know: not THAT spot"
```

#### BELLY_RUB — The Forbidden Zone

```yaml
BELLY_RUB:
  command: "RUB [cat]'S BELLY" 
  risk: HIGH
  
  base_effect: |
    The belly is a TRUST TEST. Most cats will trap and bite.
    Only attempt with very high Nice cats or established trust.
    
  success_calculation: |
    success_chance = (cat.nice - 5) / 10
    if cat.nice < 7: almost_guaranteed_failure
    
  outcomes:
    success:  # Rare!
      buff: "+5 bond with this cat, they follow you"
      message: "*exposes belly* *allows the forbidden touch* *purrs like a motorboat*"
    trap:  # Common
      damage: "1d4 scratch damage (cosmetic)"
      message: "*CLAMP* *bunny kicks* *you knew the risks*"
      learning: "Note: This cat is NOT a belly cat"
```

### PLAY INTERACTIONS

#### LASER_POINTER

```yaml
LASER_POINTER:
  command: "USE LASER POINTER"
  risk: none (physical)
  warning: |
    CAUTION: Some cats become OBSESSED.
    Always end with a "catch" (shining on a treat).
    Never just turn it off — causes existential cat crisis.
    
  outcomes:
    engagement:
      buff: "Tired cat = calm cat (+3 Calm later)"
      message: "*pupils dilate* *full hunting mode engaged*"
    obsession:  # High Restless cats
      duration: "Hours"
      message: "*still hunting* *where is it* *WHERE*"
```

### COMMUNICATION

#### SLOW_BLINK — The Feline I-Love-You

```yaml
SLOW_BLINK:
  command: "SLOW BLINK AT [cat]"
  aliases: ["CAT KISS"]
  risk: none
  
  base_effect: |
    The slow blink is cat language for trust and affection.
    Cats recognize this. They may blink back.
    
  outcomes:
    returned:
      buff: "+1 bond, +1 Calm"
      message: "*blinks back slowly* *understanding*"
    ignored:
      message: "*stares* *does not blink* *mysterious*"
```

#### PSPSPS — Universal Cat Summoning

```yaml
PSPSPS:
  command: "PSPSPS"
  
  outcomes:
    comes:
      message: "*ears perk* *trots over* *what do you want*"
    ignores:
      message: "*ear flick* *continues not caring*"
```

### SENSORY INTERACTIONS — Bidirectional!

These can be initiated by human OR cat. The initiator matters.

#### SNIFF

```yaml
SNIFF:
  bidirectional: true
  
  human_to_cat:
    effect: "Scent information gained"
    learns:
      - "Cat's current mood (anxious, content, playful...)"
      - "Where cat has been recently"
      - "Terpene notes (for the Terpene Litter)"
    message: |
      *You lean in. The cat allows it.*
      *They smell like [location] and [mood].*
      
  cat_to_human:
    trigger: "Relationship 30+ or curiosity"
    meaning: |
      The cat is interested. They want to know:
      - Where have you been?
      - Do you have food?
    message: |
      *Sniff. Sniff sniff. Extended analysis.*
      *You are being CATALOGUED.*
      
  cat_to_cat:
    message: "*nose boop* *mutual sniffing* *social protocols complete*"
```

#### LICK — Grooming as Affection

```yaml
LICK:
  bidirectional: true
  
  human_to_cat:
    warning: |
      This is... unconventional. Most humans don't lick cats.
      If you do, the cat will be VERY confused.
      
    outcomes:
      acceptance:
        requirements: "Trust 70+"
        message: |
          *You lick the cat.*
          *The cat freezes. Processing.*
          *They lick you back. Awkwardly. But sincerely.*
      confusion:
        message: |
          *The cat stares at you.*
          *What. What are you doing.*
          
  cat_to_human:
    trigger: "Relationship 'friend'+"
    meaning: |
      When a cat licks you, they are:
      1. Claiming you (you are THEIRS now)
      2. Grooming you (you clearly can't do it yourself)
      3. Showing affection (highest compliment)
      
    outcomes:
      claiming:
        message: |
          *The cat licks you thoroughly.*
          *You are THEIRS now. Officially.*
          *Other cats will know. You've been claimed.*
      sandpaper_affection:
        message: |
          *lick lick lick lick*
          *It kind of hurts.*
          *But they're purring. This is LOVE.*
          *Accept the exfoliation.*
          
  cat_to_cat:
    allogrooming: |
      Mutual grooming is social bonding. Trust. Family. Hierarchy.
      The cat who grooms more is usually higher status.
```

#### NOSE_BOOP

```yaml
NOSE_BOOP:
  command: "BOOP [cat]"
  bidirectional: true
  
  base_effect: |
    A nose boop is a tiny, perfect moment of connection.
    It's "hello" and "I like you" and "we're okay" all at once.
    
  outcomes:
    success:
      message: |
        *boop*
        *The cat's nose is cold and slightly wet.*
        *A tiny moment. Perfect.*
    counter_boop:
      requirements: "Relationship 'friend'+"
      message: |
        *boop*
        *The cat boops back.*
        *Mutual boop achieved. Friendship confirmed.*
```

## TERPENE EFFECTS — Kitten-Specific Buffs

The Terpene Litter kittens impart their namesake's psychological effects
on anyone who interacts with them successfully. This isn't metaphor —
these kittens literally exude their terpene's essence.

### Kitten Effects

| Kitten | Terpene | Effect | Buffs | Duration |
|--------|---------|--------|-------|----------|
| **Myr** | Myrcene | Deep Relaxation | +3 Calm, +2 Easy-going, -2 Active | 30 min |
| **Lemon** | Limonene | Joy Infusion | +3 Cheerful, +2 Energetic | 45 min |
| **Lily** | Linalool | Peaceful Presence | +3 Calm, +2 Caring | 1 hour |
| **Pine** | Pinene | Sharp Clarity | +3 Analytical, memory boost | 2 hours |
| **Carrie** | Caryophyllene | Guardian's Resolve | +3 Confident, threat sense | 1 hour |
| **Hops** | Humulene | Refined Standards | +2 Neat, quality detection | 45 min |
| **Terpy Jr.** | Terpinolene | Chaos Muse | +3 Imaginative, random ideas | ??? |
| **Ocie** | Ocimene | Fresh Start | +2 Energetic, clears debuffs | 30 min |

### Synergies

| Combo | Name | Effect |
|-------|------|--------|
| Myr + Lily | The Sedation Stack | Short nap = long sleep benefits |
| Lemon + Pine | The Focus Boost | Creative AND productive |
| Carrie + Pine | The Sentinel Package | Hyperawareness without anxiety |
| **All 8** | **THE FULL SPECTRUM** | ENTOURAGE EFFECT — all buffs, legendary |

**Stacking:** Maximum 3 simultaneous terpene buffs. Conflicting effects may cancel.

## CHARM TYPES — Persistent Effects

| Charm | Source Trait | Effect | Example Cats |
|-------|--------------|--------|--------------|
| **Serenity** | Calm 6+ | +2 Calm | Terpie, Myr, Lily |
| **Joy** | Cheerful 6+ | +2 Cheerful | Lemon, Ocie |
| **Focus** | Analytical 6+ | +2 Analytical | Pine |
| **Courage** | Confident 6+ | +2 Confident | Stroopwafel, Carrie |
| **Creativity** | Spontaneous 6+ | +2 Imaginative | Terpy Jr. |

## POWER-UPS — Temporary Abilities

| Power-Up | Source | Effect |
|----------|--------|--------|
| **Therapeutic Purr** | Calm 7+ | Heal 1 HP/minute |
| **Luck Boost** | Cat sits in lap unprompted | +10% random outcomes |
| **Danger Sense** | Cautious 6+ | Warning before threats |
| **Mood Read** | Caring 7+ | Sense NPC emotions |

## CURSES — Negative Effects

| Curse | Trigger | Effect | Cure |
|-------|---------|--------|------|
| **Scratched** | Failed belly rub | -1 HP, visible marks | Rest |
| **Cold Shoulder** | Multiple rejections | Cat ignores you 1hr | Wait |
| **Judged** | Failing Hops' standards | -1 Confidence | Premium food |
| **Protective Wrath** | Threatening family | -3 HP, remembered | MUCH time |

## RELATIONSHIP SYSTEM

Cats remember. Every interaction is tracked. Trust and fondness grow
(or decay) based on how you treat them.

### Relationship Levels

| Level | Points | Success Mod | Cat Behavior |
|-------|--------|-------------|--------------|
| **Stranger** | 0-10 | -10% | Cautious, may avoid |
| **Acquaintance** | 11-25 | — | Tolerates presence |
| **Familiar** | 26-50 | +10% | Comfortable |
| **Friend** | 51-75 | +20% | Seeks attention |
| **Bonded** | 76-90 | +30% | Follows you, protective |
| **Soulmate** | 91+ | +50% | Psychic connection |

### Components

| Component | Weight | Builds From | Damaged By |
|-----------|--------|-------------|------------|
| **Trust** | 40% | Respecting boundaries | Forcing contact |
| **Fondness** | 35% | Successful interactions | Ignoring |
| **History** | 25% | Time together | Long absences |

### Special Events

| Event | Bonus |
|-------|-------|
| **First Lap Sit** | +10 trust, +5 fond |
| **First Gift** | +5 fond (cat brings you something) |
| **Defense** | +10 all (cat protects you) |

### Decay

- Fondness: 1 point per session without interaction
- Trust: 0.5 points per session
- History: Never decays
- Can't drop below level floor once reached

## HOME VS LOCATION PROTOCOL

**Critical architectural pattern:**

```yaml
cat:
  home: pub/cat-cave/            # Where FILE lives (never moves)
  location: pub/cat-cave/nap-zone  # Where cat currently IS
```

| Concept | Meaning | Example |
|---------|---------|---------|
| **home:** | File's physical directory | `pub/cat-cave/` |
| **location:** | Where character currently is | `pub/` |

**Why:** Files don't move. Git tracks field changes, not file moves.

## CAT INSTANCE PATTERN

Each cat file overlays this skill:

```yaml
# pub/cat-terpie.yml
id: terpie
type: [cat, character]
home: pub/cat-cave/
location: pub/cat-cave/nap-zone

sims_traits:
  nice: 5
  outgoing: 4
  active: 3
  playful: 6
  neat: 2
  
personality:
  quirks: ["judges silently", "knows things"]
  preferences:
    scritch_spots: [chin, ears]
    dislikes: [belly rubs, sudden movements]
    
buffs:
  terpie_blessing:
    effect: "Lucky breaks for 1 hour"
    trigger: successful_deep_interaction
```

## Live Examples

- [examples/adventure-4/pub/](../../examples/adventure-4/pub/) — Room with cats
- [examples/adventure-4/pub/bar/cat-cave/](../../examples/adventure-4/pub/bar/cat-cave/) — Nested cat room

## Dovetails With

### Sister Skills
- [character/](../character/) — Cats ARE characters
- [buff/](../buff/) — Interaction effects
- [mind-mirror/](../mind-mirror/) — Personality traits
- [room/](../room/) — Where cats live
