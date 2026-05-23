---
name: fiction
description: This skill should be used when the user asks to "write a chapter", "write prose", "continue the story", "develop a character", "review my chapter", "critique my manuscript", "write a synopsis", "summarize my story", "plan my novel", "outline my book", "check for consistency", or mentions fiction writing, novels, short stories, scenes, or narrative craft.
---

# Fiction

A complete system for writing fiction—from initial concept through final draft.

## Commands

| Command | Purpose |
|---------|---------|
| `/fiction:new` | Start new project from scratch (interactive wizard) |
| `/fiction:go` | Resume a project (load context + suggest what to do next) |
| `/fiction:plan` | Design story architecture (premise, theme, ending) |
| `/fiction:outline` | Create chapter and scene breakdown |
| `/fiction:character` | Develop a character document |
| `/fiction:review` | Review current chapter (iterative feedback) |
| `/fiction:critique` | Full manuscript review (NYT/New Yorker style) |
| `/fiction:synopsis` | Generate synopsis (long/medium/short) for pitches |
| `/fiction:next` | Get suggestion for what to work on next |
| `/fiction:status` | Quick project status |
| `/fiction:reconcile` | Audit project against current conventions, offer updates |
| `/fiction:edit` | Line-level editing (spelling, grammar, word echoes) |
| `/fiction:language` | Verify foreign language phrases (grammar, period accuracy) |
| `/fiction:notes` | Collect and process inline editing markers |
| `/fiction:cover` | Generate cover art prompts for image generation |
| `/fiction:naming` | Generate and validate book title options |
| `/fiction:build` | Build EPUB for reading (`--sync` preserves highlights) |

## Natural Language Triggers

Beyond commands, respond to requests like:

- "Write chapter 8"
- "Continue from where we left off"
- "This scene isn't working—help me fix it"
- "Develop the antagonist's backstory"
- "Check this chapter for consistency issues"

## Agents

Select the appropriate agent based on task:

| Agent | Use Case | Model |
|-------|----------|-------|
| `new-project` | Start from scratch (Socratic wizard) | opus |
| `writer` | Writing prose, chapters, scenes | opus |
| `architect` | Story structure, premise, ending | opus |
| `outliner` | Chapter breakdown, scene beats | sonnet |
| `character-developer` | Character documents | opus |
| `chapter-reviewer` | Iterative chapter review | sonnet |
| `editor` | Line-level polish (spelling, grammar, echoes) | sonnet |
| `critique` | Full manuscript review | opus |
| `synopsis` | Plot synopsis for queries/pitches | opus |
| `continuity` | Consistency checking | haiku |
| `next` | Project navigation | haiku |
| `scene-analyzer` | Scene diagnosis | sonnet |
| `voice-analyzer` | POV/tense checking | haiku |
| `world-builder` | Settings, systems | sonnet |
| `cover-artist` | Book cover art prompts | opus |
| `naming` | Book title generation and validation | opus |
| `language-checker` | Foreign phrase verification | sonnet |

### Guest Critics

Summon a specific voice for manuscript review:

| Agent | Voice | Best For |
|-------|-------|----------|
| `stephen-king` | Direct, no-BS, story-focused | Commercial fiction, horror, thriller |
| `ursula-le-guin` | Thoughtful, world as meaning | Fantasy, science fiction |
| `james-wood` | Deeply literate, sentence-level | Literary fiction |
| `roxane-gay` | Culturally aware, emotionally honest | Contemporary fiction |

## Craft Reference Files

Consult reference files for craft guidance:

| Problem | Reference |
|---------|-----------|
| Story feels aimless | `../references/story-structure.md` |
| Scene drags | `../references/scene-structure.md` |
| Flat characters | `../references/character.md` |
| Stilted dialogue | `../references/dialogue.md` |
| Prose lacks rhythm | `../references/prose-style.md` |
| Pacing issues | `../references/pacing.md` |
| Weak opening | `../references/openings.md` |
| Unsatisfying ending | `../references/endings.md` |
| Genre expectations | `../references/genre-conventions.md` |
| Common mistakes | `../references/anti-patterns.md` |
| Process and mindset | `../references/craft-wisdom.md` |
| Audiobook readiness | `../references/audiobook-considerations.md` |

