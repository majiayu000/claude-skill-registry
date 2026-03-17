---
name: skill-development
description: This skill should be used when the user asks to "create a skill", "write a skill", "edit a skill", "update a skill", "improve skill description", "add skill to plugin", "organize skill content", "create SKILL.md", "skill frontmatter", "skill structure", "progressive disclosure", or needs guidance on skill development, validation, or best practices for Claude Code plugins and personal skills.
version: 1.0.0
---

# Skill Development for Claude Code

## Overview

Skills are modular packages that extend Claude's capabilities by providing specialized knowledge, workflows, and resources. Think of them as "onboarding guides" that transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

**Key capabilities:**
- Create new skills with proper structure and frontmatter
- Edit existing skills to improve discovery and content
- Organize skills using progressive disclosure
- Validate skills against best practices
- Package skills for distribution

## When to Use This Skill

Use this skill when:
- **Creating** a new skill from scratch
- **Editing** an existing skill's description, instructions, or structure
- **Refactoring** skills for token optimization or progressive disclosure
- **Validating** skill structure and frontmatter
- **Organizing** skill content across SKILL.md, references/, examples/, scripts/

## Skill Anatomy

Every skill consists of a required SKILL.md and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown body (core instructions)
└── Bundled Resources (optional)
    ├── references/    - Detailed docs loaded as needed
    ├── examples/      - Working code examples
    └── scripts/       - Utility scripts
```

### Progressive Disclosure

Skills use three-level loading to manage context:

| Level | When Loaded | Size Limit | Content |
|-------|-------------|------------|---------|
| **Metadata** | Always (startup) | ~100 words | `name` and `description` from frontmatter |
| **Instructions** | When triggered | <5k words (~1,500-2,000 words ideal) | SKILL.md body |
| **Resources** | As needed | Unlimited | references/, examples/, scripts/ |

**Design principle:** Keep SKILL.md lean. Move detailed content to references/.

## Quick Start: Create or Edit?

Determine from context whether user wants to create or edit. If unclear, ask:

```json
{
  "questions": [
    {
      "question": "O que você quer fazer?",
      "header": "Ação",
      "multiSelect": false,
      "options": [
        { "label": "Criar nova skill", "description": "Começar do zero" },
        { "label": "Editar skill existente", "description": "Atualizar uma skill que já existe" }
      ]
    }
  ]
}
```

**Then follow the appropriate workflow:**
- **Creating:** See `references/creating-skills.md` for detailed creation process
- **Editing:** See `references/editing-skills.md` for detailed editing process

## Core Workflow (Creating)

### 1. Validate Understanding and Gather Requirements

**Principle: Don't ask what the user already said.** Extract from context first, then ask only what's missing.

**Always ask these two questions together:**

```json
{
  "questions": [
    {
      "question": "Entendi que você quer uma skill para [RESUMO]. Correto?",
      "header": "Confirmação",
      "multiSelect": false,
      "options": [
        { "label": "Sim, é isso!", "description": "Prosseguir com a criação" },
        { "label": "Quase, mas...", "description": "Vou explicar melhor" }
      ]
    },
    {
      "question": "Qual a complexidade da skill?",
      "header": "Estrutura",
      "multiSelect": false,
      "options": [
        { "label": "Simples", "description": "Só SKILL.md com instruções diretas" },
        { "label": "Média", "description": "SKILL.md + examples ou references" },
        { "label": "Completa", "description": "SKILL.md + references + examples + scripts" }
      ]
    }
  ]
}
```

**Conditional questions (only when needed):**
- **Interatividade**: Se complexidade >= Média e contexto sugere necessidade
- **Location**: Só se não for óbvio (padrão: `~/.claude/skills/`)

### 2. Design Skill Structure

Determine what goes where:

**SKILL.md (always loaded when triggered):**
- Core concepts and overview
- Essential procedures and workflows
- Quick reference tables
- Pointers to references/examples/scripts
- Most common use cases

**references/ (loaded as needed):**
- Detailed patterns and advanced techniques
- Comprehensive API documentation
- Migration guides
- Edge cases and troubleshooting
- Extensive examples and walkthroughs

**examples/ (working code):**
- Complete, runnable scripts
- Configuration files
- Template files
- Real-world usage examples

**scripts/ (utilities):**
- Validation tools
- Testing helpers
- Parsing utilities
- Automation scripts

### 3. Write Effective Frontmatter

**Required fields:**

```yaml
---
name: skill-name
description: This skill should be used when the user asks to "specific trigger 1", "specific trigger 2", or mentions specific terms. Brief explanation of what it does.
---
```

**Optional fields:**

```yaml
---
name: skill-name
description: Trigger-based description
user-invocable: true          # Show in slash command list (default: true for /skills/)
context: fork                 # Run in isolated context (default: inherit)
agent: swe                    # Specify agent type to execute skill (default: main)
language: portuguese          # Force response language (default: match user's language)
allowed-tools:                # YAML-style list (cleaner than comma-separated)
  - Bash
  - Read
  - Write
  - Edit
