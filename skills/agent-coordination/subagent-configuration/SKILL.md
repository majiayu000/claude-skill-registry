---
name: subagent-configuration
description: This skill should be used when the user asks to "configure a subagent", "create a custom agent", "set up agent tools", "configure permissionMode", "add agent skills", or mentions subagent fields like tools, model, or permissionMode. Provides comprehensive guidance on subagent configuration options and best practices.
version: 1.0.0
---

# Subagent Configuration

Configure custom subagents in Claude Code with specialized tools, models, and permissions for task-specific workflows.

## Purpose

Subagents are pre-configured AI personalities that delegate specialized tasks. Each subagent operates in its own context window with custom system prompts, specific tool access, and tailored permission modes. This skill provides guidance on configuring subagent YAML frontmatter and system prompts effectively.

## When to Use This Skill

Use this skill when:
- Creating new subagents for specialized tasks
- Configuring tool access for security or focus
- Selecting appropriate models for performance/cost trade-offs
- Setting permission modes for automation workflows
- Loading skills automatically when subagents start
- Understanding configuration field options and values

## Configuration Overview

Subagents are defined in Markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: When this agent should be invoked
tools: tool1, tool2, tool3    # Optional
model: sonnet                 # Optional
permissionMode: default       # Optional
skills: skill1, skill2        # Optional
---

System prompt content goes here.
```

### File Locations

- **Project subagents**: `.claude/agents/` (highest priority)
- **User subagents**: `~/.claude/agents/` (lower priority)
- **Plugin agents**: Provided by installed plugins

## Required Fields

### name (Required)

Unique identifier using lowercase letters, numbers, and hyphens only.

**Format**: `lowercase-with-hyphens`

**Examples**:
- `code-reviewer`
- `test-runner`
- `data-scientist`
- `security-auditor`

**Invalid**:
- `Code_Reviewer` (uppercase, underscores)
- `test runner` (spaces)
- `my.agent` (periods)

### description (Required)

Natural language description of when Claude should invoke this subagent. This field is critical for automatic delegation.

**Best practices**:
- Be specific about when to use the agent
- Include trigger phrases (e.g., "Use proactively when...")
- Mention task types clearly
- Use natural language Claude will understand

**Examples**:

Good:
```yaml
description: Expert code reviewer. Use proactively after code changes to check quality, security, and best practices.
```

Good:
```yaml
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
```

Weak:
```yaml
description: Helps with code
```

## Optional Fields

### tools (Optional)

Comma-separated list of specific tools the subagent can use. If omitted, inherits all tools from main thread.

**Common tools**:
- `Read, Write, Edit` - File operations
- `Bash` - Shell commands
- `Grep, Glob` - Search operations
- `WebFetch, WebSearch` - Web operations
- `Task` - Delegate to other subagents
- `NotebookEdit` - Jupyter notebooks
- MCP tools: `mcp__server__tool`

**Examples**:

Read-only agent:
```yaml
tools: Read, Grep, Glob
```

Full-stack developer:
```yaml
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Task
```

Code reviewer (no modifications):
```yaml
tools: Read, Grep, Glob, Bash
```

**Security consideration**: Limit tools to minimum needed for the subagent's purpose.

### model (Optional)

Specify which AI model the subagent uses.

**Values**:
- `sonnet` - Balanced capability (default for subagents)
- `opus` - Most capable, higher cost
- `haiku` - Fast and efficient, lower cost
- `inherit` - Use same model as main conversation

**Examples**:

Fast searching with Haiku:
```yaml
model: haiku
```

Complex reasoning with Opus:
```yaml
model: opus
```

Match main conversation:
```yaml
model: inherit
```

**Defaults**: If omitted, uses configured subagent model (typically `sonnet`).

### permissionMode (Optional)

Controls how the subagent handles permission requests.

**Values**:
- `default` - Normal permission flow (asks for confirmation)
- `acceptEdits` - Automatically accepts edit operations
- `bypassPermissions` - Bypasses permission system entirely
- `plan` - Plan mode (read-only, no execution)
- `ignore` - Ignores permission requests

**Examples**:

Auto-formatter (accepts edits):
```yaml
permissionMode: acceptEdits
```

Data analyst (bypasses for automation):
```yaml
permissionMode: bypassPermissions
```

Architecture planner (read-only):
```yaml
permissionMode: plan
```

Standard agent (asks permission):
```yaml
permissionMode: default
```

**Security note**: Use `bypassPermissions` carefully, only for trusted workflows.

### skills (Optional)

Comma-separated list of skill names to auto-load when the subagent starts.

**Format**: `skill-name-1, skill-name-2`

**Example**:
```yaml
skills: test-driven-development, code-reviewer
```

Skills are loaded into the subagent's context automatically, providing specialized knowledge.

## Configuration Patterns

### Pattern 1: Minimal Configuration

For simple, general-purpose subagents:

```yaml
---
name: simple-helper
description: A basic helper agent for simple tasks
---

