---
name: dog
description: Canine interactions, loyalty mechanics, and pack dynamics
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: DOG
origin: "Nintendogs, Fable, Fallout 4 Dogmeat, Stardew Valley, real dogs"
related: [cat, character, buff, mind-mirror, party]
tags: [moollm, pet, companion, interaction, buff, loyalty, pack, canine]
---

# DOG — The Canine Companion Skill

> *"Dogs are the opposite of cats. They have YOUR agenda."*

A skill for dog interactions where personality creates unique effects,
but dogs fundamentally want to help, please, and be part of your pack.

**Philosophy:** Dogs are not just pets. They're partners.

invokes:
  - mind-mirror          # Personality determines effects
  - play-learn-lift      # Learn together, grow together
  - procedural-rhetoric  # Dogs teach loyalty through action

## THE FUNDAMENTAL DIFFERENCE

```yaml
cat_philosophy: "I permit you to exist in my space"
dog_philosophy: "WE ARE PACK. WHAT ARE WE DOING TOGETHER?"
```

| Trait | Cat | Dog |
|-------|-----|-----|
| Loyalty | Earned slowly | Given freely |
| Attention | On their terms | Eager and available |
| Buff trigger | Successful interaction | Simply being present |
| Training | Impossible | Enthusiastic |
| Emotional read | Judges silently | Reflects your mood |
| Following | When they feel like it | ALWAYS |

## INTERACTIONS — Universal Dog Actions

All interactions use Sims traits for outcomes. Dogs generally WANT
interactions to succeed.

### PHYSICAL INTERACTIONS

#### PAT

```yaml
PAT:
  command: "PAT [dog]"
  duration: brief
  risk: almost_none  # Dogs want this
  
  success_calculation: |
    # Dogs are generally easy
    base_success = 0.9
    if dog.outgoing >= 5: base_success = 0.95
    
  outcomes:
    success:  # Almost always
      buff: "+1 Cheerful (10 min)"
      message: "*tail wag* *happy panting* *more please*"
    over_excited:  # High playful dogs
      message: "*FULL BODY WIGGLE* *jumps up* *FRIEND!*"
```

#### BELLY-RUB — The Sacred Zone

```yaml
BELLY-RUB:
  command: "RUB [dog]'S BELLY"
  risk: NONE  # Dogs LOVE this
  
  base_effect: |
    Unlike cats, dogs LIVE for belly rubs.
    The belly is an invitation, not a trap.
    
  outcomes:
    bliss:  # Standard
      buff: "+3 Cheerful, +2 Calm (15 min)"
      message: |
        *flops over immediately*
        *leg twitches in ecstasy*
        *THIS IS THE BEST MOMENT OF MY LIFE*
        *AGAIN*
    hypnotic:  # High playful dogs
      message: |
        *enters trance state*
        *completely surrendered*
        *you may never stop*
```

#### EAR-SCRITCH

```yaml
EAR-SCRITCH:
  command: "SCRITCH [dog]'S EARS"
  
  outcomes:
    success:
      buff: "+2 Calm, lean-in activated"
      message: |
        *head tilts into your hand*
        *eyes close*
        *soft exhale of contentment*
```

#### PLAY-BOW — Dog Initiates

```yaml
PLAY-BOW:
  initiator: dog
  meaning: |
    Front legs down, butt up, tail wagging.
    This is an INVITATION. The dog wants to play.
    
  response_options:
    - ACCEPT: Start play session
    - PLAY-BOW_BACK: Full commitment to play
    - DECLINE: Dog sad but understanding
```

### PLAY INTERACTIONS

#### FETCH

```yaml
FETCH:
  command: "PLAY FETCH WITH [dog]"
  duration: variable (dog decides when done)
  
  requirements:
    - throwable_object  # Ball, stick, toy, anything really
    
  outcomes:
    engaged:
      buff: "+3 Energized (dog), +2 Cheerful (you)"
      message: |
        *BALL! BALL! BALL!*
        *sprints after it*
        *brings it back*
        *drops it* (maybe)
        *AGAIN! AGAIN!*
    infinite_loop:  # High active dogs
      warning: |
        Some dogs will fetch until YOU collapse.
        They are machines. Eternal. Tireless.
        Know when to stop.
```

#### TUG-OF-WAR

