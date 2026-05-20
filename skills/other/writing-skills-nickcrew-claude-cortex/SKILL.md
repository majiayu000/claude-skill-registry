---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment - applies TDD to process documentation by testing with subagents before writing, iterating until bulletproof against rationalization
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**Personal skills live in agent-specific directories:** `~/.claude/skills` for Claude Code, `~/.codex/skills` for Codex

**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill.

## When to Use

**Create a skill when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)

## Skill Types

- **Technique**: Concrete method with steps (condition-based-waiting, root-cause-tracing)
- **Pattern**: Way of thinking about problems (flatten-with-flags, test-invariants)
- **Reference**: API docs, syntax guides, tool documentation (office docs)

## Quick Reference

| Task | Load reference |
| --- | --- |
| Understand TDD mapping for skills | `skills/writing-skills/references/tdd-mapping.md` |
| Learn skill structure and organization | `skills/writing-skills/references/skill-structure.md` |
| Optimize for search and discovery | `skills/writing-skills/references/search-optimization.md` |
| Test skills with subagents | `skills/writing-skills/references/testing-skills.md` |
| Code examples and flowcharts | `skills/writing-skills/references/code-and-flowcharts.md` |
| Complete creation checklist | `skills/writing-skills/references/checklist.md` |

## RED-GREEN-REFACTOR Workflow

### RED: Write Failing Test (Baseline)
1. Create pressure scenarios (3+ combined pressures for discipline skills)
2. Run scenarios WITHOUT skill - document baseline behavior verbatim
3. Identify patterns in rationalizations/failures

**This is critical:** You must see what agents naturally do before writing the skill.

### GREEN: Write Minimal Skill
1. Write skill addressing specific baseline failures
2. Follow structure guidelines (see skill-structure.md)
3. Optimize for search (see search-optimization.md)
4. Run same scenarios WITH skill - verify agents now comply

### REFACTOR: Close Loopholes
1. Identify NEW rationalizations from testing
2. Add explicit counters for discipline skills
3. Build rationalization table from all iterations
4. Re-test until bulletproof

**REQUIRED SUB-SKILL:** Use superpowers:testing-skills-with-subagents for complete testing methodology.

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Delete means delete

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing skill before testing | Delete skill, run baseline test first |
| Skipping baseline (RED phase) | You don't know what to teach without seeing failure |
| Testing with skill already present | Remove skill, get true baseline behavior |
| "Batching" multiple skills | Complete RED-GREEN-REFACTOR for each skill before moving on |
| Vague descriptions | Start with "Use when...", include specific triggers |
| Using @ links to reference skills | Use skill names only, avoid force-loading |
| Multiple mediocre code examples | One excellent example in most relevant language |
| Narrative storytelling | Focus on reusable patterns, not one-off stories |

## STOP Before Moving to Next Skill

**After writing ANY skill, you MUST STOP and complete the deployment process.**

Do NOT create multiple skills in batch without testing each. Deploying untested skills = deploying untested code.

See `checklist.md` for full deployment checklist.

## Resources

- **Official guidance**: For Anthropic's official skill authoring best practices, see anthropic-best-practices.md
- **Graphviz conventions**: See @graphviz-conventions.dot for flowchart style rules
- **Testing methodology**: Use superpowers:testing-skills-with-subagents
- **TDD fundamentals**: Use superpowers:test-driven-development