hooks:                        # Inline hooks scoped to this skill
  - type: PreToolUse
    once: true               # Run hook only once per session
  - type: PostToolUse
---
```

**When to use optional fields:**

- **`user-invocable: false`**: Hide skill from `/` command list (skill only triggers automatically via description)
- **`context: fork`**: Isolate skill execution from main conversation (useful for experimental or modifying skills)
- **`agent: type`**: Route skill to specialized agent (e.g., `swe` for code-heavy tasks)
- **`language`**: Force response in specific language regardless of conversation language
- **`allowed-tools`**: Restrict tools skill can use (security/scope control)
- **`hooks`**: Add PreToolUse/PostToolUse/Stop hooks scoped to skill execution only

**Naming rules:**
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- **Use gerund form** (verb+ing): `analyzing-code`, `writing-documentation`
- Be specific, not generic

**Description requirements:**
- Max 1024 characters
- **Third person:** "This skill should be used when..." (NOT "Use this skill when..." or "I help you...")
- Include BOTH what it does AND when to use it
- Use specific trigger words users would say
- Mention file types, operations, and context

**Good example:**
```yaml
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events (PreToolUse, PostToolUse, Stop). Provides comprehensive hooks API guidance.
```

**Bad examples:**
```yaml
description: Helps with hooks  # Vague, not third person
description: Use this skill for hook development  # Wrong person
description: I can help you create hooks  # First person
```

### 4. Write Clear Instructions

**Writing style:**
- Use **imperative/infinitive form** (verb-first instructions)
- NOT second person ("You should...")
- Objective, instructional language

**Correct:**
```
To create a hook, define the event type.
Configure the MCP server with authentication.
Validate settings before use.
```

**Incorrect:**
```
You should create a hook by defining the event type.
You need to configure the MCP server.
```

**Add interactive patterns when needed:**

If the skill helps create/configure something, include `AskUserQuestion` to gather requirements:

```markdown
## Instructions

### Step 1: Gather Requirements

Use AskUserQuestion to understand what to create:

\`\`\`json
{
  "questions": [
    {
      "question": "What should this do?",
      "header": "Purpose",
      "options": [...]
    }
  ]
}
\`\`\`

### Step 2: Create Based on Answers

Based on user's selections, create the appropriate structure...
```

**When to add:** Skills for creating commands, hooks, configurations, or anything requiring user decisions

**See:** `examples/interactive-workflow-example.md` for complete patterns

### 5. Configure Tool Permissions and Hooks

**Tool permissions with YAML lists (recommended):**

```yaml
---
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---
```

Cleaner and less error-prone than comma-separated: `allowed-tools: Bash, Read, Write`

**Bash wildcards for flexible permissions:**

```yaml
---
allowed-tools:
  - Bash(npm *)              # Allow any npm command
  - Bash(git * main)         # Allow git commands with 'main' anywhere
  - Bash(* install)          # Allow any command ending with 'install'
  - Read
  - Write
---
```

Use wildcards when skill needs variations of commands without listing each one.

**Inline hooks for skill-scoped automation:**

```yaml
---
hooks:
  - type: PreToolUse         # Validate before tool execution
    once: true               # Run only once (useful for setup)
  - type: PostToolUse        # React to tool results
  - type: Stop               # Clean up when skill completes
---
```

Hooks run only when this skill is active. Use for:
- Validation specific to skill operations
- Logging/tracking skill actions
- Setup/teardown within skill lifecycle

**See:** `../hook-development/` for complete hooks documentation

### 6. Organize Content

**Keep SKILL.md lean (1,500-2,000 words ideal, <5k max):**
- Move detailed content to `references/`
- Move examples to `examples/`
- Move utilities to `scripts/`
- Reference these resources clearly in SKILL.md

**Reference resources in SKILL.md:**
```markdown
## Additional Resources

### Reference Files
- **`references/patterns.md`** - Common patterns
- **`references/advanced.md`** - Advanced techniques

### Examples
- **`examples/basic-example.sh`** - Working example
```

### 7. Validate the Skill

**CRITICAL: Always run automated validation after creating or editing a skill.**

Execute the validation script:
```bash
bash ~/.claude/skills/skill-development/scripts/validate-skill.sh path/to/skill-name
```

The script automatically checks:
- ✓ SKILL.md exists with valid YAML frontmatter
- ✓ Required fields (name, description) present and valid
- ✓ Name format (lowercase, hyphens, max 64 chars)
- ✓ Description format (third person, <1024 chars, specific triggers)
- ✓ Line count (<500 lines, warns at >400)
- ✓ Referenced files exist
- ✓ No second person usage ("you should")

