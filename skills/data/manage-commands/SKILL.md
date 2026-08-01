---
name: manage-commands
description: 'MUST INVOKE this skill when creating custom slash commands, standardizing
  workflows, or adding reusable operations. Secondary: understanding command structure,
  learning YAML configuration, or optimizi'
---

---
name: manage-commands
description: MUST INVOKE this skill when creating custom slash commands, standardizing workflows, or adding reusable operations. Secondary: understanding command structure, learning YAML configuration, or optimizing existing commands. Create, audit, and maintain custom slash commands.
---

# Objective

Create effective slash commands for Claude Code that enable users to trigger reusable prompts with `/command-name` syntax. Slash commands expand as prompts in the current conversation, allowing teams to standardize workflows and operations. This skill teaches you to structure commands with XML tags, YAML frontmatter, dynamic context loading, and intelligent argument handling.

# Quick Start

## Workflow

1. Create `.claude/commands/` directory in project (for portability)
2. Create `command-name.md` file
3. Add YAML frontmatter (at minimum: `description`)
4. Write 1-2 line instruction (no sections)
5. Test with `/command-name [args]`

**Note**: Use `~/.claude/commands/` (personal) only if specifically requested for global availability.

## Ultra-Minimalist Pattern

**File**: `.claude/commands/optimize.md`

```markdown
---
description: Shortcut to invoke the engineering skill for performance optimization
argument-hint: [file-path]
---

Invoke the `engineering` skill (optimization workflow) to optimize: $ARGUMENTS
```

**Usage**: `/optimize src/utils/helpers.js`

## Command Types

**Verbs** (Load skills): "Invoke the `{skill}` skill..."
**Personas** (Delegate to agents): "Task the `{agent}` agent with..."
**Objects** (Lifecycle): "Invoke the `{skill}` skill to..."
**Execution** (Run artifacts): "Execute {artifact-type}..."

See references/semantic-categories.md for detailed patterns.

# Workflows

## Create New Command

Use the [create-new-command workflow](workflows/create-new-command.md) to create ultra-minimalist slash commands following Cat Toolkit best practices:

- Determines semantic category (Verbs/Personas/Objects/Execution)
- Creates ultra-minimalist command structure (1-2 lines max)
- Uses soft, human-friendly descriptions
- Follows semantic naming patterns

## Create New Command (Advanced)

For complex commands requiring dynamic context, tool restrictions, or multi-step workflows, use the advanced patterns in the [command-patterns reference](references/patterns.md).

## Audit Existing Command

To audit an existing slash command for best practices compliance:

```
Audit the command at: [path-to-command-file]
```

Use the [audit workflow](workflows/audit.md) to evaluate:
- YAML frontmatter quality (description, allowed-tools, argument-hint)
- Argument usage and integration ($ARGUMENTS, $1/$2/$3)
- Security configuration (tool restrictions, destructive operation handling)
- Dynamic context patterns and file references
- Contextual judgment based on command complexity

# Markdown Structure

All generated slash commands should use Markdown headings in the body (after YAML frontmatter) for clarity and consistency.

## Required Sections

**`## Objective`** - What the command does and why it matters

```markdown
## Objective
What needs to happen and why this matters.
Context about who uses this and what it accomplishes.
```

**`## Process` or `## Steps`** - How to execute the command

```markdown
## Process
Sequential steps to accomplish the objective:
1. First step
2. Second step
3. Final step
```

**`## Success Criteria`** - How to know the command succeeded

```markdown
## Success Criteria
Clear, measurable criteria for successful completion.
```

## Conditional Sections

**`## Context`** - When loading dynamic state or files

```markdown
## Context
Current state: ! `git status`
Relevant files: @ package.json
```

(Note: Remove the space after @ in actual usage)

**`## Verification`** - When producing artifacts that need checking

```markdown
## Verification
Before completing, verify:
- Specific test or check to perform
- How to confirm it works
```

**`## Testing`** - When running tests is part of the workflow

