---
name: create-command
description: Guide for creating custom Claude Code slash commands with proper structure, argument handling, frontmatter configuration, and best practices. Use when the user wants to create slash commands, custom commands, reusable prompts, or mentions creating/designing/building commands.
---

# Create Slash Command Guide

This skill helps you create custom Claude Code slash commands - reusable prompts stored as Markdown files that can be invoked with `/command-name` syntax. Slash commands are ideal for frequently-used prompts that you want to trigger explicitly.

## Quick Start

When creating a new slash command, follow this workflow:

1. **Identify the purpose** - What reusable prompt do you need?
2. **Choose scope** - Project-level (.claude/commands/) or personal (~/.claude/commands/)?
3. **Select name** - Clear, descriptive filename without .md extension
4. **Design arguments** - Will it use $ARGUMENTS, $1/$2/$3, or none?
5. **Add frontmatter** - Optional metadata (description, tools, model)
6. **Write prompt** - The markdown content that becomes the prompt
7. **Test invocation** - Verify command works with various arguments

## Basic Syntax

Commands are invoked with:
```
/command-name [arguments]
```

The command name comes from the filename without `.md` extension.

## File Locations

### Project Commands (.claude/commands/)
- **Scope:** Project-specific, shared with team via git
- **Label:** Shows as "(project)" in help listing
- **Use for:** Team workflows, project conventions, shared prompts

```bash
# Create project command
echo "Review this code for security vulnerabilities" > .claude/commands/security-review.md
```

**Example structure:**
```
.claude/commands/
├── review.md           # /review
├── optimize.md         # /optimize
├── test.md            # /test
└── frontend/
    └── component.md   # /component (project:frontend)
```

### Personal Commands (~/.claude/commands/)
- **Scope:** Available across all projects
- **Label:** Shows as "(user)" in help listing
- **Use for:** Personal productivity, individual workflows, cross-project utilities

```bash
# Create personal command
echo "Explain this code in simple terms" > ~/.claude/commands/explain.md
```

**Example structure:**
```
~/.claude/commands/
├── explain.md         # /explain (user)
├── refactor.md        # /refactor (user)
└── snippets/
    └── doc.md         # /doc (user:snippets)
```

## Argument Handling

### No Arguments
Simple commands that don't need input:

```markdown
Review the current codebase for potential improvements and suggest optimizations.
```

Usage: `/review`

### All Arguments with $ARGUMENTS
Captures everything passed to the command:

```markdown
Fix issue #$ARGUMENTS following our coding standards and best practices.
```

Usage:
- `/fix-issue 123`
- `/fix-issue 123 high-priority security`

### Positional Arguments with $1, $2, $3, etc.
Access specific arguments by position:

```markdown
Review PR #$1 with priority $2 and assign to $3 for review.
```

Usage: `/review-pr 456 high alice`

**Benefits:**
- Access arguments in different parts of the prompt
- Provide defaults for missing arguments
- Build structured commands with specific parameter roles
- Clearer intent for multi-parameter commands

### Combining Arguments
Use both positional and all arguments:

```markdown
Create a $1 feature called "$2" with the following requirements:

$ARGUMENTS
```

Usage: `/create-feature backend "user authentication" JWT tokens, role-based access, password hashing`

## Frontmatter Configuration

Add optional metadata at the top of your command file:

```markdown
---
allowed-tools: Read, Write, Edit, Bash
argument-hint: <issue-number> [priority]
description: Fix GitHub issue following coding standards
model: claude-3-5-sonnet-20241022
---

Your command prompt content goes here...
```

### Frontmatter Fields

**allowed-tools:** Restrict which tools Claude can use
```yaml
allowed-tools: Read, Write, Edit, Bash
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

**argument-hint:** Show expected arguments in autocomplete
```yaml
argument-hint: <file-path>
argument-hint: <pr-number> [priority] [assignee]
argument-hint: [message]
```

**description:** Brief command description (overrides first line)
```yaml
description: Create a git commit with proper formatting
```

**model:** Specific model to use for this command
```yaml
model: claude-3-5-haiku-20241022      # Fast, cheap
model: claude-3-5-sonnet-20241022     # Balanced
model: claude-opus-4-20250514         # Advanced
```

**disable-model-invocation:** Prevent auto-invocation via SlashCommand tool
```yaml
disable-model-invocation: true
```

## Advanced Features

### File References with @
Include file contents in your command:

```markdown
---
description: Review code implementation
---

Review the implementation in @src/utils/helpers.js and compare it with @src/utils/legacy.js.

Identify:
- Code quality improvements
- Performance optimizations
- Security vulnerabilities
```

Usage: `/review-implementation`

### Bash Command Execution with !
Execute bash commands and include output (requires allowed-tools):

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

Create a git commit with the following context:

**Current Status:**
!`git status`

**Recent Changes:**
!`git diff HEAD`

**Commit Message:** $ARGUMENTS
```

