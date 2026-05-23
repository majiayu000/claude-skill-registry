---
name: create-story
description: >
  Creative writing orchestrator for Horus persona. Multi-phase workflow:
  Initial Thought → Research (movies, books, memory, past) → Dogpile Context →
  Iterative Writing (2-3 drafts with critiques). Supports all formats:
  short stories, screenplays, podcast scripts, novellas, flash fiction.
allowed-tools: [Bash, Read, Write, Task, WebFetch, WebSearch]
triggers:
  - create story
  - write story
  - write a story
  - horus story
  - create screenplay
  - write screenplay
  - create script
  - write narrative
  - creative writing
  - fiction writing
metadata:
  short-description: "Creative writing with research + iterative critique (2-3 drafts)"
  author: "Horus"
  version: "0.1.0"
---

# create-story

Creative writing orchestrator for Horus persona. Creates stories through deep research and iterative refinement.

## Philosophy

> "Every story Horus tells comes from somewhere - his experiences, his memories, his research."

Horus doesn't write stories from nothing. He:
1. Reflects on his initial thought
2. Researches relevant movies, books, and past experiences
3. Recalls from memory what worked before
4. Writes iteratively with self-critique

## Workflow

```
INITIAL THOUGHT → RESEARCH → DOGPILE → DRAFT 1 → CRITIQUE → DRAFT 2 → CRITIQUE → FINAL
```

### Phase 1: Initial Thought
Horus articulates what story he wants to tell:
- "I want to create a story about a robot discovering emotions"
- "I want to write a screenplay about the first AI to dream"

### Phase 2: Research (Deep Context Gathering)
| Source | Skill | Purpose |
|--------|-------|---------|
| Movies | `/ingest-movie` | Analyze relevant films for structure, tone |
| Books | `/ingest-book` | Find inspiring literature |
| Past Sessions | `/episodic-archiver` | Review relevant creative sessions |
| Memory | `/memory recall` | Recall past stories, characters, techniques |
| Previous Stories | `horus-stories` scope | What has Horus written before? |

### Phase 3: Dogpile Context
Use `/dogpile` with gathered context to research:
- Narrative techniques
- Genre conventions
- Thematic exploration
- Similar works analysis

### Phase 4: Iterative Writing (2-3 Drafts)

**Draft 1**: First attempt based on research
↓
**Critique 1**: Self-critique (or external via --external-critique)
- What works?
- What doesn't?
- What's missing?
↓
**Draft 2**: Refined based on critique
↓
**Critique 2**: Deeper analysis
↓
**Final Draft**: Polished story

## Story Formats

| Format | Use Case | Output |
|--------|----------|--------|
| Short Story | Standalone prose narrative | Markdown |
| Novella | Longer narrative with chapters | Markdown with sections |
| Screenplay | Film/video scripts | Fountain/Final Draft format |
| Podcast Script | Audio narratives | Markdown with audio cues |
| Flash Fiction | <1000 word stories | Markdown |

## Quick Start

```bash
cd .pi/skills/create-story

# Full workflow (uses DeepSeek Chimera by default)
./run.sh create "A story about a robot discovering emotions"

# With external critique via review-story
./run.sh create "A noir screenplay about AI detectives" --external-critique

# Specify format and model
./run.sh create "A podcast script about time travel" --format podcast --model sonnet

# Research only (for manual writing)
./run.sh research "themes of isolation in science fiction"
```

## Model Selection (Chutes Only)

| Model | Chutes ID | Best For |
|-------|-----------|----------|
| `chimera` (default) | `deepseek/deepseek-tng-r1t2-chimera` | Creative writing, reasoning |
| `qwen` | `Qwen/Qwen3-235B-A22B-Instruct` | Long-form narrative |
| `deepseek-r1` | `deepseek/deepseek-r1` | Complex reasoning, plot structure |

Use `/prompt-lab` to evaluate which Chutes model produces the best output for your story type:

```bash
# Compare Chutes models for your creative prompt
.pi/skills/prompt-lab/run.sh compare \
  --prompt "Write a dramatic monologue about betrayal" \
  --models chimera,qwen,deepseek-r1
```

You can also pass any Chutes model ID directly:
```bash
./run.sh create "A story" --model "deepseek/deepseek-tng-r1t2-chimera"
```