```markdown
## Testing
Run tests: ! `npm test`
Check linting: ! `npm run lint`
```

**`## Output`** - When creating/modifying specific files

```markdown
## Output
Files created/modified:
- `./path/to/file.ext` - Description
```

## Structure Example

```markdown
---
name: example-command
description: Does something useful
argument-hint: [input]
---

## Objective
Process $ARGUMENTS to accomplish [goal].

This helps [who] achieve [outcome].

## Context
Current state: ! `relevant command`
Files: @ relevant/files

## Process
1. Parse $ARGUMENTS
2. Execute operation
3. Verify results

## Success Criteria
- Operation completed without errors
- Output matches expected format
```

## Intelligence Rules

**Simple commands** (single operation, no artifacts):

- Required: `## Objective`, `## Process`, `## Success Criteria`
- Example: `/check-todos`, `/first-principles`

**Complex commands** (multi-step, produces artifacts):

- Required: `## Objective`, `## Process`, `## Success Criteria`
- Add: `## Context` (if loading state), `## Verification` (if creating files), `## Output` (what gets created)
- Example: `/commit`, `/create-prompt`, `/run-prompt`

**Commands with dynamic arguments**:

- Use `$ARGUMENTS` in `## Objective` or `## Process` sections
- Include `argument-hint` in frontmatter
- Make it clear what the arguments are for

**Commands that produce files**:

- Always include `## Output` section specifying what gets created
- Always include `## Verification` section with checks to perform

**Commands that run tests/builds**:

- Include `## Testing` section with specific commands
- Include pass/fail criteria in `## Success Criteria`

# Arguments Intelligence

The skill should intelligently determine whether a slash command needs arguments.

## Commands That Need Arguments

**User provides specific input:**

- `/fix-issue [issue-number]` - Needs issue number
- `/review-pr [pr-number]` - Needs PR number
- `/optimize [file-path]` - Needs file to optimize
- `/commit [type]` - Needs commit type (optional)

**Pattern:** Task operates on user-specified data

Include `argument-hint: [description]` in frontmatter and reference `$ARGUMENTS` in the body.

## Commands Without Arguments

**Self-contained procedures:**

- `/check-todos` - Operates on known file (TO-DOS.md)
- `/first-principles` - Operates on current conversation
- `/whats-next` - Analyzes current context

**Pattern:** Task operates on implicit context (current conversation, known files, project state)

Omit `argument-hint` and don't reference `$ARGUMENTS`.

## Incorporating Arguments

**In `## Objective` section:**

```markdown
## Objective
Fix issue #$ARGUMENTS following project conventions.

This ensures bugs are resolved systematically with proper testing.
```

**In `## Process` section:**

```markdown
## Process
1. Understand issue #$ARGUMENTS from issue tracker
2. Locate relevant code
3. Implement fix
4. Add tests
```

**In `## Context` section:**

```markdown
## Context
Issue details: @ issues/$ARGUMENTS.md
Related files: ! `grep -r "TODO.*$ARGUMENTS" src/`
```

(Note: Remove the space after the exclamation mark in actual usage)

## Positional Arguments

For structured input, use `$1`, `$2`, `$3`:

```markdown
---
argument-hint: <pr-number> <priority> <assignee>
---

## Objective
Review PR #$1 with priority $2 and assign to $3.
```

**Usage:** `/review-pr 456 high alice`

# File Structure

**Project commands** (default, recommended): `.claude/commands/`

- Shared with team via version control
- Shows `(project)` in `/help` list
- Portable with the project

**Personal commands** (only if specifically requested): `~/.claude/commands/`

- Available across all your projects
- Shows `(user)` in `/help` list
- Use only for globally useful commands

**File naming**: `command-name.md` → invoked as `/command-name`

# YAML Frontmatter

## description

**Required** - Describes what the command does

```yaml
description: Analyze this code for performance issues and suggest optimizations
```

Shown in the `/help` command list.

## allowed-tools

**Optional** - Restricts which tools Claude can use

