---
name: convertCommands
description: Atlas skill for converting Claude Code slash commands to OpenCode commands format. USE WHEN migrating from Claude Code to OpenCode or when you have existing slash command definitions to port.
context: fork
---

# Converting Claude Code Slash Commands to OpenCode Commands

This skill helps you convert Claude Code slash command definitions (from `.claude/commands/` or `~/.claude/commands/`) to OpenCode command format (`.opencode/command/` or `~/.config/opencode/command/`).

**Note:** When running from a personal config that symlinks to `~/.config/opencode/`, the command files will be available globally.

## Quick Reference

**Source formats:**

- Claude Code: `.claude/commands/*.md` or `~/.claude/commands/*.md`

**Target formats:**

- OpenCode Markdown: `.opencode/command/*.md` or `~/.config/opencode/command/*.md`
- OpenCode JSON: `opencode.json` config file

**Key differences:**

- Frontmatter fields: Different field names and options
- Argument syntax: Same (`$ARGUMENTS`, `$1`, `$2`, etc.)
- Shell commands: Same syntax (`!`command``)
- File references: Same syntax (`@filename`)
- New fields: `subtask`, `template` (in JSON)

## Conversion Workflow

### Step 1: Locate Source Commands

Find Claude Code slash commands to convert:

```bash
# Project-level commands
ls .claude/commands/

# User-level commands
ls ~/.claude/commands/
```

### Step 2: Read Source File

Read the command definition to understand its configuration:

```bash
cat .claude/commands/review.md
```

### Step 3: Map Configuration Fields

Convert each field from Claude Code format to OpenCode format:

**Frontmatter mapping:**

| Claude Code                | OpenCode      | Notes                           |
| -------------------------- | ------------- | ------------------------------- |
| `allowed-tools`            | `agent`       | Convert tool list to agent name |
| `argument-hint`            | N/A           | Not supported in OpenCode       |
| `description`              | `description` | Keep identical                  |
| `model`                    | `model`       | Keep identical                  |
| `disable-model-invocation` | N/A           | Not supported in OpenCode       |
| N/A                        | `subtask`     | New: Force subagent invocation  |
| N/A                        | `template`    | New: Only in JSON format        |

**Tool conversion:**

Claude Code uses `allowed-tools` to restrict which tools the command can use:

```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Read
```

OpenCode uses `agent` to specify which agent runs the command:

```yaml
agent: build
```

### Step 4: Handle Special Cases

**Bash commands with allowed-tools:**

Claude Code:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---
```

OpenCode - Use agent with appropriate permissions:

```markdown
---
description: Create a git commit
agent: build
---
```

Note: OpenCode handles tool permissions at the agent level, not command level.

**Model invocation control:**

Claude Code:

```markdown
---
disable-model-invocation: true
---
```

OpenCode doesn't have a direct equivalent. Commands are always user-invoked in OpenCode.

### Step 5: Create Target File

**Option A: Markdown format** (recommended for easy editing)

Create file at `.opencode/command/<command-name>.md`:

```markdown
---
description: Review code for quality and security
agent: build
model: anthropic/claude-sonnet-4-20250514
---

Review this code for:

- Security vulnerabilities
- Performance issues
- Code style violations

