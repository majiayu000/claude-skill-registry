---
name: prompt-level-selection
description: Guide selection of appropriate prompt level for a task. Use when choosing between simple prompts and complex workflows, applying the seven levels framework, or matching task complexity to prompt investment.
allowed-tools: Read, Grep, Glob
---

# Prompt Level Selection Skill

Guide selection of the appropriate prompt level for a task using the seven levels framework.

## Purpose

Match task complexity to the right prompt level. Start simple, add complexity only when needed.

## When to Use

- Starting a new prompt
- Upgrading existing prompt
- Unsure which level fits
- Teaching prompt engineering

## The Seven Levels Quick Reference

| Level | Name | Use When |
| --- | --- | --- |
| 1 | High-Level | Simple repeatable task |
| 2 | Workflow | Sequential steps needed |
| 3 | Control Flow | Conditionals or loops |
| 4 | Delegation | Multiple agents needed |
| 5 | Higher-Order | Processing other prompts |
| 6 | Template Meta | Generating prompts |
| 7 | Self-Improving | Knowledge accumulation |

## Decision Tree

```text
Is this a simple, repeatable task?
├── Yes -> Level 1 (High-Level Prompt)
└── No
    |
    Does it need sequential steps?
    ├── Yes -> Does it need conditionals/loops?
    |   ├── Yes -> Does it delegate to agents?
    | |   ├── Yes -> Level 4 (Delegation)
    | |   └── No -> Level 3 (Control Flow)
    |   └── No -> Level 2 (Workflow)
    └── No
        |
        Does it process other prompts?
        ├── Yes -> Level 5 (Higher-Order)
        └── No
            |
            Does it generate prompts?
            ├── Yes -> Level 6 (Template Meta)
            └── No
                |
                Does it need to learn over time?
                ├── Yes -> Level 7 (Self-Improving)
                └── No -> Reassess requirements
```

## The 80/20 Rule

> "Levels 3-4 cover 80% of practical use cases."

| Level Range | Coverage | Complexity |
| --- | --- | --- |
| 1-2 | 40% | Low |
| 3-4 | 80% | Medium (Sweet Spot) |
| 5-7 | 20% | High |

**Don't over-engineer.** Most tasks fit in Levels 3-4.

## Selection Process

### Step 1: Understand the Task

Ask:

- What does this task accomplish?
- How often will it be repeated?
- What inputs does it need?
- What outputs does it produce?

### Step 2: Check Complexity Indicators

| Indicator | Points To |
| --- | --- |
| One-time or rare | Level 1 |
| Sequential steps | Level 2+ |
| "If X then Y" | Level 3+ |
| "Run N agents" | Level 4 |
| "Process this spec file" | Level 5 |
| "Create prompts for..." | Level 6 |
| "Learn and improve" | Level 7 |

### Step 3: Start Low, Upgrade If Needed

1. Start with lowest applicable level
2. Build and test the prompt
3. If insufficient, upgrade one level
4. Repeat until task is satisfied

## Level Selection Examples

### Example 1: "Start the dev server"

**Analysis:** Simple, repeatable, no variables
**Level:** 1 (High-Level Prompt)

### Example 2: "Create an implementation plan"

**Analysis:** Sequential steps, needs input, produces output
**Level:** 2 (Workflow Prompt)

### Example 3: "Generate N images with validation"

**Analysis:** Loop required, conditional checking
**Level:** 3 (Control Flow)

### Example 4: "Research topic with 5 parallel agents"

**Analysis:** Multiple agents, aggregation needed
**Level:** 4 (Delegation Prompt)

### Example 5: "Build from this spec file"

**Analysis:** Accepts another prompt/spec as input
**Level:** 5 (Higher-Order)

### Example 6: "Create new slash commands"

**Analysis:** Generates prompts in specific format
**Level:** 6 (Template Meta Prompt)

### Example 7: "Hook expert that learns patterns"

**Analysis:** Accumulates expertise over time
**Level:** 7 (Self-Improving Prompt)

## Output Format

When recommending a level:

```markdown
## Level Selection

**Task:** [description]

**Recommended Level:** [1-7] ([name])

**Rationale:**
- [reason 1]
- [reason 2]

**Key Sections Needed:**
- [section 1]
- [section 2]

**Alternative Consideration:**
Level [N] if [condition]
```

## Red Flags

| Red Flag | Issue | Solution |
| --- | --- | --- |
| Jumping to Level 6-7 | Over-engineering | Start at Level 2-3 |
| Level 1 for complex task | Under-engineering | Add Workflow section |
| Level 4 for single-agent | Unnecessary delegation | Use Level 2-3 |
| No clear level fit | Vague requirements | Clarify task scope |

## Key Quote

> "Three times marks a pattern. Copy whatever you're doing and write it as a high level prompt, then move up the levels from there."

## Cross-References

- @seven-levels.md - Detailed level descriptions
- @prompt-sections-reference.md - Sections for each level
- @stakeholder-trifecta.md - Communication considerations

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
