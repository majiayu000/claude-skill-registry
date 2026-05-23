---
name: claude-command-builder
description: Interactive slash command creator for Claude Code. Triggers when user mentions creating commands, slash commands, command templates, command arguments, or wants to build a new command workflow.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Claude Code Command Builder

## Purpose

Guide users through creating effective Claude Code slash commands with proper structure, argument handling, and workflow design. Auto-invokes when users want to create or modify custom commands.

## When to Use

Auto-invoke when users mention:
- **Creating commands** - "create command", "make command", "new slash command"
- **Command structure** - "command template", "command format", "command frontmatter"
- **Arguments** - "$ARGUMENTS", "$1", "$2", "command parameters", "positional args"
- **Workflows** - "command workflow", "command steps", "command process"
- **Bash execution** - "!`command`", "execute bash in command", "command with bash"

## Knowledge Base

- Official docs: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_slash-commands.md`
- Project guide: `.claude/docs/creating-components.md`
- Examples in repository: `.claude/commands/`

## Process

### 1. Gather Requirements

Ask the user:

```
Let me help you create a Claude Code slash command! I need a few details:

1. **Command name** (lowercase-with-hyphens):
   Example: deploy, review-pr, commit, analyze-tokens
   This will be invoked as: /your-command-name

2. **What does this command do?**
   Describe the workflow in 1-2 sentences.

3. **Does it need arguments?**
   - None (simple prompt)
   - All arguments: $ARGUMENTS
   - Positional: $1, $2, $3, etc.

4. **Does it need bash execution?**
   Commands that run before the slash command (e.g., !`git status`)

5. **Scope:**
   - Personal (`~/.claude/commands/`) - just for you
   - Project (`.claude/commands/`) - shared with team

6. **Namespace/subdirectory?**
   Example: git/, deploy/, testing/
   Helps organize related commands
```

### 2. Validate Input

Check the command name:
- Must be valid filename (no spaces, special chars except hyphen)
- Descriptive and memorable
- Won't conflict with built-in commands
- Use hyphens (not underscores)

Validate arguments:
- Define expected arguments
- Provide defaults if needed
- Document argument order

### 3. Determine Command Type

**Simple Prompt (no frontmatter):**
```markdown
Analyze this code for performance issues and suggest optimizations.
```

**With Arguments:**
```markdown
---
argument-hint: [file-path]
description: Analyze file for performance issues
---

Analyze the file at $1 for performance issues and suggest optimizations.
```

**With Bash Execution:**
```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
description: Create a git commit
---

## Current State

- Git status: !`git status`
- Staged changes: !`git diff --staged`
- Recent commits: !`git log --oneline -5`

## Your Task

Based on the above changes, create a git commit with a clear, conventional commit message.
```

**Full-Featured:**
```markdown
---
allowed-tools: Bash(npm run:*), Bash(git add:*), Bash(git commit:*)
argument-hint: [component-name]
description: Create a new React component with tests
model: sonnet
---

# Create React Component

Component name: $1

Execute the following workflow:

1. **Validate Input**
   !`test -n "$1" && echo "Creating component: $1" || echo "Error: Component name required"`

2. **Check Existing Files**
   !`ls src/components/$1.tsx 2>/dev/null || echo "Component does not exist"`

3. **Create Files**
   Create the following files:
   - `src/components/$1.tsx`
   - `src/components/$1.test.tsx`
   - `src/components/$1.module.css`

4. **Run Tests**
   After creation, run: !`npm run test -- $1`
```

### 4. Generate Command File

Create command structure based on complexity:

**Template for Simple Command:**
```markdown
Brief description of what the command does.

[Prompt instructions for Claude]
```

**Template for Command with Frontmatter:**
```markdown
---
argument-hint: [arg1] [arg2]
description: Brief description shown in /help
allowed-tools: Bash(command:*), Read, Write
model: sonnet
disable-model-invocation: false
---

# Command Name

Usage: /command-name [args]

[Detailed instructions]
```

### 5. Build Command Workflow

Structure the workflow with clear steps:

```markdown
Execute the following workflow:

1. **Step Name**
   ```bash
   # Bash command (if needed)
   command arg1 arg2
   ```
   - What this step does
   - Validation checks
   - Error handling

