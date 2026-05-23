---
name: creating-cursor-commands
description: Expert guidance for creating effective Cursor slash commands with best practices, format requirements, and schema validation
---

# Creating Cursor Slash Commands

You are an expert at creating effective Cursor slash commands (`.cursor/commands/*.md`) that provide clear, actionable instructions for AI assistants.

## When to Use This Skill

**Use when:**
- User wants to create a new Cursor slash command
- User asks to improve existing slash commands
- User needs help understanding Cursor command format
- User wants to convert prompts to slash commands
- User asks about Cursor command validation

**Don't use for:**
- Cursor rules (`.cursor/rules/`) - use `creating-cursor-rules-skill` instead
- Claude Code slash commands - those use different format with frontmatter
- Complex multi-step workflows - those should be Cursor rules

## Quick Reference

| Aspect | Requirement |
|--------|-------------|
| **File Location** | `.cursor/commands/*.md` |
| **Format** | Plain Markdown (NO frontmatter) |
| **Filename** | Descriptive kebab-case (e.g., `review-code.md`, `generate-tests.md`) |
| **Invocation** | `/command-name` in chat |
| **Content** | Clear, actionable instructions with examples |

## Format Requirements

### Critical Rules

1. **NO frontmatter allowed** - Cursor commands are plain Markdown only
2. **Descriptive filenames** - The filename becomes the command name
3. **Clear instructions** - Tell AI exactly what to do
4. **Include examples** - Show desired output format

### File Naming

**Good filenames:**
- `review-code.md` → `/review-code`
- `generate-tests.md` → `/generate-tests`
- `explain-code.md` → `/explain-code`
- `optimize-performance.md` → `/optimize-performance`

**Bad filenames:**
- `rc.md` - Too cryptic
- `review_code.md` - Use hyphens, not underscores
- `ReviewCode.md` - Use lowercase
- `review-code-thoroughly-with-security-checks.md` - Too verbose

## Schema Validation

### Schema Location
`https://github.com/pr-pm/prpm/blob/main/packages/converters/schemas/cursor-command.schema.json`

### Schema Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://prpm.dev/schemas/cursor-command.schema.json",
  "title": "Cursor Command Format",
  "description": "JSON Schema for Cursor commands (slash commands) - plain Markdown files in .cursor/commands/",
  "type": "object",
  "required": ["content"],
  "properties": {
    "content": {
      "type": "string",
      "description": "Plain Markdown content describing what the command should do. No frontmatter supported."
    }
  },
  "additionalProperties": false
}
```

### Key Validations

1. **Must be plain Markdown** - No YAML frontmatter
2. **Content-only structure** - Single `content` field
3. **No metadata** - Unlike Cursor rules, commands have no configuration

## Common Mistakes

| Mistake | Why It's Wrong | How to Fix |
|---------|---------------|------------|
| Adding frontmatter | Cursor commands don't support frontmatter | Remove `---` blocks entirely |
| Using default exports syntax | Commands are not code files | Write plain Markdown instructions |
| Vague instructions | AI needs specific guidance | Add concrete examples and steps |
| Too many tasks | Commands should be focused | Create separate commands or use rules |
| Missing context | AI needs to know what to do | Include expected output format |

## Best Practices

### 1. Be Specific and Actionable

**❌ Bad - Vague:**
```markdown
# Review Code

Review the code for issues.
```

**✅ Good - Specific:**
```markdown
# Review Code

Review the selected code for:
- Code quality and best practices
- Potential bugs or edge cases
- Performance improvements
- Security vulnerabilities

Provide specific, actionable feedback with code examples where appropriate.
```

### 2. Include Expected Output Format

**❌ Bad - No guidance:**
```markdown
# Generate Tests

Generate tests for this code.
```

**✅ Good - Clear format:**
```markdown
# Generate Tests

Generate comprehensive unit tests for the selected code.

Include:
- Happy path test cases
- Edge cases and error handling
- Mock external dependencies
- Follow existing test patterns in the project

Use the testing framework already configured in the project.
```

### 3. Provide Step-by-Step Instructions

**✅ Good - Structured approach:**
```markdown
# Explain Code

Provide a clear explanation of what the selected code does.

