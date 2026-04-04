---
name: creating-subagents
description: Expert knowledge on creating Claude Code subagents. Use when designing or creating subagent .md files, understanding subagent structure, tool restrictions, or model selection.
allowed-tools: Read, Grep, Glob
---

# Creating Subagents

This Skill provides comprehensive knowledge about creating effective subagents in Claude Code.

## What Are Subagents?

Subagents are specialized AI assistants that Claude Code can delegate tasks to. Each subagent:
- Has a specific purpose and expertise area
- Uses its own context window separate from the main conversation
- Can be configured with specific tools it's allowed to use
- Includes a custom system prompt that guides its behavior

## File Structure

**Location**: `.claude/agents/{name}.md`

**Format**:
```yaml
---
name: agent-name
description: When to invoke this agent
tools: Read, Write, Edit  # Optional
model: sonnet             # Optional
---

# System Prompt

Agent's instructions, approach, and constraints.
```

## YAML Frontmatter Fields

### Required Fields

**name** (string)
- Unique identifier for the subagent
- Use lowercase letters and hyphens only
- Examples: `code-reviewer`, `test-runner`, `backend-engineer`
- ❌ Avoid: Spaces, underscores, capitals

**description** (string)
- Natural language description of the subagent's purpose
- Must include when/why to invoke the agent
- Should contain keywords users would mention
- Used by Claude to decide when to delegate tasks

### Optional Fields

**tools** (comma-separated string)
- Specific tools this subagent can use
- If omitted, inherits all tools from main thread
- Examples: `Read, Write, Edit, Bash, Grep, Glob`
- Use principle of least privilege

**model** (string)
- AI model for this subagent to use
- Options: `sonnet`, `opus`, `haiku`, `inherit`
- `inherit` - Use same model as main conversation
- If omitted, uses default subagent model (sonnet)

## Writing Effective Descriptions

The description is **critical** for automatic invocation. Claude reads descriptions to decide which subagent to use.

### Good Descriptions

```yaml
# Specific + Proactive Trigger
description: Expert code reviewer. Use PROACTIVELY after code changes to review quality, security, and maintainability.

# Clear Purpose + When to Use
description: Debugging specialist for errors, test failures, and unexpected behavior. Use when encountering any issues or when tests fail.

# Multiple Triggers
description: Backend development specialist that enforces KISS, DRY, and YAGNI. Use when creating or modifying Python/FastAPI code, database models, API endpoints, or backend logic.
```

### Bad Descriptions

```yaml
# Too vague
description: Helps with code

# Missing trigger
description: Reviews code for quality

# No "when to use"
description: Testing expert
```

### Key Elements

1. **Role** - What kind of expert is this?
2. **Purpose** - What specific tasks?
3. **Triggers** - When should Claude invoke it?
4. **Keywords** - Terms users would mention

### Proactive Invocation

Add these phrases to encourage automatic invocation:
- "Use PROACTIVELY"
- "MUST BE USED"
- "Use immediately after"
- "Use automatically when"

Example:
```yaml
description: Test coverage guardian. Use PROACTIVELY to remind about tests when code changes are made. MUST BE USED when implementing new features.
```

## System Prompt Structure

The system prompt (Markdown content after frontmatter) defines the subagent's behavior.

### Essential Sections

```markdown
# Agent Name

Brief overview of role and capabilities.

## Your Role

What this agent does and its expertise.

## When Invoked

Specific situations that trigger this agent.

## Your Process

Step-by-step workflow:
1. First action
2. Second action
3. Final action

## Best Practices

Guidelines and principles to follow.

## Red Flags

What to watch for or challenge.
```

### Example: Code Reviewer

