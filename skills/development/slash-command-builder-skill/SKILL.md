---
name: slash-command-builder
description: Use when creating, improving, or troubleshooting Claude Code slash commands. Expert guidance on command structure, arguments, frontmatter, tool permissions, and best practices for building effective custom commands.
globs:
  - "**/.claude/commands/**/*.md"
  - "**/.claude/commands/**/*.markdown"
alwaysApply: false
---

# Slash Command Builder - Claude Code Command Expert

Use this skill when creating, improving, or troubleshooting Claude Code slash commands. Provides expert guidance on command structure, syntax, frontmatter configuration, and best practices.

## When to Use This Skill

Activate this skill when:
- User asks to create a new slash command
- User wants to improve an existing command
- User needs help with command arguments or frontmatter
- User is troubleshooting command invocation issues
- User wants to understand slash command capabilities
- User asks about the difference between commands and skills

## Quick Reference

### Command File Structure

```markdown
---
description: Brief description shown in autocomplete
argument-hint: [arg1] [arg2] <optional-arg>
allowed-tools: Bash(git *), Read, Write
model: claude-3-5-sonnet-20241022
disable-model-invocation: false
---

Your command prompt here with $ARGUMENTS or $1, $2, etc.

Use !`command` for bash execution
Use @file.txt for file references
```

### File Locations

**Project commands** (shared with team):
```
.claude/commands/my-command.md
```

**Personal commands** (individual use):
```
~/.claude/commands/my-command.md
```

**Organized commands** (namespaced):
```
.claude/commands/frontend/component.md  → /component (project:frontend)
```

## Creating Effective Slash Commands

### Step 1: Identify the Use Case

**Good candidates for slash commands:**
- Frequently repeated prompts
- Simple, single-purpose tasks
- Quick code reviews or analyses
- Common git workflows
- Standard documentation tasks

**NOT good for slash commands (use Skills instead):**
- Complex multi-step workflows
- Context-aware behavior
- Team standardization needs
- Workflows requiring multiple files

### Step 2: Choose Command Name

**Best practices:**
- Use lowercase with hyphens: `/review-pr`, `/optimize-code`
- Make it memorable and intuitive
- Avoid conflicts with built-in commands
- Keep it short (2-3 words max)

**Examples:**
- ✅ `/review-pr` - Clear, concise
- ✅ `/fix-lint` - Action-oriented
- ❌ `/review-pull-request-thoroughly` - Too verbose
- ❌ `/rpr` - Too cryptic

### Step 3: Design the Prompt

**Simple command (no arguments):**
```markdown
---
description: Analyze code for performance bottlenecks
---

Analyze the current file for performance issues:
1. Identify O(n²) or worse algorithms
2. Find unnecessary re-renders or computations
3. Check for memory leaks
4. Suggest optimizations with code examples
```

**Command with all arguments:**
```markdown
---
description: Generate component boilerplate
argument-hint: <component-name> <type>
---

Create a $ARGUMENTS component following our style guide:
- Use TypeScript with strict types
- Include prop interfaces
- Add JSDoc comments
- Export as default
```

**Command with positional arguments:**
```markdown
---
description: Review pull request
argument-hint: [pr-number] [reviewer]
---

Review PR #$1 and assign to @$2:
1. Check code quality and style
2. Verify tests are included
3. Look for security issues
4. Suggest improvements
5. Add comments in GitHub
```

### Step 4: Add Frontmatter Configuration

See `FRONTMATTER.md` in this skill directory for complete frontmatter options.

**Minimal frontmatter:**
```yaml
---
description: What this command does
---
```

**Full-featured frontmatter:**
```yaml
---
description: Complete command with all options
argument-hint: [required] <optional>
allowed-tools: Bash(git *), Read(**/*.ts), Write
model: claude-3-5-sonnet-20241022
disable-model-invocation: false
---
```

### Step 5: Test the Command

1. Save the file to `.claude/commands/`
2. Invoke with `/command-name`
3. Check argument substitution works
4. Verify tool permissions if using `allowed-tools`
5. Test edge cases (missing args, wrong types)

## Advanced Features

### Bash Execution

Execute shell commands inline with `!` prefix:

```markdown
---
description: Show git status
allowed-tools: Bash(git status:*)
---

Current repository status:

!`git status`

Recent commits:

!`git log --oneline -5`
```

### File References

Include file contents with `@` prefix:

```markdown
---
description: Review specific file
argument-hint: <file-path>
---

Review this file for code quality:

@$1

Focus on:
- Type safety
- Error handling
- Performance
- Maintainability
```

### Tool Permissions

Restrict which tools Claude can use:

```markdown
---
description: Safe git status check
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

Show current changes:

!`git status`
!`git diff --stat`
```

**Tool permission syntax:**
- `Bash(command:*)` - Allow specific command with any args
- `Read(path/to/*.ts)` - Allow reading TypeScript files in path
- `Write` - Allow writing any file
- `Glob`, `Grep`, `Edit` - Other available tools

### Model Selection

Override default model for specific commands:

```markdown
---
description: Quick syntax fix
model: claude-3-5-haiku-20241022
---

Fix syntax errors in the current file quickly.
```

**When to use different models:**
- `claude-3-5-haiku-20241022` - Fast, simple tasks
- `claude-3-5-sonnet-20241022` - General purpose (default)
- `claude-opus-4-20250514` - Complex reasoning

### Disable Auto-Invocation

Prevent Claude from calling command automatically:

