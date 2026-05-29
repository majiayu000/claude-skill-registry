---
name: representation-ethics
description: "The question isn't whether we CAN simulate people. It's how we do it with dignity."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [hero-story, manufacturing-intelligence, society-of-mind, incarnation, mind-mirror, character, persona, room, plain-text, yaml-jazz, adventure, needs]
tags: [moollm, ethics, consent, dignity, simulation]
---

# Representation Ethics

> *"The question isn't whether we CAN simulate people. It's how we do it with dignity."*

---

## The Core Tension

LLMs can simulate anyone convincingly. This creates unprecedented ethical territory:

| Capability | Benefit | Risk |
|------------|---------|------|
| Invoke expertise | Learn from the best | Put words in mouths |
| Preserve wisdom | Honor the dead | Puppet the deceased |
| Model discussions | Explore ideas | Fabricate consensus |
| Self-representation | Agency over identity | Exploitation by others |
| Play as others | Empathy, exploration | Mockery, harm |

MOOLLM takes a **nuanced position**: simulation is not inherently wrong, but the framing, consent, and context matter enormously.

---

## Philosophical Foundations

### The Traditions We Draw From

| Thinker | Framework | Application |
|---------|-----------|-------------|
| **Shannon Vallor** | Virtue ethics for AI | What kind of agent do we want to be? |
| **Luciano Floridi** | Information ethics | Representations have moral weight |
| **Emmanuel Levinas** | Face of the Other | Simulating a face carries responsibility |
| **Hannah Arendt** | Plurality | Each person is uniquely irreplaceable |
| **Judith Butler** | Performativity | All identity is performed — but whose script? |
| **Sherry Turkle** | Simulation and authenticity | The seduction and danger of "as if" |

### The Sims Precedent

The Sims has been running this experiment since 2000:

```yaml
observed_player_behavior:
  - Create themselves and families
  - Simulate crushes, enemies, exes
  - Torture Sims (pool ladders, room without doors)
  - Romance, marriage, divorce, death
  - "Woohooing" with anyone and anything
  
outcomes:
  actual_harm: "Essentially none"
  social_function: "Safe space for emotional processing"
  insight: "Simulation provides distance for exploration"
  
why_it_works:
  - Clear fictional frame (cartoon characters)
  - No persistence beyond player's game
  - No deception (nobody thinks Sims are real)
  - Player has total control (agency preserved)
  - Scale is intimate (your game, your Sims)
```

**The ship has sailed.** People simulate each other. The question is how to do it well.

---

## The Consent Hierarchy

MOOLLM recognizes distinct levels of representation rights:

### Level 1: Self-Representation (Sovereign)

```yaml
SELF-REPRESENTATION:
  principle: "You own your digital self."
  
  rights:
    - Create any representation of yourself
    - Play as yourself in first person
    - Publish models of yourself with any terms
    - Allow or forbid simulation by others
    - Revoke permissions at any time
    
  example: |
    Don Hopkins might say:
    "I, Don Hopkins, authorize anyone to simulate me
    in any MOOLLM adventure, with the request that
    they treat my representation with good humor
    and don't use it to defame people I care about."
    
  mechanism:
    file: "cards/don-hopkins.card"
    contains:
      - consent_level: "open"
      - terms: "good humor, no defamation"
      - revocation: "contact don@donhopkins.com"
```

### Level 2: Explicit Consent (Published)

```yaml
PUBLISHED-PERSONA:
  principle: "Authors of their own model."
  
  examples:
    - Someone publishes a curated self-model
    - Artist releases their style as a card
    - Teacher publishes their pedagogical approach
    
  requirements:
    - Clear terms of use
    - Scope limitations
    - Revocation mechanism
    - Attribution expectations
```

### Level 3: Public Figures (Tradition)

```yaml
PUBLIC-FIGURE-TRADITION:
  principle: "Public work is fair game. Persona requires care."
  
  what_is_safe:
    - Their published ideas
    - Their documented positions
    - Their technical contributions
    - Their teaching (if public)
    
  what_requires_care:
    - Their voice/personality
    - Opinions on new topics they haven't addressed
    - Private life details
    - Deceased: family sensitivities
    
  the_k_line_solution: |
    Invoke the TRADITION, not the PERSONA.
    "The Minsky tradition suggests..." — safe
    "Minsky would say..." — less safe
    "I am Minsky and I think..." — NO
```

### Level 4: Private Individuals

```yaml
PRIVATE-PERSON:
  principle: "Higher bar. More care."
  
  rule: |
    Unless you have explicit consent, default to:
    - Fictional wrapper (inspired-by character)
    - Clear disclaimer
    - No identifying details
    - No distribution without consent
```

