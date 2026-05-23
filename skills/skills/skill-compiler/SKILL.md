# Skill Compiler Skill

> Version: 1.0.0
> Compiler: manual (bootstrap)
> Last Updated: 2026-01-22

Transform declarative input specifications into versioned, upgradeable skill files.

## When to Activate

Use this skill when:
- Creating a new skill from scratch
- Upgrading existing skills after compiler improvements
- Validating skill quality and completeness
- Refactoring skills for consistency

## When to Create a Skill

Before creating a skill, apply the **Three Times Heuristic**:

1. **First time** - You're exploring; the approach is still forming
2. **Second time** - Pattern recognition; you notice similarity to before
3. **Third time** - Confirmation; the methodology has crystallized

**Create a skill when:**
- You've done the work 3+ times
- You find yourself explaining the same approach repeatedly
- Quality varies by who does the work (expertise isn't transmissible yet)

**Don't create a skill when:**
- The domain is still being explored
- The methodology is still changing
- You can't articulate the anti-patterns (not enough experience)

### The Two Sovereignties

Skills must honor the boundary between WHAT and HOW:

| Sovereignty | Owner | Contains |
|-------------|-------|----------|
| **WHAT** | Skill author | Outcomes, constraints, quality criteria, principles |
| **HOW** | Executing agent | Implementation, tool selection, sequencing |

A skill defines WHAT success looks like. The agent executing the skill decides HOW to achieve it. Micromanagement in skills creates brittle procedures; sovereignty-honoring creates adaptable guidance.

### Compiler Architecture

The skill system has a clean separation:

```
SCHEMA (input.yaml spec)  +  COMPILER (this skill)  =  One coherent unit
                              ↓
                    input.yaml (the seed)
                              ↓
                    SKILL.md (compiled output)
```

- **Schema + Compiler** are designed together, versioned together
- **input.yaml** is the seed - declarative domain expertise conforming to schema
- **SKILL.md** is compiled output - never edit directly

Creating a skill is just filling in the input.yaml schema with good content. No separate "authoring methodology" is needed.

## Core Principles

### 1. Input Artifacts Are Source of Truth

The `input.yaml` file defines what a skill does. `SKILL.md` is compiled output.

```
input.yaml  →  [Skill Compiler]  →  SKILL.md
   ↑                                    ↓
   └──── edit here ←── regenerate ──────┘
```

Never edit `SKILL.md` directly if `input.yaml` exists. Edit the input, recompile.

### 2. Version Everything

Every skill tracks:
- **Skill version**: Changes when the skill's substance changes
- **Compiler version**: Which compiler produced this output
- **Last updated**: When the skill was last compiled

This enables:
- Knowing when skills are stale
- Reproducing exact outputs
- Bulk upgrades when compiler improves

### 3. Reproducibility

Given the same `input.yaml` and compiler version, output must be identical. No randomness, no LLM temperature variance in structure.

### 4. Graceful Bootstrapping

Not all skills need `input.yaml`. Bootstrap skills can be manually authored with `Compiler: manual` in the header. The system works without the full pipeline.

---

## Input Artifact Specification

### `input.yaml` Schema

```yaml
# Required fields
name: string           # Skill identifier (kebab-case)
version: string        # Semantic version (e.g., "1.0.0")
purpose: string        # One-line description of what the skill does

# Activation conditions
triggers:
  - string             # Keywords/phrases that should activate this skill
  - string             # e.g., "research", "investigate", "analyze"

# Core content
principles:            # 3-7 guiding principles
  - name: string
    description: string
    rationale: string  # Why this principle matters

workflow:              # Ordered phases of execution
  - phase: string      # Phase name
    description: string
    steps:
      - string
      - string
    outputs:           # What this phase produces
      - string

# Knowledge capture
patterns:              # Positive patterns to follow
  - name: string
    when: string       # Situation this applies
    do: string         # What to do
    why: string        # Rationale

antipatterns:          # Negative patterns to avoid
  - name: string
    description: string
    consequence: string
    instead: string

# Quality assurance
checklist:             # Verification items before completion
  - string
  - string

# Optional
examples:              # Concrete usage examples
  - scenario: string
    application: string

references:            # Sources and citations
  - string
  - string

metadata:
  domain: string       # Category (e.g., "research", "debugging", "workflow")
  energy: string       # Cognitive load: low, medium, high
  time_estimate: string # Typical duration
```

### Minimal Example

```yaml
name: hello-world
version: 1.0.0
purpose: Demonstrate skill structure with minimal fields

triggers:
  - "hello world skill"
  - "demonstrate skill format"

principles:
  - name: Simplicity
    description: Start with the minimum viable structure
    rationale: Complexity should be added only when needed

workflow:
  - phase: Greet
    description: Produce a greeting
    steps:
      - Identify the target audience
      - Generate appropriate greeting
    outputs:
      - Greeting message

checklist:
  - Greeting is contextually appropriate
  - Tone matches audience expectations
```

---

## Compilation Process

### Phase 1: Input Validation

Before compiling, validate the input:

1. **Required fields present**: name, version, purpose, triggers, principles, workflow, checklist
2. **Name format**: kebab-case, alphanumeric with hyphens
3. **Version format**: Semantic versioning (X.Y.Z)
4. **Triggers non-empty**: At least one trigger phrase
5. **Principles bounded**: 3-7 principles (too few = underspecified, too many = unfocused)
6. **Workflow non-empty**: At least one phase

**Validation errors halt compilation with clear messages.**

### Phase 2: Structure Generation

Generate the markdown structure:

```markdown
# {Name} Skill

> Version: {version}
> Compiler: {compiler_version}
> Last Updated: {date}

{purpose}

## When to Activate

Use this skill when:
{triggers as bullet points}

## Core Principles

{for each principle}
### {N}. {principle.name}
{principle.description}

{principle.rationale as italicized note if present}
{end for}

---

## Workflow

{for each phase}
### Phase {N}: {phase.phase}

{phase.description}

{phase.steps as numbered list}

**Outputs:** {phase.outputs as inline list}
{end for}

---

## Patterns

{patterns as table: Name | When | Do | Why}

## Anti-Patterns to Avoid

{antipatterns as table: Anti-Pattern | Why It Fails | Instead}

---

## Quality Checklist

Before completing:

{checklist as checkbox list}

---

## Examples

{for each example}
**{example.scenario}**

{example.application}
{end for}

---

## References

{references as bullet list}
```

### Phase 3: Content Enrichment

The compiler may enhance content:

1. **Expand terse descriptions**: If a principle description is <20 chars, prompt for expansion
2. **Add cross-references**: Link to related skills if detected
3. **Generate missing examples**: If no examples provided, generate one from workflow
4. **Validate internal consistency**: Ensure checklist items map to workflow outputs

### Phase 4: Output Generation

Write the compiled `SKILL.md` with:

1. Standard header with version metadata
2. All sections in canonical order
3. Consistent formatting (tables, lists, code blocks)
4. No trailing whitespace, single trailing newline

---

## Upgrading Skills

### When to Upgrade

Upgrade skills when:
- Compiler version increases (new features, better structure)
- Input artifact changes (new principles, updated workflow)
- Quality issues identified (missing sections, inconsistencies)

### Upgrade Process

```
1. Load existing input.yaml
2. Run new compiler
3. Diff old SKILL.md vs new output
4. Review changes (human gate for major versions)
5. Replace SKILL.md
6. Update version if substance changed
```

### Version Bumping Rules

| Change Type | Version Bump | Examples |
|-------------|--------------|----------|
| Typos, formatting | Patch (0.0.X) | Fix spelling, adjust whitespace |
| New examples, clarifications | Minor (0.X.0) | Add example, expand principle |
| New principles, workflow changes | Major (X.0.0) | Add phase, change core guidance |

---

## Quality Standards

### Skill Quality Criteria

| Criterion | Requirement |
|-----------|-------------|
| **Actionable** | Every principle leads to concrete behavior |
| **Bounded** | Skill has clear scope; doesn't try to do everything |
| **Testable** | Checklist items can be verified yes/no |
| **Self-contained** | Can be used without external dependencies |
| **Versioned** | Clear metadata for tracking changes |

### Common Quality Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Vague principles | Contains "should", "might", "consider" | Rewrite as specific actions |
| Unbounded scope | >7 principles or >6 workflow phases | Split into multiple skills |
| Missing rationale | Principles without "why" | Add rationale for each |
| Orphan checklist items | Checklist item doesn't map to workflow | Either add to workflow or remove |
| No examples | Empty examples section | Generate from workflow |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Editing SKILL.md directly** | Changes lost on recompile | Edit input.yaml, recompile |
| **Skipping validation** | Garbage in, garbage out | Always validate before compile |
| **Version inflation** | Loses semantic meaning | Follow bump rules strictly |
| **Kitchen sink skills** | Unfocused, hard to apply | Keep skills single-purpose |
| **Copy-paste without adaptation** | Cargo culting | Understand before copying |

---

## Prompt Templates

### For Creating input.yaml from Scratch

```
I need to create a skill for: [TOPIC]

Generate an input.yaml that:
1. Captures 3-5 core principles (specific, actionable)
2. Defines a clear workflow (3-5 phases)
3. Includes patterns and anti-patterns from real experience
4. Has a concrete checklist for verification

Focus on practical wisdom, not textbook knowledge.
What do practitioners wish they knew sooner?
```

### For Upgrading Existing Skills

```
Compare this input.yaml against the skill-compiler spec:

[INPUT.YAML CONTENT]

Identify:
1. Missing required fields
2. Quality issues (vague principles, unbounded scope)
3. Opportunities for improvement
4. Suggested version bump if changes are needed
```

### For Extracting Skills from Experience

```
I just completed a task involving: [DESCRIPTION]

Key insights I gained:
[INSIGHTS]

Mistakes I made:
[MISTAKES]

Extract an input.yaml that captures this knowledge as a reusable skill.
Focus on the non-obvious learnings—things I had to discover the hard way.
```

### Techniques for Better Content

**Principle-as-Question:** To extract good principles, ask:
> "What truth, if ignored, causes failure in this domain?"

This surfaces non-obvious principles that distinguish experts from novices.

**Failure Archaeology:** To find good anti-patterns, ask:
> "What looked right at the time but turned out wrong?"

This captures hard-won knowledge from mistakes - often the most valuable part of a skill.

**Recursive Quality Check:** Before finalizing, verify the skill follows its own principles. A skill that violates its principles signals either bad principles or bad implementation.

---

## Quality Checklist

Before completing skill compilation:

- [ ] Input validates against schema (all required fields present)
- [ ] Name is kebab-case and descriptive
- [ ] Version follows semantic versioning
- [ ] Triggers are specific enough to avoid false activation
- [ ] 3-7 principles, each with actionable guidance
- [ ] Workflow phases are sequential and complete
- [ ] Patterns include "why" rationale
- [ ] Anti-patterns include "instead" alternatives
- [ ] Checklist items are verifiable yes/no
- [ ] At least one concrete example included
- [ ] Output markdown renders correctly
- [ ] Header metadata is accurate

---

## Example: Compiling a Skill

### Input (`input.yaml`)

```yaml
name: code-review
version: 1.0.0
purpose: Systematic approach to reviewing code changes for quality and correctness

triggers:
  - "review this code"
  - "check this PR"
  - "code review"

principles:
  - name: Understand Before Judging
    description: Read the entire change before making any comments
    rationale: Context prevents nitpicking; you might comment on something explained later

  - name: Correctness Over Style
    description: Prioritize bugs and logic errors over formatting preferences
    rationale: Style is subjective and automatable; correctness is critical

  - name: Ask, Don't Tell
    description: Phrase feedback as questions when uncertain
    rationale: Reduces defensiveness, acknowledges reviewer might be missing context

workflow:
  - phase: Orientation
    description: Understand what the change does and why
    steps:
      - Read PR description and linked issues
      - Identify the type of change (feature, bug fix, refactor)
      - Note the scope (files changed, lines added/removed)
    outputs:
      - Mental model of the change
      - List of focus areas

  - phase: Deep Review
    description: Examine the code in detail
    steps:
      - Review changes file by file
      - Check for correctness, edge cases, error handling
      - Verify tests cover the changes
      - Look for security implications
    outputs:
      - List of concerns
      - Questions for author

  - phase: Feedback Synthesis
    description: Organize and deliver feedback constructively
    steps:
      - Categorize issues (blocking, suggestion, nitpick)
      - Write clear, actionable comments
      - Highlight positive aspects
    outputs:
      - Review comments
      - Overall assessment

antipatterns:
  - name: Drive-by Comments
    description: Commenting on individual lines without understanding the whole change
    consequence: Wastes author time addressing non-issues
    instead: Complete orientation phase before commenting

  - name: Style Wars
    description: Extensive feedback on formatting, naming, etc.
    consequence: Obscures important feedback, creates friction
    instead: Use automated linting; reserve review for substance

checklist:
  - Understood the purpose of the change
  - Checked for correctness issues
  - Verified test coverage
  - Feedback is actionable and respectful
  - Blocking issues clearly identified
```

### Output (`SKILL.md`)

```markdown
# Code Review Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-22

Systematic approach to reviewing code changes for quality and correctness.

## When to Activate

Use this skill when:
- Review this code
- Check this PR
- Code review

## Core Principles

### 1. Understand Before Judging
Read the entire change before making any comments.

*Context prevents nitpicking; you might comment on something explained later.*

### 2. Correctness Over Style
Prioritize bugs and logic errors over formatting preferences.

*Style is subjective and automatable; correctness is critical.*

### 3. Ask, Don't Tell
Phrase feedback as questions when uncertain.

*Reduces defensiveness, acknowledges reviewer might be missing context.*

---

## Workflow

### Phase 1: Orientation

Understand what the change does and why.

1. Read PR description and linked issues
2. Identify the type of change (feature, bug fix, refactor)
3. Note the scope (files changed, lines added/removed)

**Outputs:** Mental model of the change, List of focus areas

### Phase 2: Deep Review

Examine the code in detail.

1. Review changes file by file
2. Check for correctness, edge cases, error handling
3. Verify tests cover the changes
4. Look for security implications

**Outputs:** List of concerns, Questions for author

### Phase 3: Feedback Synthesis

Organize and deliver feedback constructively.

1. Categorize issues (blocking, suggestion, nitpick)
2. Write clear, actionable comments
3. Highlight positive aspects

**Outputs:** Review comments, Overall assessment

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Drive-by Comments** | Wastes author time addressing non-issues | Complete orientation phase before commenting |
| **Style Wars** | Obscures important feedback, creates friction | Use automated linting; reserve review for substance |

---

## Quality Checklist

Before completing:

- [ ] Understood the purpose of the change
- [ ] Checked for correctness issues
- [ ] Verified test coverage
- [ ] Feedback is actionable and respectful
- [ ] Blocking issues clearly identified
```

---

## References

This skill draws from:
- Experience with skill-based agent architectures
- Compiler design principles (source of truth, reproducibility)
- Technical writing best practices
- Anthropic: "Building Effective Agents" (2024) - skill decomposition patterns
