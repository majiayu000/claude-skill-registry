---
name: dialogue-create-note
description: Create Note (NOT) documents for transient process artefacts. Triggers on "capture notes", "document meeting", "record workshop", "save analysis", "interview notes", "exploration notes".
---

# Skill: Create Note Document

Create NOT (Note) documents that capture transient process artefacts—notes, analysis, and workshop outputs.

## When to Use

Activate this skill when:
- Capturing meeting or interview notes
- Recording workshop outputs
- Documenting analysis in progress
- Preserving exploration results
- Any ephemeral content that may contribute to standing documents

**Trigger phrases:** "capture notes", "document meeting", "record workshop", "save analysis", "interview notes", "exploration notes", "note document"

## Implementation

**Read and follow the `/create-note` command** at `${CLAUDE_PLUGIN_ROOT}/commands/create-note.md` for:
- Document type explanation and capture window concept
- Step-by-step workflow with date-based ID generation
- Full document template with frontmatter
- Observation logging integration

The command contains the authoritative implementation details.

## Critical: Capture Window

Note documents have a **capture window**. Tacit understanding not recorded at creation time is **permanently lost**.

When this skill activates, act immediately:
1. Don't delay—create the document now
2. Prompt for key insights while context is fresh
3. Ask: "What tacit understanding do you have right now that won't be obvious later?"

## Contribution Tracking

Always ask: "Which standing document should this contribute to?"

Update `not.contributes_to` in frontmatter. This enables traceability from ephemeral capture to standing documents.

## Relationship to Command

| Invocation | Trigger |
|------------|---------|
| `/create-note` | User explicitly requests |
| This skill | Claude recognises context (trigger phrases above) |

Both use the same implementation. The skill adds autonomous activation and emphasises immediate capture.
