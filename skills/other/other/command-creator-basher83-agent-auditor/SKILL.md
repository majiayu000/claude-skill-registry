---
name: command-creator
description: >
  This skill should be used when the user asks to "create a slash command", "write a command file",
  "add command to plugin", "create /command", "write command frontmatter", "add command arguments",
  "configure command tools", needs guidance on command structure, YAML frontmatter fields
  (description, argument-hint, allowed-tools), markdown command body, or wants to add custom slash
  commands to Claude Code plugins with proper argument handling and tool restrictions.
---

# Command Creator

## Overview

Creates slash commands for Claude Code plugins. Commands are user-invoked prompts that
expand into detailed instructions for Claude.

**When to use:** User wants to create a command, add command to plugin, or needs command structure help.

**References:** See
`plugins/meta/claude-docs/skills/claude-docs/reference/plugins-reference.md` for command specifications.

## Command Structure Requirements

Every command MUST:

1. Be a `.md` file in `commands/` directory
2. Include frontmatter with `description`
3. Contain clear instructions for Claude
4. Use descriptive kebab-case filename
5. Instructions written from Claude's perspective

## Creation Process

### Step 1: Define Command Purpose

Ask the user:

- What should this command do?
- What inputs/context does it need?
- What should Claude produce?

### Step 2: Choose Command Name

Create concise kebab-case name:

- "generate tests" → `generate-tests.md`
- "review pr" → `review-pr.md`
- "deploy app" → `deploy-app.md`

Name becomes the command: `/generate-tests`

### Step 3: Write Frontmatter

Required frontmatter:

```markdown
---
description: Brief description of what command does
---
```

### Step 4: Write Instructions

Write clear instructions for Claude:

```markdown
# Command Title

Detailed instructions telling Claude exactly what to do when this command is invoked.

## Steps

1. First action Claude should take
2. Second action
3. Final action

## Output Format

Describe how Claude should present results.

## Examples

Show example scenarios if helpful.
```

### Step 5: Verify Against Official Docs

Check
`plugins/meta/claude-docs/skills/claude-docs/reference/plugins-reference.md` for command specifications.

## Key Principles

- **Clarity**: Instructions must be unambiguous
- **Completeness**: Include all steps Claude needs
- **Perspective**: Write as if instructing Claude directly
- **Frontmatter**: Always include description

## Examples

### Example 1: Test Generator Command

User: "Create command to generate tests for a file"

Command file `commands/generate-tests.md`:

```markdown
---
description: Generate comprehensive tests for a source file
---

# Generate Tests

Generate test cases for the file provided by the user.

## Process

1. Read and analyze the source file
2. Identify testable functions and methods
3. Determine test scenarios (happy path, edge cases, errors)
4. Write tests using the project's testing framework
5. Ensure tests are comprehensive and follow best practices

## Test Structure

- One test file per source file
- Clear test names describing what's tested
- Arrange-Act-Assert pattern
- Cover edge cases and error conditions

## Output

Present the generated tests and explain coverage.
```

Invoked with: `/generate-tests`

### Example 2: PR Review Command

User: "Create command for reviewing pull requests"

Command file `commands/review-pr.md`:

```markdown
---
description: Conduct thorough code review of a pull request
---

# Review PR

Review the specified pull request for code quality, correctness, and best practices.

## Review Process

1. Fetch PR changes using git or gh CLI
2. Analyze changed files for:
   - Code correctness and logic errors
   - Style and formatting issues
   - Test coverage
   - Documentation completeness
   - Security concerns
   - Performance implications
3. Provide structured feedback

## Feedback Format

**Summary**: Brief overview of PR

**Strengths**: What's done well

**Issues**: Categorized by severity
- Critical: Must fix
- Important: Should fix
- Minor: Nice to have

**Suggestions**: Specific improvements with examples

## Usage

`/review-pr <pr-number>` or provide PR URL
```

Invoked with: `/review-pr 123`