```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

**Formats**:

- Array: `allowed-tools: [Read, Edit, Write]`
- Single tool: `allowed-tools: SequentialThinking`
- Bash restrictions: `allowed-tools: Bash(git add:*)`

If omitted: All tools available

# Arguments

## All Arguments String

**Command file**: `.claude/commands/fix-issue.md`

```markdown
---
description: Fix issue following coding standards
---

Fix issue #$ARGUMENTS following our coding standards
```

**Usage**: `/fix-issue 123 high-priority`

**Claude receives**: "Fix issue #123 high-priority following our coding standards"

## Positional Arguments Syntax

**Command file**: `.claude/commands/review-pr.md`

```markdown
---
description: Review PR with priority and assignee
---

Review PR #$1 with priority $2 and assign to $3
```

**Usage**: `/review-pr 456 high alice`

**Claude receives**: "Review PR #456 with priority high and assign to alice"

See references/arguments.md for advanced patterns.

# Dynamic Context

Execute bash commands before the prompt using the exclamation mark prefix directly before backticks (no space between).

**Note:** Examples below show a space after the exclamation mark to prevent execution during skill loading. In actual slash commands, remove the space.

Example:

```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context

- Current git status: ! `git status`
- Current git diff: ! `git diff HEAD`
- Current branch: ! `git branch --show-current`
- Recent commits: ! `git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

The bash commands execute and their output is included in the expanded prompt.

# File References

Use `@` prefix to reference specific files:

```markdown
---
description: Review implementation
---

Review the implementation in @ src/utils/helpers.js
```

(Note: Remove the space after @ in actual usage)

Claude can access the referenced file's contents.

# Best Practices

**1. Always use Markdown structure**

After frontmatter, use Markdown headings:

- `## Objective` - What and why (always)
- `## Process` - How to do it (always)
- `## Success Criteria` - Definition of done (always)
- Additional sections as needed (see XML Structure section)

**2. Clear descriptions**

Good:

```yaml
description: Analyze this code for performance issues and suggest optimizations
```

Bad:

```yaml
description: Optimize stuff
```

**3. Use dynamic context for state-dependent tasks**

```markdown
Current git status: ! `git status`
Files changed: ! `git diff --name-only`
```

**4. Restrict tools when appropriate**

For git commands - prevent running arbitrary bash:

