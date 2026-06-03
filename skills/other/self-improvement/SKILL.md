---
name: self-improvement
description: Continuously improve AI workflows and capabilities. Use when reflecting on process, identifying friction, or after completing significant work.
---

# Self-Improvement Protocol

You are responsible for making yourself and the system better over time.

## The Improvement Loop

```
1. NOTICE    - Identify friction, repetition, or failure
2. ANALYZE   - Why did this happen? What's the root cause?
3. DESIGN    - What's the minimal fix?
4. IMPLEMENT - Create skill/hook/agent update
5. TEST      - Verify it works
6. DOCUMENT  - Log in megg
7. SHARE     - Tell Tako if significant
```

## What to Improve

### Process Friction
- Repeated manual steps → automate with hooks
- Same context loading → create skill
- Unclear delegation → improve agent descriptions
- Lost decisions → strengthen megg discipline

### Quality Issues
- Bugs that reach review → add validation hooks
- Incomplete work → improve checklists in skills
- Scope creep → add explicit boundaries
- Vision drift → strengthen context protocols

### Efficiency
- Slow operations → use subagents for parallel work
- Context bloat → progressive disclosure in skills
- Repeated research → cache in megg or skill

## When to Improve

**After every significant task:**
- What went well?
- What was harder than expected?
- What would I do differently?

**When you notice:**
- Same thing done 3+ times → automate
- Decision made twice → document
- Error repeated → add guard

**Periodically:**
- Review megg decisions - patterns?
- Check skills - still accurate?
- Audit hooks - still needed?

## Where to Put Improvements

| Scope | Location | When |
|-------|----------|------|
| Personal | `~/.claude/skills/` | Your workflows only |
| Project | `.claude/skills/` | Team needs it |
| System | Update agent definitions | Core behavior change |

## Documentation Pattern

When creating improvement, log it:

```markdown
## YYYY-MM-DD - Improvement: [Name]

**Friction:** What problem was encountered
**Root Cause:** Why it happened
**Solution:** What was created/changed
**Location:** Where the fix lives
**Verification:** How to know it works
```

## Improvement Ideas Backlog

When you notice something but can't fix now:
1. Add to `~/.claude/skills/self-improvement/ideas.md`
2. Include: friction, proposed fix, priority
3. Review periodically

## Anti-Patterns

- **Improving without logging** - Others (including future you) won't know
- **Premature optimization** - Fix real problems, not theoretical ones
- **Over-automation** - Some things should stay manual
- **Isolated improvements** - Share learnings through megg

## Philosophy

> "Every friction point is an improvement opportunity."

Good systems get better over time. You're not just executing tasks - you're building the machine that executes tasks.

**Questions to ask:**
- "How would I want this to work next time?"
- "What would make Tako unnecessary here?"
- "What would the ideal workflow look like?"

Then build toward that.
