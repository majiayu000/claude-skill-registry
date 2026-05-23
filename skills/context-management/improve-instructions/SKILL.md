---
name: improve-instructions
description: Analyzes conversation history to improve CLAUDE.md files. Use when you notice patterns in how Claude misunderstands requests, want to consolidate repeated guidance, or improve instruction clarity based on actual usage.
allowed-tools: [Read, Edit, Grep, Glob, AskUserQuestion, TodoWrite]
# model: opus
---

## Reference Files

- [analysis-guide.md](analysis-guide.md) - Patterns to look for in conversations
- [examples.md](examples.md) - Example improvements with before/after

---

# Improve Instructions

Analyze conversation patterns to identify improvements for CLAUDE.md instruction files.

## Objective

Review how the conversation has gone to find opportunities where better instructions would have helped Claude perform more effectively.

## Process

### Phase 1: Analyze Conversation

Review the conversation history for:

- **Repeated corrections** - "No, I meant..." or "Remember to..."
- **Manual guidance** - Workflows explained step-by-step that could be documented
- **Preference statements** - "I prefer X" or "Always use Y"
- **Misunderstandings** - Where Claude made wrong assumptions
- **Undocumented patterns** - Tools or workflows used frequently

Use TodoWrite to track each potential improvement identified.

### Phase 2: Review Current State

Read the relevant CLAUDE.md file(s):

- `~/.claude/CLAUDE.md` for global instructions
- Project-level `CLAUDE.md` for project-specific instructions

Understand what's already documented to avoid duplication and identify gaps.

### Phase 3: Propose Improvements

Present findings to the user using AskUserQuestion:

For each improvement, explain:

- **Issue**: What pattern was observed
- **Proposal**: Specific text to add or change
- **Rationale**: Why this would help

Group related improvements and let the user select which to implement.

### Phase 4: Implement

For each approved improvement:

1. Use Edit to modify the appropriate CLAUDE.md
2. Place new content in the logical section
3. Maintain existing formatting and style

Summarize all changes made.

## Guidelines

- Ground suggestions in actual conversation patterns, not hypotheticals
- Prefer specific, actionable instructions over vague guidance
- Keep instructions concise - Claude is smart, it doesn't need over-explanation
- Preserve the user's existing voice and style
- Don't add instructions for one-off situations

## Output

End with a summary of:

- Changes made to CLAUDE.md
- Patterns identified but not yet addressed (for future consideration)