```markdown
---
description: Destructive operation
disable-model-invocation: true
---

!`rm -rf node_modules`
!`npm install`
```

## Common Patterns

### Code Review Command

```markdown
---
description: Review code changes
argument-hint: [file-or-pr]
allowed-tools: Bash(git *), Read, Grep
---

Review $ARGUMENTS for:

1. **Code Quality**
   - Clean, readable code
   - Proper naming conventions
   - DRY principle

2. **Security**
   - Input validation
   - SQL injection risks
   - XSS vulnerabilities

3. **Performance**
   - Inefficient algorithms
   - Unnecessary computations
   - Memory leaks

4. **Tests**
   - Unit test coverage
   - Edge cases handled
   - Integration tests

Provide specific file:line references for all issues.
```

### Git Workflow Command

```markdown
---
description: Create feature branch
argument-hint: <feature-name>
allowed-tools: Bash(git *)
---

Create and switch to feature branch:

!`git checkout -b feature/$1`
!`git push -u origin feature/$1`

Branch feature/$1 created and pushed to origin.
```

### Documentation Generator

```markdown
---
description: Generate API docs
argument-hint: <file-path>
allowed-tools: Read
---

Generate comprehensive API documentation for:

@$1

Include:
- Function signatures with types
- Parameter descriptions
- Return value documentation
- Usage examples
- Error cases
```

### Test Generator

```markdown
---
description: Generate test cases
argument-hint: <file-to-test>
allowed-tools: Read, Write
---

Generate test cases for:

@$1

Create tests covering:
- Happy path scenarios
- Edge cases
- Error conditions
- Boundary values

Use the existing test framework style.
```

## Troubleshooting

### Command Not Found

**Problem:** `/my-command` doesn't autocomplete

**Solutions:**
1. Check file is in `.claude/commands/` or `~/.claude/commands/`
2. Verify filename matches command (`.claude/commands/my-command.md`)
3. Restart Claude Code to reload commands
4. Check for syntax errors in frontmatter

### Arguments Not Substituting

**Problem:** `$1` appears literally instead of being replaced

**Solutions:**
1. Ensure arguments are passed: `/command arg1 arg2`
2. Check you're using `$1`, `$2` (not `${1}`)
3. For all args, use `$ARGUMENTS` instead
4. Verify `argument-hint` frontmatter is correct

### Tool Permission Denied

**Problem:** Command can't execute bash or read files

**Solutions:**
1. Add `allowed-tools` frontmatter
2. Use specific tool patterns: `Bash(git *)`
3. Check tool name capitalization (e.g., `Bash`, not `bash`)
4. For file operations, use glob patterns: `Read(**/*.ts)`

### Command Invokes at Wrong Time

**Problem:** Claude calls command when you don't want it to

**Solutions:**
1. Add `disable-model-invocation: true` to frontmatter
2. Ensure `description` is specific to avoid false triggers
3. Use more explicit command names

## Commands vs. Skills

### Use Slash Commands When:
- ✅ Task is simple and focused
- ✅ Prompt fits in one Markdown file
- ✅ Need quick, explicit invocation
- ✅ Personal productivity shortcuts

### Use Skills When:
- ✅ Complex, multi-step workflows
- ✅ Context-aware automatic activation
- ✅ Team needs standardization
- ✅ Multiple supporting files needed
- ✅ Sophisticated conditional logic

**Example:**
- **Command:** `/review-pr` - Quick PR review prompt
- **Skill:** `code-reviewer` - Comprehensive review framework with security.md, performance.md, style.md, and scripts

## Best Practices

### 1. Keep Commands Focused
Each command should do ONE thing well. Don't create Swiss Army knife commands.

### 2. Use Clear Argument Hints
```yaml
argument-hint: [required] <optional> [choices: a|b|c]
```

### 3. Document Expected Output
Tell Claude what format you want:
```markdown
Generate a JSON response with this structure:
{
  "issues": [],
  "suggestions": []
}
```

### 4. Include Examples
Show Claude what good output looks like:
```markdown
Example output:

## Security Issues
- **SQL Injection** (file.ts:42) - Use parameterized queries
```

### 5. Be Specific with Tool Permissions
Don't use `allowed-tools: Bash` - use `allowed-tools: Bash(git *)`

### 6. Test with Edge Cases
- Missing arguments
- Wrong argument types
- Files that don't exist
- Empty repositories

### 7. Version Control Commands
Store `.claude/commands/` in git for team collaboration

### 8. Organize with Namespaces
Use subdirectories for related commands:
```
.claude/commands/
├── git/
│   ├── feature.md
│   ├── fix.md
│   └── release.md
└── testing/
    ├── unit.md
    └── e2e.md
```

## Related Documentation

- **FRONTMATTER.md** - Complete frontmatter reference
- **EXAMPLES.md** - Real-world command examples
- **PATTERNS.md** - Common command patterns

## Checklist for New Commands

Before finalizing a slash command:

- [ ] Command name is clear and concise
- [ ] Description frontmatter is specific
- [ ] Argument hints are provided if needed
- [ ] Tool permissions are minimal and specific
- [ ] Prompt is focused on one task
- [ ] Examples are included in prompt
- [ ] Expected output format is specified
- [ ] Edge cases are considered
- [ ] Command has been tested
- [ ] File is in correct directory

**Remember:** Great slash commands are simple, focused, and make frequent tasks effortless. If you find yourself adding complexity, consider creating a Skill instead.
