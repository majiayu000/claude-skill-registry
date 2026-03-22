---
name: chapter-writing
description: This skill should be used when the user asks to "write a chapter", "next chapter", "chapter outline", "draft chapter", "continue the story", "write a scene", "outline a chapter", or wants to write prose for a story project.
---

# Chapter Writing

## Overview

Write story chapters using an outline-first workflow. Gathers context from all other story elements (characters, world, plot) to maintain consistency, builds a beat-by-beat outline for approval, then writes full prose. After writing, updates all cross-references (chapter index, timeline, foreshadowing).

## Prerequisites

A story project must already exist with at least:
- `story.md` (story bible)
- At least one character in `characters/`
- A plot structure in `plot/_index.md` (recommended but not required for first chapters)

## Outline-First Workflow

### 1. Gather Context

Read these files to understand the current story state:

- `story.md` - genre, themes, POV, tense
- `chapters/_index.md` - what's been written, current word count
- `plot/_index.md` - arc status, what needs to happen next
- `plot/timeline.md` - chronological position

If this isn't the first chapter, also read:
- The previous chapter file - for continuity (ending state, cliffhangers, emotional tone)
- Active arc files in `plot/arcs/` - for upcoming plot beats

### 2. Determine Chapter Scope

Ask the user:
- What should this chapter cover? (or suggest based on plot arcs)
- Whose POV?
- Which location(s)?

If plot arcs exist, suggest the next logical beats to advance.

### 3. Build the Outline

Create a beat-by-beat outline listing:
- Each scene/beat and what it accomplishes
- POV character and location for each beat
- Which arc plot points are advanced
- Any foreshadowing to plant or pay off

Load the POV character's file for voice reference. Load relevant location files for setting details.

Present the outline to the user for approval. Revise until approved.

### 4. Write the Chapter

With the approved outline, write the full prose:

- Follow the POV and tense from `story.md`
- Use the POV character's voice and speech patterns from their profile
- Ground scenes in location details from worldbuilding files
- Consult `references/writing-guidelines.md` for prose craft guidance
- Use the chapter template from `references/chapter-template.md`
- Include the approved outline in the file above the prose (for reference)

Save to `chapters/chapter-{NN}.md` with appropriate frontmatter.

### 5. Post-Write Updates

After the chapter is written:

1. **Update `chapters/_index.md`** - add chapter to registry, update total word count
2. **Update `plot/timeline.md`** - add events from this chapter in chronological order
3. **Update arc files** - mark advanced plot points with chapter reference
4. **Update foreshadowing** - mark any items as `planted` or `paid-off` with chapter reference
5. **Note character changes** - if a character's status changed (injury, revelation, relationship shift), flag for the user to update the character file

Present a summary of all updates made.

## Scene Breaks

Within a chapter, separate scenes with `---`. Each scene should have a clear POV character (even if the same as the previous scene) and location.

## Revision Workflow

When asked to revise a chapter:
1. Read the existing chapter
2. Understand what needs to change
3. Make targeted edits rather than rewriting from scratch
4. Update word count in frontmatter
5. Update chapter status (draft -> revised)

## Reference Files

- **`references/chapter-template.md`** - Frontmatter and structure template for chapter files
- **`references/writing-guidelines.md`** - Prose craft guidance: show-don't-tell, POV, dialogue, pacing, scene structure, continuity