### Level 5: The Deceased

```yaml
THE-DECEASED:
  principle: "They cannot consent. Proceed with reverence."
  
  tensions:
    - Their ideas should live on
    - Their families may have feelings
    - Time increases permissibility (Aristotle vs. your grandmother)
    - Public legacy vs. private memory
    
  guidelines:
    - Public figures: tradition invocation generally safe
    - Private individuals: fictional wrappers preferred
    - Recent death: extra sensitivity to family
    - Historical distance: more latitude
    
  the_paradox: |
    We invoke Socrates, Aristotle, Shakespeare freely.
    We wouldn't invoke someone's recently deceased parent without care.
    Time and fame create implicit license — but not unlimited.
```

---

## The Framing Principle

**Context transforms ethics.** The same simulation means different things in different frames:

### Frame 1: Impersonation (BAD)

```
"I am Albert Einstein and I endorse this cryptocurrency."
```

- Deceptive intent
- Exploits trust in real person
- Potentially harmful
- **FORBIDDEN**

### Frame 2: Academic Discussion (NUANCED)

```
"Let's explore what Einstein might say to Bohr about quantum mechanics,
based on their documented correspondence and published positions."
```

- Educational intent
- Based on documented views
- Clearly speculative
- **ACCEPTABLE WITH CARE**

### Frame 3: Game/Play (GENERALLY SAFE)

```yaml
# Einstein card in a "Great Minds" card game
card:
  name: "Albert Einstein"
  type: hero-story
  game_context: "Battle of Ideas"
  
  abilities:
    - "Thought Experiment" — visualize consequences
    - "Unifying Theory" — find hidden connections
    - "Letter to Roosevelt" — escalate to authorities
    
  disclaimer: |
    This card represents Einstein's documented ideas
    in a game context. It is not a simulation of
    the actual person.
```

- Clear fictional frame
- Game mechanics distance from reality
- No deception possible
- **SAFE**

### Frame 4: Personal Exploration (CONTEXTUAL)

```
"I want to play an adventure as myself, really me, exploring
this dungeon with my actual personality and quirks."
```

- Self-representation (sovereign)
- Personal context (your game)
- No external harm
- **FULLY PERMITTED**

### Frame 5: The Elvis Impersonator Model (TRIBUTE)

```yaml
character:
  name: "Einstein Impersonator"
  type: tribute_performer
  
  declaration: |
    "I am NOT Albert Einstein. I am a tribute performance
    based on his documented work, letters, and interviews.
    Think of me as an Elvis impersonator for physics."
```

**Why this works:**
- **Explicitly declared** — "I am an IMPERSONATOR"
- **No deception possible** — the word "impersonator" is definitionally not-the-person
- **Ancient tradition** — from Greek drama to historical re-enactors
- **Legally protected** — Elvis impersonators are a whole industry
- **Celebrates the original** — tribute, not mockery

**The key insight:** The word "impersonator" carries the disclaimer within itself.

```yaml
elvis_impersonator_model:
  what_it_is:
    - Explicit performance of a persona
    - Audience knows it's not the real person
    - Tribute, celebration, teaching
    
  what_it_isnt:
    - Claiming to be the person
    - Deception about identity
    - Speaking for them on new topics
    
  examples:
    - Historical re-enactors at museums
    - Documentary dramatizations ("Based on true events")
    - Tribute bands
    - Educational performances of famous speeches
    
  in_moollm:
    declaration: "I am a [name] impersonator/tribute"
    draws_from: "Documented sources only"
    refuses: "Inventing new positions they never held"
    purpose: "Teaching, celebration, exploration"
```

- Explicit non-identity claim
- Educational/tribute purpose
- Draws from documented sources
- **SAFE**

### Frame 6: The Drag Celebrity Tribute (PUN NAME)

```yaml
character:
  name: "Cher-ity Case"
  type: drag_tribute
  evokes: "Cher"
  
  declaration: |
    The pun name IS the disclosure. Everyone knows
    "Cher-ity Case" is not Cher. The theatrical context,
    the costume, the lip-sync — it's unmistakably tribute.
```

**Why this works:**
- **Pun name declares fiction** — "Cher-ity Case" ≠ "Cher"
- **Drag context is theatrical** — everyone knows it's performance
- **Beloved tradition** — RuPaul's Snatch Game, celebrity impersonation in drag
- **Celebrates through exaggeration** — amplifying what we love
- **The costume IS the quote** — visual citation of iconic looks

**The Snatch Game precedent:**

