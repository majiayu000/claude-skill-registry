---
name: convertSubagents
description: Atlas skill for converting Claude Code Subagents to OpenCode Agents format. USE WHEN migrating from Claude Code to OpenCode or when you have existing subagent definitions to port.
context: fork
---

# Converting Claude Code Subagents to OpenCode Agents

This skill helps you convert Claude Code Subagent definitions (from `.claude/agents/` or `~/.claude/agents/`) to OpenCode Agent format (`.opencode/agent/` or `~/.config/opencode/agent/`).

**Note:** When running from a personal config that symlinks to `~/.config/opencode/`, the agent files will be available globally.

## Quick Reference

**Source formats:**

- Claude Code: `.claude/agents/*.md` or `~/.claude/agents/*.md`
- JSON via CLI: `--agents` flag with JSON object

**Target formats:**

- OpenCode Markdown: `.opencode/agent/*.md` or `~/.config/opencode/agent/*.md`
- OpenCode JSON: `opencode.json` config file

**Key differences:**

- Tools: Comma-separated string → Object with boolean values
- Mode: Implicit → Explicit `mode` field (`primary`, `subagent`, `all`)
- Permissions: Via tools only → Explicit `permission` field
- New fields: `temperature`, `disable`, `mode`

## Conversion Workflow

### Step 1: Locate Source Subagents

Find Claude Code subagents to convert:

```bash
# Project-level subagents
ls .claude/agents/

# User-level subagents
ls ~/.claude/agents/
```

### Step 2: Read Source File

Read the subagent definition to understand its configuration:

```bash
cat .claude/agents/code-reviewer.md
```

### Step 3: Map Configuration Fields

Convert each field from Claude Code format to OpenCode format:

**Frontmatter mapping:**

| Claude Code   | OpenCode                   | Notes                                                        |
| ------------- | -------------------------- | ------------------------------------------------------------ |
| `name`        | filename or `name` in JSON | Filename becomes agent name in markdown                      |
| `description` | `description`              | Keep identical                                               |
| `tools`       | `tools`                    | Convert format (see below)                                   |
| `model`       | `model`                    | Keep identical, adjust defaults                              |
| n/a           | `mode`                     | Add explicit mode: `subagent` (default), `primary`, or `all` |
| n/a           | `temperature`              | Optional: Set 0.0-1.0 for response variability               |
| n/a           | `disable`                  | Optional: Set `true` to disable agent                        |
| n/a           | `permission`               | Optional: Set granular permissions                           |

**Tool format conversion:**

Claude Code (comma-separated or omitted):

```yaml
tools: Read, Grep, Glob, Bash
```

OpenCode (object with booleans):

```yaml
tools:
  read: true
  grep: true
  glob: true
  bash: true
  write: false
  edit: false
```

**If tools field is omitted in Claude Code:** It inherits all tools. In OpenCode, either omit the `tools` field entirely or set all desired tools to `true`.

**Model mapping:**

Claude Code models:

- `sonnet`, `opus`, `haiku` (aliases)
- `'inherit'` (use main conversation model)

OpenCode models:

- Full provider/model format: `anthropic/claude-sonnet-4-20250514`
- Can use same aliases if configured in OpenCode

### Step 4: Add OpenCode-Specific Features

Consider adding these optional fields:

**Temperature:**

```yaml
temperature: 0.1 # Lower = more focused, higher = more creative
```

**Mode:**

```yaml
mode: subagent # or 'primary' or 'all'
```

**Permissions:**

```yaml
permission:
  edit: ask # Options: ask, allow, deny
  bash:
    "git push": ask
    "git status": allow
    "*": ask
  webfetch: deny
```

### Step 5: Create Target File

**Option A: Markdown format** (recommended for easy editing)

Create file at `.opencode/agent/<agent-name>.md`:

