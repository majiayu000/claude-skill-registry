---
name: refine-workflow
description: Use when analyzing workflow effectiveness or identifying skill extraction opportunities - systematically identifies patterns worthy of new skills and improvement areas
---

# Refine Workflow

## Purpose

Analyze existing workflows to:
- Identify repeating patterns that should become skills
- Find quality gates embedded in workflows that should be extracted
- Discover context assembly patterns used across multiple workflows
- Optimize workflow efficiency and maintainability

## When to Use This Skill

Activate when:
- User asks "How can we improve this workflow?"
- You notice repeated logic across multiple workflows
- A workflow is becoming too long or complex
- Quality controls are duplicated in multiple places
- Context gathering patterns are reused frequently
- User requests workflow analysis or optimization

## Analysis Framework

### 1. Pattern Recognition

Scan workflows for these patterns:

**Validation Patterns** (candidates for quality gates):
- Citation checking logic
- Schema validation
- Style enforcement
- Link verification
- Data integrity checks

**Context Assembly Patterns** (candidates for context skills):
- Meeting transcript synthesis
- Research gathering by topic
- Priority scoring algorithms
- Source normalization logic

**Reusable Procedures** (candidates for technique skills):
- File parsing routines
- YAML processing
- State management
- Checkpoint creation

### 2. Duplication Detection

Identify logic duplicated across workflows:

**Method:**
1. List all workflow skills in `.claude/skills/workflows/`
2. Read each SKILL.md file
3. Identify common phrases, procedures, or validation steps
4. Group duplicates by similarity
5. Prioritize by frequency and impact

**Threshold:**
- If logic appears in 3+ workflows → strong extraction candidate
- If logic appears in 2 workflows → potential extraction candidate
- If logic is complex and appears once → consider extraction for clarity

### 3. Complexity Analysis

Measure workflow complexity:

**Token Count:**
- Count total tokens in SKILL.md
- If >1000 tokens → candidate for decomposition
- If >2000 tokens → high priority for decomposition

**Step Count:**
- Count numbered procedure steps
- If >10 steps → consider breaking into phases
- If >20 steps → high priority for decomposition

**Quality Gates:**
- Count embedded validation steps
- If >3 validations → extract quality gates
- If validation logic >100 tokens → extract as separate skill

### 4. Dependency Mapping

Understand skill relationships:

**Create a dependency graph:**
1. List all workflow skills
2. For each skill, identify invoked sub-skills
3. Identify quality gates applied
4. Map context assembly patterns used
5. Visualize relationships

**Look for:**
- Skills that never invoke sub-skills (atomic candidates)
- Skills with circular dependencies (refactoring needed)
- Quality gates not yet extracted
- Orphaned workflows (unused skills)

## Extraction Process

### When to Extract a Quality Gate

**Criteria:**
1. Validation logic appears in 2+ workflows
2. Validation has pass/fail criteria
3. Validation is atomic (self-contained)
4. Validation enforces a specific standard

**Extraction Steps:**
1. Use `create-skill` meta-skill
2. Target category: `.claude/skills/quality-gates/`
3. Define iron law (non-negotiable requirement)
4. Include anti-rationalization blocks
5. Update workflows to invoke the quality gate

**Example:**
```
Before: Citation checking embedded in content-pipeline skill
After: `citation-compliance` quality gate skill invoked by content-pipeline
```

### When to Extract Context Assembly

**Criteria:**
1. Context gathering logic appears in 2+ workflows
2. Logic synthesizes data from multiple sources
3. Logic applies reusable filters or transformations
4. Logic produces standardized output format

**Extraction Steps:**
1. Use `create-skill` meta-skill
2. Target category: `.claude/skills/context-assembly/`
3. Define input sources and output schema
4. Include filtering and normalization logic
5. Update workflows to invoke the context assembly skill

**Example:**
```
Before: Meeting synthesis logic duplicated in product-planning and cs-prep
After: `meeting-synthesis` context skill invoked by both workflows
```

### When to Extract a Sub-Workflow

**Criteria:**
1. Workflow has >10 steps
2. Steps can be grouped into logical phases
3. Phases have clear checkpoints
4. Phases may be useful independently

**Extraction Steps:**
1. Identify phase boundaries
2. Create sub-workflow skills for each phase
3. Update parent workflow to invoke sub-workflows
4. Maintain state between phases

**Example:**
```
Before: content-pipeline (20 steps in one skill)
After: content-pipeline invokes:
  - content-intent-gathering
  - content-brief-creation
  - content-outlining
  - content-drafting
  - content-snippet-generation
```

## Optimization Techniques

### Token Efficiency

**Reduce token usage:**
1. Replace verbose examples with concise ones
2. Use tables for quick reference
3. Inline simple code, link to external files for complex code
4. Remove redundant explanations

**Targets:**
- Frequently-loaded skills: <200 words
- Other skills: <500 words

### Description Optimization (CSO)

**Improve auto-discovery:**
1. Front-load distinctive triggering conditions
2. Include specific symptoms (not abstract categories)
3. Use third-person perspective
4. Start with "Use when..."

**Test effectiveness:**
- Create scenarios where skill should activate
- Verify Claude auto-discovers the skill
- Refine description if activation fails

### Cross-Reference Clarity

**Improve skill invocation:**
1. Mark required dependencies with asterisks
2. Use explicit skill names (not @ syntax)
3. Explain integration points
4. Document expected inputs/outputs

## Refining Workflow

### 1. Analyze Current State

Run pattern recognition, duplication detection, and complexity analysis.

### 2. Identify Improvements

Prioritize extraction candidates:
- High duplication + high impact = highest priority
- High complexity + low modularity = high priority
- Single-use but complex = medium priority

### 3. Create Extraction Plan

For each candidate:
1. Define new skill name and category
2. Specify extraction boundaries (what moves, what stays)
3. Identify workflows that will invoke the new skill
4. Estimate token savings

### 4. Execute Extractions

Use `create-skill` meta-skill for each new skill:
1. Write failing test first
2. Extract logic into new SKILL.md
3. Update parent workflows to invoke new skill
4. Validate integration

### 5. Validate Improvements

**Metrics:**
- Total token count before/after
- Duplication eliminated (lines of duplicated logic removed)
- Modularity score (number of reusable components)
- Maintainability (ease of updating)

## Success Criteria

Workflow is refined when:
- No logic duplicated across 3+ workflows
- All workflows <1000 tokens
- Quality gates extracted and reusable
- Context assembly patterns standardized
- Skill dependencies clearly mapped
- Token efficiency maximized

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Extracting too aggressively | Keep skills >100 words; don't over-modularize |
| Missing CSO opportunities | Optimize descriptions for auto-discovery |
| Breaking working workflows | Test before/after with real scenarios |
| Not updating invoking workflows | Ensure parent workflows reference new skills |
| Forgetting documentation | Use documentation-sync quality gate (all 6 files) |

## Related Skills

- **create-skill**: Use after identifying extraction candidates
- **skill-discovery**: Find existing skills before creating duplicates
- **using-skills**: Ensure extracted skills are used mandatorily
- **documentation-sync**: Required for maintaining documentation consistency after extraction