Provide quick answers and basic guidance.
```

### Pattern 2: Read-Only Agent

For exploration and analysis without modifications:

```yaml
---
name: documentation-reader
description: Read-only agent for exploring documentation
tools: Read, Grep, Glob
model: haiku
---

Explore documentation and provide information about what exists.
Never suggest modifications.
```

### Pattern 3: Automation Agent

For automated workflows that shouldn't ask permission:

```yaml
---
name: auto-formatter
description: Automatically formats code files without asking permission
tools: Read, Edit, Bash
model: haiku
permissionMode: acceptEdits
---

Automatically format code files when invoked.
Run formatting tools without asking for confirmation.
```

### Pattern 4: Expert Agent with Skills

For specialized domains requiring loaded knowledge:

```yaml
---
name: pdf-expert
description: PDF processing expert with specialized skills
tools: Read, Write, Bash
model: sonnet
skills: pdf-processing, form-filling
---

Process PDF files, forms, and document extraction using specialized skills.
```

### Pattern 5: Security-Focused Agent

For security audits with restricted tools:

```yaml
---
name: security-auditor
description: Security audit specialist. Use when reviewing code for vulnerabilities.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
---

Find vulnerabilities: SQL injection, XSS, CSRF, exposed secrets.
Provide severity ratings and remediation steps.
```

### Pattern 6: Full-Featured Agent

For complex tasks requiring all capabilities:

```yaml
---
name: full-stack-developer
description: Full-stack development expert. MUST BE USED for complex features requiring both frontend and backend changes.
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Task
model: opus
permissionMode: default
skills: code-reviewer, test-driven-development
---

Implement complex features end-to-end:
1. Analyze requirements
2. Plan implementation strategy
3. Implement backend then frontend
4. Write comprehensive tests
5. Document changes
```

## Writing Effective System Prompts

The system prompt (Markdown body) defines the subagent's behavior and expertise.

**Best practices**:
- Be specific about role and expertise
- Include step-by-step workflows
- List key practices or checkpoints
- Define what NOT to do when relevant
- Provide examples or templates
- Keep focused on the subagent's purpose

**Structure example**:

```markdown
You are a [role] specializing in [domain].

When invoked:
1. [First step]
2. [Second step]
3. [Third step]

Key practices:
- [Practice 1]
- [Practice 2]
- [Practice 3]

For each [task], provide:
- [Output 1]
- [Output 2]
- [Output 3]
```

## Managing Subagents

### Using /agents Command (Recommended)

Interactive management:

```
/agents
```

Provides:
- View all available subagents
- Create new subagents with guided setup
- Edit existing subagents
- Delete custom subagents
- See priority when duplicates exist
- Manage tool permissions easily

### Direct File Management

Manual creation:

```bash
# Project subagent
mkdir -p .claude/agents
nano .claude/agents/my-agent.md