Usage: `/commit "Add user authentication feature"`

### Extended Thinking
Trigger extended reasoning by including keywords in the command content:

```markdown
---
description: Analyze complex architectural decisions
---

Please use extended thinking to analyze the following architectural decision:

$ARGUMENTS

Consider:
- Scalability implications
- Maintenance overhead
- Team expertise requirements
- Long-term technical debt
```

### Namespacing with Subdirectories
Organize commands in subdirectories (affects description, not command name):

```
.claude/commands/
├── git/
│   ├── commit.md     # /commit (project:git)
│   └── review.md     # /review (project:git)
└── frontend/
    └── component.md  # /component (project:frontend)
```

The subdirectory appears in the description but doesn't change the command invocation.

## Complete Examples

### 1. Simple Code Review Command

**File:** `.claude/commands/review.md`

```markdown
---
description: Comprehensive code review for quality and security
---

Review this code for:
- Code quality and maintainability
- Security vulnerabilities
- Performance optimizations
- Best practices adherence
- Potential bugs or edge cases

Provide specific, actionable feedback with code examples.
```

Usage: `/review`

### 2. Issue Fix Command with Arguments

**File:** `.claude/commands/fix-issue.md`

```markdown
---
argument-hint: <issue-number> [priority]
description: Fix GitHub issue following coding standards
---

Fix issue #$1 following our coding standards.

Priority: $2

Steps:
1. Read the issue details from GitHub
2. Analyze the problem and root cause
3. Implement the fix with tests
4. Update documentation if needed
5. Create a commit with proper message format
```

Usage:
- `/fix-issue 123 high`
- `/fix-issue 456`

### 3. PR Creation with Template

**File:** `.claude/commands/create-pr.md`

```markdown
---
allowed-tools: Bash(git *), Read, Write
argument-hint: <title> [description]
description: Create GitHub pull request with template
model: claude-3-5-sonnet-20241022
---

Create a GitHub pull request with the following details:

**Title:** $1

**Description:** $2

**Context:**

**Current Branch:**
!`git branch --show-current`

**Changes:**
!`git diff main...HEAD --stat`

**Commits:**
!`git log main..HEAD --oneline`

Generate a comprehensive PR description following our template at @.github/pull_request_template.md
```

Usage: `/create-pr "Add user authentication" "Implements JWT-based authentication system"`

### 4. Test Runner Command

**File:** `.claude/commands/test.md`

```markdown
---
allowed-tools: Bash, Read, Grep
argument-hint: [file-pattern]
description: Run tests and analyze failures
model: claude-3-5-haiku-20241022
---

Run tests matching pattern: $ARGUMENTS

Steps:
1. Execute test suite
2. Analyze any failures
3. Suggest fixes for failing tests
4. Validate fixes and re-run

Provide clear, actionable feedback on test failures.
```

Usage:
- `/test`
- `/test auth`
- `/test src/components/Button.test.ts`

### 5. Documentation Generator

**File:** `.claude/commands/document.md`

```markdown
---
allowed-tools: Read, Write, Grep, Glob
description: Generate comprehensive documentation
---

Generate comprehensive documentation for: $ARGUMENTS

Include:
- Overview and purpose
- API reference
- Usage examples
- Configuration options
- Best practices
- Common pitfalls

Format output in clear, professional markdown.
```

Usage: `/document src/utils/api-client.ts`

### 6. Code Optimization Command

**File:** `.claude/commands/optimize.md`

```markdown
---
description: Analyze and optimize code performance
---

Analyze this code for performance optimizations:

$ARGUMENTS

Focus on:
- Algorithm complexity (O(n) analysis)
- Memory usage and allocations
- Database query efficiency
- Caching opportunities
- Parallel processing potential
- Resource cleanup and lifecycle management

Provide specific refactoring suggestions with before/after examples.
```

Usage: `/optimize`

### 7. Multi-Argument PR Review

**File:** `.claude/commands/review-pr.md`

```markdown
---
allowed-tools: Bash(gh *), Read
argument-hint: <pr-number> <priority> [assignee]
description: Review pull request with priority and assignment
---

Review PR #$1 with priority: $2

**PR Details:**
!`gh pr view $1`

**Changes:**
!`gh pr diff $1`

Review focus areas based on priority $2:
- high: Security, breaking changes, data integrity
- medium: Code quality, tests, documentation
- low: Style, minor improvements

Assign to: $3 (if provided)

Provide comprehensive feedback organized by:
1. Critical issues (blocking)
2. Important suggestions
3. Minor improvements
4. Positive observations
```

Usage: `/review-pr 123 high alice`

