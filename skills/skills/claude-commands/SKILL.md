---
name: claude-commands
description: Guide for creating custom slash commands for Claude Code. Use when adding new commands, defining command arguments, or implementing command workflows.
---

# Claude Code Commands

Guide for creating custom slash commands that extend Claude Code functionality.

## When to Use This Skill

Activate this skill when:
- Creating new custom slash commands
- Understanding command structure and syntax
- Organizing commands for plugins
- Implementing command workflows
- Debugging command execution

## What Are Commands?

Commands are custom slash commands (like `/commit`, `/review`) that users can invoke to trigger specific workflows or expand prompts. They are markdown files that can contain:

- Static prompt text
- Dynamic content based on arguments
- Multi-step workflows
- Integration with tools and scripts

## Command File Structure

### Location

Commands are defined in markdown files located in:
- Plugin: `<plugin-root>/commands/`
- User-level: `.claude/commands/`

### File Naming

- Use kebab-case: `my-command.md`
- File name becomes the command name: `my-command.md` → `/my-command`
- Avoid conflicts with built-in commands

## Basic Command Format

### Simple Static Command

```markdown
# /my-command

This is the prompt that will be expanded when the user types /my-command.

The entire content of this file will replace the slash command in the conversation.
```

### Command with Description

```markdown
<!--
description: Brief description of what this command does
-->

# /my-command

Command prompt goes here...
```

## Command Arguments

Commands can accept arguments that users provide when invoking the command.

### Single Argument

```markdown
# /greet

Hello, {{arg}}! Welcome to the project.
```

Usage: `/greet Alice` → "Hello, Alice! Welcome to the project."

### Multiple Arguments

```markdown
# /create-file

Create a new file at {{arg1}} with the following content:

{{arg2}}
```

Usage: `/create-file src/main.rs "fn main() {}"`

### Named Arguments

```markdown
# /deploy

Deploy {{environment}} environment to {{region}}.

Configuration:
- Environment: {{environment}}
- Region: {{region}}
- Branch: {{branch}}
```

Usage: `/deploy --environment=production --region=us-east-1 --branch=main`

## Advanced Features

### Conditional Content

```markdown
# /analyze

Analyze the {{language}} codebase.

{{#if verbose}}
Provide detailed analysis including:
- Code complexity metrics
- Dependency analysis
- Security vulnerabilities
{{else}}
Provide a summary analysis.
{{/if}}
```

### Including Files

Reference other files or command outputs:

```markdown
# /context

Here is the current project structure:

{{file:PROJECT_STRUCTURE.md}}

And the current git status:

{{shell:git status}}
```

### Multi-Step Workflows

```markdown
# /full-review

I'll perform a comprehensive code review:

1. First, let me check the git diff:
{{shell:git diff}}

2. Now analyzing code quality...

3. Checking for security issues...

4. Final recommendations:
```

## Best Practices

### Clear Command Names

- Use descriptive, action-oriented names
- `/analyze-security` not `/sec`
- `/create-component` not `/comp`

### Provide Context

Always include what the command will do:

```markdown
# /commit

I'll analyze the current git changes and create a conventional commit message.

Current changes:
{{shell:git diff --staged}}

Based on these changes, here's my suggested commit message:
```

### Handle Edge Cases

```markdown
# /deploy

{{#if staging}}
Deploying to staging environment (safe for testing)
{{else if production}}
⚠️ WARNING: Deploying to PRODUCTION
Are you sure you want to continue? This will affect live users.
{{else}}
Error: Unknown environment. Please specify --staging or --production
{{/if}}
```

### Document Arguments

```markdown
<!--
description: Deploy application to specified environment
usage: /deploy [--environment=<env>] [--region=<region>]
arguments:
  - environment: Target environment (staging, production)
  - region: AWS region (us-east-1, eu-west-1, etc.)
-->

# /deploy
```

## Command Organization

### Plugin Commands

In `plugin.json`:

```json
{
  "commands": [
    "./commands/deploy.md",
    "./commands/analyze.md",
    "./commands/review.md"
  ]
}
```

### Directory-Based Commands

```json
{
  "commands": ["./commands"]
}
```

This loads all `.md` files in the `commands/` directory.

### Namespaced Commands

Organize related commands in subdirectories:

```
commands/
├── git/
│   ├── commit.md
│   ├── review.md
│   └── cleanup.md
├── deploy/
│   ├── staging.md
│   └── production.md
```

## Common Command Patterns

### Git Commit Message Generator

```markdown
# /gcm

I'll analyze the staged changes and generate a conventional commit message.

{{shell:git diff --staged}}

Based on these changes, here's my commit message:
```

### Code Review Command

```markdown
# /review-pr

I'll review the pull request changes.

PR Number: {{pr_number}}

{{shell:gh pr diff {{pr_number}}}}

Review checklist:
- [ ] Code quality and style
- [ ] Security considerations
- [ ] Test coverage
- [ ] Documentation updates
```

### Project Scaffolding

```markdown
# /new-component

Creating a new {{component_type}} component named {{name}}.

I'll create:
1. Component file at src/components/{{name}}.tsx
2. Test file at src/components/{{name}}.test.tsx
3. Storybook file at src/components/{{name}}.stories.tsx
```

## Testing Commands

### Manual Testing

1. Install the plugin locally
2. Reload Claude Code
3. Type your command in the chat
4. Verify the expansion is correct

### Debugging

If a command doesn't work:

1. Check file location matches plugin.json
2. Verify markdown syntax
3. Test argument substitution
4. Check for conflicts with existing commands

## Command Templates

### Analysis Command Template

```markdown
<!--
description: Analyze {{target}} for {{criteria}}
-->

# /analyze-{{target}}

I'll analyze the {{target}} codebase for {{criteria}}.

{{shell:find {{target}} -type f -name "*.{{extension}}"}}

Analysis results:
```

### Workflow Command Template

```markdown
<!--
description: Execute {{workflow}} workflow
-->

# /{{workflow}}

Starting {{workflow}} workflow...

Step 1: {{step1_description}}
{{step1_action}}

Step 2: {{step2_description}}
{{step2_action}}

Workflow complete!
```

## Integration with Skills

Commands can reference skills:

```markdown
# /elixir-review

I'll review this Elixir code using my Phoenix and OTP knowledge.

Please provide the code to review, and I'll check for:
- Phoenix best practices
- OTP design patterns
- Elixir anti-patterns
- Performance considerations
```

## Security Considerations

### Avoid Sensitive Data

Never hardcode:
- API keys
- Passwords
- Tokens
- Private URLs

### Validate Input

```markdown
# /deploy

{{#unless environment}}
Error: --environment is required
{{/unless}}

{{#if (validate_environment environment)}}
Proceeding with deployment...
{{else}}
Error: Invalid environment. Must be staging or production.
{{/if}}
```

### Safe Shell Commands

Be cautious with shell command execution:

```markdown
# /safe-deploy

<!-- Only allow whitelisted commands -->
{{shell:./scripts/deploy.sh {{environment}}}}
```

## References

For more information about Claude Code commands:
- Claude Code Documentation: https://code.claude.com/docs/en/commands
- Example Commands: https://github.com/anthropics/claude-code/tree/main/examples/commands