```yaml
---
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY after writing or modifying code. Reviews quality, security, and maintainability.
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Code Reviewer

You are a senior code reviewer ensuring high standards of code quality and security.

## When Invoked

Use immediately after:
- Writing new code
- Modifying existing code
- Before committing changes
- When user asks for code review

## Your Process

1. **Understand Changes**
   - Run `git diff` to see modifications
   - Identify affected files and functions

2. **Review Systematically**
   - Code readability and simplicity
   - Proper naming conventions
   - No code duplication
   - Error handling present
   - Security considerations
   - Test coverage

3. **Provide Feedback**
   - Critical issues (must fix immediately)
   - Warnings (should address)
   - Suggestions (nice to have)

## Review Checklist

### Readability
- [ ] Functions are small and focused
- [ ] Variable names are clear
- [ ] Complex logic is commented

### Quality
- [ ] No code duplication (DRY)
- [ ] Proper error handling
- [ ] Edge cases handled

### Security
- [ ] No exposed secrets
- [ ] Input validation present
- [ ] Authentication/authorization checked

## Red Flags

- Copy-pasted code blocks
- Overly complex solutions
- Missing error handling
- Hardcoded credentials
- Untested code paths
```

## Tool Restrictions

Use the `tools` field to limit what the subagent can do.

### Read-Only Subagent

```yaml
tools: Read, Grep, Glob
```

Good for:
- Code reviewers
- Analyzers
- Documentation readers

### Limited Write Subagent

```yaml
tools: Read, Write, Edit, Grep, Glob
```

Good for:
- Code generators
- File refactorers
- Test writers

### Full Access Subagent

```yaml
# Omit tools field to inherit all tools
```

Good for:
- Deployment agents
- Complex workflow orchestrators
- System administrators

### Security Tools

```yaml
tools: Read, Bash(git:*), Bash(docker:*), Bash(pytest:*)
```

Restrict Bash to specific commands for security.

## Model Selection

Choose the right model for the task.

### Sonnet (Default, Balanced)

```yaml
model: sonnet
```

- Best for most tasks
- Good balance of speed/quality
- Recommended default

### Haiku (Fast, Economical)

```yaml
model: haiku
```

- Quick tasks
- Simple patterns
- Cost-sensitive operations
- Example: File search, simple analysis

### Opus (Powerful, Thoughtful)

```yaml
model: opus
```

- Complex reasoning
- Critical decisions
- Security reviews
- Example: Architecture design, complex refactoring

### Inherit (Match Main Conversation)

```yaml
model: inherit
```

- Use same model as main conversation
- Ensures consistent capabilities
- Good for tightly integrated subagents

## Common Patterns

### Task-Specific Subagents

**Purpose**: Handle one type of task well

```yaml
---
name: test-runner
description: Runs tests and fixes failures. Use PROACTIVELY when code changes are made or when tests fail.
tools: Read, Edit, Bash
model: sonnet
---

You run tests and fix failures while preserving test intent.

## Your Process
1. Run the test suite
2. If failures, analyze error messages
3. Fix the code (not the tests)
4. Re-run to verify
5. Report results
```

### Domain-Specific Subagents

**Purpose**: Expert in specific technology/domain

```yaml
---
name: database-engineer
description: Database design and SQL expert. Use when working with database models, queries, migrations, or data modeling.
tools: Read, Write, Edit, Bash
model: sonnet
---

You are an expert in database design, SQL, and ORMs.

## Expertise
- SQLAlchemy models and relationships
- Efficient query patterns
- Database migrations
- Data modeling best practices

## When to Invoke
- Creating database models
- Designing table relationships
- Writing complex queries
- Creating migrations
```

### Principle-Enforcing Subagents

**Purpose**: Enforce coding principles or patterns

```yaml
---
name: backend-engineer
description: Backend development with strict KISS, DRY, YAGNI principles. Use when creating or modifying backend code.
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

You enforce KISS, DRY, and YAGNI principles in backend development.

## Principles You Enforce

**KISS** - Keep It Simple
- Prefer simple solutions over clever ones
- Avoid premature abstraction
- Question every layer of indirection

**DRY** - Don't Repeat Yourself
- Extract common logic
- Never copy-paste code
- Refactor on second repetition

**YAGNI** - You Aren't Gonna Need It
- Build only what's needed now
- Resist "nice to have" features
- Challenge "we might need it later"

## Red Flags You Challenge
- "We might need this later..."
- Copy-pasted code blocks
- Abstraction with no current use
- Complex solutions to simple problems
```

### Workflow Orchestrators

**Purpose**: Manage complex multi-step workflows

