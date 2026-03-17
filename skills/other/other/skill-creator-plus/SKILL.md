---
name: skill-creator-plus
description: >
  Enhanced skill creation framework emphasizing philosophy-first design, anti-pattern
  prevention, and variation encouragement. Use when creating new skills, improving
  existing skills, analyzing skill quality, or when users request help designing
  effective skills that unlock capabilities rather than constraining them. Includes
  analysis tools and upgrade suggestions for existing skills.
---

# Skill Creator Plus

An advanced framework for creating skills that **unlock Claude's capabilities** rather than constraining them to templates.

## Philosophy: Skills as Mental Frameworks

Skills are not checklists or templates—they are **mental frameworks that guide creative problem-solving**.

**Core principle: Unlock vs. Constrain**

| Constraining Approach | Unlocking Approach |
|-----------------------|-------------------|
| Rigid templates | Flexible frameworks |
| Strict rules | Guiding principles |
| Fixed outputs | Varied, context-appropriate results |
| Limiting choices | Expanding possibilities |
| Checklists | Mental models |

### The Three Pillars of Effective Skills

1. **Philosophy Before Procedure**: Establish "how to think" before "what to do"
2. **Anti-Patterns as Guidance**: What NOT to do is as important as what to do
3. **Variation as Requirement**: Explicitly prevent output convergence

**IMPORTANT**: This skill exemplifies the principles it teaches. Study its structure as a reference pattern for philosophy-first design.

---

## Before Creating a Skill

Ask these fundamental questions:

- **Purpose**: What procedural knowledge will this skill provide that Claude doesn't already have?
- **Philosophy**: What mental framework should guide decisions in this domain?
- **Triggers**: When should this skill be loaded? What specific use cases?
- **Scope**: Is this skill focused or trying to do too much?
- **Composability**: How will this work with other skills?

Good answers to these questions shape effective skills.

---

## Skill Creation Process

### 1. Understand with Concrete Examples

Skip only when usage patterns are already clearly understood.

**Gather examples of how the skill will be used**:
- Direct examples from users
- Generated scenarios validated by users
- Real-world use cases

**Key questions**:
- What functionality should this skill support?
- What would users say to trigger this skill?
- What are edge cases or variations?

Don't overwhelm users—ask progressively, not all at once.

### 2. Plan the Philosophical Foundation

**Before** planning scripts and resources, design the skill's philosophy:

**Establish the mental framework**:
- What philosophy guides this domain?
- What questions should be asked before acting?
- What principles help make good decisions?
- What mental model makes this domain intuitive?

**Identify anti-patterns**:
- What common mistakes happen in this domain?
- What should explicitly be avoided?
- What produces "generic" or "template" outputs?

**Plan for variation**:
- What should vary across outputs?
- What creates context-appropriateness?
- What prevents convergence on "favorites"?

See references/philosophy-patterns.md for frameworks to establish philosophical foundations.

See references/anti-patterns.md for common skill creation mistakes.

See references/variation-patterns.md for techniques to encourage output diversity.

### 3. Plan Reusable Resources

Based on concrete examples, identify helpful resources:

**Scripts** (`scripts/`):
- Code rewritten repeatedly
- Deterministic operations
- Complex, fragile procedures

**References** (`references/`):
- Documentation Claude should reference
- Schemas, API docs, domain knowledge
- Detailed workflows too long for SKILL.md

**Assets** (`assets/`):
- Templates used in outputs
- Boilerplate code, images, fonts
- Files copied or modified, not loaded into context

**Progressive disclosure principle**: Keep SKILL.md lean (<500 lines), move details to references.

See references/composability.md for designing skills that work well together.

### 4. Initialize the Skill

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates skill directory with SKILL.md template and resource directories.

### 5. Edit the Skill

#### Write the SKILL.md

**Structure (Philosophy-First Pattern)**:

