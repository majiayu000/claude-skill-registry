---
name: creating-skill
description: Creates Skills for Claude. Use when users request creating/updating skills, need skill structure guidance, or mention extending Claude's capabilities through custom skills.
metadata:
  version: 2.1.2
---

# Creating Skills

Create portable, reusable expertise that extends Claude's capabilities across contexts.

## When to Create Skills

Skills are appropriate when:
- Capability needed across multiple projects/conversations
- Procedural knowledge that applies broadly (not project-specific)
- Instructions should activate automatically on trigger patterns
- Want portable expertise that loads progressively on-demand

Not appropriate when:
- Context is project-specific (use Project instructions instead)
- One-off task (use standalone prompt instead)
- See **crafting-instructions** skill for detailed decision framework

## Skill Structure

Every skill is a directory containing:
- `SKILL.md` (required): Frontmatter + imperative instructions
- `scripts/` (optional): Executable code for deterministic operations
- `references/` (optional): Detailed docs loaded on-demand
- `assets/` (optional): Templates/files used in output

Create this structure directly:
```bash
mkdir -p skill-name/{scripts,references,assets}
```

Delete unused directories before packaging.

## Naming Convention

Use gerund form (verb + -ing):
- ✅ `processing-pdfs`, `analyzing-data`, `creating-reports`
- ❌ `pdf-helper`, `data-tool`, `report-maker`

Requirements:
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- No reserved words (anthropic, claude)

## Frontmatter Requirements

```yaml
---
name: skill-name
description: What it does. Use when [trigger patterns].
---
```

**name:** Follow naming convention above

**description:** (max 1024 chars)
- Third person voice: "Processes files" not "I process files"
- WHAT it does + WHEN to use it (trigger patterns)
- Specify: file types, keywords, task types that should activate this skill
- No XML tags

**Good examples:**
- "Creates PowerPoint presentations. Use when users mention slides, .pptx files, or presentations."
- "Analyzes SQL queries for performance. Use when debugging slow queries, optimization requests, or EXPLAIN output."

**Ineffective examples:**
- "I can help create presentations" (first person, no triggers)
- "Presentation creator" (no triggers, vague what)
- "Advanced presentation creation with animations" (over-detailed implementation)

The description is critical—it determines when Claude activates this skill.

## Writing Effective SKILL.md

Apply **crafting-instructions** principles:

### Imperative Construction
Frame as direct commands:
- ✅ "Extract text with pdfplumber" / "Validate output with script"
- ❌ "Consider extracting..." / "You might want to validate..."

### Strategic Over Procedural
Specify goals and decision frameworks, not step-by-step procedures:
- ✅ "Create skill directory structure. Delete unused resource directories."
- ❌ "Step 1: mkdir skill-name. Step 2: mkdir scripts. Step 3: mkdir references..."

Provide steps only when order is non-obvious or fragile.

### Trust Base Behavior
Claude already knows:
- Basic programming patterns, common tools, file operations
- How to structure clear output, format markdown
- General best practices for code quality

Only specify skill-specific deviations or domain expertise Claude lacks.

### Positive Directive Framing
State what TO do, not what to avoid:
- ✅ "Write in imperative voice with direct instructions"
- ❌ "Don't use suggestive language or tentative phrasing"

Frame requirements positively because it's clearer and more actionable.

### Provide Context
Explain WHY for non-obvious requirements:
- ✅ "Keep SKILL.md under 500 lines to enable progressive loading—move detailed content to references/"
- ❌ "Keep SKILL.md under 500 lines"

Context helps Claude make good autonomous decisions in edge cases.

### Example Quality
Examples teach ALL patterns, including unintended ones. Ensure every aspect demonstrates desired behavior. Better to omit examples than include mixed signals.

**For comprehensive prompting guidance**, invoke **crafting-instructions** skill.

## Bundled Resources Patterns

### scripts/
Add when Claude would repeatedly write similar code:
- Validation logic (schema checking, format verification)
- Complex transformations (data normalization, format conversion)
- Deterministic operations requiring exact consistency

Scripts should have explicit error handling and clear variable names.

### references/
Add when:
- SKILL.md approaching 500 lines
- Detailed domain knowledge (API docs, schemas, specifications)
- Content applies to specific use cases only, not core workflow

Keep references one level deep (avoid file1 → file2 → file3 chains).