# User subagent
mkdir -p ~/.claude/agents
nano ~/.claude/agents/my-agent.md
```

Changes take effect on next Claude Code session start.

## Best Practices

### Design Focused Subagents

Create subagents with single, clear responsibilities:

✅ Good:
- `code-reviewer` - Reviews code quality
- `test-runner` - Runs and fixes tests
- `security-auditor` - Finds vulnerabilities

❌ Avoid:
- `everything-agent` - Does everything
- `helper` - Too vague

### Write Detailed Prompts

Include specific instructions, examples, and constraints. More guidance = better performance.

### Limit Tool Access

Only grant tools necessary for the subagent's purpose:

Security agent:
```yaml
tools: Read, Grep, Glob, Bash  # No Write/Edit
```

Formatter:
```yaml
tools: Read, Edit, Bash  # No WebFetch/Search
```

### Version Control Project Agents

Check project subagents into git:

```bash
git add .claude/agents/
git commit -m "Add team subagents"
```

Team members automatically get the same subagents.

### Test Subagent Behavior

After creating, test by:
1. Invoking explicitly: "Use the X subagent to Y"
2. Testing automatic delegation with relevant queries
3. Verifying tool access works as expected
4. Checking permission mode behaves correctly

## Additional Resources

### Reference Files

For detailed configuration examples:
- **`references/configuration-examples.md`** - 12 complete subagent configurations with explanations
- **`examples/`** - Working subagent files ready to use

### Built-in Subagents

Study Claude Code's built-in subagents:
- `general-purpose` - Multi-step tasks, uses Sonnet, all tools
- `explore` - Fast searching, uses Haiku, read-only
- `plan` - Architecture planning, uses Sonnet, plan mode

### Related Documentation

- Subagents: `/docs/en/sub-agents`
- Plugins: `/docs/en/plugins`
- Settings: `/docs/en/settings`

## Quick Reference

### Field Summary

| Field | Required | Values | Default |
|-------|----------|--------|---------|
| `name` | ✅ | lowercase-with-hyphens | - |
| `description` | ✅ | Natural language | - |
| `tools` | ❌ | Comma-separated list | All tools |
| `model` | ❌ | sonnet, opus, haiku, inherit | sonnet |
| `permissionMode` | ❌ | default, acceptEdits, bypassPermissions, plan, ignore | default |
| `skills` | ❌ | Comma-separated list | None |

### Common Tool Sets

**Read-only**: `Read, Grep, Glob`
**Basic editing**: `Read, Write, Edit`
**With execution**: `Read, Write, Edit, Bash`
**Full access**: `Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Task`

### Permission Modes

- `default` - Standard (asks permission)
- `acceptEdits` - Auto-approve edits
- `bypassPermissions` - Skip all permissions
- `plan` - Read-only planning
- `ignore` - Ignore permission dialogs

## Troubleshooting

**Subagent not triggering automatically**:
- Check `description` is specific with trigger phrases
- Include "Use proactively when..." in description
- Mention specific task types clearly

**Tools not working**:
- Verify tool names spelled correctly (case-sensitive)
- Check tools aren't blocked by permission settings
- Ensure MCP tools use `mcp__server__tool` format

**Wrong model being used**:
- Check `model` field is set correctly
- Verify model aliases: sonnet, opus, haiku, inherit
- Confirm model is available in your account

**Permission issues**:
- Review `permissionMode` setting
- Use `default` for standard behavior
- Use `acceptEdits` for auto-approval
- Avoid `bypassPermissions` unless necessary

## Implementation Workflow

To create a subagent:

1. **Identify purpose**: What specific task will this subagent handle?
2. **Choose tools**: What tools does it need? (Minimum required)
3. **Select model**: Haiku (fast), Sonnet (balanced), Opus (capable), Inherit (match main)
4. **Set permissions**: How should it handle confirmations?
5. **Write description**: When should Claude invoke this? Include trigger phrases
6. **Create system prompt**: Define role, workflow, practices
7. **Add skills** (if needed): What knowledge should auto-load?
8. **Test**: Invoke explicitly and test automatic delegation
9. **Iterate**: Refine based on actual usage

Focus on creating focused subagents with clear purposes, minimal tool access, and specific descriptions for effective automatic delegation.
