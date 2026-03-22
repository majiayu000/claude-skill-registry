---
name: cc-linear
description: Execute atomic Linear operations via one-shot `cc` session with Linear MCP. Use for creating issues, updating status, adding comments, querying tasks. CRITICAL: Each command performs ONE operation only. For multi-step workflows (update status THEN add comment), execute SEPARATE `cc` commands sequentially. Spawned sessions cannot ask clarifying questions - prompts must be self-contained and unambiguous. See OPERATIONS.md for patterns and anti-patterns.
---

# CC Linear

Interact with Linear task management via `cc` alias — spawns a one-shot Claude Code session with Linear MCP connected.

## When to Use

- Create Linear issues from current session
- Update issue status (In Progress, In Review, Done, etc.)
- Query issue details or search issues
- Add comments to issues
- Any Linear operation without leaving current context

## Critical: One-Shot Limitation

```
Main Chat → Bash → cc session (one-shot) → Results back
                        ↑
                  NO FEEDBACK LOOP
```

**The Problem:**
- Spawned session executes prompt and returns output
- If it asks a clarifying question → you see it but CANNOT respond
- `--dangerously-skip-permissions` removes permission prompts, but NOT clarification questions

**The Solution: Self-Contained Prompts**

All prompts MUST be:
- **Concrete** — specify exactly what to do
- **Self-contained** — include ALL required parameters
- **Unambiguous** — no room for interpretation

## Standard Syntax: Always Use Pipe

**All prompts go through pipe** — consistent, reliable, no escaping issues.

```bash
echo 'Your prompt here' | cc --mcp-config .claude/mcp/linear.json -p -
```

**Why pipe:**
- No shell escaping issues with quotes, `$`, backticks
- No command line length limits
- Works identically for short and long prompts
- Single pattern to remember

**For multiline prompts use heredoc:**
```bash
cat <<'EOF' | cc --mcp-config .claude/mcp/linear.json -p -
Create Linear issue in WYT team:
- title: "Add logout button"
- description: "Add logout functionality to settings page"
- priority: 3
Return the created issue ID.
EOF
```

## Linear Operations

### Get Issues

```bash
# Top tasks from project
echo 'Get top 5 tasks from WYT project ordered by priority' | cc --mcp-config .claude/mcp/linear.json -p -

# Specific issue details
echo 'Get details for issue WYT-66' | cc --mcp-config .claude/mcp/linear.json -p -

# Search issues
echo 'Search WYT issues containing "authentication"' | cc --mcp-config .claude/mcp/linear.json -p -
```

### Create Issue

```bash
cat <<'EOF' | cc --mcp-config .claude/mcp/linear.json -p -
Create Linear issue in WYT team:
- title: "Add user logout functionality"
- description: "Implement logout button in settings page that clears session and redirects to login"
- priority: 3 (Normal)
Return the created issue ID and URL.
EOF
```

### Update Issue Status

```bash
# Update to In Progress
echo 'Update WYT-66 status to "In Progress". Do NOT modify description.' | cc --mcp-config .claude/mcp/linear.json -p -

# Update to In Review
echo 'Update WYT-66 status to "In Review". Do NOT modify description.' | cc --mcp-config .claude/mcp/linear.json -p -

# Update to Done
echo 'Update WYT-66 status to "Done". Do NOT modify description.' | cc --mcp-config .claude/mcp/linear.json -p -
```

### Add Comment

```bash
cat <<'EOF' | cc --mcp-config .claude/mcp/linear.json -p -
Add comment to WYT-66:
"Implementation completed. PR #123 ready for review.
- Added logout endpoint
- Updated auth middleware
- Tests passing"
EOF
```

## Critical: Separate Operations

**NEVER combine status updates and comments in one prompt!**

The cc session may interpret "Add comment" as modifying the description field, causing loss of the original task description.

### WRONG - Combined prompt:
```bash
# DO NOT DO THIS - causes description overwrite
echo 'Update WYT-66: 1. Set status to In Review 2. Add comment: Implementation completed' | cc --mcp-config .claude/mcp/linear.json -p -
```

### CORRECT - Separate prompts:
```bash
# First: Update status only
echo 'Update WYT-66 status to "In Review". Do NOT modify description.' | cc --mcp-config .claude/mcp/linear.json -p -

# Second: Add comment separately
echo 'Add comment to WYT-66: "Implementation completed. PR ready for review."' | cc --mcp-config .claude/mcp/linear.json -p -
```

## Configuration

### WYT Project Settings

```yaml
Team ID: WYT
```

### Task States (in order)

```yaml
- Backlog
- Ready for Implementation
- In Progress
- In Review
- Needs Fixes
- Ready to Merge
- Done
- Canceled
```

### Priority Levels

```yaml
0: None
1: Urgent
2: High
3: Normal (default)
4: Low
```

## Usage in Commands

When commands (like `/ct`, `/si`, `/sr`) need Linear operations:

```bash
cat <<'EOF' | cc --mcp-config .claude/mcp/linear.json -p -
Create Linear issue in WYT:
- title: "[Task Title]"
- description: "[Full description with context, requirements, acceptance criteria]"
- priority: [0-4]
Return the created issue ID and URL.
EOF
```

### Template for Any Operation

```bash
cat <<'EOF' | cc --mcp-config .claude/mcp/linear.json -p -
ACTION: [create_issue | update_issue | add_comment | get_issue | search_issues]

TARGET: [issue ID if applicable, e.g., WYT-66]

PARAMETERS:
- team: WYT
- [action-specific params...]

CONSTRAINTS:
- Do NOT modify fields other than [specified field]

RETURN: [what you need back]
EOF
```

## Important Notes

1. **MCP Config Path**: Always use `.claude/mcp/linear.json`
2. **Working Directory**: Run from project root
3. **No Session Context**: Spawned session knows nothing about parent conversation
4. **Auth**: Linear MCP uses SSO — ensure authenticated in browser first
5. **Pipe + `-p -`**: The `-` tells cc to read prompt from stdin

## Troubleshooting

### Empty or Unexpected Output

Prompt was too vague. Add team ID, full description, exact parameters.

### MCP Connection Failed

```bash
echo 'List all available Linear MCP tools' | cc --mcp-config .claude/mcp/linear.json -p -
```

### Authentication Issues

Linear MCP uses browser SSO. Open Linear in browser, ensure logged in, then retry.

## References

See `references/linear-mcp-tools.md` for detailed MCP tool signatures.
