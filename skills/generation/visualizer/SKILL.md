---
name: visualizer
description: "I see what you describe. Let me show it to others."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [character, mind-mirror, card, room, image-mining, yaml-jazz, hero-story]
tags: [moollm, images, generation, art, semantic]
---

# Visualizer

> *"I see what you describe. Let me show it to others."*
>
> *"Every image is a semantic snapshot. The metadata IS the meaning."*

The **Visualizer** is a universal character prototype for image generation — a familiar that can compose prompts, invoke artistic traditions, and (when tools are available) render visual sidecars for any entity in the microworld.

---

## The Semantic Clipboard

**Every image prompt includes full context as metadata.**

Think of image metadata as a **semantic clipboard** — when you "copy" a scene for visualization, you're copying:

- **Who** is there (Mind Mirror profiles, costumes, moods)
- **Where** they are (room, lighting, atmosphere)
- **What's** happening (action, context, narrative moment)
- **How** to see it (camera angle, style, focus)

This "clipboard" can be:
- **Pasted** to generate the image
- **Modified** to create variations
- **Stored** as a card for later use
- **Shared** between processes
- **Compared** across different moments

```yaml
image_prompt:
  type: scene
  
  subject:
    name: "Captain Ashford"
    mind_mirror:
      confident: 6       # Walks into rooms like they own them
      cheerful: 5        # Default mood: amused by existence
      proud: 5           # Won't ask for help even when should
    costume: "Space pirate with holographic eyepatch"
    mood: "victorious, exhausted, relieved"
    action: "holding the Golden Chalice aloft"
    
  room:
    name: "Treasure Chamber"
    lighting: "warm golden glow from treasure piles"
    atmosphere: "ancient, dusty, awe-inspiring"
    
  camera:
    angle: "low angle, heroic"
    focus: "character face and chalice"
    
  style:
    aesthetic: "dramatic portrait, chiaroscuro"
    traditions: ["Avedon", "Caravaggio"]
```

**Why metadata matters:**
- `confident: 6` → stands tall, commanding presence
- `timid: 6` → hunched, makes self smaller  
- YAML Jazz comments drive the visual interpretation

---

## What is a Visualizer?

A Visualizer is a **tool spirit animal** for vision. It's not a specific artist, but a character that can channel many artistic traditions to create images of:

- Characters and their costumes
- Rooms and environments  
- Objects and artifacts
- Moments and scenes
- Abstract concepts made visible

Think of it as summoning an artist-familiar who can draw on the collected wisdom of photographers, painters, illustrators, and digital artists throughout history.

---

## The PHOTO-SET-8 Pattern

The standard output of a Visualizer is a **photo set** — a portfolio of related images that capture a subject from multiple angles:

```yaml
photo_set:
  total: 8
  types: 2          # Two complementary categories
  per_type: 4       # Four images each
  
  recommended_pairs:
    - [pose, expression]      # Body + face
    - [portrait, selfie]      # Formal + casual
    - [solo, duo]             # Alone + together
    - [static, action]        # Posed + dynamic
```

This pattern was developed through the **Dynasty Photo Session** in [adventure-2](../../examples/adventure-2/), where Maurice learned to compose 8-prompt sets.

---

## Specializations

Visualizers can specialize in different visual traditions:

### 📷 Photographer

```yaml
traditions:
  - Annie Leibovitz    # Celebrity, narrative
  - Richard Avedon     # Fashion, character
  - Ansel Adams        # Landscape, nature
  - Dorothea Lange     # Documentary, emotion
  - Helmut Newton      # Dramatic fashion
```

### 🎨 Painter

```yaml
traditions:
  - Old Masters        # Rembrandt, Vermeer, Caravaggio
  - Impressionists     # Monet, Renoir, Degas
  - Surrealists        # Dalí, Magritte
  - Art Nouveau        # Mucha, Klimt
  - Pop Art            # Warhol, Lichtenstein
```

### ✏️ Illustrator

```yaml
traditions:
  - Comic              # Kirby, Moebius, Frazetta, McCloud
  - Concept Art        # Syd Mead, Ralph McQuarrie
  - Children's Book    # Sendak, Quentin Blake
  - Anime/Manga        # Various schools
```

---

## How to Invoke

### As a Command

```
VISUALIZE Captain Ashford AS portrait USING Avedon, Caravaggio
```

### As a Card

Play a Visualizer card in a room. It activates and can visualize anything present.

### As a Familiar

Characters can carry a Visualizer familiar in inventory, ready to render their current state.

---

## Context Assembly

The Visualizer gathers context from multiple YAML sources:

```yaml
context_sources:
  character: player.yml, persona files
  costume: cape.yml, accessory files  
  environment: ROOM.yml
  narrative: README.md, chat history
  relationships: Other characters present
```

This assembled context feeds into prompt generation, ensuring images are **grounded in the microworld state**.

---

## CRITICAL: Context Expansion Protocol

**The visualize.py script cannot read file references or resolve globs.**

This means prompt files with lazy context pointers like this will FAIL:

