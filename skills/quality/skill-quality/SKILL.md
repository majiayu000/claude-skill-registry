---
description: "Validates Claude Code skills against best practices for structure, content quality, and effectiveness. Use when creating new skills, reviewing existing skills, debugging skill invocation issues, or preparing skills for publication."
priority: 5
---

# Skill Quality Validation

Ensures Claude Code skills follow best practices for discoverability, structure, content quality, and effectiveness. This skill provides checklists, patterns, and validation criteria for creating high-quality skills.

## When to Use This Skill

Use this skill when you see these patterns:

### ✅ Yes, use this skill for:

- "Create a new skill for [topic]"
- "Review this skill for quality"
- "Why isn't my skill being invoked?"
- "Improve this skill's structure"
- "Prepare this skill for sharing"
- "Debug skill invocation issues"
- "Make this skill more effective"

### ❌ No, use different skills for:

- Writing skill content (use topic-specific skills)
- Testing specific functionality (use testing skills)
- Code review (use code-review skills)

## Quick Reference

### Core Principles

**Every skill must have:**

- ✅ Specific description with trigger keywords (< 100 chars)
- ✅ Under 500 lines (split into directory if longer)
- ✅ Concrete examples (not abstract)
- ✅ Consistent terminology
- ✅ Progressive disclosure (most important first)

**Red flags:**

- ❌ Vague description like "Help with Python"
- ❌ Single file over 500 lines
- ❌ Abstract guidance without examples
- ❌ Mixing terminology (e.g., "commit" and "change" without explanation)
- ❌ Time-sensitive info (e.g., "new tool just released")

### Quality Checklist Workflow

When creating or reviewing a skill, copy this checklist and follow the steps:

```
Skill Quality Review Progress:
- [ ] Step 1: Verify description and metadata
- [ ] Step 2: Check structure and organization
- [ ] Step 3: Validate content quality
- [ ] Step 4: Review code and scripts (if applicable)
- [ ] Step 5: Test across models
- [ ] Step 6: Perform real usage testing
```

#### Step 1: Verify Description and Metadata

Check the YAML frontmatter:

- [ ] Description includes specific trigger keywords (what users will say)
- [ ] Description explains WHAT the skill does and WHEN to use it
- [ ] Description is in third person ("Validates...", not "Apply...")
- [ ] Description under 1024 characters
- [ ] Priority is set appropriately (5-7 for most skills)
- [ ] Name uses lowercase, hyphens, no reserved words

**If checks fail:** Update frontmatter before proceeding.

#### Step 2: Check Structure and Organization

Review file organization:

- [ ] SKILL.md is under 500 lines
- [ ] Uses directory structure if over 500 lines
- [ ] "When to Use This Skill" section exists and is clear
- [ ] Progressive disclosure: most important content first
- [ ] Headers are descriptive and scannable
- [ ] File references are one level deep maximum

**If checks fail:** Reorganize content or split into supporting files.

#### Step 3: Validate Content Quality

Review the skill content:

- [ ] Examples are concrete and copy-pasteable
- [ ] All code examples are runnable
- [ ] Terminology is consistent throughout
- [ ] No time-sensitive information (or properly isolated)
- [ ] Workflows have clear numbered steps
- [ ] Decision trees for complex choices
- [ ] All placeholders are explained or replaced

**If checks fail:** Add missing examples or clarify instructions.

#### Step 4: Review Code and Scripts

If skill includes executable code:

