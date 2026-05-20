---
name: skill-updater
description: Updates skills during project work according to their contracts. Adds references, improves explanations, and refines examples while respecting skill boundaries. Use when discovering patterns, encountering edge cases, or finding better ways to explain skill concepts. Works with skills that have Skill Contracts defined by skill-contract-generator.
---

# Skill Updater

## Overview

This skill evolves skills during project usage by adding references, improving explanations, and documenting discovered patterns—all while respecting each skill's contract. It reads a skill's "Skill Contract" section to understand what can change and what must remain stable.

## When to Use This Skill

Use this skill when:
- Discovering a pattern or technique that should be added to a skill
- Finding better ways to explain existing skill concepts
- Encountering edge cases not covered by current skill documentation
- Creating project-specific examples worth preserving
- Identifying confusing areas that need clarification

**Important**: Only use with skills that have a "Skill Contract" section (created by `skill-contract-generator`).

## Workflow

### Step 1: Identify Update Opportunity

Recognize when a skill could be improved:

**During project work:**
- "This workflow isn't documented in the skill"
- "This edge case should be mentioned"
- "A better example would clarify this"
- "This pattern keeps coming up"

**Ask yourself:**
- Is this improvement general enough for the skill?
- Or is this project-specific (belongs in CLAUDE.md)?

**Rule of thumb:**
- If useful for other projects → update skill
- If project-specific → document in CLAUDE.md or LOG.md

### Step 2: Read Skill Contract

Locate and read the skill's contract:

**Contract location:**
- In the skill's `SKILL.md` file
- Section titled "## Skill Contract"

**What to extract:**
- **Stable elements**: What cannot be changed
- **Mutable elements**: What can evolve
- **Update rules**: What's allowed, what requires review, what's prohibited
- **Knowledge extraction rules**: What to look for

**If no contract exists:**
- Use `skill-contract-generator` to create one first
- Or proceed conservatively (only add references, no SKILL.md changes)

### Step 3: Classify Update Type

Determine what kind of update is needed:

**Type 1: Add Reference File**
- New patterns, workflows, or examples
- Goes in `references/` directory
- Usually allowed without review

**Type 2: Improve SKILL.md**
- Clarify confusing wording
- Add examples to existing sections
- Fix typos or formatting
- Check contract: may need review

**Type 3: Add Script**
- Automation or validation tool
- Goes in `scripts/` directory
- Check contract: often requires review

**Type 4: Optimize Structure**
- Reorganize sections
- Add new sections
- Usually requires review or is prohibited

### Step 4: Verify Against Contract

Check if the update is allowed:

**Allowed without review:**
- Typically: reference files, examples, typos
- Check contract's "Allowed without review" list
- Proceed to Step 5

**Requires review:**
- Typically: SKILL.md structure changes, new sections
- Check contract's "Requires review" list
- Ask user: "This update requires review per the skill contract. Proceed?"
- If yes → Step 5, if no → Stop

**Prohibited:**
- Check contract's "Prohibited" list
- If prohibited: inform user, suggest alternative
- Example: "Contract prohibits changing workflow steps. Consider adding to references/ instead?"

### Step 5: Prepare Update

Create the update content:

**For reference files:**
```markdown
# [Topic Name]

## Context

[Why this reference is needed]

## Pattern/Workflow/Example

[Detailed content]

## Usage

When to use this pattern:
- [Scenario 1]
- [Scenario 2]

## Related

- Main skill: [section references]
- Other skills: [if applicable]
```

**For SKILL.md updates:**
- Read current content around update point
- Draft new content that matches existing style
- Preserve formatting and structure
- Keep additions concise

**For scripts:**
- Follow SkillOS code style (see CLAUDE.md)
- Add docstrings
- Test before adding

### Step 6: Apply Update

Execute the update:

**Adding reference file:**
```
1. Create file in references/ with descriptive name
2. Add entry to SKILL.md "Resources" section (if exists)
3. Use clear filename: references/[topic]-[type].md
```

**Updating SKILL.md:**
```
1. Read current SKILL.md
2. Find insertion point
3. Insert new content
4. Preserve existing formatting
5. Write updated SKILL.md
```

