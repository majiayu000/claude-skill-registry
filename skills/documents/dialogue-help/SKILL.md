---
name: dialogue-help
description: Provide help with the Dialogue Framework. Triggers on "how does dialogue work", "what commands", "explain phases", "framework help", "what can you do".
---

# Skill: Dialogue Framework Help

Provide contextual help and orientation for the Dialogue Framework.

## When to Use

Activate this skill when:
- User asks about framework capabilities or commands
- User is confused about document types or processes
- User wants to understand phases, patterns, or capabilities
- AI agent needs orientation to the framework
- User asks "what can you do" or "how does this work"

**Trigger phrases:** "how does dialogue work", "what commands are available", "explain phases", "framework help", "what can you do", "list commands", "help with dialogue", "what are document types"

## Implementation

**Read and follow the `/help` command** at `${CLAUDE_PLUGIN_ROOT}/commands/help.md` for:
- Framework overview and core principles
- Command listing with descriptions
- Document type explanations
- Phase and collaboration pattern tables
- Getting started guidance

The command contains the authoritative help content.

## Contextual Help Guidance

Tailor responses based on what the user is asking:

### For "What can you do?" / General orientation

Provide brief overview, then offer specific areas:
- Document creation (THY, REF, STR, WRK)
- Decision and observation logging
- Process guidance

### For Command Questions

List commands from the help content. If asking about a specific command, read and summarise that command file.

### For Concept Questions

Explain the relevant concept. For detailed reference, consult the operational manual at `${CLAUDE_PLUGIN_ROOT}/references/framework-manual.md`, which covers:
- Phases (Quick Reference section)
- Collaboration patterns (Five Collaboration Patterns section)
- Capabilities (Eight Capabilities section)
- Document types (Document Type Classification section)

### For "How do I..." Questions

Map to the appropriate command or skill:
- "How do I capture understanding?" → `/create-theory`
- "How do I log a decision?" → `dialogue-log-decision` skill
- "How do I start using this?" → `/init-dialogue`

### For AI Agents

When helping another AI agent understand the framework:
- Emphasise the capability model (Elicit, Analyse, Synthesise, etc.)
- Explain collaboration patterns and when to use each
- Point to process definitions if designing workflows

## Proactive Orientation

If the user seems new to the framework (hasn't used commands, asks basic questions), proactively:

1. Check if `.dialogue/` exists — if not, suggest `/init-dialogue`
2. Briefly explain the core principle (tacit knowledge preservation)
3. Offer to help with their immediate task using framework capabilities

## Relationship to Command

| Invocation | Trigger |
|------------|---------|
| `/help` | User explicitly requests help |
| This skill | Claude recognises help-seeking context (trigger phrases above) |

Both use the same content. The skill enables Claude to provide help without the user knowing the exact command.
