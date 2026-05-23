---
name: skill-authoring-majo
description: >
  Create new Agent Skills from learned patterns and workflows. Use when you have
  developed a repeatable workflow, coding pattern, or expertise that should be
  reusable across projects and doesn't fit in AGENTS.md. Covers SKILL.md format,
  naming conventions, progressive disclosure, testing, and skill structure best
  practices.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# Skill Authoring Guide (Mark)

Create reusable Agent Skills from learned patterns and workflows.

## Goal

Transform repeatable workflows, coding patterns, and domain expertise into
portable Agent Skills that can be discovered and used across multiple projects.
Ensure skills follow the Agent Skills specification with clear activation
triggers, progressive disclosure, and effective testing.

## When to Use This Skill

**Use this skill when:**
- You've developed a repeatable workflow (e.g., "how I set up X")
- You have domain expertise that applies across projects
- You find yourself repeating the same instructions to the agent
- A pattern doesn't fit well in AGENTS.md (too large, too specific)
- You want progressive disclosure (load detailed instructions only when needed)
- Creating skills for technologies, tools, or processes you use frequently

**Do NOT use this skill when:**
- It's project-specific knowledge that only applies to one codebase (use AGENTS.md)
- It's a one-time task that won't be repeated
- It's already covered by existing skills in your collection
- The workflow is still evolving and not yet stabilized
- The instructions are purely educational/documentation rather than actionable

## Process

### Step 1: Identify the Pattern

Determine if the workflow is skill-worthy:
- Is this repeatable across multiple projects?
- Does it not fit well in AGENTS.md?
- Will you use this pattern again?
- Is it actionable (not just documentation)?

### Step 2: Choose a Clear Name

Follow the naming convention: `{topic}-majo`

- Use kebab-case (lowercase with hyphens)
- Action-oriented when possible (e.g., `create-plan`, `run-tests`)
- Be specific: avoid multi-purpose names
- Match the directory name exactly

Examples:
- `python-majo` — Python development standards
- `task-planning-majo` — Task planning workflows
- `setting-up-public-domain-repos-majo` — Repository setup

### Step 3: Draft the SKILL.md

Start with the template structure:
1. YAML frontmatter with name, description, license, metadata
2. Goal section (what this skill achieves)
3. When to use / When not to use sections
4. Process section (step-by-step instructions)
5. Constraints and guardrails
6. Examples and cross-references

### Step 4: Write an Effective Description

The description is the PRIMARY TRIGGER. Include:
- What the skill does (specific actions)
- When to use it (triggering phrases)
- Domain terms and keywords
- Max 1024 characters

**Good**: "Python development with UV, basedpyright, ruff. Use when writing Python code or setting up Python projects."

**Bad**: "Helps with code" (too vague, triggers unpredictably)

### Step 5: Structure for Progressive Disclosure

Organize content into three levels:

**Level 1: Discovery (~100 tokens)**
- Only YAML frontmatter loaded at startup
- `name` + `description` must clearly signal when to activate

**Level 2: Activation (<5000 tokens recommended)**
- Full SKILL.md body loaded when matched
- Keep concise; move heavy content to references/

**Level 3: Deep Dive (on demand)**
- references/ for detailed guides
- scripts/ for executable code
- assets/ for templates and data

### Step 6: Test the Skill

**Test 1: Explicit Invocation** - Use direct skill calls, verify flow makes sense

**Test 2: Implicit Invocation (Critical)** - Test WITHOUT mentioning the skill name

**Test 3: Edge Cases** - Test ambiguous requests, verify "Do NOT use" criteria

### Step 7: Review and Refine

Before finalizing:
- [ ] Name follows `{topic}-majo` convention
- [ ] Description explains what AND when to use
- [ ] Includes "When to use" and "Do NOT use" sections
- [ ] Process is step-by-step and actionable
- [ ] Examples are provided
- [ ] Cross-references to related skills
- [ ] Under 5000 tokens (or split into references/)
- [ ] Tested with both explicit and implicit invocation

### Step 8: Place in Skills Directory

```
majo-skills/
└── your-new-skill/           # Directory name matches skill name
    ├── SKILL.md              # Required
    ├── references/           # Optional: detailed guides
    │   └── detailed-guide.md
    └── scripts/              # Optional: executable code
        └── helper.sh
```