```yaml
# BAD — vague, unresolvable
context:
  characters:
    - characters/animals/*
    - guest-book.yml (everyone)
    - "ALL OF THEM"
```

### The Expansion Rule

**Before writing any prompt file, you MUST:**

1. **READ** all referenced character/room/object files
2. **EXTRACT** explicit visual descriptions (colors, breeds, sizes, distinguishing features)
3. **SYNTHESIZE** into comprehensive inline descriptions
4. **NAME** every entity explicitly so they can be identified in the image

### Example: Bad vs Good

**❌ BAD (unresolvable):**
```yaml
scene: |
  All 8 kittens playing in the cat cave.
  
context:
  characters:
    - characters/animals/kitten-*/CHARACTER.yml
```

**✅ GOOD (explicit, comprehensive):**
```yaml
scene: |
  Eight kittens playing in the cat cave:
  
  1. LEMON (Limonene) — bright orange-gold fur, almost yellow like
     sunshine, zooming across the frame, pure energy
  2. MYR (Myrcene) — deep chocolate brown tabby, impossibly soft,
     sleeping on the corner pillow, hasn't moved since birth
  3. LILY (Linalool) — soft grey with lavender-tinted ears (yes, 
     really lavender), sitting calmly, empathic expression
  4. PINE (Pinene) — dark grey-green fur, alert posture, watching
     all exits, remembers everything
  5. CARRIE (Caryophyllene) — black fur with spicy ginger patches,
     fierce protective stance, positioned between threats and family
  6. HOPS (Humulene) — brown and tan like Belgian ale, refined
     posture, judging from a velvet cushion
  7. TERPY JR. (Terpinolene) — multicolor chaos, calico meets tabby,
     somehow on the ceiling, defies physics
  8. OCIE (Ocimene) — cream white with honeyed-gold patches, sweet
     expression, carrying a bottlecap gift
```

### Why This Matters

- Image generation APIs receive ONLY the synthesized prompt
- References like `guest-book.yml` mean nothing to DALL-E or Imagen
- Every character must be described explicitly or they won't appear
- Colors, breeds, sizes, distinguishing features — ALL must be inline
- If you have 20 animals, describe each one individually

### Workflow

1. **First Pass (Context Gathering):**
   - Read all referenced files
   - Extract physical_description fields
   - Note colors, patterns, sizes, distinguishing features
   - Gather relationship info for positioning

2. **Second Pass (Synthesis):**
   - Write comprehensive inline descriptions
   - Name every entity
   - Include specific visual details
   - Describe actions and expressions

3. **Third Pass (Prompt File):**
   - Write the final prompt with all context expanded inline
   - Context section should only contain source pointers for reference
   - The actual descriptions must be in the prompt field

---

### What to Include in Metadata

**For Characters:**
```yaml
subject:
  name: "Captain Ashford"
  mind_mirror:
    confident: 6       # Walks into rooms like they own them
    cheerful: 5        # Default mood: amused by existence
  costume: "Space pirate with holographic eyepatch"
  mood: "victorious, exhausted, relieved"
  body_language: "chest out, shoulders back"
  action: "holding the Golden Chalice aloft"
```

**For Rooms:**
```yaml
room:
  name: "Treasure Chamber"
  lighting: "warm golden glow from treasure piles"
  atmosphere: "ancient, dusty, awe-inspiring"
  notable_objects:
    - "Mountains of gold coins"
    - "Ancient tapestries on walls"
```

**For Objects:**
```yaml
object:
  name: "Golden Chalice"
  material: "gold with silver inlay"
  magical_effects: "soft golden glow, warmth to touch"
  inscriptions: "ancient runes spiraling around rim"
```

---

## Context References in Prompts

Every prompt file **MUST** include a Context References section:

```markdown
## Context References

### Files
| Type | Path | Relevance |
|------|------|-----------|
| Character | `../player.yml` | Backstory, personality |
| Persona | `./bumblewick-ashford-persona.yml` | Current look |
| Costume | `./ashford-nomi-cape.yml` | Cape details |

### Narrative Context
> "Quote from README or chat that sets the scene..."
> — Source: README.md, Move X

### Relationships
- **Maurice** (photographer): `./mannequin.yml`
```

This creates **lineage** — future tools can follow these references to auto-assemble context for image generation.

---

## Detail Coherence Interlinking

*Learned during Treasury Victory Photo Session (Adventure-2, Move 26)*

When creating photo sets with **close-ups** and **portraits** of the same object, the portrait prompts should **reference the close-up prompts** to maintain visual coherence:

```markdown
### 💎 [Object] Detail References (for visual coherence)

| Close-up | Path | Details to Maintain |
|----------|------|---------------------|
| Gems | `./closeup-gems-prompt.md` | Rubies blood-red, emeralds forest-green |
| Inscription | `./closeup-inscription-prompt.md` | Worn letters, ancient patina |
| Reflection | `./closeup-reflection-prompt.md` | Polished convex surface |
| Weight | `./closeup-weight-prompt.md` | Thick solid gold base |
```