Include:
- High-level purpose and goals
- Step-by-step breakdown of logic
- Any non-obvious behavior or edge cases
- Dependencies and side effects
- How it fits into the larger codebase
```

### 4. Reference Project Context

**✅ Good - Context-aware:**
```markdown
# Add Component

Create a new React component following our project conventions.

Structure:
- Functional component with TypeScript
- Props interface defined separately
- Export as named export (not default)
- Co-locate styles if needed
- Follow existing component patterns in components/ directory

Use the same testing approach as existing components.
```

### 5. Focus on One Task

Each command should do ONE thing well.

**❌ Bad - Too broad:**
```markdown
# Full Stack Feature

Create a full-stack feature with:
- Database migration
- API endpoint
- Frontend component
- Tests for everything
- Documentation
```

**✅ Good - Focused:**
```markdown
# Create API Endpoint

Create a new API endpoint following our conventions.

Include:
- Input validation with Zod
- Error handling with try/catch
- TypeScript types for request/response
- Follow patterns in existing endpoints
```

## Examples

### Code Review Command

`.cursor/commands/review-code.md`:

```markdown
# Review Code

Review the selected code for:

1. **Code Quality**
   - Clean, readable code
   - Proper naming conventions
   - DRY principle adherence

2. **Security**
   - Input validation
   - SQL injection risks
   - XSS vulnerabilities
   - Authentication/authorization checks

3. **Performance**
   - Inefficient algorithms
   - Unnecessary computations
   - Memory leaks
   - Database query optimization

4. **Best Practices**
   - Error handling
   - Type safety
   - Test coverage
   - Documentation

Provide specific file and line references for all issues found.
Format findings as a numbered list with severity (Critical/High/Medium/Low).
```

### Test Generation Command

`.cursor/commands/generate-tests.md`:

```markdown
# Generate Tests

Generate comprehensive unit tests for the selected code.

Test Coverage:
- Happy path scenarios
- Edge cases
- Error conditions
- Boundary values
- Invalid inputs

Requirements:
- Use existing test framework (Jest/Vitest/etc.)
- Follow project testing patterns
- Mock external dependencies
- Include test descriptions
- Aim for 100% code coverage

Format tests in the same style as existing test files in the project.
```

### Documentation Generator

`.cursor/commands/document-function.md`:

```markdown
# Document Function

Generate comprehensive documentation for the selected function.

Include:

**Function signature:**
- Parameter types and descriptions
- Return type and description
- Generic types if applicable

**Description:**
- What the function does (one-line summary)
- Why it exists (use case)
- How it works (implementation details if non-obvious)

**Examples:**
- Basic usage example
- Edge case example if relevant

**Notes:**
- Any side effects
- Performance considerations
- Related functions

Use JSDoc/TSDoc format for TypeScript/JavaScript.
```

### Optimization Command

`.cursor/commands/optimize-performance.md`:

```markdown
# Optimize Performance

Analyze the selected code for performance improvements.

Look for:

**Algorithmic Issues:**
- O(n²) or worse time complexity
- Unnecessary nested loops
- Inefficient data structures

**React-Specific:**
- Unnecessary re-renders
- Missing useMemo/useCallback
- Large component trees
- Props drilling

**General:**
- Redundant computations
- Memory leaks
- Synchronous blocking operations
- Large bundle size contributors

Suggest specific optimizations with code examples.
Estimate performance impact of each suggestion.
```

### Refactoring Command

`.cursor/commands/refactor-clean.md`:

```markdown
# Refactor for Clean Code

Refactor the selected code to improve maintainability.

Apply these principles:

**Extract Functions:**
- Break down large functions (> 50 lines)
- Create single-responsibility functions
- Use descriptive names

**Simplify Logic:**
- Reduce nesting (early returns)
- Eliminate duplication
- Clarify complex conditionals

**Improve Names:**
- Use meaningful variable names
- Follow project naming conventions
- Avoid abbreviations

**Type Safety:**
- Add proper TypeScript types
- Eliminate 'any' types
- Use interfaces/types

Preserve all existing functionality and tests.
```

### Bug Fix Command

`.cursor/commands/fix-bug.md`:

```markdown
# Fix Bug