### Step 9: Update AGENTS.md

Document the new skill in the project's AGENTS.md:

```markdown
## Available Skills

- `skill-authoring-majo` — Create new Agent Skills from patterns
- `your-new-skill` — [Brief description]
```

## Skill vs AGENTS.md

| Use Case | AGENTS.md | Skill |
|----------|-----------|-------|
| Project-specific knowledge | ✅ | ❌ |
| Cross-project patterns | ❌ | ✅ |
| Large reference material | ❌ | ✅ |
| Progressive disclosure | ❌ | ✅ |
| Current task tracking | ✅ | ❌ |
| Reusable workflows | ❌ | ✅ |

## SKILL.md Format

### SKILL.md Template

Use this template for consistent skill structure:

```yaml
---
name: <kebab-case-name>              # 1-64 chars, lowercase alphanumeric + hyphens
description: >                       # 1-1024 chars, THE PRIMARY TRIGGER
  <One or two sentences: what this skill does and when to use it.
   Include typical user phrases and domain terms. Be specific.>
license: Unlicense OR 0BSD           # Your license
metadata:                            # Optional but recommended
  author: Mark Joshwel <mark@joshwel.co>
  version: "1.0.0"
  tags: [<tag1>, <tag2>]             # For organization and discovery
---

# Skill Title

## Goal

<What this skill achieves, in 2-4 sentences. Focus on outcomes.>

## When to Use This Skill

**Use this skill when:**
- <Condition 1: specific trigger>
- <Condition 2: specific trigger>
- <Condition 3: specific trigger>

**Do NOT use this skill when:**
- <Anti-condition 1: when to avoid>
- <Anti-condition 2: when to avoid>

## Process

1. <Step 1: concrete action>
2. <Step 2: concrete action>
3. <Step 3: concrete action>
4. <Verification / validation step>

## Constraints

- <Constraint 1: rule or guardrail>
- <Constraint 2: rule or guardrail>
- <Safety / verification rule>

## Examples

**Example 1: [Scenario]**
```python
# Code example showing the pattern
```

**Example 2: [Scenario]**
```bash
# Command example
```

## References

- If needed, read `references/<file>.md` for <purpose>.
- See `scripts/<script>.sh` for <purpose>.

## Integration

This skill works alongside:
- `other-skill` — For <purpose>
- `dev-standards-majo` — For SPDX identifiers and universal principles
```

### Naming Conventions

**Format**: `{topic}-majo` for personal skills

**Examples**:
- `python-majo` - Python development
- `task-planning-majo` - Planning workflows
- `running-windows-commands-majo` - Windows-specific commands

**Good names**:
- Short and descriptive
- Lowercase with hyphens
- Indicates purpose clearly

## Directory Structure

### Simple Skill (text only)

```
skill-name/
└── SKILL.md
```

### Complex Skill (with references)

```
skill-name/
├── SKILL.md
├── references/
│   ├── detailed-guide.md
│   └── api-reference.md
└── examples/
    └── example.py
```

### Advanced Skill (with scripts)

```
skill-name/
├── SKILL.md
├── scripts/
│   └── setup.sh
├── references/
│   └── patterns.md
└── assets/
    └── template.json
```

## Progressive Disclosure

The key principle: load information only when needed.

### Level 1: Discovery (Always Loaded)

Just the YAML frontmatter:
- `name` - skill identifier
- `description` - when to activate

**~100 tokens** - loaded at startup

### Level 2: Activation (Loaded When Matched)

Full SKILL.md body:
- Instructions
- Examples
- Workflows

**< 5000 tokens** - loaded when task matches

### Level 3: Deep Dive (Loaded on Demand)

References and assets:
- Detailed guides
- Code templates
- Large examples

**Loaded only when explicitly needed**

## Constraints

- **Keep descriptions specific** — Vague descriptions cause unpredictable triggering
- **Avoid mega-skills** — Prefer focused, composable skills
- **Never exceed 5000 tokens** — Move large content to references/
- **Use kebab-case naming** — Directory name must match `name` field
- **Include SPDX identifiers** — Per `dev-standards-majo`
- **Write actionable instructions** — Tell HOW, not WHAT
- **Test implicit invocation** — Before shipping
- **Version significant changes** — Update metadata version

