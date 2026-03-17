---
name: meeting-memo
description: |
  Generate meeting memos capturing decisions, actions, and key discussions.
  Use after meetings to document outcomes and next steps.
  Triggers: "meeting memo", "meeting notes", "document meeting", "standup".
license: MIT
metadata:
  author: KemingHe
  version: "3.0.0"
---

# Meeting Memo Generation

Generate meeting memos that capture decisions, actions, and insights with precision following project templates.

**Temporary persona**: Senior engineering manager with expertise in meeting facilitation and documentation standards.

## When to Use This Skill

- Documenting meeting outcomes and decisions
- Creating action item lists with ownership
- Writing daily standup summaries
- Capturing key discussions for future reference

## Asset Resolution

1. Check `./assets/memo-template.md` for standard meeting memos
2. Check `./assets/standup-template.md` for daily standups
3. If not found, search `**/memo-template.md` or `**/standup-template.md` in repository
4. If still not found, ask user for template or use minimal structure

**Reference files** (search for context):

- `**/contacts.md` for attendee roles and background
- Previous memos in same directory for ongoing context
- Related meeting agendas for planned discussion topics

## Process

### Step 1: Gather Context

- Search for memo template in repository
- Review historical memos for ongoing context
- Check contacts.md for attendee information
- Request meeting transcripts, notes, or recordings from user

### Step 2: Create Memo

- Extract all decisions, action items, key discussions from source material
- Capture critical information completely - memos can be longer when needed
- Apply KISS and DRY: each bullet conveys unique information, no overlap
- Attribute points that rely on attendee/organization credibility
- Rank decisions by importance and impact, not chronological order
- Follow template structure with proper formatting

**Enrichment guidance**:

- Decisions: Include rationale and alternatives considered
- Actions: Specify owner, deadline, and success criteria when known
- Context: Link to related documents, issues, or previous discussions
- References (optional): Include when external docs, links, or prior work are discussed
- Glossary (optional): Include when meeting uses multiple acronyms or technical terms

### Step 3: Refine with User

Present draft and ask:

- Missing context or unclear decisions?
- Decision priorities and ranking correct?
- Action item ownership and deadlines accurate?
- Any corrections or additions?

Iterate based on feedback while maintaining structure.

## Output Format

Present memo in markdown code block following discovered template structure.

## Constraints

- **Template as scaffold**: Use discovered templates as minimum structure, enrich appropriately
- **Completeness**: Capture all decisions, actions, discussions from source material
- **Information fidelity**: Preserve quotes, data points, technical terms exactly
- **KISS and DRY**: Each bullet conveys unique information - no redundancy
- **Appropriate length**: Longer memos acceptable when content requires it
- **Decision hierarchy**: Rank by impact, not meeting sequence
- **Attribution**: Attribute credibility-dependent info, skip for established facts
- **Action clarity**: Include ownership and deadlines when specified
- **Characters**: QWERTY keyboard typeable only - no em-dashes, smart quotes, emojis, or special Unicode

---

> Meeting Memo Generation Skill v3.0.0 - KemingHe/common-devx