**If validation fails:**
1. Fix reported errors
2. Re-run validation script
3. Only proceed to testing after passing all checks

**Additional manual verification:**
- [ ] Clear instructions in imperative form
- [ ] Concrete examples provided
- [ ] Supporting files clearly referenced

### 8. Test the Skill

**For plugin skills:**
```bash
cc --plugin-dir /path/to/plugin
```

**For personal/project skills:**

Skills in `~/.claude/skills/` or `.claude/skills/` are **hot-reloaded automatically** - no restart needed!

1. Edit the skill file
2. Try trigger phrases that match the description
3. Verify skill activates automatically with updated content
4. Confirm instructions are clear and actionable

Note: Plugin skills still require plugin reload (remove and re-add marketplace)

**Debug if needed:**
```bash
claude --debug  # See skill loading and activation logs
```

## Common Patterns

### Minimal Skill (Simple knowledge)

```
skill-name/
└── SKILL.md
```

### Standard Skill (Recommended)

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

### Complete Skill (Complex domain)

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.sh
│   └── example2.json
└── scripts/
    └── validate.sh
```

## Plugin-Specific Considerations

### Skill Location

Plugin skills live in `plugin-name/skills/`:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
└── skills/
    └── my-skill/
        ├── SKILL.md
        ├── references/
        ├── examples/
        └── scripts/
```

### Auto-Discovery

Claude Code automatically:
- Scans `skills/` directory
- Finds subdirectories containing `SKILL.md`
- Loads skill metadata (name + description) always
- Loads SKILL.md body when skill triggers
- Loads references/examples when Claude determines needed

### Testing in Plugins

```bash
# Test with --plugin-dir
cc --plugin-dir /path/to/plugin

# Verify skill loads and triggers correctly
```

## Best Practices

**DO:**
- ✅ Use third-person in description ("This skill should be used when...")
- ✅ Include specific trigger phrases ("create X", "configure Y")
- ✅ Keep SKILL.md lean (1,500-2,000 words ideal)
- ✅ Use progressive disclosure (move details to references/)
- ✅ Write in imperative/infinitive form
- ✅ Reference supporting files clearly
- ✅ Provide working examples
- ✅ Use gerund naming (`analyzing-code` not `code-analyzer`)
- ✅ Use YAML lists for `allowed-tools` (cleaner than comma-separated)
- ✅ Use wildcards in Bash permissions when appropriate (`Bash(npm *)`)
- ✅ Set `user-invocable: false` for internal-only skills
- ✅ Use `context: fork` for experimental or high-risk operations
- ✅ Add inline hooks for skill-specific automation

**DON'T:**
- ❌ Use second person anywhere
- ❌ Have vague trigger conditions
- ❌ Put everything in SKILL.md (>3,000 words without references/)
- ❌ Leave resources unreferenced
- ❌ Include broken or incomplete examples
- ❌ Skip validation
- ❌ Make all skills user-invocable (some should be auto-trigger only)
- ❌ Over-restrict with comma-separated allowed-tools when wildcards work better

## Additional Resources

### Reference Files

For detailed processes and techniques, consult:

- **`references/creating-skills.md`** - Complete skill creation process with AskUserQuestion patterns
- **`references/editing-skills.md`** - Detailed editing workflows and refactoring patterns
- **`references/best-practices.md`** - Validation rules, common mistakes, optimization techniques

### Example Skills

Study these skills as templates:
- `../hook-development/` - Progressive disclosure, utilities, complete structure
- `../command-development/` - Clear critical concepts, good organization
- `../sync-claude-md/` - Well-structured analysis skill

## Implementation Workflow Summary

**To create a skill:**

1. **Understand use cases**: Ask questions, gather examples
2. **Plan resources**: Determine what scripts/references/examples needed
3. **Create structure**: `mkdir -p skills/skill-name/{references,examples,scripts}`
4. **Write SKILL.md**:
   - Frontmatter with third-person description and trigger phrases
   - Lean body (1,500-2,000 words) in imperative form
   - Reference supporting files
5. **Add resources**: Create references/, examples/, scripts/ as needed
6. **Validate**: Check description, writing style, organization
7. **Test**: Verify skill loads on expected triggers
8. **Iterate**: Improve based on usage

**To edit a skill:**

1. **Read current skill**: Analyze structure, content, line count
2. **Determine edit type**: Description, instructions, new section, or refactor
3. **Make changes**: Use Edit tool to update specific sections
4. **Validate**: Check all requirements still met
5. **Test**: Verify skill still activates correctly

Focus on strong trigger descriptions, progressive disclosure, and imperative writing style for effective skills that load when needed and provide targeted guidance.
