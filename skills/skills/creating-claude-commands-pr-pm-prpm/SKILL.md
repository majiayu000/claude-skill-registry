---
name: creating-claude-commands
description: Expert guidance for creating Claude Code slash commands with correct frontmatter, structure, and best practices
---

# Creating Claude Code Slash Commands

Expert guidance for creating Claude Code slash commands - quick actions triggered by `/command-name`.

## When to Use This Skill

Activate this skill when:
- User wants to create a new slash command
- User needs to understand slash command structure
- User asks about frontmatter fields for commands
- User wants validation guidance for commands
- User needs examples of command patterns

## Quick Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `description` | No | string | Brief description shown in autocomplete |
| `allowed-tools` | No | string | Comma-separated list of tools (inherits if not specified) |
| `argument-hint` | No | string | Expected arguments (e.g., `add [tagId] \| remove [tagId] \| list`) |
| `model` | No | string | Specific model (`sonnet`, `opus`, `haiku`, `inherit`) |
| `disable-model-invocation` | No | boolean | Prevent SlashCommand tool from calling this |
| `commandType` | No | string | Set to `"slash-command"` for round-trip conversion |

## Special Features

### File Referencing with `@`
Reference files directly in command prompts using `@` prefix:
```markdown
Review the implementation in @src/utils/helpers.js
Compare @src/old-version.js with @src/new-version.js
```

### Bash Execution with `!`
Execute bash commands inline using `!` prefix (requires Bash in `allowed-tools`):
```markdown
---
allowed-tools: Bash(git *)
---

Current git status: !`git status`
Last 5 commits: !`git log --oneline -5`
```

### Arguments
- `$ARGUMENTS` - All arguments passed to command
- `$1`, `$2`, `$3`... `$9` - Individual positional arguments

### Namespacing
- Use subdirectories in `.claude/commands/` to organize commands
- Commands appear as `/subdirectory.command-name`
- Example: `.claude/commands/git/quick-commit.md` → `/git.quick-commit`

## File Location

Slash commands must be saved as Markdown files:

**Project commands** (shared with team):
```
.claude/commands/command-name.md
```

**Personal commands** (individual use):
```
~/.claude/commands/command-name.md
```

## Format Requirements

### Basic Structure

```markdown
---
description: Generate documentation for code
allowed-tools: Read, Edit
model: sonnet
---

# 📝 Documentation Generator

Generate comprehensive documentation for the selected code.

## Instructions

- Analyze code structure and purpose
- Generate clear, concise documentation
- Include parameter descriptions
- Add usage examples
- Follow JSDoc/TSDoc format for TypeScript
```

### With Arguments

```markdown
---
description: Manage tags for files
argument-hint: add [tagId] | remove [tagId] | list
allowed-tools: Read, Write
---

# Tag Manager

Manage tags for project files.

## Usage

- `/tags add <tagId>` - Add a tag (use $1 for tagId)
- `/tags remove <tagId>` - Remove a tag (use $1 for tagId)
- `/tags list` - List all tags

## Implementation

Action: $1
Tag ID: $2
All arguments: $ARGUMENTS
```

### With File References

```markdown
---
description: Compare two files and suggest improvements
allowed-tools: Read, Edit
argument-hint: <file1> <file2>
---

# File Comparator

Compare @$1 with @$2 and identify:
- Differences in approach
- Which implementation is better
- Suggested improvements
```

### With Bash Execution

```markdown
---
description: Create commit with git status context
argument-hint: <commit-message>
allowed-tools: Bash(git *)
---

# Smart Git Commit

## Current Status
!`git status --short`

## Recent Changes
!`git diff --stat`

Create a commit with message: $ARGUMENTS

Ensure the commit message follows conventional commit format.
```

### Minimal Command

```markdown
---
description: Quick code review
---

Review the current file for:
- Code quality issues
- Security vulnerabilities
- Performance bottlenecks
- Best practice violations
```

## Frontmatter Fields

### description (optional)

Brief description of what the command does. Shown in autocomplete. Defaults to first line from prompt if not specified.

```yaml
---
description: Generate comprehensive documentation for selected code
---
```

### allowed-tools (optional)

Comma-separated string of tools the command can use. Inherits from conversation if not specified.

