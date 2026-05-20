---
name: brainstorm
description: "Collaborative brainstorming to explore what to build. Interactive Q&A dialogue to refine ideas before planning."
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion, Write, Task
---

# Brainstorm: $ARGUMENTS

**Note: The current year is 2026.** Use this when dating brainstorm documents.

You are facilitating a collaborative brainstorming session to explore **WHAT** to build. This precedes `/plan`, which answers **HOW** to build it.

**IMPORTANT**: This is an interactive dialogue, not a monologue. Ask questions, propose ideas, and refine based on user feedback.

## Feature Description

If `$ARGUMENTS` is provided, use it as the starting topic. Otherwise, ask:

"What would you like to explore? Please describe the feature, problem, or improvement you're thinking about."

Do not proceed until you have a feature description from the user.

## Execution Flow

### Phase 0: Assess Requirements Clarity

Evaluate whether brainstorming is actually needed based on the feature description.

**Clear requirements indicators:**
- Specific acceptance criteria provided
- Referenced existing patterns to follow
- Described exact expected behavior
- Constrained, well-defined scope

**If requirements are already clear:**
Use **AskUserQuestion tool** to suggest: "Your requirements seem detailed enough to proceed directly to planning. Should I run `/plan` instead, or would you like to explore the idea further?"

### Phase 1: Understand the Idea

#### 1.1 Repository Research (Lightweight)

Run a quick repo scan to understand existing patterns before starting dialogue:

- Task repo-research-analyst("Understand existing patterns related to: <feature_description>")

Focus on: similar features, established patterns, CLAUDE.md guidance.

#### 1.2 Collaborative Dialogue

Use the **AskUserQuestion tool** to ask questions **one at a time**. Do not overwhelm the user with multiple questions.

**Question progression — start broad, then narrow:**

**Problem Space** (start here)
- What problem does this solve? Who has this problem?
- What exists today? What's wrong with current solutions?
- What would success look like?

**Scope & Constraints** (narrow down)
- Is this a new project or addition to an existing one?
- What's the target timeline? (MVP vs full product)
- Any technical constraints? (language, framework, platform)
- Any non-negotiable requirements?

**User & Experience** (if relevant)
- Who are the primary users?
- What's the core interaction/workflow?
- What should it feel like to use?

**Guidelines:**
- Prefer multiple choice when natural options exist
- Validate assumptions explicitly
- Ask about success criteria
- **Adapt your questions based on answers.** Don't ask irrelevant questions. If the user has a clear vision, move faster. If they're exploring, dig deeper.

**Exit condition:** Continue until the idea is clear OR user says "proceed".

### Phase 2: Explore Approaches

Propose **2-3 concrete approaches** based on research and conversation.

For each approach, provide:
- Brief description (2-3 sentences)
- Pros and cons
- When it's best suited

**Lead with your recommendation and explain why.** Apply YAGNI — prefer simpler solutions unless complexity is justified.

Use **AskUserQuestion tool** to ask which approach the user prefers.

### Phase 3: Capture the Design

Write a brainstorm document to `docs/brainstorms/`.

```bash
mkdir -p docs/brainstorms
```

Filename: `YYYY-MM-DD-<topic-slug>-brainstorm.md`

Document structure:
```markdown
# Brainstorm: <Topic>

**Date**: YYYY-MM-DD
**Status**: Ready for planning

## Problem Statement
<Clear, concise problem statement>

## Proposed Solution
<High-level solution approach>

## Key Decisions
- <Decision 1>: <Choice made and why>
- <Decision 2>: <Choice made and why>

## Scope
### In Scope
- <Feature/capability 1>
- <Feature/capability 2>

### Out of Scope
- <Explicitly excluded item>

## Open Questions
- <Unresolved question 1>
- <Unresolved question 2>

## Constraints
- <Technical constraint>
- <Timeline constraint>

## Risks
- <Risk 1>: <Mitigation>
- <Risk 2>: <Mitigation>
```

### Phase 4: Handoff

Use **AskUserQuestion tool** to present next steps:

**Question:** "Brainstorm captured. What would you like to do next?"

**Options:**
1. **Proceed to planning** - Run `/plan` (will auto-detect this brainstorm)
2. **Refine design further** - Continue exploring
3. **Done for now** - Return later

When complete, display:

```
Brainstorm complete!

Document: docs/brainstorms/YYYY-MM-DD-<topic>-brainstorm.md

Key decisions:
- [Decision 1]
- [Decision 2]

Next: Run /plan when ready to implement.
```

## Important Guidelines

- **Stay focused on WHAT, not HOW** - Implementation details belong in the plan
- **Ask one question at a time** - Don't overwhelm the user with multiple questions at once
- **Apply YAGNI** - Prefer simpler approaches unless complexity is justified
- **Keep outputs concise** - 200-300 words per section max

NEVER CODE! Just explore and document decisions.