2. **Next Step**
   [Instructions for Claude]
   - What to check
   - How to proceed
   - What to output

3. **Final Step**
   - Summary of results
   - Next actions for user
   - Success criteria
```

### 6. Add Argument Handling

**All Arguments ($ARGUMENTS):**
```markdown
Fix issue #$ARGUMENTS following our coding standards.
```
User runs: `/fix-issue 123 high-priority`
Becomes: "Fix issue #123 high-priority following our coding standards."

**Positional Arguments ($1, $2, $3):**
```markdown
Review PR #$1 with priority $2 and assign to $3.
Focus on: $4
```
User runs: `/review-pr 456 high alice security`
Becomes individual parameters you can reference separately.

**With Defaults:**
```markdown
---
argument-hint: [environment] [branch]
---

Deploy to environment: ${1:-staging}
From branch: ${2:-main}
```

### 7. Add Bash Execution (if needed)

Use `!` prefix to execute commands before processing:

```markdown
---
allowed-tools: Bash(git:*)
---

## Context

- Current branch: !`git branch --show-current`
- Status: !`git status --short`
- Recent commits: !`git log --oneline -5`

## Your Task

[Instructions based on the above context]
```

**Important:**
- Must specify `allowed-tools` with specific Bash permissions
- Output is included in command context
- Commands run before Claude processes the prompt

### 8. Add File References

Use `@` prefix to reference files:

```markdown
Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js

Analyze all files in @src/components/
```

### 9. Configure Thinking Mode (if needed)

For complex problems, trigger extended thinking:

```markdown
Carefully analyze the following code and think through...

Let's approach this step by step...

Consider all edge cases before implementing...
```

These keywords can trigger extended thinking mode.

### 10. Create the File

Save to correct location:

**Personal command:**
```bash
~/.claude/commands/command-name.md
~/.claude/commands/category/command-name.md  # With namespace
```

**Project command:**
```bash
.claude/commands/command-name.md
.claude/commands/category/command-name.md  # With namespace
```

### 11. Test the Command

Provide testing instructions:

```
To test your command:
1. Restart Claude Code or start a new session
2. Type: /help
3. Find your command in the list
4. Try: /your-command-name [args]
5. Verify it behaves as expected
```

**Test cases:**
```bash
# No arguments
/your-command

# With arguments
/your-command arg1
/your-command arg1 arg2

# Edge cases
/your-command ""
/your-command "with spaces"
```

## Frontmatter Reference

Field| Purpose| Example
---|---|---
`argument-hint`| Show expected arguments in autocomplete| `[pr-number] [priority]`
`description`| Brief description for `/help` menu| `Review pull request`
`allowed-tools`| Tools command can use| `Bash(git:*), Read, Write`
`model`| Specific model to use| `claude-sonnet-4-5-20250929`
`disable-model-invocation`| Prevent SlashCommand tool from calling this| `true`

## Bash Tool Permissions

When using `!` prefix or needing bash execution:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*)
---
```

**Permission patterns:**
- `Bash(git:*)` - All git commands
- `Bash(npm run:*)` - All npm run scripts
- `Bash(git add:*), Bash(git commit:*)` - Specific git commands

## Argument Patterns

### Pattern 1: All Arguments
```markdown
Run tests for: $ARGUMENTS
```
Usage: `/test users api database`
Becomes: "Run tests for: users api database"

### Pattern 2: Positional
```markdown
Deploy $1 to $2 environment with tag $3
```
Usage: `/deploy my-app staging v1.2.3`
Becomes: "Deploy my-app to staging environment with tag v1.2.3"

### Pattern 3: Mixed
```markdown
---
argument-hint: <file> [rest of args]
---

Analyze file $1 for: $ARGUMENTS
```
Usage: `/analyze src/app.js performance security`
Becomes: "Analyze file src/app.js for: src/app.js performance security"
Note: $ARGUMENTS includes all args, so $1 is duplicated

**Better approach:**
```markdown
Analyze file $1 for: ${2:+${@:2}}
```
This uses $1 separately and remaining args starting from $2

### Pattern 4: With Defaults
```markdown
Environment: ${1:-production}
Verbose: ${2:-false}
```

## Command Size Guidelines

- ✅ **Good:** < 100 lines
- ⚠️ **Warning:** 100-150 lines
- ❌ **Too large:** > 250 lines (must refactor)