**Valid tools:** `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `WebSearch`, `WebFetch`, `Task`, `Skill`, `SlashCommand`, `TodoWrite`, `AskUserQuestion`

```yaml
---
allowed-tools: Read, Edit, Grep
---
```

**With Bash restrictions:**
```yaml
---
allowed-tools: Bash(git status:*), Bash(git diff:*), Read
---
```

### argument-hint (optional)

Expected arguments for the command. Shown when auto-completing.

```yaml
---
argument-hint: [file-path]
---
```

```yaml
---
argument-hint: add [tagId] | remove [tagId] | list
---
```

### model (optional)

Specific model to use for this command. Inherits from conversation if not specified.

**Valid values:**
- `sonnet` - General purpose (Claude Sonnet 3.5)
- `haiku` - Fast, simple tasks (Claude Haiku 3.5)
- `opus` - Complex reasoning (Claude Opus 4)
- `inherit` - Use conversation model (default)

```yaml
---
model: sonnet
---
```

### disable-model-invocation (optional)

Set to `true` to prevent Claude from automatically invoking this command via the SlashCommand tool.

```yaml
---
disable-model-invocation: true
---
```

### commandType (optional)

Set to `"slash-command"` for explicit type preservation in round-trip conversion (PRPM extension).

```yaml
---
commandType: slash-command
---
```

## Content Format

The content after frontmatter contains the command prompt and instructions.

### H1 Title (optional)

Can include emoji icon for visual identification:

```markdown
# 📝 Documentation Generator
```

```markdown
# 🔍 Code Reviewer
```

### Instructions

Clear, actionable guidance for what the command should do:

```markdown
## Instructions

- Analyze code structure and purpose
- Generate clear, concise documentation
- Include parameter descriptions
- Add usage examples
```

### Output Format

Specify expected output format:

```markdown
## Output Format

Return formatted documentation ready to paste above the code:

/**
 * Function description
 * @param {string} name - Parameter description
 * @returns {Promise<User>} Return value description
 */
```

### Examples

Show Claude what good output looks like:

```markdown
## Example Output

```typescript
/**
 * Creates a new user with the provided data
 * @param {UserData} userData - User information (email, name)
 * @returns {Promise<User>} Created user with ID
 * @throws {ValidationError} If email format is invalid
 */
async function createUser(userData: UserData): Promise<User> {
  // ...
}
```
```

## Schema Validation

Commands are validated against the JSON Schema:

**Schema Location:** https://github.com/pr-pm/prpm/blob/main/packages/converters/schemas/claude-slash-command.schema.json

**Required structure:**
```json
{
  "frontmatter": {
    "description": "string (optional)",
    "allowed-tools": "string (optional)",
    "argument-hint": "string (optional)",
    "model": "string (optional)",
    "disable-model-invocation": "boolean (optional)",
    "commandType": "slash-command (optional)"
  },
  "content": "string (markdown content)"
}
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Using array for tools | `allowed-tools: [Read, Write]` | Use string: `allowed-tools: Read, Write` |
| Wrong field names | `tools:`, `arguments:` | Use `allowed-tools`, `argument-hint` |
| Missing frontmatter delimiters | Frontmatter not parsed | Use `---` before and after YAML |
| Invalid tool names | `bash`, `grep` (lowercase) | Use capitalized: `Bash`, `Grep` |
| Invalid model values | `3.5-sonnet`, `claude-opus` | Use: `sonnet`, `opus`, `haiku`, `inherit` |
| Icons in frontmatter | `icon: 📝` | Put icon in H1: `# 📝 Title` |
| No description | Autocomplete shows filename | Add `description` field |

## Best Practices

### 1. Keep Commands Focused

Each command should do ONE thing well:

**Good:**
```markdown
---
description: Generate JSDoc comments for functions
---
```

**Bad:**
```markdown
---
description: Generate docs, fix linting, add tests, refactor code
---
```

### 2. Use Clear Descriptions

Make descriptions specific and actionable:

**Good:**
```yaml
description: Generate comprehensive JSDoc documentation for selected code
```

**Bad:**
```yaml
description: Make docs
```

### 3. Specify Tool Permissions

Only request tools actually needed:

**Good:**
```yaml
allowed-tools: Read, Edit
```

**Bad:**
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
```

### 4. Document Expected Arguments

Use `argument-hint` to show expected arguments:

```yaml
argument-hint: [file-path]
```

```yaml
argument-hint: <feature-name>
```

```yaml
argument-hint: add [item] | remove [item] | list
```

### 5. Include Usage Examples

Show users how to invoke the command:

```markdown
## Usage

- `/generate-docs path/to/file.ts` - Generate docs for specific file
- `/generate-docs` - Generate docs for current selection
```

### 6. Specify Output Format

Tell Claude what format you want:

```markdown
## Output Format

Generate TypeScript interfaces with JSDoc comments:

```typescript
/**
 * User account information
 */
interface User {
  /** Unique identifier */
  id: string;
  /** User email address */
  email: string;
}
```
```

### 7. Add Examples to Prompt

Show Claude examples of good output:

```markdown
## Example

Good documentation:

```typescript
/**
 * Calculates total price with tax
 * @param price - Base price before tax
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @returns Total price including tax
 */
function calculateTotal(price: number, taxRate: number): number {
  return price * (1 + taxRate);
}
```
```

### 8. Use Icons for Visual Identification

Add emoji to H1 heading for quick recognition:

```markdown
# 📝 Documentation Generator
# 🔍 Code Reviewer
# 🧪 Test Generator
# 🔧 Refactoring Assistant
# 🐛 Bug Finder
```

### Namespaced Commands

Organize related commands using subdirectories:

**File:** `.claude/commands/git/status.md`
```markdown
---
description: Show enhanced git status
allowed-tools: Bash(git *)
---

