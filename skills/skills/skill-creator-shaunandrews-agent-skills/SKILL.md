# Skill Creator Skill

Use this skill when creating a new agent skill. Skills provide specialized instructions for specific tasks.

## When to Use

- Creating a new skill for the agent-skills repo
- User asks to "create a skill" or "add a new skill"
- Documenting a repeatable workflow as a skill

## Skill Location

All skills live in: `~/Developer/Projects/agent-skills/skills/{skill-name}/`

Use kebab-case for skill names (e.g., `wordpress-mockups`, `project-setup`).

## Skill Structure

Minimal skill:
```
{skill-name}/
└── SKILL.md              # Required: main skill file
```

Complex skill with assets:
```
{skill-name}/
├── SKILL.md              # Required: main skill file
├── docs/                 # Optional: detailed documentation
│   └── {topic}.md
├── templates/            # Optional: file templates
│   └── {template-file}
├── examples/             # Optional: example files
│   └── {example-file}
└── assets/               # Optional: images, icons, etc.
    └── {asset-file}
```

## SKILL.md Template

```markdown
# {Skill Name} Skill

{One-line description of what this skill does}

## When to Use

- {Trigger condition 1}
- {Trigger condition 2}
- {Trigger condition 3}

## Prerequisites

{Tools, CLIs, access, or setup required — or "None" if self-contained}

## Workflow

### Step 1: {First Step}

{Instructions}

### Step 2: {Second Step}

{Instructions}

{Continue with more steps as needed}

## Commands Reference

{If the skill involves CLI tools, list key commands}

```bash
# Example command
command --flag value
```

## Templates

{If the skill includes templates, document them here}

## Examples

{Show example usage or link to examples/ folder}

## Troubleshooting

{Common issues and solutions}

## Related Skills

- {Link to related skills if applicable}
```

## Writing Good Skills

### Be Specific
- Describe exact conditions when to use the skill
- Include concrete examples, not abstract principles

### Be Procedural
- Break down workflows into clear steps
- Use numbered lists for sequences
- Use code blocks for commands and file contents

### Be Complete
- Include all necessary context
- Don't assume the agent remembers prior conversations
- Reference file paths explicitly

### Be Practical
- Focus on what the agent needs to DO, not background theory
- Include templates and examples
- Anticipate common variations

## Creation Procedure

1. **Identify the skill need**
   - What task keeps coming up?
   - What workflow should be standardized?

2. **Create skill directory**
   ```bash
   mkdir -p ~/Developer/Projects/agent-skills/skills/{skill-name}
   ```

3. **Write SKILL.md**
   - Use template above
   - Be thorough — this is the agent's only reference

4. **Add supporting files** (if needed)
   - Templates in `templates/`
   - Examples in `examples/`
   - Documentation in `docs/`

5. **Test the skill**
   - Symlink to workspace: 
     ```bash
     ln -s ~/Developer/Projects/agent-skills/skills/{skill-name} ~/.openclaw/workspace/skills/{skill-name}
     ```
   - Try using it in a conversation
   - Refine based on results

6. **Commit to agent-skills repo**
   ```bash
   cd ~/Developer/Projects/agent-skills
   git add skills/{skill-name}
   git commit -m "Add {skill-name} skill"
   git push
   ```

## Symlinking Skills

To make a skill available to the agent:

```bash
# Create symlink
ln -s ~/Developer/Projects/agent-skills/skills/{skill-name} ~/.openclaw/workspace/skills/{skill-name}

# Verify
ls -la ~/.openclaw/workspace/skills/{skill-name}
```

To remove a skill:
```bash
rm ~/.openclaw/workspace/skills/{skill-name}  # Removes symlink only, not source
```

## Skill Naming Conventions

| Pattern | Use For | Examples |
|---------|---------|----------|
| `{tool}-{action}` | Tool-specific skills | `gh-issues`, `wp-deploy` |
| `{domain}-{topic}` | Domain skills | `wordpress-blocks`, `design-mockups` |
| `{verb}-{noun}` | Action skills | `project-setup`, `skill-creator` |

## Quality Checklist

Before committing a new skill:

- [ ] SKILL.md has clear "When to Use" section
- [ ] All file paths are explicit (no assumptions)
- [ ] Commands include expected output or success criteria
- [ ] Templates are complete and copy-pasteable
- [ ] Tested with actual usage
- [ ] Committed to agent-skills repo

## Existing Skills Reference

Check existing skills for patterns:
```bash
ls ~/.openclaw/workspace/skills/
```

Read a skill to understand structure:
```bash
cat ~/.openclaw/workspace/skills/{skill-name}/SKILL.md
```