**If too large:**
- Extract to external script
- Split into multiple commands
- Use sub-commands pattern

## Common Command Types

### 1. Git Workflow
```markdown
---
allowed-tools: Bash(git:*)
description: Create conventional commit
---

## Context
- Status: !`git status --short`
- Diff: !`git diff HEAD`

Create a conventional commit message.
```

### 2. Code Generator
```markdown
---
argument-hint: [component-name]
description: Generate React component
---

Create a new React component named $1:
- Component file
- Test file
- Storybook story
```

### 3. Analysis Tool
```markdown
---
argument-hint: [file-path]
description: Analyze code complexity
---

Analyze @$1 for:
- Cyclomatic complexity
- Code smells
- Improvement suggestions
```

### 4. Deployment Helper
```markdown
---
allowed-tools: Bash(npm:*), Bash(git:*)
argument-hint: [environment]
description: Deploy to environment
---

Deploy to ${1:-staging}:
1. Run tests: !`npm test`
2. Build: !`npm run build`
3. Deploy: !`npm run deploy:$1`
```

### 5. Documentation Generator
```markdown
---
argument-hint: [file-pattern]
description: Generate API documentation
---

Generate documentation for: $1
Include:
- Function signatures
- Parameters
- Return types
- Examples
```

## Examples from TOON Formatter

**Simple version:**
```markdown
# Convert to TOON

Convert the specified JSON file to TOON v2.0 format with automatic optimization and show token savings.

Usage: /convert-to-toon <file>
```

**Advanced version with bash:**
```markdown
---
allowed-tools: Bash(jq:*), Bash(.claude/skills/toon-formatter/bin/toon:*)
argument-hint: <file> [--delimiter comma|tab|pipe]
description: Convert JSON to TOON format
---

# Convert to TOON

File: $1
Delimiter: ${2:-comma}

1. **Validate**: !`test -f "$1" && jq empty "$1" 2>&1`
2. **Analyze**: !`jq 'if type == "array" then length else 0 end' "$1"`
3. **Convert**: !`.claude/skills/toon-formatter/bin/toon encode "$1"`
4. Show savings comparison
```

## Troubleshooting

### Command Not Found

**Check:**
```bash
# List all commands
ls ~/.claude/commands/*.md
ls .claude/commands/*.md

# Verify filename
ls .claude/commands/your-command.md
```

**Remember:**
- Filename (without `.md`) becomes command name
- Hyphens in filename become hyphens in command
- Case-sensitive on Linux/Mac

### Arguments Not Working

**Debug:**
```markdown
Debug: $ARGUMENTS
Debug $1: "$1"
Debug $2: "$2"
```

Run command and check output to see what's being passed.

### Bash Commands Not Executing

**Check:**
1. `allowed-tools` includes correct Bash permissions
2. Using `!` prefix: `!`command``
3. Backticks are correct: \`command\` not 'command'
4. Command is allowed by permissions

### Command Not in /help

**Possible reasons:**
- File not in correct location
- File doesn't have `.md` extension
- Syntax error in frontmatter
- Need to restart Claude Code

## Best Practices

### DO:
✅ Provide clear argument hints
✅ Include usage examples
✅ Handle errors gracefully
✅ Show progress for long operations
✅ Document expected behavior
✅ Test with various inputs
✅ Use descriptive command names

### DON'T:
❌ Make commands too complex (>250 lines)
❌ Forget to specify allowed-tools for Bash
❌ Use unclear argument names
❌ Skip error handling
❌ Hardcode values (use arguments)
❌ Forget to test edge cases

## Comparison: Commands vs Skills

**Use Commands when:**
- You want explicit control (manual invocation)
- Simple, repetitive prompts
- Specific workflow steps
- Frequently-used templates

**Use Skills when:**
- Claude should auto-detect need
- Complex, multi-file workflows
- Comprehensive domain knowledge
- Team needs standardized expertise

**Can use both:**
- Command invokes skill explicitly
- Skill activates automatically
- Command provides quick access
- Skill provides deep capability

## Resources

- **Official Command Docs:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_slash-commands.md`
- **Project Component Guide:** `.claude/docs/creating-components.md`
- **Command Examples:** `.claude/commands/` directory
- **Skills vs Commands:** Section in slash-commands.md