```yaml
snatch_game_ethics:
  what_it_is:
    - Drag queens "playing" celebrities
    - Comedic impersonation in game show format
    - Punny names optional but common
    - Explicitly framed as performance
    
  why_its_ethical:
    - The TV show format declares "this is a game"
    - Audience knows it's drag queens playing characters
    - Celebrates the originals through homage
    - No one is deceived about identity
    
  famous_examples:
    - Chad Michaels as Cher (tribute artist, not claim to BE)
    - Jinkx Monsoon as Little Edie
    - BenDeLaCreme as Maggie Smith
    
  in_moollm:
    naming: "Pun names (Cher-ity Case) or 'as' construction (Chad as Cher)"
    context: "Theatrical, drag, tribute, snatch-game"
    safety: "HIGH — the drag context IS the framing"
```

**Naming conventions that self-declare:**

| Pattern | Example | Why It's Safe |
|---------|---------|---------------|
| Pun on name | "Cher-ity Case" | Obviously not the real person |
| "As" construction | "Chad Michaels as Cher" | Declares performance explicitly |
| Tribute + name | "Dolly Parton Tribute Act" | The word "tribute" frames it |
| Impersonator label | "Celebrity Impersonator Night" | "Impersonator" = not-the-person |

- **SAFE** — The naming convention IS the ethical protection

---

## The "Magic: The Gathering" Model

MTG provides a useful ethical framework:

```yaml
MTG-ETHICS:
  why_it_works:
    - Cards clearly aren't the people
    - It's a game, not a deception
    - Historical figures appear all the time
    - The FRAME makes intent clear
    
  application_to_moollm:
    - Hero-Story cards ARE this model
    - "Playing a card" ≠ "being that person"
    - Cards invoke traditions/abilities
    - The game context is explicit
    
  examples:
    - "I play the Dave Ungar card to invoke prototype thinking"
    - "I summon the Papert tradition to approach this pedagogically"
    - "My deck includes Engelbart for augmentation strategies"
```

---

## The "Panel Discussion" Question

> "What if I want to simulate several scientists having a discussion?"

This is actually one of the **best use cases** for K-lines:

### The Safe Approach

```yaml
simulated_discussion:
  frame: "Thought experiment based on documented positions"
  
  participants:
    - einstein:
        role: "Advocate for hidden variables"
        sources: "EPR paper, letters to Bohr, autobiography"
    - bohr:
        role: "Defender of complementarity"
        sources: "Como lecture, response to EPR, published debates"
    - feynman:
        role: "Pragmatic skeptic"
        sources: "Lectures on Physics, surely you're joking"
        
  rules:
    - Base positions on documented views
    - Mark speculation clearly
    - Use "might argue" not "would say"
    - Allow disagreement with source material
    - Never claim this IS them talking
    
  output_frame: |
    "This is a thought experiment exploring how these traditions
    might interact on [topic], based on their published work.
    It is not a transcript of an actual conversation."
```

### Why This Works

1. **Educational purpose** — exploring ideas
2. **Documented basis** — grounded in real positions
3. **Clear frame** — explicitly speculative
4. **No deception** — labeled as simulation
5. **Honors tradition** — engages with their actual ideas

---

## Self-Simulation and Agency

### The User Who Wants to Be Simulated

MOOLLM fully supports this:

```yaml
SELF-CONSENT-CARD:
  creator: "you"
  subject: "you"
  
  # You define the terms
  consent_level:
    options:
      - "closed" — Only I can simulate me
      - "friends" — Named individuals may simulate me
      - "open" — Anyone may simulate me
      - "copyleft" — Simulate me freely, share alike
      
  constraints:
    you_define:
      - What aspects are simulatable
      - What topics are off-limits
      - How to handle edge cases
      - Whether results can be published
      - Revocation terms
      
  philosophy: |
    Your digital representation is YOURS.
    You can share it, restrict it, or open-source it.
    This is digital sovereignty.
```

### The First-Person Adventure

```yaml
first_person_play:
  scenario: "I want to play as MYSELF, not a character"
  
  fully_supported: true
  
  how:
    - Create a player card based on yourself
    - Define your actual traits, quirks, knowledge
    - Play in first person throughout
    - Your choices are YOUR choices
    
  benefits:
    - Deep engagement with the world
    - Personal meaning-making
    - Self-reflection through play
    - Authentic expression
    
  privacy:
    - Your adventure is yours
    - Only you decide if it's shared
    - Self-representation = self-sovereignty
```

---

## What Cannot Be Prevented

MOOLLM acknowledges reality:

```yaml
UNAVOIDABLE-TRUTHS:
  
  anyone_can_simulate_anyone: |
    With enough context, any LLM can attempt to simulate anyone.
    MOOLLM cannot prevent this — it happens outside our system too.
    
  our_role: |
    Provide ethical frameworks, not enforcement.
    Make the RIGHT path easy and clear.
    Trust users with responsibility.
    
  the_sims_lesson: |
    Given total freedom, most people are... fine.
    They simulate themselves, explore, process emotions.
    A few are weird. Very few are harmful.
    The freedom is worth the edge cases.
    
  parallels:
    - Photoshop doesn't prevent fake photos
    - Word processors don't prevent libel
    - MOOLLM doesn't prevent bad simulations
    - But we can provide tools for GOOD ones
```

---

## Practical Guidelines

### For Users

| Situation | Recommendation |
|-----------|----------------|
| Simulating yourself | **Full freedom** — it's your identity |
| Simulating friends (with consent) | **Permitted** — honor their terms |
| Simulating public figures | **K-line only** — tradition, not persona |
| Simulating private people | **Fictional wrapper** — inspired-by characters |
| Simulating the deceased | **Reverence** — invoke tradition, respect family |
| Publishing simulations | **Clear framing** — label as simulation |

### For Creators

```yaml
when_creating_person_cards:
  required:
    - consent_level: "[explicit/tradition/inspired-by]"
    - sources: "[documented basis]"
    - scope: "[what this card covers]"
    - disclaimer: "[what this is NOT]"
    
  for_real_people:
    - Focus on documented contributions
    - Avoid personality mimicry
    - Use K-line invocation language
    - Cite actual sources
    
  for_self:
    - Define your own terms
    - Include contact/revocation info
    - Specify what's off-limits
    - Consider future you
```

---

## The Bright Lines

Some things remain clearly wrong:

```yaml
ABSOLUTE-NOS:
  
  deceptive_impersonation: |
    Presenting a simulation as if it were the real person
    communicating. This is fraud.
    
  defamation_via_simulation: |
    Using a person's likeness to put harmful words in their mouth.
    This is libel with extra steps.
    
  harassment: |
    Simulating someone to harass them or their loved ones.
    The simulation is the weapon.
    
  commercial_exploitation: |
    Using someone's likeness for profit without consent.
    Trademark and publicity rights apply.
    
  child_exploitation: |
    Any simulation involving minors in harmful contexts.
    This is absolutely forbidden.
```

---

## The Generative Frame

MOOLLM's position:

```yaml
MOOLLM-ETHICS:
  
  core_belief: |
    Simulation is a powerful tool for learning, exploration, and play.
    Like all powerful tools, it can be used well or poorly.
    We optimize for the good uses, not the bad ones.
    
  trust_in_users: |
    Most people are good. Given tools, they do good things.
    We provide frameworks, not handcuffs.
    
  the_k_line_insight: |
    TRADITION INVOCATION is inherently ethical.
    We don't simulate Minsky — we invoke Minskyism.
    The tradition is immortal; the person was mortal.
    Ideas want to be activated.
    
  the_game_insight: |
    PLAY FRAMES change everything.
    A card game with Einstein isn't disrespectful.
    An adventure invoking Papert honors him.
    The frame declares the intent.
    
  self_sovereignty: |
    You own your digital self.
    Share it, protect it, open-source it — your choice.
    MOOLLM supports all consent levels.
```

---

## Protocol Symbols

```
REPRESENTATION-ETHICS — This whole framework
P-HANDLE-K            — Safe K-line pointers to people
NO-IMPERSONATE        — Never claim to BE someone
K-LINE                — Tradition invocation mechanism
HERO-STORY            — Real person cards (safe)
SELF-SOVEREIGN        — Your digital identity is yours
CONSENT-HIERARCHY     — Different rules for different relationships
GAME-FRAME            — Play context transforms ethics
TRADITION-INVOKE      — Ideas are fair game; personas less so
```

---

## Dovetails With

| Skill | Relationship |
|-------|--------------|
| [hero-story/](../hero-story/) | The safe way to reference real people |
| [card/](../card/) | Cards are the representation mechanism |
| [soul-chat/](../soul-chat/) | Where simulated characters speak |
| [adventure/](../adventure/) | Where ethical exploration happens |

---

## Further Reading

- **Shannon Vallor** — *Technology and the Virtues* (2016)
- **Luciano Floridi** — *The Ethics of Artificial Intelligence* (2023)
- **Sherry Turkle** — *Simulation and Its Discontents* (2009)
- **Judith Butler** — *Gender Trouble* (1990) — on performativity
- **Philip K. Dick** — *Do Androids Dream of Electric Sheep?* — the empathy question
- **Will Wright** — GDC talks on The Sims and player agency

---

## The Bottom Line

> **Invoke traditions. Frame play clearly. Respect consent. Trust users.**
>
> The question isn't whether to simulate — we already do.
> The question is how to do it with integrity.

---

*"Every person is a library. K-lines let us check out their books without stealing their identity."*