```markdown
---
description: Expert code reviewer focusing on quality and security
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  read: true
  grep: true
  glob: true
  bash: true
  write: false
  edit: false
permission:
  edit: deny
  bash: ask
---

[System prompt content from original Claude Code subagent]
```

**Option B: JSON format** (for programmatic access)

Add to `opencode.json`:

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Expert code reviewer focusing on quality and security",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.1,
      "prompt": "{file:./prompts/code-review.txt}",
      "tools": {
        "read": true,
        "grep": true,
        "glob": true,
        "bash": true,
        "write": false,
        "edit": false
      },
      "permission": {
        "edit": "deny",
        "bash": "ask"
      }
    }
  }
}
```

### Step 6: Validate Conversion

Check the converted agent:

1. **Verify file location:**
   - Project agent: `.opencode/agent/` directory exists and file is present
   - Global agent: `~/.config/opencode/agent/` directory exists and file is present

2. **Verify frontmatter:**
   - Description is clear and specific
   - Mode is set appropriately
   - Tools are properly formatted as object with booleans
   - Model string is valid

3. **Verify system prompt:**
   - All content from original agent is preserved
   - No YAML frontmatter markers in the prompt body

4. **Test the agent:**
   - Use `@agent-name` to invoke the agent
   - Verify it behaves as expected

## Conversion Examples

For detailed step-by-step examples with before/after comparisons, see:

```bash
cat EXAMPLES.md
```

The EXAMPLES.md file includes:

- Code Reviewer (read-only agent)
- Debugger (with edit access)
- Test Runner (with bash permissions)
- Documentation Writer (write-only)
- Security Auditor (analysis only)
- Data Analyst (with BigQuery)
- Primary Build Agent (full access)
- Batch conversion scripts
- Complex permission examples

**Quick example snippet:**

Claude Code format:

```yaml
---
name: code-reviewer
description: Reviews code for quality and security
tools: Read, Grep, Glob
model: sonnet
---
```

OpenCode format:

```yaml
---
description: Reviews code for quality and security
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  read: true
  grep: true
  glob: true
  write: false
  edit: false
permission:
  edit: deny
---
```

## Common Conversion Patterns

### Pattern 1: Read-Only Analysis Agent

**Claude Code:**

```yaml
tools: Read, Grep, Glob
```

**OpenCode:**

```yaml
mode: subagent
tools:
  read: true
  grep: true
  glob: true
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash: deny
```

### Pattern 2: Development Agent with Full Access

**Claude Code:**

```yaml
tools: # Omitted = inherits all
```

**OpenCode:**

```yaml
mode: subagent
# Omit tools field to inherit all, or:
tools:
  read: true
  write: true
  edit: true
  bash: true
  grep: true
  glob: true
permission:
  bash:
    "rm *": ask
    "git push": ask
    "*": allow
```

### Pattern 3: Selective Bash Permissions

**Claude Code:**

```yaml
tools: Bash, Read
```

**OpenCode:**

```yaml
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
permission:
  bash:
    "git status": allow
    "git diff*": allow
    "git log*": allow
    "npm test": allow
    "npm run*": allow
    "*": ask # All other commands require approval
```

## Special Considerations

### Built-in Agents

Claude Code has built-in agents like the "Plan" subagent. OpenCode also has built-in agents:

- **Build**: Primary agent with all tools (equivalent to Claude Code default)
- **Plan**: Primary agent with restricted tools (similar to Claude Code Plan subagent)
- **General**: Subagent for complex research (similar to Claude Code general-purpose usage)

**Don't convert built-in agents** - they already exist in OpenCode with similar functionality.

### CLI-Defined Agents

Claude Code supports CLI-defined agents via `--agents` flag:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "...",
    "prompt": "...",
    "tools": ["Read", "Grep"],
    "model": "sonnet"
  }
}'
```

**OpenCode equivalent:**
Pass configuration via environment or config file. No direct CLI equivalent, but you can:

