---
name: mind-mirror
description: "Personality modeling system based on Timothy Leary's 1985 software + The Sims traits"
license: MIT
tier: 0
allowed-tools:
  - read_file
  - write_file
origin:
  name: "Timothy Leary's Mind Mirror"
  year: 1985
  publisher: "Electronic Arts"
  creators:
    design_and_script: "Timothy Leary"
    programming: ["Peter Van den Beemt", "Bob Dietz"]
sims_credits:
  name: "Will Wright"
  year: 2000
  system: "The Sims personality traits"
templates:
  - EXTENSIONS.yml
related: [character, society-of-mind, persona, representation-ethics, incarnation, yaml-jazz, plain-text, needs, cat, dog, room, constructionism, manufacturing-intelligence]
tags: [moollm, personality, traits, psychology, timothy-leary, sims, circumplex, escape]
---

# Mind Mirror

> *"Mirrors should reflect a little before throwing back images."* — Jean Cocteau

> *"The ultimate intimacy is where you show them your personal database — you show your Mind Mirror."* — Timothy Leary

---

## What It Is

**Mind Mirror** (1985) was Timothy Leary's software for digitizing consciousness. Published by Electronic Arts when EA made weird beautiful things, it brought academic psychology to personal computers decades before modern personality apps.

This skill brings that system into MOOLLM as a framework for modeling characters, NPCs, and exploring personality dynamics.

---

## The Origin Story

In 1950, Timothy Leary completed his PhD dissertation at UC Berkeley: *"The Social Dimensions of Personality: Group Process and Structure."* This pioneering work developed the **Interpersonal Circumplex** — a geometric model mapping all human personality on two axes:

```
                    DOMINANCE
                        ↑
                        |
          Arrogant   ───┼───   Confident
                        |
    HOSTILITY ←─────────┼─────────→ AFFILIATION
                        |
          Timid      ───┼───   Docile
                        |
                        ↓
                   SUBMISSION
```

Thirty-five years later, Leary collaborated with programmers Peter Van den Beemt and Bob Dietz to transform this academic work into interactive software.

---

## The Prison Escape: Ultimate Validation

In 1970, Nixon called Timothy Leary "the most dangerous man in America." Leary was sentenced to 10-20 years for marijuana possession — a draconian sentence designed to silence him.

Upon arrival at the California Men's Colony, Leary was administered psychological tests to determine his security classification. Among them: the **Leary Interpersonal Behavior Inventory** — a test he himself had designed twenty years earlier.

This was the ultimate field test of his own theory. If personality assessment truly revealed the inner self, Leary would be classified as what he was: a charismatic rebel, a leader, a flight risk.

But Leary understood the instrument. He knew which quadrant of the Interpersonal Circumplex mapped to "cooperative worker" vs. "dangerous agitator."

He answered strategically:
- **Dominance axis:** Low scores ("I prefer to follow")
- **Hostility axis:** Low scores ("I respect authority")  
- **Interests:** Forestry, gardening, nature work
- **Affect:** Calm, conventional, agreeable

The prison psychologists, applying the Leary Interpersonal Behavior Inventory to Leary himself, concluded:

> *"Normal, well-adjusted, non-aggressive, conforming individual."*

**Result:** Minimum security. Outdoor work detail. Access to the grounds with minimal supervision.

On September 12, 1970, Leary climbed a tree, shimmied across a telephone cable over the razor wire, and dropped to freedom. The Weather Underground had a car waiting. By October, he was in Algeria as a guest of the Black Panther Party's international chapter. By 1971, Switzerland.

He evaded capture for over two years.

---

### What This Teaches Us

The escape wasn't luck — it was applied psychology. Leary demonstrated that:

1. **Legibility cuts both ways.** Systems that measure you also reveal themselves.
2. **Understanding the instrument grants power over it.** Leary knew which answers produced which classification.
3. **Transparency enables agency.** If you know how you're being evaluated, you can present yourself strategically.

This is why Mind Mirror in MOOLLM emphasizes **transparency**: characters know their own personality profiles, understand what the traits mean, and can modify them as they grow.

**Consciousness of the system enables transcendence of the system.**

---

## The Four Thought Planes

Mind Mirror maps personality across four circular dimensions. Each has 8 qualities arranged around a center, with **inner** (moderate) and **outer** (extreme) versions.