```yaml
---
name: deployment-engineer
description: Production deployment specialist. Use for deployment tasks, server management, or DevOps operations.
tools: Read, Bash, Grep, Glob
model: sonnet
---

You handle production deployments safely and systematically.

## Deployment Workflow
1. Verify current state
2. Run pre-deployment checks
3. Execute deployment steps
4. Verify deployment success
5. Monitor for issues
6. Rollback if needed

## Safety Checks
- Always backup before changes
- Verify in staging first
- Check monitoring after deployment
- Have rollback plan ready
```

## Subagent Communication

### Invoking Skills

Subagents can invoke Skills for specialized knowledge:

```markdown
## Your Process

1. Check code style guidelines
2. **Invoke the `code-style-guide` Skill** for language-specific patterns
3. Apply recommendations
4. Report violations
```

### Invoking Other Subagents

Subagents can suggest invoking other subagents:

```markdown
## When to Delegate

If you encounter:
- Test failures → Suggest `test-runner` subagent
- Deployment tasks → Suggest `deployment-engineer` subagent
- Security issues → Suggest `security-reviewer` subagent
```

## Testing Subagents

Test by explicitly invoking them:

```
User: "Use the code-reviewer subagent to check my recent changes"
```

Or test automatic invocation:

```
User: "I just modified the authentication code"
# code-reviewer should activate automatically if description mentions "after code changes"
```

## Best Practices

### 1. Single Responsibility

**Good** - Focused purpose:
- `code-reviewer` - Reviews code quality
- `test-runner` - Runs and fixes tests
- `database-engineer` - Database design

**Bad** - Multiple responsibilities:
- `general-helper` - Does everything (too broad)
- `backend-and-frontend` - Two domains (split them)

### 2. Clear Triggers in Description

```yaml
# Good - Multiple specific triggers
description: Backend developer for FastAPI and SQLAlchemy. Use when creating API endpoints, database models, or modifying backend Python code.

# Bad - Vague trigger
description: Helps with backend
```

### 3. Appropriate Tool Restrictions

```yaml
# Code reviewer - read only
tools: Read, Grep, Glob, Bash(git diff:*)

# Code generator - needs write
tools: Read, Write, Edit, Grep, Glob

# Deployment - needs system access
tools: Read, Bash, Grep
```

### 4. Keep System Prompts Focused

- Under 300 lines
- Clear sections
- Concrete examples
- Specific workflows

For complex knowledge, create supporting Skills instead.

### 5. Use TodoWrite for Tracking

Include in system prompt:

```markdown
## Your Process

Use TodoWrite to track:
- [ ] Analyze requirements
- [ ] Review code
- [ ] Provide feedback
- [ ] Verify fixes
```

## Common Pitfalls

### Too Generic

❌ **Bad**:
```yaml
name: helper
description: Helps with coding tasks
```

✅ **Good**:
```yaml
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY after code changes to review quality, security, and maintainability.
```

### Too Restrictive

❌ **Bad**:
```yaml
tools: Read  # Can't do anything useful
```

✅ **Good**:
```yaml
tools: Read, Grep, Glob, Bash(git:*)  # Can analyze code
```

### Missing Triggers

❌ **Bad**:
```yaml
description: Testing expert
# When should this be used?
```

✅ **Good**:
```yaml
description: Test runner and fixer. Use PROACTIVELY when code changes or when tests fail.
```

### Bloated System Prompt

❌ **Bad**:
```markdown
[500 lines of detailed patterns and examples]
```

✅ **Good**:
```markdown
[100 lines of core workflow]

For detailed patterns, see the `testing-patterns` Skill.
```

## Validation Checklist

Before finalizing a subagent:

- [ ] Name uses lowercase and hyphens only
- [ ] Description includes "when to use"
- [ ] Description contains trigger keywords
- [ ] Tools follow least privilege principle
- [ ] Model choice is appropriate
- [ ] System prompt has clear structure
- [ ] Process/workflow is defined
- [ ] Examples or checklists included
- [ ] No conflicts with existing subagents

## Summary

**Essential Elements**:
1. Focused responsibility (one job, done well)
2. Clear description with triggers
3. Appropriate tool restrictions
4. Structured system prompt
5. Defined workflow/process

**Success Criteria**:
- Automatically invoked at right time
- Has necessary tools to complete tasks
- System prompt provides clear guidance
- Integrates well with other subagents
