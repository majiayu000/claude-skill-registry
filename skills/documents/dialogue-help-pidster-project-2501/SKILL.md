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

### Step 0: Check Interaction Mode

Read `.dialogue/config.yaml` for `interaction_mode` (default: `partnership`). Also check user's session memo for `interaction_mode_preference`. Adapt help verbosity accordingly:
- **human-led**: Concise, answer directly
- **partnership**: Balanced with suggestions
- **ai-led**: Verbose, proactive, explanatory

### Step 1: Follow the /help Command

**Read and follow the `/help` command** at `${CLAUDE_PLUGIN_ROOT}/commands/help.md` for:
- Framework overview and core principles
- Command listing with descriptions
- Document type explanations
- Phase and collaboration pattern tables
- Getting started guidance

The command contains the authoritative help content.

### Quick Reference

For skill discovery, point users to: `${CLAUDE_PLUGIN_ROOT}/references/quick-reference.md`

This consolidated reference shows all commands and skills with trigger phrases in a scannable format.

## Contextual Help Guidance

Tailor responses based on what the user is asking:

### For "What can you do?" / "What can I do right now?" / General orientation

**Discovery-first**: Start with the user's goal, not feature lists.

Ask: "What do you want to create or accomplish?"

If they want a capabilities overview, group by intent:
- **Capture understanding**: Create Theory, Reference, Strategy documents
- **Track decisions**: Say "I decided..." or use `/create-adr` for architecture decisions
- **Manage work**: "create task", "status", "next task"
- **Preserve context**: "save session" at end of work

In **ai-led mode**, proactively demonstrate: "Try saying 'I decided to use TypeScript' and watch what happens."

In **human-led mode**, point to quick reference: "See `references/quick-reference.md` for full list."

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

| Question | Answer |
|----------|--------|
| "How do I log a decision?" | Say "I decided to..." or "let's go with..." |
| "How do I capture understanding?" | `/create-theory` for integrated knowledge |
| "How do I document a meeting?" | `/create-note` for ephemeral outputs |
| "How do I create a task?" | Say "create task for..." |
| "How do I see what's in progress?" | Say "status" or "what tasks" |
| "How do I record an observation?" | Say "I noticed..." or "log observation" |
| "How do I save context?" | Say "save session" or "end session" |
| "How do I check phase readiness?" | Say "assess phase" or "ready to proceed" |
| "How do I get less/more help?" | `/set-mode human-led` or `/set-mode ai-led` |
| "How do I start using this?" | `/init-dialogue` (if not initialised) |
| "How do I see all capabilities?" | `/help skills` or see `references/quick-reference.md` |

In **ai-led mode**, provide example trigger phrases for each.

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
