---
name: plot-structure
description: This skill should be used when the user asks to "create a plot arc", "story structure", "add a plot point", "story timeline", "track foreshadowing", "pacing", "act structure", "story arc", "plot outline", or wants to plan and manage the narrative structure of a story.
---

# Plot Structure

## Overview

Plan and manage story arcs, plot points, foreshadowing, and narrative timeline. Each arc is a markdown file in `plot/arcs/` with a chronological timeline maintained in `plot/timeline.md`. The plot index tracks all arcs, their status, and theme coverage.

## Prerequisites

A story project must already exist (created via the story-init skill). Verify by checking for `story.md` in the project root.

## Choosing a Story Structure

1. Read `story.md` for genre and themes
2. Consult `references/structure-models.md` for available structures
3. Recommend a structure based on genre (default to three-act if unclear)
4. Update `plot/_index.md` frontmatter `structure` field
5. Populate the story structure section with the beat sheet

## Creating an Arc

1. Read `story.md` for themes
2. Read `plot/_index.md` for existing arcs
3. Read `characters/_index.md` to understand available characters
4. Ask for:
   - Arc name
   - Type (main, subplot, character, thematic)
   - Which characters are involved
   - Which themes it serves
5. Build the arc through conversation: setup, escalations, climax, resolution
6. Write the file using `references/arc-template.md`
7. Save to `plot/arcs/{arc-name-kebab}.md`
8. Update `plot/_index.md` arcs table
9. Update theme tracking in `plot/_index.md`
10. If characters are referenced, verify they exist in `characters/`

## Managing Plot Points

Plot points live within arc files in the "Plot Points" table. When adding a plot point:

1. Read the relevant arc file
2. Add the plot point to the table with chapter reference (if known)
3. Add the event to `plot/timeline.md` in chronological order
4. If the plot point involves foreshadowing, add it to the arc's foreshadowing table

## Timeline Management

The timeline at `plot/timeline.md` is a chronological master list of all story events across all arcs.

When adding events:
- Insert in chronological order
- Link to the relevant arc and chapter
- Keep entries concise (one line per event)

When reviewing the timeline:
- Check for chronological consistency
- Identify pacing issues (too many events clustered, long gaps)
- Flag arcs that haven't progressed

## Foreshadowing Tracking

Each arc tracks its own foreshadowing in the "Foreshadowing" table:
- **Planted:** What hint or setup is placed
- **Payoff:** What the payoff will be
- **Chapter Planted / Chapter Payoff:** Where each occurs
- **Status:** `planted` or `paid-off`

During chapter writing, flag any `planted` items that haven't been paid off as reminders.

## Cross-Referencing

- Arcs reference characters via frontmatter `characters` field
- Arcs reference themes via frontmatter `themes` field
- Plot points reference chapters
- Timeline entries link arcs and chapters
- Theme tracking in `plot/_index.md` maps themes to arcs and chapters

## Reference Files

- **`references/arc-template.md`** - Template for arc files with frontmatter and sections
- **`references/structure-models.md`** - Story structure models (three-act, hero's journey, save the cat, kishotenketsu, five-act) with beat sheets