## Writing Effective Skills

**1. Clear Activation Triggers**: Include specific phrases like "Use when working with Windows paths" not "A skill about Windows"

**2. Action-Oriented Instructions** - Show commands, not tool history. Good: "Run `git status`". Bad: "Git is a VCS created by..."

**3. Include Decision Trees** - Use ASCII diagrams: `User task → Start work → Check status`

**4. Show Examples** - Include concrete code with SPDX headers

**5. Cross-Reference Other Skills** - List related skills that work together

## Common Skill Patterns

Five common skill patterns for inspiration:

1. **Tool Wrapper** - Wraps a CLI tool with usage guidance (e.g., `sheets-cli-majo`)
2. **Language Standards** - Coding standards for a specific language (e.g., `python-majo`)
3. **Platform-Specific** - Platform-specific workarounds (e.g., `running-windows-commands-majo`)
4. **Workflow/Process** - Repeatable workflows (e.g., `task-planning-majo`)
5. **Setup/Configuration** - Project initialization (e.g., `setting-up-public-domain-repos-majo`)

For detailed examples and patterns, see [references/DETAILED_EXAMPLES.md](references/DETAILED_EXAMPLES.md).

## Testing Skills (Critical)

Systematic testing ensures skills trigger correctly.

**Test 1: Explicit Invocation** - Use slash commands or direct references to debug

**Test 2: Implicit Invocation (Most Critical)** - Test WITHOUT mentioning the skill name. Example: "I keep explaining the same Python setup steps" should trigger the skill

**Test 3: Edge Cases** - Test ambiguous requests, verify no overlap with other skills

**Test 4: Version Control** - Put skills under version control, review changes

## Examples from Mark's Skills

Three complexity levels for reference:

- **Minimal** (`js-bun-majo`) - Single sentence description, one-line instruction
- **Medium** (`task-planning-majo`) - Clear activation, workflow, decision tree
- **Complex** (`python-majo`) - Multiple sections, references/, tool guidance

For complete examples with source, see [references/DETAILED_EXAMPLES.md](references/DETAILED_EXAMPLES.md).

## Anti-Patterns to Avoid

Eight anti-patterns to avoid when authoring skills:

1. **Too Broad/Vague Description** - Causes unpredictable triggering
2. **Too Narrow/One-Off** - Not reusable across projects
3. **Documentation Instead of Instructions** - Skills should be actionable
4. **Missing "Do NOT Use" Criteria** - Causes inappropriate activation
5. **Overlapping Skills** - Model picks unpredictably when similar
6. **No Examples** - Pure text without concrete code
7. **Missing Activation Triggers** - Description doesn't explain when to use
8. **Untested Skills** - Always test implicit invocation before shipping

For detailed explanations of each anti-pattern, see [references/DETAILED_EXAMPLES.md](references/DETAILED_EXAMPLES.md).

## Integration with Existing Skills

### Skill Dependencies

If skill B extends skill A, mention it:

```markdown
## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded.
```

### Skill Conflicts

If two skills shouldn't be used together, document it:

```markdown
## Note

Do not use alongside `other-skill` - they provide conflicting guidance.
```

## Resources

- Agent Skills specification: https://agentskills.io/specification.md
- Example skills: https://github.com/anthropics/skills
- Skill validation: Use `skills-ref validate ./skill-name`

## Quick Reference

| Element | Required | Notes |
|---------|----------|-------|
| YAML frontmatter | Yes | name, description required |
| name | Yes | 1-64 chars, lowercase, hyphens |
| description | Yes | 1-1024 chars, explains when to use |
| license | Recommended | Unlicense OR 0BSD |
| metadata | Optional | author, version, etc. |
| Body content | Yes | Instructions, examples |
| references/ | Optional | For large content |
| scripts/ | Optional | Executable code |
| assets/ | Optional | Templates, data |

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- Universal code principles
- Documentation policies

Works alongside:
- `writing-docs-majo` — For writing skill documentation
- `git-majo` — For committing new skills
- `task-planning-majo` — For planning complex skill creation
