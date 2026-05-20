---
name: storytelling-tools
description: "Build narrative capture and sharing into the system."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [card, visualizer, session-log, hero-story]
tags: [moollm, narrative, sharing, capture, moments]
---

# Storytelling Tools

**Build narrative capture and sharing into the system.**

---

## What Are Storytelling Tools?

The Sims didn't just let you play — it let you **tell stories**.

- **Family Album** — Capture screenshots with captions
- **The Sims Exchange** — Upload and download stories, families, save files
- **SimShow** — Record movies of your Sims
- **Create-a-Sim** — Model yourself and your family

The game became a platform for self-expression. Storytelling wasn't an afterthought — it was **infrastructure**.

---

## MOOLLM Storytelling Tools

| Tool | Purpose | Files |
|------|---------|-------|
| **Notebook** | Collect cards, letters, photos, memories | `notebook.yml` |
| **Letters** | Two-way communication with characters | `letter-to-*.yml` |
| **Photo Prompts** | AI-generated scene visualization | `*-photo-*.yml` |
| **README** | GitHub-publishable narrative format | `README.md` |
| **Cards** | Mintable artifacts capturing moments | `*-card.yml` |

---

## The Notebook

A portable container for memories, carried in inventory:

```yaml
notebook:
  name: "Adventure Journal"
  type: container
  
  pages:
    - type: letter
      from: "Mother"
      about: "Setting out on the quest"
      
    - type: card  
      name: "The Lamp Song"
      created_in: "start/"
      
    - type: photo_series
      title: "Victory at the Treasury"
      prompts: 8
      
    - type: recipe
      name: "Klingon Victory Hors D'oeuvres"
      ingredients: ["blue cheese", "grue"]
```

---

## Letters

Two-way communication between player and world:

```yaml
letter:
  from: "Captain Ashford"
  to: "Mother"
  
  content: |
    Dear Mother,
    
    I found the treasure! Also I killed a grue with cheese.
    You won't believe how it happened...
    
  attachments:
    - photos/victory-selfie-1.yml
    - recipes/grue-hors-doeuvres.yml
    - inventory: 1 gold coin
    
  promises_made:
    - "Return home safely"
    - "Not waste food"
    - "Write often"
```

Promises become **goals**. Goals drive **narrative**.

---

## Photo Prompts

AI-generated visualizations capture moments:

```yaml
photo_prompt:
  title: "Victory Selfie with Chalice"
  
  scene:
    location: "Treasury"
    lighting: "Golden glow from treasure piles"
    
  subject:
    character: "Captain Ashford"
    expression: "Triumphant grin"
    pose: "Holding chalice aloft"
    costume: "Battle-worn waistcoat, matching cape"
    
  style: "Rembrandt lighting, oil painting texture"
  
  references:
    - chalice.yml  # For consistent details
    - costume.yml  # For matching description
```

**Key insight:** Photos reference other objects for **coherence**. The chalice in the selfie should match the chalice description.

---

## README as Narrative

Every directory can tell its story:

```markdown
# The Adventure of Captain Ashford

## Chapter 1: A Letter from Mother

I woke up. I remembered who I was...

## Chapter 2: Into the Maze

Armed with lamp and lunch, I ventured forth...

## Artifacts Created

- [lamp-song.yml](./start/lamp-song.yml) — A song about my faithful lamp
- [victory-photos/](./end/victory-photos/) — The moment of triumph
```

**GitHub renders this beautifully.** The README IS the narrative.

---

## Sharing and Remixing

Fork the adventure. Change the story.

```bash
# Clone someone's adventure
cp -r adventure-2/ adventure-3/

# Reset for new protagonist
# Edit player.yml, clear markers, keep world
```

Every adventure is **forkable**. Every story is **shareable**.

---

## The STORYTELLING-TOOLS Protocol

From [PROTOCOLS.yml](../../PROTOCOLS.yml):

```yaml
STORYTELLING-TOOLS:
  meaning: "Build narrative capture and sharing into the system."
  origin: "The Sims — Family Album, The Sims Exchange"
  
  in_moollm:
    notebook: "Cards capture moments and artifacts"
    letters: "Communication between characters and player"
    photo_prompts: "AI-generated scene visualization"
    readme: "GitHub-publishable narrative format"
    sharing: "Fork and remix adventures"
```

---

## Dovetails With

- [card/](../card/) — Mintable artifacts
- [soul-chat/](../soul-chat/) — Character conversations
- [session-log/](../session-log/) — Append-only history
- [memory-palace/](../memory-palace/) — Spatial organization
- [procedural-rhetoric/](../procedural-rhetoric/) — Story as persuasion

---

## The Insight

> *"The game became a platform for self-expression."*
> *"Storytelling wasn't an afterthought — it was infrastructure."*

Your adventure is not just played. It's **told**, **captured**, **shared**, **remixed**.

The README on GitHub is the Family Album. The fork is the Exchange.