- [ ] Scripts solve problems (don't punt to Claude)
- [ ] Error handling is explicit with helpful messages
- [ ] All constants are justified (no "voodoo constants")
- [ ] Dependencies are listed with install instructions
- [ ] Paths use forward slashes (not backslashes)
- [ ] Validation/feedback loops for critical operations

**If checks fail:** Improve error handling and documentation.

#### Step 5: Test Across Models

Test with all Claude models:

- [ ] Tested with Haiku (simple case works)
- [ ] Tested with Sonnet (moderate complexity works)
- [ ] Tested with Opus (complex case works)
- [ ] Skill invoked correctly in all cases
- [ ] Responses follow skill guidance consistently

**If checks fail:** Adjust description or add more explicit guidance.

#### Step 6: Perform Real Usage Testing

Test in actual workflows:

- [ ] Fresh start test (new project, no external docs)
- [ ] Colleague test (someone else uses it)
- [ ] Different project test (verify it's project-agnostic)
- [ ] Error path test (intentionally trigger failures)

**If checks fail:** Update skill based on observed issues.

## File Structure

**For skills under 500 lines:**

```
my-skill.md                # Single file
```

**For skills over 500 lines:**

```
my-skill/
├── SKILL.md              # Main instructions (< 500 lines)
├── examples.md           # Detailed examples
├── reference.md          # API/command reference (optional)
└── scripts/              # Helper scripts (optional)
    └── validate.py
```

**Key principles:**

- SKILL.md always under 500 lines
- Related files use UPPERCASE for visibility (FORMS.md, EXAMPLES.md)
- Scripts in subdirectory, executed not loaded as context
- Each file has single, clear purpose

**Example from real skill:**

```
pdf/
├── SKILL.md              # Core PDF guidance
├── FORMS.md              # Form-filling specific guidance
├── examples.md           # Extended examples
└── scripts/
    ├── analyze_form.py   # Utility script
    └── fill_form.py      # Form processor
```

## Core Quality Standards

### 1. Description Quality

**Format:** Frontmatter YAML at top of SKILL.md

```yaml
---
description: "Specific action + key terms + when to use"
priority: 5
---
```

**Requirements:**

- Include key terms that trigger the skill
- Explain both WHAT and WHEN
- Keep under 100 characters
- Use terms users naturally say

📖 See [EXAMPLES.md](./EXAMPLES.md#description-quality) for good/bad examples

### 2. Content Structure

**SKILL.md must be:**

- Under 500 lines total
- Well-organized with clear sections
- Using progressive disclosure
- Focused on one coherent topic

**If exceeding 500 lines:**

1. Split into directory structure
2. Keep core guidance in SKILL.md
3. Move detailed examples to examples.md
4. Move reference material to reference.md
5. Move scripts to scripts/ subdirectory

**Progressive disclosure pattern:**

```markdown
# Skill Name

Brief intro (1-2 sentences)

## When to Use

Quick bullet list

## Quick Reference

Most common cases with examples

## Detailed Guidance

(Or link to examples.md)

## Advanced Patterns

(Or link to patterns.md)
```

### 3. Terminology Consistency

**Rules:**

- Use consistent terms throughout all files
- Establish vocabulary early
- Explain synonyms when first used
- Don't mix related terms without explanation

📖 See [EXAMPLES.md](./EXAMPLES.md#terminology-consistency) for patterns

### 4. Concrete Examples

**Every pattern needs a real, runnable example.**

Examples must:

- Be copy-pasteable
- Show actual code/commands
- Include expected output
- Demonstrate the principle

📖 See [EXAMPLES.md](./EXAMPLES.md#concrete-examples) for good/bad examples

### 5. File Reference Depth

**Keep references one level deep:**

```markdown
See examples.md for detailed patterns # ✅ Good
```

```markdown
See examples.md which references patterns.md
which has code in scripts/ # ❌ Bad - too deep
```

### 6. Time-Sensitive Information

**Isolate or avoid time-sensitive content:**

```markdown
## Current Best Practice (as of 2024)

Use ast-grep for syntax-aware searches

## Legacy Patterns

Previously, ripgrep was used...
```

📖 See [EXAMPLES.md](./EXAMPLES.md#time-sensitive-information) for deprecation patterns

## Code and Script Quality

### Scripts Should Solve Problems

**Don't punt to Claude - solve the problem in the script:**

- ✅ Validate and return specific errors
- ✅ Handle edge cases explicitly
- ✅ Provide actionable error messages
- ❌ Leave TODOs for Claude to figure out
- ❌ Generic "check this" functions

### Error Handling

**Every error path needs helpful messages:**

```python
except FileNotFoundError:
    print("Error: jj not found. Install with: brew install jj")
    sys.exit(1)
```

### No Voodoo Constants

**Justify all magic numbers:**

```python
TIMEOUT_SECONDS = 30  # API requests take 5-10s, allow 3x buffer
```

### Package Verification

**List all dependencies with install instructions:**

```markdown
## Dependencies

Required:

- `ast-grep` - Install: `brew install ast-grep`

Verify: `which ast-grep`
```

📖 See [EXAMPLES.md](./EXAMPLES.md#code-and-script-quality) for detailed patterns

## Workflow Quality

### Clear Steps

**Use numbered steps with verification:**

````markdown
1. **Create directory:**
   ```bash
   mkdir my-dir
   ```
````

Verify: `ls my-dir`

2. **Create file:**
   ...

````

### Decision Trees

**Complex workflows need decision points:**

```markdown
**Need X?** → Use tool A
**Need Y?** → Use tool B
**Need both?** → Use A then B
````

📖 See [EXAMPLES.md](./EXAMPLES.md#workflow-quality) for patterns

## Testing

Every skill needs testing across:

- **Models**: Haiku, Sonnet, Opus
- **Scenarios**: Simple, edge case, complex
- **Real usage**: New project, no external help

📖 See [TESTING.md](./TESTING.md) for detailed testing guidelines

## Troubleshooting

Common issues:

- Skill not being invoked → Check description keywords
- Too broad → Split into focused skills
- Too abstract → Add concrete examples

📖 See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for complete guide

## Quality Self-Check

Before considering a skill complete, copy this checklist and verify each item:

```
Skill Quality Verification:
- [ ] Can someone use this without follow-up questions?
- [ ] Would this work in 6 months?
- [ ] Are examples copy-pasteable and runnable?
- [ ] Can you find guidance in < 30 seconds?
- [ ] Are error messages helpful enough?
- [ ] Does the description include key trigger terms?
- [ ] Is SKILL.md under 500 lines?
- [ ] Are file references one level deep?
- [ ] Is terminology consistent throughout?
```

**If any check fails:**

1. **Can't use without follow-up questions** → Add more concrete examples
2. **Won't work in 6 months** → Isolate time-sensitive info in "Current Best Practice" sections
3. **Examples not copy-pasteable** → Complete all placeholders and add setup steps
4. **Can't find guidance quickly** → Improve headers and add table of contents
5. **Error messages unclear** → Add context, hints, and recovery steps
6. **Description lacks triggers** → Add specific terms users naturally say
7. **SKILL.md too long** → Split into directory with reference files
8. **Deep file references** → Consolidate or flatten structure
9. **Inconsistent terminology** → Choose one term and use everywhere

## Evaluation Scenarios

Test this skill with these scenarios to ensure it works effectively:

### Scenario 1: Simple Case - New Skill Creation

**Input:** "Help me create a new skill for managing Docker containers"

**Expected behavior:**

- Skill is invoked and recognized
- Provides description template with trigger keywords
- Suggests file structure (single file vs directory)
- Offers checklist for required sections
- Reminds about concrete examples requirement

**Verify:**

- Skill invocation happens automatically
- Response includes specific checklist items
- Guidance is actionable and clear

### Scenario 2: Edge Case - Skill Not Being Invoked

**Input:** "My skill exists but Claude never uses it"

**Expected behavior:**

- Skill is invoked and recognized
- Diagnoses common invocation issues
- Checks description for trigger keywords
- Verifies file location and frontmatter format
- Suggests testing phrases

**Verify:**

- Troubleshooting steps are provided
- Specific fixes offered for each issue
- Testing methodology explained

### Scenario 3: Complex Case - Comprehensive Skill Review

**Input:** "Review my python-scripts skill for quality and best practices"

**Expected behavior:**

- Skill is invoked and recognized
- Provides complete quality checklist
- Reviews description, structure, examples, and testing
- Identifies specific gaps or issues
- Suggests prioritized improvements
- References relevant sections of examples.md

**Verify:**

- All quality dimensions covered
- Specific, actionable feedback provided
- Prioritization of issues clear
- References to supporting documentation included

## Additional Resources

- [EXAMPLES.md](./EXAMPLES.md) - Detailed good/bad examples for all principles
- [TESTING.md](./TESTING.md) - Complete testing guidelines
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues and fixes
