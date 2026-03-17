---
name: canonical-format-checker
description: This skill should be used when content teaches patterns (skills, subagents, ADRs, PHRs, specifications) that have canonical sources elsewhere. Prevents format drift by ensuring content references and follows the authoritative format from canonical sources. Use before implementing lessons that teach platform patterns, or when reviewing content for format consistency.
---

# Canonical Format Checker

## Overview

Prevent format drift by verifying content follows authoritative canonical sources. When teaching a pattern that exists elsewhere in the platform (skills, subagents, ADRs, etc.), this skill ensures the taught format matches the canonical source.

**Why this matters**: The Chapter 14 format drift failure occurred because the lesson taught skill format differently from Chapter 5 (canonical source). Students learned incorrect patterns that contradicted earlier chapters.

## When to Use This Skill

**Automatic Triggers** (check before implementation):
- Lesson teaches how to create skills → Check `.claude/skills/` structure
- Lesson teaches how to write subagents → Check `.claude/agents/` structure
- Lesson teaches ADR format → Check `specs/*/adrs/` structure
- Lesson teaches PHR format → Check `history/prompts/` structure
- Lesson teaches specification format → Check `specs/*/spec.md` structure

**Manual Triggers** (user requests):
- "Check canonical format for skills"
- "Verify format consistency"
- "Does this match the canonical source?"

## Canonical Source Lookup Table

| Pattern Being Taught | Canonical Source Location | Key Format Elements |
|---------------------|--------------------------|---------------------|
| **Skills** | `.claude/skills/<name>/SKILL.md` | Directory structure, YAML frontmatter with `name`, `description` |
| **Subagents** | `.claude/agents/<name>.md` | YAML frontmatter with `name`, `description`, `model`, `skills` |
| **ADRs** | `specs/<feature>/adrs/adr-*.md` | Numbered files, standard ADR structure |
| **PHRs** | `history/prompts/<stage>/` | Template from `.specify/templates/phr-template.prompt.md` |
| **Specifications** | `specs/<feature>/spec.md` | Sections: Overview, User Stories, FRs, SCs, Evals |
| **Commands** | `.claude/commands/*.md` | YAML frontmatter, step-by-step phases |

## Workflow

### Step 1: Identify What Pattern Is Being Taught

Ask yourself:
- Does this lesson teach how to CREATE any platform pattern?
- Is there an existing canonical source for this pattern?

```
Trigger Examples:
- "Lesson teaches students to write their own skills" → Skills pattern
- "Chapter covers custom commands" → Commands pattern
- "Module explains agent creation" → Subagents pattern
```

### Step 2: Locate and Read Canonical Source

**MANDATORY**: Read the canonical source BEFORE writing or reviewing content.

```bash
# For Skills - read actual skill structure
ls .claude/skills/*/
cat .claude/skills/session-intelligence-harvester/SKILL.md

# For Agents - read actual agent structure
ls .claude/agents/
cat .claude/agents/content-implementer.md

# For Commands - read actual command structure
ls .claude/commands/
head -50 .claude/commands/sp.specify.md
```

### Step 3: Extract Format Requirements

Document the required format elements from canonical source:

```markdown
## Canonical Format: Skills

**Directory Structure**:
```
.claude/skills/
└── <skill-name>/          # Directory, NOT flat file
    └── SKILL.md           # SKILL.md file (uppercase)
```

**YAML Frontmatter** (REQUIRED):
```yaml
---
name: "<skill-name>"
description: "This skill should be used when... Use when..."
---
```

**Content Structure**:
1. H1 title matching skill name
2. Overview section explaining purpose
3. When to Use section with triggers
4. Workflow section with steps
```

### Step 4: Compare Content Against Canonical

Check the lesson/content for format consistency:

```markdown
## Format Comparison Checklist

**Skill Format Check**:
- [ ] Shows directory structure (not flat file)
- [ ] Uses SKILL.md filename (not skill.md or index.md)
- [ ] Includes YAML frontmatter with `name` and `description`
- [ ] `description` starts with "This skill should be used when..."

**Agent Format Check**:
- [ ] Shows single .md file in agents directory
- [ ] Includes YAML frontmatter with `name`, `description`, `model`
- [ ] Includes `skills` array (can be empty)
- [ ] Description explains when to invoke

**Command Format Check**:
- [ ] Shows .md file in commands directory
- [ ] Has numbered phases with clear gates
- [ ] Includes enforcement checks
```

### Step 5: Report Drift or Confirm Compliance

**If Format Drift Detected**:
```markdown
## Format Drift Detected

**Pattern**: Skills
**Location**: Lesson 7, Section "Creating Your First Skill"

**Issue**: Shows flat file `.claude/skills/my-skill.md`
**Canonical**: Directory structure `.claude/skills/my-skill/SKILL.md`

**Specific Fixes Required**:
1. Line 45: Change `.claude/skills/my-skill.md` to `.claude/skills/my-skill/SKILL.md`
2. Line 52: Update example to show directory creation with `mkdir`
3. Line 60: Add YAML frontmatter example with required fields

**Cross-Reference**: Chapter 5, Lesson 7 (agent-skills.md) is canonical source
```

**If Format Compliant**:
```markdown
## Format Verified

**Pattern**: Skills
**Canonical Source**: `.claude/skills/session-intelligence-harvester/SKILL.md`
**Content Location**: Chapter 14, Lesson 5

**Verification**:
- [x] Directory structure matches canonical
- [x] YAML frontmatter format correct
- [x] Required fields present (name, description)
- [x] Description follows "This skill should be used when..." pattern

**Status**: COMPLIANT - No drift detected
```

## Common Format Drift Patterns

### Drift Pattern 1: Flat Files vs Directories
**Wrong**: `.claude/skills/my-skill.md`
**Right**: `.claude/skills/my-skill/SKILL.md`

### Drift Pattern 2: Missing YAML Frontmatter
**Wrong**: Markdown file with no frontmatter
**Right**: YAML frontmatter with required fields

### Drift Pattern 3: Wrong Filename
**Wrong**: `skill.md`, `index.md`, `README.md`
**Right**: `SKILL.md` (uppercase)

### Drift Pattern 4: Missing Required Fields
**Wrong**: Only `name` in frontmatter
**Right**: Both `name` and `description` (description starts with "This skill should be used when...")

### Drift Pattern 5: Inventing New Format
**Wrong**: Creating custom format not matching canonical
**Right**: Following exact structure from canonical source

## Integration Points

**Use With**:
- `chapter-planner` - Check during lesson planning phase
- `content-implementer` - Verify before implementation
- `validation-auditor` - Include in validation checklist

**Invoke When**:
- Planning lessons that teach platform patterns
- Reviewing content that describes file structures
- Validating documentation about Claude Code features

## Self-Monitoring

Before approving content that teaches patterns:

- [ ] Identified what pattern is being taught
- [ ] Located and READ the canonical source
- [ ] Extracted format requirements from canonical
- [ ] Compared content against canonical requirements
- [ ] Detected drift OR confirmed compliance
- [ ] Provided specific fix instructions if drift found

## Success Criteria

**You succeed when**:
- Format drift detected BEFORE publication
- Specific canonical source identified and referenced
- Exact format requirements documented
- Content matches canonical source exactly

**You fail when**:
- Content teaches incorrect format that contradicts canonical
- Canonical source not checked before implementation
- Vague feedback ("fix the format") instead of specific corrections
- New patterns invented instead of following canonical