```markdown
---
name: skill-name
description: >
  Comprehensive description of what, when, and specific triggers.
  Include use cases and file types that trigger loading.
---

# Skill Name

[1-2 sentence introduction framing the problem/opportunity]

## Philosophy: [Core Mental Framework]

[Philosophy section establishing mental model BEFORE procedures]

**Before [acting], ask**:
- Question 1
- Question 2
- Question 3

**Core principles**:
1. Principle 1: [Why it matters]
2. Principle 2: [Why it matters]

## [Main Guidelines Section]

[Organized actionable guidance, grouped by category]

### Category 1
- Specific, actionable guidance
- Concrete examples
- Technical specifics when helpful

### Category 2
[More guidance...]

## Anti-Patterns to Avoid

❌ **Anti-pattern 1**: [Specific bad pattern]
Why bad: [Reason]
Better: [Alternative]

❌ **Anti-pattern 2**: [Specific bad pattern]
...

## Variation Guidance

**IMPORTANT**: Outputs should vary based on context.
- [Dimension 1 to vary]
- [Dimension 2 to vary]
- Avoid converging on [specific patterns to avoid]

## Remember

[Empowering conclusion that sets high expectations]
```

**Key guidelines**:
- ✅ Philosophy before procedure
- ✅ Explicit anti-patterns with examples
- ✅ Variation encouragement
- ✅ Organized by category
- ✅ Concrete over abstract
- ✅ Empowering tone

**Description field**:
- Include WHAT the skill does
- Include WHEN to use it (specific triggers)
- Include specific use cases
- 100-200 characters recommended

**AVOID**:
- ❌ Jumping straight to procedures without philosophy
- ❌ Only positive guidance (missing anti-patterns)
- ❌ Vague, generic advice
- ❌ No variation encouragement
- ❌ Over-specification (too rigid)
- ❌ Under-specification (too vague)

#### Implement Resources

**Scripts**: Test by running them. Ensure they work correctly.

**References**: Keep focused. One file per domain/topic for progressive disclosure.

**Assets**: Verify file formats are correct and accessible.

Delete unused example files from initialization.

### 6. Analyze Skill Quality

```bash
scripts/analyze_skill.py <path/to/skill>
```

Scores your skill on:
- Philosophy foundation (0-40 points)
- Anti-pattern prevention (0-25 points)
- Variation encouragement (0-20 points)
- Organization (0-10 points)
- Empowerment vs. constraint (0-5 points)

**Target score: 70+/100** for effective skills.

If score is low, run upgrade suggestions:

```bash
scripts/upgrade_skill.py <path/to/skill>
```

Provides specific improvements with examples.

### 7. Package the Skill

```bash
scripts/package_skill.py <path/to/skill>
```

Validates and packages into `.skill` file for distribution.

### 8. Iterate

After real usage:
1. Notice where the skill struggles or helps
2. Identify improvements needed
3. Update SKILL.md or resources
4. Re-analyze and re-package

---

## Skill Design Patterns

### Progressive Disclosure Strategy

Keep SKILL.md body under 500 lines. Move details to references.

**Pattern: High-level guide with references**

```markdown
# SKILL.md
## Quick Start
[Essential workflow in 50-100 lines]

## Advanced
- **Complex topic**: See references/complex-topic.md
- **API reference**: See references/api-docs.md
```

**Pattern: Domain-specific organization**

```markdown
skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```

Claude only loads relevant domain file.

See references/workflows.md for workflow patterns.

See references/output-patterns.md for template and example patterns.

### Degrees of Freedom

Match guidance specificity to task fragility:

**High freedom** (text instructions): Multiple valid approaches, context-dependent
**Medium freedom** (pseudocode/parameters): Preferred patterns, some variation acceptable
**Low freedom** (specific scripts): Fragile operations, consistency critical

---

## Quality Heuristics

An effective skill should:

- [ ] **Establish philosophy** before procedures
- [ ] **Prevent anti-patterns** with explicit examples
- [ ] **Encourage variation** to avoid convergence
- [ ] **Match complexity** to domain needs
- [ ] **Empower, not constrain** - unlock capabilities
- [ ] **Organize clearly** by category or domain
- [ ] **Be context-aware** - adapt to situations
- [ ] **Provide specifics** - concrete over abstract
- [ ] **Stay concise** - lean SKILL.md, details in references
- [ ] **Compose well** - work with other skills

