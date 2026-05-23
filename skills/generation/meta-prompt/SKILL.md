---
name: "Meta Prompt"
description: "Generate prompt variations from templates. Use when creating new commands, skills, or workflows."
tools: Read, Grep, Glob, Write
model: inherit
---

# Skill: Meta Prompt

Create new prompts based on existing templates and patterns. This is a meta-skill - a tool that generates tools.

## When to Use

- Creating new slash command
- Creating new skill variation
- Creating expert workflow variation
- Adapting existing prompt for new domain

## Workflow

### 1. Identify Template

Find closest existing prompt:

```bash
# Search for similar prompts
Glob: .claude/commands/*.md
Glob: .claude/skills/*/SKILL.md
Glob: .claude/experts/*/question.md
Glob: .claude/experts/*/self-improve.md

# Read template
Read: [closest-match]
```

### 2. Define Variations

Ask user:
- What should be different?
- What domain/technology?
- What tools needed?
- What workflow changes?

### 3. Generate New Prompt

Copy structure, modify:

**YAML Frontmatter:**
```yaml
---
name: "{New Name}"
description: "{What it does}"
tools: [adjust tool list]
model: inherit
argument-hint: [if command]
---
```

**Content:**
- Keep workflow structure
- Replace domain-specific terms
- Adjust file patterns (Glob/Grep)
- Customize validation steps
- Update examples

### 4. Validate

Check:
- [ ] YAML syntax valid
- [ ] Tool references correct
- [ ] File paths appropriate
- [ ] Examples make sense

### 5. Save & Test

```bash
# Save to appropriate location
Write: .claude/commands/{name}.md  # for commands
Write: .claude/skills/{name}/SKILL.md  # for skills
Write: .claude/experts/{name}/{type}.md  # for expert workflows

# Test execution
# Run new prompt with test input
```

## Example: Create "question-with-diagram"

```markdown
# User: "Create variation of question.md that includes mermaid diagrams"

# 1. Template
Read: .claude/experts/convex-expert/question.md

# 2. Variations
- Add mermaid diagram generation step
- Include visual flow in answers
- Keep rest of workflow same

# 3. Generate
Copy question.md structure
Add step 4.5: Generate Diagram
Update output format to include diagram section

# 4. Validate
YAML valid ✓
Tools sufficient ✓
Examples updated ✓

# 5. Save
Write: .claude/experts/convex-expert/question-with-diagram.md
```

## Output Format

After creating prompt:

```markdown
## Created: {Name}

**Type:** {command/skill/expert-workflow}
**Location:** {file-path}
**Based on:** {template-used}

**Modifications:**
- {change 1}
- {change 2}

**Usage:**
{how to use the new prompt}

**Test:**
{suggested test command}
```

## Tips

- Start with closest template
- Make minimal necessary changes
- Keep proven patterns
- Test with real inputs
- Iterate based on results