# Git Status

!`git status`

Branch: !`git branch --show-current`
Recent commits: !`git log --oneline -3`
```
**Invoke with:** `/git.status`

**File:** `.claude/commands/git/quick-commit.md`
```markdown
---
description: Quick commit with conventional format
argument-hint: <type> <message>
allowed-tools: Bash(git *)
---

# Quick Commit

Create conventional commit: $1($2): $ARGUMENTS

!`git add -A && git commit -m "$1: $ARGUMENTS"`
```
**Invoke with:** `/git.quick-commit feat "add user auth"`

## Common Patterns

### Code Review Command

```markdown
---
description: Review code for quality, security, and performance issues
allowed-tools: Read, Grep
---

# 🔍 Code Reviewer

Review the selected code or current file for:

## Code Quality
- Clean, readable code
- Proper naming conventions
- DRY principle adherence
- SOLID principles

## Security
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization

## Performance
- Inefficient algorithms
- Unnecessary computations
- Memory leaks
- Database query optimization

## Output Format

Provide specific file:line references for all issues:

**[Issue Type]** (file.ts:42) - Issue description and suggested fix
```

### Documentation Generator

```markdown
---
description: Generate comprehensive documentation for selected code
allowed-tools: Read, Edit
model: sonnet
---

# 📝 Documentation Generator

Generate comprehensive documentation for the selected code.

## Instructions

- Analyze code structure and purpose
- Generate clear, concise documentation
- Include parameter descriptions with types
- Add usage examples
- Follow JSDoc/TSDoc format for TypeScript
- Document error conditions and edge cases

## Output Format

Return formatted documentation ready to paste above the code.

For TypeScript/JavaScript:
```typescript
/**
 * Function description
 * @param {Type} paramName - Parameter description
 * @returns {ReturnType} Return value description
 * @throws {ErrorType} Error conditions
 */
```
```

### Test Generator

```markdown
---
description: Generate test cases for selected code
allowed-tools: Read, Write
---

# 🧪 Test Generator

Generate comprehensive test cases for the selected code.

## Test Coverage

Create tests covering:
- Happy path scenarios
- Edge cases
- Error conditions
- Boundary values
- Invalid input handling

## Structure

Follow the project's testing conventions:
- Use existing test framework (Jest, Mocha, etc.)
- Match naming patterns
- Follow setup/teardown patterns
- Use appropriate matchers

## Example

```typescript
describe('calculateTotal', () => {
  it('should calculate total with valid inputs', () => {
    const result = calculateTotal(100, 0.08);
    expect(result).toBe(108);
  });

  it('should handle zero tax rate', () => {
    const result = calculateTotal(100, 0);
    expect(result).toBe(100);
  });

  it('should throw for negative price', () => {
    expect(() => calculateTotal(-100, 0.08)).toThrow();
  });
});
```
```

### Git Workflow Command

```markdown
---
description: Create and push feature branch
argument-hint: <feature-name>
allowed-tools: Bash(git *)
---

# 🌿 Feature Branch Creator

Create and push a new feature branch.

## Process

1. Create branch: `feature/$1`
2. Switch to new branch
3. Push to origin with upstream tracking

## Usage

```bash
/feature user-authentication
/feature api-optimization
```

## Implementation

```bash
git checkout -b feature/$1
git push -u origin feature/$1
```
```

### Refactoring Command

```markdown
---
description: Refactor code while preserving behavior
allowed-tools: Read, Edit, Bash
---

# 🔧 Refactoring Assistant

Refactor the selected code while maintaining functionality.

## Guidelines

- Preserve existing behavior exactly
- Improve code structure and readability
- Extract reusable functions
- Reduce complexity
- Follow project conventions
- Update related tests

## Process

1. Read and understand current implementation
2. Identify refactoring opportunities
3. Propose changes with explanations
4. Update code with improvements
5. Verify tests still pass
6. Update documentation if needed

## Safety

- Run tests after refactoring
- Commit changes incrementally
- Keep changes focused and atomic
```

## Validation Checklist

Before finalizing a slash command:

- [ ] Command name is clear and concise
- [ ] Description is specific and actionable
- [ ] Argument hints provided if arguments expected
- [ ] Tool permissions are minimal and specific
- [ ] Model selection appropriate for task complexity
- [ ] Frontmatter uses correct field names
- [ ] Frontmatter values match allowed types
- [ ] `allowed-tools` is comma-separated string, not array
- [ ] H1 title includes icon (optional but recommended)
- [ ] Instructions are clear and actionable
- [ ] Expected output format is specified
- [ ] Examples included in prompt
- [ ] File saved to `.claude/commands/*.md`
- [ ] Command tested and working

## Related Documentation

- **Schema:** https://github.com/pr-pm/prpm/blob/main/packages/converters/schemas/claude-slash-command.schema.json
- **Claude Docs:** https://docs.claude.com/claude-code
- **PRPM Docs:** /Users/khaliqgant/Projects/prpm/app/packages/converters/docs/claude.md
