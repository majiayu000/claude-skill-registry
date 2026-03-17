---
name: design-tracker
description: PROACTIVELY track and document project design decisions without being asked. Activate automatically when detecting architecture discussions, implementation decisions, pattern choices, library selections, or any technical decisions. Also use when user explicitly says "記録して", "設計どうなってる", "record this". Do NOT wait for user to ask - record important decisions immediately.
---

# Design Tracker Skill

## Purpose

This skill manages the project's design documentation (`.claude/docs/DESIGN.md`). It automatically tracks:
- Architecture decisions
- Implementation plans
- Library choices and their rationale
- TODO items and open questions

## When to Activate

- User discusses architecture or design patterns
- User makes implementation decisions (e.g., "let's use ReAct pattern")
- User says "record this", "add to design", "document this"
- User asks "what's our current design?" or "what have we decided?"
- Important technical decisions are made during conversation

## Workflow

### Recording Decisions

1. Read existing `.claude/docs/DESIGN.md`
2. Extract the decision/information from conversation
3. Update the appropriate section
4. Add entry to Changelog with today's date

### Sections to Update

| Conversation Topic | Target Section |
|-------------------|----------------|
| Overall goals, purpose | Overview |
| System structure, components | Architecture |
| Patterns (ReAct, etc.) | Implementation Plan > Patterns |
| Library choices | Implementation Plan > Libraries |
| Why we chose X over Y | Implementation Plan > Key Decisions |
| Things to implement later | TODO |
| Unresolved questions | Open Questions |

## Output Format

When recording, confirm in Japanese:
- What was recorded
- Which section was updated
- Brief summary of the change

## Language Rules

- **Thinking/Reasoning**: English
- **Code examples**: English
- **Document content**: English (technical terms) + Japanese (descriptions OK)
- **User communication**: Japanese