Use !`git diff HEAD` to see current changes.
```

**Option B: JSON format** (for programmatic access)

Add to `opencode.json`:

```json
{
  "command": {
    "review": {
      "description": "Review code for quality and security",
      "template": "Review this code for:\n- Security vulnerabilities\n- Performance issues\n- Code style violations\n\nUse !`git diff HEAD` to see current changes.",
      "agent": "build",
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  }
}
```

### Step 6: Validate Conversion

Check the converted command:

1. **Verify file location:**
   - Project command: `.opencode/command/` directory exists and file is present
   - Global command: `~/.config/opencode/command/` directory exists and file is present

2. **Verify frontmatter:**
   - Description is clear and specific
   - Agent is set appropriately (if needed)
   - Model string is valid (if specified)

3. **Verify command content:**
   - All content from original command is preserved
   - Arguments (`$ARGUMENTS`, `$1`, etc.) are preserved
   - Shell commands (`!`command``) are preserved
   - File references (`@filename`) are preserved

4. **Test the command:**
   - Use `/command-name` to invoke the command
   - Verify it behaves as expected

## Conversion Examples

For detailed step-by-step examples with before/after comparisons, see:

```bash
cat EXAMPLES.md
```

The EXAMPLES.md file includes:

- Simple code review command
- Git commit command with bash execution
- PR review with arguments
- Test runner command
- Documentation generator
- Batch conversion scripts
- Complex permission examples

**Quick example snippet:**

Claude Code format:

```yaml
---
description: Review code for quality and security
allowed-tools: Read, Grep, Glob
model: claude-3-5-sonnet-20241022
---
Review this code focusing on security and performance.
```

OpenCode format:

```yaml
---
description: Review code for quality and security
agent: plan
model: anthropic/claude-3-5-sonnet-20241022
---
Review this code focusing on security and performance.
```

## Common Conversion Patterns

### Pattern 1: Simple Review Command

**Claude Code:**

```yaml
---
description: Review this code
allowed-tools: Read, Grep
---
Review this code for bugs and improvements.
```

**OpenCode:**

```yaml
---
description: Review this code
agent: plan
---
Review this code for bugs and improvements.
```

### Pattern 2: Git Commit Command

**Claude Code:**

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

Current status: !`git status`
Current diff: !`git diff HEAD`

Create a commit based on these changes.
```

**OpenCode:**

```yaml
---
description: Create a git commit
agent: build
---

Current status: !`git status`
Current diff: !`git diff HEAD`

Create a commit based on these changes.
```

### Pattern 3: Command with Arguments

**Claude Code:**

```yaml
---
argument-hint: [pr-number] [priority]
description: Review pull request
---

Review PR #$1 with priority $2.
```

**OpenCode:**

```yaml
---
description: Review pull request
---
Review PR #$1 with priority $2.
```

Note: `argument-hint` is not supported in OpenCode, but the argument placeholders work the same.

### Pattern 4: Subagent Invocation

**Claude Code:**
No direct equivalent - commands run in main conversation.

**OpenCode:**

```yaml
---
description: Analyze performance
agent: plan
subtask: true
---
Analyze performance issues in this codebase.
```

The `subtask: true` forces this to run as a subagent invocation.

## Special Considerations

### Argument Hints

Claude Code supports `argument-hint` to show expected arguments:

```yaml
argument-hint: [message]
```

OpenCode doesn't have this field. Document expected arguments in the command description instead:

```yaml
description: Create git commit [message]
```

### Allowed Tools vs Agents

Claude Code controls tools at the command level with `allowed-tools`.

OpenCode controls tools at the agent level. Choose the appropriate agent for your command:

- `build` - Full access to all tools
- `plan` - Restricted tools for analysis
- Custom agents - Your defined agents

### Model Strings

Both systems use similar model strings, but ensure you use the correct provider prefix:

**Claude Code:**

```yaml
model: claude-3-5-sonnet-20241022
```

**OpenCode:**

```yaml
model: anthropic/claude-3-5-sonnet-20241022
```

### Namespacing with Subdirectories

Both systems support organizing commands in subdirectories:

**Claude Code:**
`.claude/commands/frontend/component.md` → `/component` with description showing "(project:frontend)"

**OpenCode:**
`.opencode/command/frontend/component.md` → `/frontend/component`

Note: OpenCode includes the subdirectory in the command name, while Claude Code shows it in the description only.

### File References

Both systems use the same `@` syntax for file references:

```markdown
Review the component in @src/components/Button.tsx
```

This works identically in both systems.

### Shell Command Execution

Both systems use the same `` !`command` `` syntax:

```markdown
Current git status: !`git status`
```

This works identically in both systems.

### Thinking Mode

Claude Code supports extended thinking via keywords in command content.

OpenCode doesn't have a specific thinking mode configuration for commands. Extended thinking is model-dependent.

## Validation Checklist

After conversion, verify:

- [ ] File is in correct location (`.opencode/command/` or `~/.config/opencode/command/`)
- [ ] Frontmatter has `description` (optional but recommended)
- [ ] Command content is preserved exactly from original
- [ ] Argument placeholders (`$ARGUMENTS`, `$1`, etc.) are preserved
- [ ] Shell commands (`` !`command` ``) are preserved
- [ ] File references (`@filename`) are preserved
- [ ] Model string uses correct provider prefix (if specified)
- [ ] Agent is appropriate for command's needs (if specified)
- [ ] Test command invocation with `/command-name`

## Troubleshooting

**Issue:** Command not appearing in OpenCode

- Check file is in correct directory (`.opencode/command/` or `~/.config/opencode/command/`)
- Verify frontmatter YAML is valid (if present)
- Try restarting OpenCode

**Issue:** Arguments not working

- Verify you're using `$ARGUMENTS`, `$1`, `$2`, etc. (not `{arg1}` or other syntax)
- Check argument is being passed when invoking command

**Issue:** Shell commands not executing

- Verify syntax: `` !`command` `` (backticks inside the !` ` markers)
- Check the shell command works when run manually
- Ensure agent has bash tool permissions

**Issue:** File references not working

- Verify syntax: `@path/to/file.ext`
- Check the file path is correct relative to project root

**Issue:** Model errors

- Verify model string format: `provider/model-name`
- Check provider is configured in OpenCode
- Try using `model: inherit` or omit the field

**Issue:** Command runs in wrong context

- Set `subtask: true` to force subagent invocation
- Choose appropriate `agent` for the command

## Best Practices

1. **Start simple**: Convert basic commands first to understand the process
2. **Use markdown format**: Easier to edit and maintain than JSON
3. **Choose appropriate agents**: Use `plan` for analysis, `build` for modifications
4. **Preserve command content**: Don't modify the prompt during conversion
5. **Test incrementally**: Convert one command at a time and test before converting more
6. **Document arguments**: Since `argument-hint` isn't supported, document in description
7. **Organize with subdirectories**: Keep related commands together
8. **Use project commands**: Place in `.opencode/command/` for team sharing
9. **Version control**: Commit converted commands to git for team consistency
10. **Keep it simple**: Commands should be focused and single-purpose

## Related Commands

- View commands: Check `.opencode/command/` or `~/.config/opencode/command/`
- Test command: Use `/command-name` in OpenCode TUI
- Built-in commands: `/help`, `/init`, `/undo`, `/redo`, `/share`

## References

- [OpenCode Commands Documentation](https://opencode.ai/docs/commands/)
- [Claude Code Slash Commands Documentation](https://code.claude.com/docs/en/slash-commands)