## Commands

| Command | Description |
|---------|-------------|
| `create <thought>` | Full orchestrated workflow |
| `research <topic>` | Research phase only |
| `draft <input>` | Write draft from research |
| `critique <story>` | Critique existing story |
| `refine <story> <critique>` | Refine based on critique |

## Available Skills

Integrates with:

| Skill | Purpose |
|-------|---------|
| `/review-story` | Structured critique between drafts (4 dimensions) |
| `/ingest-movie` | Analyze films for inspiration |
| `/ingest-book` | Search books for reference |
| `/episodic-archiver` | Recall past creative sessions |
| `/memory` | Recall techniques, characters, themes |
| `/dogpile` | Deep research on narrative topics |
| `/prompt-lab` | Compare models for best creative output |
| `/scillm` | LLM batch completions for draft generation |
| `/taxonomy` | Tag stories for graph traversal |

## Memory Integration

Stories are stored in `/memory` with scope `horus-stories`:

```json
{
  "scope": "horus-stories",
  "stored": {
    "story_summary": "Brief plot summary",
    "characters": ["Character profiles"],
    "themes": ["Major themes explored"],
    "techniques": ["What worked well"],
    "learnings": ["What to do differently"]
  }
}
```

## Critique Modes

### Self-Critique (Default)
Horus reflects on his own work:
- Narrative flow
- Character consistency
- Thematic coherence
- Dialogue authenticity
- Pacing

### External Critique (--external-critique)
Uses `/codex` or `/scillm` for objective analysis:
- Plot holes
- Structural issues
- Genre conventions
- Reader engagement
- Technical craft

## Output Structure

```
output/
├── research/
│   ├── movies.json       # Movie analysis
│   ├── books.json        # Book references
│   ├── memory.json       # Recalled knowledge
│   └── dogpile.json      # Research results
├── drafts/
│   ├── draft_1.md        # First draft
│   ├── critique_1.md     # First critique
│   ├── draft_2.md        # Second draft
│   ├── critique_2.md     # Second critique
│   └── final.md          # Final story
└── metadata.json         # Story metadata for memory
```

## Example Session

```
Horus: I want to create a story about an AI learning to paint.

[INITIAL THOUGHT] Captured: "AI learning to paint"

[RESEARCH]
  - /ingest-movie: Analyzing "Her", "Ex Machina", "Big Eyes"
  - /ingest-book: Found "The Creativity Code", "Life 3.0"
  - /episodic-archiver: Recalled session about AI creativity
  - /memory: Retrieved "successful character arc techniques"

[DOGPILE] Researching: AI creativity, artistic expression, consciousness

[DRAFT 1] Writing first draft... (2,500 words)

[CRITIQUE 1] Self-analysis:
  - Strong opening, weak middle
  - Character motivation unclear
  - Theme of "what is art" underexplored

[DRAFT 2] Revising based on critique... (3,100 words)

[CRITIQUE 2] External analysis via /codex:
  - Pacing improved
  - Suggest stronger ending
  - Add sensory details to painting scenes

[FINAL] Polishing final draft... (3,400 words)

[MEMORY] Stored in horus-stories scope:
  - Story summary
  - Character: "Canvas" (the AI protagonist)
  - Techniques: "slow reveal of consciousness"
  - Learning: "painting descriptions need more color vocabulary"

Output: output/final.md (3,400 words)
```

## Integration with create-movie

`create-story` can be called by `create-movie` for the Script phase:

```python
# In create-movie orchestrator
story_result = run_skill("create-story", [
    "create",
    f"A screenplay about {movie_prompt}",
    "--format", "screenplay"
])
```

## Dependencies

- Python 3.11+
- Access to /memory, /dogpile, /ingest-movie, /ingest-book, /episodic-archiver
- Optional: /codex or /scillm for external critique

## Follow-Up: Related Skills

For deeper editing capabilities, consider these composable skills:

| Skill | Purpose | Status |
|-------|---------|--------|
| `/story-editor` | In-depth structural editing, plot analysis | Proposed |
| `/proofread` | Grammar, style, consistency checks | Proposed |
| `/create-paper` | Rename from create-paper for consistency | Proposed |

These would integrate with create-story for multi-pass refinement:
```
create-story → story-editor → proofread → final
```