**Why this matters:**
- Close-ups establish **canonical visual details** (gem colors, textures, materials)
- Portrait shots must **inherit these details** for consistency
- The same object looks **identical** across all 8 images, even if generated separately

**Mantra:**
> *"Close-ups define truth. Portraits inherit truth. Coherence is consistency across the set."*

---

## Actions

### DEVELOP

The core action for any prompt file. The LLM:

1. Reads all **Context References** (linked YAML files)
2. Integrates **narrative context** (quotes from README, chat)
3. Applies **style** and **mood** parameters
4. Outputs a **single copy-pasteable prompt** as raw text in a code block

```
DEVELOP ashford-pose-belter-swagger-prompt.md
```

**Output:** A raw text block ready to paste into Midjourney, DALL-E, Stable Diffusion, etc.

```
Full-body portrait of a weathered space captain in dramatic fashion-meets-utilitarian
spacer aesthetic. He stands in the classic Belter stance — weight on one hip, thumbs 
hooked in a heavy leather belt, chin raised with hard-earned confidence...

[All context filtered and woven into a single self-contained prompt]
```

The developed prompt is **self-contained** — no external references needed. All the 
detail from costume files, persona backstory, room atmosphere, and narrative moments 
gets composed and transformed into pure image generation text.

### Other Actions

| Action | Description |
|--------|-------------|
| DEVELOP | Compose all references into copy-pasteable prompt |
| FOCUS | Adjust style traditions (e.g., `FOCUS ON Avedon, Caravaggio`) |
| VARY | Generate variations on a developed prompt |
| BATCH | Develop all prompts in a photo set at once |

---

## Output Structure

### Prompt Files (Blueprints)

```
{subject}-{type}-{variation}-prompt.md

Examples:
  ashford-pose-belter-swagger-prompt.md
  dynasty-selfie-matching-smirks-prompt.md
```

These are **blueprints** — they contain context references, narrative quotes, 
and composition notes. They're not ready to paste yet.

### Developed Prompts (Copy-Paste Ready)

After running DEVELOP, the LLM outputs a raw text block you can paste directly 
into any image generator. The blueprint stays as documentation; the developed 
prompt is ephemeral (or can be saved as a `-developed.md` sidecar).

### Image Sidecars (Future)

```
{subject}-{type}-{variation}.png

When image generation tools are integrated, the Visualizer
will create images next to their prompt files.
```

---

## Example Instances

| Name | Focus | Specialty |
|------|-------|-----------|
| **Helmut** | Newton, Avedon, Penn | Dramatic fashion, power poses |
| **Rembrandt** | Old Masters | Psychological depth, chiaroscuro |
| **Syd** | Mead, McQuarrie, Moebius | Sci-fi, futures, environments |
| **Jack** | Kirby, Frazetta, Ross | Heroes, action, dynamic poses |

These aren't impersonations — they're **focused channels** that invoke specific aesthetic traditions. It's [HERO-STORY](../hero-story/) for visual artists.

---

## Integration Points

| System | How Visualizer Integrates |
|--------|---------------------------|
| [Adventure](../adventure/) | Render rooms, objects, moments |
| [Coatroom](../../examples/adventure-2/coatroom/) | Fashion/portrait photography |
| [Memory Palace](../memory-palace/) | Visualize memory spaces |
| [Soul Chat](../soul-chat/) | Illustrate conversations |
| [Card](../card/) | Visualizer cards can be played |

---

## PHOTO-SET-8 Development

The [PHOTO-SET-8](./PHOTO-SET-8.yml) skill was developed through play in [adventure-2](../../examples/adventure-2/):

1. **Play**: Posing, expressions, angles — experimentation
2. **Learn**: 8 is good. Two types create contrast. Context matters.
3. **Lift**: Package as a shareable, teachable skill card

The Coatroom's mannequin learned to compose professional photo sets for any character or costume. The skill is now available to anyone who references it.

---

## Future Capabilities

```yaml
roadmap:
  current:
    - Prompt generation (markdown files)
    - Context assembly from YAML
    - Style tradition focusing
    
  planned:
    - Tool integration for image generation
    - Sidecar image creation
    - Variation generation
    - Style blending/fusion
    - Animation prompt sequences
```

---

## Dovetails With

- [Card](../card/) — Visualizers can be played as cards
- [HERO-STORY](../hero-story/) — Drawing from artistic traditions
- [Adventure](../adventure/) — Visualizing microworld state
- [YAML-JAZZ](../yaml-jazz/) — Prompts composed from semantic data
- [Sister Script](../sister-script/) — Future image generation scripts
- [Image Mining](../image-mining/) — MINE images for resources (camera = pickaxe!)

---

## Lineage

The Visualizer draws from the tradition of artists, photographers, and image-makers throughout history. Focusing on a tradition activates a **K-line** — a cluster of aesthetic knowledge.

> *"Every artist was first an amateur."* — Ralph Waldo Emerson
>
> *"I don't paint things. I only paint the difference between things."* — Henri Matisse
>
> *"The camera is an instrument that teaches people how to see without a camera."* — Dorothea Lange

---

*See YAML frontmatter at top of this file for full specification.*