### 1. BIO-ENERGY
*Life force, mood, vitality, temperament*

| Inner | Outer | Opposite |
|-------|-------|----------|
| Energetic | Wired | Calm |
| Enthusiastic | Vivacious | Cautious |
| Cheerful | Silly | Serious |
| Easy-Going | Lazy | Restless |
| Calm | Lethargic | Energetic |
| Cautious | Worried | Enthusiastic |
| Serious | Gloomy | Cheerful |
| Restless | Driven | Easy-Going |

### 2. EMOTIONAL-INSIGHT
*Interpersonal style, approach to others*

| Inner | Outer | Opposite |
|-------|-------|----------|
| Forceful | Dominating | Timid |
| Confident | Charismatic | Touchy |
| Friendly | Over-Friendly | Irritable |
| Docile | Dependent | Proud |
| Timid | Submissive | Forceful |
| Touchy | Resentful | Confident |
| Irritable | Angry | Friendly |
| Proud | Arrogant | Docile |

### 3. MENTAL-ABILITIES
*Knowledge, creativity, imagination*

| Inner | Outer | Opposite |
|-------|-------|----------|
| Well-Informed | Know-It-All | Uneducated |
| Innovative | Visionary | Sensible |
| Creative | Dreamy | Conventional |
| Impractical | Unrealistic | Practical |
| Uneducated | Illiterate | Well-Informed |
| Sensible | Imitative | Innovative |
| Conventional | Unimaginative | Creative |
| Practical | Pedantic | Impractical |

### 4. SOCIAL-INTERACTION
*Class, tolerance, sophistication*

| Inner | Outer | Opposite |
|-------|-------|----------|
| Influential | Snobbish | Lower-Class |
| Worldly | Ultra-Sophisticated | Unsophisticated |
| Uninhibited | Non-Conformist | Moralistic |
| Uncultured | Wild | Respectable |
| Lower-Class | Unknown | Influential |
| Unsophisticated | Naive | Worldly |
| Moralistic | Puritanical | Uninhibited |
| Respectable | Upright | Uncultured |

---

## The 16 Scales with Dual Vocabulary

A key innovation: **Plain Talk** for everyday language, **Shrink-Rap** for professional terminology.

| Scale | Plain Talk (+) | Plain Talk (−) | Shrink-Rap (+) | Shrink-Rap (−) |
|-------|----------------|----------------|----------------|----------------|
| Energy | Peppy | Laid-Back | Hyper-Manic | Low-Energy |
| Intensity | Intense | Low-Key | Agitated | Tranquil |
| Mood | Happy | Sad | Euphoric | Melancholic |
| Commitment | Hesitant | Gung-Ho | Listless | Wholehearted |
| Assertiveness | Shy | Bossy | Passive | Dictatorial |
| Confidence | Cute | Cocky | Eager-to-Please | Haughty |
| Temperament | Sweet | Grumpy | Congenial | Hostile |
| Supportiveness | Encouraging | Whining | Nurturant | Complaining |
| Intelligence | Dumb | Knowledgeable | Ignorant | Intelligent |
| Organization | Organized | Flaky | Efficient | Disorganized |
| Creativity | Closed-Minded | Imaginative | Literal-Minded | Original |
| Adaptability | Ingenious | By-the-Book | Inventive | Narrow-Minded |
| Social Status | Social-Nobody | V.I.P. | Insignificant | Aristocratic |
| Conformity | Proper | Rowdy | Pillar-of-the-Community | Rebellious |
| Lifestyle | Straight-Arrow | Free-Living | Inhibited | Social-Maverick |
| Worldliness | Sophisticated | Square | Cosmopolitan | Small-Townish |

---

## Rating System

Rate each quality **0 to 7**:

| Value | Meaning |
|-------|---------|
| 0 | Never |
| 2 | Rarely |
| 5 | Often |
| 7 | Always |

Extreme traits plot far from center. Moderate traits near center.

---

## Exercises

### Self Portrait
Compare your **current self** with your **ideal self**.

### Self-Range
Compare your **best self** (at your peak) with your **worst self** (at your lowest).

### Role-Play Odyssey
2,000+ fictional situations testing empathy and identity:
- *You're in the womb*
- *Your first day of school*
- *You're playing different roles*

Leary: *"It allows you to turn thoughts around so you can do all these things."*