**Adding script:**
```
1. Create script in scripts/ directory
2. Add to Resources section
3. Document usage in SKILL.md
```

### Step 7: Document the Update

Record what changed and why:

**Update LOG.md:**
```markdown
## YYYY-MM-DD HH:MM

### [REFACTOR] Updated [skill-name] skill

**Context:** [Why this update was needed]

**What Changed:**
- Added `references/[filename].md` documenting [topic]
- [OR] Clarified [section] in SKILL.md
- [OR] Added `scripts/[filename].py` for [purpose]

**Impact:**
- Skill now covers [new scenario]
- Better guidance for [use case]

**Contract compliance:**
- Update type: [allowed without review / reviewed and approved]
- Contract section: [which part of contract allowed this]

**Related:**
- Project: [current project name]
- Skill: `.claude/skills/[skill-name]/`
```

**Optionally update skill's contract:**
- If update reveals new patterns for extraction
- If boundaries should be refined
- Use `skill-contract-generator` to update

### Step 8: Verify and Commit

Ensure update maintains skill quality:

**Checklist:**
- [ ] Contract rules followed
- [ ] Existing content preserved
- [ ] Formatting consistent
- [ ] New content is general (not project-specific)
- [ ] References are clear and useful
- [ ] No broken links or references

**Test if possible:**
- For scripts: run and verify output
- For workflow changes: walk through mentally
- For examples: check they're correct

**Commit:**
- Use git to commit skill update
- Reference in commit message: which skill, why updated

## Update Patterns

### Pattern 1: Adding Project Workflow

**Scenario:** Discovered project-specific workflow that uses the skill

**Action:**
```
1. Create references/[project-type]-workflow.md
2. Document the workflow
3. Add pointer from main SKILL.md if generally useful
```

**Example:** Adding `references/monorepo-git-workflow.md` to `git-workflow` skill

### Pattern 2: Clarifying Confusion

**Scenario:** User confused by existing explanation

**Action:**
```
1. Identify confusing section
2. Add example or clarification
3. Test with fresh perspective
```

**Example:** Adding example to `project-logger` for complex log entries

### Pattern 3: Edge Case Documentation

**Scenario:** Encountered edge case not covered

**Action:**
```
1. Add to existing section if short
2. Or create references/edge-cases.md if many
3. Include workaround or solution
```

**Example:** Adding conflict resolution edge case to `git-workflow`

### Pattern 4: Template Enhancement

**Scenario:** Template missing useful section

**Action:**
```
1. Check contract: template changes often need review
2. If allowed: add section with [OPTIONAL] marker
3. Update template documentation
```

**Example:** Adding optional security section to CLAUDE.md template

## Important Notes

### Respect Skill Contracts

- Contracts exist to preserve skill identity
- Breaking contracts fragments knowledge
- When in doubt, add to references/ not SKILL.md

### General vs. Project-Specific

**Add to skill if:**
- Useful across multiple projects
- Generalizable pattern
- No project-specific details

**Keep in project if:**
- Specific to this codebase
- One-off solution
- Tied to project context

**Decision heuristic:**
- Would 3+ other projects benefit? → Skill
- Unique to this project? → CLAUDE.md or LOG.md

### When to Create New Skill vs. Update

**Update existing skill when:**
- Natural extension of current scope
- Fills gap in existing coverage
- Same domain and user base

**Create new skill when:**
- Different domain or use case
- Would make existing skill too complex
- Distinct workflow or purpose

### Accumulating Knowledge

Updates should accumulate wisdom:
- Each update adds value
- Preserve historical examples (don't replace)
- Build comprehensive coverage over time

## Resources

This skill operates by reading and modifying other skills' files. It doesn't require its own references or scripts, but relies on:
- Skill contracts (created by `skill-contract-generator`)
- Project LOG.md (to document updates)
- Git (to version control changes)

## Skill Contract

**Stable:** 8-step workflow, contract compliance checking, safety verifications
**Mutable:** Update patterns, decision heuristics, examples, edge case documentation
**Update rules:** See `references/contract.md` for detailed rules

> Full contract specification in `references/contract.md`