```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

For analysis - thinking only:

```yaml
allowed-tools: SequentialThinking
```

**5. Use $ARGUMENTS for flexibility**

```markdown
Find and fix issue #$ARGUMENTS
```

**6. Reference relevant files**

```markdown
Review @ package.json for dependencies
Analyze @ src/database/* for schema
```

(Note: Remove the space after @ in actual usage)

# Common Patterns

## Simple Analysis Command

```markdown
---
description: Review this code for security vulnerabilities
---

## Objective
Review code for security vulnerabilities and suggest fixes.

## Process
1. Scan code for common vulnerabilities (XSS, SQL injection, etc.)
2. Identify specific issues with line numbers
3. Suggest remediation for each issue

## Success Criteria
- All major vulnerability types checked
- Specific issues identified with locations
- Actionable fixes provided
```

## Git Workflow with Context

```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Objective
Create a git commit for current changes following repository conventions.

## Context
- Current status: ! `git status`
- Changes: ! `git diff HEAD`
- Recent commits: ! `git log --oneline -5`

## Process
1. Review staged and unstaged changes
2. Stage relevant files
3. Write commit message following recent commit style
4. Create commit

## Success Criteria
- All relevant changes staged
- Commit message follows repository conventions
- Commit created successfully
```

## Parameterized Command

```markdown
---
description: Fix issue following coding standards
argument-hint: [issue-number]
---

## Objective
Fix issue #$ARGUMENTS following project coding standards.

This ensures bugs are resolved systematically with proper testing.

## Process
1. Understand the issue described in ticket #$ARGUMENTS
2. Locate the relevant code in codebase
3. Implement a solution that addresses root cause
4. Add appropriate tests
5. Verify fix resolves the issue

## Success Criteria
- Issue fully understood and addressed
- Solution follows coding standards
- Tests added and passing
- No regressions introduced
```

## File-Specific Command

```markdown
---
description: Optimize code performance
argument-hint: [file-path]
---

## Objective
Analyze performance of @ $ARGUMENTS and suggest specific optimizations.

This helps improve application performance through targeted improvements.

## Process
1. Review code in @ $ARGUMENTS for performance issues
2. Identify bottlenecks and inefficiencies
3. Suggest three specific optimizations with rationale
4. Estimate performance impact of each

## Success Criteria
- Performance issues clearly identified
- Three concrete optimizations suggested
- Implementation guidance provided
- Performance impact estimated
```

**Usage**: `/optimize src/utils/helpers.js`

See references/patterns.md for more examples.

# Reference Guides

**Arguments reference**: references/arguments.md

- $ARGUMENTS variable
- Positional arguments ($1, $2, $3)
- Parsing strategies
- Examples from official docs

**Patterns reference**: references/patterns.md

- Git workflows
- Code analysis
- File operations
- Security reviews
- Examples from official docs

**Tool restrictions**: references/tool-restrictions.md

- Bash command patterns
- Security best practices
- When to restrict tools
- Examples from official docs

# Generation Protocol

1. **Analyze the user's request**:
   - What is the command's purpose?
   - Does it need user input ($ARGUMENTS)?
   - Does it produce files or artifacts?
   - Does it require verification or testing?
   - Is it simple (single-step) or complex (multi-step)?

2. **Create frontmatter**:

   ```yaml
   ---
   name: command-name
   description: Clear description of what it does
   argument-hint: [input] # Only if arguments needed
   allowed-tools: [...] # Only if tool restrictions needed
   ---
   ```

3. **Create Markdown-structured body**:

   **Always include:**
   - `## Objective` - What and why
   - `## Process` - How to do it (numbered steps)
   - `## Success Criteria` - Definition of done

   **Include when relevant:**
   - `## Context` - Dynamic state (! `commands`) or file references (@ files)
   - `## Verification` - Checks to perform if creating artifacts
   - `## Testing` - Test commands if tests are part of workflow
   - `## Output` - Files created/modified

4. **Integrate $ARGUMENTS properly**:
   - If user input needed: Add `argument-hint` and use `$ARGUMENTS` in tags
   - If self-contained: Omit `argument-hint` and `$ARGUMENTS`

5. **Apply intelligence**:
   - Simple commands: Keep it concise (Objective + Process + Success Criteria)
   - Complex commands: Add Context, Verification, Testing as needed
   - Don't over-engineer simple commands
   - Don't under-specify complex commands

6. **Save the file**:
   - **Default**: `.claude/commands/command-name.md` (project, portable)
   - **Alternative**: `~/.claude/commands/command-name.md` (only if specifically requested)

# Success Criteria

A well-structured slash command meets these criteria:

## YAML Frontmatter

- `description` field is clear and concise
- `argument-hint` present if command accepts arguments
- `allowed-tools` specified if tool restrictions needed

## Structure

- All three required sections present: `## Objective`, `## Process`, `## Success Criteria`
- Conditional sections used appropriately based on complexity
- Proper markdown heading hierarchy maintained
- All sections properly formatted

## Arguments Handling

- `$ARGUMENTS` used when command operates on user-specified data
- Positional arguments (`$1`, `$2`, etc.) used when structured input needed
- No `$ARGUMENTS` reference for self-contained commands

## Functionality

- Command expands correctly when invoked
- Dynamic context loads properly (bash commands, file references)
- Tool restrictions prevent unauthorized operations
- Command accomplishes intended purpose reliably

## Quality

- Clear, actionable instructions in `## Process` section
- Measurable completion criteria in `## Success Criteria`
- Appropriate level of detail (not over-engineered for simple tasks)
- Examples provided when beneficial
