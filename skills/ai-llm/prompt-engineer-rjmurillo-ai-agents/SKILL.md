---
name: prompt-engineer
description: Optimize system prompts for Claude Code agents using proven prompt engineering patterns. Use when users request prompt improvement, optimization, or refinement for agent workflows, tool instructions, or system behaviors.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Prompt Optimizer

Optimizes system prompts by applying research-backed prompt engineering patterns. Human-in-the-loop phases: understand, plan, propose changes, receive approval, then integrate.

## Purpose and Success Criteria

A well-optimized prompt achieves:

1. **Behavioral clarity**: Agent knows exactly what to do in common cases and edge cases
2. **Appropriate scope**: Complex tasks get decomposition; simple tasks don't trigger overthinking
3. **Grounded changes**: Every modification traces to a specific pattern with documented impact

Optimization is complete when:

- Every change has explicit pattern attribution from the reference document
- No section contradicts another section
- The prompt matches its operating context (tool-use vs. conversational, token constraints)
- Human has approved both section-level changes and full integration

## When to Use This Skill

Use when the user provides a prompt and wants it improved, refined, or reviewed for best practices.

Do NOT use for:

- Writing prompts from scratch (different skill)
- Prompts that are already working well and user just wants validation
- Non-prompt content (documentation, code, etc.)

## Required Resources

Before ANY analysis, read the appropriate pattern reference(s):

### Single-Turn Reference (Always Read)

```text
Read references/prompt-engineering-single-turn.md
```

Contains: Technique Selection Guide table, Quick Reference principles, domain-organized techniques with citations, Anti-Patterns section.

### Multi-Turn Reference (Conditional)

```text
Read references/prompt-engineering-multi-turn.md
```

**Read ONLY when the prompt involves:**

- Multi-turn flows (iterative refinement, conversation chains)
- Multi-agent / sub-agent orchestration

**Skip for:**

- Static system prompts executed in a single LLM call
- Tool instructions or one-shot prompts

### Workflow Reference

```text
Read references/workflow.md
```

Contains: Detailed Phase 0-4 workflows, visual card template, completion checkpoint.

## Quick Process

```text
┌─────────────────────────────────────────────────────────────────┐
│ 1. READ THE REFERENCE(S)                                        │
│    - Always: references/prompt-engineering-single-turn.md       │
│    - If multi-turn/multi-agent: also read multi-turn reference  │
├─────────────────────────────────────────────────────────────────┤
│ 2. UNDERSTAND THE PROMPT (Phase 1)                              │
│    - Operating context (single-shot? tool-use? constraints?)    │
│    - Current state (working? unclear? missing?)                 │
│    - Document specific problems with quoted prompt text         │
├─────────────────────────────────────────────────────────────────┤
│ 3. PLAN WITH VISUAL CARDS (Phase 2)                             │
│    - Present each change as a visual card with:                 │
│      SCOPE → PROBLEM → TECHNIQUE → BEFORE/AFTER                 │
│    - Quote trigger conditions from reference                    │
│    - ⚠️  WAIT FOR USER APPROVAL before proceeding               │
├─────────────────────────────────────────────────────────────────┤
│ 4. EXECUTE APPROVED CHANGES (Phase 3)                           │
│    - Apply the BEFORE → AFTER transformations                   │
├─────────────────────────────────────────────────────────────────┤
│ 5. INTEGRATE AND VERIFY QUALITY (Phase 4)                       │
│    - Check cross-section coherence                              │
│    - Final anti-pattern check                                   │
│    - Present complete optimized prompt                          │
└─────────────────────────────────────────────────────────────────┘
```

## Triage (Phase 0)

**Simple prompts** (use lightweight process):

- Under 20 lines
- Single clear purpose
- No conditional logic

**Complex prompts** (use full process):

- Multiple sections serving different functions
- Conditional behaviors or rule hierarchies
- Tool orchestration or multi-step workflows

## Core Quality Principles

1. **Quote before deciding**: Every technique selection must quote the reference's trigger condition.
2. **Open verification questions**: Ask "What behavior will this produce?" not "Is this correct?"
3. **Approval happens once, upfront**: The visual card format in Phase 2 shows full impact.
4. **Preserve what works**: Optimization means improving problems, not rewriting everything.

## Completion Checkpoint

Before presenting the final prompt, verify:

- [ ] Phase 2 plan used visual card format with BEFORE/AFTER
- [ ] Phase 2 plan quoted trigger conditions from reference
- [ ] Phase 2 plan was approved by user before Phase 3
- [ ] No technique applied without matching trigger condition
- [ ] Stacking compatibility checked; no conflicts
- [ ] Anti-patterns section consulted; none introduced
- [ ] Emphasis markers used sparingly (≤3 highest-level)

## References

- [prompt-engineering-single-turn.md](references/prompt-engineering-single-turn.md) - Single-turn patterns
- [prompt-engineering-multi-turn.md](references/prompt-engineering-multi-turn.md) - Multi-turn patterns
- [workflow.md](references/workflow.md) - Detailed phase workflows and card template