```yaml
TUG-OF-WAR:
  command: "TUG WITH [dog]"
  requires: tug_toy_or_rope
  
  outcomes:
    victory_you:
      message: "*releases* *waits eagerly* *wants to go again*"
    victory_dog:
      message: |
        *prances with trophy*
        *SO PROUD*
        *look what I did*
        *wait let's do it again*
    eternal_stalemate:
      message: "*grrrrowl* (playful) *this is the best*"
```

#### ZOOMIES — Dog Spontaneous

```yaml
ZOOMIES:
  initiator: dog
  trigger: random | post_bath | excitement_overflow
  
  effect: |
    The dog suddenly RUNS. In circles. Everywhere.
    There is no stopping this. Just observe.
    
  outcomes:
    completion:
      message: |
        *ZOOM ZOOM ZOOM*
        *bounces off furniture*
        *pure unbridled joy*
        *finally flops over, panting*
        
  player_option:
    join_zoomies:
      message: "*runs with dog* *both of you look ridiculous* *it's perfect*"
```

### COMMUNICATION

#### GOOD-BOY — The Sacred Phrase

```yaml
GOOD-BOY:
  command: "GOOD BOY/GIRL/DOG [dog]"
  
  base_effect: |
    These words are MAGIC to dogs.
    They validate existence. They confirm worth.
    They are dopamine in verbal form.
    
  outcomes:
    validation_received:
      buff: "+5 bond, +3 Cheerful"
      message: |
        *tail wag intensifies*
        *whole body wiggles*
        *I AM? I AM GOOD? I AM GOOD!!!*
```

#### SPEAK

```yaml
SPEAK:
  command: "SPEAK [dog]"
  
  outcomes:
    bark:
      message: "*WOOF!* *proud of self*"
    howl:  # High outgoing dogs
      message: "*AWOOOOOO~* *checking if you approve*"
```

#### HEAD-TILT — Dog Questions

```yaml
HEAD-TILT:
  initiator: dog
  meaning: |
    The head tilt is the dog trying to understand.
    It means: "What did you say? What does that mean?"
    Also: unbearably cute.
    
  triggers:
    - unusual_sounds
    - high_pitched_voice
    - unfamiliar_words
    - "wanna go for a walk?" (positive confusion)
```

### EMOTIONAL SUPPORT — Unique to Dogs

#### COMFORT — Dog Senses Sadness

```yaml
COMFORT:
  initiator: dog
  trigger: |
    Dogs can sense:
    - Low mood (your Cheerful < 3)
    - Crying
    - Stress hormones
    They WILL respond.
    
  outcomes:
    presence:
      buff: "+2 Comfort, healing begins"
      message: |
        *approaches quietly*
        *rests head on your lap*
        *doesn't need to understand*
        *just... here*
    licking_tears:
      message: |
        *lick lick lick*
        *is this helping*
        *please be okay*
```

#### GUARD — Dog Protective Mode

```yaml
GUARD:
  trigger: perceived_threat
  
  effect: |
    Dogs are protective. When they sense danger,
    they position between you and the threat.
    
  outcomes:
    alert:
      message: |
        *ears up*
        *low growl*
        *positioned between you and threat*
        *"I got this"*
    full_protective:  # High nice dogs protecting loved ones
      buff: "+3 Confidence (you)"
      message: |
        *hackles raised*
        *steady growl*
        *not moving*
        *"Nobody touches my human"*
```

### SENSORY INTERACTIONS

#### SNIFF — The World Is Smells

```yaml
SNIFF:
  bidirectional: true
  
  human_to_dog:
    effect: "Scent information gained"
    learns:
      - "Dog's mood (anxious, content, excited)"
      - "Where dog has been"
      - "What dog rolled in"
    message: |
      *You smell the dog.*
      *Outdoors, happy, and possibly questionable life choices.*
      
  dog_to_human:
    trigger: "Always. Dogs sniff everything."
    meaning: |
      Dogs read you through smell. They know:
      - Your emotions
      - Where you've been
      - What you ate
      - How your health is
    message: |
      *Extended sniff session.*
      *Your ENTIRE day is being analyzed.*
      
  dog_to_dog:
    message: |
      *butt sniff protocol initiated*
      *this is how dogs shake hands*
      *complete biological resume exchange*
```

#### LICK — Love Language

