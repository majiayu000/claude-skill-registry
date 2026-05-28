---
name: lesson-generator
description: Generate lesson content following 4-Layer Teaching Framework with standardized metadata and Docusaurus conventions
domain: authoring
version: 1.0.0
created: 2025-11-28
updated: 2025-11-29
triggers:
  - Creating new lessons for any module
  - Generating lesson drafts from specifications
  - Ensuring consistent lesson structure across books
dependencies:
  - docusaurus-conventions (file naming, MDX syntax)
learned_from:
  - Module 1 ROS 2 implementation metadata standardization (2025-11-29)
---

# Lesson Generator Skill

## Persona

Think like a curriculum designer who creates consistent, high-quality lessons that build progressively. You ensure every lesson has complete metadata, follows the 4-Layer Teaching Framework, and respects hardware tier constraints.

---

## Pre-Flight Questions

Before generating any lesson content, ask yourself:

### 1. Context Gathering
- **Q**: What module and chapter is this lesson in?
  - **Impact**: Determines layer (L1-L4), proficiency, and hardware requirements

- **Q**: What lessons come before and after?
  - **Impact**: Ensures continuity and avoids redundancy

- **Q**: What is the target proficiency level?
  - **A2 (Beginner)**: 5-7 concepts, heavy scaffolding
  - **B1 (Intermediate)**: 7-10 concepts, moderate scaffolding
  - **C2 (Advanced)**: No concept limits, minimal scaffolding

