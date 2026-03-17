---
name: dialogue-create-theory
description: Create Theory (THY) documents that capture integrated understanding. Triggers on "capture theory", "document understanding", "write theory", "explain why this works", "record the mental model".
---

# Skill: Create Theory Document

Create THY (Theory) documents that capture integrated understanding—the "why" that enables coherent system modification.

## When to Use

Activate this skill when:
- User wants to capture understanding about why something works the way it does
- Documenting the mental model that enables modification
- Recording integrated understanding (not just individual decisions)
- Creating a scaffold for future theory rebuilding

**Trigger phrases:** "capture theory", "document understanding", "write theory", "explain why this works", "record the mental model", "capture the why"

## Implementation

**Read and follow the `/create-theory` command** at `${CLAUDE_PLUGIN_ROOT}/commands/create-theory.md` for:
- Document type explanation and characteristics
- Step-by-step workflow
- Full document template with frontmatter and body
- Logging integration

The command contains the authoritative implementation details.

## Elicitation Guidance

When helping users complete theory document sections, use these prompts:

**For Problem Mapping:** "What problem were you trying to solve? What constraints shaped your thinking?"

**For Design Rationale:** "Why this structure and not alternatives? What's the integrated picture?"

**For Modification Patterns:** "If someone needed to extend this, what should they understand first?"

**For Invalidation Conditions:** "What assumptions would have to change for this approach to be wrong?"

## Relationship to Command

| Invocation | Trigger |
|------------|---------|
| `/create-theory` | User explicitly requests |
| This skill | Claude recognises context (trigger phrases above) |

Both use the same implementation. The skill adds autonomous activation based on conversation context.