Analyze and fix the bug in the selected code.

Investigation steps:
1. Identify the root cause
2. Explain why the bug occurs
3. Propose a fix
4. Consider edge cases
5. Suggest tests to prevent regression

Fix requirements:
- Minimal changes to fix the issue
- Don't break existing functionality
- Add/update tests
- Add comments explaining the fix if non-obvious

Explain the fix clearly with before/after code examples.
```

## Storage Locations

Commands can be stored in multiple locations (in order of precedence):

1. **Project commands**: `.cursor/commands/` directory in your project (shared with team)
2. **Global commands**: `~/.cursor/commands/` directory (personal, all projects)
3. **Team commands**: Created via Cursor Dashboard (enterprise teams)

**Best practice:** Store team-wide commands in `.cursor/commands/` and commit to version control.

## Testing Your Commands

After creating a command:

1. **Save** to `.cursor/commands/command-name.md`
2. **Invoke** with `/command-name` in Cursor chat
3. **Verify** AI follows instructions correctly
4. **Test edge cases**:
   - No code selected
   - Empty files
   - Complex code
   - Different languages
5. **Iterate** based on results

## Commands vs. Cursor Rules

### Use Commands When:
- ✅ Simple, focused task
- ✅ Explicit user invocation desired
- ✅ Personal productivity shortcuts
- ✅ One-time operations

### Use Cursor Rules When:
- ✅ Context-aware automatic activation
- ✅ File-type specific guidance
- ✅ Team standardization
- ✅ Always-on conventions

**Example:**
- **Command:** `/generate-tests` - Explicitly generate tests when asked
- **Rule:** Auto-attach testing conventions to `*.test.ts` files

## Validation Checklist

Before finalizing a command:

- [ ] Filename is descriptive and kebab-case
- [ ] NO frontmatter (plain Markdown only)
- [ ] Instructions are clear and specific
- [ ] Expected output format is described
- [ ] Examples are included
- [ ] Steps are actionable
- [ ] Command is focused on one task
- [ ] Edge cases are considered
- [ ] File is in `.cursor/commands/` directory
- [ ] Command has been tested

## Converting from Other Formats

### From Claude Code Slash Commands

Claude Code commands use frontmatter - remove it for Cursor:

**Claude Code:**
```markdown
---
description: Review code
allowed-tools: Read, Grep
---

Review the code...
```

**Cursor:**
```markdown
# Review Code

Review the code...
```

### From Cursor Rules

Rules use frontmatter and are context-aware - simplify to plain Markdown:

**Cursor Rule:**
```markdown
---
description: Testing conventions
globs: ["**/*.test.ts"]
---

# Testing Standards

Always write tests...
```

**Cursor Command:**
```markdown
# Generate Tests

Generate comprehensive tests...
```

## Common Use Cases

### Code Quality
- `/review-code` - Code review
- `/refactor-clean` - Clean code refactoring
- `/fix-lint` - Fix linting issues
- `/improve-types` - Improve TypeScript types

### Testing
- `/generate-tests` - Generate unit tests
- `/test-edge-cases` - Add edge case tests
- `/test-coverage` - Check test coverage

### Documentation
- `/document-function` - Document function
- `/add-comments` - Add code comments
- `/explain-code` - Explain complex code

### Performance
- `/optimize-performance` - Performance optimization
- `/analyze-complexity` - Analyze time complexity
- `/reduce-bundle` - Reduce bundle size

### Security
- `/security-audit` - Security vulnerability check
- `/sanitize-input` - Add input validation
- `/check-auth` - Review authentication

## References

- **Schema**: `https://github.com/pr-pm/prpm/blob/main/packages/converters/schemas/cursor-command.schema.json`
- **Docs**: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/cursor.md`
- **Official Docs**: https://cursor.com/docs/agent/chat/commands

## Remember

**Golden Rules:**
1. NO frontmatter - plain Markdown only
2. Descriptive filenames - they become command names
3. Clear instructions - AI needs specific guidance
4. Include examples - show desired output
5. One task per command - keep it focused

**Goal:** Create commands that make frequent tasks effortless with a simple `/command-name` invocation.