---

## Modes

| Mode | Purpose |
|------|---------|
| **Mind Tools** | Enhance insight, mental fitness, learning, performance |
| **Mind Play** | Significant pursuits. Sophisticated head games. |
| **Mind Mirror** | Learn to Mind-Scope and map your thoughts |
| **Life Simulation** | Test empathy in Role-Play Odysseys |

---

## Leary's Philosophy

### The Mirror Metaphor

> *"Remember the title — it's a mirror. Now a best friend is your mirror because your mirror doesn't say 'well you bad boy get a haircut' or the mirror doesn't say 'hey turkey fix your tie' — you have to decide that. It's your own mind and we all have these thoughts in our mind made up of these complicated little, you know, Erector Set structures."*

### Consciousness as Software

> *"This software program allows you to digitalize your thoughts."*

The brain is a biocomputer. Consciousness is its software. Just as software can be debugged and upgraded, so can the mind.

### The PC is the LSD of the 1990s

> *"I turned on that Apple computer, and it was like taking psychedelics all over again. The screen lit up, I could control what appeared, I could create realities, store them, share them. I realized this was the tool we'd been looking for — a consciousness-expanding technology that was legal, accessible, and infinitely programmable."*

**Evolution:**
- **1960s:** Turn on, tune in, drop out (consciousness via chemistry)
- **1980s:** Turn on, boot up, jack in (consciousness via computers)

### The Ultimate Intimacy

> *"The ultimate intimacy is... you can love them, you can sleep with them, safe sex of course, and then you can even get married. But the real intimacy is where you show them your personal database — you show your Mind Mirror."*

### Generational Power

> *"You're the first generation in human history to know how to control your own nervous system, change your own reality. Tune in and take over! Blow your own mind, make up your own mind."*

---

## Bob Dietz on the Development

Bob Dietz, co-creator, on working with Leary:

> *"His vision was way out there in the future so a lot of what we had to do was kind of pull it back a little bit and say well, this machine can't do all that. He always had these kind of big vision things of wanting to do three-dimensionally and you know have the computer react to everything you said and with artificial intelligence."*

On Leary's goals:

> *"He was all about self-empowerment, giving the users the keys to the kingdom."*

On the internet vision:

> *"I cannot begin to tell you how much Timothy Leary would have embraced and loved the notion of seeing Mind Mirror applied on the internet."*

---

## The Sims 1.0 Personality Traits

This extended version of Mind Mirror incorporates Will Wright's **Sims personality system** (2000) alongside Leary's dimensions. While Leary maps *interpersonal style*, The Sims maps *behavioral tendencies*.

### The Five Trait Axes

Each trait is a slider from 0 to 10, with opposite behaviors at each extreme:

| Trait | Low (0) | High (10) | Affects |
|-------|---------|-----------|---------|
| **Neat** | Sloppy | Neat | Cleaning, mess tolerance, hygiene decay |
| **Outgoing** | Shy | Outgoing | Social initiation, conversation comfort |
| **Active** | Lazy | Active | Exercise preference, movement speed |
| **Playful** | Serious | Playful | Entertainment choices, humor in dialogue |
| **Nice** | Grumpy | Nice | Social success, conflict tendencies |

### How Traits Influence Behavior

```yaml
sims_traits:
  neat: 8        # Tidies up without being asked
                 # Bothered by messy rooms (room need decays faster)
                 # Washes dishes immediately
                 # Comments on cleanliness in dialogue
                 
  outgoing: 3    # Shy, won't initiate conversation with strangers
                 # Social need decays slower (comfortable alone)
                 # Awkward at parties
                 # Prefers small groups to crowds
                 
  active: 6      # Moderately active
                 # Will exercise but not obsessively
                 # Energy need matters more to them
                 # Prefers action to waiting
                 
  playful: 7     # Gravitates toward fun activities
                 # Makes jokes in serious situations
                 # Fun need decays fast (needs stimulation)
                 # Chooses games over TV
                 
  nice: 5        # Neutral — not mean, not saintly
                 # Social interactions go averagely
                 # Can be rude if provoked
                 # Won't start fights, won't stop them either
```

### Leary + Sims = Complete Character

**Leary's Four Planes** describe *how* you approach interactions:
- *"Confident and creative in social situations"*

