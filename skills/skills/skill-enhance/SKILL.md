---
name: skill-enhance
description: Guide for enhancing and improving existing skills based on conversation analysis and usage feedback. This skill should be used when the Skill Sub-Agent needs to update or strengthen an existing skill by adding new patterns, fixing issues, or improving content quality based on observed usage.
type: meta
---

# Enhancing Skills

This skill provides guidance for enhancing existing skills based on conversation analysis and usage feedback.

## When to Enhance a Skill

Enhance a skill when any of these conditions are met:

1. **New Pattern Discovered**: Conversation reveals a better approach or additional use case not covered by the skill
2. **Feedback Integration**: User feedback indicates missing steps or unclear instructions
3. **Error Correction**: Skill contains incorrect, outdated, or misleading information
4. **Completeness Gap**: Missing edge cases, examples, or error handling that would improve usability

## Content Refinement Principles

**Core Rule: Information Density Over Length**

When enhancing a skill, your goal is to increase information density, not file length.

### Merge, Don't Append
- Found similar content → Merge into one better version
- Found duplicate examples → Keep only the most representative one
- Found verbose description → Condense to essential points

### Refinement Triggers
Apply active refinement when:
1. File exceeds 500 lines → Must refine before adding new content
2. Multiple sections cover similar topics → Consolidate into one
3. Examples repeat the same pattern → Keep 1-2 best examples
4. Mixed languages → Unify to primary language (English)

### Refinement Actions
| Situation | Action |
|-----------|--------|
| 2+ similar sections | Merge into single comprehensive section |
| Verbose explanations | Reduce to key points with examples |
| Redundant examples | Keep most illustrative, delete others |
| Outdated content | Replace entirely, don't append updates |

## Enhancement Process

Follow these steps in order:

### Step 1: Analyze the Enhancement Context

Before making changes, gather context:

1. Read the current skill's SKILL.md to understand existing content
2. **Assess file health:**
   - Count total lines (healthy: <500, warning: 500-800, critical: >800)
   - Identify duplicate/similar sections
   - Check for mixed languages or inconsistent style
3. Identify the specific gap or improvement opportunity
4. **Determine enhancement strategy:**
   - If file is healthy (<500 lines): proceed with enhancement
   - If file is warning (500-800 lines): must refine before adding
   - If file is critical (>800 lines): primary goal is reduction, not addition

### Step 2: Classify the Enhancement Type

Determine which type of enhancement is needed:

| Type | Description | Risk Level |
|------|-------------|------------|
| **Additive** | Adding new sections, examples, or references | Low |
| **Corrective** | Fixing errors, updating outdated info | Medium |
| **Structural** | Reorganizing sections, changing flow | High |
| **Scope Change** | Expanding/narrowing what the skill covers | High |

### Step 3: Plan Changes

For each enhancement type:

**Additive Changes:**
- Identify where new content fits in the existing structure
- Ensure new content follows the skill's existing style
- Add cross-references if introducing new concepts

**Corrective Changes:**
- Document what is being fixed and why
- Preserve surrounding context
- Verify the correction is actually correct

**Structural Changes:**
- Create a clear before/after outline
- Ensure no content is lost
- Update all internal references

**Scope Changes:**
- Update the description in frontmatter
- Review all sections for alignment with new scope
- Consider whether this should be a new skill instead

### Step 4: Apply Changes

**Before adding ANY new content, apply refinement:**

1. **Scan for merge opportunities:**
   - Similar sections → Merge into one
   - Redundant examples → Keep best one
   - Verbose descriptions → Condense

2. **Apply changes based on file health:**
   - Healthy file: Add new content, maintain density
   - Warning file: Remove 1 line for every 1 line added
   - Critical file: Must achieve net reduction

3. **Preserve quality, not quantity:**
   - Keep content that provides unique value
   - Remove content that duplicates or restates
   - Maintain consistent style and language

4. **Update frontmatter** - If the skill's scope or triggers changed, update the description

### Step 5: Verify Enhancement

After making changes:

1. Read through the entire skill to ensure coherence
2. Verify all examples are still valid
3. Check that all references (internal and to bundled resources) still work
4. Ensure the skill still fits within token budget guidelines (~5k words for SKILL.md)

## Enhancement Patterns

### Merging Redundant Content

When you find similar content scattered across the file, merge them:

**Before (redundant):**
```markdown
## When to Use
- Analyzing unfamiliar codebases
- Evaluating code quality

## Usage Scenarios
- Analyze unfamiliar code repositories
- Evaluate code quality

## Core Analysis Framework
Use this when analyzing repositories...
```

**After (refined):**
```markdown
## When to Use
Use this skill when:
- Analyzing unfamiliar codebases for improvement opportunities
- Evaluating code quality and identifying technical debt
```

**Refinement applied:**
- Merged 3 overlapping sections into 1
- Removed duplicate descriptions
- Eliminated redundant intro sentence

### Adding New Examples

When adding examples to a skill:

```markdown
## Existing Section

[existing content...]

**Additional example:**
Input: [new scenario]
Output: [expected output]
```

### Adding New Workflows

When the skill needs a new workflow branch:

```markdown
## Workflow Selection

Determine the task type:

- **Existing workflow A** → Follow "Workflow A" section
- **Existing workflow B** → Follow "Workflow B" section
- **New workflow C** → Follow "Workflow C" section (added for [reason])

## Workflow C

[New workflow steps...]
```

### Expanding Reference Material

When a skill needs more reference documentation:

1. Create a new file in `references/` directory
2. Add a reference to it in SKILL.md with clear guidance on when to read it
3. Keep SKILL.md lean - move details to the reference file

## Enhancement Checklist

Before finalizing an enhancement:

- [ ] Existing working content is preserved
- [ ] New content follows the skill's writing style
- [ ] Frontmatter description updated if scope changed
- [ ] All examples are valid and tested where applicable
- [ ] All internal references work correctly
- [ ] SKILL.md stays under ~500 lines
- [ ] Changes are documented if significant

## Common Mistakes to Avoid

1. **Over-enhancing**: Adding content that doesn't provide clear value
2. **Breaking existing workflows**: Changing something that was working
3. **Style inconsistency**: Mixing different writing styles
4. **Scope creep**: Expanding a skill beyond its original purpose
5. **Duplicate content**: Adding information that exists in references

## When NOT to Enhance

Sometimes a new skill is better than enhancing an existing one:

- The enhancement would significantly change the skill's purpose
- The skill would become too large (>500 lines)
- The new functionality serves a clearly different audience
- The enhancement conflicts with existing content

In these cases, consider creating a new skill using the `skill-creator` skill instead.