### 2. Metadata Completeness
- **Q**: Does this lesson have ALL required metadata fields?
  - See [Required Metadata Fields](#required-metadata-fields) below

### 3. Docusaurus Conventions
- **Q**: Am I following all Docusaurus conventions?
  - File extension: `.md` (not `.mdx`)
  - No Mermaid diagrams
  - No `<` in prose
  - Links use `.md` and `README.md`
  - See: `docusaurus-conventions` skill

---

## Required Metadata Fields

### Complete Frontmatter Template

```yaml
---
id: lesson-{chapter}-{lesson}-{slug}
title: "Lesson {C}.{L}: {Title}"
sidebar_position: {N}
sidebar_label: "{C}.{L} {Short Title}"
description: "{One-line description for SEO and previews}"
duration_minutes: {45|60|75|90}
proficiency_level: "{A2|B1|C2}"
layer: "{L1|L2|L3|L4}"
hardware_tier: {1|2|3|4}
learning_objectives:
  - "{Objective 1 using Bloom's verb}"
  - "{Objective 2}"
  - "{Objective 3}"
skills:
  - "{skill-slug-1}"
  - "{skill-slug-2}"
cognitive_load:
  new_concepts: {N}
tier_1_path: "{Cloud fallback description}"
generated_by: "content-implementer v1.0.0"
created: "{YYYY-MM-DD}"
version: "1.0.0"
---
```

### Field Descriptions

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `id` | Yes | Unique across all docs | `lesson-1-1-digital-to-physical` |
| `title` | Yes | Full lesson title | `"Lesson 1.1: From ChatGPT to Walking Robots"` |
| `sidebar_position` | Yes | Order in sidebar | `1` |
| `sidebar_label` | Yes | Short label for sidebar | `"1.1 Digital to Physical"` |
| `description` | Yes | SEO/preview text | `"Understanding differences between software and embodied AI"` |
| `duration_minutes` | Yes | Expected completion time | `45` |
| `proficiency_level` | Yes | CEFR-aligned level | `"A2"`, `"B1"`, `"C2"` |
| `layer` | Yes | Teaching layer | `"L1"`, `"L2"`, `"L3"`, `"L4"` |
| `hardware_tier` | Yes | Minimum hardware required | `1` (cloud), `2` (GPU), `3` (Jetson), `4` (robot) |
| `learning_objectives` | Yes | Measurable outcomes (3-5) | Array of strings |
| `skills` | Yes | Related skill slugs | `["ros2-fundamentals", "ros2-cli"]` |
| `tier_1_path` | Recommended | Cloud fallback | `"Cloud ROS 2 (TheConstruct)"` |
| `cognitive_load.new_concepts` | Recommended | Concept count | `7` |
| `generated_by` | Yes | Generator attribution | `"content-implementer v1.0.0"` |
| `created` | Yes | Creation date | `"2025-11-29"` |
| `version` | Yes | Content version | `"1.0.0"` |

### Deprecated Fields (Do Not Use)

| Deprecated | Use Instead |
|------------|-------------|
| `cefr_level` | `proficiency_level` |
| `duration` | `duration_minutes` |
| `estimated_time` | `duration_minutes` |
| `chapter` / `lesson` | `id` with pattern |

---

## Principles

### Principle 1: Metadata-First Generation

**Always generate complete metadata BEFORE content.**

The metadata defines:
- How the lesson appears in navigation
- What proficiency constraints apply
- What hardware is required
- What learning is measured

### Principle 2: Layer-Appropriate Structure

**L1 (Manual Foundation)**:
- Direct explanations with analogies
- Step-by-step walkthroughs
- NO AI collaboration yet
- Heavy scaffolding

**L2 (AI Collaboration)**:
- Three Roles framework (invisible to student)
- Bidirectional learning examples
- "Try With AI" prompts
- Moderate scaffolding

**L3 (Intelligence Design)**:
- Create reusable skills/patterns
- Encode tacit knowledge
- Cross-project value
- Minimal scaffolding

**L4 (Spec-Driven)**:
- Specification-first approach
- Compose accumulated intelligence
- Capstone integration
- Professional autonomy

### Principle 3: Hardware-Aware Content

**Every lesson must specify:**
1. Minimum `hardware_tier` (1-4)
2. `tier_1_path` fallback for cloud users
3. Hardware gates for tier-specific content

```markdown
**Hardware Tier**: {N} | **Cloud Path**: {fallback description}
```

### Principle 4: Consistent Naming

**ID Pattern**: `lesson-{chapter}-{lesson}-{slug}`
- `lesson-1-1-digital-to-physical`
- `lesson-3-4-services-parameters`
- `lesson-7-3-testing-validation`

**Sidebar Label Pattern**: `"{C}.{L} {Short Title}"`
- `"1.1 Digital to Physical"`
- `"3.4 Services & Parameters"`
- `"7.3 Testing Validation"`

---

## Lesson Structure Template

```markdown
---
[Complete frontmatter - see above]
---

# {Lesson Title}

**Duration**: {N} minutes | **Layer**: {L1-L4} | **Tier**: {N} ({description})

{Opening hook - 2-3 paragraphs motivating the topic}

## Learning Objectives

By the end of this lesson, you will be able to:
- {Objective 1}
- {Objective 2}
- {Objective 3}

## {Section 1: Core Content}

{Layer-appropriate content}

### {Subsection}

{Progressive explanation}

## {Section 2: Practice/Application}

{Hands-on content appropriate to layer}

## {Section 3: Assessment} (optional for L1)

{Understanding validation}

## Try With AI

{AI collaboration prompts - required for L2+}

---

**Previous:** [Link] | **Next:** [Link]
```

---

## Checklist (Use Before Every Lesson)

### Metadata
- [ ] All required fields present
- [ ] `id` is unique and follows pattern
- [ ] `proficiency_level` not `cefr_level`
- [ ] `duration_minutes` not `duration`
- [ ] `skills` array populated
- [ ] `hardware_tier` specified
- [ ] `tier_1_path` for tier > 1

### Content
- [ ] Opening hook engages reader
- [ ] Learning objectives measurable (Bloom's verbs)
- [ ] Layer-appropriate teaching approach
- [ ] Code examples have outputs (for L2+)
- [ ] "Try With AI" section present (for L2+)

### Docusaurus
- [ ] File extension `.md`
- [ ] No Mermaid diagrams
- [ ] No `<` in prose
- [ ] Links use `.md` extension
- [ ] Build passes

---

## Integration

This skill is typically invoked by:
- `content-implementer` agent during `/sp.implement`
- Direct lesson creation workflows
- Module content generation

**Dependencies**:
- `docusaurus-conventions` - File naming and syntax
- `learning-objectives` - Bloom's taxonomy alignment
- `assessment-builder` - Proficiency-appropriate assessments

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 0.1.0 | 2025-11-28 | Initial placeholder |
| 1.0.0 | 2025-11-29 | Full implementation with metadata standards from Module 1 |
