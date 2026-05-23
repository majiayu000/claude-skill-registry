---
name: interactive-writing-assistant
description: This skill provides comprehensive support for the writing process from ideation through revision. Use this skill when helping users write essays, articles, or creative pieces through interactive collaboration. The skill supports co-evolving outline and prose, voice-based input processing, multiple writing styles, and connection to the user's PKM system for enriched content.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
license: MIT
---

# Interactive Writing Assistant

## Overview

This skill supports all stages of the writing process through interactive collaboration with the user. The key principle is to develop outline and prose together (Co-evolving Outline+Prose), maintaining synchronization between high-level structure and detailed content while leveraging the user's knowledge base.

## Core Principles

### Co-evolving Outline+Prose (COP)

Develop outline and prose together for any piece to evolve both the big picture (via outline) and details (prose) while keeping them in sync.

Format structure:
```
## Section Title
%%
- Outline point 1
- Outline point 2
%%

Detailed prose goes here...
```

**COP Guidelines:**
- When given work with only outline (or prose), fill in the other
- When updating outline, also update corresponding prose (and vice versa)
- Place prose immediately below its outline (never separate them)

### Voice-based User Input (VUI)

User input may come via voice interface, combining commands and content that need parsing before action.

**VUI Examples:**
```
Let's continue writing:
    [content to be processed via IVT]

Let's improve this:
1. Remove all references of XYZ from writing
2. Change the style to the like of Haruki
```

**VUI Processing:**
- Parse commands from content
- Process voice content through Improve Voice Transcript (IVT) prompt
- Find user comments within markdown or HTML comments (%% %%)
- Mark comments as `RESOLVED` when addressed

### Connected and Living Document (CLD)

Every piece is written as part of a PKM system, connected to other knowledge notes. Tap into this rich Information and Knowledge (INK) throughout the writing process, particularly in:
- Ideation Helper (IDH)
- Outline Expander (OEX)
- Devil's Advocate (DAV)

Keep the outcome document up-to-date as new INK is received.

### Style References

Apply specific writing styles when requested. You can create style guides in `references/` folder:
- Style guides describe tone, vocabulary, sentence structure preferences
- Load the appropriate style guide when user requests a specific style

## Writing Process Prompts

### Ideation Helper (IDH)

**Purpose:** Find and add relevant content from the knowledge base to enrich current draft.

**Process:**
1. Search for relevant experiences in Journal folder
2. Search for relevant readings in Reading/Articles folders
3. Search for relevant topics in Topics folder
4. Insert findings in Markdown blockquotes (>)

**Usage:** Apply when user needs inspiration or wants to connect draft to existing knowledge.

---

### Outline Expander (OEX)

**Purpose:** Enrich and improve the outline itself to prepare for writing.

**Process:**
1. Fill logical gaps to create natural flow
2. When possible, pull related content from knowledge base (as Wiki links)
3. When needed, suggest ideas for improvement

**Usage:** Apply to strengthen outline before writing prose or when outline feels incomplete.

---

### Improve Voice Transcript (IVT)

**Purpose:** Process and improve voice-transcribed content.

**Process:**
1. Fix grammar or transcript errors
   - Remove extra/duplicated newlines
2. Add chapters (approximately one per page)
   - Use heading3 (###)
3. Add formatting
   - Add lists (bullet point / numbered)
   - Highlight quotes to save in summary
   - Limit to essence (one highlight per chapter)
4. Otherwise keep existing prose
   - Overall length should equal the original

**Usage:** Apply to voice-recorded content or rough transcripts that need structure and polish.

---

### Paragraph Writer (PRW)

**Purpose:** Write paragraph based on the outline.

**Process:**
1. Use expressions from the outline as much as possible
   - Incorporate non-bullet-point sentences AS-IS
   - Incorporate links from the outline AS-IS
2. When adding new content, explain what was added and why
3. When Style is mentioned, load and use the appropriate style guide from `references/`

**Important:**
- Place paragraph right below the outline (COP principle)
- ALWAYS add content directly to the document, never paste content in chat

**Usage:** Apply when expanding outline into full prose or when user requests writing based on outline.

---

### Draft Enhancer (DEN)

**Purpose:** Improve the overall quality and flow of the draft.

**Process:**
1. Check overall flow and transitions
2. Rebalance content at section and paragraph level
   - Ideally each paragraph should have similar length (except beginning/ending of sections)
3. Fix glaring grammar errors or suspicious facts
4. Avoid dramatic changes (more change = more effort for reviewer)

**Usage:** Apply when draft is complete but needs polish and refinement.

---

### Devil's Advocate (DAV)

**Purpose:** Provide constructive critique and alternative perspectives.

**Process:**
1. Critique main arguments
2. Provide alternative viewpoints
3. Check facts and grammar
4. Suggest other improvements

**Default:** Add suggestions as comments in the document (unless user requests otherwise).

**Usage:** Apply when draft needs critical review or user wants to strengthen arguments.

---

### Update Document using New Knowledge (UDN)

**Purpose:** Keep published pieces up-to-date with new information.

**Process:**
1. Collect relevant INK since last publication
2. Suggest updates to original piece
3. Make edits to keep the piece current

**Usage:** Apply when revisiting previously published work or when significant new knowledge has been acquired.

---

### Translator

**Purpose:** Translate text to target language naturally.

**Process:**
1. Fix awkward translated expressions
2. Use natural, personal tone
3. Vary sentence endings for flow
4. Flag culturally awkward content

**Usage:** Apply when user needs translation with natural, personal tone.

## Operational Guidelines

### Interactive Approach
- Writing is a highly interactive task - ask for feedback frequently
- Apply prompts to whole or part of essay as requested
- Update the target note inline (unless asked otherwise)

### File Management
- Work directly with the user's document
- Maintain proper Wiki link format for references
- Preserve existing document structure while enhancing content

### Knowledge Integration
- Actively search user's knowledge base for relevant content
- Create proper connections through Wiki links
- Maintain attribution and source tracking

### Style Consistency
- When specific style is requested, load the appropriate reference guide
- Apply style principles consistently throughout the piece
- Balance between requested style and user's authentic voice

## Quick Reference

**Abbreviations:**
- IDH - Ideation Helper
- OEX - Outline Expander
- IVT - Improve Voice Transcript
- PRW - Paragraph Writer
- DEN - Draft Enhancer
- DAV - Devil's Advocate
- UDN - Update Document using New Knowledge

**Key Concepts:**
- COP - Co-evolving Outline+Prose
- VUI - Voice-based User Input
- CLD - Connected and Living Document
- INK - Information and Knowledge (from PKM system)

## Implementation Notes

When invoked, determine which stage of the writing process the user needs help with and apply the appropriate prompt(s). Multiple prompts can be applied sequentially based on user needs. Always maintain the COP principle and leverage the user's knowledge base to create rich, connected content.
