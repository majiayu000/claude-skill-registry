---
name: create-skill
description: Create a new Claude Code agent skill with proper folder structure and SKILL.md format. Use when the user wants to add a model-invoked skill that Claude uses autonomously based on context. Handles skill folder creation with SKILL.md and optional reference files.
---

# Create Skill Skill

Create new Claude Code agent skills that Claude invokes autonomously based on task context.

## Skill Structure

Each skill lives in its own folder within `skills/`:

```
skills/
└── skill-name/
    ├── SKILL.md              # Main skill definition (required)
    ├── examples/             # Example files (optional)
    │   └── example.md
    └── templates/            # Templates (optional)
        └── template.md
```

## SKILL.md Format

```markdown
---
name: skill-name
description: When and how Claude should use this skill. Be specific about triggers and use cases.
user-invocable: false
---

# Skill Title

Detailed instructions for how to apply this skill...
```

## Required Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Unique identifier (kebab-case) | `python-best-practices` |
| `description` | When Claude should invoke this skill | `Apply Python best practices when writing or reviewing Python code. Use for type hints, docstrings, and PEP compliance.` |

## Optional Frontmatter Fields

| Field | Description | Default | Example |
|-------|-------------|---------|---------|
| `user-invocable` | Whether users can invoke skill with `/skill-name` | `true` | `false` for knowledge skills, `true` for action skills |

## Writing Effective Descriptions

The description is **critical** - it tells Claude when to use the skill. Include:

1. **Trigger conditions**: When should this skill activate?
2. **Use cases**: What tasks benefit from this skill?
3. **Scope**: What does and doesn't this skill cover?

### Good Description Examples

```yaml
description: Apply React best practices when creating or modifying React components. Use for hooks, state management, component structure, and performance optimization.
```

```yaml
description: Enforce security best practices when writing code that handles user input, authentication, or sensitive data. Covers input validation, SQL injection prevention, and XSS protection.
```

```yaml
description: Generate API documentation when creating or updating REST endpoints. Produces OpenAPI-compatible documentation with examples.
```

### Bad Description Examples

```yaml
# Too vague - Claude won't know when to use it
description: Helps with Python code
```

```yaml
# Too broad - will trigger too often
description: Use this for all coding tasks
```

## Skill Body Content

The body should include:

1. **Context**: Background information Claude needs
2. **Rules/Guidelines**: Specific practices to follow
3. **Examples**: Concrete examples of correct usage
4. **Anti-patterns**: What to avoid
5. **Output format**: How to present results

## Example Skill

```markdown
---
name: conventional-commits
description: Apply conventional commit message format when the user is committing code or asking about commit messages. Enforces type prefixes, scope, and message structure.
user-invocable: false
---

# Conventional Commits

Format all commit messages following the Conventional Commits specification.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

## Examples

### Feature
```
feat(auth): add OAuth2 login support
```

### Bug Fix
```
fix(api): handle null response in user endpoint
```

### Breaking Change
```
feat(api)!: change response format for /users endpoint

BREAKING CHANGE: Response now returns array instead of object
```

## Rules

1. Type is required and lowercase
2. Description starts lowercase, no period at end
3. Use imperative mood ("add" not "added")
4. Keep first line under 72 characters
```

## Adding Subfolders

Skills can include reference materials:

```
skills/
└── api-design/
    ├── SKILL.md
    ├── examples/
    │   ├── rest-example.md
    │   └── graphql-example.md
    └── templates/
        └── openapi-template.yaml
```

Reference these in your SKILL.md:
```markdown
See `examples/rest-example.md` for a complete REST API example.
```

## File Location

Save skills to:
```
plugins/<plugin-name>/skills/<skill-name>/SKILL.md
```
