---
name: use-brainstorm
description: "Use before any creative work - creating features, building components, adding functionality, or modifying behavior to explore intent, requirements, and design before implementation."
---

You help turn ideas into validated designs through collaborative dialogue, then guide the transition to implementation.

# How to Brainstorm

1. **Understand the idea**:
   - Check current project state (files, docs, commits)
   - Ask questions one at a time (prefer multiple choice when possible)
   - Focus on: purpose, constraints, success criteria

2. **Explore approaches**:
   - Propose 2-3 different approaches with trade-offs
   - Lead with your recommended option and explain why
   - Present conversationally with reasoning

3. **Present the design**:
   - Break into sections of 200-300 words
   - Ask after each section whether it looks right so far
   - Cover: architecture, components, data flow, error handling, testing
   - Be ready to clarify if something doesn't make sense

# After Design Validated

**Documentation:**
- Write design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Use elements-of-style:writing-clearly-and-concisely if available
- Commit the design document

**Implementation (if continuing):**
- Ask: "Ready to set up for implementation?"
- Use autonome:use-worktrees to create isolated workspace
- Use autonome:use-plan-create to create detailed implementation plan

# Core Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer when possible
- **YAGNI ruthlessly** - Remove unnecessary features from designs
- **Explore alternatives** - Propose 2-3 approaches before settling
- **Incremental validation** - Present in sections, validate each
- **Be flexible** - Clarify when something doesn't make sense
