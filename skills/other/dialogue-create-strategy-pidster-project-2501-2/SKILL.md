---
name: dialogue-create-strategy
description: Create Strategy (STR) documents for rationale, decisions, and business justification. Triggers on "document strategy", "record strategic decision", "capture rationale", "business case", "project charter".
---

# Skill: Create Strategy Document

Create STR (Strategy) documents that capture rationale, decisions, and business justification.

## When to Use

Activate this skill when:
- User makes or discusses a strategic decision
- Documenting business cases or justifications
- Recording project direction or scope decisions
- Capturing rationale that should persist

**Trigger phrases:** "document strategy", "record strategic decision", "capture rationale", "business case", "project charter", "record this decision", "document the direction"

**Note:** For formal architecture decisions requiring alternatives analysis, use the **dialogue-create-adr** skill instead.

## Implementation

**Read and follow the `/create-strategy` command** at `${CLAUDE_PLUGIN_ROOT}/commands/create-strategy.md` for:
- Document type explanation and when to use vs ADR
- Step-by-step workflow
- Full document template with frontmatter
- Decision logging integration

The command contains the authoritative implementation details.

## Decision Logging

Strategy documents automatically integrate with the decision log via the **dialogue-log-decision** skill. This creates cross-references:
- Decision log entry references the STR document
- Provides traceability between decisions and their full rationale

## Relationship to Command

| Invocation | Trigger |
|------------|---------|
| `/create-strategy` | User explicitly requests |
| This skill | Claude recognises context (trigger phrases above) |

Both use the same implementation. The skill adds autonomous activation when strategic decisions emerge in conversation.
