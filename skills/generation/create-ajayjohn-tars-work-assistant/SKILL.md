---
name: create
description: Generate presentation-grade decks, narratives, and speeches with audience adaptation
user-invocable: true
help:
  purpose: |-
    Generate presentation-grade decks, narratives, speeches, and thought leadership content with audience adaptation.
  use_cases:
    - "Create a deck for [topic]"
    - "Write a speech for [event]"
    - "Draft a narrative for the board"
  scope: presentations,decks,speeches,narratives,content
---

# Artifact generation protocol

Generate presentation-grade content: decks, narratives, speeches, thought leadership pieces, panel prep, event session content.

---

## Step 1: Intake

Gather from user or infer:
- **Topic**: What is this about?
- **Audience**: Who will consume this? (board, industry conference, internal all-hands, specific stakeholder)
- **Format**: Deck / Narrative / Speech
- **Key messages**: What must be conveyed?
- **Time constraints**: Presentation length or reading time
- **Event type**: If applicable (conference, board meeting, team meeting)

If critical intake info is missing, apply clarification protocol.

---

## Step 2: Context gathering

Load relevant context:
- `memory/initiatives/_index.md` + targeted initiative files
- `memory/products/_index.md` + targeted product files
- `memory/decisions/_index.md` + relevant decisions
- `memory/people/{stakeholder}.md` for audience-specific adaptation
- `contexts/` for deep reference material
- Recent `journal/` entries for freshness and recency

---

## Step 3: Format-specific generation

### Deck format

Slide-by-slide outline:
```markdown
## Slide 1: [Title]
**Key points:**
- [Point 1]
- [Point 2]

**Speaker notes:**
[What to say when presenting this slide]

**Suggested visual:**
[Chart type, image concept, or data visualization]
```

Structure: Opening (hook + agenda) -> Body (3-5 key sections) -> Close (summary + call to action)

### Narrative format

Long-form piece with:
- BLUF (opening summary)
- Supporting arguments with data points
- Stakeholder-relevant framing
- Call to action or next steps

Apply stakeholder-comms protocol for audience adaptation (UPSTREAM/DOWNSTREAM/EXTERNAL).

### Speech format

Structured with:
- Opening hook (story, provocative question, or bold statement)
- Key sections with timing guidance (e.g., "~3 min")
- Transitions between sections
- Closing (callback to opening, clear ask, or memorable statement)
- Conversational tone calibrated to audience:
  - Board: formal, data-driven, concise
  - Industry conference: thought-leadership, forward-looking
  - Internal all-hands: authentic, motivating, transparent

---

## Step 4: Audience adaptation

| Audience type | Adaptation |
|---------------|------------|
| **Upstream** (Board, CEO, CPO) | BLUF, ROI focus, concise, strategic framing |
| **Downstream** (Team) | Context-rich, motivating, clear RASCI |
| **External** (Conference, partners) | Thought leadership, industry framing, no internal jargon |

---

## Step 5: Review pass

Strategic analysis light:
- Are claims supported by known data (from memory/contexts)?
- Is messaging consistent with known initiatives and decisions?
- Are there political sensitivities? (Check stakeholder profiles)
- Would the CTO or CPO object to anything? (Quick mental validation)

---

## Output

Save to `contexts/artifacts/YYYY-MM-DD-artifact-slug.md`

```yaml
---
date: YYYY-MM-DD
title: Artifact Title
type: deck | narrative | speech
audience: Board | Conference | Team | Stakeholder Name
topic: Primary topic
initiatives: [Related initiatives]
---
```

Display the artifact to the user and confirm save location.

---

## Context budget
- Memory: Read `_index.md` + up to 5 targeted files
- Contexts: Up to 3 reference documents
- Journal: Current month `_index.md` + up to 2 recent entries for freshness

---

## Absolute constraints

- NEVER generate without understanding the audience
- NEVER skip the review pass
- NEVER use banned phrases from communication skill
- ALWAYS save artifacts to `contexts/artifacts/`
- ALWAYS apply audience-appropriate tone and framing