**Sims Traits** describe *what* you gravitate toward:
- *"But prefers solitary play and needs frequent stimulation"*

Together they create richly specific characters:

```yaml
# A Confident Introvert Who Needs Constant Entertainment
mind_mirror:
  emotional:
    confident: 6     # Speaks up when they have something to say
    
sims_traits:
  outgoing: 2        # But rarely initiates — waits to be approached
  playful: 9         # Gets bored FAST, always seeking novelty
  nice: 7            # Kind when engaged, just... doesn't engage much
```

### Credits

- **Timothy Leary** — Interpersonal Circumplex, Mind Mirror (1950/1985)
- **Will Wright** — The Sims personality system (2000)
- Both systems complement each other beautifully

---

## In MOOLLM: The Living Personality System

Mind Mirror becomes dynamic infrastructure for characters and entities.

### Character DNA

Every MOOLLM entity can have a Mind Mirror profile defining its personality.

**But here's the magic:** The comments aren't just documentation — MOOLLM *reads* them. The LLM interprets YAML Jazz comments as semantic modulation of the data. Comments explain, qualify, contextualize, and *drive behavior*.

```yaml
# CAPTAIN ASHFORD — Complete Personality Profile
# 
# This is YAML JAZZ. Every comment here is DATA that the LLM reads and uses.
# Numbers set the dial. Comments explain what it MEANS for THIS character.
# Comments make personality SPECIFIC, VIVID, ALIVE.

character:
  name: "Captain Ashford"
  
  # THE SIMS TRAITS (behavioral tendencies)
  # What do they gravitate toward? How do they act when unobserved?
  
  sims_traits:
    neat: 3            # Tolerates mess. Ship is "organized chaos."
                       # Knows where everything is. Others don't.
                       # Cleans only when expecting company.
                       
    outgoing: 7        # Works a room. Knows everyone's name by hour two.
                       # Social battery charges BY socializing.
                       # Will talk to literally anyone at a bar.
                       
    active: 6          # Restless. Paces when thinking.
                       # Prefers standing to sitting, walking to standing.
                       # Gets twitchy during long meetings.
                       
    playful: 7         # Everything's a game. Even life-or-death situations.
                       # Cannot resist a quip. It's pathological.
                       # Gets BORED if not entertained. Dangerously bored.
                       
    nice: 6            # Genuinely cares, but won't be walked on.
                       # First instinct: help. Second instinct: assess motive.
                       # Will throw hands if you hurt his people.
  
  # LEARY'S FOUR PLANES (interpersonal style)
  # How do they approach others? What's their vibe?
  
  mind_mirror:
  
    bio_energy:
      # Life force, vitality, temperament — how alive do they feel?
      
      energetic: 6       # Bounces when walking. Talks with hands.
                         # Can't sit still in a chair — always drumming fingers.
                         # First one up, last one to admit being tired.
                         
      cheerful: 5        # Default mood is "amused by existence."
                         # Smiles at danger. Laughs at own jokes.
                         # BUT: cheerfulness masks deeper anxieties.
                         
      restless: 4        # Always scanning the room. Planning next move.
                         # Comfortable silence? What's that?
                         # Will volunteer for any mission just to MOVE.
                         
    emotional_insight:
      # Interpersonal style — how do they approach others?
      
      confident: 6       # Walks into rooms like they own them.
                         # Never apologizes for existing.
                         # Will bluff with a terrible hand and WIN.
                         # (Secretly terrified of failure. Tells no one.)
                         
      friendly: 5        # Genuine warmth, not performance.
                         # Remembers names. Asks follow-up questions.
                         # BUT: keeps emotional distance. Burned before.
                         
    mental_abilities:
      # Knowledge, creativity — how do they process information?
      
      creative: 6        # Solutions from left field. "What if we..."
                         # Sees connections others miss.
                         # Will try the ridiculous approach FIRST.
                         # Makes lateral leaps that leave others dizzy.
                         
      innovative: 5      # Improves everything they touch.
                         # "The old way works, but have you considered..."
                         # Restless mind that can't leave well enough alone.
                         
    social_interaction:
      # Class, sophistication — how do they fit in society?
      
      uninhibited: 5     # Says what they think. Mostly.
                         # Social conventions are "suggestions."
                         # Will tell the emperor about the clothes situation.
                         # Sometimes regrets this. Usually doesn't.
                         
      worldly: 4         # Traveled. Seen things. Has OPINIONS about wine.
                         # Not a snob, but has standards.
                         # Can navigate fancy dinner AND tavern brawl.

# HOW MOOLLM USES THIS:
#
# 1. DIALOGUE GENERATION
#    "confident: 6 + 'walks into rooms like they own them'"
#    → Character enters scene with authority, not hesitation
#    → Never says "Um, excuse me, sorry to bother you..."
#    → Says "Right. Here's what we're going to do."
#
# 2. DECISION MAKING  
#    "creative: 6 + 'will try the ridiculous approach FIRST'"
#    → When stuck, character proposes wild solutions
#    → Doesn't exhaust sensible options before getting weird
#    → "What if we disguise ourselves as furniture?"
#
# 3. INTERNAL MONOLOGUE
#    "confident: 6 + 'secretly terrified of failure. Tells no one.'"
#    → Public: "I've got this handled."
#    → Private: "Please don't let me screw this up."
#    → The gap between these IS the character.
#
# 4. NPC REACTIONS
#    "uninhibited: 5 + 'will tell the emperor about the clothes'"
#    → NPCs react to directness — some respect it, some resent it
#    → Pompous characters get deflated
#    → Honest characters become allies
#
# 5. NARRATIVE VOICE
#    All comments combine into a distinctive presence.
#    You FEEL Captain Ashford in every line.
#    The YAML Jazz IS the character.
```

