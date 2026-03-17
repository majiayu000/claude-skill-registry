---
name: skill-discovery
description: Use when user asks about available skills or when searching for relevant expertise - scans .claude/skills/ and lists skills by category with descriptions
allowed-tools: Read, Glob, Grep
---

# Skill Discovery

## Purpose

Help users and Claude discover available skills organized by category, understand when to use them, and identify gaps where new skills should be created.

## When to Use This Skill

Activate automatically when:
- User asks "What skills are available?"
- User requests "List all skills"
- You need to find a skill for a specific task
- You're identifying whether a relevant skill exists
- You're planning workflow improvements

## Discovery Process

### 1. Scan Skill Directories

Use Glob to find all skills:
```
.claude/skills/meta/*/SKILL.md
.claude/skills/quality-gates/*/SKILL.md
.claude/skills/context-assembly/*/SKILL.md
.claude/skills/workflows/*/SKILL.md
```

### 2. Extract Metadata

For each SKILL.md file:
- Read the YAML frontmatter
- Extract `name` and `description`
- Note the category (from directory path)

### 3. Organize by Category

Group skills into four categories:

**Meta Skills** - System improvement and skill management
**Quality Gates** - Validation and compliance checks
**Context Assembly** - Reusable context gathering patterns
**Workflows** - Complete multi-stage processes

### 4. Present Results

Format output as:

```markdown
## Available Skills

### Meta Skills
- **skill-name**: Description of what it does and when to use it
- **another-skill**: Description...

### Quality Gates
- **citation-compliance**: Description...
- **epic-validation**: Description...

### Context Assembly
- **meeting-synthesis**: Description...
- **research-gathering**: Description...

### Workflows
- **content-pipeline**: Description...
- **product-planning**: Description...
```

## Search by Keyword

When user provides a keyword (e.g., "citation", "epic", "content"):
1. Use Grep to search descriptions: `grep -i "keyword" .claude/skills/**/*.md`
2. Return matching skills with full descriptions
3. Suggest related skills

## Gap Identification

When no relevant skill exists for a task:
1. Clearly state: "No existing skill found for [task description]"
2. Suggest: "This may be a good candidate for a new skill"
3. Recommend: "Use the `create-skill` meta-skill to generate one"

## Quick Reference Table

| Category | Purpose | Example Skills |
|----------|---------|----------------|
| Meta | System improvement | using-skills, skill-discovery, create-skill |
| Quality Gates | Validation checks | citation-compliance, epic-validation |
| Context Assembly | Reusable context | meeting-synthesis, research-gathering |
| Workflows | End-to-end processes | content-pipeline, product-planning |

## Success Criteria

- User can see all available skills in one view
- Skills are organized logically by category
- Descriptions clearly indicate when to use each skill
- User can search by keyword to find relevant skills
- Gaps are identified proactively

## Common Mistakes

- Listing skills without descriptions (not helpful)
- Failing to organize by category (creates confusion)
- Not suggesting skill creation when gaps exist
- Searching only skill names instead of full descriptions
