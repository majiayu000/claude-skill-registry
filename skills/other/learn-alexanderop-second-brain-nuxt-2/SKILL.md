---
name: learn
description: Analyze conversation for learnings and save to docs folder
argument-hint: [optional topic hint]
model: claude-opus-4-5-20251101
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Learn from Conversation

Analyze this conversation for insights worth preserving in the project's documentation.

**If a topic hint was provided via `$ARGUMENTS`, focus on capturing that specific learning.**
**If no hint provided, analyze the full conversation for valuable insights.**

## Phase 1: Deep Analysis

Think deeply about what was learned in this conversation:
- What new patterns or approaches were discovered?
- What gotchas or pitfalls were encountered?
- What architecture decisions were made and why?
- What conventions were established?
- What troubleshooting solutions were found?

Only capture insights that are:
1. **Reusable** - Will help in future similar situations
2. **Non-obvious** - Not already common knowledge
3. **Project-specific** - Relevant to this codebase

If nothing valuable was learned, say so and exit gracefully.

## Phase 2: Categorize & Locate

Read existing docs to find the best home. Look for a `docs/` folder or similar documentation directory in the project.

If no existing doc fits, propose a new doc file with kebab-case naming.

**Note:** CLAUDE.md stays stable as the entry point. All detailed learnings go to `/docs` only.

## Phase 3: Draft the Learning

Format the insight to match existing doc style:
- Clear heading describing the topic
- Concise explanation of the insight
- Code examples if applicable
- Context on when this applies

## Phase 4: User Approval (BLOCKING)

Present your proposed changes:
1. What insight you identified
2. Where you'll save it (existing doc + section, or new file)
3. The exact content to add

**Wait for explicit user approval before saving.**

## Phase 5: Save

After approval, save the learning and confirm what was captured.