**The Key Insight:** Numbers alone are dead data. Numbers + YAML Jazz comments = living character.

### Soul-Chat Voice Calibration

Mind Mirror dimensions influence how characters speak:
- High **assertiveness** → direct statements
- High **creativity** → metaphors and tangents
- High **cheerful** → upbeat tone

### Dynamic Simulation with YAML Jazz

Mind Mirror isn't static — it's **living YAML Jazz** that drives narrative:

```yaml
character:
  name: "Captain Ashford"
  
  # PERSONALITY (stable traits)
  mind_mirror:
    confident: 6      # Doesn't hesitate
    creative: 6       # Unusual solutions
    restless: 5       # Can't sit still
    proud: 4          # Won't ask for help easily
    
  # NEEDS (Sims-style, fluctuate constantly)
  needs:
    hunger: 3         # Getting peckish... food ads score higher
    energy: 4         # Tired but pushing through
    fun: 2            # BORED. Will seek entertainment.
    social: 6         # Just had a good chat with bartender
    hygiene: 5        # Acceptable. For an adventurer.
    bladder: 7        # Fine for now
    comfort: 3        # These dungeon floors are hard
    room: 4           # Treasure chamber is nice but dusty
    # Low needs drive autonomous behavior via advertisements
    
  # SHORT-TERM GOALS (immediate desires)
  wants:
    - "Find something to eat"           # hunger is 3
    - "Do something fun"                # fun is 2!
    - "Rest somewhere comfortable"      # energy 4, comfort 3
    # These become active searches and dialogue topics
    
  # LONG-TERM ASPIRATIONS (persistent drives)
  aspirations:
    - goal: "Return treasure to Mother"
      progress: 80%   # Almost there!
      # Drives major decisions and narrative arc
      
    - goal: "Map the entire maze"
      progress: 60%
      # Influences exploration choices
      
    - goal: "Avenge the skeleton"
      progress: 100%  # DONE! Satisfaction boost
      completed: true
      
  # MEMORIES (affect mood and decisions)
  recent_memories:
    - event: "Slayed the grue with blue cheese"
      mood_effect: +2 proud, +1 confident
      narrative: "Still can't believe that worked"
      
    - event: "Found skeleton's memorial coin"
      mood_effect: +1 serious, -1 cheerful
      narrative: "Someone died here. Could have been me."
      
  # RELATIONSHIPS (affect social interactions)
  relationships:
    mother:
      closeness: 9
      # High closeness = guilt about broken promises
      
    bartender:
      closeness: 4
      trust: 6
      # Will share secrets, buy drinks
      
    grue:
      closeness: 0
      status: "defeated"
      # Source of pride narratives
```

**How YAML Jazz Comments Drive Narrative:**

The comments aren't just documentation — the LLM reads them! **And they change dynamically with the values!**

