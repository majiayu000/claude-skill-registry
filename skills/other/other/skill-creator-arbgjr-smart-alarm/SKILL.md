---
name: skill-creator
description: Guide for creating effective skills. Use when users want to create a new skill, update an existing skill, or learn about skill structure, frontmatter fields, hooks, context forking, or distribution patterns.
---

# Skill Creator

This skill provides guidance for creating effective Claude Code skills following the official documentation.

## What is a Skill?

A Skill is a markdown file that teaches Claude how to do something specific. Skills transform Claude from a general-purpose agent into a specialized agent with procedural knowledge, domain expertise, and bundled resources.

## Skill Structure

```
skill-name/
├── SKILL.md                 # Required: frontmatter + instructions
├── reference.md             # Optional: detailed documentation
├── examples.md              # Optional: usage examples
├── templates/               # Optional: template files
└── scripts/                 # Optional: utility scripts
    ├── helper.py
    └── validate.sh
```

## Where Skills Live

| Location | Path | Scope | Priority |
|----------|------|-------|----------|
| Managed | See admin settings | All org users | 1 (highest) |
| Personal | `~/.claude/skills/` | You, all projects | 2 |
| Project | `.claude/skills/` | Team in repo | 3 |
| Plugin | `skills/` in plugin dir | Plugin users | 4 (lowest) |

Higher priority locations override lower ones when names conflict.

## SKILL.md Format

### Frontmatter Fields (Complete Reference)

```yaml
---
name: skill-name
description: What this skill does and when to use it
allowed-tools:
  - Read
  - Grep
  - Glob
model: claude-sonnet-4-20250514
context: fork
agent: Plan
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
user-invocable: true
disable-model-invocation: false
---
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, numbers, hyphens. Must match directory name. Max 64 chars |
| `description` | Yes | What skill does + when to use. Include trigger keywords. Max 1024 chars |
| `allowed-tools` | No | Tools Claude can use without permission when skill is active |
| `model` | No | Specific model to use (e.g., `claude-sonnet-4-20250514`) |
| `context` | No | Set to `fork` to run in isolated sub-agent context |
| `agent` | No | Agent type when `context: fork`: `Explore`, `Plan`, `general-purpose`, or custom |
| `hooks` | No | Lifecycle hooks: `PreToolUse`, `PostToolUse`, `Stop` |
| `user-invocable` | No | Show in slash menu (default: true) |
| `disable-model-invocation` | No | Block programmatic invocation via Skill tool |
| `skills` | No | (Subagents only) Skills to inject into subagent context |

## allowed-tools Configuration

### Format Options

**Comma-separated:**
```yaml
allowed-tools: Read, Grep, Glob
```

**YAML array:**
```yaml
allowed-tools:
  - Read
  - Grep
  - Glob
```

**With command filtering:**
```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

### Common Tools

`Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Skill`, `Task`

## Context Fork (Isolated Execution)

Run skills in separate sub-agent context with own conversation history:

```yaml
---
name: data-analysis
description: Analyze data and generate reports
context: fork
agent: Plan
---
```

| Aspect | Normal Skill | Forked Skill |
|--------|--------------|--------------|
| Context | Shares conversation | Isolated history |
| Visibility | In main conversation | Runs in background |
| When to use | Simple guidance | Complex multi-step workflows |

## Hooks Configuration

Only `PreToolUse`, `PostToolUse`, and `Stop` are supported in skill frontmatter.

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

### Hook Options

| Option | Type | Description |
|--------|------|-------------|
| `type` | string | `command` for bash or `prompt` for LLM evaluation |
| `command` | string | Bash command to execute |
| `prompt` | string | LLM prompt for evaluation |
| `matcher` | string | Tool pattern to match (regex) |
| `timeout` | number | Timeout in seconds (default: 60) |
| `once` | boolean | Run only once per session |

### Hook Exit Codes

- **Exit 0**: Success
- **Exit 2**: Blocking error (stderr as message)
- **Other**: Non-blocking error

## Invocation Control

### Three Invocation Methods

| Setting | Slash Menu | Skill Tool | Auto-Discovery |
|---------|-----------|-----------|----------------|
| Default | Visible | Allowed | Yes |
| `user-invocable: false` | Hidden | Allowed | Yes |
| `disable-model-invocation: true` | Visible | Blocked | Yes |

**Use `user-invocable: false`** for skills Claude should use but users shouldn't invoke manually.

**Use `disable-model-invocation: true`** for skills users invoke manually but Claude shouldn't.