## Project Structure

Detect and work with these project structures:

### Standalone Novel

```
/my-novel
├── README.md           # Overview, status, key decisions, ⚓ anchored
├── progress.md         # Review state (updated by review commands)
├── characters/         # Character documents
├── world/              # Setting documents
├── craft/              # Tone guide
├── chapters/           # Chapter files
└── themes.md           # Theme document
```

### Multi-Book Series

```
/my-series
├── README.md           # Series overview
├── series/             # Series-level material
│   ├── series-architecture.md  # ⚓ Anchored series constraints
│   ├── progress.md     # Series-level review state
│   ├── characters/
│   ├── world/
│   └── ...
└── book-n-title/       # Individual books
    ├── progress.md     # Book-level review state
    └── chapters/
```

## Core Principles

Apply these principles when writing or reviewing:

1. **Story = Character + Change** — Plot is what happens; story is what it means.
2. **Scene Economy** — Every scene must do at least two things.
3. **Specificity Creates Universality** — Concrete details create resonance.
4. **Earned Moments** — Plant before harvest.
5. **Trust the Reader** — Show, don't tell. Imply, don't explain.
6. **Write for the Ear** — Modern books become audiobooks. Clear attribution, distinct voices, no visual-only elements.

## Decision Guides

### POV Selection
- **First person**: Deep intimacy, unreliable narrator possible
- **Third limited**: Balance of intimacy and flexibility, most common
- **Third omniscient**: God's-eye view, good for epic scope

### Tense Selection
- **Past tense**: Traditional, invisible, readers expect it
- **Present tense**: Immediacy, urgency

### Scene vs. Summary
- **Scene**: Crucial moments, turning points, high emotion
- **Summary**: Routine events, transitions
- **Rule**: If it matters, show it.

## Workflow

### New Project
Run `/fiction:new` — interactive wizard guides you through:
1. Discovery (find the heart of your story)
2. Architecture (premise, theme, arc, ending)
3. Characters (protagonist, supporting cast)
4. World (if needed)
5. Outline (chapter breakdown)

Everything saved as you go. Socratic dialogue helps you discover what you already know.

### Existing Project
Run `/fiction:go` to load the project and see what to work on next.

### After Plugin Updates
1. Run `/fiction:reconcile` to audit project against current conventions
2. Review recommendations and apply updates as desired

### Writing Loop
1. Write chapter (invoke `writer` agent)
2. Run `/fiction:review` for iterative feedback
3. Apply suggested revisions
4. Repeat until chapter complete
5. Run continuity check periodically

### Completion
When manuscript is complete, run `/fiction:critique` for full literary review.

## Large Manuscript Efficiency (50k+ Words)

For novels with 15-25+ chapters, use parallel agent deployment to dramatically reduce processing time:

### Parallel-Capable Tasks

| Task | Approach | Speedup |
|------|----------|---------|
| **Editing all chapters** | Spawn one editor agent per chapter | ~20× for 20 chapters |
| **Reviewing all chapters** | Spawn one chapter-reviewer per chapter | ~20× |
| **Continuity checking** | Phase 1: parallel fact extraction; Phase 2: comparison | ~3-4× |
| **Full critique** | Parallel chapter analysis, then unified synthesis | ~2-3× |

### How It Works

When using commands like `/fiction:edit all` or `/fiction:review all`:
1. Identify all chapters to process
2. **Launch agents in parallel** using the Task tool (one call per chapter, same message)
3. Agents run concurrently, each returning structured output
4. Main conversation aggregates results and updates `progress.md`

### Sequential Tasks

Some tasks must remain sequential:
- **Writing** — Each chapter builds on the previous
- **Outlining** — Structure depends on what comes before
- **Architecture** — Single coherent vision needed

### Memory Note

Parallel agents don't share memory. Pass necessary context (character docs, tone guide) to each agent explicitly.
