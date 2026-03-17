---
name: skill-builder
description: Create new Claude Code skills with proper SKILL.md format, frontmatter, and best practices. Use when building, scaffolding, or generating a new skill for Claude Code.
allowed-tools: Read, Write, Glob, Grep, Bash
metadata:
  author: mineflayer-bedrock
  version: "1.0"
---

# Claude Code Skill Builder

Create well-structured Claude Code skills that follow best practices and the Agent Skills specification.

## Quick Start

1. **Choose skill location**: Project (`.claude/skills/`) or Personal (`~/.claude/skills/`)
2. **Create directory**: `{location}/{skill-name}/`
3. **Generate SKILL.md** using template below
4. **Add supporting files** (scripts, references, assets) as needed
5. **Test the skill** by asking Claude to perform matching tasks

## SKILL.md Template

Create file at: `{location}/{skill-name}/SKILL.md`

```markdown
---
name: your-skill-name
description: Clear description of what this skill does (max 200 chars). Include trigger keywords users would naturally say.
allowed-tools: Read, Write, Glob, Grep, Bash
metadata:
  author: your-name
  version: "1.0"
---

# Your Skill Name

Brief overview of the skill's purpose.

## When to use

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## When NOT to use

- Exclusion condition 1
- Exclusion condition 2

## Instructions

Step-by-step guidance for completing the workflow:

1. **First step**: Description
2. **Second step**: Description
3. **Third step**: Description

## Examples

### Example 1: [Scenario Name]

**Input**: User says "..."

**Output**: Claude does...

## Common mistakes to avoid

- Mistake 1 and how to prevent it
- Mistake 2 and how to prevent it

## References

| Resource | Location |
|----------|----------|
| Documentation | `references/docs.md` |
| API Reference | `references/api.md` |
```

## Frontmatter Reference

### Required Fields

| Field | Constraints | Purpose |
|-------|-------------|---------|
| `name` | Max 64 chars, lowercase, hyphens only | Unique identifier (must match directory name) |
| `description` | Max 200 chars, non-empty | **Critical** - Claude uses this to decide when to invoke |

### Optional Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `license` | License type | `Apache-2.0`, `MIT` |
| `allowed-tools` | Pre-approved tools | `Read, Write, Glob, Grep, Bash` |
| `compatibility` | Environment requirements | `node >= 18, unix` |
| `metadata` | Custom key-value pairs | `author: name`, `version: "1.0"` |

## Directory Structure

```
skill-name/
├── SKILL.md           # Required - Core instructions (<500 lines)
├── scripts/           # Optional - Executable code (Python/Bash)
│   └── helper.py
├── references/        # Optional - Documentation loaded into context
│   ├── api.md
│   └── schema.md
└── assets/            # Optional - Templates, config files
    └── template.json
```

### File Purposes

| Folder | Purpose | Loading |
|--------|---------|---------|
| `SKILL.md` | Core instructions | Always (when skill activates) |
| `scripts/` | Repeatable automation | Executed on demand |
| `references/` | Extended documentation | Read into context on demand |
| `assets/` | Templates and resources | Used for output generation |

## Writing Effective Descriptions

The description is **critical** - it determines whether Claude activates your skill.

### Good Description Pattern

```
[What it does] + [When to use it with trigger keywords]
```

### Examples

**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs, forms, or document extraction.
```

**Good:**
```yaml
description: Generate TypeScript API clients from OpenAPI specs. Use when creating SDK, API wrapper, or client code from swagger/openapi files.
```

**Bad:**
```yaml
description: Helps with PDFs.
```

**Bad:**
```yaml
description: A utility for API work.
```

## Best Practices

### Keep SKILL.md Concise

- Target under 500 lines (~5,000 tokens)
- Move detailed documentation to `references/`
- Use tables and bullet points over prose

### Define Clear Boundaries

Always include both:
- **When to use**: Positive triggers
- **When NOT to use**: Negative boundaries to prevent over-activation

### Use Relative Paths

Reference files using paths relative to skill root:
- `scripts/extract.py`
- `references/api-docs.md`
- `assets/template.html`

### Security

- Never hardcode secrets, API keys, or passwords
- Audit scripts from untrusted sources
- Use environment variables for sensitive config

## Skill vs MCP Server

| Feature | Skills | MCP Servers |
|---------|--------|-------------|
| Purpose | **How** to do something | **Access** to something |
| Contains | Instructions, templates | Tools, resources |
| Loading | On-demand (progressive) | Upfront |
| Best for | Workflows, standards | Data access, APIs |

A skill can orchestrate multiple MCP servers. Use skills for workflow logic and MCP for connectivity.

## Testing Checklist

1. [ ] Directory name matches `name` in frontmatter
2. [ ] Description includes trigger keywords
3. [ ] SKILL.md under 500 lines
4. [ ] All file references use relative paths
5. [ ] When/When NOT sections are clear
6. [ ] Examples demonstrate expected behavior
7. [ ] Restart Claude Code to load new skill
8. [ ] Test with natural language matching description

## Example: Complete Skill

### code-review Skill

```markdown
---
name: code-review
description: Review code for bugs, security issues, and best practices. Use when reviewing PRs, checking code quality, or auditing implementations.
allowed-tools: Read, Glob, Grep
metadata:
  author: team
  version: "1.0"
---

# Code Review

Systematic code review following team standards.

## When to use

- Reviewing pull requests
- Checking code before commit
- Auditing security-sensitive code
- Evaluating code quality

## When NOT to use

- Simple typo fixes (just fix them)
- Understanding code (use exploration instead)
- Writing new code (use appropriate coding skill)

## Review Checklist

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention

### Code Quality
- [ ] Functions under 50 lines
- [ ] Clear naming conventions
- [ ] Error handling present
- [ ] No dead code

### Testing
- [ ] Unit tests for new functions
- [ ] Edge cases covered
- [ ] Integration tests if needed

## Output Format

Provide findings as:

| Severity | File:Line | Issue | Suggestion |
|----------|-----------|-------|------------|
| High | src/auth.ts:42 | Hardcoded API key | Use env variable |
| Medium | src/user.ts:15 | Missing null check | Add optional chaining |
```

## Documentation Links

| Resource | URL |
|----------|-----|
| Skills Overview | https://code.claude.com/docs/en/skills |
| Creating Skills | https://support.claude.com/en/articles/12512198 |
| Agent Skills Spec | https://github.com/anthropics/skills/blob/main/agent_skills_spec.md |
| Template Skill | https://github.com/anthropics/skills/tree/main/template-skill |
| Best Practices | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills |

## Common Patterns

### Workflow Skill

For multi-step processes:
```markdown
## Workflow

1. **Gather**: Collect required information
2. **Validate**: Check prerequisites
3. **Execute**: Perform main action
4. **Verify**: Confirm success
```

### Template Skill

For generating files:
```markdown
## Template Usage

1. Copy template from `assets/template.ext`
2. Replace placeholders: `{{name}}`, `{{date}}`
3. Save to destination
```

### Integration Skill

For connecting services:
```markdown
## Integration Steps

1. Check MCP server is connected
2. Authenticate if needed
3. Call required endpoints
4. Transform response
```