### assets/
Add for:
- Templates users will receive in output
- Files copied/referenced but not loaded into context
- Images, fonts, static resources

Assets save tokens—they're used but not read into context.

**Decision framework:** Will Claude repeatedly generate similar code? → scripts/. Is there extensive domain knowledge? → references/. Are there output templates? → assets/. Otherwise SKILL.md only.

## Progressive Disclosure

Skills load in three tiers:
1. **Metadata** (name + description): Always loaded for all skills
2. **SKILL.md body**: Loaded when skill activates
3. **Bundled resources**: Loaded as Claude reads them

Keep SKILL.md focused on core workflows (~500 lines max). Move detailed content to references/ for on-demand loading. This enables context-efficient skill ecosystems.

## Token Efficiency

Challenge each line: Does Claude really need this explanation? Can I assume Claude knows this? Does this justify its token cost?

Prefer concise patterns:
- Code examples over verbose explanations
- Decision frameworks over exhaustive lists
- Strategic goals over procedural steps

## Packaging & Delivery

Create ZIP archive:
```bash
cd /home/claude
zip -r /mnt/user-data/outputs/skill-name.zip skill-name/
```

Verify contents:
```bash
unzip -l /mnt/user-data/outputs/skill-name.zip
```

Show user the packaged structure:
```bash
tree skill-name/
# or
ls -lhR skill-name/
```

Provide download link:
```markdown
[Download skill-name.zip](computer:///mnt/user-data/outputs/skill-name.zip)
```

## Version Control (Optional)

For skills under active development, track changes:
```bash
cd /home/claude/skill-name
git init && git add . && git commit -m "Initial: skill structure"
```

After modifications:
```bash
git add . && git commit -m "Update: description of change"
```

See **versioning-skills** for advanced patterns (rollback, branching, comparison).

## Best Practices

**Structure:**
- Lead with clear overview of what skill enables
- Group related instructions together
- Use headings that describe goals, not procedures
- Reference other skills/resources when appropriate

**Instructions:**
- Write TO Claude (imperative commands) not ABOUT Claude (documentation)
- Assume Claude's intelligence—avoid over-explaining basics
- Show code examples for complex patterns
- Specify success criteria, let Claude determine approach

**Content:**
- Keep frequently-used guidance in SKILL.md
- Move detailed/specialized content to references/
- Include WHY context for non-obvious requirements
- Use consistent terminology throughout

**Resources:**
- Only add bundled resources that solve real problems
- Scripts should have error handling and clear outputs
- References should be focused and topic-specific
- Delete unused directories before packaging

**Testing:**
- Test with 3+ real scenarios (simple, complex, edge case)
- Verify skill activates on expected trigger patterns
- Confirm bundled resources are accessible and functional
- Iterate based on actual usage, not assumptions

## Quality Checklist

Before providing skill to user:

**Metadata:**
- [ ] Name: lowercase, hyphens, gerund form, max 64 chars
- [ ] Description: third person, includes WHAT + WHEN triggers, max 1024 chars, no XML

**Structure:**
- [ ] SKILL.md under 500 lines (move extras to references/)
- [ ] Unused directories deleted
- [ ] References one level deep (no long chains)

**Content:**
- [ ] Imperative voice throughout
- [ ] Positive directives (not negative restrictions)
- [ ] Strategic goals over procedural steps where possible
- [ ] Context provided for non-obvious requirements
- [ ] Examples perfectly demonstrate desired patterns
- [ ] Consistent terminology

**Resources:**
- [ ] Scripts solve actual problems (not punting to Claude)
- [ ] Scripts have error handling and clear outputs
- [ ] References are focused and topic-specific
- [ ] Assets are templates/files for output

**Testing:**
- [ ] Tested on 3+ real scenarios
- [ ] Activates on expected triggers
- [ ] Bundled resources accessible
- [ ] Package structure verified

## Advanced Topics

For complex skill patterns, see:
- **crafting-instructions** skill - Comprehensive prompting principles
- **versioning-skills** skill - Git-based development workflow
- [references/advanced-patterns.md](references/advanced-patterns.md) - Validation workflows, multi-stage patterns
- [references/optimization-techniques.md](references/optimization-techniques.md) - Token budget management
- [references/bundled-resources.md](references/bundled-resources.md) - Detailed resource patterns and examples
- [references/environment-reference.md](references/environment-reference.md) - Environment-specific patterns