### 8. Git Workflow Command

**File:** `.claude/commands/git-flow.md`

```markdown
---
allowed-tools: Bash(git *)
argument-hint: <action> <branch-name>
description: Execute git workflow actions
---

Execute git workflow action: $1

Branch: $2

**Current Status:**
!`git status`

**Available Branches:**
!`git branch -a`

Actions:
- start: Create and checkout new branch
- finish: Merge branch and delete
- sync: Pull latest and rebase
- review: Show branch diff

Additional context: $ARGUMENTS
```

Usage:
- `/git-flow start feature/auth`
- `/git-flow finish bugfix/login`
- `/git-flow sync`

### 9. Database Query Optimization

**File:** `~/.claude/commands/optimize-query.md`

```markdown
---
description: Optimize database queries for performance
---

Analyze and optimize this database query:

$ARGUMENTS

Optimization checklist:
- [ ] Execution plan analysis
- [ ] Index usage and recommendations
- [ ] Query rewrite opportunities
- [ ] JOIN optimization
- [ ] Subquery vs JOIN performance
- [ ] Parameter binding and caching
- [ ] Result set size and pagination

Provide:
1. Performance analysis
2. Optimized query
3. Index recommendations
4. Before/after execution plan comparison
```

Usage: `/optimize-query`

### 10. Complex Issue Creation

**File:** `.claude/commands/create-issue.md`

```markdown
---
allowed-tools: Bash(gh *), Read
argument-hint: <title> <type>
description: Create detailed GitHub issue with template
model: claude-3-5-sonnet-20241022
---

Create a GitHub issue with:

**Title:** $1
**Type:** $2 (feature/bug/enhancement/docs)

**Repository Analysis:**
!`gh repo view --json name,description,url`

**Template:**
@.github/ISSUE_TEMPLATE/$2.md

Generate a comprehensive issue following our template structure with:
- Clear problem statement
- Proposed solution
- Acceptance criteria
- Implementation notes
- Related issues/PRs

Additional context: $ARGUMENTS
```

Usage: `/create-issue "Add dark mode support" feature "Users want theme customization"`

## Slash Commands vs Skills

### When to Use Slash Commands

**Characteristics:**
- Explicit invocation required (`/command`)
- Quick, frequently-used prompts
- Simple prompt snippets
- Single-file capabilities
- Manual control over execution

**Best for:**
- Code review workflows (`/review`)
- Quick explanations (`/explain`)
- Frequent operations (`/optimize`, `/test`)
- Personal productivity shortcuts
- Team-standardized prompts

### When to Use Skills

**Characteristics:**
- Automatic discovery based on context
- Claude decides when to invoke
- Complex workflows with multiple steps
- Multiple files (scripts, templates, docs)
- Advanced capabilities

**Best for:**
- PDF processing (auto-invoked when user mentions PDFs)
- API documentation generation (auto-invoked for API tasks)
- Complex multi-step workflows
- Capabilities requiring external scripts
- Knowledge organized across multiple files

### Can They Coexist?

**Yes!** Use both approaches:
- **Commands:** Explicit, manual shortcuts (`/review-pr`)
- **Skills:** Automatic, context-driven capabilities (PDF extraction)

## Best Practices Checklist

When creating a slash command:

- [ ] Filename is descriptive and uses kebab-case
- [ ] File location matches scope (project vs personal)
- [ ] Description frontmatter is clear and concise
- [ ] Arguments are well-documented with argument-hint
- [ ] Prompt content is specific and actionable
- [ ] File references (@) use correct paths
- [ ] Bash commands (!) have proper tool restrictions
- [ ] Model selection matches complexity (haiku/sonnet/opus)
- [ ] Command tested with various argument combinations
- [ ] Related commands organized in subdirectories
- [ ] No sensitive data (credentials, API keys) in commands
- [ ] Clear examples in comments or description

## Testing Slash Commands

### 1. Verify Command Appears

List all available commands:
```bash
# In Claude Code
/help
```

Look for your command in the output.

### 2. Test Basic Invocation

```bash
/your-command
```

Verify the prompt expands correctly.

### 3. Test with Arguments

```bash
/your-command arg1
/your-command arg1 arg2 arg3
```

Verify argument substitution works.

### 4. Test File References

If using `@file.txt`, verify the file exists and is readable.

### 5. Test Bash Commands

If using `!command`, verify:
- Command executes successfully
- Output is captured correctly
- Tool restrictions are appropriate

## Common Issues

**Command not appearing:**
- Check filename has `.md` extension
- Verify file is in correct location (.claude/commands/ or ~/.claude/commands/)
- Restart Claude Code to reload commands

**Arguments not substituting:**
- Ensure `$ARGUMENTS`, `$1`, `$2` syntax is correct
- Check for extra spaces or special characters
- Verify arguments are passed when invoking