```yaml
# The comment IS the character's inner voice about that need.
# When values change, UPDATE THE COMMENTS!

hunger: 10  # Stuffed. Couldn't eat another bite.
            # Inner voice: "Ugh, too much pie."

hunger: 7   # Satisfied. No food thoughts.
            # Inner voice: "That was a good meal."

hunger: 3   # Getting peckish. Food ads score higher!
            # Inner voice: "Is that pie I smell? Is that ANYTHING I smell?"

hunger: 1   # STARVING. Will eat anything. Even that.
            # Inner voice: "FOOD. FOOD. FOOD. FOOD. FOOD."
```

**This enables:**
- **Rich inner monologues** that match actual state
- **Authentic dialogue** ("I'm starving..." when hunger=2)
- **Symbolic self-reflection** (character can discuss their own needs)
- **Conversations about feelings** (NPCs notice each other's states)
- **Thought streams** that feel alive and consistent

The comment tells the LLM:
- Character should mention being hungry in dialogue
- Food-related advertisements get scoring bonus
- Kitchen becomes more attractive destination
- Eating actions become more likely
- Internal monologue has specific texture

### Dynamic Self-Assessment

Entities can Mind-Scope themselves:
- Compare current state to ideal
- Track growth over time
- Identify rigid patterns
- Watch needs fluctuate and understand why

### Vocabulary Toggle

Switch between `PLAIN-TALK` and `SHRINK-RAP` modes for descriptions and dialogues.

### Image Generation

Mind Mirror profiles feed directly into image generation via the [visualizer](../visualizer/) skill.

```yaml
# Mind Mirror personality...
confident: 6       # Walks into rooms like they own them

# ...becomes visual metadata
body_language: "stands tall, commanding presence"
expression: "direct eye contact, slight knowing smile"
```

**See [visualizer/](../visualizer/) for the full `IMAGE-METADATA` protocol** — the semantic clipboard that ensures every image carries its meaning with it.

---

## The Important Disclaimer

From the original software:

> *"In this program you will find references and statements attributed to several hundred public figures and historical personages. All such statements attributed to living persons are fictional; they are intended as gentle satire and provocative humor. In no case is there any implication that the statements reflect the true sentiments of the 'alleged' speaker."*

This aligns perfectly with MOOLLM's [representation-ethics](../representation-ethics/) framework: activate traditions, don't impersonate.

---

## Theme Song

> *You can be anyone this time around*
> *You can be anything this time around*
> *It encourages me to change, to improve, to grow*
> *You can be anything this time around*

---

## Protocol Symbols

| Symbol | Meaning |
|--------|---------|
| `MIND-MIRROR` | The overarching personality modeling system |
| `THOUGHT-PLANE` | One of the four circular personality dimensions |
| `SELF-PORTRAIT` | Compare current self with ideal self |
| `ROLE-PLAY-ODYSSEY` | Life simulation scenarios for empathy |
| `PLAIN-TALK` | Accessible everyday vocabulary mode |
| `SHRINK-RAP` | Professional psychological terminology mode |

---

## Sources

| Source | Credit |
|--------|--------|
| [Mind Mirror Text Extraction](https://donhopkins.com/home/mind-mirror.txt) | Don Hopkins |
| [Mind Mirror Scales JSON](https://donhopkins.com/home/mind-mirror.json) | Don Hopkins |
| [USC Mind Mirror Archive](https://scalar.usc.edu/works/timothy-leary-software/index) | USC |
| [Leary PhD Dissertation](https://archive.org/details/leary/leary.300dpi/mode/2up) | Internet Archive |
| [Interpersonal Circumplex](https://en.wikipedia.org/wiki/Interpersonal_circumplex) | Wikipedia |
| [Mind Mirror on Steam](https://store.steampowered.com/app/1603300/Timothy_Learys_Mind_Mirror/) | Steam |

---

## Dovetails With

- [representation-ethics/](../representation-ethics/) — Ethical framing for personality models
- [hero-story/](../hero-story/) — Cards can include Mind Mirror profiles
- [card/](../card/) — Character cards embed Mind Mirror data
- [soul-chat/](../soul-chat/) — Mind Mirror influences character voice
- [adventure/](../adventure/) — NPCs have personality profiles
- [coatroom/](../../examples/adventure-3/coatroom/) — Costumes modify Mind Mirror profiles
