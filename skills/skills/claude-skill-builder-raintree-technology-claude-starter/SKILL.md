---
name: claude-skill-builder
description: Interactive skill creator for Claude Code. Triggers when user mentions creating skills, building skills, skill templates, skill frontmatter, allowed-tools, or wants to scaffold a new skill.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Claude Code Skill Builder

## Purpose

Guide users through creating well-structured Claude Code skills with proper frontmatter, clear descriptions, and effective trigger keywords. Auto-invokes when users want to create or modify skills.

## When to Use

Auto-invoke when users mention:
- **Creating skills** - "create a skill", "make a skill", "new skill"
- **Skill structure** - "skill template", "skill format", "skill frontmatter"
- **Trigger keywords** - "skill description", "when to invoke", "trigger words"
- **Skill configuration** - "allowed-tools", "skill permissions", "skill model"
- **Skill organization** - "skill directory", "skill files", "multi-file skill"

## Knowledge Base

- Official docs: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_skills.md`
- Project guide: `.claude/docs/creating-components.md`
- Examples in repository: `.claude/skills/`

## Process

### 1. Gather Requirements

Ask the user:

```
Let me help you create a Claude Code skill! I need a few details:

1. **Skill name** (lowercase-with-hyphens):
   Example: nextjs-expert, pdf-processor, git-commit-helper

2. **What does this skill do?**
   Describe the capability in 1-2 sentences.

3. **When should this skill activate?**
   List keywords users will mention: Next.js, React, API, authentication, etc.

4. **What tools will it need?**
   - Read (read files)
   - Write (create new files)
   - Edit (modify existing files)
   - Grep (search file contents)
   - Glob (find files by pattern)
   - Bash (run shell commands)

5. **Scope:**
   - Personal (`~/.claude/skills/`) - just for you
   - Project (`.claude/skills/`) - shared with team

6. **Category/subdirectory?**
   Example: data, api, frontend, backend, testing
```

### 2. Validate Input

Check the skill name:
- Must be lowercase
- Use hyphens (not underscores or spaces)
- Maximum 64 characters
- Descriptive and clear

Validate description:
- Maximum 1024 characters
- Must include trigger keywords
- Should explain both WHAT and WHEN

### 3. Create Skill Structure

Determine file structure:

**Single file skill (simple):**
```
skill-name/
└── SKILL.md
```

**Multi-file skill (complex):**
```
skill-name/
├── SKILL.md (overview and main instructions)
├── REFERENCE.md (detailed API reference)
├── EXAMPLES.md (code examples)
├── scripts/
│   └── helper.py (utility scripts)
└── templates/
    └── template.txt (file templates)
```

### 4. Generate SKILL.md

Create frontmatter with:
- `name`: Skill identifier (from user input)
- `description`: Clear description with ALL trigger keywords
- `allowed-tools`: Only tools actually needed
- `model`: sonnet (default), opus (complex), or haiku (fast)

Template structure:
```markdown
---
name: skill-identifier
description: What this does and when to use it. Include keywords: keyword1, keyword2, keyword3
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Skill Name

## Purpose
[Clear explanation of what this skill provides]

## When to Use
- Trigger condition 1 (specific keywords)
- Trigger condition 2 (user scenarios)
- Trigger condition 3 (related topics)

## Process

### 1. Analyze the Request
[How to understand what the user wants]

### 2. Gather Context
Use tools to collect information:
- Read relevant files
- Search for patterns
- Find related code

### 3. Provide Solution
[Step-by-step approach to solving the problem]

### 4. Verify Result
[How to confirm the solution works]

## Examples

### Example 1: Basic Usage
**User request:** [Example request]
**Process:** [How skill handles it]
**Output:** [What user sees]

### Example 2: Advanced Usage
**User request:** [Complex scenario]
**Process:** [Multi-step handling]
**Output:** [Comprehensive result]

## Best Practices
- Practice 1: [Specific guidance]
- Practice 2: [Common pattern]
- Practice 3: [Expert tip]

## Common Pitfalls
- ❌ **Pitfall 1**: [What to avoid and why]
  ✅ **Instead**: [Better approach]

- ❌ **Pitfall 2**: [Common mistake]
  ✅ **Instead**: [Correct way]

## Resources
- [Official Documentation](url)
- [Related Guide](path/to/guide.md)
```

### 5. Create Supporting Files (if needed)

For complex skills, offer to create:

**REFERENCE.md:**
```markdown
# Detailed Reference

## API Documentation
[Comprehensive API details]

## Configuration Options
[All available settings]

## Advanced Features
[Expert-level capabilities]
```

**EXAMPLES.md:**
```markdown
# Examples

## Example 1: [Scenario]
[Detailed code example with explanation]

## Example 2: [Scenario]
[Another complete example]
```

### 6. Test and Validate

After creating the skill:

```bash
# Verify file exists
ls -la path/to/skill/SKILL.md

# Check file structure
cat path/to/skill/SKILL.md | head -20

