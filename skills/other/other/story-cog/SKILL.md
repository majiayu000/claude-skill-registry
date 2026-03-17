---
category: Lifestyle
id: story-cog
name: Story Cog
description: Creative writing and storytelling powered by CellCog. Create stories, novels, screenplays, fan fiction, world building, character development, narrative design. AI-powered creative writing assistant.
metadata:
  openclaw:
    emoji: "📖"
author: CellCog
dependencies: [cellcog]
---

# Story Cog - Storytelling Powered by CellCog

Create compelling stories with AI - from short fiction to novels to screenplays to immersive worlds.

---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you what's possible.

**Quick pattern (v1.0+):**
```python
# Fire-and-forget - returns immediately
result = client.create_chat(
    prompt="[your story request]",
    notify_session_key="agent:main:main",
    task_label="story-creation",
    chat_mode="agent"  # Agent mode for most stories
)
# Daemon notifies you when complete - do NOT poll
```

---

## What Stories You Can Create

### Short Fiction

Complete short stories:

- **Flash Fiction**: "Write a 500-word horror story that ends with a twist"
- **Short Stories**: "Create a 3,000-word sci-fi story about first contact"
- **Micro Fiction**: "Write a complete story in exactly 100 words"
- **Anthology Pieces**: "Create a short story for a cyberpunk anthology"

**Example prompt:**
> "Write a 2,000-word short story:
> 
> Genre: Magical realism
> Setting: A small Japanese village with a mysterious tea shop
> Theme: Grief and healing
> 
> The protagonist discovers that the tea shop owner can brew memories into tea.
> 
> Tone: Melancholic but hopeful. Studio Ghibli meets Haruki Murakami."

### Novel Development

Long-form fiction support:

- **Novel Outlines**: "Create a detailed outline for a fantasy trilogy"
- **Chapter Drafts**: "Write Chapter 1 of my mystery novel"
- **Character Arcs**: "Develop the protagonist's arc across a 3-act structure"
- **Plot Development**: "Help me work through a plot hole in my thriller"

**Example prompt:**
> "Create a detailed outline for a YA fantasy novel:
> 
> Concept: A magic school where students' powers are tied to their fears
> Protagonist: 16-year-old who's afraid of being forgotten
> Antagonist: Former student whose fear consumed them
> 
> Include:
> - Three-act structure
> - Major plot points
> - Character arcs for 4 main characters
> - Magic system explanation
> - Potential sequel hooks"

### Screenwriting

Scripts for film and TV:

- **Feature Scripts**: "Write the first 10 pages of a heist movie"
- **TV Pilots**: "Create a pilot script for a workplace comedy"
- **Short Films**: "Write a 10-minute short film script about loneliness"
- **Scene Writing**: "Write the confrontation scene between hero and villain"

**Example prompt:**
> "Write a cold open for a TV drama pilot:
> 
> Show concept: Medical thriller set in a hospital hiding dark secrets
> Tone: Tense, mysterious, hook the audience immediately
> 
> The scene should:
> - Introduce the hospital setting
> - Hint at something wrong without revealing it
> - End on a moment that makes viewers need to know more
> 
> Format: Standard screenplay format"

### Fan Fiction

Stories in existing universes:

- **Continuations**: "Write a story set after the events of [series]"
- **Alternate Universes**: "Create an AU where [character] made a different choice"
- **Crossovers**: "Write a crossover between [universe A] and [universe B]"
- **Missing Scenes**: "Write the scene that happened between [event A] and [event B]"

### World Building

Create immersive settings:

- **Fantasy Worlds**: "Design a complete magic system for my novel"
- **Sci-Fi Settings**: "Create the political structure of a galactic empire"
- **Historical Fiction**: "Research and outline 1920s Paris for my novel"
- **Mythology**: "Create a pantheon of gods for my fantasy world"

**Example prompt:**
> "Build a complete world for a steampunk fantasy:
> 
> Core concept: Victorian era where magic is industrialized
> 
> I need:
> - Geography (3 major nations)
> - Magic system and its limitations
> - Social structure and conflicts
> - Key historical events
> - Major factions and their goals
> - Technology level and aesthetics
> - 5 interesting locations with descriptions"

### Character Development

Deep character work:

- **Character Bibles**: "Create a complete character bible for my protagonist"
- **Backstories**: "Write the backstory of my villain"
- **Dialogue Voice**: "Help me develop a unique voice for this character"
- **Relationships**: "Map out the relationships between my ensemble cast"

---

## Story Genres

| Genre | Characteristics | CellCog Strengths |
|-------|-----------------|-------------------|
| **Fantasy** | Magic, world building, epic scope | Deep world creation, consistent magic systems |
| **Sci-Fi** | Technology, speculation, ideas | Hard science integration, future extrapolation |
| **Mystery/Thriller** | Suspense, clues, twists | Plot structure, misdirection, pacing |
| **Romance** | Emotional depth, relationships | Character chemistry, emotional beats |
| **Horror** | Fear, atmosphere, dread | Tension building, psychological depth |
| **Literary** | Theme, style, meaning | Nuanced prose, thematic depth |

---

## Chat Mode for Stories

| Scenario | Recommended Mode |
|----------|------------------|
| Short stories, scenes, character work, outlines | `"agent"` |
| Complex narratives, novel development, deep world building | `"agent team"` |

**Use `"agent"` for most creative writing.** Short stories, individual scenes, and character development execute well in agent mode.

**Use `"agent team"` for narrative complexity** - novel-length outlines, intricate plot development, or multi-layered world building that benefits from deep thinking.

---

## Example Prompts

**Complete short story:**
> "Write a complete 2,500-word science fiction short story:
> 
> Title: 'The Last Upload'
> Concept: In a world where consciousness can be uploaded, one person chooses to be the last to die naturally
> 
> Structure: Non-linear, moving between their final day and key memories
> Tone: Philosophical, bittersweet
> 
> End with an ambiguous moment that makes readers question their own choice."

**Character development:**
> "Create a complete character bible for a morally complex antagonist:
> 
> Setting: Modern political thriller
> Role: Senator who believes they're saving the country through corrupt means
> 
> Include:
> - Detailed backstory (childhood, formative events)
> - Psychology (fears, desires, defense mechanisms)
> - Relationships (family, allies, enemies)
> - Speech patterns and mannerisms
> - Their 'truth' they tell themselves
> - What would make them change"

**World building:**
> "Design the magic system for a fantasy novel:
> 
> Constraints:
> - Magic has a real cost (not just tiredness)
> - Some people are born with it, some earn it
> - It should enable interesting conflicts
> 
> I need:
> - How magic works mechanically
> - Its limitations and costs
> - How society treats magic users
> - How it's learned/controlled
> - 5 example uses (combat, utility, creative)
> - Potential for abuse and safeguards"

---

## Tips for Better Stories

1. **Genre expectations**: Readers have expectations. Honor them or subvert them intentionally, but know what they are.

2. **Character drives plot**: Give CellCog clear character motivations. Plot emerges from characters wanting things.

3. **Specific details**: "A coffee shop" is generic. "A coffee shop with mismatched furniture and a cat named Hemingway" is memorable.

4. **Emotional truth**: Even in fantasy, the emotions should feel real. Specify the emotional journey you want.

5. **Show, don't tell**: Ask for scenes, not summaries. "Write the moment she realizes..." not "Describe that she was sad."

6. **Iterate**: First drafts are starting points. Use CellCog to revise, expand, and refine.