1. Define in `opencode.json` for persistence
2. Use project-specific `.opencode/agent/` files
3. Use global `~/.config/opencode/agent/` files

### Tool Name Differences

Most tools have the same names, but watch for:

- Claude Code: `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`
- OpenCode: `bash`, `read`, `write`, `edit`, `grep`, `glob` (lowercase in YAML)

In OpenCode markdown frontmatter, use lowercase. In JSON, also lowercase.

### MCP Tools

Both systems support MCP (Model Context Protocol) tools:

- **Claude Code**: Subagents inherit MCP tools when `tools` field is omitted
- **OpenCode**: Same behavior, plus wildcard control: `mymcp_*: false`

When converting, if the Claude Code agent uses MCP tools:

```yaml
# OpenCode - allow specific MCP server tools
tools:
  read: true
  myserver_*: true # All tools from 'myserver' MCP
  write: false
```

### Resumable Agents

Claude Code supports resumable subagents via `agentId` and `resume` parameter. OpenCode uses session-based continuity with parent/child session navigation:

- **Ctrl+Right**: Cycle forward through sessions
- **Ctrl+Left**: Cycle backward through sessions

**Conversion strategy:**

- Claude Code's resumable agents → OpenCode's session continuity (automatic)
- No configuration changes needed
- Sessions are tracked automatically in OpenCode

## Validation Checklist

After conversion, verify:

- [ ] File is in correct location (`.opencode/agent/` or `~/.config/opencode/agent/`)
- [ ] Frontmatter has `description` (required)
- [ ] `mode` is set to `subagent`, `primary`, or `all` (defaults to `all` if omitted)
- [ ] `tools` field uses object format with booleans (or omitted to inherit all)
- [ ] `model` string is valid for your OpenCode provider configuration
- [ ] System prompt is preserved exactly from original
- [ ] No `name` field in frontmatter (filename is the name)
- [ ] `temperature` is set if behavioral control is important
- [ ] `permission` is configured for potentially destructive tools
- [ ] Test agent invocation with `@agent-name`

## Troubleshooting

**Issue:** Agent not appearing in OpenCode

- Check file is in correct directory (`.opencode/agent/` or `~/.config/opencode/agent/`)
- Verify frontmatter YAML is valid
- Ensure `description` field is present
- Check for `disable: true` in frontmatter

**Issue:** Tools not working as expected

- Verify `tools` object format (not comma-separated string)
- Check permissions aren't blocking tool usage
- Ensure tool names are lowercase

**Issue:** Agent behaves differently than in Claude Code

- Review `temperature` setting (may need adjustment)
- Check `permission` settings (may be blocking operations)
- Verify system prompt is identical to original

**Issue:** Model errors

- Verify model string format: `provider/model-name`
- Check provider is configured in OpenCode
- Try using `inherit` if main model should be used

## Best Practices

1. **Start with read-only agents**: Convert agents without write access first to minimize risk
2. **Use markdown format**: Easier to edit and maintain than JSON
3. **Set explicit permissions**: Don't rely on tool restrictions alone
4. **Test incrementally**: Convert one agent at a time and test before converting more
5. **Document changes**: Note any behavioral differences in agent comments
6. **Use temperature**: Set appropriate temperature for agent's task type
7. **Leverage wildcards**: Use glob patterns for tool and permission management
8. **Keep system prompts identical**: Don't modify the prompt during conversion
9. **Use project agents**: Place in `.opencode/agent/` for team sharing
10. **Version control**: Commit converted agents to git for team consistency

## Related Commands

- `opencode agent create` - Create a new agent with guided setup
- View agents: Check `.opencode/agent/` or `~/.config/opencode/agent/`
- Test agent: Use `@agent-name` in OpenCode conversation
- Switch primary agents: Use **Tab** key or configured keybind

## References

- [OpenCode Agents Documentation](https://opencode.ai/docs/agents/)
- [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