**File references not working:**
- Confirm file path is correct (relative to project root)
- Check file exists and is readable
- Verify `@` prefix is present

**Bash commands failing:**
- Add `allowed-tools: Bash` to frontmatter
- Verify command works independently
- Check tool restriction patterns (e.g., `Bash(git *)`)

**Description not showing:**
- Add `description` field in frontmatter
- Ensure frontmatter YAML is valid (opening/closing `---`)

## Organization Strategies

### By Feature Area

```
.claude/commands/
├── git/
│   ├── commit.md
│   ├── review.md
│   └── workflow.md
├── testing/
│   ├── run.md
│   ├── coverage.md
│   └── debug.md
└── docs/
    ├── generate.md
    └── update.md
```

### By Complexity

```
~/.claude/commands/
├── quick/         # Simple, haiku-model commands
│   ├── explain.md
│   └── format.md
├── standard/      # Regular sonnet commands
│   ├── review.md
│   └── optimize.md
└── complex/       # Advanced opus commands
    └── architect.md
```

### By Team Role

```
.claude/commands/
├── frontend/
│   ├── component.md
│   └── style.md
├── backend/
│   ├── api.md
│   └── database.md
└── devops/
    ├── deploy.md
    └── monitor.md
```

## Migration from Skills

Converting a skill to a slash command:

**Skill (automatic invocation):**
```markdown
---
name: code-explainer
description: Explain code in simple terms when user asks
---

# Code Explainer
Instructions for explaining code...
```

**Slash Command (explicit invocation):**
```markdown
---
description: Explain code in simple terms
---

Explain this code in simple, beginner-friendly terms:

$ARGUMENTS

Include:
- What the code does
- How it works
- Why it's structured this way
- Common use cases
```

Usage: `/explain`

## Security Considerations

**Avoid:**
- Hardcoding credentials or API keys
- Network calls without encryption
- Destructive commands without confirmation
- Accessing sensitive files unnecessarily

**Safe practices:**
- Use environment variables for secrets
- Validate file paths before access
- Restrict bash command patterns
- Log command execution for audit trails

## Advanced Patterns

### Template-Based Commands

```markdown
---
description: Create component from template
---

Create a new $1 component named $2:

**Template:**
@templates/$1-template.tsx

**Destination:**
src/components/$2/

Generate files:
1. Component implementation
2. Test file
3. Styles
4. Documentation
5. Storybook story
```

Usage: `/create-component button UserProfileButton`

### Multi-Step Workflows

```markdown
---
allowed-tools: Bash, Read, Write, Edit
description: Complete feature implementation workflow
---

Implement feature: $ARGUMENTS

Workflow:
1. Create feature branch
2. Generate boilerplate code
3. Implement core logic
4. Add tests
5. Update documentation
6. Run quality checks
7. Create PR

Execute each step with confirmation.
```

Usage: `/feature-workflow "user authentication"`

### Context-Rich Commands

```markdown
---
allowed-tools: Bash(git *), Read
description: Comprehensive code review with full context
---

Review code with full context:

**Project Structure:**
!`find . -type f -name "*.ts" -o -name "*.tsx" | head -20`

**Recent Changes:**
!`git log --oneline -10`

**Modified Files:**
!`git diff --name-only HEAD~5..HEAD`

**Code to Review:**
$ARGUMENTS

Provide comprehensive feedback considering project context.
```

## Key Principles

1. **Descriptive names** - Clear, action-oriented command names
2. **Explicit invocation** - Users trigger commands intentionally
3. **Argument clarity** - Use argument-hint for discoverability
4. **Scope appropriately** - Project commands for team, personal for you
5. **Tool restrictions** - Only grant necessary tool access
6. **Model selection** - Match model to task complexity
7. **Organization** - Use subdirectories for related commands
8. **Documentation** - Clear descriptions and argument hints
9. **Testing** - Verify with various inputs before sharing
10. **Security** - Never hardcode sensitive data

## Workflow Summary

When user asks to create a slash command:

1. **Clarify purpose** - What prompt should be reusable?
2. **Choose scope** - Project or personal command?
3. **Design arguments** - $ARGUMENTS, $1/$2/$3, or none?
4. **Select name** - Descriptive, kebab-case filename
5. **Add frontmatter** - Description, tools, model, argument-hint
6. **Write prompt** - Clear, actionable command content
7. **Add features** - File references (@), bash commands (!)
8. **Test thoroughly** - Various arguments, edge cases
9. **Document usage** - Examples in comments or description
10. **Share if needed** - Commit project commands to git

Remember: Slash commands are for explicit, manual invocation of frequently-used prompts. Use skills for automatic, context-driven capabilities.
