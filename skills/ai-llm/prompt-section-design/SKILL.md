---
name: prompt-section-design
description: Design composable prompt sections for building agentic prompts. Use when creating reusable prompt components, designing LEGO-block prompt sections, or structuring prompts for the stakeholder trifecta.
allowed-tools: Read, Grep, Glob
---

# Prompt Section Design Skill

Design composable prompt sections that work like LEGO blocks for building prompts at any level.

## Purpose

Create well-structured prompt sections that are reusable, consistent, and effective for the stakeholder trifecta.

## When to Use

- Creating a new prompt
- Restructuring existing prompt
- Adding sections to prompt
- Standardizing team prompts

## Section Tier List

| Tier | Sections | Priority |
| --- | --- | --- |
| S | Workflow | Always include (Level 2+) |
| A | Variables, Examples, Control Flow, Delegation, Template | High value |
| B | Purpose, High-Level, Higher Order, Instructions | Supporting |
| C | Metadata, Codebase Structure, Relevant Files, Report | As needed |

## Design Process

### Step 1: Identify Prompt Purpose

Ask:

- What does this prompt accomplish?
- Who will use it? (you, team, agents)
- What level is it? (1-7)
- What inputs/outputs are needed?

### Step 2: Select Required Sections

Based on level:

| Level | Required | Recommended |
| --- | --- | --- |
| 1 | Title, Prompt | - |
| 2 | Title, Workflow | Variables, Report |
| 3 | Title, Workflow | Variables, Control Flow |
| 4 | Title, Workflow | Variables, Delegation |
| 5 | Title, Workflow | Variables |
| 6 | Title, Workflow, Template | Variables |
| 7 | Title, Workflow, Expertise | Variables |

### Step 3: Design Each Section

#### Metadata (Frontmatter)

```yaml
---
description: Clear, searchable description
argument-hint: [arg1] [arg2]
allowed-tools: Read, Write, Edit
model: sonnet
---
```

**Guidelines:**

- `description`: What does it do? When to use?
- `argument-hint`: What parameters expected?
- `allowed-tools`: Minimal set needed
- `model`: Match to task complexity

#### Title

```markdown
# Action-Oriented Title
```

**Guidelines:**

- Use imperative verb: Create, Build, Generate, Analyze
- Be specific: "Create Implementation Plan" not "Plan"
- Keep concise: 2-5 words

#### Purpose

```markdown
## Purpose
[1-2 sentences describing what the prompt accomplishes]
```

**Guidelines:**

- Direct language to agent
- Reference key sections
- Explain the "what" and "why"

#### Variables

```markdown
## Variables

# Dynamic (from user)
USER_PROMPT: $ARGUMENTS
FILE_PATH: $1
COUNT: $2 or 3 if not provided

# Static (fixed)
OUTPUT_DIR: specs/
MODEL: sonnet
```

**Guidelines:**

- SCREAMING_SNAKE_CASE
- Dynamic first, static second
- Include defaults where appropriate
- Clear descriptions

#### Workflow (S-Tier)

```markdown
## Workflow

1. Validate inputs
   - Check USER_PROMPT is provided
   - If not, STOP and ask user
2. Process task
   - Sub-step detail
3. Generate output
4. Report results
```

**Guidelines:**

- Numbered steps for sequence
- Sub-bullets for details
- STOP conditions explicit
- Clear progression

#### Instructions

```markdown
## Instructions

- IMPORTANT: Always validate before processing
- Handle edge cases gracefully
- Never modify files outside project
```

**Guidelines:**

- Bullet points for rules
- IMPORTANT markers for critical
- Edge cases explicit

#### Report

```markdown
## Report

## Task Complete

**Files:** [count]
**Status:** [status]

### Changes
- [change 1]
- [change 2]
```

**Guidelines:**

- Template for output
- Consistent format
- Easy to parse

#### Template (Level 6)

<!-- markdownlint-disable MD033 MD025 MD003 MD040 -->

```markdown
## Specified Format

```text
---

allowed-tools: <tools>
description: <description>
---

# <name>

## Variables

<VAR>: $1

## Workflow

<steps>
```

<!-- markdownlint-enable MD033 MD025 MD003 MD040 -->

**Guidelines:**

- Complete template
- Placeholders marked clearly
- Follows prompt conventions

#### Expertise (Level 7)

```text
## Expertise

### Domain Knowledge
- Pattern 1 learned
- Pattern 2 discovered

### Discovered Patterns
- Implementation insight 1
- Best practice 2
```

**Guidelines:**

- Organized by category
- Grows over time
- Never modify Workflow

### Step 4: Validate Structure

Checklist:

- [ ] Title is action-oriented
- [ ] Workflow has numbered steps
- [ ] Variables use SCREAMING_SNAKE_CASE
- [ ] STOP conditions are explicit
- [ ] Frontmatter has description
- [ ] Sections in logical order

## Section Order Convention

<!-- markdownlint-disable MD033 MD025 MD040 -->

```text
---

[frontmatter]
---

# [Title]

## Purpose

[purpose]

## Variables

[variables]

## Instructions

[instructions]

## Workflow

[workflow]

## Report

[report format]
```

<!-- markdownlint-enable MD033 MD025 MD040 -->

## Output Format

When designing sections:

````markdown
## Section Design

**Prompt:** [name]
**Level:** [1-7]

### Recommended Sections

1. **Title**: [suggested title]

2. **Frontmatter**:

```yaml
description: ...
argument-hint: ...
allowed-tools: ...
model: ...
```

1. **Variables**:
   - Dynamic: [list]
   - Static: [list]

2. **Workflow**: [step count] steps
   - Step 1: [overview]
   - Step 2: [overview]
   ...

3. **Report**: [format type]
````

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| No Workflow section | Agent lacks direction | Always add for Level 2+ |
| Inconsistent variable names | Confusion | SCREAMING_SNAKE_CASE |
| Missing STOP conditions | Runaway execution | Explicit early exits |
| Over-detailed workflow | Reduces agent autonomy | High-level steps |
| No frontmatter | Hard to discover | Add description |

## Key Quote

> "Build libraries of reusable battle-tested agentic prompts with composable sections that work like LEGO blocks."

## Cross-References

- @prompt-sections-reference.md - Section definitions
- @seven-levels.md - Sections by level
- @variable-patterns.md - Variable conventions

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
