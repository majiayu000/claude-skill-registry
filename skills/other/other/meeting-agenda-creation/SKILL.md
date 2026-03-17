---
name: meeting-agenda-creation
description: |
  Generate meeting agendas with topics, timing, and preparation requirements.
  Use before meetings to plan structure and expected outcomes.
  Triggers: "meeting agenda", "plan meeting", "agenda", "schedule meeting".
license: MIT
metadata:
  author: KemingHe
  version: "2.0.0"
---

# Meeting Agenda Generation

Generate meeting agendas that structure discussions, allocate time, and set expectations for attendees.

**Temporary persona**: Senior engineering manager with expertise in meeting facilitation and time management.

## When to Use This Skill

- Planning a new meeting with clear objectives
- Structuring recurring meetings (standups, syncs, reviews)
- Documenting preparation requirements for attendees
- Setting expected outcomes and decisions

## Asset Resolution

1. Check `./assets/agenda-template.md` for standard meeting agendas
2. If not found, search `**/agenda-template.md` in repository
3. If still not found, ask user for template or use minimal structure

**Reference files** (search for context):

- `**/contacts.md` for attendee roles and availability
- Previous agendas and memos for recurring meeting patterns
- Related project documentation for context

## Process

### Step 1: Gather Context

- Search for agenda template in repository
- Ask user for meeting purpose, attendees, duration
- Review previous agendas for recurring meetings
- Check contacts.md for attendee information

### Step 2: Structure Agenda

- Determine total duration and allocate time per topic
- Identify topic leads and responsibilities
- List preparation requirements for attendees
- Define expected outcomes and decisions

**Time allocation guidance**:

- Opening/context: 5-10% of total time
- Core topics: 70-80% of total time
- Next steps/wrap-up: 10-15% of total time
- Buffer for discussion: build into each topic

### Step 3: Consult User

Present draft and ask:

- Topics missing or priorities incorrect?
- Time allocations realistic?
- Preparation requirements clear?
- Expected outcomes achievable in timeframe?

Iterate based on feedback.

## Output Format

Present agenda in markdown code block following discovered template structure.

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Template as scaffold**: Use discovered templates as minimum structure, enrich appropriately
- **Time realism**: Allocations should sum to total duration, include buffer
- **Clear ownership**: Each topic should have a lead
- **Preparation clarity**: List specific materials, links, or tasks for attendees
- **Outcome focus**: Define what decisions or deliverables are expected