## Skills and Subagents

Subagents don't automatically inherit skills. To give a custom subagent access:

**File: `.claude/agents/code-reviewer.md`**
```yaml
---
name: code-reviewer
description: Review code for quality
skills: pr-review, security-check, style-guide
---

Review this code thoroughly...
```

## Core Principles

### 1. Concise is Key

The context window is a public good. Skills share it with system prompt, conversation history, other skills' metadata, and user requests.

**Default assumption: Claude is already smart.** Only add context Claude doesn't have.

### 2. Set Appropriate Degrees of Freedom

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| High (text instructions) | Multiple valid approaches | General guidelines |
| Medium (pseudocode) | Preferred pattern exists | Configurable workflows |
| Low (specific scripts) | Operations are fragile | Critical sequences |

### 3. Progressive Disclosure

Skills use three-level loading:

1. **Metadata** (always in context) - name + description (~100 words)
2. **SKILL.md body** (when triggered) - instructions (<5k words)
3. **Bundled resources** (as needed) - scripts, references, assets

**Keep SKILL.md under 500 lines.** Split content when approaching this limit.

## Writing Effective Descriptions

A good description answers:
1. **What does this skill do?** - List specific capabilities
2. **When should Claude use it?** - Include trigger keywords

**Poor:**
```yaml
description: Helps with documents
```

**Good:**
```yaml
description: Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

## File Organization Patterns

### Pattern 1: High-level guide with references

```markdown
# PDF Processing

## Quick start
[code example]

## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md)
- **API reference**: See [REFERENCE.md](REFERENCE.md)
```

### Pattern 2: Domain-specific organization

```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Framework variants

```
cloud-deploy/
├── SKILL.md
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

**Important:** Keep references one level deep. Avoid chains (A -> B -> C).

## What NOT to Include

- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- User-facing documentation
- Setup/testing procedures

The skill should only contain information needed for Claude to do the job.

## Skill Creation Process

1. **Understand the skill** - Gather concrete usage examples
2. **Plan resources** - Identify scripts, references, assets needed
3. **Create directory** - `mkdir -p .claude/skills/skill-name`
4. **Write SKILL.md** - Frontmatter + instructions
5. **Add resources** - Scripts, references, assets as needed
6. **Test** - Use the skill on real tasks
7. **Iterate** - Improve based on actual usage

## Complete Examples

### Example 1: Simple Single-File Skill

```yaml
---
name: commit-helper
description: Generate clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
allowed-tools: Bash(git diff:*), Bash(git status:*)
---

# Commit Message Generator

## Instructions

1. Run `git diff --staged` to see changes
2. Suggest commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best Practices

- Use present tense imperative
- Explain what and why, not how
```

### Example 2: Multi-File with Scripts

```yaml
---
name: pdf-processor
description: Extract text, fill forms, merge PDFs. Use when working with PDF files.
allowed-tools: Read, Bash(python:*)
---

# PDF Processing

## Quick Start

```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Validation

```bash
python scripts/validate.py input.pdf
```

## Resources
- Form filling: See [FORMS.md](FORMS.md)
- API reference: See [REFERENCE.md](REFERENCE.md)
```

### Example 3: Security-Focused with Hooks

```yaml
---
name: secure-db-ops
description: Execute database queries with validation and audit logging.
allowed-tools: Bash(psql:*), Bash(mysql:*)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-query.sh"
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/audit-log.sh"
---

# Secure Database Operations

All queries are validated before execution and logged for audit.
```

### Example 4: Forked Context Skill

```yaml
---
name: code-analysis
description: Analyze code quality and generate detailed reports
context: fork
agent: Plan
---

# Code Analysis

Run comprehensive analysis in isolated context...
```

## Troubleshooting

### Skill Not Triggering

Make description more specific with trigger keywords.

### Skill Won't Load

1. File must be `SKILL.md` (case-sensitive)
2. YAML must start with `---` on line 1 (no blank lines)
3. Use spaces for indentation (not tabs)
4. Run `claude --debug` to see errors

### Script Permission Issues

```bash
chmod +x scripts/*.py scripts/*.sh
```

### Multiple Skills Conflict

Make descriptions distinct with specific trigger terms.

## Environment Variables (Hooks Only)

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Absolute path to project root |
| `CLAUDE_PLUGIN_ROOT` | Absolute path to plugin directory |
| `CLAUDE_CODE_REMOTE` | "true" if remote environment |