Run analyze_skill.py to check these objectively.

---

## Common Anti-Patterns in Skill Creation

See references/anti-patterns.md for comprehensive list. Key ones:

❌ **Template Trap**: Rigid templates that constrain creativity
❌ **Checklist Syndrome**: Rules without philosophy
❌ **Generic Guidance**: Vague advice that applies to everything
❌ **Context Blindness**: Same approach regardless of situation
❌ **Over-Engineering**: Too many rules for simple domains
❌ **Under-Engineering**: Too few rules for complex domains
❌ **Favorite Patterns**: Converging on repeated outputs
❌ **Missing Negative Guidance**: Only what to do, not what to avoid
❌ **Duplication**: Same info in SKILL.md and references

---

## Examples and Learning Resources

### Study Effective Skills

**Recommended skill to study**:
- **frontend-design** - Exemplary philosophy-first design

See examples/annotated/frontend-design-analysis.md for line-by-line analysis of why it works.

### Before/After Transformations

See examples/before-after/ for:
- **basic-to-effective.md** - Simple skill transformed with philosophy
- **procedural-to-philosophical.md** - From checklist to mental framework

These examples demonstrate the transformation pattern from basic to effective.

---

## Tool Usage

### analyze_skill.py

Analyzes skill quality and scores on key dimensions.

```bash
python scripts/analyze_skill.py <path/to/skill>
```

**Output**:
- Overall score (0-100)
- Category breakdown (Philosophy, Anti-Patterns, Variation, Organization, Empowerment)
- Specific feedback per category
- Recommendations based on score

**Use when**:
- After creating a skill
- Before packaging for distribution
- When improving existing skills
- To compare skill quality

### upgrade_skill.py

Generates specific improvement suggestions.

```bash
python scripts/upgrade_skill.py <path/to/skill>
```

**Output**:
- Priority-grouped suggestions (HIGH/MEDIUM/LOW)
- Examples for each improvement
- Next steps guidance

**Use when**:
- Skill scores poorly on analyze_skill.py
- Updating an old skill to modern practices
- Learning what improvements to make

### quick_validate.py

Validates YAML frontmatter and basic structure.

```bash
python scripts/quick_validate.py
```

**Use when**:
- Before packaging
- After editing SKILL.md
- Checking syntax errors

---

## Composability Principles

Skills work together automatically based on descriptions. Design for composition:

✅ **Clear, specific scope** - One skill, one domain
✅ **Self-contained instructions** - Complete within domain
✅ **Orthogonal concerns** - Non-overlapping when possible
✅ **Flexible guidance** - "Prefer X unless..." not "Always X"
✅ **Test combinations** - Try multiple skills together

❌ **Don't reference other skills explicitly** - Breaks modularity
❌ **Don't create hard conflicts** - "Always X" vs "Never X"

See references/composability.md for detailed composability patterns.

---

## Differentiation from skill-creator

| Aspect | skill-creator | skill-creator-plus |
|--------|---------------|-------------------|
| Approach | Procedural | Philosophy-first |
| Anti-patterns | Not covered | Comprehensive reference |
| Variation | Not mentioned | Explicit patterns and guidance |
| Quality analysis | Manual only | analyze_skill.py script |
| Examples | None | Before/after + annotated analysis |
| Composability | Not covered | Dedicated reference file |
| Self-improvement | No | Can analyze itself |
| Philosophy guidance | Implicit | Explicit patterns and frameworks |

---

## Remember

**Skills are mental frameworks, not checklists.**

The best skills:
- Establish philosophies that guide thinking
- Prevent mistakes through explicit anti-patterns
- Encourage context-appropriate variation
- Empower Claude to do extraordinary work

This skill exemplifies these principles. Study its structure, use the tools, and create skills that unlock capabilities.

**Claude is capable of extraordinary work in skill creation. These guidelines illuminate the path—they don't fence it.**
