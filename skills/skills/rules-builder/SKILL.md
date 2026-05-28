---
name: rules-builder
description: Use when the user wants to create, edit, list, or manage Claude Code rules in .claude/rules/. Provides guided elicitation to configure path-specific rules with proper YAML frontmatter and glob patterns. Can list all available rules from user-level and project directories.
---

# Rules Builder

Interactive skill for creating and managing Claude Code modular rules using guided elicitation with `AskUserQuestion`.

## When to Use

- User wants to create a new rule file
- User wants to edit or delete an existing rule
- User wants to list or view existing rules
- User mentions `.claude/rules/`
- User asks about path-specific rules or glob patterns
- User wants to organize project instructions
- User wants personal rules across all projects

## Elicitation Approach

Use `AskUserQuestion` throughout the workflow to guide the user through all available options. Present relevant choices based on context and let the user shape the rule configuration step by step.

## What Can Be Done with Rules

### Rule Scope Options

| Scope | Description |
|-------|-------------|
| **Global** | Applies to all files in the project (no `paths` frontmatter) |
| **Path-specific** | Only applies to files matching glob patterns |

### Rule Locations

| Location | Path | Applies To |
|----------|------|------------|
| User-level | `~/.claude/rules/` | All your projects (personal preferences) |
| Project root | `.claude/rules/` | Current project only |
| Subdirectory | `.claude/rules/frontend/` | Current project, organized by domain |
| Subdirectory | `.claude/rules/backend/` | Current project, organized by domain |

**Priority**: User-level rules load first, project rules load after and can override.

### Glob Pattern Options

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `**/*.{ts,tsx}` | TypeScript and React files |
| `src/**/*` | All files under src/ |
| `src/api/**/*.ts` | API files only |
| `**/*.{test,spec}.ts` | Test files only |
| `*.config.{js,ts,json}` | Config files in root |
| `{src,lib}/**/*.ts` | Multiple directories |

See `${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/references/glob-patterns.md` for complete reference.

### Rule Categories

Common categories to organize rules:
- Code style and formatting
- Testing conventions
- Security requirements
- API development patterns
- Documentation standards
- Performance guidelines
- Framework-specific rules (React, Node, etc.)

### Frontmatter Options

Valid YAML frontmatter fields:

```yaml
---
paths: "src/**/*.ts"        # Glob pattern(s) - string or array
description: "API rules"    # Optional description (max 200 chars)
priority: 75                # Optional priority 0-100 (default 50)
enabled: true               # Optional enable/disable (default true)
---
```

Validate against schema: `${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/schemas/rule-frontmatter.schema.json`

### Available Operations

| Operation | Description |
|-----------|-------------|
| **Create** | New rule file with guided configuration |
| **Edit** | Modify existing rule (scope, content, frontmatter) |
| **Delete** | Remove a rule file |
| **List** | Show all rules in project or user directory |
| **Validate** | Check frontmatter against schema |
| **Move** | Change rule location (project ↔ user-level) |

## Workflow

1. **Determine intent** - Create, edit, delete, or list rules
2. **Elicit configuration** - Use `AskUserQuestion` to gather:
   - Rule scope (global vs path-specific)
   - Target files (glob patterns)
   - Location (user-level vs project)
   - Category and filename
   - Initial content suggestions
3. **Generate/modify file** - Create or edit the rule with proper frontmatter
4. **Validate** - Check frontmatter against JSON schema
5. **Confirm** - Show result and offer next actions

## User-Level Rules

Personal rules in `~/.claude/rules/` apply to all projects:

```
~/.claude/rules/
├── preferences.md    # Personal coding preferences
├── workflows.md      # Preferred workflows
└── shortcuts.md      # Personal shortcuts
```

Use cases:
- Consistent style across all projects
- Personal workflow reminders
- Default behaviors that projects can override

## Organizing Rules

### By Domain (Subdirectories)

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

### By Scope (Path-Specific)

```yaml
---
paths: src/api/**/*.ts
---
# API Rules
```

### Symlinks for Shared Rules

```bash
ln -s ~/shared-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

## Best Practices

- **Keep rules focused** - One topic per file
- **Use descriptive filenames** - `code-style.md` not `rules1.md`
- **Use conditional rules sparingly** - Only when truly path-specific
- **Organize with subdirectories** - Group related rules
- **Be specific** - "Use 2-space indentation" not "Format properly"
- **Review periodically** - Update as project evolves

## Listing Rules

To show all available rules from both user-level and project directories:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/scripts/list_rules.py [project_path]
```

**Examples:**
```bash
# List rules for current directory
python3 ${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/scripts/list_rules.py

# List rules for specific project
python3 ${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/scripts/list_rules.py /path/to/project
```

**Output includes:**
- User-level rules from `~/.claude/rules/`
- Project rules from `<project>/.claude/rules/`
- For each rule: name, path, description, glob patterns, scope, priority, enabled status

## Validation

Before saving, validate frontmatter against the JSON schema:

| Field | Type | Constraints |
|-------|------|-------------|
| `paths` | string or string[] | Valid glob pattern(s) |
| `description` | string | Max 200 characters |
| `priority` | integer | 0-100, default 50 |
| `enabled` | boolean | default true |

## References

- **Glob patterns**: `${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/references/glob-patterns.md`
- **Frontmatter schema**: `${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/schemas/rule-frontmatter.schema.json`
- **List rules script**: `${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/scripts/list_rules.py`
- **Validate script**: `${CLAUDE_PLUGIN_ROOT}/skills/rules-builder/scripts/validate_frontmatter.py`

## Examples

**Create API-specific rules**
```
User: "I want rules for my API endpoints"
-> Elicit scope, patterns, location, category
-> Create .claude/rules/api.md with paths: src/api/**/*.ts
```

**Edit existing rule scope**
```
User: "Update testing rules to include integration tests"
-> List rules, elicit selection
-> Show current config, elicit changes
-> Update paths to **/*.{test,spec,integration}.ts
```

**Create personal preferences**
```
User: "Add my coding preferences for all projects"
-> Elicit location (user-level)
-> Create ~/.claude/rules/preferences.md
```

**Organize by domain**
```
User: "Organize my frontend rules"
-> Elicit subdirectory structure
-> Create .claude/rules/frontend/ with react.md, styles.md
```

**List all rules**
```
User: "Show me all my rules"
-> Run list_rules.py script
-> Display user-level and project rules with metadata
-> Offer to edit, delete, or create new rules
```
