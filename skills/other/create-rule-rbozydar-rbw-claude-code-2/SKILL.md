---
name: create-rule
description: Create new Claude Code rules with proper structure and best practices. Use this skill when developing custom rules for coding standards, conventions, or guidelines that Claude should follow.
---

# Create Rules

This skill helps you develop effective Claude Code rules. Rules are markdown files in `.claude/rules/` that provide persistent instructions Claude follows during a session.

## Rule Basics

### What Rules Are For

- Coding standards and conventions
- Project-specific guidelines
- Language or framework patterns
- Prohibited practices
- Style preferences

### What Rules Are NOT For

- One-time instructions (just tell Claude directly)
- Dynamic content (use commands/skills instead)
- Tool configurations (use hooks)

## Rule Structure

### Basic Template

```markdown
# Rule Name

Brief description of what this rule enforces.

## Section 1

Clear, actionable guidelines.

## Section 2

Examples showing good vs bad patterns.

## Checklist (optional)

- [ ] Quick verification items
```

### Key Principles

1. **Be Specific** - Vague rules get ignored
2. **Show Examples** - Good vs bad patterns are clearer than descriptions
3. **Stay Focused** - One topic per rule file
4. **Be Actionable** - Rules should guide decisions

## Rule Types

### Standards Rules

Define coding standards for a language or framework:

```markdown
# TypeScript Standards

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Interfaces | PascalCase with I prefix | `IUserService` |
| Types | PascalCase | `UserResponse` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |

## Preferred Patterns

### Use type inference when obvious

```typescript
// Good - type is obvious
const count = 0;

// Bad - redundant
const count: number = 0;
```
```

### Prohibited Rules

List things to avoid:

```markdown
# Prohibited Patterns

## Never Use

### 1. any type

```typescript
// Bad
function process(data: any) { ... }

// Good
function process(data: unknown) { ... }
```

### 2. Non-null assertions without checks

```typescript
// Bad
const name = user!.name;

// Good
if (user) {
  const name = user.name;
}
```

## Quick Checklist

- [ ] No `any` types
- [ ] No `!` assertions without guards
- [ ] No `@ts-ignore` without comments
```

### Style Rules

Define formatting and style preferences:

```markdown
# Code Style

## Imports

Order imports in these groups, separated by blank lines:
1. Node built-ins
2. External packages
3. Internal modules
4. Relative imports

## Comments

- Explain WHY, not WHAT
- No commented-out code in commits
- Use JSDoc for public APIs only

## Formatting

- Max line length: 100 characters
- Use trailing commas in multiline
- Prefer template literals over concatenation
```

### Architecture Rules

Define structural patterns:

```markdown
# Service Layer Architecture

## Structure

```
src/
  services/
    user/
      user.service.ts    # Business logic
      user.repository.ts # Data access
      user.types.ts      # Types and interfaces
      index.ts           # Public exports
```

## Patterns

### Services depend on repositories, never the reverse

```typescript
// Good
class UserService {
  constructor(private repo: UserRepository) {}
}

// Bad - repository importing service
class UserRepository {
  constructor(private service: UserService) {} // NO!
}
```
```

## Best Practices

### DO

- Use tables for quick reference
- Include code examples for every guideline
- Group related items together
- Provide a checklist at the end
- Keep rules under 200 lines

### DON'T

- Write walls of text
- Be vague ("write good code")
- Include too many topics in one file
- Repeat what's in other rules
- Use rules for documentation

## Adding Rules to Templates

To contribute a rule to rbw-claude-code:

1. Create the rule in `templates/rules/` or a subdirectory
2. Follow the structure of existing rules
3. Update the README in that directory
4. Test by symlinking to a project

### Directory Structure

```
templates/rules/
├── python/           # Python-specific rules
│   ├── README.md
│   ├── asyncio.md
│   └── ...
├── typescript/       # TypeScript rules (create if needed)
│   └── ...
├── anti-slop.md      # General rules at root
└── README.md         # Overview of all rules
```

## Testing Your Rule

1. Create the rule in your project's `.claude/rules/`
2. Start a new Claude Code session
3. Ask Claude to do something the rule addresses
4. Verify Claude follows the rule
5. Iterate on wording if needed

## Templates

Ready-to-use templates are available in:

```
${CLAUDE_PLUGIN_ROOT}/skills/create-rule/templates/
```

- `standards.md` - Coding standards template
- `prohibited.md` - Prohibited patterns template
- `style.md` - Style guide template