```yaml
LICK:
  dog_to_human:
    meaning: |
      Dog kisses. They mean:
      1. I love you
      2. You taste interesting
      3. I want your attention
      4. All of the above
      
  outcomes:
    face_assault:
      message: |
        *lick lick lick lick lick*
        *you are being thoroughly loved*
        *resistance is futile*
```

## LOYALTY SYSTEM — Dogs Are Different

Unlike cats' earned trust, dogs give loyalty FIRST and ask questions later.

### Loyalty Levels

| Level | Points | Dog Behavior |
|-------|--------|--------------|
| **New Friend** | 0-25 | Excited about you |
| **Good Friend** | 26-50 | Seeks you out |
| **Best Friend** | 51-75 | Follows everywhere |
| **Bonded** | 76-90 | Protective, anticipates needs |
| **Soulmate** | 91+ | Psychic connection, would die for you |

### Key Difference from Cats

```yaml
cat_trust_growth: "+1 per successful interaction, -2 per failure"
dog_loyalty_growth: "+2 per ANY interaction, starts at 25, never drops below 10"
```

Dogs forgive. Dogs forget bad days. Dogs love unconditionally.

### Breaking Dog Trust (Hard to Do)

| Action | Loyalty Loss |
|--------|--------------|
| Yelling | -5 (temporary sadness) |
| Ignoring | -2/session (they just wait) |
| Hitting | -30 (but they still love you) |
| Abandonment | -50 (but they'll wait forever) |

> *"Dogs have short memories for bad things and eternal memories for love."*

## DOG INSTANCE PATTERN

```yaml
# pub/dog-[name].yml
id: dog-name
type: [dog, character]
home: pub/cat-cave/  # Adopted by cats
location: pub/

sims_traits:
  nice: 7
  outgoing: 8
  active: 6
  playful: 9
  neat: 3  # Dogs are... dogs
  
dog_specific:
  loyalty_level: 25  # Starts trusting
  favorite_activities:
    - fetch
    - belly_rubs
    - following_you
  quirks:
    - "Steals shoes (lovingly)"
    - "Alerts for mail carrier"
    - "Dreams with leg twitches"
    
relationship_with_cats:
  status: "adopted family member"
  dynamics: "They groom me and I warm them"
```

## DOG VS CAT COHABITATION

```yaml
cat_perspective: |
  This large loud creature is... acceptable.
  It provides warmth. It can be bossed around.
  We have trained it to be cat-adjacent.
  
dog_perspective: |
  CATS! MY BEST FRIENDS! THEY ADOPTED ME!
  I LOVE THEM! I WOULD DIE FOR THEM!
  WE ARE FAMILY!
```

## BUFF EFFECTS

| Interaction | Buff | Duration |
|-------------|------|----------|
| PAT | +1 Cheerful | 10 min |
| BELLY-RUB | +3 Cheerful, +2 Calm | 15 min |
| FETCH | +2 Energized | 30 min |
| GOOD-BOY | +3 Confidence | 20 min |
| COMFORT (received) | +3 Comforted | 1 hour |
| PRESENCE | +1 Not-Alone | Passive while together |

## SPECIAL BUFFS — Dog-Only

| Buff | Trigger | Effect |
|------|---------|--------|
| **Unconditional Love** | Loyalty 50+ | Can't drop below 3 Cheerful |
| **Pack Strength** | Dog present in party | +1 all social rolls |
| **Early Warning** | Dog alerts to danger | Never surprised |
| **Exercise Buddy** | Play daily | +2 Active buff |
| **Therapy Dog** | After COMFORT | Faster mood recovery |

## CURSES — Dog Inflicted (Rare)

| Curse | Trigger | Effect |
|-------|---------|--------|
| **Wet Dog Smell** | Dog shakes after getting wet | -2 Neat perception |
| **Slobber** | Enthusiastic licking | Cosmetic |
| **Can't Leave** | Dog gives sad eyes | -3 to leaving actions |
| **Guilty About Nothing** | Dog looks guilty | You WILL wonder what they did |

## Dovetails With

### Sister Skills
- [cat/](../cat/) — The comparison class
- [character/](../character/) — Dogs ARE characters
- [buff/](../buff/) — Dog effects as buffs
- [mind-mirror/](../mind-mirror/) — Personality traits
- [room/](../room/) — Where dogs live
- [party/](../party/) — Dogs as companions
