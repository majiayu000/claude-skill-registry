---
name: dev-research-gdd-reading
description: Read Game Design Document for design context
category: research
---

# GDD Reading

Read the Game Design Document to understand design requirements.

## Essential Files

Always read these before implementing:

### Main GDD
- `docs/design/gdd/index.md` - Design overview
- `docs/design/gdd/game-loop.md` - Core gameplay loop

### Feature Specifications
- `docs/design/gdd/{feature}.md` - Feature-specific specs

### Decision Log
- `docs/design/decision_log.md` - Design rationale

### Open Questions
- `docs/design/open_questions.md` - Check for unresolved issues

## Reading Strategy

1. **Start with overview** - Get big picture context
2. **Find relevant sections** - Focus on feature being implemented
3. **Check decisions** - Understand why design choices were made
4. **Look for constraints** - Technical or design limitations

## Key Information to Extract

### Requirements
- What is being built?
- What are the acceptance criteria?
- What are the edge cases?

### Constraints
- Performance requirements?
- Platform limitations?
- Design constraints?

### Patterns
- Similar features already implemented?
- Shared patterns to follow?

## If Requirements Are Unclear

1. Check `open_questions.md` for existing discussions
2. Look at related features for patterns
3. Ask Game Designer via `design_question` message
4. Document assumptions and verify

## GDD-First Workflow

```
Task Assigned → Read GDD → Check Decisions → Identify Patterns → Implement
```

Never implement without understanding the design intent.

## Anti-Patterns

❌ **DON'T:**

- Skip the GDD and implement from PRD only - Missing design context causes rework
- Ignore the decision log - Reimplementing rejected decisions wastes time
- Assume requirements are complete - Open questions may affect your task
- Start coding before understanding the "why" - Design intent guides implementation choices
- Forget to check open questions - Unresolved issues may block your work

✅ **DO:**

- Read GDD before writing any code - Design context prevents mistakes
- Check decision log for relevant decisions - Learn from past design discussions
- Review open questions - Unclear requirements need clarification first
- Ask Game Designer when uncertain - Better to ask than to implement wrong
- Reference GDD sections in commits - Links design to implementation
