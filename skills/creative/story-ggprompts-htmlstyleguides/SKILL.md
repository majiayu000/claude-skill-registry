---
name: story
description: Build an interactive educational story with a style guide aesthetic
argument-hint: <style-name> [topic-hint]
allow-model-invocation: true
---

# Build an Interactive Story

Create an interactive educational story using **$ARGUMENTS**.

Follow the full conventions in `stories/CLAUDE.md`. The story must be self-contained HTML with inline CSS/JS, 10-15 scenes, 3-5 branching points, 2-3 endings, and keyboard navigation (1-9 keys).

## Phase 0 — Plan (interactive)

1. Parse the argument: first word is the style name, optional remaining words hint at the topic.
2. Read the **Style Guide Catalog** table in `README.md` to confirm the style is available (empty Story column) and see what's already taken.
3. Read the chosen style's HTML file from `styles/{name}.html` to extract the design system.
4. Read `stories/CLAUDE.md` for the template and conventions.
4. Read 1 existing story to match structure — skim for the STORY data format, engine pattern, and component mapping.
5. If no topic was given:
   - Research the style's cultural/historical period
   - Propose 2-3 story concepts that thematically match the aesthetic
   - Ask the user to pick one
6. Propose the story arc: title, setting, 10-15 scene outline with branching diagram, key historical facts, and how style components map to narrative functions (e.g., "cards = case files", "alerts = discoveries").
7. Discuss with the user before proceeding.

## Phase 1 — Research (parallel Sonnet subagents)

Launch 2-3 **sonnet** subagents in parallel to research:
- **Historical facts**: Real names, dates, numbers, events for the chosen topic. Need 8-12 concrete facts.
- **Cultural context**: Period details, atmosphere, vocabulary appropriate to the era.
- **Style component mapping**: How to repurpose the style guide's CSS classes for narrative elements.

Each subagent returns structured research notes.

## Phase 2 — Build (sequential Opus subagents)

Use 3-4 sequential **opus** subagents:

1. **First agent**: Create the full HTML file with adapted CSS, title screen with back-to-stories link, scene wrapper structure, and the story engine JavaScript. Write the first 5 scenes of the STORY object. Include CSS for scene types (narration, investigation, confrontation, ending).
2. **Second agent**: Read the file, add scenes 6-10 (or remaining scenes). Ensure branching points connect correctly.
3. **Third agent**: Read the file, add remaining scenes and endings. Verify all `next` values point to defined scenes. Ensure every scene has a `fact` property. Test that no orphan scenes exist.
4. **Fourth agent (polish)**: Read complete file. Verify scene graph integrity (no dead ends, no orphans), keyboard navigation works, clue tracker collects facts, all historical content is accurate.

**Critical rules for build agents:**
- Each agent MUST read the current file before writing
- All `next` values in choices must reference existing scene IDs in the STORY object
- Every scene needs: `year`, `era`, `content`, `fact`, `choices`
- Endings should offer "Play Again" (next: 'intro') and "Back to Stories" (next: '_exit')
- Back-to-stories link on title screen: `<a href="index.html">`

## Phase 3 — Brief & Index

1. Write a research brief to `stories/briefs/{style-name}-brief.md` documenting the historical facts, story arc, and component mapping.
2. Read `stories/index.html` to understand the card format.
3. Add a card for the new story with: scene count, ending count, style name, title, description.
4. Update the **Style Guide Catalog** table in `README.md` — add the story title in the Story column for the chosen style.
5. Commit with message: `Add {title} interactive story ({style-name} style)`
6. Push using: `git config --global credential.helper store && echo "https://GGPrompts:$(gh auth token --user GGPrompts)@github.com" > ~/.git-credentials && git push origin main`