# Validate YAML frontmatter
cat path/to/skill/SKILL.md | sed -n '1,/^---$/p'
```

Provide testing instructions:
```
To test your skill:
1. Restart Claude Code or start a new session
2. Mention one of your trigger keywords
3. Watch for skill activation
4. Ask: "What skills are available?" to verify it's loaded
```

### 7. Provide Next Steps

Give the user:
- Path to the created skill file
- How to test it
- How to modify it
- How to share it (if project skill)
- How to add more supporting files

## Skill Size Guidelines

Warn if skill is getting large:
- ✅ **Good:** < 600 lines
- ⚠️ **Warning:** 600-900 lines (consider splitting)
- ❌ **Too large:** > 900 lines (must split or refactor)

**If too large, suggest:**
- Split into multiple focused skills
- Move detailed docs to separate reference files
- Extract examples to EXAMPLES.md
- Link to external documentation

## Frontmatter Best Practices

### Description Field

✅ **Good descriptions:**
```yaml
description: Expert in Next.js App Router, server components, server actions, and React Server Components. Use when user mentions Next.js, RSC, App Router, or server-side React patterns.
```

❌ **Bad descriptions:**
```yaml
description: Helps with Next.js
```

### Allowed Tools

Only request tools you actually use:
- Don't request all tools "just in case"
- Be specific about needs
- Consider security implications

**Examples:**
```yaml
# Read-only skill
allowed-tools: Read, Grep, Glob

# Code generator
allowed-tools: Read, Write, Grep, Glob

# Full development workflow
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
```

### Model Selection

Choose based on complexity:
- `haiku`: Fast, simple tasks, quick responses
- `sonnet`: Balanced, most skills (recommended)
- `opus`: Complex reasoning, advanced tasks

## Example Skills to Reference

Point users to examples in the repository:
- `.claude/skills/data/toon-formatter/skill.md` - Data processing
- `.claude/skills/ai/anthropic/skill.md` - API expertise
- `.claude/skills/ai/claude-code/skill.md` - Tool knowledge

## Common Skill Types

### API/Framework Expert
**Purpose:** Deep knowledge of a specific framework or API
**Triggers:** Framework name, features, patterns
**Tools:** Read, Grep, Glob
**Example:** Next.js expert, FastAPI expert, React expert

### Code Generator
**Purpose:** Create boilerplate or scaffolding
**Triggers:** "generate", "create", "scaffold", "template"
**Tools:** Write, Read, Grep, Glob
**Example:** Component generator, test file creator

### Code Analyzer
**Purpose:** Review and analyze existing code
**Triggers:** "review", "analyze", "check", "audit"
**Tools:** Read, Grep, Glob
**Example:** Security auditor, performance analyzer

### Development Workflow
**Purpose:** Automate common dev tasks
**Triggers:** Workflow steps, automation keywords
**Tools:** Read, Write, Edit, Bash
**Example:** Deployment helper, commit message generator

### Data Processor
**Purpose:** Transform or analyze data
**Triggers:** Data formats, transformation keywords
**Tools:** Read, Write, Edit, Grep
**Example:** TOON formatter, JSON converter

## Troubleshooting

### Skill Not Activating

**Check:**
1. Description has specific trigger keywords
2. File is named `SKILL.md` (case-sensitive)
3. File is in correct location:
   - Personal: `~/.claude/skills/category/skill-name/SKILL.md`
   - Project: `.claude/skills/category/skill-name/SKILL.md`
4. YAML frontmatter is valid (no tabs, proper indentation)
5. Restart Claude Code to load new skills

**Debug with:**
```bash
# Verify location
ls ~/.claude/skills/*/SKILL.md
ls .claude/skills/*/SKILL.md

# Check YAML syntax
head -20 path/to/SKILL.md

# Run in debug mode
claude --debug
```

### Skill Conflicts

If multiple skills have similar triggers:
- Make descriptions more specific
- Use distinct keywords
- Reference specific use cases
- Consider combining into one skill

### File Not Found Errors

Check that referenced files exist:
```bash
# From SKILL.md, check references like [reference.md](reference.md)
ls path/to/skill/reference.md
```

## Best Practices Summary

### DO:
✅ Include specific trigger keywords in description
✅ Keep skills focused on one capability
✅ Provide clear examples in the skill
✅ Use progressive disclosure (reference external files)
✅ Test the skill before sharing
✅ Document version changes

### DON'T:
❌ Make descriptions too vague
❌ Try to handle everything in one skill
❌ Request unnecessary tools
❌ Skip examples
❌ Forget to test activation triggers
❌ Go over 900 lines without splitting

## Resources

- **Official Skill Docs:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_skills.md`
- **Anthropic Skill Guide:** https://docs.claude.com/en/docs/agents-and-tools/agent-skills/
- **Project Component Guide:** `.claude/docs/creating-components.md`
- **Skill Examples:** `.claude/skills/` directory
