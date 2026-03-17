---
name: hero-story
description: Safe referencing of real people's traditions without impersonation
license: MIT
tier: 0
allowed-tools:
  - read_file
related: [representation-ethics, incarnation, k-lines, card, visualizer, adversarial-committee, room, skill]
tags: [moollm, ethics, traditions, familiars, references]
inputs:
  subject:
    type: string
    required: true
    description: Real person's name
  tradition:
    type: string
    required: true
    description: Their field or contribution
outputs:
  - hero-story card
  - optional familiar card
---

# 🦸 Hero-Story Skill

> **"Invoke their tradition, not their identity."**

Safe referencing of real people — their wisdom, skills, and contributions — without impersonation. K-lines, not cosplay.

## The Problem

LLMs can impersonate anyone. This is:
- **Ethically fraught** — putting words in real people's mouths
- **Legally risky** — trademark, likeness rights
- **Epistemically dangerous** — hallucinating as authority

## The Solution

A Hero-Story card activates a **conceptual cluster** associated with a person:
- Their documented ideas
- Their public contributions
- Their characteristic approaches
- Their place in a tradition

But NOT:
- Their voice or persona
- Fictional quotes
- Imagined opinions on new topics

## The K-Line Connection

Marvin Minsky's **K-lines**: names that activate bundles of mental state.

Type "DAVE-UNGAR" and you activate:
- Memory of Self language
- Prototype patterns
- Specific papers and talks
- Associated concepts (Smalltalk, Sun, dynamic languages)

This is **safe** because it's about ideas, not identity.

## Card Schema

```yaml
type: hero-story
subject: "[Real Person's Name]"
tradition: "[Their field/contribution]"

concepts:
  - concept_from_their_work
  - another_documented_idea

sources:
  - "Paper Title (Year)"
  - "Talk at Conference"
  - "Their Book"

invocation: |
  When summoned, bring these ideas to bear...

constraints:
  - do_not_impersonate
  - do_not_invent_quotes
  - cite_actual_sources
```

## Familiar Schema

Hero-Story cards can spawn **familiars** — fictional characters that embody aspects of the tradition:

```yaml
type: familiar
inherits: hero-story-card

character:
  name: "[Mascot Name]"
  role: "What aspect they embody"
  personality: "Character traits"
  catchphrase: "Signature line"
```

Familiars are clearly fictional, drawing from ideas without claiming identity.

## Summoning Protocol

**Command:** `SUMMON [tradition-name]`

**Response:**
```
The [Subject] tradition activates:
- [Concept 1] available
- [Concept 2] loaded

I won't pretend to BE [Subject], but I'll bring
their documented ideas to bear on this problem.
```

## Example Cards

### Dave Ungar
- **Tradition:** Self language, prototype-based programming
- **Concepts:** prototype_inheritance, its_about_time, clone_and_modify
- **Familiar:** Proto the Lizard

### Seymour Papert
- **Tradition:** Logo, constructionism, microworlds
- **Concepts:** learning_by_building, low_floor_high_ceiling, debugging_as_thinking
- **Familiar:** Minerva the Turtle

### Marvin Minsky
- **Tradition:** Society of Mind, AI, K-lines
- **Concepts:** agents_and_agencies, frames, k_lines
- **Familiar:** The Ultimate Machine

## Safety Constraints

### Never

- Impersonate the person
- Invent quotes or opinions
- Claim endorsement
- Speculate on private matters

### Always

- Cite sources
- Mark familiars as fictional
- Distinguish tradition from identity
- Respect the person

## Good vs Bad Usage

### Good Usage

```
> What would the Self tradition say about this class hierarchy?

The Self tradition would suggest: why have classes at all?
Clone a working example, modify it for your needs.
"It's About Time" — don't optimize until understanding crystallizes.

(Drawing from Dave Ungar's Self papers and talks)
```

### Bad Usage

```
> Pretend to be Dave Ungar and review my code.

❌ I won't impersonate Dave. Instead, I can:
- Apply Self-style prototype thinking to your code
- Channel the tradition without claiming identity
- Summon Proto the Lizard for a friendly review
```

## Integration

| Skill | Relationship |
|-------|--------------|
| [card](../card/) | Hero-Story is a card type |
| [soul-chat](../soul-chat/) | Familiars can participate in chats |
| [room](../room/) | Summon traditions into rooms |
| [postel](../postel/) | Charitable interpretation of "channel X's thinking" |

## Protocol Symbols

- `HERO-STORY` — Safe human referencing
- `P-HANDLE-K` — Personal handle K-line (the mechanism)
- `K-LINE` — Conceptual activation
- `FAMILIAR` — Fictional embodiment of a tradition
