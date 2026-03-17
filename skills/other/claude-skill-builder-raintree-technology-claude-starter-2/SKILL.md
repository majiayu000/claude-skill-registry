---
name: claude-skill-builder
description: Interactive skill creator for Claude Code and Agent Skills ecosystem. Build SKILL.md files with proper frontmatter, triggers, and structure. Triggers on creating skills, building skills, skill templates, skill frontmatter, allowed-tools, npx add-skill, agent skills.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "1.0"
---

# Claude Code Skill Builder

Create well-structured skills compatible with Claude Code and the Agent Skills specification (used by `npx add-skill`).

## When to Use

- User wants to create a new skill
- User needs help with skill structure or frontmatter
- User asks about trigger keywords or descriptions
- User wants to publish skills for `npx add-skill`

## Skill Structure

### Minimal Skill (Single File)

```
skill-name/
└── SKILL.md
```

### Full Skill (With References)

```
skill-name/
├── SKILL.md           # Main skill file (required)
├── references/        # Additional documentation
│   └── api-guide.md
├── scripts/           # Helper scripts
│   └── helper.py
└── assets/            # Templates, examples
    └── template.txt
```

## SKILL.md Template

```markdown
---
name: my-skill-name
description: Clear description of what this skill does. Include trigger keywords like keyword1, keyword2, keyword3 so the agent knows when to activate this skill.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: your-name
  version: "1.0"
---

# Skill Title

## Purpose
Brief explanation of what this skill provides.

## When to Use
- Scenario 1 (include keywords)
- Scenario 2 (include keywords)
- Scenario 3 (include keywords)

## Process

### 1. Understand the Request
How to analyze what the user needs.

### 2. Gather Context
What information to collect.

### 3. Provide Solution
Step-by-step approach.

## Examples

### Example 1: Basic Usage
**Request:** "Help me with X"
**Response:** [How skill handles it]

## Best Practices
- Practice 1
- Practice 2

## Common Pitfalls
- Avoid X, do Y instead
```

## Frontmatter Reference

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Lowercase with hyphens, max 64 chars | `nextjs-expert` |
| `description` | What + When + Keywords, max 1024 chars | See below |

### Optional Fields

| Field | Description | Values |
|-------|-------------|--------|
| `allowed-tools` | Tools skill can use | `Read, Write, Edit, Grep, Glob, Bash` |
| `model` | AI model preference | `haiku`, `sonnet`, `opus` |
| `license` | License type | `MIT`, `Apache-2.0` |
| `metadata.author` | Skill author | Your name |
| `metadata.version` | Semantic version | `"1.0"` |

### Writing Effective Descriptions

**Good description (includes what, when, keywords):**
```yaml
description: Expert in Next.js App Router, server components, and React Server Components. Use when user mentions Next.js, RSC, App Router, server actions, or React server-side patterns.
```

**Bad description (too vague):**
```yaml
description: Helps with Next.js
```

## Skill Types

### 1. Framework/API Expert
**Purpose:** Deep knowledge of specific technology
**Triggers:** Framework name, features, patterns
**Tools:** `Read, Grep, Glob`

```yaml
name: fastapi-expert
description: FastAPI web framework expert covering routing, dependencies, Pydantic models, async endpoints, and OpenAPI generation. Triggers on FastAPI, Python API, Pydantic, async web.
```

### 2. Code Generator
**Purpose:** Create boilerplate or scaffolding
**Triggers:** "generate", "create", "scaffold"
**Tools:** `Write, Read, Grep, Glob`

```yaml
name: component-generator
description: Generate React components with TypeScript, tests, and stories. Triggers on generate component, create component, scaffold component.
```

### 3. Code Analyzer
**Purpose:** Review and analyze code
**Triggers:** "review", "analyze", "audit"
**Tools:** `Read, Grep, Glob`

```yaml
name: security-auditor
description: Security code review for common vulnerabilities including XSS, SQL injection, and OWASP Top 10. Triggers on security review, audit code, find vulnerabilities.
```

### 4. Workflow Automator
**Purpose:** Automate development tasks
**Triggers:** Task-specific keywords
**Tools:** `Read, Write, Edit, Bash`

```yaml
name: release-helper
description: Automate release workflows including changelog generation, version bumping, and git tagging. Triggers on release, changelog, version bump, tag release.
```

### 5. Data Processor
**Purpose:** Transform or analyze data
**Triggers:** Format names, transformation keywords
**Tools:** `Read, Write, Edit, Grep`

```yaml
name: csv-processor
description: Parse, transform, and analyze CSV files. Convert between CSV, JSON, and other formats. Triggers on CSV, parse CSV, convert CSV.
```

## Publishing for npx add-skill

Skills following this format work with `npx add-skill` from any Git repository.

### Repository Structure

```
your-repo/
├── skills/
│   ├── skill-one/
│   │   └── SKILL.md
│   └── skill-two/
│       └── SKILL.md
└── README.md
```

### Installation Commands

```bash
# Users install from your repo
npx add-skill your-username/your-repo

# List available skills
npx add-skill your-username/your-repo --list

# Install specific skill
npx add-skill your-username/your-repo --skill my-skill

# Direct link to skill
npx add-skill https://github.com/user/repo/tree/main/skills/my-skill
```

### Installation Locations

| Scope | Path | Use Case |
|-------|------|----------|
| Personal | `~/.claude/skills/` | Your own tools |
| Project | `.claude/skills/` | Team-shared skills |

## Interactive Skill Creation

When helping users create skills, gather:

1. **Skill name** - lowercase-with-hyphens
2. **What it does** - 1-2 sentence description
3. **When to activate** - trigger keywords
4. **Tools needed** - Read, Write, Edit, Grep, Glob, Bash
5. **Scope** - personal or project

Then generate the SKILL.md with proper structure.

## Validation Checklist

Before publishing:

- [ ] Name is lowercase with hyphens only
- [ ] Description includes trigger keywords
- [ ] Description explains both WHAT and WHEN
- [ ] SKILL.md filename is uppercase
- [ ] YAML frontmatter is valid (no tabs)
- [ ] Only necessary tools are requested
- [ ] Examples are included
- [ ] Under 500 lines (move details to references/)

## Troubleshooting

### Skill Not Activating

1. Check description has specific keywords
2. Verify file is named `SKILL.md` (uppercase)
3. Confirm path: `~/.claude/skills/name/SKILL.md` or `.claude/skills/name/SKILL.md`
4. Validate YAML syntax (no tabs, proper indentation)
5. Restart Claude Code

### Skill Conflicts

Multiple skills with similar triggers:
- Make descriptions more specific
- Use distinct keywords
- Consider combining into one skill

## Resources

- **Agent Skills Spec:** https://agentskills.io
- **Claude Code Docs:** https://docs.anthropic.com/en/docs/claude-code
- **npx add-skill:** https://github.com/vercel-labs/add-skill
